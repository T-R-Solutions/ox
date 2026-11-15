---
skill: distributed-systems
skill_path: .codex/skills/distributed-systems/SKILL.md
bridge_version: 1
---
# SDD bridge: distributed-systems

## Selection

Use for: Independent failure domains or delivery guarantees.
Do not select for: Local-only state change.
Read the actual skill before use. Its technical scope/procedure remains authoritative
for the method; this bridge only maps that method to project artifacts. Presence here
does not activate it. Record the selected bridge and reason in the feature plan.

## Inputs and contributions

| Artifact | Required input / contribution |
|---|---|
| Constitution | Read the project's existing principles and permissions; introduce no skill-specific product policy automatically. |
| Spec | Establish consistency, ordering, duplication and partial-failure guarantees. Proposed criteria require a concrete scenario and an oracle, not invented universal thresholds. |
| Plan / ADR | Resolve failure domains, ownership, coordination and delivery alternatives. Link the requirement, decision and risk IDs. |
| Tasks | Exercise lost/delayed/duplicated messages and recovery against explicit invariants. Name affected files, dependencies, actual tools and completion checks. |
| Evidence / convergence | Return changes, findings, observed results, criterion IDs and residual limits. Separate structural checks, semantic review, executed tests and comparative effectiveness. |

## Conditional handoff

Optional specialist: `domain-modeling`.
Technical question: “Which intermediate state is forbidden during cross-node recovery?”
Only request this handoff if the question remains unresolved and that skill is
available. Supply task/requirement IDs, affected surface, known facts, hypotheses,
constraints, required evidence and existing permission scope. Never recursively
activate a dependency chain or claim work by an absent skill. Continue independent
work; record a gap when the missing capability is material to acceptance.

## Completion and authority

Shared routing, authorization and documentation closure follow
[workflow](../workflow.md); outcome states follow [evidence](../evidence.md).
Return every applicable criterion with evidence or its explicit SDD state,
including UNVERIFIED or INCONCLUSIVE where appropriate. The feature spec owns
behavior, plan/ADRs own decisions and tasks organize execution. This bridge maps
the selected method to artifacts without activating skills or expanding permissions.
For reuse elsewhere, keep these contracts and adapt skill_path to that project.

## Conditional project profile

Guarantees across independently failing processes, ordering, replay or synchronization; IPC alone is insufficient. Availability does not imply selection, consultation or use.
