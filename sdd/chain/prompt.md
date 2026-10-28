---
skill: prompt
skill_path: .codex/skills/prompt/SKILL.md
bridge_version: 1
---
# SDD bridge: prompt

Copy this file into the destination sdd/chain directory. Set `skill_path` to the
project-relative path of the copied SKILL.md. This document is an optional bridge,
not a skill implementation or an instruction to install other skills.

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

Read only relevant project artifacts, changed surfaces and constraints. Discover
available tools/versions before execution. Missing tools leave the affected criterion
unverified; they do not permit changing the requirement to make it pass.

## Conditional handoff

Optional specialist: `application-security`.
Technical question: “Can retrieved content cause a tool action outside the caller authority?”
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

## Perfil condicional do projeto

Pedido de criar ou revisar um prompt como artefato; não qualquer tarefa com IA. Disponibilidade não significa seleção, consulta ou uso.
