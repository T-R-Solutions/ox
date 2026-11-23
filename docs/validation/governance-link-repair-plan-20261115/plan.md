# Plano de correção de links históricos e diagnóstico de governança

Data: 15/11/2026. Pedido: **“Crie um planejamento para correção completa desse problema!”**
Estado desta entrega: planejamento; implementação e aceitação operacional **UNVERIFIED**.

## Autorização, rota e limite

Esta solicitação autoriza leitura, diagnóstico e elaboração/revisão deste plano.
O único destino de escrita desta etapa é
`docs/validation/governance-link-repair-plan-20261115/`. Não autoriza implementação,
alteração de snapshots ou envelopes de aceite, execução completa, downloads,
manutenção do Toolbox, commits ou publicação. Autorizações antigas em documentos
não ampliam esse escopo. O inventário [planning-inputs.json](planning-inputs.json)
identifica bytes consultados e alterações preexistentes; não é evidência de execução
da correção nem um registro de origens aceito pelo checker.

A futura correção segue rota SDD completa e coordenação alta: modifica a resolução
de evidências históricas em um gate e a projeção de falhas. Há risco de falsa
aprovação e de quebra de consumidores de cópia. Nenhuma dificuldade demonstrada
justifica esforço extra alto. Este plano reúne requisitos, decisões, tarefas e
verificação; não cria uma feature vazia ou altera estados existentes por formalidade.
Após autorização de implementação, estender `configuration-cohesion` para origem,
integridade e consumidores, e `terminal-progress` para diagnóstico/apresentação.
Os critérios completos dessas features continuam aplicáveis; não selecionar só
critérios convenientes. Se a inspeção de bindings revelar contrato independente,
justificar uma feature dedicada antes de mudar a organização, sem mover as atuais.

Autoridades lidas: `AGENTS.md`, `sdd/project.md`, `docs/constitution.md`,
`docs/architecture/context.md`, `sdd/workflow.md`, `sdd/evidence.md` e
`docs/development/codex-agents.md`. ADRs pertinentes consultados:
`governance-instruction-reconciliation.md`, `scripts-task-closure.md` e
`scripts-toolbox-native.md`, em `docs/decisions/`. POL-05/06/08/10 e GOV-05/08
fundamentam preservação, evidência, raw e limites de autorização.

## Diagnóstico observado e limites

Na execução preservada `ox-run-5DyYy5sn`, os arquivos locais
`.local/logs/2026-11-15/ox-run-5DyYy5sn--ox--process.json.log` e
`ox-run-5DyYy5sn--ox--result.json.log` registram cwd
`/home/rodrigo/Projetos/ox`, estado `failed`, exit 1 e `argv_recorded: false`.
O argv original não pode ser reconstruído como fato a partir desses registros.
O stdout do mesmo check contém exatamente 22 ocorrências `Broken/escaping link`;
o stderr está vazio. A raiz relatou reprodução dos mesmos 22 erros executando
somente `check-ox.py`; esta coordenação inspecionou os logs e fontes, sem repetir
essa execução. A existência de stdout com falhas contradiz a hipótese de que o
problema seja apenas falta de mensagem da ferramenta ou cwd incorreto.

| Snapshot imutável, relativo à raiz | Ocorrências | Origem proposta para revisão |
| --- | ---: | --- |
| `docs/validation/terminal-style-20261115/before/terminal-converge.md` | 1 | `sdd/features/terminal-progress/converge.md` |
| `docs/validation/terminal-style-20261115/before/scripts-README.md` | 10 | `scripts/README.md` |
| `docs/validation/terminal-style-20261115/pre-final-validation/terminal-progress-converge.md` | 1 | `sdd/features/terminal-progress/converge.md` |
| `docs/validation/history-correction-20261115/coordinator/terminal-converge-before.md` | 1 | `sdd/features/terminal-progress/converge.md` |
| `docs/validation/history-correction-20261115/coordinator/scripts-readme-before.md` | 9 | `scripts/README.md` |

