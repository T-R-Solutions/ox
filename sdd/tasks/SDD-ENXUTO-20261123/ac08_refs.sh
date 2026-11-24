#!/usr/bin/env bash
# AC-08 (r3) de SDD-ENXUTO-20261123: gera as listas do Git e roda ac08_refs.py (exit 0 = nenhuma).
# A base é fixa: ea3cf0f é o último commit com o legado. Com HEAD, os caminhos removidos sumiriam
# da lista depois do commit da remoção e a busca deixaria de vê-los (revisão externa 2).
set -euo pipefail
base=ea3cf0f2b52deefb68126c4469320846aa37d438
if ! git cat-file -e "${base}^{commit}" 2>/dev/null; then
  echo "falha: commit base ${base} ausente (clone raso?)" >&2
  exit 2
fi
dir=$(mktemp -d)
trap 'rm -rf -- "$dir"' EXIT
git ls-tree -r -z --name-only "$base" >"$dir/base.txt"
git ls-files -z -co --exclude-standard >"$dir/active.txt"
echo "base=${base:0:7}"
python3 "$(dirname -- "$0")/ac08_refs.py" "$dir/base.txt" "$dir/active.txt"
