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


class MaintenanceSuccessionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='ox-maintenance-succession-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.relative = 'sdd/workflow.md'
        content = (ROOT / R.MAINTENANCE_REGISTRY).read_bytes()
        registry = self.root / R.MAINTENANCE_REGISTRY
        registry.parent.mkdir(parents=True)
        registry.write_bytes(content)
        self.row = next(r for r in json.loads(content)['records'] if r['destination'] == self.relative)
        previous = self.root / self.row['previous']
        previous.parent.mkdir(parents=True)
        previous.write_bytes((ROOT / self.row['previous']).read_bytes())
        self.previous = previous
        # This unit fixture represents the 09/11 transition, not today's terminal.
        self.current = (ROOT / 'docs/validation/governance-corrections-20261114/before/sdd/workflow.md.bin').read_bytes()
        import hashlib
        self.assertEqual(hashlib.sha256(self.current).hexdigest(), self.row['sha256'])
        target = self.root / self.relative
        target.parent.mkdir(parents=True)
        target.write_bytes(self.current)

    def test_exact_transition_and_unknown_mutation(self):
        self.assertEqual(R.maintenance_predecessor(self.root, self.relative, self.current), self.previous.read_bytes())
        self.assertEqual(R.maintenance_predecessor(self.root, self.relative, self.current + b'unknown'), self.current + b'unknown')

    def test_registry_mutation_is_rejected(self):
        (self.root / R.MAINTENANCE_REGISTRY).write_text('{}')
        with self.assertRaisesRegex(ValueError, 'registry changed'):
            R.maintenance_predecessor(self.root, self.relative, self.current)

    def test_preimage_mutation_is_rejected(self):
        self.previous.write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError, 'predecessor changed'):
            R.maintenance_predecessor(self.root, self.relative, self.current)

    def test_downgrade_is_rejected(self):
        old = self.previous.read_bytes()
        (self.root / self.relative).write_bytes(old)
        with self.assertRaisesRegex(ValueError, 'downgrade'):
            R.maintenance_predecessor(self.root, self.relative, old)

    def test_symlinked_preimage_is_rejected(self):
        self.previous.unlink()
        self.previous.symlink_to(ROOT / self.row['previous'])
        with self.assertRaises(ValueError):
            R.maintenance_predecessor(self.root, self.relative, self.current)

    def test_prior_observations_preserved_verbatim(self):
        base = ROOT / 'docs/validation/repository-maintenance-20261109/before-features'
        count = 0
        for p in base.rglob('evidence.json.bin'):
            original = json.loads(p.read_text())
            relative = str(p.relative_to(base))[:-4]
            current = json.loads((ROOT / relative).read_text())
            for old in original['evidence']:
                if old['id'] == 'E-README-SKILL-INTEGRATION-REVIEW':
                    self.assertIn(old, current['historical_evidence'])
                    self.assertNotIn(old, current['evidence'])
                    count += 1
        self.assertEqual(count, 14)
