# Ox — estado do projeto

Estado atual apenas. Autorizações anteriores estão no histórico do Git e não renovam permissões.

## Identidade e fase

- Produto: Ox — aplicativo desktop agent-first, local-first e extensível.
- Fase: `implementation-foundation`. Estado do aplicativo: `bootstrap-implemented`.

## Escopo autorizado vigente

| Data | Task | Escopo | Exclusões |
|---|---|---|---|
| — | — | Nenhuma task aberta. [SDD-FLUXO-20261124](tasks/SDD-FLUXO-20261124.md) (fonte única das regras de execução e registro mais leve) foi fechada em 2026-11-24 | — |

Pedidos novos definem o próprio escopo no prompt da task; o pedido original é o
limite de permissão.

## Stack e organização

- Produto: Rust 1.99.1 (pinado), edition 2024, Iced 0.14.0; workspace virtual em
  `application/` com 16 crates (`application/crates/<crate>/src|tests`). Linux x86_64.
- Governança: Python 3.11+ stdlib em `sdd/tools/` e `tools/governance/`. Não valida o
  produto Rust.
- Visual: [DESIGN.md](../DESIGN.md) e [surfaces](../docs/design/surfaces.md), baseline RQ-01.

## Estado das capacidades

Specs vivas em [specs/](specs/README.md). As 10 migradas em 2026-11-23 têm ACs `(herdado)`:
o estado vem do modelo anterior e a evidência bruta foi removida. Limites conhecidos:

- `local-persistence`: AC-01–07 UNVERIFIED; armazenamento D5/D6 pendente.
- `ide-shell`: AC-02 e AC-07 APPROVED; AC-01, AC-03–06 INCONCLUSIVE.
- `bootstrap` AC-02 e `local-task-ui` AC-05 APPROVED; os demais ACs de produto INCONCLUSIVE
  ou UNVERIFIED.
- Agentes reais, grafo e persistência de tarefas: não implementados.

## Comandos

Do SDD: no [workflow](workflow.md). Do produto, em `application/`:

```bash
cargo test --workspace --locked --offline
cargo clippy --workspace --all-targets --locked --offline -- -D warnings
cargo run -p ox-app --bin ox
```

Verificação completa: [AGENTS.md](../AGENTS.md#local-full-verification-environment).
Automação Bash: [scripts/README.md](../scripts/README.md).

## Decisões pendentes

[docs/decisions/open-questions.md](../docs/decisions/open-questions.md) (RQ-03).
