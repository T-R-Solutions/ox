---
skill: workspace-integrity-engineering
skill_path: .codex/skills/workspace-integrity-engineering/SKILL.md
bridge_version: 1
---

# SDD bridge: workspace-integrity-engineering

Copy this file to the destination project's `sdd/chain/` and set `skill_path` to the actual project-relative path of the skill entry. This is an optional bridge and does not install or activate the skill.

## Selection

Use for: Edição concorrente, watcher, atomicidade de escrita, Git/worktree, rollback, caminhos e links simbólicos.

Do not select for: Não ativar para adicionar uma coluna SQLite ou revisar formato de UI; database-engineering/design-system. Não reimplementar Git apenas para satisfazer conveniência.

Select only when the concrete feature has this specialized question. Read the actual skill; record its path/version and selection reason in the plan. A bridge reference does not recursively select other skills.

## Inputs and contributions

Known inputs: árvore do workspace, política de exclusões, raízes autorizadas, plano de edições, Git state, eventos do SO. Do not infer missing capabilities or permissions.

| Artifact | Required input / contribution |
|---|---|
| Constitution | Reconcile existing authorization, data residency, safety and project constraints; add no product policy automatically. |
| Spec | Define scoped, observable behavior and rejected cases. Todas as mudanças em arquivos respeitam raiz autorizada e versão observada. |
| Plan / ADR | Compare alternatives, contract versions and failure modes; link REQ, AC, D and R IDs; preserve authority boundaries. Gravação staging+rename quando semântica da plataforma permitir; fallback documentado. |
| Tasks | Name actual files, fixtures, tools, real permissions, failure injections and completion checks. Implementar testes em diretórios temporários e com concorrência. |
| Evidence / convergence | Identify observed implementation/oracle/configuration versions and hashes, test results, unsatisfied criteria and explicit limits. transações de arquivo com validação, prevenção de perda, trilhas de alteração, estratégia de snapshot e recuperação |

## Conditional handoff

Optional specialist: `application-security`. Specific unresolved question: “Existem caminhos alternativos/symlinks que escapam da raiz concedida ao agente?” Consult only if actually present and needed. Supply relevant IDs, known facts, unknowns, permission scope, versions and required evidence. Do not install or load a whole dependency chain. Continue independent work and mark blocked criteria unverified.

## Completion and authority

Use the destination SDD's states: APROVADO, REPROVADO, NÃO VERIFICADO, INCONCLUSIVO, NÃO APLICÁVEL (with justification). A mock or document is not execution evidence. Record freshness of inputs and source of each observation. Spec owns behavior; plan/ADRs own decisions; tasks own work; this bridge only connects the skill to those artifacts.
