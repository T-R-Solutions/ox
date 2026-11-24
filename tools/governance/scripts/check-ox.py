#!/usr/bin/env python3
"""Verificação de governança do Ox (somente leitura, stdlib).

Verifica o que vale no SDD (sdd/constitution.md e sdd/workflow.md):
1. SDD: estrutura, tasks e specs pelo validador sdd/tools/validate.py.
2. Constituição: IDs POL/GOV/RQ únicos em sdd/constitution.md.
3. Skills (GOV-04): os diretórios .codex/skills/*/SKILL.md são exatamente as skills da
   tabela da seção "Skills" de sdd/workflow.md, e as excluídas não estão instaladas.
4. Links locais dos .md: arquivo e âncora existentes.
5. GOV-01: os estudos externos não estão na árvore, nem dentro de archives.

Saída 0: PASS. Saída 1: linhas "FAIL: ...". Saída 2: erro de leitura ou configuração.
Um exit 0 não aceita o produto.
"""
from __future__ import annotations

import importlib.util
import json
import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import unquote, urlsplit

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(Path(__file__).resolve().parent))
_support = importlib.import_module("governance_support")
FINGERPRINTS = _support.FINGERPRINTS
governance_files = _support.governance_files
inspect_bytes = _support.inspect_bytes

WORKFLOW = "sdd/workflow.md"
CONSTITUTION = "sdd/constitution.md"
RULE_ID_RE = re.compile(r"^- ((?:POL|GOV|RQ)-\d+):", re.M)
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
INSPECTED_PREFIXES = ("sdd/", "docs/", ".codex/", ".claude/", "tools/governance/", "scripts/")
INSPECTED_ROOT = ("AGENTS.md", "DESIGN.md", "README.md", "NOTICE", "LICENSE")


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def read_json(path: Path):
    def no_duplicates(pairs):
        keys = [k for k, _ in pairs]
        if len(keys) != len(set(keys)):
            raise ValueError(f"chave duplicada em {path}")
        return dict(pairs)
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=no_duplicates)


def sdd_errors(root: Path) -> list[str]:
    validator = load_module(root / "sdd/tools/validate.py", "ox_sdd_validate")
    errors = [f"SDD: {e}" for e in validator.structure_errors(root)]
    if errors:
        return errors
    pattern = validator.term_pattern(validator.forbidden_terms(root))
    for path in validator.T.find_tasks(root):
        rel = path.relative_to(root).as_posix()
        errors += [f"SDD: {rel}: {e}" for e in validator.task_errors(root, path, pattern)]
    for path in sorted((root / "sdd/specs").glob("*.md")):
        if path.name != "README.md":
            rel = path.relative_to(root).as_posix()
            errors += [f"SDD: {rel}: {e}" for e in validator.spec_errors(path)]
    return errors


def normative_errors(root: Path) -> list[str]:
    """Cada ID POL/GOV/RQ aparece uma única vez como regra da constituição."""
    ids = RULE_ID_RE.findall((root / CONSTITUTION).read_text(encoding="utf-8"))
    return [f"Duplicate local normative ID: {rid}" for rid in sorted({i for i in ids if ids.count(i) > 1})]


def skill_errors(root: Path) -> list[str]:
    """Inventário de .codex/skills igual à tabela da seção Skills do workflow (GOV-04)."""
    sys.path.insert(0, str(root / "sdd/tools"))
    import sddtask
    lines = sddtask.unfenced((root / WORKFLOW).read_text(encoding="utf-8").splitlines())
    section, inside = [], False
    for n, line in lines:
        if line.startswith("## "):
            inside = line.strip() == "## Skills"
        elif inside:
            section.append((n, line))
    mapped: list[str] = []
    excluded: set[str] = set()
    for table in sddtask.parse_tables(section):
        if table.header and table.header[0] == "Skill":
            mapped += [sddtask.strip_code(row["Skill"]) for row in table.rows]
    for _, line in section:
        if line.startswith("Fora do perfil:"):
            excluded |= set(re.findall(r"`([^`]+)`", line))
    errors = []
    if not mapped:
        return [f"Skill table missing in {WORKFLOW}#skills"]
    if len(mapped) != len(set(mapped)):
        errors.append(f"Duplicate skill in {WORKFLOW}#skills")
    skills = root / ".codex/skills"
    installed = {p.parent.name for p in skills.glob("*/SKILL.md")}
    for name in sorted(installed - set(mapped)):
        errors.append(f"Skill not mapped in {WORKFLOW}#skills: {name}")
    for name in sorted(set(mapped) - installed):
        errors.append(f"Mapped skill not installed: {name}")
    for name in sorted(excluded & {p.name for p in skills.iterdir() if p.is_dir()}):
        errors.append(f"Excluded skill installed: {name}")
    return errors


