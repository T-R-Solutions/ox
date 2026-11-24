# Spec — bootstrap

Spec viva da capacidade `bootstrap`. Migrada em 2026-11-23 da feature `product-bootstrap` do modelo
anterior (título original: "Specification: product-bootstrap"). Texto original preservado; ACs marcados
`(herdado)` mantêm o estado registrado até 2026-11-23, mas a evidência bruta foi removida e
não sustenta nova aprovação. A task que tocar a capacidade reescreve o AC na forma
`| método: … | esperado: …` e o reavalia. As limitações técnicas foram mantidas; as notas de
controle de evidência do modelo anterior, não.

## O quê e por quê

Request: execute the bootstrap prompt v2.0 (removed on 2026-11-23; recoverable from Git history). Actor: local desktop user.
Action: open Ox, show/hide foundation details and exit. No agent, persistence or plugin runs.
Future actions are not presented as available. Closing has no external work to cancel.

Risks: native dependencies, unavailable display, false positive from treating a state test as a visual test.
OPEN-01: the maintainer confirmed Linux x86_64 as the initial target. Exact toolchain 1.99.1 by the reconciliation request; declared Rust floor remains 1.99.

### Authorized local UI succession

The original no-adapter-execution actor description is historical to the initial
shell. The maintainer-authorized product-local-task-ui delivery adds only controlled
local task fixtures and explicit verification. Existing launch, details and exit
requirements remain; new task behavior is accepted in its own feature. General
agents, sandbox, persisted history and plugin-host UI remain unavailable. This
supersedes no other policy and does not complete F0.

### IPC applicability clarification — 2026-11-17

The product-plugin-host successor recorded in `ea3cf0f:sdd/features/product-bootstrap/plan.md` (D-08) and T011
(`ea3cf0f:sdd/features/product-bootstrap/tasks.md`) supersedes only
the initial absence-of-IPC clause of REQ-11/AC-11. Versioned-contract and explicit
sandbox limits remain applicable. No whole-criterion NOT APPLICABLE verdict or
new operational approval follows. Current bootstrap evidence remains undecided;
the prior observations and criterion text remain in its historical records.
Documentation review: spec, plan/T011 and plugin-host host.rs inspected for this
correction; no new product behavior or IPC execution.

## Requisitos

- REQ-01: Virtual workspace with 16 compilable crates and a single lockfile.
- REQ-02: The Iced window opens, interaction reveals details, and both the button and window close it.
- REQ-03: The ox binary delegates to the library.
- REQ-04: All first-party roots prohibit unsafe; dependencies are evaluated separately.
- REQ-05: External modules without mod.rs.
- REQ-06: Unit and external tests are discovered and executed.
- REQ-07: Acyclic graph and UI separate from domains.
- REQ-08: Distinct identities are used, UUID v7 only for globally persistent entities.
- REQ-09: Evidence with actual inputs and results.
- REQ-10: Governance checkers remain operational.
- REQ-11: Versioned plugin contract; sandbox remains unavailable. The initial absence of IPC is superseded only by the authorized local Unix transport in product-plugin-host.
- REQ-12: Product separate from governance distribution.
- REQ-13: 16 useful contracts and future capabilities explicitly unavailable.

## Critérios de aceitação