As três referências de convergência apontam para `evidence.json`; as duas cópias
de README contêm referências relativas de `scripts/README.md`. Os relatórios
dessas alterações corroboram o contexto das cópias. Essa correspondência deve ser
revista semanticamente antes de ser autenticada: nome parecido e SHA-256 isolado
não provam a origem. Resolver uma referência ao caminho original também não prova
que o conteúdo atual do destino seja o conteúdo histórico observado.

Em `tools/governance/scripts/check-ox.py`, o percurso de Markdown consulta
`log_repair_revision.origin` e resolve links a partir da origem devolvida. O
registro autenticado `docs/validation/log-repair-20261115/governance-origins.json`
abrange capturas anteriores de welcome/folder-picker, mas não estas cinco cópias.
O fallback devolve o próprio caminho da cópia. Assim, links antes válidos passam
a ser interpretados em uma pasta de retenção diferente. O registro anterior e seu
digest permanecem válidos para seu escopo; não devem ser atualizados como se já
incluíssem estas capturas.

Em `scripts/lib/progress.sh`, `progress_end` escolhe `stderr.log` pela existência,
mesmo vazio, e `failed` cai no texto genérico “falha de execução ou relatório
inválido”. A publicação já traduz referências temporárias para nomes retidos em
`progress_finalize`/`progress_log_reference`; deve-se corrigir a seleção e verificar
esse contrato existente, não presumir ausência de publicação. Os streams nativos
permanecem separados e `result.json` continua autoridade do estado/código.

`governance_support.transient` exclui áreas locais/geradas e somente scratch dentro
de validation. Não há justificativa para excluir `docs/validation` globalmente.
Os testes de origem existentes cobrem tamper, symlinks e exclusões limitadas em
cópia; os novos casos devem preservar essas garantias e desafiar o caminho público.

## Métodos realmente consultados

O catálogo `.codex/skills/README.md` foi consultado para duas questões concretas.
As entradas e pontes abaixo foram lidas e aplicadas ao desenho deste plano;
SHA-256 editorial de cada arquivo consta no inventário. As skills não declaram
versão semântica própria; ambas as pontes declaram `bridge_version: 1`.

| Papel e entrada | Caminhos | Questão e contribuição nesta etapa |
| --- | --- | --- |
| Primária: autonomous-verification-engineering | `.codex/skills/autonomous-verification-engineering/SKILL.md`; `sdd/chain/autonomous-verification-engineering.md` | Como evitar falsa aceitação após mudar o gate: critérios com inputs, oráculos independentes, negativos, estado UNVERIFIED e invalidação seletiva. |
| Auxiliar: tool-output-engineering | `.codex/skills/tool-output-engineering/SKILL.md`; `sdd/chain/tool-output-engineering.md` | Como produzir diagnóstico útil sem perder raw/códigos: seleção de streams, fallback conservador, orçamento, sanitização e referência recuperável. |

Não foram carregadas referências adicionais, cadeias recursivas ou outras skills.
Casos abaixo são planejados, não testes já executados.

## Requisitos e critérios futuros

Os IDs GL são locais deste plano; T001 fará seu vínculo aos critérios normativos
das duas features, preservando os IDs e obrigações existentes.

