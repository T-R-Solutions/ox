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
