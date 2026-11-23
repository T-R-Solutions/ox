# Remediação R3 — registro em andamento

Estado: **INCOMPLETO**, sem aceite global. Este relatório descreve a disposição corrente. As versões anteriores, falhas, preimages e observações permanecem retidas; nenhuma observação antiga teve hashes renovados para aparentar atualidade.

## Escopo e responsabilidades

R3-1, R3-2 e R3-3, disposição explícita dos 31 itens R3-4 e execução do inventário obrigatório. `claude_analysis.md` permanece histórico. Não houve commit, push ou publicação. Alterações preexistentes foram preservadas. A rota é completa/alta: coordenador responsável por governança, SDD e artefatos comuns; raiz pelos três harnesses nativos e execuções atribuídas; revisão e validação em contextos independentes.

Autorizações adicionais específicas: refresh OSV pelo Toolbox; aquisição exata de lru 0.18.5; nova geração RustSec no commit `472a4c9a785030434f15d7da84964d60fbe789ab`. Não autorizam outras aquisições ou manutenção central geral. A renderização usou Firefox já presente na imagem local Playwright, sem download de navegador.

| Achado | Correção integrada | Evidência e pendência atual |
| --- | --- | --- |
| R3-1 | Fixtures e expectativas confrontadas com contratos; negativas desafiam seções protegidas, não contexto legítimo. Fechamento de AGENTS/SDD/skills exige governança integral. Reuso de observação limitado à operação, com readset validado e revogação; orçamento operacional de 300 s do checker histórico calibrado e revisado | Integral candidata inicial: 257 testes, 16 falhas. Focais posteriores passaram, mas não substituem a integral. Tentativas interrompidas permanecem incompletas; nova full integral e entradas adicionais finais ainda necessárias |
| R3-2 | Log obrigatório; fronteira exata do produto IDE em ZIP/export/cópias; inventário externo finito para o ZIP, serialização canônica e EOF, limites por membro/aninhamento e modos 644/755 preservados | Named regressions e focais de pacote passaram. Falha antiga de 128 MiB preservada. Geração, extração, cinco comandos documentados na cópia e exportação final continuam pendentes |
| R3-3 | Contratos por seção/identificador para as três autoridades vivas; identidade histórica separada. Um registro schema 2 versionado representa cinco sucessões de oráculos/convergência como dados, sem nova constante Python para cada atualização | ADRs e revisão independentes; 35 testes da última âncora passaram. Demonstração03 satisfez sete oráculos reais, com 59 executores estáveis antes/depois. Não equivale a exportação ou suíte integral. T09-3/T10-2 continuam reabertos até verificação final |
| R3-4 | Os 31 itens mantêm disposições explícitas e respectivas condições de retomada | Não autoriza implementar toda a Parte 2, apagar corpora ou modificar o Toolbox central. Harnesses/vendor são integrações delimitadas necessárias ao inventário |

O registro de sucessão demonstra consistência e proveniência declarada sob revisão/VCS confiáveis, não autenticação criptográfica de autorização. Reescrita coerente de todo checker/registro não é detectável universalmente. A reutilização de observações não oferece atomicidade contra um escritor hostil; verifica bytes/caminhos, limita a vida do contexto e reabre o readset ao sair. Esses limites permanecem explícitos nas decisões.

## Integrações complementares e observações atuais

