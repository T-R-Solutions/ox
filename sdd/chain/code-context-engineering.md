---
skill: code-context-engineering
skill_path: .codex/skills/code-context-engineering/SKILL.md
bridge_version: 1
---

# SDD bridge: code-context-engineering

Copy this file to the destination project's `sdd/chain/` and set `skill_path` to the actual project-relative path of the skill entry. This is an optional bridge and does not install or activate the skill.

## Selection

Use for: Indexação/invalidadores, busca por código, análise AST/LSP, seleção contextual, cache, freshness e evidência de recuperação.

Do not select for: Não selecionar para RAG genérico de documentos sem código; ai-engineering cobre isso. Não tratar AST como prova de resolução de chamadas.

Select only when the concrete feature has this specialized question. Read the actual skill; record its path/version and selection reason in the plan. A bridge reference does not recursively select other skills.

## Inputs and contributions

Known inputs: repositório/snapshot, regras de ignore, línguas suportadas, modelo de símbolos, orçamentos de recurso e consultas. Do not infer missing capabilities or permissions.

| Artifact | Required input / contribution |
|---|---|
| Constitution | Reconcile existing authorization, data residency, safety and project constraints; add no product policy automatically. |
| Spec | Define scoped, observable behavior and rejected cases. Consultas retornam contexto ligado a uma versão identificável do repositório. |
| Plan / ADR | Compare alternatives, contract versions and failure modes; link REQ, AC, D and R IDs; preserve authority boundaries. Índice de caminhos/texto sempre útil, parser incremental por linguagem e LSP somente quando justificado. |
| Tasks | Name actual files, fixtures, tools, real permissions, failure injections and completion checks. Definir integração opcional LSP e semântica de evidência. |
| Evidence / convergence | Identify observed implementation/oracle/configuration versions and hashes, test results, unsatisfied criteria and explicit limits. índice versionado, APIs de busca, ranking, proveniência, invalidação incremental, testes de precisão/custo e degradação |

## Conditional handoff

Optional specialist: `ai-engineering`. Specific unresolved question: “A recuperação realmente eleva a taxa de sucesso da tarefa em relação a uma busca simples?” Consult only if actually present and needed. Supply relevant IDs, known facts, unknowns, permission scope, versions and required evidence. Do not install or load a whole dependency chain. Continue independent work and mark blocked criteria unverified.

## Completion and authority

Use the destination SDD's states: APROVADO, REPROVADO, NÃO VERIFICADO, INCONCLUSIVO, NÃO APLICÁVEL (with justification). A mock or document is not execution evidence. Record freshness of inputs and source of each observation. Spec owns behavior; plan/ADRs own decisions; tasks own work; this bridge only connects the skill to those artifacts.
