"""Behavioral regressions for the 2026-11-17 scripts analysis."""

import hashlib
import json
import shutil
import tempfile
import unittest
from pathlib import Path

import support as S


class AnalysisRegressionTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)

    def invoke(self, script, *args, **kwargs):
        return S.run(["bash", str(S.ROOT / "scripts" / script), *map(str, args)],
                     capture_output=True, **kwargs)

    def fixture_root(self):
        for rel in ("AGENTS.md", "sdd/tools/validate.py",
                    "tools/governance/scripts/check-ox.py",
                    "tools/governance/scripts/run-tests.py"):
            path = self.root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("", encoding="utf-8")

    def test_report_consumes_actual_run_and_filtered_omissions(self):
        self.fixture_root()
        result = self.invoke("automate.sh", "run", "--root", self.root,
                             "--surface", "docs", "--check", "ox")
        self.assertEqual(result.returncode, 0, result.stderr)
        reports = list((self.root / ".local/logs").glob("*/*--results.json.log"))
        self.assertEqual(len(reports), 1)
        projected = self.invoke("reports/summarize.sh", reports[0])
        self.assertEqual(projected.returncode, 0, projected.stderr)
        self.assertIn(b"| ox | passed | 0 |", projected.stdout)
        # Governance remains mandatory even when a single governance check is named.
        self.assertEqual(json.loads(reports[0].read_text())["omitted"], [])

    def test_filtered_surface_baseline_keeps_unselected_checks(self):
        output = S.shell('source "$1/lib/selection.sh"; requested=(ruff); '
                         'requested_surfaces=(scripts); scope=default; select_checks; '
                         'json_args "${BASE[@]}"', S.ROOT / "scripts")
        self.assertEqual(set(json.loads(output)),
                         {"sdd-structure", "ox", "governance-tests", "scripts-syntax",
                          "scripts-tests", "ruff", "shellcheck"})

    def test_summary_aggregate_is_order_independent_and_redacts_argv(self):
        report = self.root / "results.json"
        rows = [{"check": "finding", "state": "findings", "exit_code": 1},
                {"check": "blocked", "state": "blocked", "exit_code": 3},
                {"check": "error", "state": "error", "exit_code": 2}]
        for selected, expected in ((rows, 2), (rows[::-1], 2), (rows[:2], 3),
                                   (rows[:1], 1)):
            with self.subTest(expected=expected, selected=selected):
                report.write_text(json.dumps({"results": selected,
                                              "product_acceptance": False}), encoding="utf-8")
                result = self.invoke("reports/summarize.sh", report)
                self.assertEqual(result.returncode, expected, result.stderr)
        rows[0]["argv"] = ["secret-credential"]
        report.write_text(json.dumps({"results": rows, "product_acceptance": False}),
                          encoding="utf-8")
        self.assertNotIn(b"secret-credential", self.invoke("reports/summarize.sh", report).stdout)

    def test_common_preserves_explicit_operator_environment(self):
        result = S.run(["bash", "-c", 'source "$1"; printf "%s:%s:%s" '
                        '"$CARGO_NET_OFFLINE" "$RUSTUP_AUTO_INSTALL" "$PYTHONDONTWRITEBYTECODE"',
                        "_", str(S.ROOT / "scripts/lib/common.sh")],
                       env=S.environment(CARGO_NET_OFFLINE="false", RUSTUP_AUTO_INSTALL="1",
                                         PYTHONDONTWRITEBYTECODE=""), capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, b"false:1:")

    def test_local_path_is_order_independent_and_rejects_bad_arguments(self):
        for args in (("--path", "runs", "--root", self.root),
                     ("--root", self.root, "--path", "runs")):
            result = self.invoke("local.sh", *args)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout.decode().strip(), str(self.root / ".local/logs"))
        for args in (("--root",), ("--path",), ("--root", self.root / "missing", "--path", "runs"),
                     ("--path", "runs", "--apply"), ("--path", "unknown")):
            with self.subTest(args=args):
                result = self.invoke("local.sh", *args)
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertTrue(result.stderr)
        self.assertFalse((self.root / ".local").exists())

    def test_deny_native_bitmask_is_normalized_without_losing_findings(self):
        for field, raw in (("bans", 2), ("licenses", 4), ("sources", 8)):
            fields = {key: {"errors": int(key == field), "warnings": 0}
                      for key in ("bans", "licenses", "sources")}
            report = self.root / "deny.json"
            report.write_text(json.dumps([
                {"type": "diagnostic", "fields": {"code": "fixture", "severity": "error"}},
                {"type": "summary", "fields": fields},
            ]), encoding="utf-8")
            self.assertEqual(S.assess("deny", raw, report), ("findings", 1, 1))
            with S.rejected(self):
                S.assess("deny", 0, report)

    def test_missing_analyzer_inputs_emit_structured_error(self):
        for script, args in (("security/analyzers/check-report.sh", ("--parser", "ruff")),
                             ("security/analyzers/validate-exceptions.sh", ())):
            result = self.invoke(script, *args, self.root / "missing.json")
            self.assertEqual(result.returncode, 2)
            self.assertEqual(json.loads(result.stdout)["state"], "error")

    def test_empty_exclusions_do_not_invent_a_find_predicate(self):
        source = self.root / "source"
        source.mkdir()
        (source / "keep.md").write_text("fixture", encoding="utf-8")
        output = self.root / "out"
        output.mkdir()
        S.shell('catalog_load; AUTOMATION_JSON=$(jq \' .inputs.exclude_names=[] | '
                '.inputs.exclude_paths=[]\' <<<"$AUTOMATION_JSON"); ROOT=$2; '
                'source_snapshot "$1" all', output, source)
        self.assertEqual(set(json.loads((output / "inputs.json").read_text())), {"keep.md"})

    def test_catalog_rejects_unsafe_selectors_and_review_bindings(self):
        scripts = self.root / "scripts"
        shutil.copytree(S.ROOT / "scripts/lib", scripts / "lib")
        (scripts / "config").mkdir()
        original = json.loads((S.ROOT / "scripts/config/automation.json").read_text())
        changes = [("inputs", "roots", ["../escape"]), ("paths", "runs", "/absolute"),
                   ("inputs", "exclude_names", "not-an-array"),
                   ("reviews", "history_sha256", "invalid")]
        for section, field, value in changes:
            with self.subTest(section=section, field=field):
                catalog = json.loads(json.dumps(original))
                catalog[section][field] = value
                (scripts / "config/automation.json").write_text(json.dumps(catalog), encoding="utf-8")
                result = S.run(["bash", "-c", 'source "$1/lib/common.sh"; '
                                'source "$1/lib/registry.sh"; catalog_load', "_", str(scripts)],
                               capture_output=True)
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertIn(b"Invalid inputs/paths/databases/reviews catalog", result.stderr)

    def test_reason_codes_are_translated_without_echoing_raw_text(self):
        result = S.shell('source "$1/lib/progress.sh"; progress_cause '
                         '\'untrusted-secret\' DATASET_INVALID', S.ROOT / "scripts")
        self.assertIn("vencida", result.decode())
        self.assertNotIn(b"untrusted-secret", result)
        result = S.shell('source "$1/lib/progress.sh"; progress_cause '
                         '\'untrusted-secret\' UNKNOWN', S.ROOT / "scripts")
        self.assertEqual(result.decode(), "causa não determinada")

    def test_unclassified_adapter_failure_does_not_claim_invalid_inputs(self):
        binary = self.root / "bin"
        binary.mkdir()
        shim = binary / "sha256sum"
        shim.write_text("#!/bin/sh\nexit 7\n", encoding="utf-8")
        shim.chmod(0o700)
        result = self.invoke(
            "checks/run.sh", "--root", self.root, "--check", "gitleaks",
            env=S.environment(PATH=f"{binary}:/usr/bin:/bin"),
        )
        self.assertEqual(result.returncode, 3, result.stderr)
        paths = S.published_assessments(self.root)
        self.assertEqual(len(paths), 1)
        row = json.loads(paths.pop().read_text(encoding="utf-8"))
        self.assertEqual(row["reason_code"], "UNKNOWN")
        self.assertEqual(row["reason"], "Check ended without a classified cause")
        self.assertEqual(row["state"], "blocked")

    def test_batched_manifest_matches_canonical_bytes_for_unusual_paths(self):
        tree = self.root / "tree"
        tree.mkdir()
        names = ["plain", "space name", "line\nbreak", "back\\slash", "café", "-option"]
        manifest = {}
        for name in names:
            (tree / name).write_bytes(b"fixture")
            manifest[name] = hashlib.sha256(b"fixture").hexdigest()
        canonical = json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode()
        self.assertEqual(S.tree_identity(tree), hashlib.sha256(canonical).hexdigest())
        (tree / "link").symlink_to(tree / "plain")
        with S.rejected(self):
            S.tree_identity(tree)

    def test_batched_hash_failure_does_not_accept_partial_inventory(self):
        tree = self.root / "tree"
        tree.mkdir()
        (tree / "item").write_bytes(b"fixture")
        binary = self.root / "bin"
        binary.mkdir()
        shim = binary / "sha256sum"
        shim.write_text("#!/bin/sh\nexit 7\n", encoding="utf-8")
        shim.chmod(0o700)
        # GNU xargs reports a failed child as 123; the pipeline must retain it.
        with S.rejected(self, returncode=123):
            S.shell('PATH="$1:$PATH"; tree_identity "$2"', binary, tree)

    def test_inspect_data_and_output_guards_use_real_entry(self):
        dataset = self.root / "data"
        dataset.mkdir()
        (dataset / "record").write_text("fixture", encoding="utf-8")
        result = self.invoke("checks/run.sh", "--root", self.root, "--inspect-data", "data")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["sha256"], S.tree_identity(dataset))
        (self.root / "linked").symlink_to(dataset, target_is_directory=True)
        rejected = self.invoke("checks/run.sh", "--root", self.root, "--inspect-data", "linked")
        self.assertEqual(rejected.returncode, 2)
        self.assertIn(b"without symlinks", rejected.stderr)
        outside = self.root / "outside"
        rejected = self.invoke("checks/run.sh", "--root", self.root, "--check", "ruff",
                               "--output", outside)
        self.assertEqual(rejected.returncode, 2)
        self.assertIn(b"active temporary run", rejected.stderr)
        self.assertFalse(outside.exists())

    def test_automate_source_guard_rejects_without_execution(self):
        result = S.run(["bash", "-c", 'source "$1"', "_",
                        str(S.ROOT / "scripts/automate.sh")], cwd=self.root,
                       capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn(b"do not source", result.stderr)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_toolbox_builder_preserves_argument_boundaries(self):
        result = S.shell('source "$1/lib/backends.sh"; SCANNER=fixture; '
                         'NATIVE_TIMEOUT=42; NATIVE=(scan "argument with spaces"); '
                         'toolbox_command "/tool box" "/source dir" "/result dir"; '
                         'json_args "${CMD[@]}"', S.ROOT / "scripts")
        self.assertEqual(json.loads(result), ["/tool box", "exec", "--tool", "fixture",
                         "--project-root", "/source dir", "--results", "/result dir",
                         "--timeout", "42", "--diagnostic-file", "/result dir/backend_record.json",
                         "--", "scan", "argument with spaces"])


if __name__ == "__main__":
    unittest.main()
