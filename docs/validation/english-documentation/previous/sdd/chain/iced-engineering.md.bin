---
skill: iced-engineering
skill_path: .codex/skills/iced-engineering/SKILL.md
bridge_version: 1
---

# SDD bridge: iced-engineering

Copy this file to the destination project's `sdd/chain/` and set `skill_path` to the actual project-relative path of the skill entry. This is an optional bridge and does not install or activate the skill.

## Selection

Use for: Código Iced, modelos de update/view, widgets customizados, split panes, temas, acessibilidade e visualização gráfica.

Do not select for: Não selecionar para projeto sem Iced; não substituir design-review/design-system na decisão de hierarquia visual.

Select only when the concrete feature has this specialized question. Read the actual skill; record its path/version and selection reason in the plan. A bridge reference does not recursively select other skills.

## Inputs and contributions

Known inputs: versão do Iced e features, estado da GUI, fluxos, eventos, restrições de tamanho, acessibilidade e latência. Do not infer missing capabilities or permissions.

| Artifact | Required input / contribution |
|---|---|
| Constitution | Reconcile existing authorization, data residency, safety and project constraints; add no product policy automatically. |
| Spec | Define scoped, observable behavior and rejected cases. A UI não bloqueia em processos, busca, indexação ou eventos de agentes. |
| Plan / ADR | Compare alternatives, contract versions and failure modes; link REQ, AC, D and R IDs; preserve authority boundaries. Modelo Message/Update/View com estado explícito e tarefas externas à renderização. |
| Tasks | Name actual files, fixtures, tools, real permissions, failure injections and completion checks. Criar harness de UI e fixtures para estados/carregamento/eventos. |
| Evidence / convergence | Identify observed implementation/oracle/configuration versions and hashes, test results, unsatisfied criteria and explicit limits. componentes/contratos de update, UI testável, estados vazios/erro/carregamento, orçamento de renderização e benchmark |

## Conditional handoff

Optional specialist: `design-system`. Specific unresolved question: “O componente reutilizável preserva tokens, variantes, estados e contrato de interação definidos?” Consult only if actually present and needed. Supply relevant IDs, known facts, unknowns, permission scope, versions and required evidence. Do not install or load a whole dependency chain. Continue independent work and mark blocked criteria unverified.

## Completion and authority

Use the destination SDD's states: APROVADO, REPROVADO, NÃO VERIFICADO, INCONCLUSIVO, NÃO APLICÁVEL (with justification). A mock or document is not execution evidence. Record freshness of inputs and source of each observation. Spec owns behavior; plan/ADRs own decisions; tasks own work; this bridge only connects the skill to those artifacts.
