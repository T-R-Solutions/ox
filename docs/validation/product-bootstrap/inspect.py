"""Read-only structural oracle; does not establish GUI behavior."""
from pathlib import Path
import json, subprocess, hashlib
root=Path(__file__).resolve().parents[3]
metadata=json.loads(subprocess.check_output(['cargo','metadata','--manifest-path','application/Cargo.toml','--no-deps','--format-version','1'],cwd=root))
packages={p['name']:p for p in metadata['packages']}
expected={'ox-'+s for s in 'app ui core agent plugin policy task workspace storage context graph output verification observability sdd skills'.split()}
assert set(packages)==expected
assert len(metadata['workspace_members'])==16
edges={name:[d['name'] for d in p['dependencies'] if d['name'] in packages] for name,p in packages.items()}
def visit(name,stack):
 assert name not in stack,stack
 for dep in edges[name]:visit(dep,stack+[name])
for name in packages:visit(name,[])
for name,p in packages.items():
 for target in p['targets']:
  if 'lib' in target['kind'] or 'bin' in target['kind']:
   assert '#![forbid(unsafe_code)]' in Path(target['src_path']).read_text()
 if name not in ('ox-ui','ox-app'):
  assert not any(d['name'] in ('iced','ox-ui','ox-app') for d in p['dependencies'])
assert not list((root/'application/crates').rglob('mod.rs'))
assert list((root/'application').glob('Cargo.lock'))
assert not list((root/'application/crates').rglob('Cargo.lock'))
for p in (root/'application/crates').rglob('*.rs'):
 text=p.read_text();assert 'todo!(' not in text and 'unimplemented!(' not in text
assert 'ox_app::run()' in (root/'application/crates/ox-app/src/main.rs').read_text()
assert 'channel = "stable"' in (root/'application/rust-toolchain.toml').read_text()
print(json.dumps({'result':'PASS','members':sorted(packages),'edges':edges,'limits':['Structural inspection does not prove runtime correctness, isolation, or transitive safety.']},indent=2))
