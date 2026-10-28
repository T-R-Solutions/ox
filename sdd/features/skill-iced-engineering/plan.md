# Plano de autoria de iced-engineering

Rota completa por contrato de competência, fronteiras e critérios de avaliação. Autoridade: spec desta feature e constituição do consumidor para efeitos autorizados.

## Alternativas técnicas preservadas

As escolhas abaixo são alternativas de método a ensinar/avaliar, não decisões técnicas aprovadas do Ox.


| ID | Decisão ou risco | Verificação proposta |

|---|---|---|

| D-01 | Modelo Message/Update/View com estado explícito e tarefas externas à renderização. | Revisão de alternativas + contrato observado |

| D-02 | Renderização incremental, virtualização quando necessária e política de suspensão de views pesadas. | Cenários rejeitados e comparação de opções |

| R-01 | UI bloqueada por trabalho síncrono acoplado a evento. | Teste adverso pertinente |

| R-02 | Acessibilidade e comportamento multiplataforma incompletos de widget customizado. | Falsificação controlada do resultado |



D-03 [REQ-04]: criar entrada, três referências especializadas e casos próprios em vez de duplicar uma skill geral; custo de manutenção justificado pela competência especializada e pelos cenários locais da spec; o comparativo é somente origem histórica. R-03 [REQ-04]: seleção ambígua ou texto superficial; verificar com casos positivos, negativos e falha. Reavaliar após uso observado ou mudança das fontes.

## Seleção de métodos e dependências

Método primário de autoria efetivamente consultado: skill-creator do ambiente (versão não declarada; cópia de consulta em docs/validation/adoption-baseline/skill-creator.md). Sem ponte local para esse método. Esta nova skill não existia na seleção inicial e não é declarada consultada na própria autoria.

A ponte sdd/chain/iced-engineering.md, bridge_version 1, e entrada .codex/skills/iced-engineering/SKILL.md ficam disponíveis para consumidores e avaliação posterior; existência não prova consulta. Auxiliar condicional proposta: `design-system` — O componente reutilizável preserva tokens, variantes, estados e contrato de interação definidos? Sem consulta automática.

Dependências de autoria: protocolo → runtime → verificação; workspace/Iced completam fundação; contexto antecede grafo; output e uso dependem do vocabulário de eventos. Não são dependências de instalação.

## Atividades técnicas propostas a ensinar e retomar

> - [ ] P001 [REQ, AC, D, R aplicáveis]: Inventariar as APIs realmente presentes na versão escolhida de Iced.
> - [ ] P002 [REQ, AC, D, R aplicáveis]: Definir contrato de componentes, layout e tarefas/assinaturas.
> - [ ] P003 [REQ, AC, D, R aplicáveis]: Criar harness de UI e fixtures para estados/carregamento/eventos.
> - [ ] P004 [REQ, AC, D, R aplicáveis]: Medir responsividade, revisar acessibilidade e atualizar limites documentados.

P001..P004 preservam a intenção das tarefas propostas; não declaram implementação do produto. A execução local de autoria está em tasks.md. Testes reais dependem de consumidor e escopo autorizado.

## Consulta posterior na avaliação

Em 2026-10-26 um subagente interno consultou `.codex/skills/iced-engineering/SKILL.md` versão 1.0.0 e referências técnicas para responder cenário adverso. Ponte disponível bridge_version 1; avaliação direta, sem alegar consulta da ponte. Primária: esta skill, agora existente; auxiliares não necessárias. Catálogo de descrições usado antes da leitura para seleção. Perguntas, resposta bruta, caminhos consultados e limitações em `docs/validation/agent-evals/`; julgamento do executor separado em review.md. Não é consulta durante autoria nem integração do produto.
