---
skill: software-testing
skill_path: .codex/skills/software-testing/SKILL.md
bridge_version: 1
---
# SDD bridge: software-testing

Copy this file into the destination sdd/chain directory. Set `skill_path` to the
project-relative path of the copied SKILL.md. This document is an optional bridge,
not a skill implementation or an instruction to install other skills.

## Selection

Use for: Test strategy, regression or oracle quality.
Do not select for: Mechanical edit with no behavioral risk.
Read the actual skill before use. Its technical scope/procedure remains authoritative
for the method; this bridge only maps that method to project artifacts. Presence here
does not activate it. Record the selected bridge and reason in the feature plan.

## Inputs and contributions

| Artifact | Required input / contribution |
|---|---|
| Constitution | Read the project's existing principles and permissions; introduce no skill-specific product policy automatically. |
| Spec | Establish observable scenarios, rejected transitions and independent acceptance oracles. Proposed criteria require a concrete scenario and an oracle, not invented universal thresholds. |
| Plan / ADR | Resolve risk-based test scope, doubles, integration boundaries and known omissions. Link the requirement, decision and risk IDs. |
| Tasks | Implement tests, prove targeted defect sensitivity and report failures/skips separately. Name affected files, dependencies, actual tools and completion checks. |
| Evidence / convergence | Return changes, findings, observed results, criterion IDs and residual limits. Separate structural checks, semantic review, executed tests and comparative effectiveness. |

Read only relevant project artifacts, changed surfaces and constraints. Discover
available tools/versions before execution. Missing tools leave the affected criterion
unverified; they do not permit changing the requirement to make it pass.

## Conditional handoff

Optional specialist: `domain-modeling`.
Technical question: “Which rejected transition is required by the business invariant?”
Only request this handoff if the question remains unresolved and that skill is
available. Supply task/requirement IDs, affected surface, known facts, hypotheses,
constraints, required evidence and existing permission scope. Never recursively
activate a dependency chain or claim work by an absent skill. Continue independent
work; record a gap when the missing capability is material to acceptance.

## Completion and authority

Use the outcome vocabulary defined by the destination SDD. Return every applicable
criterion with its evidence or explicit pending/inconclusive status. The feature's
spec defines behavior; plan/ADRs define decisions; tasks define executable work.
This bridge cannot override those artifacts or expand authorization. Changes to
product rules belong in their authoritative artifact, not in this bridge.
