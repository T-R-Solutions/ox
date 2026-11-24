# Spec — plugin-host

Spec viva da capacidade `plugin-host`. Migrada em 2026-11-23 da feature `product-plugin-host` do modelo
anterior (título original: "Specification: product-plugin-host"). Texto original preservado; ACs marcados
`(herdado)` mantêm o estado registrado até 2026-11-23, mas a evidência bruta foi removida e
não sustenta nova aprovação. A task que tocar a capacidade reescreve o AC na forma
`| método: … | esperado: …` e o reavalia. As limitações técnicas foram mantidas; as notas de
controle de evidência do modelo anterior, não.

## O quê e por quê

Actor: local application caller using explicitly supplied local fixtures.
Scope: bounded Linux x86_64 library slice, no UI integration or remote services.

No sandbox, remote-provider integration, production readiness or F0 completion is claimed.

## Requisitos

- REQ-01: A real local plugin process negotiates protocol 1.0 and completes a correlated echo request.
- REQ-02: An incompatible major version is rejected before any operation.
- REQ-03: Echo requires both plugin-advertised support and caller grant; denied operations are not sent.
- REQ-04: Malformed, oversized and mismatched response frames fail the host without approval.
- REQ-05: A silent plugin times out within the configured deadline and an unexpected exit is distinguished.
- REQ-06: Shutdown closes admission, reaps the child and releases its socket; recovery starts a new independent host.

## Critérios de aceitação

- AC-01 → REQ-01: A real local plugin process negotiates protocol 1.0 and completes a correlated echo request. (herdado)
- AC-02 → REQ-02: An incompatible major version is rejected before any operation. (herdado)
- AC-03 → REQ-03: Echo requires both plugin-advertised support and caller grant; denied operations are not sent. (herdado)
- AC-04 → REQ-04: Malformed, oversized and mismatched response frames fail the host without approval. (herdado)
- AC-05 → REQ-05: A silent plugin times out within the configured deadline and an unexpected exit is distinguished. (herdado)
- AC-06 → REQ-06: Shutdown closes admission, reaps the child and releases its socket; recovery starts a new independent host. (herdado)

## Estado atual

| AC | Estado | Decidido por (task) | Data |
|---|---|---|---|
| AC-01 | INCONCLUSIVE | modelo anterior (herdado) | ≤ 2026-11-23 |
| AC-02 | INCONCLUSIVE | modelo anterior (herdado) | ≤ 2026-11-23 |
| AC-03 | INCONCLUSIVE | modelo anterior (herdado) | ≤ 2026-11-23 |
| AC-04 | INCONCLUSIVE | modelo anterior (herdado) | ≤ 2026-11-23 |
| AC-05 | INCONCLUSIVE | modelo anterior (herdado) | ≤ 2026-11-23 |
| AC-06 | INCONCLUSIVE | modelo anterior (herdado) | ≤ 2026-11-23 |

## Limites e questões abertas

- Current successor: F0 OPEN. Historical limitations below describe their original observations. Full native journey, GUI/frame/CPU adopted limits and instrumented GUI intermittency remain unresolved; see current report. No persistence/distribution/remote-agent implementation or commits.
- Linux-only Unix sockets; controlled fixture, no authentication against malicious same-user clients or OS sandbox.
- One direct child supervised; descendants, CPU/RAM enforcement and hostile executable cleanup are not covered.
- Deadline per connection/frame/shutdown, not one aggregate session budget; no retry or persistent recovery.
- No desktop UI or third-party plugin integration, installation, publication or remote service.
