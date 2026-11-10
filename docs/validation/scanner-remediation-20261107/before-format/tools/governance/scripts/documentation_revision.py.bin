"""Exact-content successor for the authorized technical-documentation visual method."""
from pathlib import Path
import hashlib
import json
import re

BASE = 'docs/validation/technical-documentation-visuals-20261104'
REGISTRY = BASE + '/revision.json'
DECISION = 'docs/decisions/technical-documentation-visuals.md'
REVISION = 'technical-documentation-visuals-001'
SKILL = '.codex/skills/technical-documentation/'
EXISTING = frozenset({SKILL + 'SKILL.md', 'sdd/chain/technical-documentation.md'})
ADDED = frozenset(SKILL + 'references/' + name + '.md' for name in (
    'visual-quality', 'mermaid', 'media-and-data', 'evaluation-cases'))


def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Duplicate documentation revision property: ' + key)
        result[key] = value
    return result


def file(root, relative):
    path = root / relative
    if (path.is_symlink() or not path.is_file()
            or not path.resolve().is_relative_to(root.resolve())):
        raise ValueError('Missing or escaping documentation revision file: ' + relative)
    return path


def digest(data):
    return hashlib.sha256(data).hexdigest()


def records(root):
    registry = root / REGISTRY
    if not registry.exists() and not registry.is_symlink():
        if any((root / name).exists() for name in ADDED):
            raise ValueError('Missing documentation visual revision registry')
        return {}
    document = json.loads(file(root, REGISTRY).read_text(), object_pairs_hook=unique)
    if (document.get('revision') != REVISION or document.get('decision') != DECISION
            or document.get('schema_version') != 1):
        raise ValueError('Unexpected documentation visual revision')
    file(root, DECISION)
    rows = document.get('records', [])
    paths = [row['destination'] for row in rows]
    if len(paths) != len(set(paths)) or set(paths) != EXISTING | ADDED:
        raise ValueError('Documentation visual revision scope differs')
    for row in rows:
        if not re.fullmatch('[a-f0-9]{64}', str(row.get('sha256'))):
            raise ValueError('Invalid documentation current digest')
        name = row['destination']
        if name in ADDED:
            if row.get('previous') is not None or row.get('previous_sha256') is not None:
                raise ValueError('Unexpected documentation predecessor')
        else:
            if row.get('previous') != BASE + '/before/' + name + '.bin':
                raise ValueError('Unexpected documentation predecessor path')
            previous = file(root, row['previous']).read_bytes()
            if digest(previous) != row.get('previous_sha256'):
                raise ValueError('Documentation predecessor changed: ' + name)
    return {row['destination']: row for row in rows}


def predecessor(root, relative, data):
    if relative not in EXISTING | ADDED:
        return data
    row = records(root).get(relative)
    if row and row['previous'] is not None and digest(data) == row['sha256']:
        return file(root, row['previous']).read_bytes()
    return data


def errors(root):
    result = []
    for name, row in records(root).items():
        try:
            data = file(root, name).read_bytes()
        except ValueError as error:
            result.append(str(error))
            continue
        if digest(data) != row['sha256']:
            result.append('Documentation visual current changed: ' + name)
    return result
