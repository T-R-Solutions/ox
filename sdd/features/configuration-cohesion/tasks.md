# Tarefas

- [x] T001 — Inventariar entradas, recursos, pontes e autoridades; separar duplicações de métodos próprios. Registro: inventory.json e report.md no diretório de validação configuration-refactor-20261111. Cobertura estática de 225 arquivos; eficácia completa dos métodos não foi reavaliada.
- [x] T002 — Refatorar 26 pontes, nove skills e AGENTS; preservar procedimentos, links e contribuições. Atualizados project.md, guia sdd-skills.md e chain/README.md; perfil e identidades permanecem coerentes. Comparações em preservation.json e preimagens em before/. Corrigida afirmação obsoleta sobre aceitação dos cenários.
- [x] T003 — Verificar estrutura e preservação, registrar resultados e atualizar documentação. 28 testes de sucessão, sete de fechamento, 31 validações de skills e check-ox aprovados. Evidências antigas afetadas preservadas; sem nova aceitação de produto ou eficácia. Documentos revisados: AGENTS, workflow/evidence/templates, catálogo/perfil, pontes, guia de integração e artefatos desta feature. Workflow já contém a regra normativa de atualização ao encerrar tarefas; não foi duplicada nas skills.

Comandos e resultados: docs/validation/configuration-refactor-20261111/checks.log.
Limites e condição de retomada: executar consumidores/oráculos representativos sobre
os bytes atuais para afirmar eficácia técnica; usar tokenizador e workload definidos
para alegar economia de tokens. Redução em palavras/bytes não comprova essas alegações.

## Execução autorizada — 14/11/2026

O mantenedor aprovou integralmente o plano A01–A10. Os registros de planejamento
continuam históricos; esta seção adota suas tarefas sem alterar T001–T003.

| ID / situação | Escopo e arquivos | Dependência | Dono e condição de conclusão |
|---|---|---|---|
| T004 — planejamento produzido; conferência registrada em converge | Este suplemento; requisitos, decisões, tarefas e observações | Pedido atual | Coordenador; dez achados cobertos e proposta apresentada, sem aplicar correções |
| T005 — executado | Atualizar inventário, precondições e mapa de inputs afetados; registrar escopo aprovado | Aprovação de implementação | Coordenador; versões reais e dono único por caminho, conflitos tratados |
| T006 — executado | ADR proposta, artefatos canônicos de configuration-cohesion, rastreabilidade e mapa de sucessão | T005 | Coordenador; AC-01–03 preservados, critérios novos adotados explicitamente e evidências dependentes identificadas |
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

Disposição documental e resultados atuais: docs/validation/governance-corrections-20261114/report.md.
As marcações históricas não substituem os estados de evidence.json.

## Disposição documental da implementação

T005/T006: inputs-before/bindings-before, ADR e spec/plan/traceability revisados;
57 fontes do planejamento coincidiram. Autorização sucessora preserva o suplemento.
T007–T010: commit skill, evidence/README, checker e chamada check-ox atualizados;
regressões novas e compatibilidade executadas, resultados nos relatórios dos autores.
T011/T012: README/templates revisados; cópia/adaptação padrão/custom e adoção
independente sem/com skill verificados; fixture de cópia é classificada integração.
T013/T014: procedimento comum/config/perfis/guias revisados; modelos inalterados,
matriz e cenários textuais conferidos. Criação real de contextos/vagas foi observada;
não é medição de obediência ou qualidade de modelos.
T015: 31 pares inventariados, quatro deltas de skill/pontes mapeados e medidas
recalculáveis; mapa de seções corrigido após revisão independente.
T016: project e abertura de architecture/context revisados, história preservada;
README/AGENTS já encaminham autoridades e não precisam outra cópia de comandos.
T017: sucessão delimitada e invalidação seletiva, com predecessores íntegros;
fixtures históricas atualizadas para incluir registro atual, sem reduzir rejeições.
T018: métodos, resultados finais, revisão independente e limites pertencem a
report.md, final-observations.json e independent-validation.md no diretório
`docs/validation/governance-corrections-20261114/`; o estado de conclusão por
critério é exclusivamente evidence.json e sua projeção. Não há aprovação de
scanners reais, produto ou features pendentes por esses checks.

T017/T018 — achado de integração: cópias legítimas distinguem-se por receipt explícito;
perfis são snapshots observados, com comparação obrigatória de fontes no checkout.
Docs README permanece intacto; predecessor anterior recuperado pela remoção exata
da única linha de agentes. ADR, README SDD e guia comum documentam fronteira,
negativos e limites; logs iniciais falhos permanecem, reexecução limitada aos
consumidores afetados. EOF de duas pontes removeu exatamente um LF, com nova
inspeção/medidas; a suíte anterior não é alegada como execução desses bytes finais.

## Continuação de reparo de logs — 2026-11-15

G1–G4: revisar deltas, registrar sucessores exatos, corrigir consumidores e verificar
rejeição de mutação/downgrade/links escapando. Dono governance_repair; revisão e
validação independentes pendentes. Disposição documental e comandos em
docs/validation/log-repair-20261115/governance.md. Evidências antigas preservadas;
estados afetados aguardam novas observações.

## Sucessor de links históricos — 15/11/2026

T019 — autorizado pelo pedido “implemente”: confirmar inventário/proveniência,
implementar registro adicional e sucessão exata, executar positivos/negativos e
cópia independente, revisar/validar em contextos próprios e atualizar documentação.
AC-16/REQ-16/D-15/R-15; dependências e donos por caminho são T001–T008 do plano
governance-link-repair-plan-20261115. Os 15 critérios anteriores continuam exigidos
pelo gate completo; sua condição inicial UNVERIFIED não é convertida em aceite.
Resultados, disposição documental e pendências pertencem ao relatório
docs/validation/governance-link-repair-20261115/report.md e ao envelope atual.
