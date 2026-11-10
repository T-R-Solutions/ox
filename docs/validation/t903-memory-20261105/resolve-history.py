from pathlib import Path
import json,hashlib,stat
r=Path(__file__).resolve().parents[3];b=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();cache={}
def digest(p):
 if p not in cache:cache[p]=sha(p)
 return cache[p]
needed={};records=[]
for p in (r/'sdd/features').glob('*/evidence.json'):
 d=json.loads(p.read_text())
 for e in d['evidence']:
  for x in e.get('inputs',[]):
   target=r/x['path']
   if not target.is_file() or digest(target)!=x['sha256']:needed.setdefault(x['sha256'],[]).append((p,e['id'],x['path']))
archives={}
for p in (r/'docs/validation').rglob('*'):
 if stat.S_ISREG(p.lstat().st_mode) and (any(part.startswith('before') for part in p.parts) or p.suffix=='.bin'):
  h=digest(p)
  if h in needed:archives[h]=str(p.relative_to(r))
missing={h:items for h,items in needed.items() if h not in archives}
if missing:
 print('Missing preimages',missing);raise SystemExit(1)
for p in (r/'sdd/features').glob('*/evidence.json'):
 d=json.loads(p.read_text());changed=False
 for e in d['evidence']:
  for x in e.get('inputs',[]):
   if x['sha256'] in needed and x['path'] in [v[2] for v in needed[x['sha256']]]:
    original=x['path'];x['path']=archives[x['sha256']];changed=True
    records.append({'consumer':str(p.relative_to(r)),'evidence':e['id'],'original':original,'sha256':x['sha256'],'preimage':x['path']})
 if changed:p.write_text(json.dumps(d,indent=2)+'\n')
previous=json.loads((b/'historical-preimages.json').read_text()) if (b/'historical-preimages.json').exists() else []
version=len(list(b.glob('historical-preimages-[0-9]*.json')))+1
(b/f'historical-preimages-{version}.json').write_text(json.dumps(records,indent=2)+'\n')
(b/'historical-preimages.json').write_text(json.dumps(previous+records,indent=2)+'\n');print('Resolved',len(records),'bindings without changing digests')