| Requisito / critério | Resultado exigido e oráculo independente | Estado atual |
| --- | --- | --- |
| GL-01: origem exata | As 22 ocorrências resolvem pelos cinco pares revisados; bytes das cópias e do registro anterior permanecem idênticos. Comparação byte a byte + tabela de pares esperados escrita pelo testador + checker real. | UNVERIFIED |
| GL-02: integridade e limites | Registro/cópia alterados, ausentes, duplicados, conflitantes ou com escape/symlink são rejeitados, inclusive após tentativa de recalcular hashes locais. Não listado continua sujeito à regra comum. Corpus adversarial e subprocesso público. | UNVERIFIED |
| GL-03: consumidores | Checkout e cópia de governança independente mantêm seus limites, sem ler o checkout original; exceções anteriores não crescem. Testes de cópia/receipt e leitura isolada. | UNVERIFIED |
| GL-04: diagnóstico útil | Falha `ox` apresenta classe, arquivo/referência quando extraíveis com segurança, quantidade e locator do stream com os diagnósticos. Para o corpus observado, 22 ocorrências em cinco arquivos; repetições não desaparecem. Sem confundir reprovação do checker com relatório inválido. | UNVERIFIED |
| GL-05: projeção conservadora | stdout/stderr, código nativo/runner/agregado e formatos vigentes são preservados. Desconhecido, inválido, vazio ou truncado mantém falha e limitações explícitas; nenhum texto arbitrário executado ou exposto. | UNVERIFIED |
| GL-06: publicação e terminal | Após publicação, locator aponta ao arquivo retido correto e a bytes iguais aos capturados; após falha de publicação, nenhuma referência inexistente é apresentada como confirmada. TTY, redirecionamento, TERM=dumb, NO_COLOR e cancelamento mantêm contratos. | UNVERIFIED |
| GL-07: integração e evidência | Revisão e validação independentes, regressões pertinentes e gates completos das features afetadas com bindings atuais. Observações anteriores não são reetiquetadas nem rehashadas como execução nova. | UNVERIFIED |
| GL-P1: integridade deste plano | Somente a pasta autorizada recebe arquivos; links Markdown novos resolvem a partir dela; nenhum snapshot Markdown deslocado é criado. Inventário, inspeção do diff e checagem documental focada sustentam só a entrega de planejamento. | A avaliar no fechamento documental |

## Decisões propostas e alternativas

**D-01 — registro adicional, limitado e autenticado (GL-01/02/03).** Criar um
registro novo em `docs/validation/governance-link-repair-20261115/origins.json`
durante a implementação autorizada. Conter versão, identificador de revisão,
referência à decisão, vínculo ao digest do registro anterior e os cinco pares
`source`, `origin`, `sha256`. O novo registro terá digest fixado em código revisado,
além de schema e escopo verificados. Não confiar em um hash armazenado apenas ao
lado dos dados que ele verifica. Identificar a proveniência revisada por par no
relatório da mudança. Conservar integralmente o registro antigo e seus 16 pares;
um sucessor não substitui nem amplia `excluded_targets` anteriores.

Integrar a leitura em `log_repair_revision.py` com o mesmo ponto público `origin`.
O registro novo é obrigatório no novo checkout/cópia; ausência não aciona fallback
silencioso. A inspeção de `distribution_files`/`product_record` indica que as cinco
cópias e suas duas origens pertencem à distribuição atual: nenhuma está na lista
de exclusão de produto. T001 deve fechar e registrar essa matriz de presença antes
de T002; T003 a demonstra em cópia real. Fixtures parciais antigas precisam carregar
explicitamente os inputs novos. Não se propõe modo legado sem o registro. Se surgir
um consumidor incompatível, suspender sua implementação dependente e revisar a
decisão de compatibilidade; ausência de arquivo nunca escolhe um bypass.

Validar chaves únicas JSON, schema suportado, tipos, inventário exato, fontes
únicas entre registros, inexistência de pares conflitantes e SHA-256 dos bytes.
`source`/`origin` devem ser caminhos relativos canônicos, não vazios, internos,
sem `..`, absolutos ou componentes symlink. Verificar os componentes lexicais
antes da normalização, também quando o destino final volta para dentro da raiz.
Links continuam passando pela checagem comum de existência/contenção/symlink.
O registro altera a base de resolução; não isenta link quebrado ou alvo externo.
Fontes não registradas continuam com a localização própria e devem falhar se seus
links forem inválidos. Nenhuma heurística por basename, pasta `before`, conteúdo
parecido ou busca pelo primeiro alvo existente é aceitável.

