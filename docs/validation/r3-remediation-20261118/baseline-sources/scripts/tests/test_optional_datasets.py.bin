"""The migrated scanners must never prepare local databases in Ox."""

import tempfile
import unittest
from pathlib import Path

import support as S


class ToolboxDatasetOwnership(unittest.TestCase):
    def test_local_preparation_denied_before_writes(self):
        with tempfile.TemporaryDirectory(prefix="Ox dataset ownership ") as temporary:
            root = Path(temporary)
            review = root / "review.json"
            review.write_text("{}")
            for name in ("osv", "trivy", "grype"):
                with self.subTest(name=name):
                    run = S.run(
                        ["bash", str(S.ROOT / "scripts/security/prepare-datasets.sh"),
                         "--root", str(root), "--review", str(review),
                         "--download", "--only", name], capture_output=True)
                    self.assertNotEqual(run.returncode, 0)
                    self.assertIn(b"owned by toolbox", run.stderr)
                    self.assertFalse((root / ".cache/ox/security").exists())
                    self.assertEqual(set(root.iterdir()), {review})
