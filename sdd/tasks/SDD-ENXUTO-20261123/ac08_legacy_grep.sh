#!/usr/bin/env bash
# AC-08 de SDD-ENXUTO-20261123: referências ao legado em arquivos ativos (exit 0 = nenhuma).
set -u
excl='^(sdd/tasks/SDD-ENXUTO-20261123(\.md|/.*)|docs/decisions/sdd-model\.md|scripts/config/native/gitleaks/gitleaks-history\.ignore|scripts/tests/test_governance_diagnostics\.py|scripts/tests/fixtures/governance-links\.txt|application/vendor/cryoglyph-0\.1\.0/OX-PATCH\.md|docs/licensing/copy-provenance\.json|docs/licensing/license-inventory\.json)$'
pattern='sdd/history|docs/validation|\.ai/|task_finalizada|profile\.json|normative-coverage|history-manifest|codex-agents\.md|ec_triador|ec_validador|ec_revisor|ec_testador|ec_analista|sdd/skills\.md|sdd/agents\.md'
hits=$({ git ls-files; git ls-files -o --exclude-standard; } | sort -u | grep -Ev "$excl" \
  | while IFS= read -r f; do [ -f "$f" ] && printf '%s\0' "$f"; done | xargs -0 grep -nIE "$pattern" 2>/dev/null)
canon=$(grep -rn "procedimento canônico" .codex 2>/dev/null)
all=$(printf '%s\n%s' "$hits" "$canon" | sed '/^$/d')
printf '%s\n' "$all"
echo "ocorrencias=$(printf '%s' "$all" | grep -c .)"
[ -z "$all" ]
