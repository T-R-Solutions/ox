"""Behavioral integrity checks for the bounded skill import and its recovery path."""
from pathlib import Path
import hashlib
import importlib.util
import json
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'tools/governance/scripts'))
from skill_revision import records, predecessor, errors, EXISTING, ADDED, REVISION
import readme_revision as R
from governance_support import copy_distribution


def checker():
    spec = importlib.util.spec_from_file_location('readme_import_checker', ROOT/'tools/governance/scripts/check-ox.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ReadmeImportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in ['docs/structure/files.json', 'docs/decisions/readme-skill-integration.md', *EXISTING, *ADDED]:
            self.copy(name)
        for name in [R.REGISTRY, R.DECISION, R.PREVIOUS, R.VISUAL_REGISTRY, R.VISUAL_DECISION, R.VISUAL_PREVIOUS]:
            self.copy(name)
        for row in records(ROOT).values():
            if row['previous'] is not None:
                self.copy(row['previous'])

    def copy(self, name):
        p = self.root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes((ROOT/name).read_bytes())

    def test_registered_files_recover_exact_predecessors(self):
        self.assertEqual(errors(self.root), [])
        for name, row in records(self.root).items():
            current = (self.root/name).read_bytes()
            recovered = predecessor(self.root, name, current)
            if row['previous'] is None:
                self.assertEqual(recovered, current)
            else:
                self.assertEqual(hashlib.sha256(recovered).hexdigest(), row['previous_sha256'])
            altered = current + b'\nnot reviewed\n'
            self.assertEqual(predecessor(self.root, name, altered), altered)
        self.assertEqual(predecessor(self.root, 'unrelated', b'unchanged'), b'unchanged')

    def test_every_registered_current_mutation_or_deletion_is_rejected(self):
        for name in EXISTING | ADDED:
            p = self.root/name
            original = p.read_bytes()
            with self.subTest(name=name):
                p.write_bytes(original+b'\ncorrupt\n')
                self.assertTrue(errors(self.root))
                p.unlink()
                self.assertTrue(errors(self.root))
                p.write_bytes(original)

    def test_missing_corrupt_escaping_or_symlink_predecessor_is_rejected(self):
        row = next(x for x in records(self.root).values() if x['previous'])
        p = self.root/row['previous']
        original = p.read_bytes()
        p.write_bytes(original+b'corrupt')
        with self.assertRaises(ValueError): records(self.root)
        p.unlink()
        with self.assertRaises(ValueError): records(self.root)
        p.write_bytes(original)
        doc = json.loads((self.root/'docs/structure/files.json').read_text())
        revision = next(x for x in doc['revisions'] if x['id']==REVISION)
        next(x for x in revision['records'] if x['destination']==row['destination'])['previous']='../outside'
        (self.root/'docs/structure/files.json').write_text(json.dumps(doc))
        with self.assertRaises(ValueError): records(self.root)
        self.copy('docs/structure/files.json')
        replacement=self.root/'same-bytes.bin';replacement.write_bytes(original)
        p.unlink();p.symlink_to(replacement)
        with self.assertRaises(ValueError): records(self.root)

    def test_scope_decision_and_digest_mutations_are_rejected(self):
        p = self.root/'docs/structure/files.json';original=p.read_text()
        for mutation in ['extra','missing','duplicate','digest','decision','revision']:
            d=json.loads(original);rev=next(x for x in d['revisions'] if x['id']==REVISION)
            if mutation=='extra':rev['records'].append(dict(rev['records'][0],destination='unexpected'))
            elif mutation=='missing':rev['records'].pop()
            elif mutation=='duplicate':rev['records'].append(rev['records'][0])
            elif mutation=='digest':rev['records'][0]['sha256']='0'
            elif mutation=='decision':rev['decision']='unreviewed.md'
            else:d['revisions'].remove(rev)
            p.write_text(json.dumps(d))
            with self.subTest(mutation=mutation), self.assertRaises(ValueError): records(self.root)
        p.write_text(original)

    def test_new_resource_and_metadata_bytes_are_actually_protected(self):
        p=self.root/'.codex/skills/readme-lifecycle-engineering/agents/openai.yaml'
        p.write_bytes(p.read_bytes().replace(b'README',b'FALSE'))
        self.assertTrue(any('agents/openai.yaml' in x for x in errors(self.root)))

    def test_successor_registry_and_preimage_fail_closed(self):
        expected = records(self.root)['README.md']['sha256']
        registry = self.root / R.REGISTRY
        original = registry.read_bytes()
        for mutation in ('scope', 'duplicate', 'digest', 'binding', 'escape', 'decision', 'revision'):
            doc = json.loads(original)
            if mutation == 'scope': doc['records'][0]['destination'] = 'unreviewed.md'
            elif mutation == 'duplicate': doc['records'].append(dict(doc['records'][0]))
            elif mutation == 'digest': doc['records'][0]['sha256'] = 'bad'
            elif mutation == 'binding': doc['records'][0]['previous_sha256'] = '0' * 64
            elif mutation == 'escape': doc['records'][0]['previous'] = '../outside'
            elif mutation == 'decision': doc['decision'] = 'unreviewed.md'
            else: doc['revision'] = 'unreviewed'
            registry.write_text(json.dumps(doc))
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                errors(self.root)
        registry.write_bytes(original.replace(b'"schema_version": 1', b'"schema_version": 1, "schema_version": 1'))
        with self.assertRaises(ValueError): errors(self.root)
        registry.unlink()
        with self.assertRaises(ValueError): errors(self.root)
        registry.write_bytes(original)
        for name in [R.REGISTRY, R.DECISION, R.PREVIOUS]:
            path = self.root / name
            data = path.read_bytes()
            if name == R.PREVIOUS:
                path.write_bytes(data + b'corrupt')
                with self.assertRaises(ValueError): errors(self.root)
            path.unlink()
            with self.assertRaises(ValueError): errors(self.root)
            other = self.root / 'same-bytes.bin'
            other.write_bytes(data)
            path.symlink_to(other)
            with self.assertRaises(ValueError): errors(self.root)
            path.unlink()
            path.write_bytes(data)
        self.assertEqual(R.record(self.root, expected)['previous_sha256'], expected)

    def test_visual_successor_corruption_and_downgrade_fail(self):
        original = (self.root / R.VISUAL_REGISTRY).read_bytes()
        for mutation in ('scope', 'duplicate', 'binding', 'escape', 'revision', 'decision', 'digest'):
            doc = json.loads(original)
            if mutation == 'scope': doc['records'][0]['destination'] = 'unexpected.md'
            elif mutation == 'duplicate': doc['records'].append(dict(doc['records'][0]))
            elif mutation == 'binding': doc['records'][0]['previous_sha256'] = '0' * 64
            elif mutation == 'escape': doc['records'][0]['previous'] = '../outside'
            elif mutation == 'revision': doc['revision'] = 'unexpected'
            elif mutation == 'decision': doc['decision'] = 'unexpected.md'
            else: doc['records'][0]['sha256'] = 'invalid'
            (self.root / R.VISUAL_REGISTRY).write_text(json.dumps(doc))
            with self.subTest(mutation=mutation), self.assertRaises(ValueError): errors(self.root)
        (self.root / R.VISUAL_REGISTRY).write_bytes(original.replace(b'"schema_version": 1', b'"schema_version": 1, "schema_version": 1'))
        with self.assertRaises(ValueError): errors(self.root)
        (self.root / R.VISUAL_REGISTRY).write_bytes(original)
        for name in [R.VISUAL_REGISTRY, R.VISUAL_DECISION, R.VISUAL_PREVIOUS]:
            p = self.root / name
            data = p.read_bytes()
            if name == R.VISUAL_PREVIOUS:
                p.write_bytes(data+b'corrupt')
                with self.assertRaises(ValueError): errors(self.root)
            p.unlink()
            with self.assertRaises(ValueError): errors(self.root)
            replacement = self.root/'visual-preimage.bin'
            replacement.write_bytes(data)
            p.symlink_to(replacement)
            with self.assertRaises(ValueError): errors(self.root)
            p.unlink(); p.write_bytes(data)
        (self.root/'README.md').write_bytes((self.root/R.VISUAL_PREVIOUS).read_bytes())
        self.assertTrue(errors(self.root))

    def test_downgrade_to_original_integration_readme_is_rejected(self):
        (self.root / 'README.md').write_bytes((self.root / R.PREVIOUS).read_bytes())
        self.assertTrue(errors(self.root))

    def test_successor_rejects_symlinked_parent(self):
        parent = self.root / R.BASE / 'before'
        replacement = self.root / 'moved-before'
        parent.rename(replacement)
        parent.symlink_to(replacement, target_is_directory=True)
        with self.assertRaises(ValueError): errors(self.root)



class ReadmeDistributionTests(unittest.TestCase):
    integration = True

    def test_excluded_references_remain_exact_and_governance_links_are_required(self):
        with tempfile.TemporaryDirectory() as destination:
            root = Path(destination)
            copy_distribution(ROOT, root)
            app = root / 'application/README.md'
            self.assertTrue(R.excluded_product_reference(root, 'README.md', app))
            self.assertFalse(R.excluded_product_reference(root, 'README.md', root/'application/missing.rs'))
            self.assertFalse(R.excluded_product_reference(root, 'README.md', root/'docs/missing.md'))
            self.assertFalse(R.excluded_product_reference(root, 'README.md', root.parent/'outside'))
            readme = root/'README.md'
            original = readme.read_bytes()
            readme.write_bytes(original + b'changed')
            self.assertFalse(R.excluded_product_reference(root, 'README.md', app))
            readme.write_bytes(original)
            (root/'application').mkdir()
            self.assertFalse(R.excluded_product_reference(root, 'README.md', app))

    def test_independent_distribution_retains_import_and_preserved_originals(self):
        with tempfile.TemporaryDirectory() as destination:
            root=Path(destination);copy_distribution(ROOT,root)
            self.assertEqual(errors(root), [])
            for name in EXISTING | ADDED:
                self.assertEqual((root/name).read_bytes(),(ROOT/name).read_bytes())
            self.assertEqual(checker().check(root), [])
            extra=root/'.codex/skills/readme-lifecycle-engineering/references/unreviewed.md'
            extra.write_text('unexpected resource')
            self.assertTrue(any('Unexpected copied resource' in x for x in checker().check(root)))