Alternativas rejeitadas: editar/mover/deletar snapshots; mudar extensão para evitar
varredura; excluir validation; adicionar exceções somente ao erro textual; reescrever
o registro antigo e renovar seu pin sem preservar a revisão. Um resolvedor genérico
de todas as linhagens seria maior que a causa observada. Reavaliar a extração de um
módulo comum apenas se T001 demonstrar contratos repetidos incompatíveis.

**D-02 — diagnóstico determinístico, restrito e conservador (GL-04/05).** Selecionar
diagnóstico estruturado válido quando o check o fornece; para `ox`, reconhecer
somente classes conhecidas do checker em stdout/stderr. Se stderr não contém
diagnóstico reconhecido e stdout contém, usar stdout, mesmo com stderr não vazio.
Se ambos contêm diagnósticos, preservar contagem/proveniência por stream sem
inventar ordenação entre eles. Ambos vazios: localizar `result.json` e declarar
diagnóstico indisponível. Saída não reconhecida: manter falha/causa desconhecida,
indicar streams não vazios e não despejar texto arbitrário. Metadados estruturados
inválidos não podem se tornar “sem achados”. Reconhecimento não modifica o exit.

Projetar classe, caminho e alvo apenas quando parseáveis e seguros; nunca reproduzir
mensagem livre, trecho de fonte, credencial ou instrução embutida. Usar sanitização
de controles e validar limites; um campo ambíguo fica indisponível e aponta ao raw.
Proposta de orçamento inicial: até 10 grupos de diagnóstico, campos de até 256
caracteres visíveis e leitura de até 64 KiB por stream. Validar esses limites no
corpus real antes de fixá-los. Contagem total só é “total” se todo o stream foi
processado; leitura limitada deve dizer “ao menos N” e declarar truncamento.
Agrupamento conserva quantidade de ocorrências e identificação dos grupos omitidos
quando conhecida. Não prometer que todos os 22 itens cabem no terminal.

**D-03 — reutilizar publicação, com confirmação por referência (GL-06).** Incluir
todo raw selecionado em `PROGRESS_REFERENCES`; após publicação, conferir que o
locator traduzido existe. Reusar a codificação de `%`, hífen e separador já usada
em `logs.sh`, testando que caminhos com esses caracteres não colidem. Um caminho
temporário pode aparecer durante a fase, mas o fechamento deve fornecer sua
referência retida. “Persistente” significa durante as duas datas da política atual,
não retenção eterna. Falha parcial mantém erro de publicação, referência emergencial
quando realmente disponível e sinal de captura incompleta. Nenhuma rotação real
do histórico do mantenedor é necessária aos testes: usar raízes temporárias.

**D-04 — sucessão documental e aceite separados (GL-07).** Não tocar nos envelopes
atuais nesta etapa. Na implementação, preservar preimages e mapear inputs alterados
para critérios afetados antes de editar autoridades autenticadas. Revisões novas
devem representar observações novas; hashes de observações antigas permanecem.
O plano exige novos testes dos casos afetados, sem promover critérios de scanners,
histórico Gitleaks ou produto. Exits estruturais não aprovam funcionamento.

## Riscos e respostas

| Risco | Controle / tarefa |
| --- | --- |
| R-01: inferir origem errada e mascarar destino inválido | Revisar os cinco pares e sua proveniência; teste esperado independente e novos links quebrados fora/dentro de validation; T001–T003. |
| R-02: novo registry permitir tamper, duplicação ou ausência silenciosa | Pin revisado, schema estrito, escopo exato, casos com hashes recalculados e ausências; T002/T003. |
| R-03: quebrar cópia de governança ou ampliar exceções | Repetir consumidores isolados e comparar allowlist/receipt/exclusões; T003/T005. |
| R-04: vazar segredo/controle pelo resumo | Reconhecimento de campos, sanitização, limites e casos hostis; nenhuma impressão livre de raw; T004/T005. |
| R-05: locator temporário inválido após limpeza ou corrida de publicação | Conferir arquivos publicados, bytes e falhas parciais; manter ownership da publicação e watcher sem novas escritas concorrentes; T004/T005. |
| R-06: sobrescrever mudanças de outras tarefas ou renovar aceite histórico | Hash/precondição por arquivo, dono único, parar diante de drift; sucessão explícita e validação independente; todas as tarefas. |
| R-07: integração mascarar pendências externas | Separar regressão introduzida de falha preexistente, manter estado não aprovado e condição precisa de retomada; T006/T007. |

