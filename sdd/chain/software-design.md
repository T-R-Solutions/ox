---
skill: software-design
skill_path: .codex/skills/software-design/SKILL.md
bridge_version: 1
---
# SDD bridge: software-design

## Selection

Use for: Local responsibility, interface or refactoring.
Do not select for: System boundary selection without requirements.
Read the actual skill before use. Its technical scope/procedure remains authoritative
for the method; this bridge only maps that method to project artifacts. Presence here
does not activate it. Record the selected bridge and reason in the feature plan.

## Inputs and contributions

| Artifact | Required input / contribution |
|---|---|
| Constitution | Read the project's existing principles and permissions; introduce no skill-specific product policy automatically. |
| Spec | Establish behavior to preserve, intentional contract changes and failure effects. Proposed criteria require a concrete scenario and an oracle, not invented universal thresholds. |
| Plan / ADR | Resolve responsibility/interface alternatives, coupling and migration costs. Link the requirement, decision and risk IDs. |
| Tasks | Refactor incrementally and test public behavior plus error/cleanup effects. Name affected files, dependencies, actual tools and completion checks. |
| Evidence / convergence | Return changes, findings, observed results, criterion IDs and residual limits. Separate structural checks, semantic review, executed tests and comparative effectiveness. |

## Conditional handoff

Optional specialist: `software-testing`.
Technical question: “Which observable error and cleanup effects must the refactor preserve?”
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
