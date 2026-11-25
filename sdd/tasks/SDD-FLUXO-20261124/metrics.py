#!/usr/bin/env python3
"""Métricas de inchaço e fragmentação do SDD (SDD-FLUXO-20261124). Somente leitura, stdlib.

Uso, da raiz do Ox:
  python3 sdd/tasks/SDD-FLUXO-20261124/metrics.py                 # working tree
  bash sdd/tasks/SDD-FLUXO-20261124/head_metrics.sh [<commit>]    # bytes de um commit (HEAD)

Conjunto normativo: AGENTS.md, sdd/constitution.md, sdd/project.md, sdd/workflow.md,
sdd/templates/*.md, .codex/config.toml e .codex/agents/*.toml. Leitura obrigatória (ADR
docs/decisions/sdd-model.md): AGENTS.md, constitution, project, workflow e a skill prompt.
Fragmentação: trechos de 8 palavras seguidas (tokens \\w+, minúsculas) presentes em mais de um
arquivo do conjunto, ou repetidos em posições não sobrepostas dentro de um mesmo arquivo. Texto de
um TOML: comentários e os campos `description` e `developer_instructions`, cada um à parte; nomes
de chave e valores de configuração (modelo, esforço) são dados cuja fonte única é o próprio TOML.
"""
import argparse
import json
import re
import sys
import tomllib
from pathlib import Path

N = 8
READING = ["AGENTS.md", "sdd/constitution.md", "sdd/project.md", "sdd/workflow.md",
           ".codex/skills/prompt/SKILL.md"]
FIXED = ["AGENTS.md", "sdd/constitution.md", "sdd/project.md", "sdd/workflow.md",
         "sdd/templates/task.md", "sdd/templates/spec.md", ".codex/config.toml"]
MODEL_RE = re.compile(r"gpt-\d|\bSol \d|\bAstra \d")


def parts(path: str, text: str) -> list[str]:
    """Trechos de texto normativo de um arquivo; cada trecho gera 8-gramas sem cruzar o vizinho."""
    if not path.endswith(".toml"):
        return [text]
    data = tomllib.loads(text)
    comments = [line for line in text.splitlines() if line.lstrip().startswith("#")]
    return comments + [str(data[k]) for k in ("description", "developer_instructions") if k in data]


def shingles(text: str) -> list[str]:
    words = re.findall(r"\w+", text.lower())
    return [" ".join(words[i:i + N]) for i in range(len(words) - N + 1)]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".", type=Path, help="árvore medida (padrão: working tree)")
    ap.add_argument("--label", default="working-tree")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    root = args.root
    paths = FIXED + sorted(p.relative_to(root).as_posix() for p in (root / ".codex/agents").glob("*.toml"))
    texts = {p: (root / p).read_text(encoding="utf-8") for p in paths}
    owners: dict[str, set[str]] = {}
    intra: dict[str, int] = {}
    for path, text in texts.items():
        seq = [(k, i, s) for k, part in enumerate(parts(path, text)) for i, s in enumerate(shingles(part))]
        first: dict[str, tuple[int, int]] = {}
        for k, i, s in seq:
            owners.setdefault(s, set()).add(path)
            if s in first and (first[s][0] != k or i - first[s][1] >= N):
                intra[path] = intra.get(path, 0) + 1
            first.setdefault(s, (k, i))
    cross = sorted(s for s, ps in owners.items() if len(ps) > 1)
    pairs: dict[str, int] = {}
    for s in cross:
        key = " + ".join(sorted(owners[s]))
        pairs[key] = pairs.get(key, 0) + 1
    report = {
        "rev": args.label,
        "reading_words": sum(len((root / p).read_text(encoding="utf-8").split()) for p in READING),
        "normative_lines": sum(t.count("\n") for t in texts.values()),
        "normative_words": sum(len(t.split()) for t in texts.values()),
        "profile_instruction_words": sum(len(" ".join(parts(p, t)).split()) for p, t in texts.items()
                                         if p.startswith(".codex/")),
        "template_task_words": len(texts["sdd/templates/task.md"].split()),
        "cross_file_shared_8grams": len(cross),
        "cross_file_by_files": pairs,
        "intra_file_repeated_8grams": intra,
        "model_mentions_outside_toml": {p: len(MODEL_RE.findall(t)) for p, t in texts.items()
                                        if not p.endswith(".toml") and MODEL_RE.search(t)},
    }
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=1, sort_keys=True))
    else:
        for k, v in report.items():
            print(f"{k}: {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
