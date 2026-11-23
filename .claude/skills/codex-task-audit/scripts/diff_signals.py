#!/usr/bin/env python3
"""Sinais de dívida técnica nas linhas adicionadas do trabalho não commitado.

Somente leitura. Linhas adicionadas = `git diff HEAD` (+) mais o conteúdo inteiro de
arquivos não rastreados. Um sinal é um ponto a inspecionar, não um defeito confirmado.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

CODE_EXT = {".rs", ".py", ".sh", ".toml", ".json", ".js", ".ts"}
SOURCE_EXT = {".rs", ".py", ".sh"}
EVIDENCE_HINT = ("docs/validation/", "/evidence.json", "/fixtures/")

SIGNALS: list[tuple[str, str, re.Pattern, set[str] | None]] = [
    ("todo", "M06", re.compile(r"\b(TODO|FIXME|XXX|HACK)\b"), None),
    ("deprecated", "M06", re.compile(r"deprecat|#\[deprecated|DeprecationWarning|\blegacy\b|\bobsolete\b", re.I), SOURCE_EXT),
    ("dead-code-allow", "M06", re.compile(r"#!?\[allow\((dead_code|unused[^)]*)\)\]"), {".rs"}),
    ("lint-allow", "M14", re.compile(r"#!?\[allow\(clippy::[^)]*\)\]"), {".rs"}),
    ("ignored-test", "M04", re.compile(r"#\[ignore|@unittest\.skip|\.skipTest\(|pytest\.mark\.skip"), {".rs", ".py"}),
    ("unwrap-expect", "M10", re.compile(r"\.unwrap\(\)|\.expect\("), {".rs"}),
    ("panic", "M10", re.compile(r"\b(panic!|unreachable!|todo!|unimplemented!)\("), {".rs"}),
    ("unsafe", "M11", re.compile(r"\bunsafe\s*[{(fn]"), {".rs"}),
    ("scanner-suppression", "M11", re.compile(r"#\s*nosec|#\s*noqa|shellcheck disable|nolint|gitleaks:allow"), None),
    ("shell-true", "M11", re.compile(r"shell\s*=\s*True"), {".py"}),
    ("swallowed-error", "M10", re.compile(r"\|\|\s*true\b|except\s*(Exception)?\s*:\s*(pass)?\s*$|2>/dev/null"), {".sh", ".py"}),
    ("dead-handler", "M06", re.compile(r"^\s*(local\s+)?\w+=\$\{?\w+\}?\s*\|\|"), {".sh"}),
    ("magic-sleep", "M04", re.compile(r"\bsleep\s*\(?\s*\d|thread::sleep|time\.sleep"), {".rs", ".py", ".sh"}),
]

ARTIFACT_RE = re.compile(r"(__pycache__/|\.pyc$|\.pyo$|\.DS_Store$|\.orig$|\.rej$)")


def git(root: Path, *args: str) -> str:
    proc = subprocess.run(["git", "-C", str(root), *args], capture_output=True, check=False)
    if proc.returncode not in (0, 1):
        raise RuntimeError(proc.stderr.decode(errors="replace"))
    return proc.stdout.decode(errors="replace")


def is_test_path(path: str) -> bool:
    return "/tests/" in path or path.startswith("tests/") or "/test_" in path or path.endswith("_test.rs") \
        or "#[cfg(test)]" in path


def added_lines(root: Path, paths: list[str]) -> dict[str, list[tuple[int, str]]]:
    out: dict[str, list[tuple[int, str]]] = {}
    diff = git(root, "diff", "HEAD", "--unified=0", "--no-color", "--", *paths)
    current = None
    lineno = 0
    for line in diff.splitlines():
        if line.startswith("+++ "):
            current = line[6:] if line.startswith("+++ b/") else None
            continue
        if line.startswith("@@"):
            m = re.search(r"\+(\d+)", line)
            lineno = int(m.group(1)) if m else 0
            continue
        if current and line.startswith("+"):
            out.setdefault(current, []).append((lineno, line[1:]))
            lineno += 1
    untracked = git(root, "ls-files", "--others", "--exclude-standard", "--", *paths).splitlines()
    for rel in untracked:
        p = root / rel
        if not p.is_file() or p.suffix not in CODE_EXT | {".md", ".txt", ".yml", ".yaml"}:
            out.setdefault(rel, [])
            continue
        try:
            text = p.read_text(errors="replace")
        except OSError:
            continue
        out[rel] = list(enumerate(text.splitlines(), start=1))
    return out


def rust_test_region(root: Path, rel: str) -> int | None:
    """Linha onde começa `#[cfg(test)]` (regiões de teste inline em Rust)."""
    p = root / rel
    if p.suffix != ".rs" or not p.is_file():
        return None
    for n, line in enumerate(p.read_text(errors="replace").splitlines(), start=1):
        if line.strip().startswith("#[cfg(test)]"):
            return n
    return None


def new_functions(lines: list[tuple[int, str]], suffix: str) -> list[str]:
    pat = {".rs": r"^\s*(pub(\([^)]*\))?\s+)?(async\s+)?fn\s+(\w+)",
           ".py": r"^\s*def\s+(\w+)",
           ".sh": r"^\s*(function\s+)?(\w+)\s*\(\)\s*\{"}.get(suffix)
    if not pat:
        return []
    names = []
    for _, text in lines:
        m = re.match(pat, text)
        if m:
            names.append(m.groups()[-1])
    return [n for n in names if not n.startswith("test") and n not in {"main", "new", "default", "fmt"}]


def build(root: Path, paths: list[str], include_evidence: bool, large: int) -> dict:
    added = added_lines(root, paths)
    findings: list[dict] = []
    summary: dict[str, int] = {}
    artifacts, large_files, untested = [], [], []
    test_corpus = None

    for rel, lines in sorted(added.items()):
        if rel.startswith(".claude/"):
            continue  # ferramentas do próprio auditor
        if ARTIFACT_RE.search(rel):
            artifacts.append(rel)
            continue
        if not include_evidence and any(h in rel for h in EVIDENCE_HINT):
            continue
        suffix = Path(rel).suffix
        p = root / rel
        if p.is_file() and suffix in SOURCE_EXT:
            try:
                total = sum(1 for _ in p.open(errors="replace"))
            except OSError:
                total = 0
            if total >= large:
                large_files.append({"path": rel, "lines": total, "added": len(lines)})
        test_start = rust_test_region(root, rel)
        testy = is_test_path(rel)
        for lineno, text in lines:
            in_test = testy or (test_start is not None and lineno >= test_start)
            for name, metric, pat, exts in SIGNALS:
                if exts is not None and suffix not in exts:
                    continue
                if name == "unwrap-expect" and in_test:
                    continue
                if pat.search(text):
                    findings.append({"signal": name, "metric": metric, "path": rel, "line": lineno,
                                     "in_test": in_test, "text": text.strip()[:160]})
                    summary[name] = summary.get(name, 0) + 1
        if suffix in SOURCE_EXT and not testy:
            fns = new_functions(lines, suffix)
            if fns:
                if test_corpus is None:
                    test_corpus = _test_corpus(root)
                for fn in fns:
                    if not re.search(rf"\b{re.escape(fn)}\b", test_corpus):
                        untested.append({"path": rel, "function": fn})

    return {"files_with_added_lines": len(added), "summary": summary, "findings": findings,
            "artifacts_in_diff": artifacts, "large_source_files": large_files,
            "new_functions_not_named_in_tests": untested}


def _test_corpus(root: Path) -> str:
    chunks = []
    for pattern in ("**/tests/**/*.py", "**/tests/**/*.rs", "**/tests/*.py", "**/tests/*.rs"):
        for p in root.glob(pattern):
            if "target" in p.parts or ".cache" in p.parts:
                continue
            try:
                chunks.append(p.read_text(errors="replace"))
            except OSError:
                pass
    for p in root.glob("application/**/src/**/*.rs"):
        if "target" in p.parts:
            continue
        text = p.read_text(errors="replace")
        idx = text.find("#[cfg(test)]")
        if idx >= 0:
            chunks.append(text[idx:])
    return "\n".join(chunks)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=".", type=Path)
    ap.add_argument("--paths", nargs="*", default=[], help="limita a estes caminhos/pastas")
    ap.add_argument("--include-evidence", action="store_true", help="inclui docs/validation e evidence.json")
    ap.add_argument("--large", type=int, default=800, help="limiar de linhas para arquivo grande")
    ap.add_argument("--summary", action="store_true", help="imprime só contagens")
    args = ap.parse_args()
    try:
        res = build(args.root.resolve(), args.paths, args.include_evidence, args.large)
    except RuntimeError as exc:
        print(exc, file=sys.stderr)
        return 2
    if args.summary:
        res = {k: v for k, v in res.items() if k != "findings"}
    json.dump(res, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
