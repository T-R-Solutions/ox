# Spec — foundation

Spec viva da capacidade `foundation`. Migrada em 2026-11-23 da feature `product-foundation` do modelo
anterior (título original: "Ox product foundation — phase transition"). Texto original preservado; ACs marcados
`(herdado)` mantêm o estado registrado até 2026-11-23, mas a evidência bruta foi removida e
não sustenta nova aprovação. A task que tocar a capacidade reescreve o AC na forma
`| método: … | esperado: …` e o reavalia. As limitações técnicas foram mantidas; as notas de
controle de evidência do modelo anterior, não.

## O quê e por quê

Actor: maintainer and authorized agents. Request: examine and implement transition
plan v1.0, correcting its SDD integration where necessary.
Feature scope: development contract, SDD-integrated library,
checkers and governance distribution. Does not deliver crates or an application.

Reject: application approval based on documentation, updating hashes to
recycle old results, changes to POL-01..10, installation/publication based on
a roadmap mention. The local route remains available according to sdd/workflow.md.
Textual gates detect representative regressions without proving the semantics of
arbitrary paraphrases. This feature accepts only the transition.

### Current applicability note — 2026-11-01

The literal requirement to keep all 36 skill scenarios UNVERIFIED records the preparatory baseline, not their current observed state. ADR technical-acceptance (removida em 2026-11-23; ver docs/decisions/sdd-model.md) explicitly supersedes product-foundation AC-03 and the transition decision; skill-consumer-validation records the successor executions. Its named supersession does not expressly enumerate governance-externalization AC-06, governance-layout AC-04 or maintenance-001 AC-04. Those compound legacy gates remain INCONCLUSIVE pending maintainer confirmation of succession scope and any remaining preservation/qualification evidence. No original scenario, historical result or other clause is waived. Current consumer acceptance never transfers to the product. See (evidência removida em 2026-11-23)

## Requisitos

- REQ-01: Record phase and scope in the context authority, preserving effective permissions.
- REQ-02: Keep AGENTS as the entry point and integrate capabilities with SDD without duplicating policies in skills.
- REQ-03: Separate product acceptance, skill authoring and historical observations.
- REQ-04: Identify and qualify distribution exclusively as governance.
- REQ-05: Preserve a recoverable baseline and reexamine evidence dependent on changed inputs.

## Critérios de aceitação

- AC-01 → REQ-01: Context records implementation-foundation and not-yet-implemented; authorities allow bounded development and do not grant unrestricted execution. (herdado)
- AC-02 → REQ-02: AGENTS refers to authorities; the integration guide distinguishes selection, consultation and use, local/full routes and bridge contributions; 29 skills, 29 bridges and SDD 1.3.0 remain intact. (herdado)
- AC-03 → REQ-03: product-foundation has its own criteria; the skills' 36 technical scenarios remain UNVERIFIED and mutations promoting them are rejected. (herdado)
- AC-04 → REQ-04: ZIP ox-governance.zip and receipts declare governance without the product; the manifest excludes Cargo/crates and independent extraction passes the five qualification commands. (herdado)
- AC-05 → REQ-05: Checks and adversarial tests pass; immutable history and baseline retain their bytes; affected observations are archived and replaced by new review/execution with schema 2 and current inputs. (herdado)

## Estado atual

| AC | Estado | Decidido por (task) | Data |
|---|---|---|---|
| AC-01 | INCONCLUSIVE | modelo anterior (herdado) | ≤ 2026-11-23 |
| AC-02 | INCONCLUSIVE | modelo anterior (herdado) | ≤ 2026-11-23 |
| AC-03 | INCONCLUSIVE | modelo anterior (herdado) | ≤ 2026-11-23 |
| AC-04 | INCONCLUSIVE | modelo anterior (herdado) | ≤ 2026-11-23 |
| AC-05 | INCONCLUSIVE | modelo anterior (herdado) | ≤ 2026-11-23 |

## Limites e questões abertas

- Current successor: F0 OPEN. Historical limitations below describe their original observations. Full native journey, GUI/frame/CPU adopted limits and instrumented GUI intermittency remain unresolved; see current report. No persistence/distribution/remote-agent implementation or commits.
- Acceptance restricted to governance/authoring; no Rust compilation, Iced integration or product effectiveness.
- Executor review is not independent human review; historical trials were not rerun.
- The skills' 36 technical scenarios remain UNVERIFIED.
