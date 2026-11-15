"""Pinned predecessor chain rejects drift instead of renewing historical digests."""
import importlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'tools/governance/scripts'))
R = importlib.import_module('instruction_revision')


class InstructionSuccessionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='ox-instruction-succession-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        rows = json.loads((ROOT / R.REGISTRY).read_text())['records']
        self.rows = rows
        names = {R.REGISTRY, R.DECISION}
        for row in rows:
            names.update((row['destination'], row['previous']))
        names.add(R.AGENT_SNAPSHOT)
        for agent in R.agent_snapshots(ROOT):
            names.update((agent['source'], agent['snapshot']))
        import log_repair_revision
        names = list(names) + log_repair_revision.fixture_paths(ROOT)
        for name in names:
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((ROOT / name).read_bytes())
        self.row = next(row for row in rows if row['destination'] == 'sdd/project.md')

    def test_exact_transition_and_unknown_mutation(self):
        self.assertEqual(R.errors(self.root), [])
        for row in self.rows:
            name = row['destination']
            data = (self.root / name).read_bytes()
            self.assertEqual(R.predecessor(self.root, name, data), (self.root / row['previous']).read_bytes())
            self.assertEqual(R.predecessor(self.root, name, data + b'unknown'), data + b'unknown')
        target = self.root / self.row['destination']
        target.write_bytes(target.read_bytes() + b'unknown')
        self.assertTrue(R.errors(self.root))

    def test_registry_and_decision_mutation_rejected(self):
        for name in (R.REGISTRY, R.DECISION):
            target = self.root / name
            data = target.read_bytes()
            target.write_bytes(data + b'changed')
            self.assertTrue(R.errors(self.root))
            target.write_bytes(data)

    def test_preimage_mutation_and_downgrade_rejected(self):
        old = self.root / self.row['previous']
        data = old.read_bytes()
        old.write_bytes(b'tampered')
        self.assertTrue(R.errors(self.root))
        old.write_bytes(data)
        (self.root / self.row['destination']).write_bytes(data)
        with self.assertRaisesRegex(ValueError, 'downgrade'):
            R.predecessor(self.root, self.row['destination'], data)

    def test_symlink_substitutions_and_missing_registry_rejected(self):
        for name in (self.row['destination'], self.row['previous'], R.REGISTRY):
            target = self.root / name
            data = target.read_bytes()
            replacement = self.root / 'same.bin'
            replacement.write_bytes(data)
            target.unlink()
            target.symlink_to(replacement)
            self.assertTrue(R.errors(self.root))
            target.unlink()
            target.write_bytes(data)
        (self.root / R.REGISTRY).unlink()
        self.assertTrue(R.errors(self.root))


    def test_missing_new_registry_cannot_accept_changed_current_sources(self):
        import log_repair_revision
        (self.root / log_repair_revision.REGISTRY).unlink()
        self.assertTrue(R.errors(self.root))


if __name__ == '__main__':
    unittest.main()
