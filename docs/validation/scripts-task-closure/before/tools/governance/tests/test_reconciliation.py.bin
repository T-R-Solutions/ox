"""Regression oracles for bounded succession and Git-free distributions."""
from pathlib import Path
from io import BytesIO
import hashlib
import importlib.util
import json
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[3]

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT/path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

C = load('reconcile_checker', 'tools/governance/scripts/check-ox.py')
M = load('reconcile_maintenance', 'tools/governance/scripts/verify-maintenance.py')
P = load('reconcile_package', 'tools/governance/scripts/package-ox.py')
from governance_support import copy_distribution, distribution_files, succession_errors, inspect_bytes


class GitBoundaryTests(unittest.TestCase):
    def test_archived_git_metadata_rejected_recursively(self):
        nested = BytesIO()
        with zipfile.ZipFile(nested, 'w') as archive:
            archive.writestr('nested/worktree/.git', 'gitdir: /private/path')
        outer = BytesIO()
        with zipfile.ZipFile(outer, 'w') as archive:
            archive.writestr('nested.zip', nested.getvalue())
        self.assertTrue(any('Git metadata in archive' in e
                            for e in inspect_bytes('outer.zip', outer.getvalue(), {})))
        clean = BytesIO()
        with zipfile.ZipFile(clean, 'w') as archive:
            archive.writestr('nested/.gitignore', 'target/')
        self.assertEqual(inspect_bytes('clean.zip', clean.getvalue(), {}), [])

    def test_nested_git_directories_and_worktree_files_excluded(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            allowed = ['AGENTS.md', 'README.md', 'LICENSE', 'NOTICE', 'docs/nested/.gitignore',
                       'docs/nested/.github/workflows/build.yml', '.codex/skills/demo/SKILL.md']
            forbidden = ['.git/config', 'docs/nested/.git/config', 'sdd/worktree/.git',
                         '.codex/skills/demo/.git/objects/aa', 'tools/governance/nested/.git']
            for relative in allowed + forbidden:
                path = root/relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text('fixture')
            self.assertEqual({str(p.relative_to(root)) for p in distribution_files(root)}, set(allowed))
            package = BytesIO()
            P.create_archive(root, package)
            with zipfile.ZipFile(package) as archive:
                self.assertFalse(any('.git' in Path(n).parts for n in archive.namelist()))
                self.assertIn('docs/nested/.gitignore', archive.namelist())
            copied = root/'copied'
            copy_distribution(root, copied)
            self.assertEqual({str(p.relative_to(copied)) for p in copied.rglob('*') if p.is_file()}, set(allowed))


class SuccessionTests(unittest.TestCase):
    integration = True

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        copy_distribution(ROOT, self.root)

    def test_current_original_and_metadata_integrity(self):
        self.assertEqual(M.verify(self.root)['errors'], [])
        self.assertEqual(M.verify(self.root)['recovered_layout_inputs'], 439)
        for name in ['AGENTS.md', '.codex/skills/prompt/agents/openai.yaml',
                     '.codex/skills/rust/agents/openai.yaml',
                     'docs/validation/governance-reconciliation/recovered/AGENTS.md.bin',
                     'docs/validation/governance-reconciliation/previous/AGENTS.md.bin']:
            path = self.root/name
            data = path.read_bytes()
            for mutation in ['corrupt', 'delete']:
                with self.subTest(name=name, mutation=mutation):
                    if mutation == 'corrupt':
                        path.write_bytes(data+b'\ncorrupt\n')
                    else:
                        path.unlink()
                    try:
                        try:
                            errors = M.verify(self.root)['errors']
                        except ValueError as exc:
                            errors = [str(exc)]
                        self.assertTrue(errors)
                    finally:
                        path.write_bytes(data)

    def test_profile_still_rejects_unauthorized_skills_and_bridges(self):
        path = self.root/'.codex/skills/unauthorized/SKILL.md'
        path.parent.mkdir()
        path.write_text('---\nname: unauthorized\ndescription: fixture\n---\n')
        self.assertTrue(any('Skill inventory differs' in e for e in C.check(self.root)))
        path.unlink()
        path.parent.rmdir()
        bridge = self.root/'sdd/chain/commit-governance.md'
        bridge.write_text(bridge.read_text().replace('skill: commit-governance', 'skill: rust'))
        self.assertTrue(C.check(self.root))

    def test_succession_predecessor_and_scope_fail_closed(self):
        path = self.root/'docs/structure/files.json'
        before = path.read_bytes()
        for mutation in ['duplicate', 'predecessor', 'escaping', 'missing']:
            doc = json.loads(before)
            rows = next(r for r in doc['revisions'] if r['id']=='governance-reconciliation-001')['records']
            if mutation == 'duplicate': rows.append(rows[0])
            elif mutation == 'predecessor': rows[0]['previous_sha256'] = '0'*64
            elif mutation == 'escaping': rows[0]['previous'] = '../outside'
            else: rows.pop()
            with self.subTest(mutation=mutation):
                path.write_text(json.dumps(doc))
                with self.assertRaises(ValueError): succession_errors(self.root)
        path.write_bytes(before)
