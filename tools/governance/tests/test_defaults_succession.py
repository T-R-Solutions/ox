"""Script defaults documentation accepts only reviewed bytes and intact history."""
import importlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools/governance/scripts"))
R = importlib.import_module("closure_revision")


class DefaultsSuccessionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.relative = "AGENTS.md"
        content = (ROOT / R.DEFAULTS_REGISTRY).read_bytes()
        self.registry = self.root / R.DEFAULTS_REGISTRY
        self.registry.parent.mkdir(parents=True)
        self.registry.write_bytes(content)
        row = next(row for row in json.loads(content)["records"] if row["destination"] == self.relative)
        self.previous = self.root / row["previous"]
        self.previous.parent.mkdir(parents=True)
        self.previous.write_bytes((ROOT / row["previous"]).read_bytes())
        self.current = (ROOT / self.relative).read_bytes()
        self.target = self.root / self.relative
        self.target.write_bytes(self.current)

        # The current consumer requires explicit repair inputs even in a partial fixture.
        import instruction_revision as I
        import log_repair_revision as L
        for name in (I.REGISTRY, I.DECISION, *L.fixture_paths(ROOT)):
            p = self.root / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes((ROOT / name).read_bytes())

    def test_reviewed_and_unknown_bytes(self):
        self.assertEqual(R.defaults_predecessor(self.root, self.relative, self.current), self.previous.read_bytes())
        self.assertEqual(R.defaults_predecessor(self.root, self.relative, self.current + b"unknown"), self.current + b"unknown")

    def test_corrupt_registry(self):
        self.registry.write_text("{}")
        with self.assertRaisesRegex(ValueError, "registry changed"):
            R.defaults_predecessor(self.root, self.relative, self.current)

    def test_corrupt_preimage(self):
        self.previous.write_bytes(b"unknown")
        with self.assertRaisesRegex(ValueError, "predecessor changed"):
            R.defaults_predecessor(self.root, self.relative, self.current)

    def test_downgrade(self):
        old = self.previous.read_bytes()
        self.target.write_bytes(old)
        with self.assertRaisesRegex(ValueError, "downgrade"):
            R.defaults_predecessor(self.root, self.relative, old)

    def test_symlink_preimage(self):
        self.previous.unlink()
        self.previous.symlink_to(ROOT / self.relative)
        with self.assertRaises(ValueError):
            R.defaults_predecessor(self.root, self.relative, self.current)
