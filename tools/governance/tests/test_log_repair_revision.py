"""Exact-origin metadata preserves history without allowing arbitrary Markdown."""
import importlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'tools/governance/scripts'))
R = importlib.import_module('log_repair_revision')


class HistoricalOriginTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='ox-origin-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.rows = json.loads((ROOT / R.ORIGINS).read_text())['records']
        for name in [R.ORIGINS, *[row['source'] for row in self.rows]]:
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes((ROOT / name).read_bytes())

    def test_exact_original_locations_and_unlisted_sources(self):
        for row in self.rows:
            self.assertEqual(R.origin(self.root, row['source']), row['origin'])
        self.assertEqual(R.origin(self.root, 'docs/unlisted.md'), 'docs/unlisted.md')

    def test_unknown_bytes_missing_and_symlink_source_rejected(self):
        row = self.rows[0]
        path = self.root / row['source']
        data = path.read_bytes()
        path.write_bytes(data + b'\n[escape](../../../../../../outside.md)\n')
        with self.assertRaisesRegex(ValueError, 'source changed'):
            R.origin(self.root, row['source'])
        path.unlink()
        with self.assertRaises(ValueError):
            R.origin(self.root, row['source'])
        with self.assertRaises(ValueError):
            R.origin(self.root, 'docs/unlisted.md')
        other = self.root / 'other.bin'
        other.write_bytes(data)
        path.symlink_to(other)
        with self.assertRaisesRegex(ValueError, 'symlinked'):
            R.origin(self.root, row['source'])

    def test_recalculated_registry_and_escape_rejected(self):
        path = self.root / R.ORIGINS
        document = json.loads(path.read_text())
        document['records'][0]['origin'] = '../../outside.md'
        path.write_text(json.dumps(document))
        with self.assertRaisesRegex(ValueError, 'registry changed'):
            R.origin(self.root, self.rows[0]['source'])


class LogSuccessorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='ox-successor-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.rows = R.records(ROOT)
        self.row = next(row for row in self.rows if row['destination'] == 'sdd/project.md')
        historical = importlib.import_module('instruction_revision')
        self.historical = historical.REGISTRY
        for name in [self.historical, *R.fixture_paths(ROOT), *[row['destination'] for row in self.rows]]:
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((ROOT / name).read_bytes())

    def test_exact_successors_and_unrecognized_bytes(self):
        for row in self.rows:
            data = (self.root / row['destination']).read_bytes()
            expected = (self.root / row['previous']).read_bytes()
            self.assertEqual(R.predecessor(self.root, row['destination'], data), expected)
            self.assertEqual(R.predecessor(self.root, row['destination'], data + b'unknown'), data + b'unknown')
        self.assertTrue(R.original_branch(self.root, self.row['destination'],
                                         (self.root / self.row['destination']).read_bytes()))
        metadata = json.loads((self.root / R.REGISTRY).read_text())
        self.assertEqual(metadata['missing_intermediate']['status'], 'UNVERIFIED')

    def test_original_downgrade_and_corrupt_preimage_rejected(self):
        name = self.row['destination']
        target = self.root / name
        current = target.read_bytes()
        previous = self.root / self.row['previous']
        data = previous.read_bytes()
        target.write_bytes(data)
        with self.assertRaisesRegex(ValueError, 'downgrade'):
            R.predecessor(self.root, name, data)
        target.write_bytes(current)
        previous.write_bytes(data + b'changed')
        with self.assertRaisesRegex(ValueError, 'predecessor changed'):
            R.predecessor(self.root, name, current)

    def test_recalculated_metadata_and_historical_registry_tamper_rejected(self):
        name = self.row['destination']
        data = (self.root / name).read_bytes()
        registry = self.root / R.REGISTRY
        original = registry.read_bytes()
        document = json.loads(original)
        document['records'][0]['sha256'] = '0' * 64
        registry.write_text(json.dumps(document))
        with self.assertRaisesRegex(ValueError, 'registry changed'):
            R.predecessor(self.root, name, data)
        registry.write_bytes(original)
        historical = self.root / self.historical
        historical.write_bytes(historical.read_bytes() + b'changed')
        with self.assertRaisesRegex(ValueError, 'Historical instruction registry changed'):
            R.predecessor(self.root, name, data)

    def test_missing_and_symlink_metadata_or_preimage_rejected(self):
        name = self.row['destination']
        data = (self.root / name).read_bytes()
        for relative in [R.REGISTRY, self.row['previous']]:
            path = self.root / relative
            original = path.read_bytes()
            path.unlink()
            if relative == R.REGISTRY:
                self.assertEqual(R.predecessor(self.root, name, data), data)
                self.assertFalse(R.original_branch(self.root, name, data))
            else:
                with self.assertRaises(ValueError):
                    R.predecessor(self.root, name, data)
            replacement = self.root / 'replacement.bin'
            replacement.write_bytes(original)
            path.symlink_to(replacement)
            with self.assertRaisesRegex(ValueError, 'symlinked'):
                R.predecessor(self.root, name, data)
            path.unlink()
            path.write_bytes(original)


    def test_all_available_previous_terminals_are_rejected_as_live_downgrades(self):
        for row in self.rows:
            with self.subTest(path=row['destination']):
                path = self.root / row['destination']
                original = path.read_bytes()
                previous = (self.root / row['previous']).read_bytes()
                path.write_bytes(previous)
                with self.assertRaisesRegex(ValueError, 'downgrade'):
                    R.predecessor(self.root, row['destination'], previous)
                path.write_bytes(original)


