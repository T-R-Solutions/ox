# Spec — local-task-ui

Spec viva da capacidade `local-task-ui`. Migrada em 2026-11-23 da feature `product-local-task-ui` do modelo
anterior (título original: "Specification: product-local-task-ui"). Texto original preservado; ACs marcados
`(herdado)` mantêm o estado registrado até 2026-11-23, mas a evidência bruta foi removida e
não sustenta nova aprovação. A task que tocar a capacidade reescreve o AC na forma
`| método: … | esperado: …` e o reavalia. As limitações técnicas foram mantidas; as notas de
controle de evidência do modelo anterior, não.

## O quê e por quê

Actor: local desktop user. One active controlled task; no arbitrary commands, remote agents, sandbox claim or general persistence. Scope authorized in sdd/project.md.

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

- REQ-01: Existing accessible workspace accepted; missing or inaccessible directory refused before process launch.
- REQ-02: Real controlled task execution reaches coherent observed success, failure or timeout states.
- REQ-03: Cancellation remains pending until child termination is observed.
- REQ-04: Duplicate actions, workspace changes while busy and late events cannot corrupt another attempt.
- REQ-05: Execution and verification leave the actual interface responsive.
- REQ-06: Independent oracle approves the correct task-produced result and rejects incorrect bytes or identity.
- REQ-07: Absent evidence and completion claims never approve a result.
- REQ-08: Changed inputs invalidate current acceptance while preserving prior observations.
- REQ-09: Exclusive task directories preserve all preexisting workspace content.
- REQ-10: Window close supervises owned work through termination before application exit.
- REQ-11: Five evidence states, criterion, attempt, verification run, inputs and observation freshness are visible.

## Critérios de aceitação

- AC-01 → REQ-01: Existing accessible workspace accepted; missing or inaccessible directory refused before process launch. (herdado)
- AC-02 → REQ-02: Real controlled task execution reaches coherent observed success, failure or timeout states. (herdado)
- AC-03 → REQ-03: Cancellation remains pending until child termination is observed. (herdado)
- AC-04 → REQ-04: Duplicate actions, workspace changes while busy and late events cannot corrupt another attempt. (herdado)
- AC-05 → REQ-05: Execution and verification leave the actual interface responsive. (herdado)
- AC-06 → REQ-06: Independent oracle approves the correct task-produced result and rejects incorrect bytes or identity. (herdado)
- AC-07 → REQ-07: Absent evidence and completion claims never approve a result. (herdado)
- AC-08 → REQ-08: Changed inputs invalidate current acceptance while preserving prior observations. (herdado)
- AC-09 → REQ-09: Exclusive task directories preserve all preexisting workspace content. (herdado)
- AC-10 → REQ-10: Window close supervises owned work through termination before application exit. (herdado)
- AC-11 → REQ-11: Five evidence states, criterion, attempt, verification run, inputs and observation freshness are visible. (herdado)

## Estado atual

| AC | Estado | Decidido por (task) | Data |
|---|---|---|---|
| AC-01 | INCONCLUSIVE | modelo anterior (herdado) | ≤ 2026-11-23 |
| AC-02 | INCONCLUSIVE | modelo anterior (herdado) | ≤ 2026-11-23 |
| AC-03 | INCONCLUSIVE | modelo anterior (herdado) | ≤ 2026-11-23 |
| AC-04 | INCONCLUSIVE | modelo anterior (herdado) | ≤ 2026-11-23 |
| AC-05 | APPROVED | modelo anterior (herdado) | ≤ 2026-11-23 |
| AC-06 | INCONCLUSIVE | modelo anterior (herdado) | ≤ 2026-11-23 |
| AC-07 | INCONCLUSIVE | modelo anterior (herdado) | ≤ 2026-11-23 |
| AC-08 | INCONCLUSIVE | modelo anterior (herdado) | ≤ 2026-11-23 |
| AC-09 | INCONCLUSIVE | modelo anterior (herdado) | ≤ 2026-11-23 |
| AC-10 | INCONCLUSIVE | modelo anterior (herdado) | ≤ 2026-11-23 |
| AC-11 | INCONCLUSIVE | modelo anterior (herdado) | ≤ 2026-11-23 |

## Limites e questões abertas

- Current memory successor: T903 complete within the adopted controlled boundary; earlier open/inconclusive entries below are historical. Isolated sessions, no physical scanout, direct children only, cooperative I/O cancellation; see successor report.
- Current memory successor: Final documentary gates pending. Isolated sessions, no physical scanout, direct children only, cooperative I/O cancellation; see successor report.
- T903 successor: current F0/full-count GUI RSS acceptance INCONCLUSIVE, T903 open; small GUI/functional/worker observations and documentary preparation are independently bounded. See report. Historical limitations below retain original scope.
- Current successor: F0 OPEN. Historical limitations below describe their original observations. Full native journey, GUI/frame/CPU adopted limits and instrumented GUI intermittency remain unresolved; see current report. No persistence/distribution/remote-agent implementation or commits.
- Controlled local fixtures only; no sandbox, remote agents, persistent history or F0 completion.
- Refresh is explicit; displayed acceptance is as of its observation time. Engine history is bounded to 32 observations.
- Direct-child supervision only; graceful close waits for work; forced application kill and process descendants are outside this guarantee.
- Native observation is reused only after production input/binary comparison; X11 is a separate temporary-server result, not main-session repair.
- Some user _new screenshots were unavailable when archival was attempted; direct visual review and explicit human replies are retained.
- Verification responsiveness/closing combines worker ownership review and Engine/reducer tests with actual fast graphical verification; no slow-verification graphical capture or numerical latency SLO claimed.
- 2026-11-05: historical graphical/performance closure is preserved on old inputs; current UI response/close/display and F0 operational acceptance await T903. Storage is not implemented. See (evidência removida em 2026-11-23; histórico Git)
- 2026-11-19 R3: only AC-05 reaccepted for the identified current X11 observation. Historical environments, failures and other unverified criteria remain unchanged; hashbrown and other task-level blockers remain.
