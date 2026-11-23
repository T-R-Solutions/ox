#!/usr/bin/env python3
"""Inventário somente-leitura da task do Codex descrita em .ai/.

Lê .ai/task_planning.md (plano + critérios de finalização) e .ai/task_completed.md
(relato do que foi feito), extrai critérios e caminhos citados e cruza com o
trabalho não commitado (git status). Também confere se task_finalizada.md foi
alterado só por acréscimo. Não escreve nada; imprime JSON ou Markdown.

Saída 0: inventário gerado. Saída 2: repositório inválido ou arquivo .ai ausente/vazio.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

TASK_LOG = "task_finalizada.md"
PLANNING = "task_planning.md"
COMPLETED = "task_completed.md"
# Caminhos que não são trabalho do Codex a auditar: handoff .ai e ferramentas do auditor.
EXCLUDED_PREFIXES = (".claude/",)
HEADING_RE = re.compile(r"^(?P<hashes>#{1,6})\s+(?P<title>.+?)\s*#*\s*$")
CRITERIA_HEADING_RE = re.compile(
    r"crit[ée]rio|aceite|aceita[çc][ãa]o|acceptance|finaliza|conclus[ãa]o|done|definition of done|dod",
    re.I,
)
ITEM_RE = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+(?:\[(?P<mark>[ xX])\]\s+)?(?P<text>\S.*)$")
BACKTICK_RE = re.compile(r"`([^`\n]+)`")
LINK_RE = re.compile(r"\]\(([^)\s]+)\)")
PATHLIKE_RE = re.compile(r"^[A-Za-z0-9_.\-][A-Za-z0-9_.\-/]*$")
LINE_SUFFIX_RE = re.compile(r":\d+(?:[-:]\d+)?$")


class InventoryError(RuntimeError):
    pass


def git(root: Path, *args: str, check: bool = True) -> bytes:
    proc = subprocess.run(["git", "-C", str(root), *args], capture_output=True, check=False)
    if check and proc.returncode != 0:
        raise InventoryError(f"git {' '.join(args)} falhou: {proc.stderr.decode(errors='replace').strip()}")
    return proc.stdout


def blob(root: Path, spec: str) -> bytes | None:
    proc = subprocess.run(["git", "-C", str(root), "show", spec], capture_output=True, check=False)
    return proc.stdout if proc.returncode == 0 else None


def changed_paths(root: Path) -> list[dict]:
    raw = git(root, "status", "--porcelain=v1", "-z", "--untracked-files=all")
    entries = raw.split(b"\0")
    out: list[dict] = []
    i = 0
    while i < len(entries):
        item = entries[i]
        i += 1
        if not item:
            continue
        status = item[:2].decode()
        path = item[3:].decode(errors="surrogateescape")
        orig = None
        if status[0] in "RC":
            orig = entries[i].decode(errors="surrogateescape")
            i += 1
        out.append({"status": status, "path": path, "orig": orig})
    return out


def read_ai(ai_dir: Path, name: str) -> tuple[str, str]:
    path = ai_dir / name
    if not path.is_file():
        raise InventoryError(f"{path} ausente: o Codex precisa criá-lo antes da análise")
    data = path.read_bytes()
    text = data.decode(errors="replace")
    if not text.strip():
        raise InventoryError(f"{path} vazio: nada a analisar")
    return text, hashlib.sha256(data).hexdigest()


def title_of(text: str) -> str | None:
    for line in text.splitlines():
        if m := HEADING_RE.match(line):
            return m.group("title")
    return None


def criteria(text: str) -> list[dict]:
    """Itens de lista sob títulos de critério/aceite/finalização (inclui subtítulos)."""
    out: list[dict] = []
    active_level: int | None = None
    section = ""
    in_fence = False
    for n, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith(("```", "~~~")):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if m := HEADING_RE.match(line):
            level = len(m.group("hashes"))
            if active_level is not None and level <= active_level:
                active_level = None
            if active_level is None and CRITERIA_HEADING_RE.search(m.group("title")):
                active_level = level
                section = m.group("title")
            continue
        if active_level is None:
            continue
        if m := ITEM_RE.match(line):
            mark = m.group("mark")
            out.append({
                "line": n,
                "section": section,
                "text": m.group("text").strip(),
                "checked": None if mark is None else mark.lower() == "x",
            })
    return out


def cited_paths(text: str) -> list[str]:
    found: set[str] = set()
    for raw in BACKTICK_RE.findall(text) + LINK_RE.findall(text):
        cand = raw.strip().split("#", 1)[0]
        cand = LINE_SUFFIX_RE.sub("", cand)
        cand = cand.removeprefix("./")
        if "://" in raw or not cand or not PATHLIKE_RE.match(cand):
            continue
        # Exige forma de caminho: barra ou extensão; ignora versões/números ("1.2", "0.13").
        if "/" not in cand and not re.search(r"\.[A-Za-z][A-Za-z0-9]*$", cand):
            continue
        found.add(cand)
    return sorted(found)


def matches(cited: str, path: str) -> bool:
    c = cited.rstrip("/")
    return path == c or path.startswith(c + "/") or path.endswith("/" + c)


def task_log(root: Path) -> dict:
    path = root / TASK_LOG
    if not path.exists():
        return {"present": False}
    data = path.read_bytes()
    checks = {}
    for label, spec in (("HEAD", f"HEAD:{TASK_LOG}"), ("index", f":{TASK_LOG}")):
        prev = blob(root, spec)
        if prev is None:
            checks[label] = "ausente"
        elif data == prev:
            checks[label] = "sem alteração"
        else:
            checks[label] = "prefixo preservado" if data.startswith(prev) else "VIOLAÇÃO: bytes anteriores alterados"
    return {"present": True, "bytes": len(data), "append_only": checks}


def build(root: Path, ai_rel: str) -> dict:
    if not (root / ".git").exists():
        git(root, "rev-parse", "--git-dir")  # gera erro claro fora de um repositório
    ai_dir = root / ai_rel
    planning, planning_sha = read_ai(ai_dir, PLANNING)
    completed, completed_sha = read_ai(ai_dir, COMPLETED)

    ai_prefix = ai_rel.strip("/") + "/"
    all_changes = changed_paths(root)
    changes = [c for c in all_changes
               if not c["path"].startswith(ai_prefix) and not c["path"].startswith(EXCLUDED_PREFIXES)]
    work = [c for c in changes if c["path"] != TASK_LOG]

    planned = cited_paths(planning)
    reported = cited_paths(completed)

    def changed_for(cited: str) -> list[str]:
        return [c["path"] for c in work if matches(cited, c["path"])]

    cited_without_change = [
        {"path": p, "exists": (root / p).exists()} for p in reported if not changed_for(p)
    ]
    changed_uncited = [c for c in work if not any(matches(p, c["path"]) for p in reported)]
    planned_not_reported = [p for p in planned if not any(matches(p, r) or matches(r, p) for r in reported)]
    crit = criteria(planning)

    head = git(root, "log", "-1", "--format=%H%x00%ci%x00%s", check=False).decode().split("\0")
    branch = git(root, "rev-parse", "--abbrev-ref", "HEAD", check=False).decode().strip()
    warnings = []
    if not crit:
        warnings.append(f"nenhum critério de finalização reconhecido em {PLANNING}: "
                        "leia o arquivo e extraia-os manualmente; ausência real é achado")
    return {
        "root": str(root),
        "branch": branch or None,
        "base_commit": {"sha": head[0], "date": head[1], "subject": head[2].strip()} if len(head) == 3 else None,
        "ai": {
            "planning": {"path": f"{ai_prefix}{PLANNING}", "sha256": planning_sha, "title": title_of(planning)},
            "completed": {"path": f"{ai_prefix}{COMPLETED}", "sha256": completed_sha, "title": title_of(completed)},
            "analyzed_exists": (ai_dir / "task_analyzed.md").is_file(),
        },
        "criteria": crit,
        "changed_total": len(work),
        "changes": work,
        "planned_paths": planned,
        "reported_paths": reported,
        "cited_without_change": cited_without_change,
        "changed_uncited": changed_uncited,
        "planned_not_reported": planned_not_reported,
        "task_log": task_log(root) | {"changed": any(c["path"] == TASK_LOG for c in changes)},
        "warnings": warnings,
    }


def to_markdown(inv: dict) -> str:
    base = inv["base_commit"] or {"sha": "(sem commit)", "date": "-"}
    ai = inv["ai"]
    lines = [
        f"# Inventário da task — {ai['planning']['title'] or '(sem título)'}",
        "",
        f"Base {base['sha'][:7]} ({base['date']}), branch {inv['branch']}.",
        f"- `{ai['planning']['path']}` sha256 {ai['planning']['sha256']}",
        f"- `{ai['completed']['path']}` sha256 {ai['completed']['sha256']}",
        f"- task_analyzed.md existente: {'sim (nova rodada)' if ai['analyzed_exists'] else 'não (rodada 1)'}",
        "",
    ]
    lines += [f"> AVISO: {w}" for w in inv["warnings"]]
    lines += ["", f"## Critérios de finalização ({len(inv['criteria'])})", ""]
    for c in inv["criteria"]:
        mark = {True: "[x]", False: "[ ]", None: "-"}[c["checked"]]
        lines.append(f"- L{c['line']} {mark} {c['text']}  _(seção: {c['section']})_")
    lines += ["", f"## Arquivos alterados (não commitados, fora de .ai/): {inv['changed_total']}", ""]
    lines += [f"- `{c['status']}` {c['path']}" for c in inv["changes"]] or ["- (nenhum)"]
    lines += ["", f"## Alterados sem citação em task_completed.md: {len(inv['changed_uncited'])}", ""]
    lines += [f"- `{c['status']}` {c['path']}" for c in inv["changed_uncited"]] or ["- (nenhum)"]
    lines += ["", f"## Citados em task_completed.md sem mudança no diff: {len(inv['cited_without_change'])}", ""]
    lines += [f"- {c['path']}{'' if c['exists'] else ' — NÃO EXISTE'}" for c in inv["cited_without_change"]] or ["- (nenhum)"]
    lines += ["", f"## Planejados e não relatados: {len(inv['planned_not_reported'])}", ""]
    lines += [f"- {p}" for p in inv["planned_not_reported"]] or ["- (nenhum)"]
    log = inv["task_log"]
    lines += ["", f"## {TASK_LOG}", ""]
    if log.get("present"):
        lines.append(f"- alterado nesta task: {'sim' if log['changed'] else 'não'}; append-only: {log['append_only']}")
    else:
        lines.append("- ausente")
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=".", type=Path)
    ap.add_argument("--ai-dir", default=".ai", help="diretório do handoff, relativo à raiz")
    ap.add_argument("--format", choices=("json", "md"), default="json")
    args = ap.parse_args()
    root = args.root.resolve()
    try:
        inv = build(root, args.ai_dir)
    except InventoryError as exc:
        print(exc, file=sys.stderr)
        return 2
    if args.format == "json":
        json.dump(inv, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        sys.stdout.write(to_markdown(inv))
    return 0


if __name__ == "__main__":
    sys.exit(main())
