"""RustSec reviewed imports remain operational after database ownership changes."""

import datetime
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

import support as S


class RustSecPreparation(unittest.TestCase):
    def test_reviewed_import_and_corruption_preserve_registry(self):
        with tempfile.TemporaryDirectory(prefix="Ox RustSec import ") as temporary:
            root = Path(temporary)
            origin = root / "imports/rustsec"
            origin.mkdir(parents=True)
            def git(*args):
                return subprocess.check_output(["git", "-C", str(origin), *args], stderr=subprocess.PIPE).decode().strip()
            git("init")
            git("remote", "add", "origin", "https://github.com/RustSec/advisory-db.git")
            (origin / "advisory.md").write_text("controlled advisory fixture")
            git("add", "advisory.md")
            git("-c", "user.name=Ox Fixture", "-c", "user.email=fixture@example.invalid", "-c", "commit.gpgsign=false", "commit", "-m", "fixture")
            day = git("show", "-s", "--format=%cs", "HEAD")
            review = {"source": "https://github.com/RustSec/advisory-db.git", "revision": git("rev-parse", "HEAD"),
                      "dataset_date": day, "valid_until": datetime.datetime.now(datetime.UTC).date().isoformat(),
                      "license": "fixture", "reviewer": "test", "provenance": "controlled Git fixture",
                      "sha256": S.tree_identity(origin)}
            review_file = root / "review.json"
            review_file.write_text(json.dumps({"rustsec": review}))
            binary = root / "bin"
            binary.mkdir()
            scanner = binary / "cargo-audit"
            scanner.write_text("#!/bin/sh\nif [ \"$1\" = \"--version\" ]; then echo fixture; else echo '{\"vulnerabilities\":{}}'; fi\n")
            scanner.chmod(0o755)
            (root / "application").mkdir()
            (root / "application/Cargo.lock").write_text("version = 4\n")
            argv = ["bash", str(S.ROOT / "scripts/security/prepare-datasets.sh"), "--root", str(root),
                    "--review", str(review_file), "--import", str(root / "imports")]
            env = dict(os.environ, PATH=str(binary) + ":/usr/bin:/bin")
            run = subprocess.run(argv, capture_output=True, env=env)
            self.assertEqual(run.returncode, 0, run.stderr)
            registry = root / ".cache/ox/security/datasets.json"
            before = registry.read_bytes()
            self.assertEqual(list(json.loads(before)), ["rustsec"])
            (origin / "advisory.md").write_text("corrupted")
            run = subprocess.run(argv, capture_output=True, env=env)
            self.assertNotEqual(run.returncode, 0)
            self.assertEqual(registry.read_bytes(), before)
