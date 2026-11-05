"""Reconstruct the observed disposable diagnostic copy using existing dependencies only."""
import pathlib,shutil,hashlib,json,subprocess,os
B=pathlib.Path(__file__).resolve().parent;ROOT=B.parents[2]
app=pathlib.Path('/tmp/ox-f0-frame-app');iced=pathlib.Path('/tmp/ox-f0-frame-iced-winit')
# Fail closed on changed product inputs; this does not reaccept a different tree.
for item in json.loads((B/'inputs-final.json').read_text())['inputs']:
 if item['path'].startswith('application/'):
  p=ROOT/item['path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==item['sha256'],p
if not app.exists():
 app.mkdir()
 for name in ['Cargo.toml','Cargo.lock','rust-toolchain.toml']:shutil.copy2(ROOT/'application'/name,app/name)
 shutil.copytree(ROOT/'application/crates',app/'crates')
else:
 # Existing destination is not overwritten unless already exactly the observed copy.
 for src,rel in [('final-diagnostic-desktop.rs.bin','crates/ox-ui/src/desktop.rs'),('final-diagnostic-tests.rs.bin','crates/ox-app/tests/desktop.rs')]:
  assert (app/rel).read_bytes()==(B/src).read_bytes(),f'Unexpected existing diagnostic bytes: {app/rel}'
if not iced.exists():
 candidates=list((pathlib.Path.home()/'.cargo/registry/src').glob('*/iced_winit-0.14.1'));assert len(candidates)==1,'Existing iced_winit 0.14.1 source required; no download'
 shutil.copytree(candidates[0],iced)
 (iced/'src/lib.rs').write_bytes((B/'diagnostic-iced-winit.rs.bin').read_bytes())
else:assert (iced/'src/lib.rs').read_bytes()==(B/'diagnostic-iced-winit.rs.bin').read_bytes(),'Unexpected instrumented dependency bytes'
for src,rel in [('final-diagnostic-desktop.rs.bin','crates/ox-ui/src/desktop.rs'),('final-diagnostic-tests.rs.bin','crates/ox-app/tests/desktop.rs'),('diagnostic-Cargo.toml.bin','Cargo.toml'),('diagnostic-Cargo.lock.bin','Cargo.lock')]:
 target=app/rel;data=(B/src).read_bytes()
 if target.read_bytes()!=data:target.write_bytes(data)
subprocess.run(['cargo','build','--workspace','--offline'],cwd=app,env=dict(os.environ,CARGO_TARGET_DIR='/tmp/ox-f0-frame-target'),check=True)
print('Prepared observed diagnostic copy. GUI commands require graphical execution permissions.')
