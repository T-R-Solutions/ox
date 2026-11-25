#!/usr/bin/env bash
# Linha de base de metrics.py nos bytes de um commit (padrão: HEAD), extraídos com git archive
# para um diretório descartável; o Python não chama subprocess. Rode da raiz do Ox.
set -euo pipefail
rev=${1:-HEAD}
base=$(mktemp -d)
trap 'rm -rf "$base"' EXIT
git archive "$rev" AGENTS.md sdd/constitution.md sdd/project.md sdd/workflow.md sdd/templates \
    .codex/config.toml .codex/agents .codex/skills/prompt/SKILL.md | tar -x -C "$base"
python3 -I sdd/tasks/SDD-FLUXO-20261124/metrics.py --root "$base" --label "$rev"
