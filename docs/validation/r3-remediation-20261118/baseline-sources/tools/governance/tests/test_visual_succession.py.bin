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


class VisualSuccessionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='ox-visual-succession-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.relative = 'AGENTS.md'
        content = (ROOT / R.VISUAL_REGISTRY).read_bytes()
        registry = self.root / R.VISUAL_REGISTRY
        registry.parent.mkdir(parents=True)
        registry.write_bytes(content)
        self.row = next(r for r in json.loads(content)['records'] if r['destination'] == self.relative)
        previous = self.root / self.row['previous']
        previous.parent.mkdir(parents=True)
        previous.write_bytes((ROOT / self.row['previous']).read_bytes())
        self.previous = previous
        self.current = (ROOT / 'docs/validation/configuration-refactor-20261111/before/AGENTS.md.bin').read_bytes()
        target = self.root / self.relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(self.current)

    def test_exact_transition_and_unknown_mutation(self):
        self.assertEqual(R.visual_predecessor(self.root, self.relative, self.current), self.previous.read_bytes())
        self.assertEqual(R.visual_predecessor(self.root, self.relative, self.current + b'unknown'), self.current + b'unknown')

    def test_registry_mutation_is_rejected(self):
        (self.root / R.VISUAL_REGISTRY).write_text('{}')
        with self.assertRaisesRegex(ValueError, 'registry changed'):
            R.visual_predecessor(self.root, self.relative, self.current)

    def test_preimage_mutation_is_rejected(self):
        self.previous.write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError, 'predecessor changed'):
            R.visual_predecessor(self.root, self.relative, self.current)

    def test_downgrade_is_rejected(self):
        old = self.previous.read_bytes()
        (self.root / self.relative).write_bytes(old)
        with self.assertRaisesRegex(ValueError, 'downgrade'):
            R.visual_predecessor(self.root, self.relative, old)

    def test_symlinked_preimage_is_rejected(self):
        self.previous.unlink()
        self.previous.symlink_to(ROOT / self.row['previous'])
        with self.assertRaises(ValueError):
            R.visual_predecessor(self.root, self.relative, self.current)


