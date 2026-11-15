---
skill: performance-engineering
skill_path: .codex/skills/performance-engineering/SKILL.md
bridge_version: 1
---
# SDD bridge: performance-engineering

## Selection

Use for: Measured cost, slowdown or capacity question.
Do not select for: Speculative optimization during unrelated work.
Read the actual skill before use. Its technical scope/procedure remains authoritative
for the method; this bridge only maps that method to project artifacts. Presence here
does not activate it. Record the selected bridge and reason in the feature plan.

## Inputs and contributions

| Artifact | Required input / contribution |
|---|---|
| Constitution | Read the project's existing principles and permissions; introduce no skill-specific product policy automatically. |
| Spec | Establish cost metric, workload, input scale and approved performance criterion. Proposed criteria require a concrete scenario and an oracle, not invented universal thresholds. |
| Plan / ADR | Resolve baseline, measurement method, confounders and profiling alternatives. Link the requirement, decision and risk IDs. |
| Tasks | Measure before/after under comparable conditions and verify equivalent results. Name affected files, dependencies, actual tools and completion checks. |
| Evidence / convergence | Return changes, findings, observed results, criterion IDs and residual limits. Separate structural checks, semantic review, executed tests and comparative effectiveness. |

## Conditional handoff

Optional specialist: `reliability-engineering`.
Technical question: “What admission and cancellation policy bounds unfinished work?”
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
