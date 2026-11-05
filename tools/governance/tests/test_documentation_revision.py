"""Exact visual-method succession, denied mutations and independent-copy recovery."""
from pathlib import Path
import hashlib
import importlib.util
import json
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'tools/governance/scripts'))
import documentation_revision as D
from governance_support import copy_distribution, preservation_bytes


class DocumentationRevisionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='ox-documentation-revision-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        names = {D.REGISTRY, D.DECISION} | D.EXISTING | D.ADDED
        names |= {r['previous'] for r in D.records(ROOT).values() if r['previous']}
        for name in names:
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((ROOT / name).read_bytes())

    def test_exact_predecessors_and_unknown_mutations(self):
        self.assertEqual(D.errors(self.root), [])
        for name, row in D.records(self.root).items():
            data = (self.root / name).read_bytes()
            actual = D.predecessor(self.root, name, data)
            expected = (self.root / row['previous']).read_bytes() if row['previous'] else data
            self.assertEqual(actual, expected)
            changed = data + b'\nunknown mutation\n'
            self.assertEqual(D.predecessor(self.root, name, changed), changed)
        self.assertEqual(D.predecessor(self.root, 'unrelated', b'data'), b'data')

    def test_each_current_corruption_deletion_and_symlink_is_rejected(self):
        for name in D.EXISTING | D.ADDED:
            target = self.root / name
            data = target.read_bytes()
            with self.subTest(path=name):
                target.write_bytes(data + b'corrupt')
                self.assertTrue(D.errors(self.root))
                target.unlink()
                self.assertTrue(D.errors(self.root))
                replacement = self.root / 'identical.bin'
                replacement.write_bytes(data)
                target.symlink_to(replacement)
                self.assertTrue(D.errors(self.root))
                target.unlink()
                target.write_bytes(data)

    def test_invalid_registry_scope_and_duplicate_properties_are_rejected(self):
        path = self.root / D.REGISTRY
        original = path.read_text()
        for mutation in ('duplicate', 'missing', 'extra', 'digest', 'predecessor', 'revision', 'decision'):
            document = json.loads(original)
            rows = document['records']
            if mutation == 'duplicate': rows.append(dict(rows[0]))
            elif mutation == 'missing': rows.pop()
            elif mutation == 'extra': rows.append(dict(rows[0], destination='unreviewed.md'))
            elif mutation == 'digest': rows[0]['sha256'] = 'invalid'
            elif mutation == 'predecessor':
                next(r for r in rows if r['destination'] in D.EXISTING)['previous'] = '../outside'
            elif mutation == 'revision': document['revision'] = 'unreviewed'
            else: document['decision'] = 'unreviewed.md'
            path.write_text(json.dumps(document))
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                D.records(self.root)
        path.write_text(original.replace('"schema_version": 1', '"schema_version": 1, "schema_version": 1'))
        with self.assertRaises(ValueError): D.records(self.root)
        path.write_text(original)
        path.unlink()
        with self.assertRaises(ValueError): D.records(self.root)

    def test_predecessor_corruption_absence_and_symlink_are_rejected(self):
        for row in D.records(self.root).values():
            if row['previous'] is None: continue
            target = self.root / row['previous']
            original = target.read_bytes()
            target.write_bytes(original + b'corrupt')
            with self.assertRaises(ValueError): D.records(self.root)
            target.unlink()
            with self.assertRaises(ValueError): D.records(self.root)
            identical = self.root / 'predecessor.bin'
            identical.write_bytes(original)
            target.symlink_to(identical)
            with self.assertRaises(ValueError): D.records(self.root)
            target.unlink()
            target.write_bytes(original)


class DocumentationDistributionTests(unittest.TestCase):
    integration = True

    def test_independent_copy_preserves_original_method_and_rejects_extra_resource(self):
        with tempfile.TemporaryDirectory(prefix='ox-documentation-copy-') as destination:
            root = Path(destination)
            copy_distribution(ROOT, root)
            self.assertEqual(D.errors(root), [])
            for name in D.EXISTING | D.ADDED:
                self.assertEqual((root / name).read_bytes(), (ROOT / name).read_bytes())
            copied = json.loads((root / 'docs/structure/files.json').read_text())['revisions'][0]['records']
            source = next(r for r in copied if r['destination'] == 'skills/technical-documentation/SKILL.md')
            self.assertEqual(hashlib.sha256(preservation_bytes(root, D.SKILL + 'SKILL.md')).hexdigest(), source['source_sha256'])
            spec = importlib.util.spec_from_file_location('documentation_checker', ROOT / 'tools/governance/scripts/check-ox.py')
            checker = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(checker)
            baseline = checker.check(root)
            extra = root / D.SKILL / 'references' / 'unreviewed.md'
            extra.write_text('unreviewed')
            errors = checker.check(root)
            self.assertEqual([x for x in errors if x not in baseline], [
                'Unexpected copied resource: ' + str(extra.relative_to(root))])
