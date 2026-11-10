"""Unit tests validate platform logic, not real scanner integration."""
import concurrent.futures
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from toolbox.adapters import adapter, classify
from toolbox.config import ConfigError, REPO, load, read_json
from toolbox.docker import command
from toolbox.runner import exit_status, run
from toolbox.storage import Store, atomic_json, tree_manifest
from toolbox.prepare import recipe_identity


class CoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='toolbox test ')
        self.root = Path(self.tmp.name)
        self.consumer = self.root / 'consumer with spaces'
        self.consumer.mkdir()
        self.path = self.consumer / 'toolbox.json'
        self.data = {'schema': 1, 'project': 'test', 'tools': {'ruff': {'version': '0.11.13'}}}
        self.save()
        self.store = Store(self.root / 'state', tools_root=self.root / 'tools')
        self.store.tools_root.mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def save(self):
        atomic_json(self.path, self.data)

    def test_unknown_and_duplicate_fields(self):
        self.data['typo'] = True
        self.save()
        with self.assertRaisesRegex(ConfigError, 'unknown field'):
            load(self.path)
        self.path.write_text('{"schema":1,"schema":1}')
        with self.assertRaisesRegex(ConfigError, 'duplicate'):
            load(self.path)

    def test_invalid_types_and_paths(self):
        for value in [True, -1, '600', float('inf')]:
            self.data['tools']['ruff']['timeout'] = value
            self.save()
            with self.assertRaises(ValueError):
                load(self.path)
        self.data['tools']['ruff'] = {'version': '0.11.13', 'paths': ['../escape']}
        self.save()
        with self.assertRaisesRegex(ConfigError, 'inside consumer'):
            load(self.path)

    def test_omission_requires_reason(self):
        self.data['tools']['ruff']['enabled'] = False
        self.save()
        with self.assertRaisesRegex(ConfigError, 'reason'):
            load(self.path)

    def test_profiles_never_choose_versions_implicitly(self):
        self.data['profiles'] = ['python']
        self.save()
        with self.assertRaisesRegex(ConfigError, 'bandit'):
            load(self.path)

    def test_private_selinux_mount_preserves_isolation(self):
        output = self.root / 'results'
        output.mkdir()
        with patch.dict(os.environ, {'TOOLBOX_SELINUX_LABEL': 'private'}):
            _, cmd = command('sha256:' + '0'*64, [], self.consumer, output)
            self.assertIn(f'{self.consumer}:/src:ro,Z', cmd)
            self.assertIn(f'{output}:/out:rw,Z', cmd)
            self.assertIn('--cap-drop=ALL', cmd)
            self.assertNotIn('label=disable', cmd)
            with self.assertRaises(ValueError):
                command('sha256:' + '0'*64, [], self.root / 'missing', output)
        with patch.dict(os.environ, {'TOOLBOX_SELINUX_LABEL': 'disable'}):
            with self.assertRaises(ValueError):
                command('sha256:' + '0'*64, [], self.consumer, output)

    def test_shared_selinux_mount_preserves_uid_and_readonly(self):
        output = self.root / 'shared results'
        output.mkdir()
        with patch.dict(os.environ, {'TOOLBOX_SELINUX_LABEL': 'shared'}):
            _, cmd = command('sha256:' + '0'*64, [], self.consumer, output)
            self.assertIn(f'{self.consumer}:/src:ro,z', cmd)
            self.assertIn(f'{output}:/out:rw,z', cmd)
            self.assertIn(f'{os.getuid()}:{os.getgid()}', cmd)
            self.assertIn('--cap-drop=ALL', cmd)
            self.assertNotIn('label=disable', cmd)
            self.assertNotIn('--privileged', cmd)

    def test_mount_contract_and_paths_with_spaces(self):
        name, cmd = command('sha256:' + '0'*64, ['check', 'a file.py'], self.consumer, self.root / 'results')
        self.assertIn(f'type=bind,src={self.consumer},dst=/src,readonly', cmd)
        self.assertIn('--pull=never', cmd)
        self.assertIn(f'{os.getuid()}:{os.getgid()}', cmd)
        self.assertNotIn('--privileged', cmd)
        self.assertNotIn('/var/run/docker.sock', ' '.join(cmd))
        self.assertEqual(cmd[-1], 'a file.py')
        self.assertTrue(name.startswith('toolbox-'))

    def test_native_reports_separate_findings_and_errors(self):
        mod = adapter('ruff')
        out = self.root
        execution = {'tool_exit_code': 1, 'container_state': {}}
        (out / 'stdout.log').write_text('[{"code":"F401"}]')
        self.assertEqual(classify(mod, execution, out)[0], 'findings')
        execution['tool_exit_code'] = 2
        self.assertEqual(classify(mod, execution, out)[0], 'operational_failure')
        execution['tool_exit_code'] = 0
        (out / 'stdout.log').write_text('[]')
        self.assertEqual(classify(mod, execution, out)[0], 'success')
        (out / 'stdout.log').write_text('invalid JSON')
        self.assertEqual(classify(mod, execution, out)[0], 'operational_failure')

    def test_gitleaks_does_not_treat_generic_exit_one_as_finding(self):
        atomic_json(self.root / 'native.json', [{'RuleID': 'fixture'}])
        self.assertEqual(adapter('gitleaks').classify(1, self.root)[0], 'operational_failure')
        self.assertEqual(adapter('gitleaks').classify(42, self.root)[0], 'findings')

    def test_playwright_no_tests_and_config_errors_never_pass(self):
        for report in [{'errors': [{'message': 'bad config'}]}, {'stats': {'expected': 0, 'unexpected': 0, 'skipped': 4, 'flaky': 0}}]:
            atomic_json(self.root / 'native.json', report)
            self.assertEqual(classify(adapter('playwright'), {'tool_exit_code': 1}, self.root)[0], 'operational_failure')

    def test_aggregation_never_approves_nonexecution(self):
        for status, expected in [('success', 0), ('findings', 1), ('operational_failure', 2),
                                 ('prerequisite_missing', 2), ('measurement', 3), ('omitted', 3), ('inapplicable', 3)]:
            self.assertEqual(exit_status({'tools': [{'status': status}]}), expected)
        self.assertEqual(exit_status({'tools': []}), 3)

    def test_concurrent_run_ids_are_unique(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
            paths = list(pool.map(lambda _: self.store.run_dir('test'), range(32)))
        self.assertEqual(len(set(paths)), 32)

    def test_atomic_writes_under_contention(self):
        p = self.root / 'record.json'
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
            list(pool.map(lambda n: atomic_json(p, {'n': n}), range(32)))
        self.assertIn(read_json(p)['n'], range(32))
        self.assertEqual(list(self.root.glob('*.tmp')), [])

    def test_prune_keeps_other_projects_and_incomplete_runs(self):
        for project in ['test', 'other']:
            for _ in range(3):
                p = self.store.run_dir(project)
                atomic_json(p / 'summary.json', {'status': 'done'})
                self.store.tool_run('ruff', project, p.name)
                self.store.tool_run('gitleaks', project, p.name)
        pending = self.store.run_dir('test')
        self.assertEqual(len(self.store.prune('test', 1)), 2)
        self.store.prune('test', 1, apply=True)
        self.assertTrue(pending.exists())
        self.assertEqual(len(list((self.store.root / 'projects/other/runs').iterdir())), 3)
        for tool in ['ruff', 'gitleaks']:
            self.assertEqual(len(list((self.store.volume(tool) / 'projects/test/runs').iterdir())), 1)
            self.assertEqual(len(list((self.store.volume(tool) / 'projects/other/runs').iterdir())), 3)

    def test_real_cli_missing_image_persists_result_and_preserves_sources(self):
        # Docker is not emulated as a scanner. No image => no tool execution.
        before = tree_manifest(self.consumer)
        with patch('toolbox.docker.doctor', return_value={'ready': False, 'error': 'daemon absent'}):
            result = run(self.store, load(self.path), self.data['tools'])
        self.assertEqual(result['tools'][0]['status'], 'prerequisite_missing')
        self.assertEqual(tree_manifest(self.consumer), before)
        p = Path(result['directory'])
        self.assertTrue((p / 'summary.json').exists())
        output = Path(result['tools'][0]['output'])
        self.assertEqual(output, self.store.tools_root / 'ruff/volume/projects/test/runs' / p.name)
        self.assertTrue((output / 'stdout.log').exists())
        self.assertEqual((output / 'stderr.log').stat().st_uid, os.getuid())

    def test_config_examples(self):
        for p in (REPO / 'examples').glob('*/toolbox.json'):
            load(p)

    def test_recipe_identity_ignores_bytecode_and_documentation(self):
        folder = self.root / 'recipe'
        folder.mkdir()
        (folder / 'Dockerfile').write_text('ARG BASE\nFROM ${BASE}\n')
        with patch('toolbox.prepare.tool_folder', return_value=folder):
            before = recipe_identity('ruff', {'version': '0.11.13'}, {'base': 'test'})
            (folder / '__pycache__').mkdir()
            (folder / '__pycache__/adapter.pyc').write_bytes(b'local bytecode')
            (folder / 'README.md').write_text('docs update')
            (folder / 'volume').mkdir()
            (folder / 'volume/result.json').write_text('runtime data must not affect image identity')
            self.assertEqual(before, recipe_identity('ruff', {'version': '0.11.13'}, {'base': 'test'}))
            (folder / 'Dockerfile').write_text('changed recipe')
            self.assertNotEqual(before, recipe_identity('ruff', {'version': '0.11.13'}, {'base': 'test'}))

    def test_tool_data_is_scoped_to_its_volume(self):
        volume = self.store.tools_root / 'grype/volume'
        self.assertEqual(self.store.database('grype', '0.119.0', 'abc'), volume / 'databases/0.119.0/abc')
        self.assertEqual(self.store.preparation_dir('grype').parent, volume / 'preparation')
        with self.store.lock(['database', 'grype']):
            self.assertEqual(len(list((volume / 'locks').glob('*.lock'))), 1)
        self.assertFalse((self.store.root / 'databases').exists())

    def test_reject_volume_inside_consumer_sources(self):
        store = Store(self.root / 'state', tools_root=self.consumer / 'tools')
        with self.assertRaisesRegex(ValueError, 'volume directory'):
            run(store, load(self.path), self.data['tools'])


if __name__ == '__main__':
    unittest.main()
