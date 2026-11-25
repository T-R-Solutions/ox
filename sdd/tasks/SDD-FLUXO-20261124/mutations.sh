#!/usr/bin/env bash
# AC-06 de SDD-FLUXO-20261124: numa cópia descartável, o teste de instruções passa no original e
# falha em cada mutação. Rode da raiz do Ox; não altera o repositório.
set -euo pipefail

work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
files=(AGENTS.md sdd/constitution.md sdd/project.md sdd/workflow.md sdd/templates/task.md
       sdd/templates/spec.md sdd/tools/sddtask.py .codex/config.toml .codex/agents/*.toml
       tools/governance/tests/test_instruction_routes.py)

fresh() {
    rm -rf "$work/c"
    for f in "${files[@]}"; do
        mkdir -p "$work/c/$(dirname "$f")"
        cp "$f" "$work/c/$f"
    done
}

# Os testes estruturais; os de commit e do CLI em modo plano não leem os arquivos mutados.
run() {
    (cd "$work/c" && PYTHONDONTWRITEBYTECODE=1 python3 -I -m unittest discover \
        -s tools/governance/tests -p test_instruction_routes.py \
        -k profiles -k workflow_names -k model_and_effort -k stage_8 -k no_rule_text -k template_keeps) \
        >"$work/log" 2>&1
}

# mutate <arquivo> <trecho> <substituto>: troca exatamente uma ocorrência ou aborta.
mutate() {
    python3 -I - "$work/c/$1" "$2" "$3" <<'PY'
import sys
from pathlib import Path
path, old, new = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
text = path.read_text(encoding="utf-8")
if text.count(old) != 1:
    sys.exit(f"mutação não aplicável: {old!r} em {path}")
path.write_text(text.replace(old, new), encoding="utf-8")
PY
}

fresh
run || { cat "$work/log"; echo "FALHA: o original não passa"; exit 1; }
echo "original: passa"

failures=0
check() {
    if run; then
        echo "FALHA: mutação não detectada: $1"
        failures=$((failures + 1))
    else
        echo "mutação detectada: $1"
    fi
}

fresh; mutate .codex/agents/ec_verificador.toml 'papel-verificador."' 'papel-verificador. Rode sddtask.py evidence."'
check "comando do SDD num perfil"
fresh; mutate sdd/workflow.md '| Raiz (controlador) | sessão raiz |' '| Raiz (controlador) | sessão raiz (gpt-6.1-sol) |'
check "modelo no workflow"
fresh; mutate .codex/agents/ec_planejador.toml 'developer_instructions = "Siga sdd/workflow.md#papel-planejador."' 'developer_instructions = "Siga sdd/workflow.md#papel-inexistente."'
check "âncora inexistente"
fresh; mutate sdd/workflow.md 'com `--write` e depois com `--check --require-all`' 'com `--check --require-all` e depois com `--write`'
check "ordem invertida na etapa 8"
fresh; mutate sdd/workflow.md '| Verificador | `ec_verificador` | — |' '| Verificador | `ec_verificador` | `ec_revisor`, sem TOML |'
check "perfil sem TOML"
fresh; mutate AGENTS.md '## Permissões que exigem pedido explícito' 'Cada resposta reescreve o AC pendente na forma completa.

## Permissões que exigem pedido explícito'
check "regra do workflow copiada no AGENTS.md"
fresh; mutate .codex/agents/ec_implementador.toml 'papel-implementador."' 'papel-implementador. Rode cargo test."'
check "outro comando num perfil"
fresh; mutate .codex/agents/ec_verificador.toml 'description = "Verificador independente (sdd/workflow.md#papel-verificador)."' 'description = "Verificador (sdd/workflow.md#papel-inexistente); rode python3 x.py."'
check "âncora inexistente e comando na description"

echo "$failures mutação(ões) não detectada(s) de 8"
exit $((failures > 0))
