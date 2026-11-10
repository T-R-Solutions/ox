"""Criterion-specific mutation tests, using the actual Ox gate and SDD validator."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest
from test_governance import V, C


class TechnicalAcceptanceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='ox-technical-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.feature = self.root / 'sdd/features/skill-example'
        self.feature.mkdir(parents=True)
        for name, content in {'spec.md': '- REQ-01: bounded consumer\n- AC-01 → REQ-01: expected behavior\n', 'plan.md': 'D-01 R-01', 'tasks.md': 'T001'}.items():
            (self.feature / name).write_text(content)
        self.rows = [dict(acceptance='AC-01', requirement='REQ-01', decision='D-01', risk='R-01', tasks=['T001'], implementation='skill.md', oracle='cases.md')]
        (self.feature / 'traceability.json').write_text(json.dumps(self.rows))
        for name in ('skill.md', 'cases.md', 'consumer.rs', 'test.rs', 'review.txt', 'run.log', 'unrelated.rs'):
            (self.root / name).write_text(name)
        inputs = [self.binding(str(p.relative_to(self.root))) for p in self.feature.iterdir()]
        inputs += [self.binding(p) for p in ('skill.md', 'cases.md', 'consumer.rs', 'test.rs')]
        self.doc = dict(schema_version=2, environment='isolated fixture', limitations=['synthetic contract test'], requirements=[dict(id='AC-01', criterion='expected behavior', status='APPROVED', evidence_ids=['review', 'run'], technical_review=dict(version=1, scope='bounded fixture', review='review', execution=['run'], consumer='consumer.rs', oracle='test.rs'))], evidence=[self.evidence('review', 'inspection', 'review.txt', inputs), self.evidence('run', 'test', 'run.log', [self.binding('consumer.rs', 'implementation'), self.binding('test.rs', 'oracle')])])

    def binding(self, name, role='other'):
        return dict(path=name, sha256=V.digest(self.root / name), role=role)

    def evidence(self, name, kind, artifact, inputs):
        return dict(id=name, kind=kind, artifact=artifact, sha256=V.digest(self.root / artifact), inputs=inputs, command_or_method='controlled fixture', observed_result='known outcome')

    def errors(self, doc=None):
        doc = self.doc if doc is None else doc
        return (V.evidence_errors(doc, self.root) + V.input_errors(doc, self.root, self.rows, self.feature, True)
                + V.trace_errors(self.rows, self.root, self.feature, doc)
                + C.technical_errors(self.root, self.feature, doc, self.rows, V))

    def test_all_states_and_legacy_aliases(self):
        for value in list(V.STATES) + list(V.LEGACY_STATES):
            with self.subTest(value=value):
                d = deepcopy(self.doc)
                r = d['requirements'][0]
                r['status'] = value
                if V.state(value) in {'UNVERIFIED', 'INCONCLUSIVE', 'NOT APPLICABLE'}:
                    r['technical_review']['execution'] = []
                    r['evidence_ids'] = ['review']
                    d['evidence'] = d['evidence'][:1]
                if V.state(value) == 'UNVERIFIED':
                    r.pop('technical_review')
                if V.state(value) == 'NOT APPLICABLE':
                    r['reason'] = 'Consumer excludes this platform'
                self.assertEqual(self.errors(d), [])

    def test_bare_status_or_authoring_review_never_approves(self):
        for change in ('descriptor', 'execution', 'kind', 'same-artifact', 'authoring-consumer', 'authoring-oracle', 'unlinked', 'unrelated', 'roles'):
            with self.subTest(change=change):
                d = deepcopy(self.doc); r = d['requirements'][0]; t = r['technical_review']
                if change == 'descriptor': r.pop('technical_review')
                if change == 'execution': t['execution'] = []
                if change == 'kind': d['evidence'][1]['kind'] = 'inspection'
                if change == 'same-artifact':
                    d['evidence'][1]['artifact'] = 'review.txt'
                    d['evidence'][1]['sha256'] = V.digest(self.root / 'review.txt')
                if change == 'authoring-consumer': t['consumer'] = 'skill.md'
                if change == 'authoring-oracle': t['oracle'] = 'cases.md'
                if change == 'unlinked': r['evidence_ids'] = ['review']
                if change == 'unrelated': t['consumer'] = 'unrelated.rs'
                if change == 'roles': d['evidence'][1]['inputs'][0]['role'] = 'other'
                self.assertTrue(self.errors(d))

    def test_partial_states_require_review_and_scope(self):
        for state in ('INCONCLUSIVE', 'NOT APPLICABLE'):
            for field in ('scope', 'review', 'version'):
                d = deepcopy(self.doc); r = d['requirements'][0]
                r.update(status=state, reason='platform excluded')
                r['technical_review'].pop(field)
                self.assertTrue(self.errors(d), (state, field))
        self.doc['requirements'][0]['status'] = 'NOT APPLICABLE'
        self.assertTrue(self.errors())

    def test_stale_artifacts_and_each_bound_input_rejected(self):
        for path in list(self.feature.iterdir()) + [self.root / p for p in ('skill.md', 'cases.md', 'consumer.rs', 'test.rs', 'review.txt', 'run.log')]:
            with self.subTest(path=path.name):
                before = path.read_bytes()
                path.write_bytes(before + b' altered')
                self.assertTrue(self.errors())
                path.write_bytes(before)
                self.assertEqual(self.errors(), [])

    def test_missing_files_escape_and_duplicate_references(self):
        for value in ('missing.rs', '../outside', None, [], {}):
            d = deepcopy(self.doc); d['requirements'][0]['technical_review']['consumer'] = value
            self.assertTrue(self.errors(d))
        for refs in (['run', 'run'], ['missing'], 'run', None):
            d = deepcopy(self.doc); d['requirements'][0]['technical_review']['execution'] = refs
            self.assertTrue(self.errors(d))
        self.doc['schema_version'] = 1
        self.assertTrue(self.errors())

    def test_review_cannot_borrow_contract_binding_from_execution(self):
        item = self.doc['evidence'][0]['inputs'].pop(0)
        self.doc['evidence'][1]['inputs'].append(item)
        self.assertTrue(self.errors())

    def test_unrelated_change_does_not_invalidate_acceptance(self):
        (self.root / 'unrelated.rs').write_text('unrelated change')
        self.assertEqual(self.errors(), [])

    def test_symlink_alias_does_not_hide_authoring_substitution(self):
        (self.root / 'alias').symlink_to(self.root / 'skill.md')
        self.doc['requirements'][0]['technical_review']['consumer'] = 'alias'
        self.assertTrue(self.errors())


if __name__ == '__main__':
    unittest.main()
