"""Resolve only the registered README successor to its integration preimage."""
import hashlib
import json
import re
from pathlib import Path

BASE = 'docs/validation/readme-preservation-20261104'
REGISTRY = BASE + '/revision.json'
DECISION = 'docs/decisions/readme-preservation.md'
PREVIOUS = BASE + '/before/README.md.bin'
VISUAL_BASE = 'docs/validation/documentation-visuals-20261104'
VISUAL_REGISTRY = VISUAL_BASE + '/revision.json'
VISUAL_DECISION = 'docs/decisions/documentation-visuals.md'
VISUAL_PREVIOUS = VISUAL_BASE + '/before/README.md.bin'


def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Duplicate README successor property: ' + key)
        result[key] = value
    return result


def file(root, relative):
    path = root / relative
    if (not path.resolve().is_relative_to(root.resolve()) or not path.is_file()
            or any((root / parent).is_symlink() for parent in
                   [Path(relative), *Path(relative).parents])):
        raise ValueError('Missing, escaping or symlinked README successor file: ' + relative)
    return path


def record(root, expected):
    registry = root / REGISTRY
    if not registry.exists() and not registry.is_symlink():
        if (root / BASE).exists():
            raise ValueError('Missing README successor registry')
        return None
    document = json.loads(file(root, REGISTRY).read_text(), object_pairs_hook=unique)
    if (not isinstance(document, dict) or document.get('schema_version') != 1
            or document.get('revision') != 'readme-preservation-001'
            or document.get('decision') != DECISION):
        raise ValueError('Unexpected README successor revision')
    file(root, DECISION)
    rows = document.get('records')
    if (not isinstance(rows, list) or len(rows) != 1 or not isinstance(rows[0], dict)
            or rows[0].get('destination') != 'README.md'
            or rows[0].get('previous') != PREVIOUS):
        raise ValueError('Unexpected README successor scope')
    row = rows[0]
    if (not re.fullmatch('[a-f0-9]{64}', str(row.get('sha256')))
            or row.get('previous_sha256') != expected):
        raise ValueError('Invalid README successor digest or integration binding')
    if hashlib.sha256(file(root, PREVIOUS).read_bytes()).hexdigest() != expected:
        raise ValueError('README successor predecessor changed')
    return row


def predecessor(root, relative, data, expected):
    if relative != 'README.md':
        return data
    row = record(root, expected)
    if row:
        data = visual_predecessor(root, data, row['sha256'])
    if row and hashlib.sha256(data).hexdigest() == row['sha256']:
        return file(root, PREVIOUS).read_bytes()
    return data


def errors(root, expected):
    row = record(root, expected)
    if row is None:
        return []
    try:
        current = file(root, 'README.md')
    except ValueError as error:
        return [str(error)]
    visual = visual_record(root, row['sha256'])
    expected_current = visual['sha256'] if visual else row['sha256']
    if hashlib.sha256(current.read_bytes()).hexdigest() != expected_current:
        return ['README successor current changed: README.md']
    return []


def excluded_product_reference(root, source, target):
    """Exact declared source references in a governance-only tree, never escapes."""
    if (root / 'application').exists() or not target.is_relative_to(root):
        return False
    visual = (root / VISUAL_BASE).exists()
    registry = (VISUAL_BASE if visual else BASE) + '/product-references.json'
    document = json.loads(file(root, registry).read_text(), object_pairs_hook=unique)
    if (document.get('schema_version') != 1 or document.get('decision') != (VISUAL_DECISION if visual else DECISION)
            or not isinstance(document.get('records'), list)):
        raise ValueError('Invalid excluded product references')
    sources = [row.get('source') for row in document['records'] if isinstance(row, dict)]
    allowed = {'README.md', 'docs/README.md', 'docs/development/governance.md',
               'docs/architecture/application.md', 'docs/architecture/contracts.md'}
    if len(sources) != len(document['records']) or len(sources) != len(set(sources)) or set(sources) != allowed:
        raise ValueError('Unexpected excluded-reference source scope')
    from governance_support import product_record
    for row in document['records']:
        if (not re.fullmatch('[a-f0-9]{64}', str(row.get('sha256')))
                or not isinstance(row.get('targets'), dict) or not row['targets']):
            raise ValueError('Invalid excluded-reference source digest or targets')
        for name, digest in row['targets'].items():
            path = Path(name)
            if (path.is_absolute() or '..' in path.parts
                    or not (name.startswith('application/') or product_record(path))
                    or not re.fullmatch('[a-f0-9]{64}', str(digest))):
                raise ValueError('Invalid excluded-reference target')
    relative = target.relative_to(root).as_posix()
    if not (relative.startswith('application/') or product_record(Path(relative))):
        return False
    for row in document['records']:
        if row['source'] == source:
            if hashlib.sha256(file(root, source).read_bytes()).hexdigest() != row['sha256']:
                return False
            return bool(re.fullmatch('[a-f0-9]{64}', str(row['targets'].get(relative))))
    return False


def visual_record(root, expected):
    registry = root / VISUAL_REGISTRY
    if not registry.exists() and not registry.is_symlink():
        if (root / VISUAL_BASE).exists():
            raise ValueError('Missing visual README successor registry')
        return None
    document = json.loads(file(root, VISUAL_REGISTRY).read_text(), object_pairs_hook=unique)
    if (not isinstance(document, dict) or document.get('schema_version') != 1
            or document.get('revision') != 'readme-visuals-001'
            or document.get('decision') != VISUAL_DECISION):
        raise ValueError('Unexpected visual README successor revision')
    file(root, VISUAL_DECISION)
    rows = document.get('records')
    if (not isinstance(rows, list) or len(rows) != 1 or not isinstance(rows[0], dict)
            or rows[0].get('destination') != 'README.md'
            or rows[0].get('previous') != VISUAL_PREVIOUS):
        raise ValueError('Unexpected visual README successor scope')
    row = rows[0]
    if (not re.fullmatch('[a-f0-9]{64}', str(row.get('sha256')))
            or row.get('previous_sha256') != expected
            or hashlib.sha256(file(root, VISUAL_PREVIOUS).read_bytes()).hexdigest() != expected):
        raise ValueError('Invalid visual README digest or predecessor binding')
    return row


def visual_predecessor(root, data, expected):
    row = visual_record(root, expected)
    if row and hashlib.sha256(data).hexdigest() == row['sha256']:
        return file(root, VISUAL_PREVIOUS).read_bytes()
    return data
