"""Fail-closed project transition checks with diagnostic assertions."""

import json
import unittest
from pathlib import Path

import project_revision as P
from skill_revision import errors, predecessor, records
from test_readme_skill_integration import ReadmeImportTests


class ProjectRevisionTests(unittest.TestCase):
    setUp = ReadmeImportTests.setUp
    copy = ReadmeImportTests.copy

    def test_reviewed_chain_and_original_consumers(self):
        self.assertEqual(errors(self.root), [])
        row = records(self.root)["sdd/project.md"]
        data = (self.root / "sdd/project.md").read_bytes()
        self.assertEqual(
            predecessor(self.root, "sdd/project.md", data),
            (self.root / row["previous"]).read_bytes(),
        )
        self.assertEqual(
            predecessor(self.root, "sdd/project.md", data + b"unknown"),
            data + b"unknown",
        )
        for name in ["README.md", "sdd/project.md"]:
            p = self.root / name
            original = p.read_bytes()
            changed = (original.replace(b"## Authorities", b"## Lost authorities", 1)
                       if name == "sdd/project.md" else original + b"unknown")
            self.assertNotEqual(changed, original)
            p.write_bytes(changed)
            self.assertTrue(
                any(
                    ("current" in e and ("README" in e or "Project succession" in e))
                    for e in errors(self.root)
                )
            )
            p.write_bytes(original)
        for name in P.PREIMAGES:
            (self.root / "sdd/project.md").write_bytes((self.root / name).read_bytes())
            self.assertIn(
                "Project succession current digest mismatch", errors(self.root)
            )

    def test_invalid_ambiguous_scope_and_digest_reasons(self):
        p = self.root / P.REGISTRY
        original = p.read_text()
        for mutation, reason in [
            ("scope", "scope"),
            ("escape", "scope"),
            ("absolute", "scope"),
            ("count", "transition count"),
            ("binding", "binding"),
            ("digest", "binding"),
            ("review", "review digest"),
            ("invalid", "Invalid project"),
        ]:
            d = json.loads(original)
            if mutation == "scope":
                d["records"][0]["destination"] = "README.md"
            elif mutation == "escape":
                d["records"][0]["previous"] = "../outside"
            elif mutation == "absolute":
                d["records"][0]["previous"] = "/tmp/outside"
            elif mutation == "count":
                d["records"].append(d["records"][0])
            elif mutation == "binding":
                d["records"][1]["previous_sha256"] = "0" * 64
            elif mutation == "digest":
                d["records"][1]["sha256"] = "bad"
            elif mutation == "review":
                d["review_sha256"] = "0" * 64
            else:
                d["schema_version"] = 2
            p.write_text(json.dumps(d))
            with (
                self.subTest(mutation=mutation),
                self.assertRaisesRegex(ValueError, reason),
            ):
                errors(self.root)
        p.write_text(
            original.replace(
                '"schema_version": 1', '"schema_version": 1, "schema_version": 1'
            )
        )
        with self.assertRaisesRegex(ValueError, "Duplicate README successor property"):
            errors(self.root)
        p.write_text("[]")
        with self.assertRaisesRegex(ValueError, "Invalid project succession record"):
            errors(self.root)

    def test_preimages_review_registry_and_links(self):
        for name in [*P.PREIMAGES, P.REVIEW, P.REGISTRY]:
            p = self.root / name
            data = p.read_bytes()
            if name != P.REGISTRY:
                p.write_bytes(data + b"corrupt")
                with self.assertRaisesRegex(ValueError, "digest mismatch"):
                    errors(self.root)
            p.unlink()
            with self.assertRaisesRegex(ValueError, "Missing"):
                errors(self.root)
            other = self.root / "substitute"
            other.write_bytes(data)
            p.symlink_to(other)
            with self.assertRaisesRegex(ValueError, "symlinked"):
                errors(self.root)
            p.unlink()
            p.write_bytes(data)
        parent = (self.root / P.PREIMAGES[1]).parent
        other = self.root / "moved"
        parent.rename(other)
        parent.symlink_to(other, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symlinked"):
            errors(self.root)

    def test_external_parent_and_current_link(self):
        p = self.root / "sdd/project.md"
        data = p.read_bytes()
        p.unlink()
        p.symlink_to(Path("/etc/passwd"))
        self.assertTrue(
            any("changed/missing" in e or "symlinked" in e for e in errors(self.root))
        )
        p.unlink()
        p.write_bytes(data)
        parent = (self.root / P.PREIMAGES[1]).parent
        import tempfile

        with tempfile.TemporaryDirectory() as outside:
            (Path(outside) / "project.md.bin").write_bytes(
                (parent / "project.md.bin").read_bytes()
            )
            parent.rename(self.root / "saved")
            parent.symlink_to(outside, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "escaping or symlinked"):
                errors(self.root)

    def test_rehashing_unreviewed_bytes_does_not_authorize_a_transition(self):
        import hashlib

        p = self.root / "sdd/project.md"
        p.write_bytes(p.read_bytes() + b"unreviewed")
        registry = self.root / P.REGISTRY
        doc = json.loads(registry.read_text())
        doc["records"][-1]["sha256"] = hashlib.sha256(p.read_bytes()).hexdigest()
        registry.write_text(json.dumps(doc))
        with self.assertRaisesRegex(ValueError, "digest binding mismatch"):
            errors(self.root)
