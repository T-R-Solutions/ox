"""Reviewed visual-method edits authenticate without stored predecessor copies."""

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
R = importlib.import_module("visual_skill_revision")


class VisualSkillRevisionTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="ox-visual-skill-revision-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        from windows_design_revision import fixture_paths
        for name in R.EXISTING | R.ADDED | {R.REGISTRY} | set(fixture_paths(ROOT)):
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((ROOT / name).read_bytes())

    def test_exact_predecessor_and_unknown_buffers(self):
        self.assertEqual(R.errors(self.root), [])
        for name, row in R.records(self.root).items():
            current = (self.root / name).read_bytes()
            if name in R.ADDED:
                from windows_design_revision import predecessor
                self.assertEqual(R.predecessor(self.root, name, current), predecessor(self.root, name, current))
                continue
            actual = R.predecessor(self.root, name, current)
            unknown = current + b"unreviewed passed bytes"
            self.assertEqual(R.predecessor(self.root, name, unknown), unknown)
            self.assertEqual(hashlib.sha256(actual).hexdigest(), row["previous_sha256"])
        self.assertEqual(R.predecessor(self.root, "unrelated", b"bytes"), b"bytes")

    def test_reverse_edits_restore_a_literal_independent_example(self):
        row = {
            "destination": "fixture",
            "previous_sha256": hashlib.sha256(b"alpha BETA gamma").hexdigest(),
            "reverse_edits": [
                {"start": 6, "end": 10, "previous_hex": b"BETA".hex()},
                {"start": 16, "end": 20, "previous_hex": ""},
            ],
        }
        self.assertEqual(R._reverse(b"alpha beta gamma new", row), b"alpha BETA gamma")

    def test_each_mutation_deletion_symlink_and_downgrade_is_rejected(self):
        self.assertEqual(R.errors(self.root), [])
        for name in sorted(R.EXISTING | R.ADDED):
            with self.subTest(path=name):
                target = self.root / name
                original = target.read_bytes()
                target.write_bytes(original + b"unreviewed mutation")
                self.assertTrue(any(name in error for error in R.errors(self.root)))
                self.assertEqual(R.predecessor(self.root, name, target.read_bytes()), target.read_bytes())
                target.unlink()
                self.assertTrue(any(name in error for error in R.errors(self.root)))
                replacement = self.root / "identical-resource"
                replacement.write_bytes(original)
                target.symlink_to(replacement)
                self.assertTrue(any(name in error for error in R.errors(self.root)))
                target.unlink()
                target.write_bytes(original)
                if name in R.EXISTING:
                    previous = R.predecessor(self.root, name, original)
                    target.write_bytes(previous)
                    self.assertTrue(any(name in error for error in R.errors(self.root)))
                    with self.assertRaisesRegex(ValueError, "downgrade"):
                        R.predecessor(self.root, name, previous)
                    target.write_bytes(original)

    def test_current_gate_and_predecessor_require_the_registry(self):
        name = "tools/governance/scripts/check-ox.py"
        current = (self.root / name).read_bytes()
        (self.root / R.REGISTRY).unlink()
        with self.assertRaises(ValueError):
            R.predecessor(self.root, name, current)
        with self.assertRaises(ValueError):
            R.errors(self.root)

    def test_registry_mutation_missing_and_symlink_are_rejected(self):
        target = self.root / R.REGISTRY
        original = target.read_bytes()
        target.write_bytes(original + b" ")
        with self.assertRaisesRegex(ValueError, "registry changed"):
            R.records(self.root)
        target.unlink()
        with self.assertRaises(ValueError):
            R.records(self.root)
        replacement = self.root / "registry-resource"
        replacement.write_bytes(original)
        target.symlink_to(replacement)
        with self.assertRaises(ValueError):
            R.records(self.root)

    def test_authenticated_malformed_scope_or_edits_still_rejected(self):
        target = self.root / R.REGISTRY
        original = target.read_bytes()
        for kind in ("extra", "missing", "duplicate", "path", "bounds", "overlap", "digest"):
            with self.subTest(mutation=kind):
                document = json.loads(original)
                rows = document["records"]
                existing = next(row for row in rows if row["destination"] in R.EXISTING)
                if kind == "extra":
                    rows.append(dict(rows[0], destination="unreviewed.md"))
                elif kind == "missing":
                    rows.pop()
                elif kind == "duplicate":
                    rows.append(dict(rows[0]))
                elif kind == "path":
                    rows[0]["destination"] = "../outside"
                elif kind == "bounds":
                    existing["reverse_edits"][-1]["end"] = 10**9
                elif kind == "overlap":
                    existing["reverse_edits"].append(dict(existing["reverse_edits"][0]))
                elif kind == "digest":
                    existing["previous_sha256"] = "0" * 64
                changed = json.dumps(document).encode()
                target.write_bytes(changed)
                with patch.object(R, "REVIEWED", hashlib.sha256(changed).hexdigest()):
                    if kind in {"bounds", "digest"}:
                        expected = ("reverse edit exceeds input" if kind == "bounds"
                                    else "reconstructed predecessor changed: " + existing["destination"])
                        self.assertTrue(any(expected in error for error in R.errors(self.root)))
                    else:
                        with self.assertRaises(ValueError):
                            R.records(self.root)
        target.write_bytes(original)

    def test_symlinked_parent_and_duplicate_json_properties_are_rejected(self):
        directory = self.root / ".codex"
        destination = self.root / "relocated-codex"
        directory.rename(destination)
        directory.symlink_to(destination, target_is_directory=True)
        self.assertTrue(any("symlinked" in error and ".codex" in error
                            for error in R.errors(self.root)))
        target = self.root / R.REGISTRY
        changed = target.read_bytes().replace(b'"schema_version": 1', b'"schema_version": 1, "schema_version": 1', 1)
        self.assertNotEqual(changed, target.read_bytes())
        target.write_bytes(changed)
        with patch.object(R, "REVIEWED", hashlib.sha256(changed).hexdigest()):
            with self.assertRaisesRegex(ValueError, "Duplicate"):
                R.records(self.root)


if __name__ == "__main__":
    unittest.main()
