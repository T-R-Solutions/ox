---
skill: code-context-engineering
skill_path: .codex/skills/code-context-engineering/SKILL.md
bridge_version: 1
---

# SDD bridge: code-context-engineering

## Selection

Use for: Indexing/invalidators, code search, AST/LSP analysis, context selection, caching, freshness and retrieval evidence.

Do not select for: generic document RAG without code; ai-engineering covers that. Do not treat an AST as proof of call resolution.

## Inputs and contributions

Known inputs: repository/snapshot, ignore rules, supported languages, symbol model, resource budgets and queries. Do not infer missing capabilities or permissions.

| Artifact | Required input / contribution |
|---|---|
| Constitution | Reconcile existing authorization, data residency, safety and project constraints; add no product policy automatically. |
| Spec | Define scoped, observable behavior and rejected cases. Queries return context bound to an identifiable repository version. |
| Plan / ADR | Compare alternatives, contract versions and failure modes; link REQ, AC, D and R IDs; preserve authority boundaries. Always-useful path/text index, incremental parser per language and LSP only when justified. |
| Tasks | Name actual files, fixtures, tools, real permissions, failure injections and completion checks. Define optional LSP integration and evidence semantics. |
| Evidence / convergence | Identify observed implementation/oracle/configuration versions and hashes, test results, unsatisfied criteria and explicit limits. versioned index, search APIs, ranking, provenance, incremental invalidation, accuracy/cost tests and degradation |

## Conditional handoff

Optional specialist: `ai-engineering`. Specific unresolved question: “Does retrieval actually improve task success compared with simple search?” Consult only if actually present and needed. Supply relevant IDs, known facts, unknowns, permission scope, versions and required evidence. Do not install or load a whole dependency chain. Continue independent work and mark blocked criteria unverified.

## Completion and authority

Shared routing, authorization, outcome states and documentation closure follow
[workflow](../workflow.md) and [evidence](../evidence.md). This bridge maps a
selected method to artifacts; it neither activates skills nor changes permissions.
For reuse elsewhere, keep these shared contracts and adapt skill_path to that project.
