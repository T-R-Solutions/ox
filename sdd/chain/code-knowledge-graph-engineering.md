---
skill: code-knowledge-graph-engineering
skill_path: .codex/skills/code-knowledge-graph-engineering/SKILL.md
bridge_version: 1
---

# SDD bridge: code-knowledge-graph-engineering

Copy this file to the destination project's `sdd/chain/` and set `skill_path` to the actual project-relative path of the skill entry. This is an optional bridge and does not install or activate the skill.

## Selection

Use for: Schema de nós/arestas, provenance, análise de impacto, caminhos, clusters e visualização por subgrafo/densidade.

Do not select for: Não selecionar para fazer um grafo de marketing ou apresentação estática; design-system/design-review. Não substituir compilador/LSP por embeddings.

Select only when the concrete feature has this specialized question. Read the actual skill; record its path/version and selection reason in the plan. A bridge reference does not recursively select other skills.

## Inputs and contributions

Known inputs: identidades estáveis, relações extraídas/inferidas, snapshots, consultas de impacto, limites de cardinalidade e layout. Do not infer missing capabilities or permissions.

| Artifact | Required input / contribution |
|---|---|
| Constitution | Reconcile existing authorization, data residency, safety and project constraints; add no product policy automatically. |
| Spec | Define scoped, observable behavior and rejected cases. Nós/arestas têm tipos, identidade e proveniência ligada ao snapshot. |
| Plan / ADR | Compare alternatives, contract versions and failure modes; link REQ, AC, D and R IDs; preserve authority boundaries. Modelo tipado de nós/arestas com IDs estáveis e fonte de verdade por snapshot. |
| Tasks | Name actual files, fixtures, tools, real permissions, failure injections and completion checks. Testar invalidação incremental e diferenciar inferências. |
| Evidence / convergence | Identify observed implementation/oracle/configuration versions and hashes, test results, unsatisfied criteria and explicit limits. contrato de grafo versionado, consultas com limites, rastreabilidade de arestas, políticas de invalidação, modos estruturais/densos |

## Conditional handoff

Optional specialist: `code-context-engineering`. Specific unresolved question: “A origem da aresta pode ser verificada no snapshot de código indexado?” Consult only if actually present and needed. Supply relevant IDs, known facts, unknowns, permission scope, versions and required evidence. Do not install or load a whole dependency chain. Continue independent work and mark blocked criteria unverified.

## Completion and authority

Use the destination SDD's states: APROVADO, REPROVADO, NÃO VERIFICADO, INCONCLUSIVO, NÃO APLICÁVEL (with justification). A mock or document is not execution evidence. Record freshness of inputs and source of each observation. Spec owns behavior; plan/ADRs own decisions; tasks own work; this bridge only connects the skill to those artifacts.
