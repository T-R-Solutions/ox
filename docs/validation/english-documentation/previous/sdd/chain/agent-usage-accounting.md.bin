---
skill: agent-usage-accounting
skill_path: .codex/skills/agent-usage-accounting/SKILL.md
bridge_version: 1
---

# SDD bridge: agent-usage-accounting

Copy this file to the destination project's `sdd/chain/` and set `skill_path` to the actual project-relative path of the skill entry. This is an optional bridge and does not install or activate the skill.

## Selection

Use for: Contagem de tokens por chat/dia/projeto, custos multimodelo, janela de contexto, cache, preços e relatórios de uso.

Do not select for: Não selecionar para instrumentar CPU/RAM genericamente; observability-and-diagnostics. Não confundir progresso funcional com consumo de contexto.

Select only when the concrete feature has this specialized question. Read the actual skill; record its path/version and selection reason in the plan. A bridge reference does not recursively select other skills.

## Inputs and contributions

Known inputs: eventos de provedores/agentes, tipos de tokens/caches, tarifas versionadas, intervalos, identidade de sessão/tarefa. Do not infer missing capabilities or permissions.

| Artifact | Required input / contribution |
|---|---|
| Constitution | Reconcile existing authorization, data residency, safety and project constraints; add no product policy automatically. |
| Spec | Define scoped, observable behavior and rejected cases. Registros distinguem medição fornecida pelo provedor, derivação e estimativa. |
| Plan / ADR | Compare alternatives, contract versions and failure modes; link REQ, AC, D and R IDs; preserve authority boundaries. Ledger imutável de eventos de uso mais views computadas; não mutar evento medido. |
| Tasks | Name actual files, fixtures, tools, real permissions, failure injections and completion checks. Criar fixtures com cache, replay, streaming parcial e falta de preço. |
| Evidence / convergence | Identify observed implementation/oracle/configuration versions and hashes, test results, unsatisfied criteria and explicit limits. esquema de ledger de uso, regras para duplicação e gaps, visões por período, proveniência e precisão das estimativas |

## Conditional handoff

Optional specialist: `observability-and-diagnostics`. Specific unresolved question: “O evento de uso chega integralmente e pode ser correlacionado sem violar privacidade?” Consult only if actually present and needed. Supply relevant IDs, known facts, unknowns, permission scope, versions and required evidence. Do not install or load a whole dependency chain. Continue independent work and mark blocked criteria unverified.

## Completion and authority

Use the destination SDD's states: APROVADO, REPROVADO, NÃO VERIFICADO, INCONCLUSIVO, NÃO APLICÁVEL (with justification). A mock or document is not execution evidence. Record freshness of inputs and source of each observation. Spec owns behavior; plan/ADRs own decisions; tasks own work; this bridge only connects the skill to those artifacts.