class CopyHistoricalReferenceTests(unittest.TestCase):
    setUp = HistoricalOriginTests.setUp

    def test_only_twelve_exact_absent_pairs_in_declared_copy(self):
        instruction = importlib.import_module('instruction_revision')
        marker = self.root / instruction.COPY_CONTEXT
        marker.write_bytes(instruction.COPY_CONTEXT_BYTES)
        pairs = [(row['source'], name) for row in self.rows for name in row['excluded_targets']]
        self.assertEqual(len(pairs), 12)
        for source, name in pairs:
            self.assertTrue(R.excluded_reference(self.root, source, self.root / name))
        source, name = pairs[0]
        self.assertFalse(R.excluded_reference(self.root, 'docs/unlisted.md', self.root / name))
        self.assertFalse(R.excluded_reference(self.root, source, self.root / 'application/unlisted'))
        self.assertFalse(R.excluded_reference(self.root, source, self.root.parent / 'escape'))
        marker.unlink()
        self.assertFalse(R.excluded_reference(self.root, source, self.root / name))
        marker.write_bytes(instruction.COPY_CONTEXT_BYTES + b'changed')
        with self.assertRaises(ValueError):
            R.excluded_reference(self.root, source, self.root / name)

    def test_present_changed_and_symlink_targets_fail_closed(self):
        instruction = importlib.import_module('instruction_revision')
        (self.root / instruction.COPY_CONTEXT).write_bytes(instruction.COPY_CONTEXT_BYTES)
        row = next(row for row in self.rows if any(name.startswith('sdd/') for name in row['excluded_targets']))
        name = next(iter(row['excluded_targets']))
        target = self.root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(b'unreviewed target')
        self.assertFalse(R.excluded_reference(self.root, row['source'], target))
        with self.assertRaisesRegex(ValueError, 'target present'):
            R.origin(self.root, 'docs/unlisted.md')
        target.unlink()
        target.symlink_to(self.root / 'missing')
        self.assertFalse(R.excluded_reference(self.root, row['source'], target))
        with self.assertRaisesRegex(ValueError, 'target present'):
            R.origin(self.root, 'docs/unlisted.md')

    def test_missing_or_mutated_metadata_never_exempts_a_target(self):
        instruction = importlib.import_module('instruction_revision')
        (self.root / instruction.COPY_CONTEXT).write_bytes(instruction.COPY_CONTEXT_BYTES)
        row = next(row for row in self.rows if row['excluded_targets'])
        target = self.root / next(iter(row['excluded_targets']))
        metadata = self.root / R.ORIGINS
        content = metadata.read_bytes()
        metadata.write_bytes(content + b'changed')
        with self.assertRaisesRegex(ValueError, 'registry changed'):
            R.excluded_reference(self.root, row['source'], target)
        metadata.unlink()
        self.assertFalse(R.excluded_reference(self.root, row['source'], target))
        (self.root / R.REGISTRY).write_text('fixture-presence-only')
        with self.assertRaisesRegex(ValueError, 'Missing historical origin registry'):
            R.excluded_reference(self.root, row['source'], target)


    def test_lexical_symlink_is_rejected_before_resolve_hides_it(self):
        folder = self.root / 'links'
        folder.mkdir()
        alias = folder / 'alias'
        alias.symlink_to(self.root / 'missing-dir')
        target = alias / '..' / 'target'
        self.assertTrue(R.symlinked(self.root, target))
        self.assertFalse(R.symlinked(self.root, target.resolve()))
        alias.unlink()
        alias.symlink_to(self.root)
        self.assertTrue(R.symlinked(self.root, alias / 'inside'))
        self.assertFalse(R.symlinked(self.root, self.root / 'ordinary'))