- Harnesses desktop08/Python04 integrados após revisão independente. Os seis testes X11 finais passaram explicitamente, sem ignored/filtered; ambas as entradas Wayland finais foram executadas. Binário observado: `39d517bb89494ba73725c4da2e7e7fd8b326f1abd3c38dce21a88a3593e03f86`. As imagens finais confirmam correto → não verificado após mudança de inputs → reprovado, cancelamento inconclusivo, expansão/recolhimento e interação durante execução/verificação. A área de histórico/inputs fora da captura não recebeu aceite por inferência.
- WC07 completou sete sessões naturais e 100 checks. A inspeção encontrou menu aberto após clique externo em 2560; o driver não tinha oráculo semântico para esse fechamento. Uma nova repetição com a mesma sequência de recentes mostrou fechamento e foco em Arquivo, com revisão independente. AC02 recebeu APPROVED no ambiente observado, combinando essa prova aos testes atuais de modalidade, despacho e título e às geometrias WC07. As três imagens posteriores da nova repetição reutilizam uma amostra: não medem latência, e a causa retrospectiva do frame WC07 continua indeterminada. O mantenedor aprovou somente o julgamento visual AC07 do conjunto vinculado; evento, índice imutável e 53 inputs foram validados independentemente. Isso não aprova técnica, direitos ou a tarefa inteira.
- O patch local de cryoglyph 0.1.0 usa lru 0.18.5 para remover a versão vulnerável observada. Origem e licenças foram preservadas. Dois casts identificados pelo scan foram substituídos por conversões bytemuck, sem novas supressões. Runner integrado: quatro testes reais de layout e duas rejeições específicas, todos os oráculos satisfeitos. Não comprova GPU runtime, exemplos ou benchmarks.
- RustSec foi preparado pela entrada mantida em raiz descartável e promovido com lock/precondição, preservando geração anterior e o máximo de cinco dias. Probe do lock final: zero vulnerabilidades e dois avisos já nomeados na política, sem exceções novas. Segurança final permanece uma obrigação separada.
- Renderização final: 49 vistas e 11 figuras, com duas exportações SVG corrigidas a partir das fontes Mermaid existentes. Inspeção independente cobriu as seis páginas alteradas e figuras em combinações selecionadas, não todas as vistas manualmente nem tecnologia assistiva. Checker de assets: 262 links e 11 SVG, zero falhas. Tentativas e limites em `documentation-render/`.
- Ruff02 foi bloqueado antes do scanner, exit 3/INPUT_INVALID: a guarda ainda fixava as versões antigas dos dois drivers Python. Revisão de segurança e validação independentes autorizaram somente os dois bindings atuais; políticas, baseline e seleção permaneceram idênticas. Delta integrado em `static-native-binding-integration/`. Ruff e Bandit reais passaram com zero achados finais, reports válidos e 139 inputs estáveis; a baseline permaneceu idêntica. As métricas Bandit anteriores à baseline registram 68 ocorrências, portanto não se afirma ausência de ocorrências brutas. Nova full continua necessária.

## Execuções interrompidas e gates

Full01, módulo histórico final01 e focal instruction final01 terminaram em 143 sem sinal enviado pelos respectivos executores e sem causa estabelecida. Seus resultados são incompletos. A focal preservou cinco métodos concluídos e o sexto em andamento; nenhum resumo de suíte foi produzido.

Full02 terminou deliberadamente em 130 após SIGINT da raiz, registrado em journal, porque a guarda estática comprovadamente inválida impedia scanners obrigatórios e exigia correção da configuração. Não foi interrupção por duração nem aprovação de subconjunto. Os 1196 inputs antes/depois permaneceram iguais; processos restantes foram conferidos. A nova full deverá executar a seleção integral com os bindings finais.

O gate observado das 19 features retornou exit 1, com 92 critérios INCONCLUSIVE e 30 UNVERIFIED naquela execução. A contagem não representa 122 novos defeitos: o crosswalk distingue prova operacional, vínculo documental pendente e lacuna efetiva. Atualizações serão feitas por critério, preservando envelopes históricos. AC07 recebeu apenas o aceite visual explícito que lhe corresponde. O primeiro envelope omitiu cinco bindings obrigatórios e a convergência; check-ox06 rejeitou essa composição, e a falha foi preservada. O envelope incompleto permanece inalterado em histórico; a nova inspeção V2 vincula o contrato e T011 estabilizada. AC02 e AC07 têm projeções coerentes. A validação fresca da feature passou, mas o gate completo ainda retorna 1 pelos outros cinco critérios INCONCLUSIVE.

`maintenance-001` AC05 permanece INCONCLUSIVE: a condição de confirmação dos direitos de terceiros ainda não foi satisfeita. Licenças do vendor e aprovação estética não resolvem essa obrigação. As decisões F0-D4, perfil 31 e bootstrap-implemented são sucessores expressos dos respectivos estados antigos, sem dispensar outras provas ou conceder publicação.

## Próximas verificações e fechamento

Executar nova full integral, pacote com extração e cinco comandos, exportação real e seus checkers públicos, opt-in real final e demais entradas do inventário. Interpretar achados, skips, negativos e inputs; exit zero isolado não é aceite.

`verification-matrix.md`, `root-checks/report.md` e os subdiretórios de observações preservam comandos, ambientes, exits e limitações. Novos streams operacionais ficam fora do checkout enquanto as verificações observam o corpus. Após os resultados finais: atualizar decisões sustentadas, executar gates completos, conferir documentação e anexar o registro completo a `task_finalizada.md`, preservando todo prefixo. O registro final desta execução ainda não foi anexado.

