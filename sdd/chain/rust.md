---
skill: rust
skill_path: .codex/skills/rust/SKILL.md
bridge_version: 1
---
# SDD bridge: rust

## Selection

Use for: Rust implementation, API design, debugging, refactoring or review, including
ownership, error handling, unsafe boundaries and synchronization.
Do not select for: Unrelated language or product policy.
Read the actual skill before use. Its technical scope/procedure remains authoritative
for the method; this bridge only maps that method to project artifacts. Presence here
does not activate it. Record the selected bridge and reason in the feature plan.

## Inputs and contributions

| Artifact | Required input / contribution |
|---|---|
| Constitution | Read the project's existing principles and permissions; introduce no skill-specific product policy automatically. |
| Spec | Establish observable safety and error invariants at Rust boundaries. Proposed criteria require a concrete scenario and an oracle, not invented universal thresholds. |
| Plan / ADR | Resolve edition/MSRV, ownership, unsafe/FFI justification and synchronization alternatives. Link the requirement, decision and risk IDs. |
| Tasks | Implement the changed rust surface and run supported compiler/tests or concurrency checks. Name affected files, dependencies, actual tools and completion checks. |
| Evidence / convergence | Return changes, findings, observed results, criterion IDs and residual limits. Separate structural checks, semantic review, executed tests and comparative effectiveness. |

## Conditional handoff

Optional specialist: `software-testing`.
Technical question: “Which controlled schedule can falsify the publication invariant?”
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
