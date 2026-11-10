"""Verify the reviewed packet without building or executing any product/fixture."""
import hashlib
import json
from pathlib import Path
R = Path(__file__).resolve().parents[3]
B = Path(__file__).resolve().parent
raw=(B/'freeze.json').read_bytes()
assert hashlib.sha256(raw).hexdigest() == (B/'freeze.sha256').read_text().split()[0], 'freeze identity'
doc=json.loads(raw)
seen=set()
for row in doc['files']:
    relative=Path(row['path'])
    assert not relative.is_absolute() and '..' not in relative.parts, row['path']
    assert row['path'] not in seen, 'duplicate path'
    seen.add(row['path']);p=R/relative
    assert p.is_file() and p.resolve().is_relative_to(R), row['path']
    assert not any((R/q).is_symlink() for q in [relative,*relative.parents]), row['path']
    assert hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256'], row['path']
print(f'PASS: {len(seen)} reviewed files, sha256={hashlib.sha256(raw).hexdigest()}')
# Additional successor links and inherited historical-resource checks.
pre=doc['predecessor'];assert hashlib.sha256((R/pre['path']).read_bytes()).hexdigest()==pre['sha256']
indexed={x['path']:x for x in doc['files']}
old=json.loads((R/pre['path']).read_text());old_rows={x['path']:x for x in old['files']}
assert len(doc['inherited_resources'])==len(old_rows)
assert len({x['original_path'] for x in doc['inherited_resources']})==len(old_rows)
for row in doc['inherited_resources']:
 assert row['sha256']==old_rows[row['original_path']]['sha256']
 assert indexed[row['retained_path']]['sha256']==row['sha256']
for row in json.loads((B/'license-matrix.json').read_text()):
 for item in [row['archive'],*row['texts']]:assert indexed[item['path']]['sha256']==item['sha256']
for row in json.loads((B/'iced-applicability.json').read_text()):
 for key in ['archive','submanifest','root_manifest','main_text']:
  item=row[key];assert indexed[item['path']]['sha256']==item['sha256']
assert len(json.loads((B/'license-matrix.json').read_text()))==159
assert len(json.loads((B/'graph-review.json').read_text())['exclusions'])==113
print('PASS: predecessor identity, 1388 inherited resource links, license/archive/text links; preparation remains BLOCKED')
