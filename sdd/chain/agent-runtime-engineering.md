---
skill: agent-runtime-engineering
skill_path: .codex/skills/agent-runtime-engineering/SKILL.md
bridge_version: 1
---

# SDD bridge: agent-runtime-engineering

Copy this file to the destination project's `sdd/chain/` and set `skill_path` to the actual project-relative path of the skill entry. This is an optional bridge and does not install or activate the skill.

## Selection

Use for: ACP/CLI adapter, process supervisor, session/task state, parallel agents, cancellation and resumption.

Do not select for: Do not select for standalone prompts, model comparison or response quality evaluation without effects; use ai-engineering.

Select only when the concrete feature has this specialized question. Read the actual skill; record its path/version and selection reason in the plan. A bridge reference does not recursively select other skills.

## Inputs and contributions

Known inputs: supported protocols, executables/versioning, permission policy, resources, session semantics, events and limits. Do not infer missing capabilities or permissions.

| Artifact | Required input / contribution |
|---|---|
| Constitution | Reconcile existing authorization, data residency, safety and project constraints; add no product policy automatically. |
| Spec | Define scoped, observable behavior and rejected cases. Sessions and tasks have legal states, stable identifiers and rejected transitions. |
| Plan / ADR | Compare alternatives, contract versions and failure modes; link REQ, AC, D and R IDs; preserve authority boundaries. Standard adapter (e.g. ACP) with agent-specific fallback; version capabilities. |
| Tasks | Name actual files, fixtures, tools, real permissions, failure injections and completion checks. Create controllable fakes and minimal ACP/CLI integration. |
| Evidence / convergence | Identify observed implementation/oracle/configuration versions and hashes, test results, unsatisfied criteria and explicit limits. state machine, testable adapters, ordered events, process controls, cancellation handling, policy integration |

## Conditional handoff

Optional specialist: `reliability-engineering`. Specific unresolved question: “How can orphaned processes, duplicate effects and event loss be bounded during failures?” Consult only if actually present and needed. Supply relevant IDs, known facts, unknowns, permission scope, versions and required evidence. Do not install or load a whole dependency chain. Continue independent work and mark blocked criteria unverified.

## Completion and authority

Use the destination SDD's states: APPROVED, REJECTED, UNVERIFIED, INCONCLUSIVE, NOT APPLICABLE (with justification). A mock or document is not execution evidence. Record freshness of inputs and source of each observation. Spec owns behavior; plan/ADRs own decisions; tasks own work; this bridge only connects the skill to those artifacts.