## Tarefas, dependências e responsabilidade por caminho

Papéis abaixo são atribuições futuras, não agentes já executando implementação.
Cada escritor deve receber pedido, permissões, critérios, bases observadas e caminhos;
não está sozinho no checkout e não pode reverter alterações alheias. Não subdelegar.

| ID | Dono / caminhos exclusivos | Dependência e entrega verificável |
| --- | --- | --- |
| T001 | Coordenador alto: documentação comum, futuro `docs/validation/governance-link-repair-20261115/`, `docs/decisions/governance-historical-links.md`, `sdd/project.md`, artefatos de `configuration-cohesion` e `terminal-progress` | Autorização de implementação. Atualizar inventário do estado real; revisar origem dos cinco snapshots; inventariar demais capturas Markdown dessas tarefas e consumidores sem acrescentar exceções silenciosas. Registrar decisão/sucessão e mapear GL a ACs e bindings existentes. Incluir procedimento de registro de futuras capturas antes de considerá-las validadas. |
| T002 | Implementador de governança: `tools/governance/scripts/log_repair_revision.py`, `tools/governance/scripts/check-ox.py`; `governance_support.py` somente se integração de cópia comprovadamente exigir | T001. Ler o novo registro criado pelo coordenador, aplicar validação estrita e preservar guardas anteriores. Nenhuma escrita nos cinco snapshots ou no registro antigo. Mudança da allowlist exige decisão explícita, não remendo automático. |
| T003 | Testador: `tools/governance/tests/test_log_repair_revision.py`, novo `test_historical_link_resolution.py`, `test_instruction_copy.py` e fixtures estritamente necessárias | T001 para desenhar casos; T002 para execução. Implementar positivos/negativos independentes, cópia sem acesso à raiz e rejeição pública. Registrar comandos, exits, inputs, raw e limitações. |
| T004 | Implementador de terminal: `scripts/lib/progress.sh`; `scripts/automate.sh` e `scripts/lib/logs.sh` só se necessário ao locator confirmado, com justificativa | T001; pode ocorrer em paralelo a T002 se capacidade permitir. Seleção de streams e projeção segura; reaproveitar publicação. Contratos de processo, gate e catálogo preservados. |
| T005 | Testador: `scripts/tests/test_terminal_progress.py`, `test_terminal_publication.py`, novo `test_governance_diagnostics.py`; regressões de `test_terminal_style.py`, `test_capture_status.py`, `test_process_lifecycle.py`, `test_local_lifecycle.py` | T004; T002 para cenário integrado. Corpus real mínimo e fixtures adversariais; executar casos TTY/plain, códigos, raw, publicação e falhas. T003/T005 podem usar o mesmo testador em sequência; testes não viram o único oráculo de si mesmos. |
| T006 | Revisor independente: leitura de todos os caminhos; observações devolvidas ao coordenador | T002–T005 estabilizadas. Examinar contratos, bindings, rejeições, segredos e consumidores; achados retornam ao dono, sem escrever implementação. |
| T007 | Validador alto independente: leitura e verificações autorizadas; coordenador integra documentação/evidência | T006 resolvida. Confrontar cada GL/AC com evidências dos inputs finais, avaliar oráculos, executar gates selecionados, registrar cinco estados e limites; nenhum aceite por declaração de agente. |
| T008 | Coordenador: `scripts/README.md`, `docs/development/governance.md`, `docs/development/local-artifacts.md` se comportamento documentado mudar; demais documentos comuns de T001 | Incrementalmente antes de fechar cada tarefa; conclusão após T007. Registrar disposição documental, exemplos/links conferidos, pendências e retomada. Alteração em fonte autenticada exige sucessor delimitado e preimage. |

