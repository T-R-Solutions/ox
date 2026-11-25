# Instruções operacionais — Ox

Entrada operacional (GOV-03): as regras vivem em [sdd/](sdd/), na ordem de autoridade da
[constituição](sdd/constitution.md#governança-do-processo).

## Para todo pedido

Siga [sdd/workflow.md](sdd/workflow.md) a partir da etapa 0. Use subagentes nos casos definidos
pela [triagem do Ox](sdd/workflow.md#triagem). Instruções de subdiretórios não podem contradizer
o SDD.

## Permissões que exigem pedido explícito

- Commit, tag, push ou publicação; para commit, consulte
  [commit-governance](.codex/skills/commit-governance/SKILL.md) antes do stage.
- Downloads e manutenção central de ferramentas.
- Verificação completa (seção abaixo).

## Local full-verification environment

Quando a verificação completa for autorizada, use exatamente, da raiz do Ox:

```bash
TOOLBOX_BIN=/home/rodrigo/Projetos/dev_audit/shared-toolbox/bin/toolbox \
TOOLBOX_SELINUX_LABEL=shared \
CARGO_HOME="$PWD/.cache/ox/cargo-home" \
  ./scripts/automate.sh run --scope complete
```

Não omita `TOOLBOX_BIN` nem presuma `toolbox` no PATH. Mantenha o contrato portátil de
override/PATH do wrapper público.

## Trabalho visual

RQ-01: [DESIGN.md](DESIGN.md), [surfaces](docs/design/surfaces.md) e, ao integrar fontes
fornecidas, [reference coverage](docs/design/reference-coverage.md).
