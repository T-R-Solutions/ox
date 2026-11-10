"""Read-only verification of r3 content, inherited bytes and local resource copies."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[3]; B=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(B/'freeze.json')==(B/'freeze.sha256').read_text().split()[0]
d=json.loads((B/'freeze.json').read_text());seen={}
for x in d['files']:
 n=Path(x['path']);assert not n.is_absolute() and '..' not in n.parts
 assert str(n) not in seen;seen[str(n)]=x
 p=R/n;assert p.is_file() and p.resolve().is_relative_to(R)
 assert not any((R/q).is_symlink() for q in [n,*n.parents])
 assert sha(p)==x['sha256'],str(n)
 assert p.stat().st_size==x['bytes']
p=R/d['predecessor']['path'];assert sha(p)==d['predecessor']['sha256']
old={x['path']:x for x in json.loads(p.read_text())['files']}
assert len(old)==len(d['inherited_resources'])
assert len({x['original_path'] for x in d['inherited_resources']})==len(old)
for x in d['inherited_resources']:
 assert old[x['original_path']]['sha256']==x['sha256']
 assert seen[x['retained_path']]['sha256']==x['sha256']
for x in json.loads((B/'local-resources.json').read_text()):assert seen[x['retained_path']]['sha256']==x['sha256']
for x in json.loads((B/'primary-index.json').read_text()):
 assert seen[x['path']]['sha256']==x['sha256']
 assert seen[x['archive']]['sha256']==x['archive_sha256']
print('PASS:',len(seen),'files;',len(old),'inherited identities; primary/archive/local-resource links')
print('SHA-256',sha(B/'freeze.json'))
print('Preparation BLOCKED; maintainer approval PENDING; no execution permission')
