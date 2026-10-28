"""Local distribution boundary and recursive archive inspection (stdlib only)."""
from pathlib import PurePosixPath
from io import BytesIO
import gzip
import hashlib
import json
import shutil
import stat
import tarfile
import zipfile

EXTERNAL_DOCUMENTS = frozenset({
    'Ox_Roadmap_Arquitetura_v0.2.md',
    'Ox_Comparativo_Skills_e_SDD_v1.0.md',
    'Ox_Regras_SDD_Skills_AGENTS_v1.0.md',
})
ROOT_FILES = ('AGENTS.md', 'README.md', 'LICENSE', 'NOTICE')
ROOT_DIRS = ('.codex/skills', 'sdd', 'tools/governance', 'config/governance', 'docs')
PACKAGE_NAME = 'ox-governance.zip'
MAX_EXPANDED = 128 * 1024 * 1024

# Historical paths are translated only for preservation comparisons. No aliases
# are installed in src/, and old observations retain their original identities.
RELOCATIONS = (
    ('src/fixtures/profile.json', 'config/governance/profile.json'),
    ('src/fixtures/normative-coverage.json', 'config/governance/normative-coverage.json'),
    ('src/fixtures/', 'tools/governance/tests/fixtures/'),
    ('src/scripts/', 'tools/governance/scripts/'),
    ('src/tests/', 'tools/governance/tests/'),
)


def relocated_path(relative):
    for previous, current in RELOCATIONS:
        if relative == previous or (previous.endswith('/') and relative.startswith(previous)):
            return current + relative[len(previous):]
    return relative


def relocated_traceability(data):
    """Change only the two file-reference fields, preserving the JSON formatting."""
    rows = json.loads(data)
    for row in rows:
        for key in ('implementation', 'oracle'):
            previous = row[key]
            current = relocated_path(previous)
            if current != previous:
                data = data.replace(json.dumps(previous).encode(), json.dumps(current).encode())
    return data


def governance_scope():
    """A fresh receipt shared by the ZIP and runner; never product acceptance."""
    return {
        'package_kind': 'governance',
        'product_included': False,
        'limitations': [
            'Validation covers governance/skills/SDD, not the Ox Rust application.',
            'Cargo workspace, binaries, installers and product integration tests are out of this package.',
        ],
    }


def scope_errors(receipt):
    """Fail closed when a governance receipt claims product coverage."""
    errors = []
    if receipt.get('package_kind') != 'governance':
        errors.append('Package kind must be governance')
    if receipt.get('product_included') is not False:
        errors.append('Governance package must exclude product')
    if not isinstance(receipt.get('limitations'), list) or not receipt['limitations']:
        errors.append('Governance scope limitations required')
    return errors


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def transient(path):
    return '__pycache__' in path.parts or path.as_posix().startswith('docs/validation/scratch/')


def product_record(path):
    """Product evidence depends on sources deliberately absent from governance exports."""
    return path.as_posix().startswith((
        'sdd/features/product-bootstrap/', 'docs/validation/product-bootstrap/',
    ))


def distribution_files(root):
    """Governance only: documents, skills, SDD, tooling and evidence, not Cargo/product."""
    paths = [root / name for name in ROOT_FILES]
    for name in ROOT_DIRS:
        paths.extend(p for p in (root / name).rglob('*')
                     if (p.is_file() or p.is_symlink()) and not transient(p.relative_to(root))
                     and not product_record(p.relative_to(root)))
    return sorted(set(paths))


def copy_distribution(root, destination):
    for source in distribution_files(root):
        if source.is_symlink() or not source.resolve().is_relative_to(root.resolve()):
            raise ValueError(f'Nonportable distribution path: {source}')
        target = destination / source.relative_to(root)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def inspect_bytes(name, data, fingerprints, *, budget=None, depth=0):
    """Inspect without extraction; reject links, traversal and full external texts.

    Line signatures normalize whitespace/newlines; not an obfuscation detector.
    Encrypted/unsupported archives and inspection limits fail closed.
    """
    budget = [MAX_EXPANDED] if budget is None else budget
    budget[0] -= len(data)
    if budget[0] < 0 or depth > 8:
        return [f'Archive inspection limit exceeded: {name}']
    errors = []
    if PurePosixPath(name.rsplit('::', 1)[-1].replace('\\', '/')).name in EXTERNAL_DOCUMENTS:
        errors.append(f'External document name: {name}')
    digest = hashlib.sha256(data).hexdigest()
    lines = [hashlib.sha256(line.strip()).hexdigest() for line in data.splitlines() if line.strip()]
    for original, record in fingerprints.items():
        expected = record['line_hashes']
        # Interior lines catch a wrapper attached to the first/last line as well.
        needle = expected[1:-1] if len(expected) > 4 else expected
        found = bool(needle) and any(lines[i:i+len(needle)] == needle
                                     for i, line in enumerate(lines) if line == needle[0])
        if digest == record['sha256'] or found:
            errors.append(f'External document content: {name}: {original}')

    def member_path(member):
        path = PurePosixPath(member.replace('\\', '/'))
        if path.is_absolute() or '..' in path.parts:
            errors.append(f'Unsafe archive path: {name}::{member}')
        return f'{name}::{member}'

    def visit(member, content):
        errors.extend(inspect_bytes(member_path(member), content, fingerprints,
                                    budget=budget, depth=depth+1))

    try:
        stream = BytesIO(data)
        if zipfile.is_zipfile(stream):
            with zipfile.ZipFile(stream) as archive:
                for item in archive.infolist():
                    member_path(item.filename)
                    if stat.S_ISLNK(item.external_attr >> 16):
                        errors.append(f'Archive symlink: {name}::{item.filename}')
                    if item.is_dir():
                        continue
                    if item.file_size > budget[0]:
                        errors.append(f'Archive inspection limit exceeded: {name}')
                        break
                    visit(item.filename, archive.read(item))
        elif data.startswith(b'\x1f\x8b'):
            stream.seek(0)
            with gzip.GzipFile(fileobj=stream) as compressed:
                expanded = compressed.read(min(MAX_EXPANDED, max(0, budget[0])) + 1)
            visit('<gzip>', expanded)
        elif len(data) > 262 and data[257:262] == b'ustar':
            stream.seek(0)
            with tarfile.open(fileobj=stream, mode='r:') as archive:
                for member in archive:
                    member_path(member.name)
                    if member.isdir():
                        continue
                    if not member.isfile():
                        errors.append(f'Archive nonregular member: {name}::{member.name}')
                        continue
                    if member.size > budget[0]:
                        errors.append(f'Archive inspection limit exceeded: {name}')
                        break
                    visit(member.name, archive.extractfile(member).read())
        elif name.lower().endswith(('.zip','.tar','.gz','.tgz','.bz2','.xz','.7z','.rar')):
            errors.append(f'Unrecognized or unsupported archive: {name}')
    except (OSError,ValueError,EOFError,RuntimeError,tarfile.TarError,zipfile.BadZipFile) as exc:
        errors.append(f'Cannot inspect archive: {name}: {exc}')
    return errors


def inspect_tree(root):
    fingerprints = json.loads((root/'docs/validation/governance-externalization/external-fingerprints.json').read_text())
    errors = []
    for path in sorted(root.rglob('*')):
        rel = path.relative_to(root)
        if transient(rel) or rel.parts[0] == 'dist':
            continue  # Package outputs are inspected directly; scratch is disposable.
        if path.is_symlink():
            errors.append(f'Symlink not portable: {rel}')
        elif path.is_file():
            errors.extend(inspect_bytes(rel.as_posix(), path.read_bytes(), fingerprints))
    return errors
