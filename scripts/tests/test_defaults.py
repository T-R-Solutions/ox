"""Ec command/default parity through the public shell entry, without native scans."""

import json
import tempfile
import unittest
from pathlib import Path

import support as S


class DefaultParityTests(unittest.TestCase):
    def invoke(self, *args, root=S.ROOT):
        return S.shell('bash "$1" "${@:2}"', S.ROOT / 'scripts/automate.sh', *args, root=root)

    def plan(self, *args):
        return json.loads(self.invoke('plan', *args))

    def names(self, *args):
        return [row[0] for row in self.plan(*args)]

    def test_default_and_complete_match_ec_complementary_selection(self):
        default = self.names()
        complete = self.names('--scope', 'complete')
        self.assertEqual(set(complete) - set(default), {'grype', 'bandit', 'sbom', 'malware'})
        self.assertEqual(len(complete), len(set(complete)))
        self.assertTrue({'coverage', 'geiger', 'history', 'trivy', 'shellcheck', 'scripts-tests'} <= set(default))
        legacy = json.loads(self.invoke('--scope', 'complete', '--plan'))
        self.assertEqual(set(complete) - {row[0] for row in legacy}, {'scripts-tests', 'scripts-syntax'})

    def test_filters_keep_governance_and_deduplicate(self):
        mandatory = ['sdd-structure', 'ox', 'governance-tests']
        self.assertEqual(self.names('--check', 'ruff', '--check', 'ruff'), mandatory + ['ruff'])
        self.assertEqual(self.names('--check', 'secrets'), mandatory + ['gitleaks', 'history'])
        self.assertEqual(self.names('--surface', 'application', '--check', 'coverage'), mandatory + ['coverage'])
        self.assertEqual(self.names('--check', 'syft'), mandatory + ['sbom'])
        self.assertEqual(self.names('--surface', 'scripts', '--surface', 'docs'),
                         mandatory + ['scripts-syntax', 'shellcheck', 'ruff', 'scripts-tests'])

    def test_bad_arguments_are_rejected_before_execution(self):
        for args in [(), ('execute',), ('run', '--scope', 'full'),
                     ('run', '--scope', 'complete', '--check', 'ruff'),
                     ('run', '--scope', 'complete', '--surface', 'docs'),
                     ('run', '--scope', 'complete', '--scope', 'complete'),
                     ('run', '--surface', 'unknown'), ('run', '--check', 'unknown'),
                     ('run', '--surface', 'scripts', '--check', 'rust-check'),
                     ('run', '--check', 'coverage'), ('run', '--root'),
                     ('run', '--check', '--surface', 'docs'), ('run', '--plan')]:
            with self.subTest(args=args), self.assertRaises(ValueError):
                self.invoke(*args)

    def test_plan_does_not_probe_cargo_or_create_local_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for rel in ['AGENTS.md', 'sdd/tools/validate.py',
                        'tools/governance/scripts/check-ox.py',
                        'tools/governance/scripts/run-tests.py', 'application/Cargo.lock']:
                p = root / rel
                p.parent.mkdir(parents=True, exist_ok=True)
                p.touch()
            # There is deliberately no Cargo manifest or toolchain in this root.
            result = self.plan('--root', tmp, '--scope', 'complete')
            self.assertEqual(len(result), 26)
            legacy = json.loads(self.invoke('--root', tmp, '--scope', 'complete', '--plan'))
            self.assertEqual(len(legacy), 24)
            self.assertFalse((root / '.local').exists())

    def test_run_uses_same_selection_defaults_and_aggregate_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'AGENTS.md').touch()
            for rel, code in [('sdd/tools/validate.py', 1),
                              ('tools/governance/scripts/check-ox.py', 3),
                              ('tools/governance/scripts/run-tests.py', 2)]:
                p = root / rel
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text('import os, sys\n'
                             'assert os.environ["NO_COLOR"] == "1"\n'
                             'assert os.environ["CARGO_NET_OFFLINE"] == "true"\n'
                             f'sys.exit({code})\n')
            result = S.shell('set +e; bash "$1" run --root "$2" --surface docs; rc=$?; printf "exit=%s\\n" "$rc"',
                             S.ROOT / 'scripts/automate.sh', tmp)
            self.assertIn(b'exit=2', result)
            reports = list((root / '.local/logs').rglob('*results.json.log'))
            self.assertEqual(len(reports), 1)
            rows = json.loads(reports[0].read_text())['results']
            self.assertEqual([r['check'] for r in rows], self.names('--surface', 'docs'))
            self.assertEqual([r['exit_code'] for r in rows], [1, 3, 2])

    def test_environment_discovers_toolbox_and_preserves_explicit_overrides(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'ox'
            root.mkdir()
            cache = root / '.cache/ox/cargo-home'
            cache.mkdir(parents=True)
            toolbox = root.parent / 'dev_audit/shared-toolbox/bin/toolbox'
            toolbox.parent.mkdir(parents=True)
            toolbox.write_text('#!/bin/sh\nexit 99\n')
            toolbox.chmod(0o700)
            prelude = 'source "$1/lib/selection.sh"; ROOT=$OX_TEST_ROOT; catalog_load; '
            # Restrict PATH so discovery does not depend on an installed toolbox.
            result = S.shell(prelude + 'unset TOOLBOX_BIN TOOLBOX_ROOT TOOLBOX_SELINUX_LABEL CARGO_HOME; '
                             'PATH=/usr/bin:/bin; execution_environment; '
                             'json_args "$TOOLBOX_BIN" "$TOOLBOX_SELINUX_LABEL" "$CARGO_HOME"',
                             S.ROOT / 'scripts', root=root)
            self.assertEqual(json.loads(result), [str(toolbox), 'shared', str(cache)])
            result = S.shell(prelude + 'TOOLBOX_BIN=""; TOOLBOX_SELINUX_LABEL=private; '
                             'CARGO_HOME="/explicit cache"; execution_environment; '
                             'json_args "$TOOLBOX_BIN" "$TOOLBOX_SELINUX_LABEL" "$CARGO_HOME"',
                             S.ROOT / 'scripts', root=root)
            self.assertEqual(json.loads(result), ['', 'private', '/explicit cache'])

    def test_generated_inputs_are_excluded_and_sources_remain(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'root'
            root.mkdir()
            keep = ['.env.local', 'scripts/source.py', 'scripts/evidence.log',
                    'scripts/.yarn/releases/tool.cjs', '.codex/skills/example/SKILL.md']
            omit = ['scripts/node_modules/lib/main.js', 'scripts/.pytest_cache/data',
                    'scripts/test-results/result.json', 'scripts/main.profraw',
                    'scripts/editor.swp', 'scripts/coverage/index.html']
            for rel in keep + omit:
                path = root / rel
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text('fixture\n')
            output = Path(tmp) / 'output'
            output.mkdir()
            _, manifest = S.source_copy(root, output)
            self.assertEqual(set(manifest), set(keep))

    def test_trivy_counts_all_scanners_and_redacts_before_retention(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            report = output / 'report.json'
            data = {'SchemaVersion': 2, 'Results': [{
                'Vulnerabilities': [{'VulnerabilityID': 'fixture'}],
                'Secrets': [{'RuleID': 'fixture', 'Match': 'sensitive-value',
                             'Code': {'Lines': ['sensitive-value']}}],
                'Misconfigurations': [{'Status': 'FAIL', 'CauseMetadata': {
                    'Code': {'Lines': ['sensitive-value']}}}, {'Status': 'PASS'}],
            }]}
            report.write_text(json.dumps(data))
            self.assertEqual(S.assess('trivy', 1, report), ('findings', 1, 3))
            S.shell('redact_trivy "$1" "$2"', report, output)
            self.assertNotIn('sensitive-value', report.read_text())
            self.assertEqual(S.assess('trivy', 1, report), ('findings', 1, 3))
            self.assertFalse(json.loads((output / 'redaction.json').read_text())['raw_retained'])
            data['Results'][0]['ExperimentalModifiedFindings'] = [{}]
            report.write_text(json.dumps(data))
            with self.assertRaises(ValueError):
                S.assess('trivy', 0, report)
            with self.assertRaises(ValueError):
                S.shell('redact_trivy "$1" "$2"', report, output)
            self.assertNotIn('sensitive-value', report.read_text())
            report.write_text('{malformed sensitive-value')
            with self.assertRaises(ValueError):
                S.shell('redact_trivy "$1" "$2"', report, output)
            self.assertNotIn('sensitive-value', report.read_text())

    def test_clippy_and_trivy_plans_enable_the_ec_policies(self):
        clippy = self.plan('--check', 'clippy')[-1][2]
        for flag in ['clippy::all', 'clippy::pedantic', 'clippy::nursery',
                     'clippy::cargo', '--all-features', '--keep-going']:
            self.assertIn(flag, clippy)
        self.assertTrue(any('CLIPPY_CONF_DIR=' in arg for arg in clippy))
        trivy = self.plan('--check', 'trivy')[-1][2]
        self.assertNotIn('--scanners', trivy)
        self.assertIn('/out/report.json', trivy)
        self.assertIn('--include-non-failures', trivy)

    def test_missing_toolchain_is_blocked_not_a_finding(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for rel in ['AGENTS.md', 'sdd/tools/validate.py',
                        'tools/governance/scripts/check-ox.py',
                        'tools/governance/scripts/run-tests.py', 'application/Cargo.lock']:
                path = root / rel
                path.parent.mkdir(parents=True, exist_ok=True)
                path.touch()
            result = S.shell('set +e; bash "$1" run --root "$2" --check rust-check; rc=$?; '
                             'printf "exit=%s\\n" "$rc"', S.ROOT / 'scripts/automate.sh', tmp)
            self.assertIn(b'exit=3', result)


if __name__ == '__main__':
    unittest.main()