O coordenador também é dono de `origins.json` e seus pins documentais; o implementador
de governança integra o pin em código somente após transferência explícita dos bytes
estabilizados. O testador não altera produção. Helpers adicionais exigem atribuição
de caminho antes da escrita. O registro antigo e snapshots são leitura apenas para
todos. Uma alteração concorrente invalida a base daquele arquivo: preservar o novo
estado, reconciliar com o dono e repetir somente observações dependentes.

## Verificação planejada

**V-01 / GL-01/02.** Oráculo manual independente com os cinco pares e as 22
ocorrências da captura, sem importar a tabela esperada do registro candidato.
Resolver referências do corpus e exigir que cada uma aponte ao alvo previsto.
Comparar bytes dos snapshots/registro antigo antes/depois. Introduzir em cópias
descartáveis: fonte alterada/ausente, registry ausente/alterado, SHA errado ou
recalculado, campos/tipos/schema inválidos, chaves JSON e fontes duplicadas,
conflito entre registros, origem absoluta/com `..`, fonte e origem com symlink,
symlink no alvo ou ancestral, caminho codificado que escape, alvo ausente e link
novo quebrado num arquivo comum e num snapshot não registrado. Todos os negativos
devem falhar com diagnóstico, sem bypass de validation. Exercitar fixtures válidas
para não atribuir rejeição por pin incorreto a um teste que pretendia testar schema.

**V-02 / GL-03.** Cópia pelo mecanismo existente, com receipt e allowlist atuais,
em diretório temporário, sem acesso à raiz original. Exigir novo registro/snapshots
necessários, testar ausências/symlinks/receipt adulterado e preservar as 12 exceções
exatas anteriores para destinos excluídos. Tentar uma 13ª exceção desconhecida deve
falhar. Não gerar/publicar pacote real para provar cópia isolada; se o contrato de
archives for alterado, acrescentar teste de archive temporário autorizado.

**V-03 / GL-04/05.** Corpus com stderr vazio + 22 erros no stdout; stderr com ruído
e stdout com erros; só stderr; ambos com diagnósticos; ambos vazios; bytes inválidos,
ANSI/OSC/CR, texto de instrução, credencial sintética, nomes ambíguos/longos, formato
desconhecido, arquivo ilegível/ausente e stream maior que o orçamento. Conferir
classe, contagem exata ou limite inferior explícito, seleção/identidade do stream,
causa desconhecida quando não demonstrada, e ausência de vazamento no terminal.
Comparar hashes raw antes/depois, estado/códigos de processo e JSON de plan/result.
Formato/arquivo inválido não pode produzir sucesso. Um caso com erro deliberadamente
removido do resumo deve ser pego pelo oráculo (mutação controlada).

**V-04 / GL-06.** Runner real com ferramentas simuladas; verificar locators após
remoção do run temporário, nomes escapados e conteúdo. Publicação lenta, parcial,
falha, colisão, mudança de data e cancelamento; não introduzir escrita no diretório
do publisher pelo heartbeat. Confirmar que total 100% não representa aprovação e
não surge antes de publicação confirmada. Testar TTY real de fixture, saída
redirecionada, TERM=dumb e NO_COLOR. Não executar scanners reais para esses casos.

