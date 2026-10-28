---
skill: plugin-protocol-engineering
skill_path: .codex/skills/plugin-protocol-engineering/SKILL.md
bridge_version: 1
---

# SDD bridge: plugin-protocol-engineering

Copy this file to the destination project's `sdd/chain/` and set `skill_path` to the actual project-relative path of the skill entry. This is an optional bridge and does not install or activate the skill.

## Selection

Use for: Novo protocolo/plugin host, manifest de capacidades, IPC, compatibilidade vN/vN+1, instalação/desinstalação segura.

Do not select for: Não selecionar para um plugin de lint que apenas utiliza SDK já estabilizado; nesse caso, aplicar Rust e API Testing. Não converter a skill em recomendação automática de Wasm, gRPC ou Dylib.

Select only when the concrete feature has this specialized question. Read the actual skill; record its path/version and selection reason in the plan. A bridge reference does not recursively select other skills.

## Inputs and contributions

Known inputs: políticas de extensibilidade, modelo de ameaças, operações/capacidades, matriz de versões, SO, recursos disponíveis. Do not infer missing capabilities or permissions.

| Artifact | Required input / contribution |
|---|---|
| Constitution | Reconcile existing authorization, data residency, safety and project constraints; add no product policy automatically. |
| Spec | Define scoped, observable behavior and rejected cases. Negociar versão e capacidades sem executar operações ainda não autorizadas. |
| Plan / ADR | Compare alternatives, contract versions and failure modes; link REQ, AC, D and R IDs; preserve authority boundaries. Processo externo + contrato versionado versus biblioteca dinâmica carregada no host; decidir por modelo de falhas e ABI. |
| Tasks | Name actual files, fixtures, tools, real permissions, failure injections and completion checks. Implementar harness de testes de contrato, falha, limites e compatibilidade. |
| Evidence / convergence | Identify observed implementation/oracle/configuration versions and hashes, test results, unsatisfied criteria and explicit limits. contrato de mensagens, estados do host, modelo de permissões, limites de recursos, matriz compatível, testes de falhas e migração |

## Conditional handoff

Optional specialist: `application-security`. Specific unresolved question: “O isolamento escolhido realmente impede os efeitos não autorizados de um plugin comprometido?” Consult only if actually present and needed. Supply relevant IDs, known facts, unknowns, permission scope, versions and required evidence. Do not install or load a whole dependency chain. Continue independent work and mark blocked criteria unverified.

## Completion and authority

Use the destination SDD's states: APROVADO, REPROVADO, NÃO VERIFICADO, INCONCLUSIVO, NÃO APLICÁVEL (with justification). A mock or document is not execution evidence. Record freshness of inputs and source of each observation. Spec owns behavior; plan/ADRs own decisions; tasks own work; this bridge only connects the skill to those artifacts.
