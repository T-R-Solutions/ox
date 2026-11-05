"""Exercise preserved originals and reject unregistered document mutations."""
from pathlib import Path
import hashlib
import json
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'tools/governance/scripts'))
from governance_support import documentary_predecessor

REGISTRY = 'docs/validation/f0-reconciliation-20261101/document-succession.json'


class DocumentSuccessionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.document = json.loads((ROOT / REGISTRY).read_text())
        self.registry = self.root / REGISTRY
        self.registry.parent.mkdir(parents=True)
        self.registry.write_bytes((ROOT / REGISTRY).read_bytes())
        for row in self.document['records']:
            for key in ('destination', 'previous'):
                target = self.root / row[key]
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes((ROOT / row[key]).read_bytes())

    def test_recovers_exact_original_and_rejects_unknown_current(self):
        for row in self.document['records']:
            name = row['destination']
            current = (self.root / name).read_bytes()
            expected = (self.root / row['previous']).read_bytes()
            self.assertEqual(documentary_predecessor(self.root, name, current), expected)
            self.assertEqual(hashlib.sha256(expected).hexdigest(), row['previous_sha256'])
            changed = current + b'\nunregistered semantic change\n'
            self.assertEqual(documentary_predecessor(self.root, name, changed), changed)

    def test_corrupt_missing_and_escaping_predecessor_fail(self):
        row = self.document['records'][0]
        name = row['destination']
        current = (self.root / name).read_bytes()
        path = self.root / row['previous']
        original = path.read_bytes()
        path.write_bytes(original + b'corrupt')
        with self.assertRaises(ValueError):
            documentary_predecessor(self.root, name, current)
        path.unlink()
        with self.assertRaises(ValueError):
            documentary_predecessor(self.root, name, current)
        row['previous'] = '../outside'
        self.registry.write_text(json.dumps(self.document))
        with self.assertRaises(ValueError):
            documentary_predecessor(self.root, name, current)

    def test_scope_duplicate_and_invalid_digest_fail(self):
        original = self.registry.read_text()
        for mutation in ('extra', 'missing', 'duplicate', 'digest', 'revision'):
            doc = json.loads(original)
            if mutation == 'extra':
                doc['records'].append(dict(doc['records'][0], destination='README.md'))
            elif mutation == 'missing':
                doc['records'].pop()
            elif mutation == 'duplicate':
                doc['records'].append(doc['records'][0])
            elif mutation == 'digest':
                doc['records'][0]['sha256'] = 'not a digest'
            else:
                doc['revision'] = 'unreviewed'
            self.registry.write_text(json.dumps(doc))
            with self.assertRaises(ValueError):
                documentary_predecessor(self.root, 'unrelated', b'unchanged')

    def test_unrelated_file_is_not_rewritten(self):
        self.assertEqual(documentary_predecessor(self.root, 'unrelated', b'data'), b'data')
