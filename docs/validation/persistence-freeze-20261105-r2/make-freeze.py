"""Issue r2 exactly once after input stabilization. Do not execute candidates."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[3];B=Path(__file__).resolve().parent;P=R/'docs/validation/persistence-freeze-20261105'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
old=json.loads((P/'freeze.json').read_text());names=set();inherited=[]
preimages={}
for base in [B/'before',B/'intermediate',P/'before',R/'docs/validation/persistence-preflight-20261105/successor/before']:
 if base.exists():
  for p in base.rglob('*'):
   if p.is_file():preimages[sha(p)]=p
for row in old['files']:
 p=R/row['path'];actual=p
 if not p.is_file() or sha(p)!=row['sha256']:actual=preimages[row['sha256']]
 assert sha(actual)==row['sha256']
 names.add(str(actual.relative_to(R)));names.add(row['path'])
 inherited.append({'original_path':row['path'],'sha256':row['sha256'],'retained_path':str(actual.relative_to(R)),'use':'historical predecessor resource' if actual!=p else 'unchanged predecessor resource'})
for base in [B,P]:
 for p in base.rglob('*'):
  if p.is_file() and '__pycache__' not in p.parts and not (base==B and p.name in {'freeze.json','freeze.sha256','freeze-verification.log'}):names.add(str(p.relative_to(R)))
for p in (R/'sdd/features').glob('*/evidence.json'):
 d=json.loads(p.read_text())
 if not any(e['id']=='E-T011-R2-FINAL-SELECTIVE-REVIEW' for e in d['evidence']):continue
 names.add(str(p.relative_to(R)))
 for e in d['evidence']:
  if e['id']=='E-T011-R2-FINAL-SELECTIVE-REVIEW':names.update(x['path'] for x in e['inputs']);names.add(e['artifact'])
files=[]
for n in sorted(names):
 p=R/n;assert p.is_file() and p.resolve().is_relative_to(R) and not any((R/q).is_symlink() for q in [Path(n),*Path(n).parents]),n
 files.append({'path':n,'sha256':sha(p),'bytes':p.stat().st_size,'role':'local reproduction resource' if n.startswith('.local/') else 'current review or explicit historical context'})
d={'schema_version':1,'successor_id':'persistence-freeze-20261105-r2','predecessor':{'path':str((P/'freeze.json').relative_to(R)),'sha256':sha(P/'freeze.json')},'scope':'T011/T009 preparation only; BLOCKED on source/asset license attribution; maintainer approval PENDING','limitations':['Git alone omits retained crate archives and raw payloads','Historical resources mapped to exact preimages; old manifest not rewritten','Current binding integrity does not establish legal clearance, product operation, maintainer approval or execution authorization','No reproducible candidate binary or vendor-ready Cargo installation exists; no trial performed'],'inherited_resources':inherited,'files':files}
raw=(json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode()
with (B/'freeze.json').open('xb') as f:f.write(raw)
with (B/'freeze.sha256').open('x') as f:f.write(hashlib.sha256(raw).hexdigest()+'  freeze.json\n')
print(hashlib.sha256(raw).hexdigest(),len(files),'files')
