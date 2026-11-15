"""Declarative configuration contracts through public plan entry points."""
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(ROOT / 'scripts', self.root / 'scripts')
        self.catalog = self.root / 'scripts/config/automation.json'
        self.data = json.loads(self.catalog.read_text())

    def plan(self):
        return subprocess.run(
            ['bash', str(self.root / 'scripts/checks/run.sh'), '--check', 'ruff', '--plan'],
            capture_output=True, text=True, check=False,
        )

    def test_native_paths_exist_and_legacy_copies_absent(self):
        for path in self.data['policies'].values():
            self.assertTrue((self.root / path).is_file(), path)
        self.assertFalse((self.root / 'scripts/config/ruff.toml').exists())
        self.assertFalse((self.root / 'scripts/config/static-review.json').exists())
        self.assertEqual(self.plan().returncode, 0)

    def test_catalog_drives_timeout_and_policy_without_shell_evaluation(self):
        self.data['runtime']['native_timeout'] = 321
        self.data['policies']['ruff.toml'] = 'scripts/config/native/ruff/space ; literal.toml'
        self.catalog.write_text(json.dumps(self.data))
        run = self.plan()
        self.assertEqual(run.returncode, 0, run.stderr)
        argv = json.loads(run.stdout)['argv']
        self.assertEqual(argv[argv.index('--timeout') + 1], '321')
        self.assertIn('/project/scripts/config/native/ruff/space ; literal.toml', argv)

    def test_invalid_catalogs_fail_before_execution(self):
        for mutation in ('duplicate', 'escape', 'executor', 'timeout', 'geiger-stack', 'policy'):
            with self.subTest(mutation=mutation):
                data = json.loads(json.dumps(self.data))
                if mutation == 'escape':
                    data['policies']['ruff.toml'] = 'scripts/../outside'
                elif mutation == 'executor':
                    data['checks']['ruff']['executor'] = 'shell'
                elif mutation == 'timeout':
                    data['runtime']['native_timeout'] = 0
                elif mutation == 'geiger-stack':
                    data['runtime']['geiger_stack_bytes'] = 0
                elif mutation == 'policy':
                    data['checks']['ruff']['policy'] = 'missing'
                text = json.dumps(data)
                if mutation == 'duplicate':
                    text = text.replace('"schema": 1', '"schema": 1, "schema": 1')
                self.catalog.write_text(text)
                self.assertNotEqual(self.plan().returncode, 0)
