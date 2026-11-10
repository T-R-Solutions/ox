"""Issue successor once; preserve predecessor identities via exact historical bytes."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[3];B=Path(__file__).resolve().parent;P=R/'docs/validation/persistence-freeze-20261105-r2'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return str(p.relative_to(R))
entry=json.loads((B/'entry.json').read_text())['files'];changes=[]
for n,h in entry.items():
 p=R/n
 if not p.is_file() or sha(p)!=h:changes.append(n)
allowed={'sdd/features/product-local-persistence/'+n for n in ['plan.md','tasks.md','converge.md','evidence.json']}
assert set(changes)==allowed,changes
(B/'preservation.json').write_text(json.dumps({'criterion':'Preserve previous packages, product operational inputs and unrelated edits','method':'Compare exact SHA-256 against entry inventory','changed_paths':changes,'all_other_entry_files_unchanged':True,'limitations':'Entry inventory excludes application target build artifacts; no product command executed'},indent=2)+'\n')
old=json.loads((P/'freeze.json').read_text());names=set();inherited=[]
preimages={sha(p):p for p in (B/'before').rglob('*') if p.is_file()}
local={x['original_path']:x for x in json.loads((B/'local-resources.json').read_text())}
for x in old['files']:
 p=R/x['path']
 if x['path'] in local:q=R/local[x['path']]['retained_path']
 elif p.is_file() and sha(p)==x['sha256']:q=p
 else:q=preimages[x['sha256']]
 assert sha(q)==x['sha256'];names.add(rel(q))
 # Current inputs remain current; historical identities use the mapped preimage.
 if p.is_file():names.add(rel(p))
 inherited.append({'original_path':x['path'],'retained_path':rel(q),'sha256':x['sha256'],'use':'historical preimage' if q!=p else 'unchanged resource'})
for p in B.rglob('*'):
 if p.is_file() and p.name not in ['freeze.json','freeze.sha256','freeze-verification.log']:names.add(rel(p))
for n in allowed:names.add(n)
# Original package manifests/checks stay unchanged and become inherited context.
names.update([rel(P/'freeze.json'),rel(P/'freeze.sha256'),rel(P/'freeze-verification.log')])
files=[]
for n in sorted(names):
 p=R/n;assert p.is_file() and p.resolve().is_relative_to(R)
 assert not any((R/q).is_symlink() for q in [Path(n),*Path(n).parents])
 files.append({'path':n,'sha256':sha(p),'bytes':p.stat().st_size})
d={'schema_version':1,'successor_id':B.name,'predecessor':{'path':rel(P/'freeze.json'),'sha256':sha(P/'freeze.json')},'scope':'Local T011/T009 documentary/license review; preparation BLOCKED; maintainer approval PENDING; no execution authorization','inherited_resources':inherited,'files':files,'verification':'python3 docs/validation/persistence-freeze-20261105-r3/verify-freeze.py','limitations':['Keep full resource closure including resources/.local; Git alone insufficient','Historical resources use exact preimages, never renewed verdicts','Manifest excludes itself, detached digest and final verification log to avoid circular hashes','Identity/structure do not establish licensing applicability, compatibility, storage behavior or approval']}
raw=(json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode()
with (B/'freeze.json').open('xb') as f:f.write(raw)
with (B/'freeze.sha256').open('x') as f:f.write(hashlib.sha256(raw).hexdigest()+'  freeze.json\n')
print(hashlib.sha256(raw).hexdigest(),len(files),'files')
