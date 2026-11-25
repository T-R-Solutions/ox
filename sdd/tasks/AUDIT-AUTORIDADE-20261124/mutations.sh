#!/usr/bin/env bash
# Sensibilidade de check.sh (AUDIT-AUTORIDADE-20261124): numa cópia descartável do commit-base,
# passa só com a correção e falha sem ela e em cada mutação; continua passando com a correção já
# commitada sobre a base. Rode da raiz do Ox; não altera o repositório.
set -euo pipefail
root=$PWD
base=10d9570ba57d98597491b2372e3e310dd46a7851
ref=.claude/skills/codex-task-audit/references/ox-governance.md
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
git archive "$base" .claude sdd/constitution.md | tar -x -C "$work"
cp sdd/tasks/AUDIT-AUTORIDADE-20261124/check.sh "$work/check.sh"
cd "$work"
git init -q && git add -A && git -c user.name=oracle -c user.email=oracle@invalid commit -qm base
copy_base=$(git rev-parse HEAD)

failures=0
# case_ <esperado: passa|falha> <nome>: roda o oráculo contra a base da cópia, compara e restaura.
case_() {
    if bash check.sh "$copy_base" >log 2>&1; then got=passa; else got=falha; fi
    if [ "$got" = "$1" ]; then echo "ok     $got: $2"; else echo "FALHA  $got: $2"; failures=$((failures + 1)); fi
    git checkout -q -- . && git clean -qfd -e check.sh -e log
}
fix() { cp "$root/$ref" "$ref"; }

case_ falha "commit-base, sem a correção"
fix; case_ passa "com a correção"
fix; sed -i 's/governança-do-processo/governanca-do-processo/' "$ref"; case_ falha "âncora inexistente"
fix; echo '`a` > `b`' >>.claude/skills/codex-task-audit/SKILL.md; case_ falha "ordem de autoridade em outro arquivo da skill"
fix; echo 'x' >>"$ref"; case_ falha "outra linha alterada"
fix; sed -i 's/\*\*Cadeia de autoridade:\*\*/Cadeia:/' sdd/constitution.md; case_ falha "seção sem a cadeia de autoridade"
fix; git add "$ref" && git -c user.name=oracle -c user.email=oracle@invalid commit -qm fix
[ -z "$(git diff HEAD -- "$ref")" ] || { echo "FALHA  a correção não entrou no commit"; exit 1; }
case_ passa "correção já commitada (diff contra HEAD vazio)"
echo "$failures caso(s) divergente(s) de 7"
exit $((failures > 0))
