#!/usr/bin/env bash
# AC-02 e AC-03 de SDD-AJUSTES-20261124. Somente leitura; rode da raiz do Ox.
set -euo pipefail
w=sdd/workflow.md
if grep -nE '\b9\.[12]\b' "$w"; then echo "AC-02 falhou: $w cita 9.1 ou 9.2"; exit 1; fi
awk '/^### 7\. Executar/{f=1;next} /^#/{f=0} f' "$w" \
  | grep -q 'atualiza a documentação afetada e `sdd/project.md`' \
  || { echo "AC-02 falhou: etapa 7 não manda atualizar documentação e sdd/project.md"; exit 1; }
echo "AC-02 ok"
bad=$(grep -nH 'validate\.py' "$w" sdd/templates/task.md .codex/agents/*.toml | grep -e '--task' | grep -v -e '--matrix' || true)
[ -z "$bad" ] || { echo "AC-03 falhou:"; echo "$bad"; exit 1; }
echo "AC-03 ok"
