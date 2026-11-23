"""Eight-path successor rejects unknown bytes and reconstructs exact predecessors."""

import hashlib
import importlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools/governance/scripts"))
R = importlib.import_module("windows_design_revision")


class WindowsDesignRevisionTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="ox-windows-design-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        for name in R.fixture_paths(ROOT):
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((ROOT / name).read_bytes())

    def test_exact_reconstruction_and_unknown_buffers(self):
        self.assertEqual(R.errors(self.root), [])
        for name, row in R.records(self.root).items():
            current = (self.root / name).read_bytes()
            previous = R.predecessor(self.root, name, current)
            self.assertEqual(hashlib.sha256(previous).hexdigest(), row["previous_sha256"])
            unknown = current + b"unknown supplied buffer"
            self.assertEqual(R.predecessor(self.root, name, unknown), unknown)
        self.assertEqual(R.predecessor(self.root, "other.md", b"unrelated"), b"unrelated")

    def test_each_live_mutation_deletion_symlink_and_downgrade_rejected(self):
        self.assertEqual(R.errors(self.root), [])
        for name in sorted(R.DESTINATIONS):
            with self.subTest(path=name):
                target = self.root / name
                original = target.read_bytes()
                previous = R.predecessor(self.root, name, original)
                changed = (original.replace(b"## Authorities", b"## Lost authorities", 1)
                           if name == "sdd/project.md" else original + b"unknown live mutation")
                self.assertNotEqual(changed, original)
                target.write_bytes(changed)
                self.assertTrue(any(name in error for error in R.errors(self.root)))
                self.assertEqual(R.predecessor(self.root, name, changed), changed)
                target.unlink()
                self.assertTrue(any(name in error for error in R.errors(self.root)))
                replacement = self.root / "replacement"
                replacement.write_bytes(original)
                target.symlink_to(replacement)
                self.assertTrue(any(name in error for error in R.errors(self.root)))
                target.unlink()
                target.write_bytes(previous)
                self.assertTrue(any(name in error for error in R.errors(self.root)))
                with self.assertRaisesRegex(ValueError, "downgrade"):
                    R.predecessor(self.root, name, previous)
                target.write_bytes(original)

    def test_registry_missing_mutated_and_symlinked_rejected(self):
        target = self.root / R.REGISTRY
        original = target.read_bytes()
        target.write_bytes(original + b" ")
        with self.assertRaisesRegex(ValueError, "registry changed"):
            R.records(self.root)
        target.unlink()
        with self.assertRaises(ValueError):
            R.errors(self.root)
        replacement = self.root / "registry-replacement"
        replacement.write_bytes(original)
        target.symlink_to(replacement)
        with self.assertRaises(ValueError):
            R.errors(self.root)

    def test_even_authenticated_invalid_schema_scope_and_edits_rejected(self):
        target = self.root / R.REGISTRY
        original = target.read_bytes()
        for kind in ("schema", "extra", "missing", "duplicate", "escape", "bounds", "overlap", "digest"):
            with self.subTest(kind=kind):
                doc = json.loads(original)
                row = doc["records"][0]
                if kind == "schema":
                    doc["schema_version"] = True
                elif kind == "extra":
                    doc["records"].append(dict(row, destination="unknown.md"))
                elif kind == "missing":
                    doc["records"].pop()
                elif kind == "duplicate":
                    doc["records"].append(row.copy())
                elif kind == "escape":
                    row["destination"] = "../AGENTS.md"
                elif kind == "bounds":
                    row["reverse_edits"][-1]["end"] = 10**9
                elif kind == "overlap":
                    row["reverse_edits"].append(row["reverse_edits"][0].copy())
                else:
                    row["previous_sha256"] = "0" * 64
                raw = json.dumps(doc).encode()
                target.write_bytes(raw)
                with patch.object(R, "REVIEWED", R.digest(raw)):
                    if kind in {"bounds", "digest"}:
                        expected = ("reverse edit exceeds input" if kind == "bounds"
                                    else "reconstructed predecessor changed: " + row["destination"])
                        self.assertTrue(any(expected in error for error in R.errors(self.root)))
                    else:
                        with self.assertRaises(ValueError):
                            R.records(self.root)
        target.write_bytes(original)

    def test_duplicate_json_properties_and_symlinked_parent_rejected(self):
        target = self.root / R.REGISTRY
        changed = target.read_bytes().replace(b'"schema_version": 1', b'"schema_version": 1, "schema_version": 1', 1)
        target.write_bytes(changed)
        with patch.object(R, "REVIEWED", R.digest(changed)):
            with self.assertRaisesRegex(ValueError, "Duplicate"):
                R.records(self.root)
        target.write_bytes((ROOT / R.REGISTRY).read_bytes())
        directory = self.root / ".codex"
        destination = self.root / "relocated"
        directory.rename(destination)
        directory.symlink_to(destination, target_is_directory=True)
        self.assertTrue(any("symlinked" in error and ".codex" in error
                            for error in R.errors(self.root)))


if __name__ == "__main__":
    unittest.main()
