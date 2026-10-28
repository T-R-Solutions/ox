---
skill: autonomous-verification-engineering
skill_path: .codex/skills/autonomous-verification-engineering/SKILL.md
bridge_version: 1
---

# SDD bridge: autonomous-verification-engineering

Copy this file to the destination project's `sdd/chain/` and set `skill_path` to the actual project-relative path of the skill entry. This is an optional bridge and does not install or activate the skill.

## Selection

Use for: Sistemas que aprovam/reprovam entregas de agentes; evidências, critérios, gates, execução autônoma e risco de aceitação falsa.

Do not select for: Não usar para apenas criar testes unitários ou investigar flaky tests; software-testing é responsável por esses métodos. Não produzir “score de confiança” sem calibração.

Select only when the concrete feature has this specialized question. Read the actual skill; record its path/version and selection reason in the plan. A bridge reference does not recursively select other skills.

## Inputs and contributions

Known inputs: critérios normativos, snapshots de código, testes/verificadores autorizados, risco da mudança, política de aprovação. Do not infer missing capabilities or permissions.

| Artifact | Required input / contribution |
|---|---|
| Constitution | Reconcile existing authorization, data residency, safety and project constraints; add no product policy automatically. |
| Spec | Define scoped, observable behavior and rejected cases. Todo veredicto está vinculado a critério explícito, método e snapshot dos inputs. |
| Plan / ADR | Compare alternatives, contract versions and failure modes; link REQ, AC, D and R IDs; preserve authority boundaries. Estados separados: pendente, aprovado, reprovado, inconclusivo, não aplicável justificado. |
| Tasks | Name actual files, fixtures, tools, real permissions, failure injections and completion checks. Criar fixtures com testes falsos, falhas, skips e mudanças após validação. |
| Evidence / convergence | Identify observed implementation/oracle/configuration versions and hashes, test results, unsatisfied criteria and explicit limits. modelo de gates, status auditáveis, vínculo requisito-evidência-snapshot, separação implementação/oráculo, procedimentos de replay |

## Conditional handoff

Optional specialist: `software-testing`. Specific unresolved question: “O oráculo escolhido realmente falha quando introduzimos o defeito representativo?” Consult only if actually present and needed. Supply relevant IDs, known facts, unknowns, permission scope, versions and required evidence. Do not install or load a whole dependency chain. Continue independent work and mark blocked criteria unverified.

## Completion and authority

Use the destination SDD's states: APROVADO, REPROVADO, NÃO VERIFICADO, INCONCLUSIVO, NÃO APLICÁVEL (with justification). A mock or document is not execution evidence. Record freshness of inputs and source of each observation. Spec owns behavior; plan/ADRs own decisions; tasks own work; this bridge only connects the skill to those artifacts.
