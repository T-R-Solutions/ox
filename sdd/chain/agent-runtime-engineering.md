---
skill: agent-runtime-engineering
skill_path: .codex/skills/agent-runtime-engineering/SKILL.md
bridge_version: 1
---

# SDD bridge: agent-runtime-engineering

Copy this file to the destination project's `sdd/chain/` and set `skill_path` to the actual project-relative path of the skill entry. This is an optional bridge and does not install or activate the skill.

## Selection

Use for: Adaptador ACP/CLI, supervisor de processos, estado de sessão/tarefa, paralelismo entre agentes, cancelamento e retomada.

Do not select for: Não selecionar para prompt isolado, comparação de modelos ou avaliação de qualidade de respostas sem efeitos; usar ai-engineering.

Select only when the concrete feature has this specialized question. Read the actual skill; record its path/version and selection reason in the plan. A bridge reference does not recursively select other skills.

## Inputs and contributions

Known inputs: protocolos suportados, executáveis/versionamento, política de permissão, recursos, semântica de sessão, eventos e limites. Do not infer missing capabilities or permissions.

| Artifact | Required input / contribution |
|---|---|
| Constitution | Reconcile existing authorization, data residency, safety and project constraints; add no product policy automatically. |
| Spec | Define scoped, observable behavior and rejected cases. Sessões e tarefas têm estados legais, identificadores estáveis e transições rejeitadas. |
| Plan / ADR | Compare alternatives, contract versions and failure modes; link REQ, AC, D and R IDs; preserve authority boundaries. Adaptador padronizado (ex. ACP) com fallback específico por agente; versionar capabilities. |
| Tasks | Name actual files, fixtures, tools, real permissions, failure injections and completion checks. Criar fakes controláveis e integração mínima ACP/CLI. |
| Evidence / convergence | Identify observed implementation/oracle/configuration versions and hashes, test results, unsatisfied criteria and explicit limits. máquina de estados, adaptadores testáveis, eventos ordenados, controles de processo, tratamento de cancelamento, integração de políticas |

## Conditional handoff

Optional specialist: `reliability-engineering`. Specific unresolved question: “Como limitar processos órfãos, duplicação de efeitos e perda de eventos durante falhas?” Consult only if actually present and needed. Supply relevant IDs, known facts, unknowns, permission scope, versions and required evidence. Do not install or load a whole dependency chain. Continue independent work and mark blocked criteria unverified.

## Completion and authority

Use the destination SDD's states: APROVADO, REPROVADO, NÃO VERIFICADO, INCONCLUSIVO, NÃO APLICÁVEL (with justification). A mock or document is not execution evidence. Record freshness of inputs and source of each observation. Spec owns behavior; plan/ADRs own decisions; tasks own work; this bridge only connects the skill to those artifacts.
