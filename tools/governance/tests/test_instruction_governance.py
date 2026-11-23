"""Destination procedures and current-state contracts, without source-checkout links."""
import importlib.util
import os
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location('instruction_governance_validator', ROOT / 'sdd/tools/validate.py')
V = importlib.util.module_from_spec(spec)
spec.loader.exec_module(V)


class TemplateInstantiationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='ox-template-adoption-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'task_finalizada.md').write_text('# Destination task log\n')
        (self.root / 'sdd').mkdir()
        for name in ('workflow.md', 'evidence.md'):
            shutil.copyfile(ROOT / 'sdd' / name, self.root / 'sdd' / name)

    def instantiate(self, relative, adapt):
        folder = self.root / relative
        folder.mkdir(parents=True)
        for name in ('spec.md', 'plan.md', 'tasks.md', 'converge.md', 'checklist.md'):
            text = (ROOT / 'sdd/templates' / name).read_text()
            if adapt:
                for authority in ('workflow.md', 'evidence.md'):
                    text = text.replace('../' + authority, os.path.relpath(self.root / 'sdd' / authority, folder))
            (folder / name).write_text(text)
        return folder

    def test_standard_and_custom_destinations_preserve_fragments(self):
        for path in ('sdd/features/example', 'work/specifications/nested/example'):
            with self.subTest(path=path):
                folder = self.instantiate(path, True)
                self.assertEqual(V.markdown_errors(folder, self.root), [])
                for name in ('tasks.md', 'checklist.md'):
                    self.assertIn('#documentation-before-task-closure', (folder / name).read_text())
        self.assertEqual(len(list(self.root.rglob('evidence.md'))), 1)
        self.assertEqual(len(list(self.root.rglob('workflow.md'))), 1)

    def test_unadapted_copy_exposes_original_failure(self):
        folder = self.instantiate('sdd/features/unadapted', False)
        self.assertTrue(V.markdown_errors(folder, self.root))


class CleanAdoptionTests(unittest.TestCase):
    # Independent copied model/skill execution is integration, not merely parsing.
    integration = True

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='ox-clean-sdd-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'task_finalizada.md').write_text('# Destination task log\n')
        for folder in ('sdd/templates', 'sdd/tools', 'sdd/chain', 'docs'):
            (self.root / folder).mkdir(parents=True)
        names = ['workflow.md', 'evidence.md', 'tools/validate.py']
        names += ['templates/' + n for n in ('README.md', 'spec.md', 'plan.md', 'tasks.md', 'converge.md', 'checklist.md')]
        for name in names:
            shutil.copyfile(ROOT / 'sdd' / name, self.root / 'sdd' / name)
        (self.root / 'sdd/README.md').write_text('# Destination SDD\nUse workflow.md.\n')
        (self.root / 'sdd/project.md').write_text('# Destination context\nScope: isolated fixture.\n')
        (self.root / 'docs/constitution.md').write_text('# Destination constitution\nFixture policies only.\n')
        (self.root / 'sdd/constitution.md').write_text('[Constitution](../docs/constitution.md)\n')
        (self.root / 'sdd/chain/README.md').write_text('# Bridges\nNo bridges selected.\n')
        s = importlib.util.spec_from_file_location('isolated_sdd_validator', self.root / 'sdd/tools/validate.py')
        self.validator = importlib.util.module_from_spec(s)
        s.loader.exec_module(self.validator)

    def test_allowlisted_model_without_skills_and_sibling_authority(self):
        self.assertEqual(self.validator.audit(self.root, check_evidence=False), [])
        self.assertTrue(self.validator.audit(self.root, check_evidence=False, link_scope='portable'))
        for forbidden in ('sdd/features', 'sdd/codex-agents.md', '.codex', 'docs/validation'):
            self.assertFalse((self.root / forbidden).exists())
        self.assertFalse(any(p.is_symlink() for p in self.root.rglob('*')))

    def test_selected_complete_skill_and_diagnosed_missing_skill(self):
        dest = self.root / 'skills/software-design'
        shutil.copytree(ROOT / '.codex/skills/software-design', dest)
        text = (ROOT / 'sdd/chain/software-design.md').read_text().replace('.codex/skills/software-design/SKILL.md', 'skills/software-design/SKILL.md')
        (self.root / 'sdd/chain/software-design.md').write_text(text)
        self.assertEqual(self.validator.audit(self.root, check_evidence=False), [])
        self.assertEqual(self.validator.skill_errors(dest), [])
        (dest / 'SKILL.md').unlink()
        self.assertTrue(self.validator.audit(self.root, check_evidence=False))


class CurrentEntryTests(unittest.TestCase):
    def test_current_summary_precedes_explicit_history(self):
        text = (ROOT / 'sdd/project.md').read_text()
        current, history = text.split('## Historical project context and authorization records', 1)
        for phrase in ('implementation-foundation', 'bootstrap-implemented', 'UNVERIFIED', 'configuration-cohesion', 'evidence.json', 'original inputs'):
            self.assertIn(phrase, current)
        self.assertIn('## Authorized configuration cohesion — 2026-11-11', history)
        self.assertIn('active-authorized-slice-product-plugin-host', history)
        self.assertNotIn('### Active authorized slice:', history)


if __name__ == '__main__':
    unittest.main()