- AC-01 → REQ-01: Virtual workspace with 16 compilable crates and a single lockfile; verify with Cargo, inspection or graphical execution according to the plan. (herdado)
- AC-02 → REQ-02: The Iced window opens, interaction reveals details, and both the button and window close it; verify with Cargo, inspection or graphical execution according to the plan. (herdado)
- AC-03 → REQ-03: The ox binary delegates to the library; verify with Cargo, inspection or graphical execution according to the plan. (herdado)
- AC-04 → REQ-04: All first-party roots prohibit unsafe; dependencies are evaluated separately; verify with Cargo, inspection or graphical execution according to the plan. (herdado)
- AC-05 → REQ-05: External modules without mod.rs; verify with Cargo, inspection or graphical execution according to the plan. (herdado)
- AC-06 → REQ-06: Unit and external tests are discovered and executed; verify with Cargo, inspection or graphical execution according to the plan. (herdado)
- AC-07 → REQ-07: Acyclic graph and UI separate from domains; verify with Cargo, inspection or graphical execution according to the plan. (herdado)
- AC-08 → REQ-08: Distinct identities are used, UUID v7 only for globally persistent entities; verify with Cargo, inspection or graphical execution according to the plan. (herdado)
- AC-09 → REQ-09: Evidence with actual inputs and results; verify with Cargo, inspection or graphical execution according to the plan. (herdado)
- AC-10 → REQ-10: Governance checkers remain operational; verify with Cargo, inspection or graphical execution according to the plan. (herdado)
- AC-11 → REQ-11: Verify the versioned plugin contract and explicit absence of sandbox; local IPC is scoped and accepted independently in product-plugin-host, not inferred from bootstrap acceptance. (herdado)
- AC-12 → REQ-12: Product separate from governance distribution; verify with Cargo, inspection or graphical execution according to the plan. (herdado)
- AC-13 → REQ-13: 16 useful contracts and future capabilities explicitly unavailable; verify with Cargo, inspection or graphical execution according to the plan. (herdado)

## Estado atual

| AC | Estado | Decidido por (task) | Data |
|---|---|---|---|
| AC-01 | INCONCLUSIVE | modelo anterior (herdado) | ≤ 2026-11-23 |
| AC-02 | APPROVED | modelo anterior (herdado) | ≤ 2026-11-23 |
| AC-03 | INCONCLUSIVE | modelo anterior (herdado) | ≤ 2026-11-23 |
| AC-04 | INCONCLUSIVE | modelo anterior (herdado) | ≤ 2026-11-23 |
| AC-05 | INCONCLUSIVE | modelo anterior (herdado) | ≤ 2026-11-23 |
| AC-06 | INCONCLUSIVE | modelo anterior (herdado) | ≤ 2026-11-23 |
| AC-07 | INCONCLUSIVE | modelo anterior (herdado) | ≤ 2026-11-23 |
| AC-08 | INCONCLUSIVE | modelo anterior (herdado) | ≤ 2026-11-23 |
| AC-09 | INCONCLUSIVE | modelo anterior (herdado) | ≤ 2026-11-23 |
| AC-10 | INCONCLUSIVE | modelo anterior (herdado) | ≤ 2026-11-23 |
| AC-11 | INCONCLUSIVE | modelo anterior (herdado) | ≤ 2026-11-23 |
| AC-12 | INCONCLUSIVE | modelo anterior (herdado) | ≤ 2026-11-23 |
| AC-13 | INCONCLUSIVE | modelo anterior (herdado) | ≤ 2026-11-23 |

## Limites e questões abertas

- Current successor: F0 OPEN. Historical limitations below describe their original observations. Full native journey, GUI/frame/CPU adopted limits and instrumented GUI intermittency remain unresolved; see current report. No persistence/distribution/remote-agent implementation or commits.
- Controlled local fixtures only; no sandbox, remote agents, persistent history or F0 completion.
- Refresh is explicit; displayed acceptance is as of its observation time. Engine history is bounded to 32 observations.
- Direct-child supervision only; graceful close waits for work; forced application kill and process descendants are outside this guarantee.
- Native observation is reused only after production input/binary comparison; X11 is a separate temporary-server result, not main-session repair.
- Some user _new screenshots were unavailable when archival was attempted; direct visual review and explicit human replies are retained.
- Verification responsiveness/closing combines worker ownership review and Engine/reducer tests with actual fast graphical verification; no slow-verification graphical capture or numerical latency SLO claimed.
- 2026-11-01 technical gate reexamination: unchanged product/metadata evidence reused by new review; full 42-test suite and five exported methods executed. Exact prior envelope retained.
- 2026-11-19 R3: only AC-02 reaccepted for the identified current X11 observation. Historical environments, failures and other unverified criteria remain unchanged; hashbrown and other task-level blockers remain.
