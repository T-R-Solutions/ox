"""Strict native report boundaries and installed Machete 0.9.2 compatibility."""

import json
import shutil
import tempfile
import unittest
from pathlib import Path

import support as S


class NativeReports(unittest.TestCase):
    def test_machete_real_clean_findings_and_invalid_manifest(self):
        binary = shutil.which("cargo-machete") or str(
            Path.home() / ".cargo/bin/cargo-machete"
        )
        if not Path(binary).is_file():
            self.skipTest("installed cargo-machete required")
        with tempfile.TemporaryDirectory(prefix="ox-machete-real-") as temporary:
            root = Path(temporary)
            (root / "src").mkdir()
            (root / "src/lib.rs").write_text("pub fn fixture() {}\n")
            manifest = root / "Cargo.toml"
            for suffix, expected in (
                ("", "passed"),
                ('\n[dependencies]\nserde="1"\n', "findings"),
                ("invalid = [", None),
            ):
                manifest.write_text(
                    '[package]\nname="probe"\nversion="0.1.0"\nedition="2021"\n'
                    + suffix
                )
                environment = S.environment()
                result = S.run(
                    [binary, "--skip-target-dir", "--no-ignore", "."],
                    cwd=root,
                    env=environment,
                    capture_output=True,
                )
                (root / "stdout.log").write_bytes(result.stdout)
                (root / "stderr.log").write_bytes(result.stderr)
                if expected:
                    self.assertEqual(
                        S.assess(
                            "machete-text", result.returncode, root / "stdout.log"
                        )[0],
                        expected,
                    )
                else:
                    with S.rejected(self):
                        S.assess("machete-text", result.returncode, root / "stdout.log")

    def test_machete_rejects_incomplete_stderr_without_installed_binary(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "stdout.log").write_text(
                "cargo-machete didn't find any unused dependencies in this directory. Good job!\n"
            )
            for stderr in (
                "",
                "Done!\n",
                "Analyzing dependencies of crates in ....\nerror when handling manifest\nDone!\n",
            ):
                (root / "stderr.log").write_text(stderr)
                with S.rejected(self):
                    S.assess("machete-text", 0, root / "stdout.log")

    def test_deny_summary_and_exit_must_agree(self):
        summary = {
            "type": "summary",
            "fields": {
                k: {"errors": 0, "warnings": 0, "helps": 0, "notes": 0}
                for k in ("licenses", "bans", "sources")
            },
        }
        diagnostic = {
            "type": "diagnostic",
            "fields": {"code": "rejected", "severity": "error"},
        }
        with tempfile.TemporaryDirectory() as temporary:
            report = Path(temporary) / "report.json"
            report.write_text(json.dumps([summary]))
            self.assertEqual(S.assess("deny", 0, report), ("passed", 0, 0))
            for value, raw in (
                ([], 0),
                ([summary], 6),
                ([diagnostic], 1),
                ([diagnostic, summary], 1),
                ([summary, summary], 0),
            ):
                report.write_text(json.dumps(value))
                with S.rejected(self):
                    S.assess("deny", raw, report)
            summary["fields"]["licenses"]["errors"] = 1
            report.write_text(json.dumps([diagnostic, summary]))
            self.assertEqual(S.assess("deny", 4, report)[0], "findings")
            diagnostic["fields"]["severity"] = "bug"
            summary["fields"]["licenses"]["errors"] = 0
            report.write_text(json.dumps([diagnostic, summary]))
            self.assertEqual(S.assess("deny", 0, report)[0], "error")
