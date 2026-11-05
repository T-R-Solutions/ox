"""Reproduce the optimized diagnostic build from exact observed local inputs."""
from pathlib import Path
import hashlib,json,shutil,subprocess,os
B=Path(__file__).resolve().parent;R=B.parents[2];app=Path('/tmp/ox-f0-history-app');iced=Path('/tmp/ox-f0-frame-iced-winit')
doc=json.loads((B/'optimized-build-inputs.json').read_text())
for item in doc['product_inputs']:
 assert hashlib.sha256((R/item['path']).read_bytes()).hexdigest()==item['sha256'],item['path']
if not iced.exists():
 candidates=list((Path.home()/'.cargo/registry/src').glob('*/iced_winit-0.14.1'));assert len(candidates)==1
 shutil.copytree(candidates[0],iced);(iced/'src/lib.rs').write_bytes((B/'diagnostic-iced-winit.rs.bin').read_bytes())
assert (iced/'src/lib.rs').read_bytes()==(B/'diagnostic-iced-winit.rs.bin').read_bytes()
if not app.exists():
 app.mkdir()
 for name in ['Cargo.toml','Cargo.lock','rust-toolchain.toml']:shutil.copy2(R/'application'/name,app/name)
 shutil.copytree(R/'application/crates',app/'crates')
 for rel,snapshot in doc['diagnostic_differences'].items():(app/rel).write_bytes((B/snapshot).read_bytes())
for item in doc['product_inputs']:
 rel=str(Path(item['path']).relative_to('application'));expected=(B/doc['diagnostic_differences'][rel]).read_bytes() if rel in doc['diagnostic_differences'] else (R/item['path']).read_bytes()
 assert (app/rel).read_bytes()==expected,f'Unexpected scratch content: {rel}'
subprocess.run(['cargo','build','--workspace','--offline'],cwd=app,env=dict(os.environ,CARGO_TARGET_DIR='/tmp/ox-f0-history-target'),check=True)
print('Exact optimized diagnostic copy verified and built; no registry source edited.')
