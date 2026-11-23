"""Consumer exec contract tests. The fake executor does not homologate scanners."""

import json
import sys
import tempfile
import unittest
from pathlib import Path

import support as S


class Backends(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="ox native ; $ space ")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        S.copy_scripts_fixture(self.root)
        (self.root / "scripts/probe.py").write_text('print("fixture")\n')
        (self.root / "application").mkdir()
        (self.root / "application/Cargo.lock").write_text("version = 4\n")
        self.cli = self.root / "executor with spaces"
        self.cli.write_text(
            "#!"
            + sys.executable
            + "\n"
            + r"""
import sys, json, os
from pathlib import Path
a=sys.argv[1:]; assert a[0]=='exec'
def value(k): return a[a.index(k)+1]
tool=value('--tool'); root=Path(value('--project-root')); out=Path(value('--results'))
assert '--project-write' not in a and '--network' not in a and '--mount' not in a
assert '--timeout' in a and '--' in a
native=a[a.index('--')+1:]; assert native
mode=os.environ.get('FIXTURE_MODE','clean')
count=1 if mode in ('finding','old-upstream-finding') else 0
code=0
if tool=='gitleaks':
 assert '--redact=100' in native and '--ignore-gitleaks-allow' in native
 if native[0]=='git': assert (root/'.git/objects').is_dir() and '--log-opts=--all' in native
 (out/'report.json').write_text(json.dumps([{}]*count)); code=10 if count else 0
 report=[]
elif tool in ('ruff','shellcheck'):
 assert any(x.startswith('/project/scripts/') for x in native)
 if tool=='ruff': assert '--ignore-noqa' in native and '--no-fix' in native
 if tool=='shellcheck': assert '/project/scripts/security/prepare-datasets.sh' in native and '/project/scripts/toolbox.sh' in native
 report=[{'code':'F821'}]*count; code=1 if count else 0
elif tool=='bandit':
 assert '--ignore-nosec' in native and '--ini' in native and '--quiet' in native
 report={'errors':[], 'results':[{}]*count, 'metrics':{'/project/'+str(p.relative_to(root)):{} for p in root.rglob('*.py')}}; code=1 if count else 0
elif tool=='opengrep':
 assert '--disable-nosem' in native and '--no-git-ignore' in native
 report={'results':[{'check_id':'fixture'}]*count,'errors':[],'paths':{'scanned':['/project/'+str(p.relative_to(root)) for p in root.rglob('*') if p.suffix in ('.rs','.py')]}}; code=1 if count else 0
elif tool=='syft': report={'descriptor':{},'artifacts':[{}]}
elif tool=='yara-x': report={'version':'1.0.0','matches':[{'rule':'fixture','file':'fixture'}]*count}
elif tool=='grype': report={'descriptor':{},'source':{},'matches':[{}]*count}
elif tool=='osv-scanner':
 assert '--offline' in native and '--all-packages' in native
 report={'results':[{'packages':[{'package':{'name':'fixture'},'vulnerabilities':[{'id':'TEST-1'}]*count}]}]}; code=1 if count else 0
else: report={}
if mode=='exit-disagreement': code=0; report=[{'code':'F821'}]
if mode=='omit' and tool=='bandit': report['metrics']={'other':{}}
if mode=='invalid': print('{')
else: print(json.dumps(report))
if mode=='mutate': (root/'scripts/probe.py').write_text('changed')
if mode=='mode': (root/'scripts/probe.py').chmod(0o777)
if mode=='add': (Path(os.environ['FIXTURE_PROJECT'])/'scripts/new source.py').write_text('x=1')
d={'tool':tool,'version':'fixture','image':'sha256:'+'a'*64,'database':'b'*64,'native_exit_code':code,'outcome':'native','cleanup':'removed'}
if tool=='osv-scanner' and mode.startswith('old-upstream'):
 timestamp='2000-01-01T00:00:00Z'
 d['database_metadata']={'schema':1,'snapshot':'b'*64,'data_timestamp':timestamp,'timestamp_semantics':'oldest_required_source','sources':[{'url':'https://official.example','sha256':'c'*64,'data_timestamp':timestamp,'timestamp_semantics':'upstream_object_generation_created'}]*2}
if mode in ('timeout','cancelled','infrastructure'): d['outcome']=mode; d['native_exit_code']=None; code=124
if mode=='cleanup': d['cleanup']='failed'
if mode=='identity': d['image']='mutable'
if mode!='missing': Path(value('--diagnostic-file')).write_text(json.dumps(d))
sys.exit(code)
"""
        )
        self.cli.chmod(0o755)
        self.env = dict(
            S.environment(), TOOLBOX_BIN=str(self.cli), FIXTURE_PROJECT=str(self.root)
        )
        for k in ("OX_TOOLBOX_BIN", "OX_SCANNER_BACKEND"):
            self.env.pop(k, None)

    def run_check(self, name, mode="clean"):
        before = S.published_assessments(self.root)
        run = S.run(
            [
                "bash",
                str(S.ROOT / "scripts/checks/run.sh"),
                "--root",
                str(self.root),
                "--check",
                name,
            ],
            env=dict(self.env, FIXTURE_MODE=mode),
            capture_output=True,
        )
        row = S.current_assessment(self.root, before)
        return run, row

    def test_all_aliases_native_exits_and_measurements(self):
        for name in (
            "gitleaks",
            "ruff",
            "shellcheck",
            "bandit",
            "opengrep",
            "sbom",
            "malware",
            "grype",
        ):
            for mode in ("clean", "finding"):
                with self.subTest(name=name, mode=mode):
                    run, row = self.run_check(name, mode)
                    self.assertEqual(
                        row["state"],
                        "recorded"
                        if name == "sbom"
                        else ("findings" if mode == "finding" else "passed"),
                        (run.stderr, row),
                    )
                    self.assertFalse(row["product_acceptance"])
                    self.assertNotIn("argv", row)
                    self.assertEqual(row["backend_record"]["outcome"], "native")

    def test_native_plugin_discovery_preserves_path_priority(self):
        cargo = self.root / "cargo-home"
        selected = self.root / "selected plugins"
        path_bin = self.root / "path-bin"
        for directory in (cargo / "bin", selected, path_bin):
            directory.mkdir(parents=True)
            tool = directory / "cargo-geiger"
            tool.write_text("#!/bin/sh\nexit 99\n")
            tool.chmod(0o700)
        program = '''source "$1/lib/backends.sh"
EXECUTOR=native
TOOL=cargo-geiger
PATH=$2
CARGO_HOME=$3
unset OX_CARGO_BIN OX_TOOLBOX_BIN OX_SCANNER_BACKEND
if [[ $4 != unset ]]; then OX_CARGO_BIN=$4; fi
if select_backend; then json_args "$TOOL_BIN"; else json_args "$BACKEND_REASON"; fi
'''
        for path, override, expected in (
            (f"{path_bin}:/usr/bin:/bin", "unset", path_bin / "cargo-geiger"),
            ("/usr/bin:/bin", "unset", cargo / "bin/cargo-geiger"),
            ("/usr/bin:/bin", str(selected), selected / "cargo-geiger"),
            (f"{path_bin}:/usr/bin:/bin", str(selected), path_bin / "cargo-geiger"),
            (f"{path_bin}:/usr/bin:/bin", "", "OX_CARGO_BIN is empty; select the installed Cargo plugins"),
        ):
            with self.subTest(path=path, override=override):
                result = S.shell(program, S.ROOT / "scripts", path, cargo, override)
                self.assertEqual(json.loads(result), [str(expected)])

    def test_fail_closed_diagnostic_report_integrity(self):
        for mode in (
            "timeout",
            "cancelled",
            "infrastructure",
            "cleanup",
            "missing",
            "identity",
            "invalid",
            "mutate",
            "mode",
            "exit-disagreement",
        ):
            with self.subTest(mode=mode):
                run, row = self.run_check("ruff", mode)
                self.assertNotEqual(run.returncode, 0, row)
                self.assertEqual(row["state"], "error")

    def test_new_source_during_scan_rejected(self):
        run, row = self.run_check("ruff", "add")
        self.assertEqual(row["state"], "error", row)
        self.assertIn("inventory", row["reason"])

    def test_osv_old_upstream_provenance_passes_and_findings_still_fail(self):
        for mode, expected in (("old-upstream", "passed"), ("old-upstream-finding", "findings")):
            with self.subTest(mode=mode):
                run, row = self.run_check("osv", mode)
                self.assertEqual(row["state"], expected, (run.stderr, row))
                self.assertEqual(run.returncode, 0 if expected == "passed" else 1)
                self.assertFalse(row["product_acceptance"])

    def test_inventory_and_age_gaps(self):
        run, row = self.run_check("bandit", "omit")
        self.assertNotEqual(run.returncode, 0, row)
        for name in ("osv", "trivy"):
            run, row = self.run_check(name)
            self.assertIn("database metadata", row["reason"])
            self.assertNotEqual(run.returncode, 0)

    def test_history_requires_full_self_contained_git(self):
        S.run(["git", "init", str(self.root)], check=True, capture_output=True)
        run, row = self.run_check("history")
        self.assertEqual(run.returncode, 0, (run.stderr, row))
        (self.root / ".git/objects/info/alternates").write_text("/unavailable")
        run, row = self.run_check("history")
        self.assertNotEqual(run.returncode, 0)

    def test_wrapper_argv_path_empty_override_and_no_fallback(self):
        echo = self.root / "toolbox"
        echo.write_text(
            "#!"
            + sys.executable
            + "\nimport sys,json; print(json.dumps(sys.argv[1:]))\n"
        )
        echo.chmod(0o755)
        args = ["exec", "--", "space name", ";$(false)", "", "--"]
        wrapper = str(S.ROOT / "scripts/toolbox.sh")
        env = dict(self.env, PATH=str(self.root) + ":" + S.environment()["PATH"])
        env.pop("TOOLBOX_BIN")
        run = S.run([wrapper, *args], env=env, capture_output=True)
        self.assertEqual(json.loads(run.stdout), args)
        for invalid in ("", "/missing", str(self.root)):
            run = S.run(
                [wrapper, *args],
                env=dict(env, TOOLBOX_BIN=invalid),
                capture_output=True,
            )
            self.assertEqual(run.returncode, 125)
        native = self.root / "ruff"
        native.write_text('#!/bin/sh\ntouch "' + str(self.root / "native-ran") + '"\n')
        native.chmod(0o755)
        self.env["PATH"] = str(self.root) + ":" + S.environment()["PATH"]
        self.env["TOOLBOX_BIN"] = "/missing"
        run, row = self.run_check("ruff")
        self.assertNotEqual(run.returncode, 0)
        self.assertIsNone(row["tool_exit_code"])
        self.assertFalse((self.root / "native-ran").exists())
        self.assertEqual(row["runner_exit_code"], 125)
        self.assertIn("runner exit 125", row["reason"])
        self.assertIn("TOOLBOX_BIN", row["reason"])
        self.assertNotIn(b"awk:", run.stderr)

    def test_plans_use_central_transport_and_unavailable_local_has_no_command(self):
        for name in (
            "gitleaks",
            "osv",
            "ruff",
            "opengrep",
            "bandit",
            "trivy",
            "grype",
            "sbom",
            "malware",
            "shellcheck",
            "history",
        ):
            run = S.run(
                [
                    "bash",
                    str(S.ROOT / "scripts/checks/run.sh"),
                    "--root",
                    str(self.root),
                    "--check",
                    name,
                    "--plan",
                ],
                env=self.env,
                capture_output=True,
            )
            self.assertEqual(run.returncode, 0, run.stderr)
            row = json.loads(run.stdout)
            self.assertEqual(row["backend"], "toolbox")
            self.assertEqual(row["argv"][1], "exec")
            self.assertIn("--diagnostic-file", row["argv"])
            self.assertIn("--project-root", row["argv"])
            self.assertNotIn("--project-write", row["argv"])
            if name == "trivy":
                self.assertNotIn("--cache-dir", row["argv"])
                self.assertIn("--skip-check-update", row["argv"])
            if name == "history":
                self.assertIn("--gitleaks-ignore-path", row["argv"])
            if name == "gitleaks":
                self.assertNotIn("--gitleaks-ignore-path", row["argv"])
            if name == "osv":
                self.assertIn("--offline", row["argv"])
                self.assertIn("/project/application/Cargo.lock", row["argv"])
        # A missing product utility must not leave obsolete host invocation argv.
        run = S.run(
            [
                "bash",
                str(S.ROOT / "scripts/checks/run.sh"),
                "--root",
                str(self.root),
                "--check",
                "audit",
                "--plan",
            ],
            env=dict(
                self.env, PATH="/usr/bin:/bin", CARGO_HOME=str(self.root / "empty")
            ),
            capture_output=True,
        )
        self.assertEqual(run.returncode, 0, run.stderr)
        row = json.loads(run.stdout)
        self.assertEqual(row["backend"], "unavailable")
        self.assertEqual(row["argv"], [])

    def test_sentinel_values_absent_from_process_metadata(self):
        out = self.root / "capture"
        out.mkdir()
        sentinel = "synthetic-private-value-123"
        result = S.execute(
            [sys.executable, "-c", "import sys;print(sys.argv[1])", sentinel],
            self.root,
            self.env,
            out,
        )
        self.assertNotIn(sentinel, json.dumps(result))
        self.assertIn(sentinel, (out / "stdout.log").read_text())

    def test_static_review_rejects_changed_source_and_policy(self):
        target = self.root / "scripts/tests/support.py"
        old = target.read_bytes()
        target.write_bytes(old + b"\n# unreviewed mutation\n")
        _, row = self.run_check("ruff")
        self.assertEqual(row["state"], "blocked")
        self.assertIn("review", row["reason"].lower())
        target.write_bytes(old)
        policy = self.root / "scripts/config/native/ruff/ruff.toml"
        policy.write_bytes(policy.read_bytes() + b"\n# mutation\n")
        _, row = self.run_check("ruff")
        self.assertEqual(row["state"], "blocked")

    def test_static_review_missing_registry_is_rejected(self):
        catalog = self.root / "scripts/config/automation.json"
        data = json.loads(catalog.read_text())
        del data["reviews"]["static"]
        catalog.write_text(json.dumps(data))
        _, row = self.run_check("bandit")
        self.assertEqual(row["state"], "blocked")
        self.assertIn("Missing static review", row["reason"])

    def test_history_fingerprints_require_exact_reviewed_bytes(self):
        S.run(["git", "init", "-q", str(self.root)], check=True, capture_output=True)
        run, row = self.run_check("history")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(row["state"], "passed")
        policy = self.root / "scripts/config/native/gitleaks/gitleaks-history.ignore"
        policy.write_text(policy.read_text() + "unknown:secret.txt:rule:1\n")
        run, row = self.run_check("history")
        self.assertNotEqual(run.returncode, 0)
        self.assertIn("reviewed history fingerprints", row["reason"])
        self.assertIsNone(row["tool_exit_code"])
        policy.unlink()
        run, row = self.run_check("history")
        self.assertNotEqual(run.returncode, 0)
        self.assertIn("reviewed history fingerprints", row["reason"])
