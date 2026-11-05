# Plano de autoria de agent-usage-accounting

Rota completa por contrato de competência, fronteiras e critérios de avaliação. Autoridade: spec desta feature e constituição do consumidor para efeitos autorizados.

## Alternativas técnicas preservadas

As escolhas abaixo são alternativas de método a ensinar/avaliar, não decisões técnicas aprovadas do Ox.


| ID | Decisão ou risco | Verificação proposta |

|---|---|---|

| D-01 | Ledger imutável de eventos de uso mais views computadas; não mutar evento medido. | Revisão de alternativas + contrato observado |

| D-02 | Unidades/tarifas versão-datadas, escopos de agregação e flags de exatidão e indisponibilidade. | Cenários rejeitados e comparação de opções |

| R-01 | Dupla contagem por retries, streaming e reconexão. | Teste adverso pertinente |

| R-02 | Preço, cache e granularidade diferentes entre agentes geram números enganosos. | Falsificação controlada do resultado |



D-03 [REQ-04]: criar entrada, três referências especializadas e casos próprios em vez de duplicar uma skill geral; custo de manutenção justificado pela competência especializada e pelos cenários locais da spec; o comparativo é somente origem histórica. R-03 [REQ-04]: seleção ambígua ou texto superficial; verificar com casos positivos, negativos e falha. Reavaliar após uso observado ou mudança das fontes.

## Seleção de métodos e dependências

Método primário de autoria efetivamente consultado: skill-creator do ambiente (versão não declarada; cópia de consulta em docs/validation/adoption-baseline/skill-creator.md). Sem ponte local para esse método. Esta nova skill não existia na seleção inicial e não é declarada consultada na própria autoria.

A ponte sdd/chain/agent-usage-accounting.md, bridge_version 1, e entrada .codex/skills/agent-usage-accounting/SKILL.md ficam disponíveis para consumidores e avaliação posterior; existência não prova consulta. Auxiliar condicional proposta: `observability-and-diagnostics` — O evento de uso chega integralmente e pode ser correlacionado sem violar privacidade? Sem consulta automática.

Dependências de autoria: protocolo → runtime → verificação; workspace/Iced completam fundação; contexto antecede grafo; output e uso dependem do vocabulário de eventos. Não são dependências de instalação.

## Atividades técnicas propostas a ensinar e retomar

> - [ ] P001 [REQ, AC, D, R aplicáveis]: Inventariar campos disponíveis e ausência de dados por adaptador.
> - [ ] P002 [REQ, AC, D, R aplicáveis]: Definir ledger idempotente, tipos/unidades, moeda e timezones.
> - [ ] P003 [REQ, AC, D, R aplicáveis]: Criar fixtures com cache, replay, streaming parcial e falta de preço.
> - [ ] P004 [REQ, AC, D, R aplicáveis]: Confrontar agregações com fonte observada e registrar precisão/limites.

P001..P004 preservam a intenção das tarefas propostas; não declaram implementação do produto. A execução local de autoria está em tasks.md. Testes reais dependem de consumidor e escopo autorizado.

## Consulta posterior na avaliação

Em 2026-10-26 um subagente interno consultou `.codex/skills/agent-usage-accounting/SKILL.md` versão 1.0.0 e referências técnicas para responder cenário adverso. Ponte disponível bridge_version 1; avaliação direta, sem alegar consulta da ponte. Primária: esta skill, agora existente; auxiliares não necessárias. Catálogo de descrições usado antes da leitura para seleção. Perguntas, resposta bruta, caminhos consultados e limitações em `docs/validation/agent-evals/`; julgamento do executor separado em review.md. Não é consulta durante autoria nem integração do produto.
