---
skill: tool-output-engineering
skill_path: .codex/skills/tool-output-engineering/SKILL.md
bridge_version: 1
---

# SDD bridge: tool-output-engineering

Copy this file to the destination project's `sdd/chain/` and set `skill_path` to the actual project-relative path of the skill entry. This is an optional bridge and does not install or activate the skill.

## Selection

Use for: Redução de tokens de stdout/stderr, parsers de comando, resumos de testes, supressão controlada de ruído, detecção de truncamento.

Do not select for: Não aplicar a log de auditoria irreversivelmente; não vender redução estimada de caracteres como redução medida na conta do provedor.

Select only when the concrete feature has this specialized question. Read the actual skill; record its path/version and selection reason in the plan. A bridge reference does not recursively select other skills.

## Inputs and contributions

Known inputs: bytes brutos, metadados exit code, formato da ferramenta, limites/encoding, estratégia de retenção e orçamento. Do not infer missing capabilities or permissions.

| Artifact | Required input / contribution |
|---|---|
| Constitution | Reconcile existing authorization, data residency, safety and project constraints; add no product policy automatically. |
| Spec | Define scoped, observable behavior and rejected cases. Cada saída transformada conserva exit code, sinais de erro e referência ao bruto. |
| Plan / ADR | Compare alternatives, contract versions and failure modes; link REQ, AC, D and R IDs; preserve authority boundaries. Três formas: raw append-only, estrutura normalizada e visão compacta. |
| Tasks | Name actual files, fixtures, tools, real permissions, failure injections and completion checks. Construir corpus adverso e testes diferenciais com saídas reais autorizadas. |
| Evidence / convergence | Identify observed implementation/oracle/configuration versions and hashes, test results, unsatisfied criteria and explicit limits. saída bruta preservada, eventos estruturados, resumo com sinalização de perda/truncamento, mensuração comparável |

## Conditional handoff

Optional specialist: `application-security`. Specific unresolved question: “Texto de stdout pode ser confundido com instrução ou dado autorizado para ferramenta?” Consult only if actually present and needed. Supply relevant IDs, known facts, unknowns, permission scope, versions and required evidence. Do not install or load a whole dependency chain. Continue independent work and mark blocked criteria unverified.

## Completion and authority

Use the destination SDD's states: APROVADO, REPROVADO, NÃO VERIFICADO, INCONCLUSIVO, NÃO APLICÁVEL (with justification). A mock or document is not execution evidence. Record freshness of inputs and source of each observation. Spec owns behavior; plan/ADRs own decisions; tasks own work; this bridge only connects the skill to those artifacts.
