"""Behavioral scanner contracts using controlled executables; no real scanner claims."""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts/tests"))
import support as S

ROOT = Path(__file__).resolve().parents[3]


class SecurityQualityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="Ox scanner spaces ")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.bin = self.root / "bin"
        self.bin.mkdir()
        (self.bin / "python3").symlink_to(sys.executable)
        (self.bin / "dirname").symlink_to(shutil.which("dirname"))
        shutil.copytree(
            ROOT / "scripts",
            self.root / "scripts",
            ignore=shutil.ignore_patterns("__pycache__"),
        )
        for rel in (
            "AGENTS.md",
            "sdd/tools/validate.py",
            "tools/governance/scripts/check-ox.py",
            "tools/governance/scripts/run-tests.py",
        ):
            p = self.root / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text("# fixture\n")
        p = self.root / "application/main.rs"
        p.parent.mkdir()
        p.write_text("fn main() {}\n")
        (self.root / "application/Cargo.toml").write_text("[workspace]\nmembers=[]\n")
        shutil.copy2(
            ROOT / "application/rust-toolchain.toml",
            self.root / "application/rust-toolchain.toml",
        )
        (self.root / "application/Cargo.lock").write_text("version = 4\n")
        self.env = dict(
            os.environ,
            PATH=str(self.bin) + ":/usr/bin:/bin",
            PYTHONDONTWRITEBYTECODE="1",
            TOOLBOX_BIN=str(self.bin / "toolbox"),
        )

        # Simulated central exec boundary; only for consumer contract tests.
        self.fake(
            "toolbox",
            r"""a=sys.argv[1:]
assert a[0]=="exec" and "--" in a
def val(k): return a[a.index(k)+1]
args=a[a.index("--")+1:]
root=val("--project-root");out=val("--results")
args=[x.replace("/project",root).replace("/out",out) for x in args]
name=val("--tool"); binary=Path(__file__).with_name("yr" if name=="yara-x" else name)
import subprocess
if binary.exists():
 run=subprocess.run([str(binary),*args]);code=run.returncode; outcome="native"
else: code=125;outcome="infrastructure"
Path(val("--diagnostic-file")).write_text(json.dumps({"tool":name,"version":"fixture","image":"sha256:"+"a"*64,"native_exit_code":code if outcome=="native" else None,"outcome":outcome,"cleanup":"removed"}))
sys.exit(code)""",
        )

    def fake(self, name, body):
        p = self.bin / name
        p.write_text(
            "#!"
            + sys.executable
            + '\nimport sys,json,os\nfrom pathlib import Path\nif "--version" in sys.argv:\n print("fixture tool 1.0");sys.exit(0)\n'
            + body
            + "\n"
        )
        p.chmod(0o755)

    def call(self, name):
        return subprocess.run(
            [
                "/bin/bash",
                str(self.root / "scripts/automate.sh"),
                "--root",
                str(self.root),
                "--scope",
                "security",
                "--check",
                name,
            ],
            cwd="/tmp",
            env=self.env,
            capture_output=True,
        )

    def observation(self, name):
        return json.loads(
            next(
                (self.root / ".local/logs").glob("*/*--" + name + "--assessment.json.log")
            ).read_text()
        )

    def test_real_wrapper_spaces_clean_and_findings(self):
        self.fake(
            "gitleaks",
            'assert "--redact=100" in sys.argv\nassert not any("baseline" in a for a in sys.argv)\np=Path(sys.argv[sys.argv.index("--report-path")+1]);p.write_text(json.dumps([{"RuleID":"fixture","Secret":"REDACTED"}]))\nsys.exit(10)',
        )
        wrapper = self.root / "scripts/automate.sh"
        run = subprocess.run(
            [
                "/bin/bash",
                str(wrapper),
                "--scope",
                "security",
                "--check",
                "gitleaks",
                "--root",
                str(self.root),
            ],
            cwd="/tmp",
            env=self.env,
            capture_output=True,
        )
        self.assertEqual(run.returncode, 1, run.stderr)
        result = self.observation("gitleaks")
        self.assertEqual(result["state"], "findings")
        self.assertEqual(result["tool_exit_code"], 10)
        report = json.loads(
            next((self.root / ".local/logs").glob("*/*--results.json.log")).read_text()
        )
        self.assertEqual(report["results"][0]["state"], "findings")
        self.assertIn("application/main.rs", result["inputs"])
        self.assertFalse(report["product_acceptance"])

    def test_missing_native_tool_blocks_without_installing(self):
        result = self.call("malware")
        self.assertEqual(result.returncode, 2)
        row = self.observation("malware")
        self.assertEqual(row["state"], "error")
        self.assertIsNone(row["tool_exit_code"])
        self.assertIn("Executor infrastructure", row["reason"])

    def test_osv_central_fixture_still_requires_age_evidence(self):
        marker = self.root / "native-osv-executed"
        self.fake("osv-scanner", "Path(" + repr(str(marker)) + ").touch()")
        run = self.call("osv")
        self.assertEqual(run.returncode, 2, run.stderr)
        row = self.observation("osv")
        self.assertEqual(row["state"], "error")
        self.assertIn("central database metadata", row["reason"])
        self.assertTrue(marker.exists())
        self.assertFalse((self.root / ".local/security").exists())
        self.assertEqual(row["tool_exit_code"], 0)

    def test_data_expiry_digest_and_escape_are_denied(self):
        base = self.root / ".cache/ox/security"
        base.mkdir(parents=True)
        d = base / "data"
        d.mkdir()
        (d / "x").write_text("x")
        row = {
            "path": ".cache/ox/security/data",
            "sha256": S.tree_identity(d),
            "valid_until": "2000-01-01",
            "source": "fixture",
            "license": "fixture",
        }
        reg = base / "datasets.json"
        reg.write_text(json.dumps({"osv": row}))
        with self.assertRaisesRegex(ValueError, "expired"):
            S.dataset(self.root, "osv")
        row["valid_until"] = "2999-01-01"
        row["sha256"] = "0" * 64
        reg.write_text(json.dumps({"osv": row}))
        with self.assertRaisesRegex(ValueError, "digest"):
            S.dataset(self.root, "osv")
        row["path"] = "../outside"
        reg.write_text(json.dumps({"osv": row}))
        with self.assertRaisesRegex(ValueError, "relative"):
            S.dataset(self.root, "osv")

    def test_partial_and_suppressed_sast_never_passes(self):
        for mutation in ("errors", "skip", "ignored", "empty"):
            p = self.root / "report.json"
            value = {"results": [], "errors": [], "paths": {"scanned": ["main.rs"]}}
            if mutation == "errors":
                value["errors"] = [{"type": "parse"}]
            elif mutation == "skip":
                value["paths"]["skipped"] = [{"path": "main.rs"}]
            elif mutation == "ignored":
                value["results"] = [{"check_id": "rule", "extra": {"is_ignored": True}}]
            else:
                value["paths"]["scanned"] = []
            p.write_text(json.dumps(value))
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                S.assess("opengrep", 0, p)

    def test_tool_error_keeps_raw_exit_and_output(self):
        self.fake(
            "opengrep",
            'sys.stdout.buffer.write(b"invalid\\x00");sys.stderr.write("fixture failure\\n");sys.exit(23)',
        )
        run = self.call("opengrep")
        self.assertNotEqual(run.returncode, 0)
        obs = self.observation("opengrep")
        self.assertEqual(obs["tool_exit_code"], 23)
        self.assertEqual(obs["state"], "error")
        log = next((self.root / ".local/logs").glob("*/*--opengrep--tool--stdout.log.log"))
        self.assertEqual(log.read_bytes(), b"invalid\x00")

    def test_snapshot_preserves_source_and_rejects_alias(self):
        d = self.root / "out"
        d.mkdir()
        source, rows = S.source_copy(self.root, d, True)
        self.assertEqual(
            rows["application/main.rs"], S.digest(self.root / "application/main.rs")
        )
        (source / "application/main.rs").write_text("changed copy")
        self.assertEqual(
            (self.root / "application/main.rs").read_text(), "fn main() {}\n"
        )
        (self.root / "application/link.rs").symlink_to("/etc/passwd")
        d2 = self.root / "out2"
        d2.mkdir()
        with self.assertRaisesRegex(ValueError, "source symlink"):
            S.source_copy(self.root, d2, True)

    def test_coverage_and_sbom_are_measurements_not_gates(self):
        report = self.root / "cov"
        report.write_text("SF:src/main.rs\nDA:1,1\nend_of_record\n")
        self.assertEqual(S.assess("coverage", 0, report)[0], "recorded")
        report.write_text("")
        with self.assertRaises(ValueError):
            S.assess("coverage", 0, report)
        report.write_text(
            json.dumps({"artifacts": [{"name": "fixture"}], "descriptor": {}})
        )
        self.assertEqual(S.assess("sbom", 0, report)[0], "recorded")

    def test_duplicate_report_and_exceptions_expiry(self):
        from support import exceptions, read_json

        p = self.root / "duplicate.json"
        p.write_text('{"results":[],"results":[]}')
        with self.assertRaises(ValueError):
            read_json(p)
        row = {
            k: "fixture"
            for k in (
                "id",
                "tool",
                "finding",
                "component",
                "owner",
                "reason",
                "control",
            )
        }
        row.update(reviewed="2000-01-01", expires="2000-01-02")
        with self.assertRaises(ValueError):
            exceptions([row])
        self.assertFalse(exceptions([])["applied"])

    def test_all_wrappers_plan_without_tools(self):
        for wrapper in [self.root / "scripts/automate.sh"]:
            run = subprocess.run(
                [
                    "/bin/bash",
                    str(wrapper),
                    "--scope",
                    "security",
                    "--root",
                    str(self.root),
                    "--plan",
                ],
                cwd="/tmp",
                env=self.env,
                capture_output=True,
            )
            self.assertEqual(run.returncode, 0, (str(wrapper), run.stderr))
            self.assertTrue(json.loads(run.stdout))
        self.assertFalse((self.root / ".local").exists())

    def test_geiger_covers_virtual_workspace_members_and_rejects_escape(self):
        manifests = S.member_manifests(ROOT / "application")
        self.assertEqual(len(manifests), 16)
        self.assertEqual(
            {p.parent.name for p in manifests},
            {p.parent.name for p in (ROOT / "application/crates").glob("*/Cargo.toml")},
        )
        workspace = self.root / "escape-workspace"
        workspace.mkdir()
        (workspace / "Cargo.toml").write_text('[workspace]\nmembers=["../outside"]\n')
        with self.assertRaises(ValueError):
            S.member_manifests(workspace)

    def test_sast_zero_exit_with_unscanned_sources_is_error(self):
        self.fake(
            "opengrep",
            'print(json.dumps({"results":[],"errors":[],"paths":{"scanned":["different.rs"]}}))',
        )
        result = self.call("opengrep")
        self.assertEqual(result.returncode, 2, result.stderr)
        obs = self.observation("opengrep")
        self.assertEqual(obs["state"], "error")
        self.assertEqual(obs["tool_exit_code"], 0)
        self.assertIn("omitted selected", obs["reason"])

    def test_missing_report_is_not_clean_gitleaks(self):
        self.fake("gitleaks", 'print("[]")')
        result = self.call("gitleaks")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(self.observation("gitleaks")["tool_exit_code"], 0)

    def test_missing_license_policy_blocks_even_with_tool(self):
        (self.root / "scripts/config/native/cargo-deny/deny.toml").unlink()
        self.fake(
            "cargo-deny", 'raise AssertionError("scan must not run without policy")'
        )
        self.fake("rustup", 'print("/usr/bin/true")')
        (self.root / "application/rust-toolchain.toml").write_text(
            '[toolchain]\nchannel="1.99.1"\n'
        )
        result = subprocess.run(
            [
                "/bin/bash",
                str(self.root / "scripts/automate.sh"),
                "--scope",
                "quality",
                "--check",
                "deny",
            ],
            cwd="/tmp",
            env=self.env,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 3, result.stderr)
        obs = self.observation("deny")
        self.assertIn("deny.toml", obs["reason"])
        self.assertIsNone(obs["tool_exit_code"])

    def test_security_successor_rejects_previous_authority_bytes(self):
        sys.path.insert(0, str(ROOT / "tools/governance/scripts"))
        import closure_revision as C

        registry = self.root / C.SECURITY_REGISTRY
        registry.parent.mkdir(parents=True)
        shutil.copy2(ROOT / C.SECURITY_REGISTRY, registry)
        for row in json.loads(registry.read_text())["records"]:
            target = self.root / row["previous"]
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / row["previous"], target)
        shell_registry = self.root / C.SHELL_REGISTRY
        shell_registry.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / C.SHELL_REGISTRY, shell_registry)
        for row in json.loads(shell_registry.read_text())["records"]:
            target = self.root / row["previous"]
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / row["previous"], target)
        current = (
            ROOT / "docs/validation/scripts-shell-refactor/before/README.md.bin"
        ).read_bytes()
        (self.root / "README.md").write_bytes(current)
        before = C.security_predecessor(self.root, "README.md", current)
        self.assertNotEqual(before, current)
        (self.root / "README.md").write_bytes(before)
        with self.assertRaisesRegex(ValueError, "downgrade"):
            C.security_predecessor(self.root, "README.md", before)

    def test_grype_has_no_inherited_severity_threshold_or_error_suppression(self):
        argv = json.loads(
            S.shell(
                'ROOT=$OX_TEST_ROOT; name=grype; check_properties "$name"; native_command "{source}"; json_args "${NATIVE[@]}"',
                root=self.root,
            )
        )
        self.assertNotIn("--fail-on", argv)
        report = self.root / "grype.json"
        report.write_text(
            json.dumps({"matches": [{"fixture": True}], "descriptor": {}, "source": {}})
        )
        self.assertEqual(S.assess("grype", 0, report)[:2], ("findings", 1))
        self.assertEqual(S.assess("grype", 2, report)[:2], ("failed", 2))
