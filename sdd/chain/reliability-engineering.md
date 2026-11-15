---
skill: reliability-engineering
skill_path: .codex/skills/reliability-engineering/SKILL.md
bridge_version: 1
---
# SDD bridge: reliability-engineering

## Selection

Use for: Overload, leak, cancellation or recovery.
Do not select for: Small pure-function edit.
Read the actual skill before use. Its technical scope/procedure remains authoritative
for the method; this bridge only maps that method to project artifacts. Presence here
does not activate it. Record the selected bridge and reason in the feature plan.

## Inputs and contributions

| Artifact | Required input / contribution |
|---|---|
| Constitution | Read the project's existing principles and permissions; introduce no skill-specific product policy automatically. |
| Spec | Establish failure behavior, resource bounds, recovery and workload-specific objectives. Proposed criteria require a concrete scenario and an oracle, not invented universal thresholds. |
| Plan / ADR | Resolve ownership, admission/cancellation, fault propagation and recovery alternatives. Link the requirement, decision and risk IDs. |
| Tasks | Exercise failure/overload/cleanup and observe independent resource and recovery outcomes. Name affected files, dependencies, actual tools and completion checks. |
| Evidence / convergence | Return changes, findings, observed results, criterion IDs and residual limits. Separate structural checks, semantic review, executed tests and comparative effectiveness. |

## Conditional handoff

Optional specialist: `performance-engineering`.
Technical question: “Does retained work grow after arrivals stop and cleanup completes?”
Only request this handoff if the question remains unresolved and that skill is
available. Supply task/requirement IDs, affected surface, known facts, hypotheses,
constraints, required evidence and existing permission scope. Never recursively
activate a dependency chain or claim work by an absent skill. Continue independent
work; record a gap when the missing capability is material to acceptance.

## Completion and authority

Shared routing, authorization, outcome states and documentation closure follow
[workflow](../workflow.md) and [evidence](../evidence.md). This bridge maps a
selected method to artifacts; it neither activates skills nor changes permissions.
For reuse elsewhere, keep these shared contracts and adapt skill_path to that project.
