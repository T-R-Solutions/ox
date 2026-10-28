"""Offline structural checks for this local SDD integration (standard library only)."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

STATES = {'APROVADO', 'REPROVADO', 'NÃO VERIFICADO', 'INCONCLUSIVO', 'NÃO APLICÁVEL'}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def local_file(root, value):
    if not isinstance(value, str) or not value or Path(value).is_absolute():
        raise ValueError(f'Expected relative file: {value!r}')
    path = (root / value).resolve()
    if not path.is_relative_to(root.resolve()) or not path.is_file():
        raise ValueError(f'Missing or escaping file: {value}')
    return path


def strict_json(path):
    """Reject ambiguous objects before any status/trace reconciliation."""
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f'Duplicate JSON property {key!r} in {path}')
            result[key] = value
        return result
    return json.loads(path.read_text(), object_pairs_hook=unique)


def acceptance_ids(text):
    """Declarations only: unquoted AC-N: text or - AC-N → REQ-N: text.

    Fenced code and HTML comments are non-normative. This is a deliberately
    small line grammar, not a general Markdown parser.
    """
    ids = set()
    fence = None
    comment = False
    for line_no, line in enumerate(text.splitlines(), 1):
        marker = re.match(r'^ {0,3}(`{3,}|~{3,})(.*)$', line)
        if fence is not None:
            if marker:
                token, tail = marker.groups()
                if token[0] == fence[0] and len(token) >= len(fence) and not tail.strip():
                    fence = None
            continue
        if marker and not comment:
            fence = marker[1]
            continue
        # Comments inside fenced examples (including info strings) are literal.
        visible = ''
        rest = line
        while rest:
            if comment:
                _, end, rest = rest.partition('-->')
                if not end:
                    break
                comment = False
            else:
                before, start, rest = rest.partition('<!--')
                visible += before
                if not start:
                    break
                comment = True
        line = visible
        if not re.match(r'^ {0,3}(?:- )?AC-', line):
            continue
        match = re.fullmatch(r' {0,3}(?:- )?(AC-\d+)(?: → REQ-\d+)?:[ \t]*(\S.*)', line)
        if not match:
            raise ValueError(f'Malformed acceptance declaration at line {line_no}: {line}')
        identifier = match[1]
        if identifier in ids:
            raise ValueError(f'Duplicate acceptance declaration {identifier} at line {line_no}')
        ids.add(identifier)
    return ids


def input_errors(document, root, rows, feature, require_fresh):
    """Content bindings are scoped per observation; they do not attest execution."""
    if not isinstance(document, dict):
        return []  # schema diagnostics belong to evidence_errors
    version = document.get('schema_version')
    if version != 2:
        return ['Freshness requires evidence schema_version 2'] if require_fresh else []
    errors, bindings = [], {}
    evidence = document.get('evidence', [])
    if not isinstance(evidence, list):
        return []
    for item in evidence:
        if not isinstance(item, dict):
            continue
        identifier = item.get('id')
        if not isinstance(identifier, str):
            continue
        inputs = item.get('inputs')
        if not isinstance(inputs, list) or not inputs:
            errors.append(f'Missing input bindings: {identifier}')
            continue
        paths = set()
        for value in inputs:
            if (not isinstance(value, dict) or value.get('role') not in
                    ('implementation', 'oracle', 'configuration', 'contract', 'other')):
                errors.append(f'Invalid input binding: {identifier}')
                continue
            try:
                path = local_file(root, value.get('path'))
                relative = str(path.relative_to(root.resolve()))
                if relative in paths:
                    errors.append(f'Duplicate input binding: {identifier}: {relative}')
                paths.add(relative)
                if digest(path) != value.get('sha256'):
                    errors.append(f'Stale input: {identifier}: {relative}')
            except ValueError as exc:
                errors.append(str(exc))
        bindings[identifier] = paths
    if not isinstance(rows, list) or not isinstance(document.get('requirements'), list):
        return errors
    for criterion in document['requirements']:
        if not isinstance(criterion, dict) or criterion.get('status') not in ('APROVADO', 'REPROVADO'):
            continue
        refs = criterion.get('evidence_ids', [])
        if not isinstance(refs, list) or any(not isinstance(x, str) for x in refs):
            continue
        linked = set().union(*(bindings.get(ref, set()) for ref in refs))
        required = {str((feature / name).relative_to(root)) for name in
                    ('spec.md', 'plan.md', 'tasks.md', 'traceability.json')}
        for row in rows:
            if isinstance(row, dict) and row.get('acceptance') == criterion.get('id'):
                for key in ('implementation', 'oracle'):
                    try:
                        required.add(str(local_file(root, row.get(key)).relative_to(root.resolve())))
                    except ValueError:
                        pass  # trace_errors reports path failures
        for missing in sorted(required - linked):
            errors.append(f'Missing criterion input binding: {criterion.get("id")}: {missing}')
    return errors


def evidence_errors(document, root):
    errors = []
    if not isinstance(document, dict):
        return ['Evidence document must be an object']
    if type(document.get('schema_version')) is not int or document['schema_version'] not in (1, 2):
        errors.append('Unsupported schema_version')
    if not isinstance(document.get('environment'), str) or not document['environment'].strip():
        errors.append('Missing environment')
    if (not isinstance(document.get('limitations'), list)
            or any(not isinstance(x, str) for x in document['limitations'])):
        errors.append('Missing limitations list')
    evidence = document.get('evidence', [])
    requirements = document.get('requirements', [])
    if not isinstance(evidence, list) or not isinstance(requirements, list) or not requirements:
        return errors + ['Evidence/requirements must be lists; criteria must not be empty']
    ids = set()
    for item in evidence:
        if not isinstance(item, dict):
            errors.append('Invalid evidence object'); continue
        for field in ('id', 'kind', 'command_or_method', 'observed_result', 'artifact', 'sha256'):
            if not isinstance(item.get(field), str) or not item[field].strip():
                errors.append(f'Missing evidence field: {field}')
        identifier = item.get('id')
        if not isinstance(identifier, str): continue
        if identifier in ids: errors.append(f'Duplicate evidence: {identifier}')
        ids.add(identifier)
        if not isinstance(item.get('kind'), str) or item['kind'] not in {'test', 'benchmark', 'inspection', 'trace', 'other'}:
            errors.append(f'Invalid evidence kind: {identifier}')
        try:
            path = local_file(root, item.get('artifact'))
            if digest(path) != item.get('sha256'):
                errors.append(f'Artifact hash mismatch: {identifier}')
        except ValueError as exc: errors.append(str(exc))
    criteria = set()
    for row in requirements:
        if not isinstance(row, dict):
            errors.append('Invalid criterion object'); continue
        identifier = row.get('id')
        if not isinstance(identifier, str) or not identifier.strip():
            errors.append('Missing criterion id'); continue
        if identifier in criteria: errors.append(f'Duplicate criterion: {identifier}')
        criteria.add(identifier)
        if not isinstance(row.get('criterion'), str) or not row['criterion'].strip():
            errors.append(f'Missing criterion text: {identifier}')
        if not isinstance(row.get('status'), str) or row['status'] not in STATES:
            errors.append(f'Invalid status: {identifier}'); continue
        refs = row.get('evidence_ids')
        if not isinstance(refs, list) or any(not isinstance(x, str) for x in refs):
            errors.append(f'Invalid evidence_ids: {identifier}'); continue
        if len(refs) != len(set(refs)) or not set(refs) <= ids:
            errors.append(f'Duplicate or dangling evidence IDs: {identifier}')
        if row.get('status') in {'APROVADO', 'REPROVADO'} and not refs:
            errors.append(f'Decided criterion without evidence: {identifier}')
        if (row.get('status') == 'NÃO APLICÁVEL'
                and (not isinstance(row.get('reason'), str) or not row['reason'].strip())):
            errors.append(f'Inapplicable criterion without reason: {identifier}')
    return errors


def trace_errors(rows, root, feature, document=None):
    """Check explicit links, not semantic equivalence of free-text requirements."""
    errors = []
    texts = {name: (feature / (name + '.md')).read_text() for name in ('spec', 'plan', 'tasks')}
    expected = acceptance_ids(texts['spec'])
    if not expected:
        errors.append('Spec has no acceptance IDs')
    if not isinstance(rows, list):
        return errors + ['Traceability must be a list']
    valid = []
    for row in rows:
        fields = ('acceptance', 'requirement', 'decision', 'risk', 'implementation', 'oracle')
        if (not isinstance(row, dict)
                or any(not isinstance(row.get(k), str) or not row[k].strip() for k in fields)
                or not isinstance(row.get('tasks'), list)
                or any(not isinstance(t, str) or not t.strip() for t in row['tasks'])):
            errors.append('Invalid traceability row')
            continue
        valid.append(row)
    rows = valid
    actual = [row['acceptance'] for row in rows]
    if set(actual) != expected or len(actual) != len(set(actual)):
        errors.append('Traceability must cover each spec acceptance ID exactly once')
    for row in rows:
        for key, source in [('requirement', 'spec'), ('decision', 'plan'), ('risk', 'plan')]:
            if not re.search(r'\b' + re.escape(row[key]) + r'\b', texts[source]):
                errors.append(f'Unknown {key}: {row[key]}')
        if not row.get('tasks'): errors.append('Trace row has no tasks')
        for task in row.get('tasks', []):
            if not re.search(r'\b' + re.escape(task) + r'\b', texts['tasks']):
                errors.append(f'Unknown task: {task}')
        for key in ('implementation', 'oracle'):
            try: local_file(root, row[key])
            except ValueError as exc: errors.append(str(exc))
    if document is not None:
        requirements = document.get('requirements', []) if isinstance(document, dict) else []
        reported = {row['id'] for row in requirements
                    if isinstance(row, dict) and isinstance(row.get('id'), str)} if isinstance(requirements, list) else set()
        if not expected <= reported: errors.append('Missing acceptance result in evidence')
    return errors


def feature_errors(root, check_evidence=True, require_approved=False, directory=None, require_fresh=False):
    """Check every direct feature; keep integrity distinct from acceptance."""
    directory = directory or root / 'sdd/features'
    if not directory.exists() and not require_approved:
        return []
    if not directory.is_dir() or directory.is_symlink():
        return ['Missing or symlink feature directory']
    features = sorted(directory.iterdir())
    errors = []
    count = 0
    for feature in features:
        if feature.is_symlink():
            errors.append(f'{feature.name}: Symlink feature is not allowed')
            continue
        if not feature.is_dir():
            continue
        count += 1
        prefix = str(feature.relative_to(root))
        try:
            for name in ('spec.md', 'plan.md', 'tasks.md', 'traceability.json'):
                local_file(root, str((feature / name).relative_to(root)))
            document = None
            if check_evidence:
                path = local_file(root, str((feature / 'evidence.json').relative_to(root)))
                document = strict_json(path)
                errors.extend(f'{prefix}: {e}' for e in evidence_errors(document, root))
            rows = strict_json(feature / 'traceability.json')
            errors.extend(f'{prefix}: {e}' for e in trace_errors(rows, root, feature, document))
            if check_evidence:
                errors.extend(f'{prefix}: {e}' for e in input_errors(document, root, rows, feature, require_fresh))
            if require_approved:
                expected = acceptance_ids((feature / 'spec.md').read_text())
                requirements = document.get('requirements', []) if isinstance(document, dict) else []
                if isinstance(requirements, list):
                    for row in requirements:
                        if isinstance(row, dict) and isinstance(row.get('id'), str) and row['id'] in expected:
                            if row.get('status') not in {'APROVADO', 'NÃO APLICÁVEL'}:
                                errors.append(f"{prefix}: Acceptance {row['id']} is {row.get('status')}")
        except (OSError, ValueError, KeyError, TypeError) as exc:
            errors.append(f'{prefix}: Could not audit feature: {exc}')
    if not count and require_approved:
        errors.append('No feature directories found')
    return errors



def markdown_errors(folder):
    """Resolve inline file links without opening external URLs or following symlinks."""
    errors = []
    for p in sorted(folder.rglob('*')):
        if p.is_symlink():
            errors.append(f'Symlink is not portable: {p}')
            continue
        if p.suffix != '.md' or not p.is_file():
            continue
        for raw in re.findall(r'\[[^\]]*\]\(([^)]+)\)', p.read_text()):
            parts = urlsplit(raw.strip('<>'))
            if parts.scheme or parts.netloc or not parts.path:
                continue
            target = (p.parent / unquote(parts.path)).resolve()
            if not target.is_relative_to(folder.resolve()) or not target.is_file():
                errors.append(f'Nonportable or missing link: {p}: {raw}')
    return errors


def skill_errors(folder, expected=None):
    errors = []
    if folder.is_symlink() or not folder.is_dir():
        return [f'Missing or symlink skill folder: {folder}']
    entry = folder / 'SKILL.md'
    if not entry.is_file() or entry.is_symlink():
        return [f'Missing or symlink SKILL.md: {folder}']
    text = entry.read_text()
    header = re.match(r'\A---\n(.*?)\n---(?:\n|$)', text, re.S)
    name = re.search(r'^name: ([a-z0-9-]+)$', header[1], re.M) if header else None
    if not name or not re.search(r'^description: .+', header[1], re.M):
        errors.append(f'Invalid skill metadata: {entry}')
    elif expected and name[1] != expected:
        errors.append(f'Skill name mismatch: expected {expected}, found {name[1]}')
    errors.extend(markdown_errors(folder))
    return errors


def bridge_errors(root, folder):
    errors = []
    names = set()
    if folder.is_symlink():
        return ['Symlink Chain directory is not allowed']
    for p in sorted(folder.glob('*.md')):
        if p.name == 'README.md':
            continue
        if p.is_symlink():
            errors.append(f'Symlink bridge: {p}'); continue
        text = p.read_text()
        header = re.match(r'\A---\n(.*?)\n---(?:\n|$)', text, re.S)
        if not header:
            errors.append(f'Missing bridge header: {p}'); continue
        fields = {}
        for line in header[1].splitlines():
            key, sep, value = line.partition(':')
            if not sep or key.strip() in fields:
                errors.append(f'Malformed or duplicate bridge field: {p}')
            fields[key.strip()] = value.strip()
        name, location = fields.get('skill', ''), fields.get('skill_path', '')
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name) or p.stem != name:
            errors.append(f'Invalid bridge identity: {p}')
        if name in names: errors.append(f'Duplicate bridge: {name}')
        names.add(name)
        if fields.get('bridge_version') != '1':
            errors.append(f'Unsupported bridge_version: {p}')
        if location == 'UNCONFIGURED':
            errors.append(f'Unconfigured skill_path: {p}'); continue
        try:
            entry = local_file(root, location)
            if entry.name != 'SKILL.md':
                errors.append(f'Bridge must point to SKILL.md: {p}'); continue
            # Reject symlink aliases even if their resolved target remains in root.
            raw = root / location
            if any(part.is_symlink() for part in [raw, *raw.parents] if part.is_relative_to(root)):
                errors.append(f'Symlink skill path: {p}'); continue
            errors.extend(skill_errors(entry.parent, name))
        except ValueError as exc:
            errors.append(f'{p}: {exc}')
    return errors


def audit(root, check_evidence=True, require_approved=False, features=None, model='sdd', require_fresh=False):
    root = root.resolve()
    if not root.is_dir():
        raise ValueError(f'Missing project root: {root}')
    sdd = root / model
    if Path(model).is_absolute() or not sdd.resolve().is_relative_to(root):
        return ['Model path must stay inside the project root']
    for path in ('README.md', 'project.md', 'constitution.md', 'workflow.md', 'evidence.md',
                 'templates/spec.md', 'templates/plan.md', 'templates/tasks.md', 'templates/converge.md'):
        local_file(root, str(Path(model) / path))
    if sdd.is_symlink():
        return ['Symlink SDD directory is not allowed']
    errors = markdown_errors(sdd)
    errors.extend(bridge_errors(root, sdd / 'chain'))
    directory = root / (features or str(Path(model) / 'features'))
    if Path(features or str(Path(model) / 'features')).is_absolute() or not directory.resolve().is_relative_to(root):
        return errors + ['Feature path must stay inside the project root']
    if features and not directory.is_dir():
        return errors + ['Explicit feature directory is missing']
    errors.extend(feature_errors(root, check_evidence, require_approved, directory, require_fresh))
    return errors


def main():
    parser = argparse.ArgumentParser(description='Optional offline checks; no fixed skill catalog or library baseline.')
    parser.add_argument('--root', type=Path, default=Path.cwd())
    parser.add_argument('--model', default='sdd', help='Model directory relative to root (default: sdd)')
    parser.add_argument('--features', help='Directory of feature directories, relative to project root')
    parser.add_argument('--skill', type=Path, help='Check one standalone skill instead of a project')
    parser.add_argument('--require-fresh', action='store_true', help='Require schema 2 content bindings; not proof of execution')
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--structure-only', action='store_true')
    mode.add_argument('--require-approved', action='store_true')
    args = parser.parse_args()
    if args.structure_only and args.require_fresh:
        parser.error('--require-fresh cannot be combined with --structure-only')
    if args.skill and (args.features or args.require_approved or args.structure_only or args.require_fresh):
        parser.error('--skill cannot be combined with feature modes')
    try:
        errors = skill_errors(args.skill) if args.skill else audit(
            args.root, not args.structure_only, args.require_approved, args.features, args.model, args.require_fresh)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f'Could not audit: {exc}', file=sys.stderr); return 2
    for error in errors: print('FAIL:', error, file=sys.stderr)
    if errors: return 1
    print('PASS: portable files, configured bridges and requested evidence checks')
    print('Not proof of semantic adequacy, agent execution or comparative effectiveness.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