## Adendo: preflight estrito e reparos delimitados

O Clippy do catálogo revelou falhas que o comando padrão anterior não cobria.
As duplicações de hashbrown/miniz já existiam no lock inicial; LRU já usa std.
Foi integrado o patch PNG 0.18.1 que remove somente uma dependência direta sem
uso, preservando fontes, licenças, testes, exemplos e benches. Quatro oráculos
públicos passaram no original e no patch. A suíte upstream não foi executada: o
pacote não inclui seu corpus e faltam dependências de desenvolvimento no cache.

Quatro reparos UI foram independentemente revisados e integrados pela raiz:
nomes de parâmetros, extração local de pintura, conversões/FMA caracterizados
e empréstimo const do evento de drag. A matriz registra as tentativas da
proposta; as observações nativas antigas continuam vinculadas ao binário antigo
até a reexecução. Não são implementação geral da Parte 2.

Hashbrown permanece um erro obrigatório do Clippy. O mantenedor recusou a
aquisição exata proposta de indexmap; nenhuma exceção foi adicionada e nenhuma
aquisição ou fork foi substituído. A verificação integral ainda será executada
com esse impedimento explícito, sem declarar a tarefa concluída.


## Checkpoint de interrupção solicitada — 2026-11-19

Estado **INCOMPLETO**: o usuário informou desligamento do computador em30min; a
execução foi encerrada controladamente para preservar resultados. Não é timeout
técnico nem conclusão da tarefa. Full03 foi interrompida para o desligamento informado pelo usuário: SIGINT2 recebido em2026-11-19T18:43:40.550436Z, término18:43:40.776806Z, exit130,31793.396s. Os1428inputs observados antes/depois não diferiram; supervisor/helper mantiveram SHA. A governança ficou parcial, sem resumo agregado; nenhuma fase posterior ou suíte integral foi aprovada por essa tentativa.

[Checkpoint e retomada](shutdown-checkpoint-20261119/checkpoint.md) registram os
lançadores preservados, inputs, processos e etapas pendentes. [Observações nativas
atuais](root-checks/native-ui03/report.md) continuam vinculadas aos próprios inputs.
O último gate ANTES deste checkpoint/anexação terminou1 com118estados pendentes
em19features, sem erro de bindings/freshness; freshness após append não observada.
Clippy do catálogo101/hashbrown, direitosAC05 e demais critérios pendentes não foram
dispensados. GUIconsumer final, quickskills, opt-in real final, pacote/export/demo,
discovergovernança explícito da raiz emS1 e guardasS2 continuam não executados.
O registro append-only de atividade documenta trabalho/interrupção, não aceite.
Nenhuma tarefa T003/T004/T005 é marcada concluída por este checkpoint.


### Adendo factual após a retenção inicial

Os logs internos foram publicados pelo finalizador e encontrados:18arquivos exatos
retidos em root-checks/full-final-03/published, com publication-retention.json.
partial-governance-observation.json registra268linhas de execuções nomeadas OK,
0linhas FAIL/ERROR e AUSÊNCIA de resumo final da suíte. Há IDs duplicados do loader;
não são268testes únicos nem aprovação integral. O caso efetivamente interrompido
foi test_ui_metadata_inventory.MetadataInventoryTests.test_corruption_and_deletion_fail_for_new_and_existing_metadata.
Os dois testes nominais R3-2 e o longo teste de snapshots terminaram OK nessa tentativa
parcial; o restante não foi aprovado por inferência. Não houve perda desses raws.

Revisão e validação independentes conferiram o checkpoint inicial integrado:
28retenções,4adendos documentais e prefixo38189+append5486=43675bytes do log, links
e ausência de placeholders. Pareceres limitados à preservação/coerência do checkpoint,
sem aceite técnico R3. SuíteS1 e guardas terminaisS2 NÃO foram executadas.


- Complemento dos resultados publicados da full03: sdd-structure e ox terminaram
  passed/exit0. governance-tests ficou failed/cancelled=true/signalINT,exit130,
  child_exit_code143. Esse143interno ocorreu sob cancelamentoINT conhecido e não
  se confunde com as tentativas históricas143 de causa desconhecida.
  product_acceptance=false. omitted[] não comprova execução das fases posteriores;
  o stderr declara restantes não executadas. Mantém-se INCOMPLETO, sem resumo da suíte.
