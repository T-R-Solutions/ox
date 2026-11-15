---
skill: code-context-engineering
skill_path: .codex/skills/code-context-engineering/SKILL.md
bridge_version: 1
---

# SDD bridge: code-context-engineering

Copy this file to the destination project's `sdd/chain/` and set `skill_path` to the actual project-relative path of the skill entry. This is an optional bridge and does not install or activate the skill.

## Selection

Use for: Indexing/invalidators, code search, AST/LSP analysis, context selection, caching, freshness and retrieval evidence.

Do not select for: Do not select for generic document RAG without code; ai-engineering covers that. Do not treat an AST as proof of call resolution.

Select only when the concrete feature has this specialized question. Read the actual skill; record its path/version and selection reason in the plan. A bridge reference does not recursively select other skills.

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

Use the destination SDD's states: APPROVED, REJECTED, UNVERIFIED, INCONCLUSIVE, NOT APPLICABLE (with justification). A mock or document is not execution evidence. Record freshness of inputs and source of each observation. Spec owns behavior; plan/ADRs own decisions; tasks own work; this bridge only connects the skill to those artifacts.
