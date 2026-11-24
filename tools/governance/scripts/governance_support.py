"""Funções compartilhadas da governança do Ox (stdlib apenas, somente leitura).

Usado por check-ox.py e por scripts/tests. Contém:
- `transient`: caminhos descartáveis (logs, caches, bytecode);
- `governance_files`: arquivos versionáveis da árvore (Git sem locks opcionais);
- `inspect_bytes`: inspeção de conteúdo e de arquivos compactados para a GOV-01
  (os três estudos externos não podem estar na árvore, nem dentro de archives).
"""
from __future__ import annotations

import gzip
import hashlib
import os
import stat
import subprocess
import tarfile
import zipfile
from io import BytesIO
from pathlib import Path, PurePosixPath

EXTERNAL_DOCUMENTS = frozenset(
    {
        "Ox_Roadmap_Arquitetura_v0.2.md",
        "Ox_Comparativo_Skills_e_SDD_v1.0.md",
        "Ox_Regras_SDD_Skills_AGENTS_v1.0.md",
    }
)
FINGERPRINTS = "tools/governance/config/external-fingerprints.json"
MAX_EXPANDED = 128 * 1024 * 1024
GIT_ENV = dict(os.environ, GIT_OPTIONAL_LOCKS="0")


def transient(path):
    return (
        ".git" in path.parts
        or "__pycache__" in path.parts
        or bool(path.parts and path.parts[0] in {".local", ".cache", ".inputs"})
    )


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def governance_files(root: Path) -> list[str]:
    """Arquivos rastreados ou novos não ignorados, relativos à raiz, sem transitórios.

    Fora de um repositório Git, percorre a árvore (uso em cópias de teste).
    """
    proc = subprocess.run(
        ["git", "--no-optional-locks", "-C", str(root), "ls-files", "-co", "--exclude-standard", "-z"],
        capture_output=True, check=False, env=GIT_ENV,
    )
    if proc.returncode == 0:
        names = [n.decode(errors="surrogateescape") for n in proc.stdout.split(b"\0") if n]
    else:
        names = [p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file() or p.is_symlink()]
    out = []
    for name in sorted(set(names)):
        rel = Path(name)
        path = root / rel
        if transient(rel) or not (path.is_file() or path.is_symlink()):
            continue
        out.append(rel.as_posix())
    return out


def inspect_bytes(name, data, fingerprints, *, budget=None, depth=0):
    """Inspect without extraction; reject links, traversal and full external texts.

    Line signatures normalize whitespace/newlines; not an obfuscation detector.
    Encrypted/unsupported archives and inspection limits fail closed.
    """
    budget = [MAX_EXPANDED] if budget is None else budget
    budget[0] -= len(data)
    if budget[0] < 0 or depth > 8:
        return [f"Archive inspection limit exceeded: {name}"]
    errors = []
    if PurePosixPath(name.rsplit("::", 1)[-1].replace("\\", "/")).name in EXTERNAL_DOCUMENTS:
        errors.append(f"External document name: {name}")
    data_digest = hashlib.sha256(data).hexdigest()
    lines = [hashlib.sha256(line.strip()).hexdigest() for line in data.splitlines() if line.strip()]
    for original, record in fingerprints.items():
        expected = record["line_hashes"]
        # Interior lines catch a wrapper attached to the first/last line as well.
        needle = expected[1:-1] if len(expected) > 4 else expected
        found = bool(needle) and any(
            lines[i: i + len(needle)] == needle for i, line in enumerate(lines) if line == needle[0]
        )
        if data_digest == record["sha256"] or found:
            errors.append(f"External document content: {name}: {original}")

    def member_path(member):
        path = PurePosixPath(member.replace("\\", "/"))
        if ".git" in path.parts:
            errors.append(f"Git metadata in archive: {name}::{member}")
        if path.is_absolute() or ".." in path.parts:
            errors.append(f"Unsafe archive path: {name}::{member}")
        return f"{name}::{member}"

    def visit(member, content):
        errors.extend(inspect_bytes(member_path(member), content, fingerprints, budget=budget, depth=depth + 1))

    try:
        stream = BytesIO(data)
        if zipfile.is_zipfile(stream):
            with zipfile.ZipFile(stream) as archive:
                for item in archive.infolist():
                    member_path(item.filename)
                    if stat.S_ISLNK(item.external_attr >> 16):
                        errors.append(f"Archive symlink: {name}::{item.filename}")
                    if item.is_dir():
                        continue
                    if item.file_size > budget[0]:
                        errors.append(f"Archive inspection limit exceeded: {name}")
                        break
                    visit(item.filename, archive.read(item))
        elif data.startswith(b"\x1f\x8b"):
            stream.seek(0)
            with gzip.GzipFile(fileobj=stream) as compressed:
                expanded = compressed.read(min(MAX_EXPANDED, max(0, budget[0])) + 1)
            visit("<gzip>", expanded)
        elif len(data) > 262 and data[257:262] == b"ustar":
            stream.seek(0)
            with tarfile.open(fileobj=stream, mode="r:") as archive:
                for member in archive:
                    member_path(member.name)
                    if member.isdir():
                        continue
                    if not member.isfile():
                        errors.append(f"Archive nonregular member: {name}::{member.name}")
                        continue
                    if member.size > budget[0]:
                        errors.append(f"Archive inspection limit exceeded: {name}")
                        break
                    visit(member.name, archive.extractfile(member).read())
        elif name.lower().endswith((".zip", ".tar", ".gz", ".tgz", ".bz2", ".xz", ".7z", ".rar")):
            errors.append(f"Unrecognized or unsupported archive: {name}")
    except (OSError, ValueError, EOFError, RuntimeError, tarfile.TarError, zipfile.BadZipFile) as exc:
        errors.append(f"Cannot inspect archive: {name}: {exc}")
    return errors
