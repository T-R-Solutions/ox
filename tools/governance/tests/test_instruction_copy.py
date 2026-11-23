"""Explicit consumer receipts, observed profiles and mandatory live-source checking."""
import importlib
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'tools/governance/scripts'))
R = importlib.import_module('instruction_revision')
product_record = importlib.import_module('governance_support').product_record


class InstructionCopyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='ox-declared-copy-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.rows = R.records(ROOT)
        names = {R.REGISTRY, R.DECISION, R.AGENT_SNAPSHOT}
        for row in self.rows:
            names.add(row['previous'])
            if not product_record(Path(row['destination'])):
                names.add(row['destination'])
        for row in R.agent_snapshots(ROOT):
            names.add(row['snapshot'])
        names.add('docs/validation/governance-audit-20261114/report.md')
        import log_repair_revision
        names = list(names) + log_repair_revision.fixture_paths(ROOT)
        names += [log_repair_revision.ORIGINS]
        names += [name for row in log_repair_revision.origin_records(ROOT)
                  for name in (row['source'], row['origin'])]
        import visual_skill_revision
        names += list(visual_skill_revision.records(ROOT))
        # A declared governance copy excludes live product origins, even when
        # the source checkout's history fixtures include those origins.
        names = [name for name in names if not name.startswith('application/')
                 and not product_record(Path(name))]
        for name in names:
            p = self.root / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes((ROOT / name).read_bytes())
        R.write_copy_context(self.root)

    def fixture_errors(self):
        # Transitive fixture inputs belong to several historical validators.
        import document_ledger
        import log_repair_revision
        import visual_skill_revision
        try:
            result = R.errors(self.root) + visual_skill_revision.errors(self.root)
            log_repair_revision.origin_records(self.root)
            for name in document_ledger.records(self.root):
                if not product_record(Path(name)):
                    document_ledger.predecessor(self.root, name, (self.root / name).read_bytes())
            return result
        except (ValueError, OSError) as error:
            return [str(error)]

    def test_explicit_copy_accepts_only_deliberately_excluded_records(self):
        self.assertTrue(R.governance_copy(self.root))
        self.assertEqual(R.errors(self.root), [])
        (self.root / 'sdd/project.md').unlink()
        self.assertTrue(R.errors(self.root))

    def test_missing_context_never_turns_missing_live_sources_into_snapshot_acceptance(self):
        (self.root / R.COPY_CONTEXT).unlink()
        # Remove excluded records from this minimal local fixture's concern by
        # checking live configuration directly: absence is an error, regardless
        # of absent application/config directories.
        self.assertFalse(R.governance_copy(self.root))
        self.assertTrue(R.agent_errors(self.root, False))
        for row in R.agent_snapshots(self.root):
            p = self.root / row['source']
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes((self.root / row['snapshot']).read_bytes())
        self.assertEqual(R.agent_errors(self.root, False), [])
        extra = self.root / '.codex/agents/unobserved.toml'
        extra.write_text('name = \"unexpected\"\n')
        self.assertTrue(R.agent_errors(self.root, False))
        extra.unlink()
        source = self.root / '.codex/agents/ec_triador.toml'
        data = source.read_bytes()
        source.write_bytes(data + b'drift')
        self.assertTrue(R.agent_errors(self.root, False))
        source.unlink()
        self.assertTrue(R.agent_errors(self.root, False))
        source.symlink_to(self.root / R.agent_snapshots(self.root)[0]['snapshot'])
        self.assertTrue(R.agent_errors(self.root, False))

    def test_receipt_mutation_symlink_and_live_checkout_conflicts(self):
        marker = self.root / R.COPY_CONTEXT
        marker.write_bytes(R.COPY_CONTEXT_BYTES + b'changed')
        self.assertTrue(R.errors(self.root))
        marker.unlink()
        other = self.root / 'receipt.bin'
        other.write_bytes(R.COPY_CONTEXT_BYTES)
        marker.symlink_to(other)
        self.assertTrue(R.errors(self.root))
        marker.unlink()
        R.write_copy_context(self.root)
        for name in ('.git', 'application', '.codex/config.toml', '.codex/agents'):
            p = self.root / name
            p.parent.mkdir(parents=True, exist_ok=True)
            for mode in ('file', 'directory', 'symlink'):
                with self.subTest(path=name, mode=mode):
                    if mode == 'file':
                        p.write_text('local')
                    elif mode == 'directory':
                        p.mkdir()
                    else:
                        p.symlink_to(self.root / 'missing-local')
                    self.assertTrue(R.errors(self.root))
                    if p.is_dir() and not p.is_symlink():
                        p.rmdir()
                    else:
                        p.unlink()

    def test_snapshots_and_excluded_predecessors_still_required(self):
        profile = R.agent_snapshots(self.root)[0]
        names = [R.AGENT_SNAPSHOT, profile['snapshot']]
        excluded = next(row for row in self.rows if product_record(Path(row['destination'])))
        names.append(excluded['previous'])
        import log_repair_revision
        names = list(names) + log_repair_revision.fixture_paths(ROOT)
        names = [name for name in names if not name.startswith('application/')
                 and not product_record(Path(name))]
        self.assertEqual(self.fixture_errors(), [])
        for name in names:
            p = self.root / name
            data = p.read_bytes()
            # Authorization prose is mutable; challenge a protected authority
            # section instead of an allowed contextual append.
            changed = (data.replace(b'## Authorities', b'## Lost authorities', 1)
                       if name == 'sdd/project.md' else data + b'changed')
            p.write_bytes(changed)
            import historical_link_revision
            if name != historical_link_revision.DECISION:
                self.assertTrue(self.fixture_errors(), name)
            p.unlink()
            self.assertTrue(self.fixture_errors(), name)
            p.write_bytes(data)

    def test_audit_exception_is_source_destination_and_snapshot_exact(self):
        source = 'docs/validation/governance-audit-20261114/report.md'
        target = self.root / '.codex/agents/ec_triador.toml'
        self.assertTrue(R.excluded_local_reference(self.root, source, target))
        self.assertFalse(R.excluded_local_reference(self.root, source, self.root / '.codex/agents/other.toml'))
        self.assertFalse(R.excluded_local_reference(self.root, 'README.md', target))
        p = self.root / source
        p.write_bytes(p.read_bytes() + b'changed')
        self.assertFalse(R.excluded_local_reference(self.root, source, target))
        p.write_bytes((ROOT / source).read_bytes())
        (self.root / R.COPY_CONTEXT).unlink()
        self.assertFalse(R.excluded_local_reference(self.root, source, target))

    def test_docs_index_only_exact_successor_is_recognized(self):
        row = next(row for row in self.rows if row['destination'] == 'docs/README.md')
        p = self.root / row['destination']
        self.assertEqual(R.predecessor(self.root, row['destination'], p.read_bytes()), (self.root / row['previous']).read_bytes())
        p.write_bytes(p.read_bytes() + b'unknown')
        self.assertTrue(R.errors(self.root))


if __name__ == '__main__':
    unittest.main()
