#!/usr/bin/env python3
"""Inventário somente-leitura de uma task do Ox (sdd/tasks/<ID>.md) para revisão.

Lê o registro com o parser único sdd/tools/sddtask.py, recalcula os SHA-256 da
seção 8 sobre os bytes atuais e cruza a seção 7 com o trabalho não commitado.
Também confere o parecer existente (<ID>.review.md). Não escreve nada; imprime JSON
ou Markdown.

Somente leitura também no Git: todas as chamadas usam `--no-optional-locks`, para
que `git status` não regrave `.git/index`. O parser é carregado do checkout que
contém esta skill, nunca do `--root` auditado (o código auditado não é executado).

Saída 0: inventário gerado. Saída 2: fora de repositório Git, parser da skill
ausente, registro inexistente ou sem cabeçalho `# <ID> — <título>`.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TRUSTED_PARSER = HERE.parents[3] / "sdd" / "tools" / "sddtask.py"
GIT_ENV = dict(os.environ, GIT_OPTIONAL_LOCKS="0")
CODE_PATH_RE = re.compile(r"`([A-Za-z0-9_.][A-Za-z0-9_.\-/]*/[A-Za-z0-9_.\-/]*|[A-Za-z0-9_.\-]+\.[A-Za-z][A-Za-z0-9]*)`")
REVIEW_REV_RE = re.compile(r"^## Revisão (r\d+)\b", re.M)


class InventoryError(RuntimeError):
    pass


def git(root: Path, *args: str, check: bool = True) -> bytes:
    proc = subprocess.run(["git", "--no-optional-locks", "-C", str(root), *args],
                          capture_output=True, check=False, env=GIT_ENV)
    if check and proc.returncode != 0:
        raise InventoryError(f"git {' '.join(args)} falhou: {proc.stderr.decode(errors='replace').strip()}")
    return proc.stdout


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


def load_parser():
    path = TRUSTED_PARSER
    if not path.is_file() or path.is_symlink():
        raise InventoryError(f"{path} ausente: a skill usa o parser do próprio checkout, não o do --root")
    spec = importlib.util.spec_from_file_location("sddtask", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["sddtask"] = mod
    previous = sys.dont_write_bytecode
    sys.dont_write_bytecode = True  # somente leitura: não criar __pycache__ no repositório auditado
    try:
        spec.loader.exec_module(mod)
    finally:
        sys.dont_write_bytecode = previous
    return mod


def pick_task(root: Path, sddtask, task_id: str | None) -> Path:
    if task_id:
        path = root / "sdd" / "tasks" / f"{task_id}.md"
        if not path.is_file():
            raise InventoryError(f"{path} ausente")
        return path
    tasks = sddtask.find_tasks(root)
    if not tasks:
        raise InventoryError("nenhum registro em sdd/tasks/")
    open_tasks = [p for p in tasks if sddtask.parse(p).meta.get("Estado", "").startswith("aberta")]
    return max(open_tasks or tasks, key=lambda p: (p.stat().st_mtime, p.name))


def cited_paths(text: str) -> set[str]:
    out = set()
    for raw in CODE_PATH_RE.findall(text):
        cand = raw.rstrip("/").removeprefix("./")
        if "*" in cand or cand.startswith(("-", "http")):
            continue
        out.add(cand)
    return out


def matches(cited: str, path: str) -> bool:
    return path == cited or path.startswith(cited + "/") or path.endswith("/" + cited)


def build(root: Path, task_id: str | None) -> dict:
    git(root, "rev-parse", "--git-dir")
    sddtask = load_parser()
    path = pick_task(root, sddtask, task_id)
    task = sddtask.parse(path)
    if not task.id:
        raise InventoryError(f"{path}: primeira linha deve ser '# <ID> — <título>'")

    criteria = [{"id": c.id, "lineno": c.lineno, "sha256": c.sha256, "method": bool(c.method),
                 "expected": bool(c.expected), "pending": c.pending} for c in task.criteria]
    ac_ids = {c.id for c in task.criteria}
    mapped = set(task.ac_req)
    reqs_with_ac = {r for rs in task.ac_req.values() for r in rs}
    fresh = sddtask.freshness(task, root)

    rel_task = path.relative_to(root).as_posix()
    own = {rel_task, rel_task.removesuffix(".md") + ".review.md"}
    changes = [c for c in changed_paths(root) if c["path"] not in own]
    cited = cited_paths(task.section_text(5) + "\n" + task.section_text(7)) - own
    changed_uncited = [c for c in changes if not any(matches(p, c["path"]) for p in cited)]
    cited_without_change = sorted(
        p for p in cited if not any(matches(p, c["path"]) or (c["orig"] and matches(p, c["orig"])) for c in changes)
    )

    review = path.with_name(path.name.removesuffix(".md") + ".review.md")
    review_info = {"present": review.is_file()}
    if review.is_file():
        data = review.read_bytes()
        review_info |= {"path": review.relative_to(root).as_posix(), "sha256": hashlib.sha256(data).hexdigest(),
                        "revisions": REVIEW_REV_RE.findall(data.decode(errors="replace"))}

    head = git(root, "log", "-1", "--format=%H%x00%ci", check=False).decode().split("\0")
    return {
        "root": str(root),
        "branch": git(root, "rev-parse", "--abbrev-ref", "HEAD", check=False).decode().strip() or None,
        "base_commit": {"sha": head[0], "date": head[1].strip()} if len(head) == 2 else None,
        "task": {"path": rel_task, "id": task.id, "title": task.title, "meta": task.meta,
                 "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                 "revisions": [r.rev for r in task.revisions]},
        "divisions_missing": [f"{n} - {name}" for n, name in sddtask.DIVISIONS.items() if n not in task.divisions],
        "criteria": criteria,
        "criteria_incomplete": [c["id"] for c in criteria if not c["pending"] and not (c["method"] and c["expected"])],
        "criteria_pending": [c["id"] for c in criteria if c["pending"]],
        "ac_without_req": sorted(ac_ids - mapped),
        "req_without_ac": sorted(set(task.reqs) - reqs_with_ac),
        "ac_req_unknown": sorted(f"{a}→{r}" for a, rs in task.ac_req.items() for r in rs
                                 if a not in ac_ids or r not in task.reqs),
        "freshness": fresh,
        "freshness_problems": [f for f in fresh if f["status"] in sddtask.PROBLEM_STATUSES],
        "parser": {"path": str(TRUSTED_PARSER), "sha256": hashlib.sha256(TRUSTED_PARSER.read_bytes()).hexdigest()},
        "changed_total": len(changes),
        "changed_uncited": changed_uncited,
        "cited_without_change": cited_without_change,
        "review": review_info,
    }


def to_markdown(inv: dict) -> str:
    t = inv["task"]
    base = inv["base_commit"] or {"sha": "(sem commit)", "date": "-"}
    lines = [f"# Inventário — {t['id']} — {t['title'] or '(sem título)'}", "",
             f"Base {base['sha'][:12]} ({base['date']}), branch {inv['branch']}.",
             f"- Registro `{t['path']}` SHA-256 {t['sha256']}",
             f"- Rota: {t['meta'].get('Rota', '?')} · Revisão: {t['meta'].get('Revisão atual', '?')} · Estado: {t['meta'].get('Estado', '?')}",
             f"- Parser: `{inv['parser']['path']}` SHA-256 {inv['parser']['sha256']}",
             f"- Parecer: " + (f"`{inv['review']['path']}` revisões {inv['review']['revisions']}" if inv["review"]["present"] else "inexistente (será r1)"),
             ""]

    def block(title: str, items: list[str]) -> None:
        lines.extend([f"## {title}: {len(items)}", ""] + ([f"- {i}" for i in items] or ["- (nenhum)"]) + [""])

    block("Divisões do prompt ausentes", inv["divisions_missing"])
    block("ACs sem método ou esperado", inv["criteria_incomplete"])
    block("ACs PENDENTE", inv["criteria_pending"])
    block("ACs sem REQ", inv["ac_without_req"])
    block("REQs sem AC", inv["req_without_ac"])
    block("Mapeamentos AC→REQ com ID inexistente", inv["ac_req_unknown"])
    block("Evidência com problema (stale, malformed, missing, duplicate, no-inputs, unknown-criterion)",
          [f"{f['kind']} {f['id']} [{f.get('layer') or '-'}]: {f['status']}"
           + (f" (registrado {f['recorded'][:16]}…, atual {f['current'][:16] or '—'}…)" if f["kind"] in ("criterion", "input") else "")
           for f in inv["freshness_problems"]])
    block("Inputs não verificáveis por bytes", [f["id"] for f in inv["freshness"] if f["status"] == "unverifiable"])
    block(f"Alterados no Git sem citação nas seções 5/7 (de {inv['changed_total']})",
          [f"`{c['status']}` {c['path']}" for c in inv["changed_uncited"]])
    block("Citados nas seções 5/7 sem mudança no Git", inv["cited_without_change"])
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=".", type=Path)
    ap.add_argument("--task", help="ID da task; padrão: a aberta alterada mais recentemente")
    ap.add_argument("--format", choices=("json", "md"), default="json")
    args = ap.parse_args()
    try:
        inv = build(args.root.resolve(), args.task)
    except (InventoryError, OSError, UnicodeDecodeError) as exc:
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
