"""Exact-content maintenance succession must reject drift and preserve history."""
import importlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'tools/governance/scripts'))
R = importlib.import_module("closure_revision")


class ConfigurationSuccessionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='ox-visual-succession-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.relative = 'AGENTS.md'
        content = (ROOT / R.CONFIGURATION_REGISTRY).read_bytes()
        registry = self.root / R.CONFIGURATION_REGISTRY
        registry.parent.mkdir(parents=True)
        registry.write_bytes(content)
        self.row = next(r for r in json.loads(content)['records'] if r['destination'] == self.relative)
        previous = self.root / self.row['previous']
        previous.parent.mkdir(parents=True)
        previous.write_bytes((ROOT / self.row['previous']).read_bytes())
        self.previous = previous
        self.current = (ROOT / self.relative).read_bytes()
        target = self.root / self.relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(self.current)
        complete = self.root / R.COMPLETE_REGISTRY
        complete.parent.mkdir(parents=True, exist_ok=True)
        complete.write_bytes((ROOT / R.COMPLETE_REGISTRY).read_bytes())
        for row in json.loads(complete.read_text())["records"]:
            p = self.root / row["previous"]
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes((ROOT / row["previous"]).read_bytes())

        defaults = self.root / R.DEFAULTS_REGISTRY
        defaults.parent.mkdir(parents=True, exist_ok=True)
        defaults.write_bytes((ROOT / R.DEFAULTS_REGISTRY).read_bytes())
        for row in json.loads(defaults.read_text())["records"]:
            p = self.root / row["previous"]
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes((ROOT / row["previous"]).read_bytes())

        # The current consumer requires explicit repair inputs even in a partial fixture.
        import instruction_revision as I
        import log_repair_revision as L
        for name in (I.REGISTRY, I.DECISION, *L.fixture_paths(ROOT)):
            p = self.root / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes((ROOT / name).read_bytes())

    def test_exact_transition_and_unknown_mutation(self):
        self.assertEqual(R.configuration_predecessor(self.root, self.relative, self.current), self.previous.read_bytes())
        self.assertEqual(R.configuration_predecessor(self.root, self.relative, self.current + b'unknown'), self.current + b'unknown')

    def test_registry_mutation_is_rejected(self):
        (self.root / R.CONFIGURATION_REGISTRY).write_text('{}')
        with self.assertRaisesRegex(ValueError, 'registry changed'):
            R.configuration_predecessor(self.root, self.relative, self.current)

    def test_preimage_mutation_is_rejected(self):
        self.previous.write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError, 'predecessor changed'):
            R.configuration_predecessor(self.root, self.relative, self.current)

    def test_downgrade_is_rejected(self):
        old = self.previous.read_bytes()
        (self.root / self.relative).write_bytes(old)
        with self.assertRaisesRegex(ValueError, 'downgrade'):
            R.configuration_predecessor(self.root, self.relative, old)

    def test_symlinked_preimage_is_rejected(self):
        self.previous.unlink()
        self.previous.symlink_to(ROOT / self.row['previous'])
        with self.assertRaises(ValueError):
            R.configuration_predecessor(self.root, self.relative, self.current)


