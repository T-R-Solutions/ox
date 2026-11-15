---
skill: tool-output-engineering
skill_path: .codex/skills/tool-output-engineering/SKILL.md
bridge_version: 1
---

# SDD bridge: tool-output-engineering

## Selection

Use for: Reducing stdout/stderr tokens, command parsers, test summaries, controlled noise suppression, truncation detection.

Do not select for: Do not irreversibly transform audit logs; do not present estimated character reduction as measured savings on the provider bill.

## Inputs and contributions

Known inputs: raw bytes, exit-code metadata, tool format, limits/encoding, retention strategy and budget. Do not infer missing capabilities or permissions.

| Artifact | Required input / contribution |
|---|---|
| Constitution | Reconcile existing authorization, data residency, safety and project constraints; add no product policy automatically. |
| Spec | Define scoped, observable behavior and rejected cases. Each transformed output preserves exit code, error signals and a reference to raw output. |
| Plan / ADR | Compare alternatives, contract versions and failure modes; link REQ, AC, D and R IDs; preserve authority boundaries. Three forms: append-only raw output, normalized structure and compact view. |
| Tasks | Name actual files, fixtures, tools, real permissions, failure injections and completion checks. Build an adversarial corpus and differential tests with authorized real output. |
| Evidence / convergence | Identify observed implementation/oracle/configuration versions and hashes, test results, unsatisfied criteria and explicit limits. preserved raw output, structured events, summaries flagging loss/truncation, comparable measurements |

## Conditional handoff

Optional specialist: `application-security`. Specific unresolved question: “Can stdout text be mistaken for an instruction or authorized tool input?” Consult only if actually present and needed. Supply relevant IDs, known facts, unknowns, permission scope, versions and required evidence. Do not install or load a whole dependency chain. Continue independent work and mark blocked criteria unverified.

## Completion and authority

Shared routing, authorization, outcome states and documentation closure follow
[workflow](../workflow.md) and [evidence](../evidence.md). This bridge maps a
selected method to artifacts; it neither activates skills nor changes permissions.
For reuse elsewhere, keep these shared contracts and adapt skill_path to that project.
