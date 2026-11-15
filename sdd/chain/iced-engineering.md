---
skill: iced-engineering
skill_path: .codex/skills/iced-engineering/SKILL.md
bridge_version: 1
---

# SDD bridge: iced-engineering

## Selection

Use for: Iced code, update/view models, custom widgets, split panes, themes, accessibility and graph visualization.

Do not select for: projects without Iced; do not replace design-review/design-system when deciding visual hierarchy.

## Inputs and contributions

Known inputs: Iced version and features, GUI state, flows, events, size constraints, accessibility and latency. Do not infer missing capabilities or permissions.

| Artifact | Required input / contribution |
|---|---|
| Constitution | Reconcile existing authorization, data residency, safety and project constraints; add no product policy automatically. |
| Spec | Define scoped, observable behavior and rejected cases. The UI does not block on processes, search, indexing or agent events. |
| Plan / ADR | Compare alternatives, contract versions and failure modes; link REQ, AC, D and R IDs; preserve authority boundaries. Message/Update/View model with explicit state and tasks outside rendering. |
| Tasks | Name actual files, fixtures, tools, real permissions, failure injections and completion checks. Create a UI harness and fixtures for states/loading/events. |
| Evidence / convergence | Identify observed implementation/oracle/configuration versions and hashes, test results, unsatisfied criteria and explicit limits. components/update contracts, testable UI, empty/error/loading states, rendering budget and benchmark |

## Conditional handoff

Optional specialist: `design-system`. Specific unresolved question: “Does the reusable component preserve the defined tokens, variants, states and interaction contract?” Consult only if actually present and needed. Supply relevant IDs, known facts, unknowns, permission scope, versions and required evidence. Do not install or load a whole dependency chain. Continue independent work and mark blocked criteria unverified.

## Completion and authority

Shared routing, authorization, outcome states and documentation closure follow
[workflow](../workflow.md) and [evidence](../evidence.md). This bridge maps a
selected method to artifacts; it neither activates skills nor changes permissions.
For reuse elsewhere, keep these shared contracts and adapt skill_path to that project.