def slug(heading: str) -> str:
    text = re.sub(r"[`*_]|<[^>]+>", "", heading.strip()).lower()
    text = "".join(ch for ch in text if ch.isalnum() or ch in " -" or unicodedata.category(ch) == "Mn")
    return text.replace(" ", "-")


def anchors(path: Path, cache: dict) -> set[str]:
    if path not in cache:
        sys.path.insert(0, str(ROOT / "sdd/tools"))
        import sddtask
        seen: dict[str, int] = {}
        out = set()
        for _, line in sddtask.unfenced(path.read_text(encoding="utf-8").splitlines()):
            m = re.match(r"^#{1,6}\s+(.+?)\s*#*\s*$", line)
            if not m:
                continue
            base = slug(m.group(1))
            n = seen.get(base, 0)
            out.add(base if n == 0 else f"{base}-{n}")
            seen[base] = n + 1
        cache[path] = out
    return cache[path]


def link_errors(root: Path, files: list[str]) -> list[str]:
    sys.path.insert(0, str(root / "sdd/tools"))
    import sddtask
    errors, cache = [], {}
    root_resolved = root.resolve()
    for rel in files:
        if not rel.endswith(".md"):
            continue
        path = root / rel
        if path.is_symlink():
            continue
        for _, line in sddtask.unfenced(path.read_text(encoding="utf-8").splitlines()):
            for target in LINK_RE.findall(re.sub(r"`[^`]*`", "", line)):
                parsed = urlsplit(target.strip("<>"))
                if parsed.scheme or parsed.netloc:
                    continue
                dest = path if not parsed.path else (path.parent / unquote(parsed.path))
                resolved = dest.resolve()
                if not resolved.is_relative_to(root_resolved) or not resolved.exists():
                    errors.append(f"Broken/escaping link: {rel}: {target}")
                    continue
                if parsed.fragment and resolved.is_file() and resolved.suffix == ".md":
                    if unquote(parsed.fragment).lower() not in anchors(resolved, cache):
                        errors.append(f"Broken/escaping link: {rel}: {target}")
    return errors


def external_errors(root: Path, files: list[str]) -> list[str]:
    fingerprints = read_json(root / FINGERPRINTS)
    errors = []
    for rel in files:
        if not (rel.startswith(INSPECTED_PREFIXES) or rel in INSPECTED_ROOT):
            continue
        path = root / rel
        if path.is_symlink():
            continue
        errors += inspect_bytes(rel, path.read_bytes(), fingerprints)
    return errors


def check(root: Path) -> list[str]:
    files = governance_files(root)
    return (sdd_errors(root) + normative_errors(root) + skill_errors(root)
            + link_errors(root, files) + external_errors(root, files))


def main(argv: list[str]) -> int:
    root = ROOT
    if "--root" in argv:
        root = Path(argv[argv.index("--root") + 1]).resolve()
    try:
        errors = check(root)
    except (OSError, ValueError, KeyError, TypeError, UnicodeDecodeError) as exc:
        print("FAIL:", exc)
        return 2
    for error in errors:
        print("FAIL:", error)
    if not errors:
        print("PASS: SDD, normative IDs, skill map, local links and external-content inspection. "
              "No product acceptance.")
    return int(bool(errors))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
