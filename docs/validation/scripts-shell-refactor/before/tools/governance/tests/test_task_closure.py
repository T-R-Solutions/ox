"""Observable closure contracts: disposable repositories and subprocess effects."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location('closure', ROOT/'scripts/automate.py')
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)


class ClosureTests(unittest.TestCase):
    def test_scope_and_offline_workspace(self):
        rust = C.commands('rust')
        self.assertEqual([x[0] for x in rust], ['rust-fmt','rust-check','rust-build','rust-test','rust-clippy'])
        for name, cwd, argv in rust:
            self.assertEqual(cwd, 'application')
            if name != 'rust-fmt':
                self.assertTrue({'--locked','--offline','--workspace'} <= set(argv))
        self.assertEqual(C.commands('full')[2][2][-1], 'all')
        self.assertEqual(C.commands('governance')[2][2][-1], 'fast')

    def test_real_cli_from_other_cwd_and_spaces(self):
        with tempfile.TemporaryDirectory(prefix='Ox with spaces ') as tmp:
            dest=Path(tmp)
            for rel in ('scripts/automate.py','AGENTS.md','sdd/tools/validate.py','tools/governance/scripts/check-ox.py','tools/governance/scripts/run-tests.py','application/Cargo.toml','application/Cargo.lock','application/rust-toolchain.toml'):
                p=dest/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/rel,p)
            shutil.copytree(ROOT/'scripts/security',dest/'scripts/security')
            run=subprocess.run([sys.executable,str(dest/'scripts/automate.py'),'--scope','full','--plan'],cwd='/tmp',capture_output=True)
            self.assertEqual(run.returncode,0,run.stderr)
            self.assertTrue({'gitleaks','osv','opengrep','audit','bandit','machete','ruff','deny'} <= {t[0] for t in json.loads(run.stdout)})
            self.assertFalse((dest/'.local').exists())
            (dest/'application/Cargo.toml').write_text('invalid = [')
            run=subprocess.run([sys.executable,str(dest/'scripts/automate.py'),'--scope','rust','--plan'],capture_output=True)
            self.assertEqual(run.returncode,2)

    def test_failure_and_raw_streams(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)
            result=C.execute([sys.executable,'-c',"import os;os.write(1,b'out\\x00');os.write(2,b'err\\xff');raise SystemExit(23)"],p,os.environ,p)
            self.assertEqual(result['exit_code'],23)
            self.assertEqual(result['state'],'failed')
            self.assertEqual((p/'stdout.log').read_bytes(),b'out\x00')
            self.assertEqual((p/'stderr.log').read_bytes(),b'err\xff')

    def test_missing_required_tool(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)
            result=C.execute(['ox-nonexistent-required-tool'],p,{'PATH':tmp},p)
            self.assertEqual(result['exit_code'],127)
            self.assertEqual(result['state'],'blocked')

    def test_unknown_configuration(self):
        run=subprocess.run([sys.executable,str(ROOT/'scripts/automate.py'),'--scope','governance','--config','foreign.toml'],capture_output=True)
        self.assertEqual(run.returncode,2)

    def test_succession_rejects_mutation_and_escape(self):
        sys.path.insert(0,str(ROOT/'tools/governance/scripts'))
        import closure_revision as R
        data=(ROOT/'sdd/workflow.md').read_bytes()
        self.assertNotEqual(R.predecessor(ROOT,'sdd/workflow.md',data),data)
        self.assertEqual(R.predecessor(ROOT,'sdd/workflow.md',data+b'unknown'),data+b'unknown')
        with tempfile.TemporaryDirectory() as tmp:
            dest=Path(tmp);registry=dest/R.REGISTRY;registry.parent.mkdir(parents=True)
            registry.write_text('{}')
            with self.assertRaises(ValueError):R.predecessor(dest,'sdd/workflow.md',data)

    def test_execution_from_other_directory_and_blocked_toolchain(self):
        with tempfile.TemporaryDirectory(prefix='Ox execution spaces ') as tmp:
            dest=Path(tmp)
            for rel in ('scripts/automate.py','AGENTS.md','application/Cargo.toml','application/Cargo.lock','application/rust-toolchain.toml'):
                p=dest/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/rel,p)
            for rel in ('sdd/tools/validate.py','tools/governance/scripts/check-ox.py','tools/governance/scripts/run-tests.py'):
                p=dest/rel;p.parent.mkdir(parents=True,exist_ok=True)
                p.write_text('import os\nprint(os.getcwd())\n')
            run=subprocess.run([sys.executable,str(dest/'scripts/automate.py'),'--scope','governance'],cwd='/tmp',capture_output=True)
            self.assertEqual(run.returncode,0,run.stderr)
            report=json.loads(next((dest/'.local/checks').glob('*/results.json')).read_text())
            self.assertTrue(all(x['cwd']==str(dest) for x in report['results']))
            self.assertEqual(len(report['results']),3)
            run=subprocess.run([sys.executable,str(dest/'scripts/automate.py'),'--scope','rust'],cwd='/tmp',env=dict(os.environ,PATH=tmp),capture_output=True)
            self.assertEqual(run.returncode,127)
            reports=[json.loads(p.read_text()) for p in (dest/'.local/checks').glob('*/results.json')]
            blocked=next(x for x in reports if x['scope']=='rust')
            self.assertEqual(blocked['results'][0]['state'],'blocked')
