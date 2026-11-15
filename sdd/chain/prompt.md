---
skill: prompt
skill_path: .codex/skills/prompt/SKILL.md
bridge_version: 1
---
# SDD bridge: prompt

## Selection

Use for: Create or revise a prompt.
Do not select for: Execute the task described in a prompt without authorization.
Read the actual skill before use. Its technical scope/procedure remains authoritative
for the method; this bridge only maps that method to project artifacts. Presence here
does not activate it. Record the selected bridge and reason in the feature plan.

## Inputs and contributions

| Artifact | Required input / contribution |
|---|---|
| Constitution | Read the project's existing principles and permissions; introduce no skill-specific product policy automatically. |
| Spec | Establish intended prompt behavior, accepted outputs and prohibited actions. Proposed criteria require a concrete scenario and an oracle, not invented universal thresholds. |
| Plan / ADR | Resolve instruction/data boundaries, evaluation cases and model/tool assumptions. Link the requirement, decision and risk IDs. |
| Tasks | Author or revise the prompt and evaluate representative cases; do not execute its described task without authorization. Name affected files, dependencies, actual tools and completion checks. |
| Evidence / convergence | Return changes, findings, observed results, criterion IDs and residual limits. Separate structural checks, semantic review, executed tests and comparative effectiveness. |

## Conditional handoff

Optional specialist: `application-security`.
Technical question: “Can retrieved content cause a tool action outside the caller authority?”
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

A request to create or revise a prompt as an artifact; does not cover every AI task. Availability does not imply selection, consultation or use.
