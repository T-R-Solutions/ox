#!/usr/bin/env bash
# AC-13 (r2) de SDD-ENXUTO-20261123: o aceite das tasks é conferível em outro checkout.
# Copia os arquivos ativos (git ls-files -co --exclude-standard) para um diretório temporário,
# sem .local/ nem outros ignorados, e roda nele validate.py e evidence --check --require-all
# de cada task. Reproduz a revisão externa (achado 2). Exit 0 = nenhuma falha.
set -euo pipefail
dir=$(mktemp -d)
trap 'rm -rf -- "$dir"' EXIT
git ls-files -co --exclude-standard -z \
  | while IFS= read -r -d '' f; do
      if [ -e "$f" ] || [ -L "$f" ]; then printf '%s\0' "$f"; fi
    done \
  | tar --null -T - -cf - | tar -xf - -C "$dir"
if [ -e "$dir/.local" ]; then echo "falha: .local/ copiado"; exit 1; fi
cd "$dir"
fails=0
tasks=0
PYTHONDONTWRITEBYTECODE=1 python3 sdd/tools/validate.py --root . || fails=$((fails + 1))
for rec in sdd/tasks/*.md; do
  case "$rec" in *.review.md) continue ;; esac
  id=$(basename "$rec" .md)
  tasks=$((tasks + 1))
  PYTHONDONTWRITEBYTECODE=1 python3 sdd/tools/sddtask.py evidence --root . --task "$id" --check --require-all \
    || fails=$((fails + 1))
done
echo "tasks=$tasks falhas=$fails local_copiado=0"
[ "$fails" -eq 0 ]
