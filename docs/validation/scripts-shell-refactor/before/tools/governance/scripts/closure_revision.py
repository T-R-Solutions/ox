"""Exact-content task closure succession; never grants generic path exemptions."""
import hashlib
import json
from pathlib import Path

REGISTRY = 'docs/validation/scripts-task-closure/revision.json'
REVIEWED = '252155ba4dbe8defb06e55fae98367c457a646965d2a033b538dbb71114be54b'


def predecessor(root, relative, data):
    data = security_predecessor(root, relative, data)
    registry = root / REGISTRY
    if not registry.exists():
        return data
    if registry.is_symlink() or hashlib.sha256(registry.read_bytes()).hexdigest() != REVIEWED:
        raise ValueError('Closure succession registry changed')
    rows = json.loads(registry.read_text())['records']
    for row in rows:
        if row['destination'] != relative:
            continue
        path = root / row['previous']
        if (not path.resolve().is_relative_to(root.resolve()) or not path.is_file()
                or any(p.is_symlink() for p in (path, *path.parents) if p.is_relative_to(root))):
            raise ValueError('Missing/escaping closure predecessor')
        previous = path.read_bytes()
        if hashlib.sha256(previous).hexdigest() != row['previous_sha256']:
            raise ValueError('Closure predecessor changed')
        if hashlib.sha256(data).hexdigest() == row['sha256']:
            return previous
    return data


SECURITY_REGISTRY = 'docs/validation/scripts-security-quality/revision.json'
SECURITY_REVIEWED = 'a8813214de37239eba23e8830a550d6af898c0143e0ad1b99957303f369b232b'


def security_predecessor(root, relative, data):
    registry = root / SECURITY_REGISTRY
    if not registry.exists():
        if (root/'docs/decisions/scripts-security-quality.md').exists():
            raise ValueError('Missing security succession registry')
        return data
    if (not registry.is_file() or any(p.is_symlink() for p in (registry,*registry.parents) if p.is_relative_to(root))
            or hashlib.sha256(registry.read_bytes()).hexdigest()!=SECURITY_REVIEWED):
        raise ValueError('Security succession registry changed')
    doc=json.loads(registry.read_text())
    for row in doc['records']:
        if row['destination']!=relative:continue
        p=root/row['previous']
        if (not p.resolve().is_relative_to(root.resolve()) or not p.is_file()
                or any(x.is_symlink() for x in (p,*p.parents) if x.is_relative_to(root))):
            raise ValueError('Missing/escaping security predecessor')
        previous=p.read_bytes()
        if hashlib.sha256(previous).hexdigest()!=row['previous_sha256']:
            raise ValueError('Security predecessor changed')
        active=root/relative
        if (active.is_file() and active.read_bytes()==data
                and hashlib.sha256(data).hexdigest()==row['previous_sha256']):
            raise ValueError('Security succession predecessor downgrade: '+relative)
        if hashlib.sha256(data).hexdigest()==row['sha256']:
            return previous
    return data
