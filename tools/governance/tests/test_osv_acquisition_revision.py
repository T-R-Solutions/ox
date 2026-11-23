"""Reject unreviewed OSV document changes without rewriting historical registries."""

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
OSV_REVISION = importlib.import_module("osv_acquisition_revision")


class OSVDocumentSuccessors(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="ox-osv-documents-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.rows = OSV_REVISION.records(ROOT)
        for name in OSV_REVISION.fixture_paths(ROOT):
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((ROOT / name).read_bytes())

    def test_exact_successor_maps_to_observed_predecessor_only(self):
        for row in self.rows:
            name = row["destination"]
            data = (self.root / name).read_bytes()
            previous = (self.root / row["previous"]).read_bytes()
            self.assertEqual(OSV_REVISION.predecessor(self.root, name, data), previous)
            self.assertEqual(OSV_REVISION.predecessor(self.root, name, data + b"unknown"), data + b"unknown")
        self.assertEqual(OSV_REVISION.predecessor(self.root, "ordinary.md", b"ordinary"), b"ordinary")

    def test_unregistered_append_and_predecessor_downgrade_reject(self):
        for row in self.rows:
            target = self.root / row["destination"]
            current = target.read_bytes()
            invalid = (current.replace(b"## Authorities", b"## Lost authorities", 1)
                       if row["destination"] == "sdd/project.md" else current + b"\nUnreviewed change\n")
            self.assertNotEqual(invalid, current)
            for rejected in (invalid,
                             (self.root / row["previous"]).read_bytes()):
                target.write_bytes(rejected)
                with self.assertRaises(ValueError):
                    OSV_REVISION.predecessor(self.root, row["destination"], rejected)
            target.write_bytes(current)

    def test_missing_mutated_or_symlinked_metadata_and_preimages_reject(self):
        for name in (OSV_REVISION.REGISTRY, OSV_REVISION.CLOSURE_REGISTRY, OSV_REVISION.DECISION,
                     *[row["previous"] for row in self.rows]):
            target = self.root / name
            original = target.read_bytes()
            for mode in ("missing", "mutated", "symlink"):
                target.unlink()
                if mode == "mutated":
                    target.write_bytes(original + b"changed")
                elif mode == "symlink":
                    alias = self.root / "same-bytes.bin"
                    alias.write_bytes(original)
                    target.symlink_to(alias)
                with self.subTest(name=name, mode=mode), self.assertRaises(ValueError):
                    OSV_REVISION.records(self.root)
                if target.exists() or target.is_symlink():
                    target.unlink()
                target.write_bytes(original)

    def test_recalculated_registry_does_not_authorize_unknown_bytes(self):
        registry = self.root / OSV_REVISION.REGISTRY
        doc = json.loads(registry.read_bytes())
        target = self.root / self.rows[0]["destination"]
        target.write_bytes(target.read_bytes() + b"unreviewed")
        doc["records"][0]["sha256"] = hashlib.sha256(target.read_bytes()).hexdigest()
        registry.write_text(json.dumps(doc))
        with self.assertRaisesRegex(ValueError, "registry changed"):
            OSV_REVISION.predecessor(self.root, self.rows[0]["destination"], target.read_bytes())

    def test_closure_is_a_separate_exact_successor(self):
        original_registry = (ROOT / OSV_REVISION.REGISTRY).read_bytes()
        self.assertEqual(hashlib.sha256(original_registry).hexdigest(),
                         "72103f35d7c9271ca551d2114a2e82b13adcfe7d7809af4c10306e0813c24720")
        closure = [row for row in self.rows
                   if row["destination"] in OSV_REVISION.CLOSURE_DESTINATIONS]
        self.assertEqual(len(closure), 1)
        row = closure[0]
        target = self.root / row["destination"]
        target.write_bytes(target.read_bytes() + b"unreviewed closure")
        with self.assertRaises(OSV_REVISION.CurrentContentError):
            OSV_REVISION.predecessor(self.root, row["destination"], target.read_bytes())

    def test_schema_inventory_and_escaping_paths_reject_after_test_pin(self):
        original = (self.root / OSV_REVISION.REGISTRY).read_bytes()
        for mode in ("duplicate", "escape", "unknown", "empty", "bool-schema"):
            doc = json.loads(original)
            if mode == "duplicate":
                doc["records"].append(doc["records"][0])
            elif mode == "escape":
                doc["records"][0]["previous"] = "../outside"
            elif mode == "unknown":
                doc["records"][0]["destination"] = "docs/unreviewed.md"
            elif mode == "empty":
                doc["records"] = []
            else:
                doc["schema_version"] = True
            data = json.dumps(doc).encode()
            (self.root / OSV_REVISION.REGISTRY).write_bytes(data)
            with self.subTest(mode=mode), patch.object(OSV_REVISION, "REVIEWED", hashlib.sha256(data).hexdigest()), self.assertRaises(ValueError):
                OSV_REVISION.records(self.root)
