"""Exact documentary succession cannot authorize arbitrary or downgraded bytes."""

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools/governance/scripts"))
C = __import__("closure_revision")


class NativeExecSuccession(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.doc = json.loads((ROOT / C.NATIVE_REGISTRY).read_text())
        names = [C.NATIVE_REGISTRY, self.doc["review"]]
        for row in self.doc["records"]:
            names.extend([row["destination"], row["previous"]])
        operational = json.loads((ROOT / C.OPERATIONAL_REGISTRY).read_text())
        names.extend([C.OPERATIONAL_REGISTRY, operational["review"]])
        names.extend(row["previous"] for row in operational["records"])
        repair = json.loads((ROOT / C.REPAIR_REGISTRY).read_text())
        names.append(C.REPAIR_REGISTRY)
        for row in repair["records"]:
            names.extend([row["destination"], row["previous"]])
        maintenance = json.loads((ROOT / C.MAINTENANCE_REGISTRY).read_text())
        names.append(C.MAINTENANCE_REGISTRY)
        names.extend(row["previous"] for row in maintenance["records"])
        for registry in (C.CONFIGURATION_REGISTRY, C.VISUAL_REGISTRY, C.COMPLETE_REGISTRY, C.DEFAULTS_REGISTRY):
            names.append(registry)
            names.extend(row['previous'] for row in json.loads((ROOT / registry).read_text())['records'])
        import instruction_revision as I
        names.extend([I.REGISTRY, I.DECISION])
        names.extend(row['previous'] for row in json.loads((ROOT / I.REGISTRY).read_text())['records'])
        import log_repair_revision
        names = list(names) + log_repair_revision.fixture_paths(ROOT)
        for name in names:
            p = self.root / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes((ROOT / name).read_bytes())

    def test_reviewed_unknown_and_downgrade(self):
        for row in self.doc["records"]:
            name = row["destination"]
            p = self.root / name
            current = p.read_bytes()
            previous = (self.root / row["previous"]).read_bytes()
            self.assertEqual(
                C.native_exec_predecessor(
                    self.root, name, C.operational_predecessor(self.root, name, C.repair_predecessor(self.root, name, C.maintenance_predecessor(self.root, name, C.visual_predecessor(self.root, name, C.configuration_predecessor(self.root, name, current)))))
                ),
                previous,
            )
            self.assertEqual(
                C.native_exec_predecessor(self.root, name, current + b"unknown"),
                current + b"unknown",
            )
            p.write_bytes(previous)
            with self.assertRaisesRegex(ValueError, "downgrade"):
                C.native_exec_predecessor(self.root, name, previous)

    def test_missing_corrupt_symlink_preimage(self):
        row = self.doc["records"][0]
        p = self.root / row["previous"]
        old = p.read_bytes()
        current = (self.root / row["destination"]).read_bytes()
        for mode in ("missing", "corrupt", "symlink"):
            p.unlink()
            if mode == "corrupt":
                p.write_bytes(old + b"corrupt")
            if mode == "symlink":
                p.symlink_to(ROOT / row["previous"])
            with self.assertRaises(ValueError):
                C.native_exec_predecessor(self.root, row["destination"], current)
            if p.is_symlink() or p.exists():
                p.unlink()
            p.write_bytes(old)

    def test_recalculated_registry_is_rejected(self):
        self.doc["records"][0]["sha256"] = hashlib.sha256(b"unknown").hexdigest()
        (self.root / C.NATIVE_REGISTRY).write_text(json.dumps(self.doc))
        with self.assertRaisesRegex(ValueError, "registry changed"):
            C.native_exec_predecessor(self.root, "README.md", b"unknown")

    def test_historical_observations_preserved_and_no_current_approval(self):
        base = ROOT / "docs/validation/toolbox-governance-reconciliation"
        old = json.loads(
            (
                base
                / "recovery/sdd/features/scripts-toolchain-config/evidence.json.bin"
            ).read_text()
        )
        new = json.loads(
            (ROOT / "sdd/features/scripts-toolchain-config/evidence.json").read_text()
        )
        ids = {
            "E-OWNERSHIP-RECOVERY-TESTS",
            "E-OWNERSHIP-RECOVERY-REVIEW-FINAL",
            "E-OWNERSHIP-CLEANUP-REEXAMINATION",
            "E-OWNERSHIP-RECOVERY-COPY",
        }
        for item in old["evidence"]:
            if item["id"] in ids:
                self.assertIn(item, new["historical_evidence"])
                self.assertNotIn(item, new["evidence"])
        for q in new["requirements"]:
            if q["id"] in ("AC-05", "AC-06", "AC-07"):
                if q["status"] == "APPROVED":
                    self.assertIn("E-OPERATIONAL-COMPLETION", q["evidence_ids"])
                else:
                    self.assertEqual(q["status"], "UNVERIFIED")
                self.assertFalse(set(q["evidence_ids"]) & ids)
        for name in ("toolbox.json", "toolbox.images.lock.json"):
            self.assertFalse((ROOT / "scripts/config" / name).exists())
