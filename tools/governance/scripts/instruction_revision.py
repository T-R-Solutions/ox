"""Authenticate only the adopted 2026-11-14 instruction-governance transition."""
import hashlib
import json

REGISTRY = 'docs/validation/governance-corrections-20261114/succession.json'
REVIEWED = '0f5733af045a50631d5a04d897bc526510a14b8c7742bebc02fd1ae5febf0fdd'
DECISION = 'docs/decisions/governance-instruction-reconciliation.md'


def records(root):
    from readme_revision import file, unique
    registry = root / REGISTRY
    if not registry.exists() and not registry.is_symlink():
        if (root / DECISION).exists():
            raise ValueError('Missing instruction succession registry')
        return []
    data = file(root, REGISTRY).read_bytes()
    if hashlib.sha256(data).hexdigest() != REVIEWED:
        raise ValueError('Instruction succession registry changed')
    doc = json.loads(data, object_pairs_hook=unique)
    if hashlib.sha256(file(root, DECISION).read_bytes()).hexdigest() != doc['decision_sha256']:
        raise ValueError('Instruction succession decision changed')
    names = [row['destination'] for row in doc['records']]
    if len(names) != len(set(names)):
        raise ValueError('Duplicate instruction succession destination')
    return doc['records']


def predecessor(root, relative, data):
    from document_ledger import succession_predecessor
    from log_repair_revision import predecessor as log_predecessor
    from readme_revision import file
    from visual_skill_revision import predecessor as visual_skill_predecessor
    rows = records(root)  # Authenticate the immutable historical registry first.
    data = succession_predecessor(root, relative, data)
    data = visual_skill_predecessor(root, relative, data)
    data = log_predecessor(root, relative, data)
    for row in rows:
        if row['destination'] != relative:
            continue
        previous = file(root, row['previous']).read_bytes()
        if hashlib.sha256(previous).hexdigest() != row['previous_sha256']:
            raise ValueError('Instruction predecessor changed')
        active = file(root, relative).read_bytes()
        if active == data and hashlib.sha256(data).hexdigest() == row['previous_sha256']:
            raise ValueError('Instruction predecessor downgrade: ' + relative)
        if hashlib.sha256(data).hexdigest() == row['sha256']:
            return previous
    return data


def errors(root):
    from pathlib import Path

    from document_ledger import succession_predecessor
    from governance_support import product_record
    from readme_revision import file
    result = []
    try:
        rows = records(root)
        if not rows:
            return []
        copy_mode = governance_copy(root)
        for row in rows:
            name = row['destination']
            if copy_mode and product_record(Path(name)):
                current = root / name
                if current.exists() or current.is_symlink():
                    result.append('Excluded product record present in governance copy: ' + name)
                previous = file(root, row['previous']).read_bytes()
                if hashlib.sha256(previous).hexdigest() != row['previous_sha256']:
                    result.append('Instruction predecessor changed: ' + name)
                continue
            current = file(root, name).read_bytes()
            from log_repair_revision import original_branch
            from log_repair_revision import predecessor as log_predecessor
            from visual_skill_revision import predecessor as visual_skill_predecessor
            normalized = succession_predecessor(root, name, current)
            normalized = visual_skill_predecessor(root, name, normalized)
            normalized = log_predecessor(root, name, normalized)
            expected = row['previous_sha256'] if original_branch(root, name, current) else row['sha256']
            if hashlib.sha256(normalized).hexdigest() != expected:
                result.append('Instruction current changed: ' + name)
            predecessor(root, name, current)
        result.extend(agent_errors(root, copy_mode))
    except (ValueError, OSError) as exc:
        result.append(str(exc))
    return result

# An explicit consumer receipt, never inferred from absent local sources.
COPY_CONTEXT = '.ox-governance-copy.json'
COPY_CONTEXT_BYTES = b'{"schema_version":1,"consumer":"ox-governance-copy","contract":"governance-instruction-reconciliation-20261114","agent_configuration":"observed-snapshots-only","product":"excluded-by-product_record"}\n'
AGENT_SNAPSHOT = 'docs/validation/governance-corrections-20261114/agent-snapshot.json'


def write_copy_context(destination):
    path = destination / COPY_CONTEXT
    if path.exists() or path.is_symlink():
        raise ValueError('Governance copy context already exists')
    path.write_bytes(COPY_CONTEXT_BYTES)


def governance_copy(root):
    from readme_revision import file
    path = root / COPY_CONTEXT
    if not path.exists() and not path.is_symlink():
        return False
    if file(root, COPY_CONTEXT).read_bytes() != COPY_CONTEXT_BYTES:
        raise ValueError('Governance copy context changed')
    for local in ('.git', 'application', '.codex/config.toml', '.codex/agents'):
        p = root / local
        if p.exists() or p.is_symlink():
            raise ValueError('Governance copy context conflicts with local checkout: ' + local)
    return True


def agent_snapshots(root):
    from readme_revision import file, unique
    # Registry bytes are pinned by records(); its manifest identity is immutable.
    records(root)
    document = json.loads(file(root, REGISTRY).read_text(), object_pairs_hook=unique)
    content = file(root, AGENT_SNAPSHOT).read_bytes()
    if hashlib.sha256(content).hexdigest() != document['agent_snapshot_sha256']:
        raise ValueError('Agent snapshot manifest changed')
    rows = json.loads(content, object_pairs_hook=unique)['records']
    for row in rows:
        if hashlib.sha256(file(root, row['snapshot']).read_bytes()).hexdigest() != row['sha256']:
            raise ValueError('Agent snapshot changed: ' + row['source'])
    return rows


def agent_errors(root, copy_mode):
    from readme_revision import file
    rows = agent_snapshots(root)
    if copy_mode:
        return []  # Only retained observed snapshots, explicitly not installation.
    errors = []
    expected = {row['source'] for row in rows if row['source'].startswith('.codex/agents/')}
    actual = {str(path.relative_to(root)) for path in (root / '.codex/agents').glob('*.toml')}
    if actual != expected:
        errors.append('Live agent profile inventory differs from observed snapshot')
    for row in rows:
        try:
            if hashlib.sha256(file(root, row['source']).read_bytes()).hexdigest() != row['sha256']:
                errors.append('Live agent configuration changed: ' + row['source'])
        except (ValueError, OSError) as exc:
            errors.append('Live agent configuration unavailable: ' + row['source'] + ': ' + str(exc))
    return errors


def excluded_local_reference(root, source, target):
    """One immutable historical audit link, interpreted only in explicit copies."""
    from readme_revision import file
    if not governance_copy(root) or source != 'docs/validation/governance-audit-20261114/report.md':
        return False
    if hashlib.sha256(file(root, source).read_bytes()).hexdigest() != 'd4cf3458bca8c51bab2101d392d25d7776f75d52b09c94e642c53b8a7fcddb0e':
        return False
    if not target.is_relative_to(root) or target.relative_to(root).as_posix() != '.codex/agents/ec_triador.toml':
        return False
    return any(row['source'] == '.codex/agents/ec_triador.toml' for row in agent_snapshots(root))
