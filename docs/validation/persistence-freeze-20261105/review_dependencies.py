"""Offline inventory from versioned Linux Cargo graph and checksum-verified archives.
No build, executable fixture, network or product modification.
"""
from pathlib import Path
import hashlib
import json
import tarfile
import tomllib

R = Path(__file__).resolve().parents[3]
B = Path(__file__).resolve().parent
LOCAL = R / '.local/build/persistence-experiment-preflight-20261105'
def load(p): return json.loads(p.read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p, data):
    p.parent.mkdir(parents=True, exist_ok=True)
    if p.exists():
        assert p.read_bytes() == data, f'Preserve unexpected bytes: {p}'
    else: p.write_bytes(data)
d = load(B/'linux-metadata.json')
nodes = {n['id']: n for n in d['resolve']['nodes']}
seen = set(); todo = [(d['resolve']['root'], 'target')]
while todo:
    i, role = todo.pop()
    if (i,role) in seen: continue
    seen.add((i,role))
    for edge in nodes[i]['deps']:
        for k in edge['dep_kinds']:
            if k['kind'] != 'dev':
                todo.append((edge['pkg'], 'build' if role == 'build' or k['kind'] == 'build' else 'target'))
old = load(R/'docs/validation/persistence-preflight-20261105/successor/licenses.json')
by = {(p['name'],p['version']):p for p in old}
lock = {(p['name'], p['version']): p.get('checksum') for p in tomllib.loads((LOCAL/'dependencies/Cargo.lock').read_text())['package']}
rows=[]
for p in load(LOCAL/'dependencies/metadata.json')['packages']:
    if not p['source']: continue
    row = dict(by[p['name'],p['version']])
    assert row['registry_checksum'] == lock[p['name'], p['version']]
    row['roles'] = sorted(k for i,k in seen if i == p['id'])
    row['id'] = p['id']
    if not row['roles']:
        row['disposition'] = 'excluded: not reachable in Linux-filtered normal/build root graph; see linux-metadata.json'
    else:
        row['disposition'] = 'applicable; text and compatibility review below, no legal clearance'
        source = Path(p['manifest_path']).parent
        # Standard Cargo registry cache sibling, read only. Retain original archives.
        archive = source.parents[1].parent/'cache'/source.parent.name/(source.name+'.crate')
        assert sha(archive) == row['registry_checksum'], archive
        retained = LOCAL/'reviewed-crates'/archive.name
        write(retained, archive.read_bytes())
        row['archive']={'path':str(retained.relative_to(R)), 'sha256':sha(retained)}
        row['texts']=[]
        with tarfile.open(retained) as tar:
            for entry in tar.getmembers():
                name=Path(entry.name)
                if not entry.isfile() or not any(t in name.name.lower() for t in ['license','licence','notice','copying','copyright']): continue
                assert not name.is_absolute() and '..' not in name.parts
                data=tar.extractfile(entry).read()
                dest=B/'licenses'/source.name/Path(*name.parts[1:])
                write(dest,data)
                row['texts'].append({'path':str(dest.relative_to(R)), 'sha256':sha(dest), 'archive_member':entry.name})
        row['obligations'] = ['Retain applicable copyright, license and disclaimer texts and origin; no relicensing by root GPL.']
        expr=row['declared_license'] or ''
        if 'Apache' in expr: row['obligations'].append('If using Apache branch: license copy, retain relevant notices/NOTICE and mark modifications; patent terms apply.')
        if 'Unicode' in expr: row['obligations'].append('Unicode notice required in addition to selected MIT/Apache branch.')
        if 'Zlib' in expr: row['obligations'].append('If using Zlib branch: preserve notice; mark altered sources; do not misrepresent origin.')
        if 'LLVM' in expr: row['obligations'].append('Retain LLVM exception if selecting that branch; no automatic branch selection.')
        row['compatibility'] = 'PENDING: no branch selection/distribution compatibility clearance; GPL-3.0-only own-material ADR retained'
        if row['name'] == 'iced_core':
            row['main_license_gap'] = 'Only third-party DRUID_LICENSE present; main inherited MIT text absent'
        row['text_status'] = 'retained for review; embedded assets/native system libraries still require build attribution' if row['texts'] else 'BLOCKED: versioned package lacks license/NOTICE text; inherited declaration is insufficient'
    rows.append(row)
(B/'linux-licenses.json').write_text(json.dumps(rows,indent=2)+'\n')
summary={'applicable':sum(bool(x['roles']) for x in rows),'excluded':sum(not x['roles'] for x in rows),'missing_texts':[x['name']+'@'+x['version'] for x in rows if x['roles'] and (not x['texts'] or x.get('main_license_gap'))], 'method':'cargo metadata --locked --offline --filter-platform x86_64-unknown-linux-gnu; normal/build graph from isolated root; dev edges excluded; build role propagates; archive checksums checked against lock inventory'}
(B/'license-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