**V-05 / GL-07.** Após estabilizar código, testes e documentos, rodar checks pertinentes
e obter review/validação independentes. Comandos abaixo são plano de execução futura,
confirmados contra guias e layout atual; confirmar novamente ao retomar. Cada
execução deve guardar comando, cwd, ambiente relevante, exit, stdout/stderr, hashes
de implementação/oráculo/configuração/fixtures/contratos e limitações. Capturas novas
ficam no registro futuro conforme política; nenhuma cópia Markdown deslocada sem
origem revisada. Não chamar um teste controlado de homologação de scanners.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools/governance/tests -p 'test_*historical*py' -v
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools/governance/tests -p test_log_repair_revision.py -v
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools/governance/tests -p test_instruction_copy.py -v
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s scripts/tests -p test_governance_diagnostics.py -v
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s scripts/tests -p 'test_terminal*.py' -v
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=scripts/tests python3 -m unittest -v test_capture_status test_process_lifecycle test_local_lifecycle
bash -n scripts/lib/progress.sh scripts/automate.sh scripts/lib/logs.sh
PYTHONDONTWRITEBYTECODE=1 python3 tools/governance/scripts/check-ox.py
PYTHONDONTWRITEBYTECODE=1 python3 sdd/tools/validate.py --root . --structure-only
PYTHONDONTWRITEBYTECODE=1 python3 sdd/tools/validate.py --root . --features sdd/features --feature configuration-cohesion --feature terminal-progress --require-approved --require-fresh --check-convergence
```

Padrões dos testes novos devem corresponder a casos reais e não aceitar “0 tests”
como verificação. Acrescentar a suíte de governança documentada quando os testes
focados passarem, pois há consumidores compartilhados. A ampliação não inclui o
pipeline completo. Um `check-ox.py` global ainda rejeitado por causa independente
impede afirmar gate verde; registrar causa, inputs e condição de retomada sem
ocultar o erro. O teste público do corpus deve passar após correção e voltar a
falhar diante das mutações deliberadas, não apenas verificar funções auxiliares.

Verificação completa só se o mantenedor a autorizar separadamente. Nesse caso usar
exatamente o ambiente Toolbox/SELinux/Cargo de `AGENTS.md` na raiz; não inferir
download, manutenção central ou permissão de escrita externa dessa autorização.
Nada nesta entrega executa o comando completo ou solicita essa autorização.

## Capacidades, revisão desta entrega e retomada

Na sessão de planejamento foram observadas ferramentas de criação por perfil,
contexto novo, mensagens, listagem e interrupção; o limite informado é quatro
agentes contando a raiz. Raiz + coordenador deixam no máximo dois especialistas.
Não foi observada operação de encerramento que assegure liberar vaga; término ou
interrupção não prova disponibilidade. Revisão independente deste plano deve usar
contexto próprio, somente leitura, sem subdelegação; o coordenador integra achados
na pasta autorizada. Na implementação futura, reservar contextos independentes
para revisor e validador, sequenciando se necessário. Ausência dessas capacidades
bloqueia o aceite material, não transforma autorrevisão em validação.

Retomada: obter autorização de implementação; ler este plano e seu fechamento;
comparar `planning-inputs.json` aos bytes atuais; reconciliar mudanças e disponibilidade
das capturas locais, sem copiar hashes antigos para observações novas. Se os logs
expirarem pela retenção, os hashes deste inventário não recuperam conteúdo: coletar
novo diagnóstico focado autorizado. Executar T001, atribuir arquivos e só então
iniciar implementação. Não é necessário pedir confirmação para cada ação reversível
que a autorização futura efetivamente cobrir. Se faltarem origem demonstrável,
capacidade independente ou permissões externas necessárias, manter os respectivos
critérios UNVERIFIED e registrar a condição exata, prosseguindo em trabalho independente.

## Disposição documental desta etapa

Consultados `README.md`, `scripts/README.md`, `docs/development/governance.md`,
`docs/development/local-artifacts.md`, `sdd/project.md`, specs de
`configuration-cohesion`/`terminal-progress` e relatórios de terminal-style e
history-correction. Não há mudança atual de comportamento, CLI, retenção ou estado
de aceite; por isso esses documentos e autoridades autenticadas permanecem intactos.
As atualizações futuras estão atribuídas em T001/T008. Esta pasta registra o escopo
planning-only e satisfaz o fechamento documental sem renovar autorizações antigas.

O fechamento em [review.md](review.md) deve registrar revisão independente e a
checagem focal dos links/inventário desta pasta. Não foram executados por esta
coordenação testes funcionais, pipeline completo, cópia independente, aceite SDD
ou implementação. O defeito continua presente até a execução autorizada do plano.
