"""Shell acceptance through public CLIs and boundary effects, using disposable files."""

import hashlib
import json
import shutil
import tempfile
import unittest
from pathlib import Path

import support as S

ROOT = S.ROOT


class ShellAutomationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="Ox shell paths ")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def report(self, value, parser="gitleaks", raw=False):
        p = self.root / "report.json"
        p.write_text(value if raw else json.dumps(value))
        return S.run(
            [
                "/bin/bash",
                str(ROOT / "scripts/security/analyzers/check-report.sh"),
                "--parser",
                parser,
                str(p),
            ],
            capture_output=True,
        )

    def test_json_duplicate_container_and_nonfinite_rejected(self):
        for text in (
            '{"a":1,"a":2}',
            '{"a":{"x":1},"a":{"y":2}}',
            '{"a":{},"a":[]}',
            '[{"a":1,"a":2}]',
            "NaN",
            "Infinity",
            "{} {}",
            "",
        ):
            with self.subTest(text=text):
                self.assertEqual(self.report(text, raw=True).returncode, 2)
        for text in (
            "[]",
            "[{},{}]",
            '[{"a":{"x":1,"y":2},"b":3}]',
            '[{"a":1},{"a":2}]',
        ):
            with self.subTest(valid=text):
                self.assertIn(self.report(text, raw=True).returncode, (0, 1))

    def test_all_report_schemas_clean_findings_and_malformed(self):
        cases = {
            "gitleaks": ([], [{}]),
            "shellcheck": ([], [{}]),
            "pssa": ([], [{}]),
            "opengrep": (
                {"results": [], "errors": [], "paths": {"scanned": ["x.rs"]}},
                None,
            ),
            "osv": ({"results": [{"packages": [{"package": {"name": "x"}}]}]}, None),
            "sarif": (
                {
                    "runs": [
                        {
                            "tool": {},
                            "invocations": [{"executionSuccessful": True}],
                            "results": [],
                        }
                    ]
                },
                None,
            ),
            "json-findings": (
                {"complete": True, "findings": []},
                {"complete": True, "findings": [{}]},
            ),
            "syft": ({"artifacts": [{}], "descriptor": {}}, None),
            "grype": (
                {"matches": [], "descriptor": {}, "source": {}},
                {"matches": [{}], "descriptor": {}, "source": {}},
            ),
            "yara": (
                {"version": "1", "matches": []},
                {"version": "1", "matches": [{"rule": "x", "file": "y"}]},
            ),
        }
        for parser, (clean, findings) in cases.items():
            with self.subTest(parser=parser):
                self.assertEqual(self.report(clean, parser).returncode, 0)
                if findings is not None:
                    self.assertEqual(self.report(findings, parser).returncode, 1)
                self.assertEqual(self.report(None, parser).returncode, 2)
        native = {
            "audit": {
                "vulnerabilities": {"list": [], "count": 0},
                "database": {},
                "lockfile": {},
            },
            "bandit": {"errors": [], "metrics": {"x": {}}, "results": []},
            "ruff": [],
            "machete": {"crates": []},
            "trivy": {"SchemaVersion": 2, "Results": [{}]},
            "geiger": {
                "packages": [{}],
                "packages_without_metrics": [],
                "used_but_not_scanned_files": [],
            },
        }
        for parser, clean in native.items():
            p = self.root / "native.json"
            p.write_text(json.dumps(clean))
            with self.subTest(parser=parser):
                self.assertEqual(
                    S.assess(parser, 0, p)[0],
                    "recorded" if parser == "geiger" else "passed",
                )
                p.write_text("{}")
                with S.rejected(self):
                    S.assess(parser, 0, p)

    def test_all_checks_plan_offline_and_no_writes(self):
        names = "gitleaks osv opengrep audit bandit machete ruff deny history coverage geiger trivy sbom grype malware shellcheck".split()
        for name in names:
            run = S.run(
                [
                    "/bin/bash",
                    str(ROOT / "scripts/checks/run.sh"),
                    "--check",
                    name,
                    "--plan",
                    "--root",
                    str(self.root),
                ],
                capture_output=True,
            )
            with self.subTest(check=name):
                self.assertEqual(run.returncode, 0, run.stderr)
                self.assertEqual(json.loads(run.stdout)["check"], name)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_tree_digest_matches_historical_format_hidden_unicode_and_spaces(self):
        for name in ["z", ".hidden", "á name", "sub/a\nb"]:
            p = self.root / name
            p.parent.mkdir(exist_ok=True)
            p.write_text(name)
        rows = {
            p.relative_to(self.root).as_posix(): S.digest(p)
            for p in self.root.rglob("*")
            if p.is_file()
        }
        expected = hashlib.sha256(
            json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        self.assertEqual(S.tree_identity(self.root), expected)
        (self.root / "alias").symlink_to("/etc/passwd")
        with S.rejected(self):
            S.tree_identity(self.root)

    def test_snapshot_change_and_root_symlink_rejected(self):
        (self.root / "scripts").mkdir()
        p = self.root / "scripts/a.sh"
        p.write_text("exit 0\n")
        out = self.root / "out"
        out.mkdir()
        S.source_copy(self.root, out)
        p.write_text("exit 1\n")
        with S.rejected(self):
            S.shell('ROOT=$OX_TEST_ROOT; verify_inputs "$1"', out, root=self.root)
        (self.root / "application").symlink_to("/tmp", target_is_directory=True)
        out2 = self.root / "out2"
        out2.mkdir()
        with S.rejected(self):
            S.source_copy(self.root, out2)

    def test_summarizer_preserves_failure_and_rejects_invalid_state(self):
        p = self.root / "results.json"
        row = {"check": "a|b", "state": "failed", "exit_code": 23}
        p.write_text(
            json.dumps(
                {
                    "results": [row],
                    "product_acceptance": False,
                    "omitted": [{"check": "x"}],
                }
            )
        )
        argv = ["/bin/bash", str(ROOT / "scripts/reports/summarize.sh"), str(p)]
        run = S.run(argv, capture_output=True)
        self.assertEqual(run.returncode, 2, run.stderr)
        self.assertIn(b"Omitted:", run.stdout)
        row["state"] = "invented"
        p.write_text(json.dumps({"results": [row], "product_acceptance": False}))
        self.assertEqual(S.run(argv, capture_output=True).returncode, 2)

    def test_shell_layout_and_syntax(self):
        for p in (ROOT / "scripts").rglob("*"):
            if p.suffix == ".py":
                self.assertIn("tests", p.relative_to(ROOT / "scripts").parts)
            if p.suffix == ".sh":
                run = S.run(["/bin/bash", "-n", str(p)], capture_output=True)
                self.assertEqual(run.returncode, 0, (str(p), run.stderr))
                self.assertNotRegex(p.read_bytes(), rb"python3\s+-(?:c(?:\s|$)|\s)")

    def test_generated_scanner_snapshots_are_transient_not_source_documents(self):
        import sys

        sys.path.insert(0, str(ROOT / "tools/governance/scripts"))
        from governance_support import transient

        self.assertTrue(transient(Path(".local/logs/run-ID/source/README.md")))
        self.assertFalse(transient(Path("docs/README.md")))
        self.assertFalse(transient(Path("docs/.local/reference.md")))

    def test_root_ignore_files_require_review_even_for_code_scans(self):
        (self.root / "scripts").mkdir()
        (self.root / "scripts/test.py").write_text("pass\n")
        (self.root / ".semgrepignore").write_text("scripts/\n")
        out = self.root / "out"
        out.mkdir()
        with S.rejected(self, message="requires review"):
            S.source_copy(self.root, out, True)

    def test_native_adapters_execute_controlled_tool_and_record_identity(self):
        import datetime as dt
        import sys

        shutil.copytree(ROOT / "scripts", self.root / "scripts")
        app = self.root / "application"
        app.mkdir()
        for name, text in {
            "Cargo.toml": '[workspace]\nmembers=["crates/fixture"]\n',
            "Cargo.lock": "version = 4\n",
            "rust-toolchain.toml": '[toolchain]\nchannel="1.99.1"\n',
        }.items():
            (app / name).write_text(text)
        crate = app / "crates/fixture"
        crate.mkdir(parents=True)
        (crate / "Cargo.toml").write_text(
            '[package]\nname="fixture"\nversion="0.1.0"\n'
        )
        (crate / "fixture.rs").write_text("fn main() {}\n")
        binary = self.root / "bin"
        binary.mkdir()
        for name in ["llvm-cov", "llvm-profdata"]:
            p = self.root / "lib/rustlib/fixture/bin" / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.touch()
        registry = {}
        for name in ["osv", "rustsec", "trivy", "grype"]:
            d = self.root / ".cache/ox/security" / name
            d.mkdir(parents=True)
            (d / "data").write_text(name)
            registry[name] = {
                "path": str(d.relative_to(self.root)),
                "sha256": S.tree_identity(d),
                "valid_until": (dt.datetime.now(dt.UTC).date() + dt.timedelta(days=1)).isoformat(),
                "source": "controlled fixture",
                "license": "fixture",
            }
        (self.root / ".cache/ox/security/datasets.json").write_text(json.dumps(registry))
        (self.root / ".cache/ox/security/deny.toml").write_text("[licenses]\nallow=[]\n")
        tools = {
            "gitleaks": "gitleaks",
            "osv": "osv-scanner",
            "opengrep": "opengrep",
            "audit": "cargo-audit",
            "bandit": "bandit",
            "machete": "cargo-machete",
            "ruff": "ruff",
            "deny": "cargo-deny",
            "history": "gitleaks",
            "coverage": "cargo-llvm-cov",
            "geiger": "cargo-geiger",
            "trivy": "trivy",
            "sbom": "syft",
            "grype": "grype",
            "malware": "yr",
            "shellcheck": "shellcheck",
        }
        body = """import sys,json,os
from pathlib import Path
n=Path(sys.argv[0]).name
if n=="rustup": print(str(Path(__file__).with_name("cargo")));sys.exit(0)
if n=="cargo":
 root=Path(os.environ["FIXTURE_ROOT"])
 members=["fixture","second"] if os.environ.get("GEIGER_INCOMPLETE") else ["fixture"]
 print(json.dumps({"workspace_members":members,"packages":[{"id":m,"manifest_path":str(root/"application/crates"/m/"Cargo.toml")} for m in members]}));sys.exit(0)
if n=="git":print("false");sys.exit(0)
if "--version" in sys.argv or "version" in sys.argv:print("0.9.2" if n=="cargo-machete" else "controlled tool 1");sys.exit(0)
if n=="cargo-geiger":
 assert os.environ["RUST_MIN_STACK"]=="16777216"
 assert "--all-features" in sys.argv
if n=="gitleaks":Path(sys.argv[sys.argv.index("--report-path")+1]).write_text("[]");sys.exit(0)
if n=="cargo-llvm-cov":Path(sys.argv[sys.argv.index("--output-path")+1]).write_text("SF:fixture.rs\\nend_of_record\\n");sys.exit(0)
if n=="cargo-machete":
 print("cargo-machete didn't find any unused dependencies in this directory. Good job!")
 print("Analyzing dependencies of crates in ....\\nDone!",file=sys.stderr);sys.exit(0)
if n=="cargo-deny":
 print(json.dumps({"type":"summary","fields":{k:{"errors":0,"warnings":0,"notes":0,"helps":0} for k in ("bans","licenses","sources")}}),file=sys.stderr);sys.exit(0)
reports={"osv-scanner":{"results":[{"packages":[{"package":{"name":"fixture"}}]}]},
 "cargo-audit":{"database":{},"lockfile":{},"vulnerabilities":{"list":[],"count":0}},
 "bandit":{"errors":[],"metrics":{"fixture":{}},"results":[]},
 "cargo-machete":{"crates":[]},"ruff":[],"shellcheck":[],
 "cargo-geiger":{"packages":[{}],"packages_without_metrics":[],"used_but_not_scanned_files":[]},
 "trivy":{"SchemaVersion":2,"Results":[{}]},"syft":{"descriptor":{},"artifacts":[{}]},
 "grype":{"matches":[],"source":{},"descriptor":{}},"yr":{"version":"1","matches":[]}}
if n=="opengrep":
 source=Path(sys.argv[-1]);print(json.dumps({"results":[],"errors":[],"paths":{"scanned":[str(p) for p in source.rglob("*") if p.suffix in (".py",".rs")]}}))
else:
 if n=="cargo-geiger" and os.environ.get("GEIGER_INCOMPLETE") and "/fixture/" in sys.argv[-1]:
  reports[n]["used_but_not_scanned_files"]=["generated.rs"]
 print(json.dumps(reports[n]))
"""
        for name in {*tools.values(), "rustup", "cargo", "git"}:
            p = binary / name
            p.write_text("#!" + sys.executable + "\n" + body)
            p.chmod(0o755)
        catalog_path = self.root / "scripts/config/automation.json"
        catalog = json.loads(catalog_path.read_text())
        catalog["checks"]["geiger"]["executable"] = {
            "path": "bin/cargo-geiger",
            "sha256": S.digest(binary / "cargo-geiger"),
        }
        catalog_path.write_text(json.dumps(catalog))
        env = dict(
            S.environment(), PATH=str(binary) + ":/usr/bin:/bin", FIXTURE_ROOT=str(self.root),
            CARGO_HOME=str(self.root / "cargo-home"), OX_CARGO_BIN=str(binary),
        )
        # Database scanners are covered by toolbox boundary tests.
        for name in (n for n in tools if n in ("audit", "deny", "machete", "coverage", "geiger")):
            before = S.published_assessments(self.root)
            run = S.run(
                [
                    "/bin/bash",
                    str(self.root / "scripts/checks/run.sh"),
                    "--check",
                    name,
                ],
                env=env,
                capture_output=True,
            )
            with self.subTest(check=name):
                self.assertEqual(run.returncode, 0, run.stderr)
                row = S.current_assessment(self.root, before)
                self.assertEqual(row["tool_exit_code"], 0)
                self.assertEqual(row["tool"]["sha256"], S.digest(binary / tools[name]))
                self.assertEqual(
                    row["state"],
                    "recorded" if name in ("coverage", "geiger", "sbom") else "passed",
                )

        # An incomplete first member must neither approve nor hide later members.
        second = app / "crates/second"
        second.mkdir()
        (second / "Cargo.toml").write_text('[package]\nname="second"\nversion="0.1.0"\n')
        (second / "lib.rs").write_text("pub fn second() {}\n")
        before = S.published_assessments(self.root)
        run = S.run(
            ["/bin/bash", str(self.root / "scripts/checks/run.sh"), "--check", "geiger"],
            env=dict(env, GEIGER_INCOMPLETE="1"), capture_output=True,
        )
        self.assertEqual(run.returncode, 2, run.stderr)
        row = S.current_assessment(self.root, before)
        self.assertEqual(row["state"], "error")
        self.assertEqual([m["state"] for m in row["member_results"]], ["error", "recorded"])
        self.assertEqual(row["tool_exit_code"], 0)
        self.assertIn("all workspace members attempted", row["reason"])


if __name__ == "__main__":
    unittest.main()
