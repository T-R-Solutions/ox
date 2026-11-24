# Spec — verification-engine

Spec viva da capacidade `verification-engine`. Migrada em 2026-11-23 da feature `product-verification-engine` do modelo
anterior (título original: "Specification: product-verification-engine"). Texto original preservado; ACs marcados
`(herdado)` mantêm o estado registrado até 2026-11-23, mas a evidência bruta foi removida e
não sustenta nova aprovação. A task que tocar a capacidade reescreve o AC na forma
`| método: … | esperado: …` e o reavalia. As limitações técnicas foram mantidas; as notas de
controle de evidência do modelo anterior, não.

## O quê e por quê

Actor: local application caller using explicitly supplied local fixtures.
Scope: bounded Linux x86_64 library slice, no UI integration or remote services.

No sandbox, remote-provider integration, production readiness or F0 completion is claimed.

### Bounded robustness clarification — 2026-11-05

Existing criteria include rejection of nonregular evidence with no approval;
regular files and symlinks to regular files retain the exact-byte behavior.
Metadata checks are not atomic capture. Linux nonblocking open covers FIFO
replacement at open, not universal filesystem cancellation. Deadline covers
subprocess supervision, not metadata/open/read/reap. Graceful close waits for
worker return; no universal close latency is promised. Every spawned direct
child has an owner through error cleanup; cleanup failures are visible alongside
the original error. No descendant or OS-isolation guarantee is introduced.

## Requisitos

- REQ-01: Approval requires a real local execution matching an explicit exit-code oracle and unchanged observed inputs.
- REQ-02: Missing evidence and agent/task completion claims never produce approval.
- REQ-03: Observed failures remain in immutable history and contradictory same-input observations cannot silently replace rejection.
- REQ-04: Changed implementation inputs, criterion or oracle invalidate dependent acceptance without invalidating unrelated criteria.
- REQ-05: Five SDD states remain distinct and each observation exposes execution identity, command, result and evaluated content.

## Critérios de aceitação

- AC-01 → REQ-01: Approval requires a real local execution matching an explicit exit-code oracle and unchanged observed inputs. (herdado)
- AC-02 → REQ-02: Missing evidence and agent/task completion claims never produce approval. (herdado)
- AC-03 → REQ-03: Observed failures remain in immutable history and contradictory same-input observations cannot silently replace rejection. (herdado)
- AC-04 → REQ-04: Changed implementation inputs, criterion or oracle invalidate dependent acceptance without invalidating unrelated criteria. (herdado)
- AC-05 → REQ-05: Five SDD states remain distinct and each observation exposes execution identity, command, result and evaluated content. (herdado)

## Estado atual

| AC | Estado | Decidido por (task) | Data |
|---|---|---|---|
| AC-01 | INCONCLUSIVE | modelo anterior (herdado) | ≤ 2026-11-23 |
| AC-02 | INCONCLUSIVE | modelo anterior (herdado) | ≤ 2026-11-23 |
| AC-03 | INCONCLUSIVE | modelo anterior (herdado) | ≤ 2026-11-23 |
| AC-04 | INCONCLUSIVE | modelo anterior (herdado) | ≤ 2026-11-23 |
| AC-05 | INCONCLUSIVE | modelo anterior (herdado) | ≤ 2026-11-23 |

## Limites e questões abertas

- Current memory successor: T903 complete within the adopted controlled boundary; earlier open/inconclusive entries below are historical. Isolated sessions, no physical scanout, direct children only, cooperative I/O cancellation; see successor report.
- Current memory successor: Final documentary gates pending. Isolated sessions, no physical scanout, direct children only, cooperative I/O cancellation; see successor report.
- T903 successor: current F0/full-count GUI RSS acceptance INCONCLUSIVE, T903 open; small GUI/functional/worker observations and documentary preparation are independently bounded. See report. Historical limitations below retain original scope.
- Current successor: F0 OPEN. Historical limitations below describe their original observations. Full native journey, GUI/frame/CPU adopted limits and instrumented GUI intermittency remain unresolved; see current report. No persistence/distribution/remote-agent implementation or commits.
- In-memory local exit-code oracle only; no persistence, artifact authentication, arbitrary oracle suitability proof or real-agent integration.
- Exact byte snapshots are bounded, not cryptographic hashes; dependency completeness is caller responsibility. Environment/dynamic libraries and transient concurrent changes between snapshots are not fully bound.
- Direct-child deadlines only; no process-tree or OS sandbox. Output is unavailable for this exit-only oracle.
- Caller explicitly supplies executable and inputs; accepting evidence grants no execution, publication or deployment permissions.
- 2026-11-05: historical graphical/performance closure is preserved on old inputs; current UI response/close/display and F0 operational acceptance await T903. Storage is not implemented. See (evidência removida em 2026-11-23; histórico Git)
