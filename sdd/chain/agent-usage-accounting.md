---
skill: agent-usage-accounting
skill_path: .codex/skills/agent-usage-accounting/SKILL.md
bridge_version: 1
---

# SDD bridge: agent-usage-accounting

Copy this file to the destination project's `sdd/chain/` and set `skill_path` to the actual project-relative path of the skill entry. This is an optional bridge and does not install or activate the skill.

## Selection

Use for: Token counts by chat/day/project, multi-model costs, context windows, caching, prices and usage reports.

Do not select for: Do not select for generic CPU/RAM instrumentation; use observability-and-diagnostics. Do not confuse functional progress with context consumption.

Select only when the concrete feature has this specialized question. Read the actual skill; record its path/version and selection reason in the plan. A bridge reference does not recursively select other skills.

## Inputs and contributions

Known inputs: provider/agent events, token/cache types, versioned rates, intervals, session/task identity. Do not infer missing capabilities or permissions.

| Artifact | Required input / contribution |
|---|---|
| Constitution | Reconcile existing authorization, data residency, safety and project constraints; add no product policy automatically. |
| Spec | Define scoped, observable behavior and rejected cases. Records distinguish provider-supplied measurements, derivations and estimates. |
| Plan / ADR | Compare alternatives, contract versions and failure modes; link REQ, AC, D and R IDs; preserve authority boundaries. Immutable usage-event ledger plus computed views; do not mutate measured events. |
| Tasks | Name actual files, fixtures, tools, real permissions, failure injections and completion checks. Create fixtures with caching, replay, partial streaming and missing pricing. |
| Evidence / convergence | Identify observed implementation/oracle/configuration versions and hashes, test results, unsatisfied criteria and explicit limits. usage ledger schema, duplicate and gap rules, period views, provenance and estimate accuracy |

## Conditional handoff

Optional specialist: `observability-and-diagnostics`. Specific unresolved question: “Does the usage event arrive in full, and can it be correlated without violating privacy?” Consult only if actually present and needed. Supply relevant IDs, known facts, unknowns, permission scope, versions and required evidence. Do not install or load a whole dependency chain. Continue independent work and mark blocked criteria unverified.

## Completion and authority

Use the destination SDD's states: APPROVED, REJECTED, UNVERIFIED, INCONCLUSIVE, NOT APPLICABLE (with justification). A mock or document is not execution evidence. Record freshness of inputs and source of each observation. Spec owns behavior; plan/ADRs own decisions; tasks own work; this bridge only connects the skill to those artifacts.
