# Spec — agent-runtime

Spec viva da capacidade `agent-runtime`. Migrada em 2026-11-23 da feature `product-agent-runtime` do modelo
anterior (título original: "Specification: product-agent-runtime"). Texto original preservado; ACs marcados
`(herdado)` mantêm o estado registrado até 2026-11-23, mas a evidência bruta foi removida e
não sustenta nova aprovação. A task que tocar a capacidade reescreve o AC na forma
`| método: … | esperado: …` e o reavalia. As limitações técnicas foram mantidas; as notas de
controle de evidência do modelo anterior, não.

## O quê e por quê

Actor: local application caller using explicitly supplied local fixtures.
Scope: bounded Linux x86_64 library slice, no UI integration or remote services.

No sandbox, remote-provider integration, production readiness or F0 completion is claimed.

## Requisitos

- REQ-01: A controlled local adapter runs to success or nonzero failure with observed process exit and ordered lifecycle events.
- REQ-02: Cancellation enters Cancelling before an observed terminal Cancelled outcome and reaps the owned child.
- REQ-03: Wrong-generation, duplicate, out-of-order and late completion events cannot corrupt terminal or current session state.
- REQ-04: Execution deadlines stop a hanging local adapter and recovery creates a fresh attempt with no old events or grants.
- REQ-05: Runtime and controlled adapter preserve a workspace sentinel; output and supervision limitations are explicit.

## Critérios de aceitação

- AC-01 → REQ-01: A controlled local adapter runs to success or nonzero failure with observed process exit and ordered lifecycle events. (herdado)
- AC-02 → REQ-02: Cancellation enters Cancelling before an observed terminal Cancelled outcome and reaps the owned child. (herdado)
- AC-03 → REQ-03: Wrong-generation, duplicate, out-of-order and late completion events cannot corrupt terminal or current session state. (herdado)
- AC-04 → REQ-04: Execution deadlines stop a hanging local adapter and recovery creates a fresh attempt with no old events or grants. (herdado)
- AC-05 → REQ-05: Runtime and controlled adapter preserve a workspace sentinel; output and supervision limitations are explicit. (herdado)

## Estado atual

| AC | Estado | Decidido por (task) | Data |
|---|---|---|---|
| AC-01 | INCONCLUSIVE | modelo anterior (herdado) | ≤ 2026-11-23 |
| AC-02 | INCONCLUSIVE | modelo anterior (herdado) | ≤ 2026-11-23 |
| AC-03 | INCONCLUSIVE | modelo anterior (herdado) | ≤ 2026-11-23 |
| AC-04 | INCONCLUSIVE | modelo anterior (herdado) | ≤ 2026-11-23 |
| AC-05 | INCONCLUSIVE | modelo anterior (herdado) | ≤ 2026-11-23 |

## Limites e questões abertas

- Controlled local no-output adapter only; no real agent, provider, credentials, network or code transmission.
- Caller must poll to enforce runtime deadline; process-tree containment and OS CPU/memory limits absent.
- Drop kills/reaps direct child only; no durable state, crash restart, pause, resume, usage or output capture.
- Workspace preservation demonstrated with controlled fixture; arbitrary executable retains OS permissions.
