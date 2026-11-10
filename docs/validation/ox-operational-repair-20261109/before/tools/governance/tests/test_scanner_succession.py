"""Content-bound scanner successor, including active downgrades and corruption."""

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(
    0, str(Path(__file__).resolve().parents[3] / "tools/governance/scripts")
)
import closure_revision as C
from governance_support import copy_distribution

ROOT = Path(__file__).resolve().parents[3]


class ScannerSuccession(unittest.TestCase):
    integration = True

    def test_current_unknown_downgrade_and_recovery_corruption(self):
        with tempfile.TemporaryDirectory(prefix="ox-scanner-copy-") as temporary:
            root = Path(temporary)
            copy_distribution(ROOT, root)
            registry = root / C.REMEDIATION_REGISTRY
            for row in json.loads(registry.read_text())["records"]:
                name = row["destination"]
                target = root / name
                current = target.read_bytes()
                previous = (root / row["previous"]).read_bytes()
                self.assertEqual(
                    C.remediation_predecessor(
                        root, name, C.ownership_predecessor(root, name, C.native_exec_predecessor(root, name, current))
                    ), previous
                )
                self.assertEqual(
                    C.remediation_predecessor(root, name, current + b"unknown"),
                    current + b"unknown",
                )
                target.write_bytes(previous)
                with self.assertRaisesRegex(ValueError, "downgrade"):
                    C.remediation_predecessor(root, name, previous)
                target.write_bytes(current)
                (root / row["previous"]).write_bytes(previous + b"corrupt")
                with self.assertRaisesRegex(ValueError, "predecessor changed"):
                    C.remediation_predecessor(root, name, current)
                (root / row["previous"]).write_bytes(previous)
            registry.write_text("{}")
            with self.assertRaisesRegex(ValueError, "registry changed"):
                C.remediation_predecessor(
                    root, "README.md", (root / "README.md").read_bytes()
                )


class OwnershipSuccession(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="ox-ownership-succession-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.registry = self.root / C.OWNERSHIP_REGISTRY
        document = json.loads((ROOT / C.OWNERSHIP_REGISTRY).read_text())
        self.row = document["records"][0]
        self.review = document["review"]
        for relative in (
            C.OWNERSHIP_REGISTRY, self.review,
            self.row["previous"], self.row["destination"],
        ):
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((ROOT / relative).read_bytes())
        # This unit fixture exercises the ownership transition's terminal bytes.
        # Later native exec successors are tested through the complete chain above.
        native = json.loads((ROOT / C.NATIVE_REGISTRY).read_text())
        for row in native['records']:
            if row['destination'] == self.row['destination']:
                (self.root / row['destination']).write_bytes((ROOT / row['previous']).read_bytes())
        self.current = (self.root / self.row["destination"]).read_bytes()

    def observe(self, data=None):
        return C.ownership_predecessor(
            self.root, self.row["destination"], self.current if data is None else data
        )

    def test_exact_successor_unknown_and_active_downgrade(self):
        previous = (self.root / self.row["previous"]).read_bytes()
        self.assertEqual(self.observe(), previous)
        self.assertEqual(self.observe(self.current + b"unknown"), self.current + b"unknown")
        (self.root / self.row["destination"]).write_bytes(previous)
        with self.assertRaisesRegex(ValueError, "downgrade"):
            self.observe(previous)

    def test_registry_review_and_preimage_corruption_or_loss(self):
        for relative in (C.OWNERSHIP_REGISTRY, self.review, self.row["previous"]):
            path = self.root / relative
            original = path.read_bytes()
            with self.subTest(path=relative, mutation="corrupt"):
                path.write_bytes(original + b"unknown")
                with self.assertRaises(ValueError):
                    self.observe()
                path.write_bytes(original)
            with self.subTest(path=relative, mutation="missing"):
                path.unlink()
                with self.assertRaises(ValueError):
                    self.observe()
                path.write_bytes(original)

    def test_symlinks_and_escaping_parent_rejected(self):
        for relative in (C.OWNERSHIP_REGISTRY, self.review, self.row["previous"]):
            path = self.root / relative
            original = path.read_bytes()
            with self.subTest(path=relative):
                path.unlink()
                path.symlink_to("/etc/passwd")
                with self.assertRaises(ValueError):
                    self.observe()
                path.unlink()
                path.write_bytes(original)
        before = (self.root / self.row["previous"]).parent
        moved = self.root / "unexpected-parent"
        before.rename(moved)
        before.symlink_to(moved, target_is_directory=True)
        with self.assertRaises(ValueError):
            self.observe()
