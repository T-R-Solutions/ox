# ADR — Modelo enxuto do SDD e remoção do legado — 2026-11-23

Estado: adotada em 2026-11-23 pelo pedido do mantenedor ("Refatore como o sdd está configurado
para algo mais objetivo e centralizado [...] E apague todo o legado do projeto"), na task
[SDD-ENXUTO-20261123](../../sdd/tasks/SDD-ENXUTO-20261123.md). Substitui os ADRs de processo
removidos nesta data (adoção, `governance-*`, `maintenance-001`, `prompt-execution-contract`,
`sdd-centralization`, `implementation-transition`, `technical-acceptance`,
`skill-ui-metadata-inventory`, `readme-skill-integration`, `readme-preservation`,
`visual-skill-refinement`, `technical-documentation-visuals`). O texto deles está no histórico do Git.

## Contexto

A centralização anterior (mesma data) criou `sdd/` com constituição, estado, workflow, specs e
tasks, mas congelou o modelo antigo em `sdd/history/` e manteve `docs/validation/` (17.440
arquivos versionados), manifestos de histórico e de cobertura normativa, perfil de skills,
`.ai/`, `task_finalizada.md` e 13 perfis de agente que citavam um procedimento só existente no
histórico. A etapa 8 exigia sha256 calculado à mão e a matriz da etapa 6 era redigida à mão.

## Decisão

1. Autoridade em três arquivos lidos sempre: `sdd/constitution.md`, `sdd/project.md` e
   `sdd/workflow.md`. O workflow absorve o mapa de skills e os papéis dos agentes (GOV-02, GOV-04);
   `sdd/skills.md`, `sdd/agents.md`, `sdd/README.md` e o catálogo `.codex/skills/README.md` saem.
2. Fluxo: pedido → prompt (skill `prompt`) → esclarecer → especificar → planejar → itens →
   coerência → executar → validar → fechar, cada etapa com saída, skill, papel e gate.
3. Ferramentas: `sdd/tools/sddtask.py evidence --write|--check` calcula os hashes da seção 8;
   `sdd/tools/validate.py --matrix` deriva a matriz REQ → D → T → AC. Sem índice paralelo de
   tasks: o estado está no cabeçalho de cada registro.
4. Agentes do Codex: 6 perfis (`ec_orquestrador_normal`, `ec_orquestrador_alta`,
   `ec_planejador`, `ec_implementador`, `ec_implementador_extra_alto`, `ec_verificador`), cada
   um apontando para uma seção existente do workflow.
5. Legado removido do working tree, sem reescrever o histórico Git: `sdd/history/`,
   `docs/validation/`, `docs/structure/`, `config/governance/`, `.ai/`, `task_finalizada.md`,
   `claude_analysis.md`, tasks fechadas do modelo anterior, `tools/governance/consumers/` e os
   guias de `docs/development/` do processo antigo.
6. IDs POL/GOV/RQ não são renumerados; GOV-08 (já revogada) foi removida do texto.

## Fatos técnicos preservados

- As 10 features `product-*` viraram specs vivas em `sdd/specs/`, com texto original, estados de
  AC herdados (`(herdado)`) e limitações. Features `skill-*` e de governança eram processo.
- Inventários movidos para junto do consumidor: `docs/design/reference-members.json`
  (membros das fontes visuais), `docs/licensing/license-inventory.json` (marcadores de licença
  dos archives, 2026-10-27) e `docs/licensing/copy-provenance.json` (origem e bytes das skills e
  materiais copiados).
- Perfil de skills: 17 gerais, 5 condicionais (`commit-governance`, `distributed-systems`,
  `engineering-productivity`, `prompt`, `readme-lifecycle-engineering`) e 9 especializações
  próprias (`plugin-protocol-engineering`, `agent-runtime-engineering`,
  `autonomous-verification-engineering`, `workspace-integrity-engineering`, `iced-engineering`,
  `code-context-engineering`, `code-knowledge-graph-engineering`, `tool-output-engineering`,
  `agent-usage-accounting`); `gleam`, `kotlin` e `postgresql` excluídas. O mapa vive em
  [workflow](../../sdd/workflow.md#skills); a origem para licença, no `NOTICE`.
- GOV-01: `tools/governance/scripts/check-ox.py` inspeciona conteúdo e archives recursivamente
  (`inspect_bytes`, orçamento expandido de 128 MiB, profundidade ≤ 8).
- Ferramentas de governança ficam em `tools/governance/`; `src/` na raiz fica reservado a fontes
  da aplicação (decisão de 2026-10-27).
- Todo pedido de trabalho começa por um prompt objetivo gerado pela skill `prompt` (decisão de
  2026-11-19, hoje GOV-09).
- `scripts/config/native/gitleaks/gitleaks-history.ignore` continua: o histórico Git ainda contém
  os arquivos removidos e seus falsos positivos revisados.

## Alternativas descartadas

- Manter `sdd/history/` e `docs/validation/` congelados: mantém 6 GB no checkout, manifestos de
  verificação e cerca de 60 referências ativas ao modelo antigo.
- Reescrever o histórico Git para remover os bytes: destrutivo para clones e remotos e não pedido.
- Remover os sha256 da evidência: perde a detecção de critério ou input alterado na retomada.
- Manter 13 perfis só corrigindo as referências: a árvore admite 2 especialistas simultâneos e
  vários perfis nunca coexistem.

## Consequências

- Evidência anterior a 2026-11-23 só é recuperável pelo Git (`git show <commit>:<caminho>`); ela
  não sustenta aprovação nova. ACs herdados são reavaliados pela task que tocar a capacidade.
- `check-ox.py` deixa de verificar manifesto de histórico, cobertura normativa e perfil JSON;
  passa a conferir `.codex/skills/` contra a tabela de skills do workflow.

## Gatilho de revisão

Reabrir se uma task precisar de observação antiga que o Git não recupere, se o Codex não carregar
os 6 perfis com `codex --strict-config`, ou se a leitura obrigatória (AGENTS, constitution,
project, workflow e skill `prompt`) passar de 5.635 palavras.
