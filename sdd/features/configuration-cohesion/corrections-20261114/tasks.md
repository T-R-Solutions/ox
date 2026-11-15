# Tarefas propostas — correções A01–A10

Escopo autorizado em 14/11/2026: preparar e apresentar o planejamento. Aplicação
das correções aguarda revisão do mantenedor. Este suplemento não altera as tarefas
T001–T003 nem os estados atuais da feature pai. Os IDs seguintes ficam reservados
para sua integração depois da aprovação. Contratos: [spec](spec.md) e [plan](plan.md).

| ID / situação | Escopo e arquivos | Dependência | Dono e condição de conclusão |
|---|---|---|---|
| T004 — planejamento produzido; conferência registrada em converge | Este suplemento; requisitos, decisões, tarefas e observações | Pedido atual | Coordenador; dez achados cobertos e proposta apresentada, sem aplicar correções |
| T005 — pendente de aprovação | Atualizar inventário, precondições e mapa de inputs afetados; registrar escopo aprovado | Aprovação de implementação | Coordenador; versões reais e dono único por caminho, conflitos tratados |
| T006 — pendente | ADR proposta, artefatos canônicos de configuration-cohesion, rastreabilidade e mapa de sucessão | T005 | Coordenador; AC-01–03 preservados, critérios novos adotados explicitamente e evidências dependentes identificadas |
| T007 — A02, REQ-05, AC-05 | commit-governance; consumidores de escolha pré-commit e verificação por plano | T006 | Implementador de instruções; receita atual alcançada pelas referências e cenários Sim/Não/sem resposta preservados |
| T008 — A01, REQ-04, AC-04 | Projeções de converge, evidence.md, checker, integração check-ox e testes | T006 | Coordenador + implementador do checker em caminhos disjuntos; projeções adotadas coerentes e mutação negativa detectada |
| T009 — A04, REQ-07, AC-07 | Fronteira de links em validate.py, README e testes | T008 | Implementador do checker; autoridade interna válida aceita, escape/symlink recusados e modo portátil preservado |
| T010 — A06, REQ-09, AC-09 | Seleção --feature, ajuda, consumidores e testes | T009 | Mesmo dono do checker; seleção explícita completa, sem aprovação global ou seleção vazia silenciosa |
| T011 — A03, REQ-06, AC-06 | Templates/README e instruções de cópia; regressão em destino | T009 | Coordenador documental + testador; passos publicados produzem links válidos nos dois layouts |
| T012 — A05, REQ-08, AC-08 | README SDD, receita de adoção e fixture independente | T010, T011 | Coordenador documental + testador; consumidor limpo funciona sem carregar features/evidências Ox |
| T013 — A08, REQ-11, AC-11 | Procedimento de agentes, config raiz, guia e escopo de instalação | T006 e aprovação de D-11 | Coordenador; matriz de execução/revisão clara, direitos do host respeitados, alto risco sem fallback silencioso |
| T014 — A07, REQ-10, AC-10 | ec_triador.toml e referências pertinentes | T013 | Implementador de instruções; raiz/controlador e triador delegado sem proibições incompatíveis |
| T015 — A09, REQ-12, AC-12 | Manifesto delimitado de skills/pontes/perfis/guias; catálogo apenas se houver encaminhamento afetado | T007–T014 | Implementador de instruções; comparação semântica preserva métodos, identidades e uso independente |
| T016 — A10, REQ-13, AC-13 | project.md, índice histórico e entradas atuais efetivamente afetadas | T008, T015 | Coordenador; resumo vigente rastreável e histórico claramente identificado, sem novas alegações de aceite |
| T017 — REQ-14, AC-14 | Registros de sucessão e consumidores afetados; disposições de evidência | T007–T016, com preparação por lote desde T006 | Coordenador; mutações desconhecidas recusadas, predecessores preservados e nenhuma renovação fictícia |
| T018 — REQ-15, AC-15 | Testes finais, revisão independente, validação e fechamento documental | T017 | Testador, revisor e validador; critérios originais/novos confrontados com inputs estáveis e limites explícitos |

Cada item A01–A10 também referencia D-04/R-04 até D-13/R-13 conforme o plan.
T017 e T018 usam D-14/R-14. Esta tabela distribui responsabilidades lógicas;
não registra agentes já criados. Um arquivo compartilhado nunca terá dois
escritores simultâneos. T008/T009/T010 ficam com o mesmo dono do checker.

## Regras de execução após aprovação

- Conferir a revisão aprovada e as condições reais de delegação antes de atribuir
  trabalho. A ausência de capacidade só bloqueia sua etapa dependente.
- Fazer verificações focadas por tarefa; a suíte final ocorre após estabilização
  dos inputs e encerramento dos escritores. Registrar falhas, skips e limitações.
- Antes de concluir cada tarefa, registrar no próprio item os documentos revisados,
  atualizados, verificações e limites, ou justificativa concreta de ausência de
  impacto. A política vem do [workflow](../../../workflow.md#documentation-before-task-closure).
- Ao mudar um input vinculado, preservar a observação anterior e reavaliar apenas
  o que depende dele. Um resultado UNVERIFIED/INCONCLUSIVE não vira aprovado pela
  marcação de uma tarefa.
- Não executar as tarefas de correção durante a entrega deste planejamento.

## Disposição documental do planejamento

Revisados: AGENTS, constituição, estado do projeto, arquitetura, workflow/evidence,
procedimento/config/perfis dos agentes, auditoria, feature configuration-cohesion,
templates, skill/pontes selecionadas, contratos e testes de governança/sucessão e
receitas de automação/commit citadas no plano. Resultado: somente este suplemento
foi criado; os contratos, código e evidências existentes continuam com seus bytes
anteriores. A razão é verificável: o pedido autoriza planejar e exige apresentação
antes de aplicar. Observações da conferência documental ficam em [converge](converge.md).
