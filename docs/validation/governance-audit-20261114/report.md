# Auditoria de agents, SDD, skills e AGENTS — 14/11/2026

O problema principal é a divergência entre representações do mesmo contrato: há
aprovação ainda apresentada como atual em Markdown quando o JSON já a invalidou,
um comando de gate antigo na skill de commit e instruções de reutilização que
produzem caminhos inválidos. Não foi encontrado um conflito geral entre
“ser detalhista” e “resumir”. As entradas normalmente pedem detalhe proporcional
ao risco e ao tipo de entrega.

Escopo autorizado: analisar o checkout atual e registrar o diagnóstico. Nenhuma
política, skill, configuração, evidência anterior ou implementação foi corrigida.
Este relatório é o único arquivo criado. As numerosas alterações preexistentes
foram preservadas. Não houve commit, publicação ou verificação completa.

## Método e cobertura

Rota local de auditoria, sem mudar contratos. A complexidade da interpretação é
alta; isso não transforma uma análise em autorização para refatorar a governança.
Foi aplicado o método de `engineering-productivity`, entrada
`.codex/skills/engineering-productivity/SKILL.md`: comparar a regra com o efeito
observável, distinguir impedimento de preferência e não inventar ganho de tempo,
tokens ou qualidade. As demais skills foram lidas como objetos da auditoria;
essa leitura não significa execução dos seus métodos.

Cobertura realizada:

- AGENTS.md da raiz, busca de AGENTS/overrides nos ancestrais e de AGENTS no
  conteúdo do projeto fora de caches/temporários. Não foi encontrado outro
  AGENTS aplicável nesses locais.
- Os 13 perfis TOML, a configuração de entrada, procedimento canônico, guia de
  replicação, registro SDD e relatório da instalação dos agentes.
- Os 31 SKILL.md completos, 31 metadados `agents/openai.yaml`, catálogo, perfil
  versionado, 31 pontes e seu índice. As entradas de skills somam 1.994 linhas.
- Workflow, evidence, README, constitution, project, seis arquivos de templates
  e implementação do checker SDD nas rotas relevantes.
- Inventário de todos os 183 arquivos das skills: 152 Markdown e 31 YAML.
  Os 120 Markdown de recursos internos tiveram busca transversal de instruções
  e verificação de links pelo checker; referências pertinentes aos achados foram
  lidas integralmente. Não se alega releitura semântica integral de todos esses
  recursos nem revisão de toda fonte bibliográfica externa.
- Inspeção dos 39 envelopes `evidence.json`, busca de divergências com converge,
  leitura dirigida dos registros conflitantes e autoridades/consumidores
  relacionados. Os 39 históricos de features não foram reexecutados.

O corpus é o estado de trabalho, incluindo arquivos modificados e não rastreados,
e não apenas HEAD. A análise não mede obediência, latência ou custo dos modelos.
Não houve ensaio de toda a árvore de agentes. A restrição vigente da sessão a
novas delegações foi respeitada neste contexto de auditoria; não há parecer de
revisor independente desta entrega.

## Achados prioritários

### A01 — Alta: convergência atual diverge da evidência atual

Em [configuration-cohesion/converge.md](../../../sdd/features/configuration-cohesion/converge.md),
linhas 5–7, AC-01/02/03 estão `APPROVED`; o texto ainda fala em “Current feature
acceptance”. Entretanto, [evidence.json](../../../sdd/features/configuration-cohesion/evidence.json),
linhas 8, 14 e 20, contém `INCONCLUSIVE`, sem evidências ativas, explicando a
invalidação de inputs em 13/11.

Em [skill-agent-runtime-engineering/converge.md](../../../sdd/features/skill-agent-runtime-engineering/converge.md),
linhas 1–8, o título é “Current convergence” e os seis critérios estão `APPROVED`.
No [envelope atual](../../../sdd/features/skill-agent-runtime-engineering/evidence.json),
linhas 8–56, os seis estão `UNVERIFIED`. A busca encontrou a mesma forma de
divergência nas nove especializações; outras ocorrências em registros com
sucessores históricos não devem ser promovidas automaticamente a novos defeitos.

**Efeito:** uma retomada que lê converge pode partir de uma aprovação inexistente
nos inputs atuais; outra que lê JSON chega à conclusão oposta. Isso afeta
diretamente a regra de retomada do workflow. O checker padrão e check-ox passaram
apesar dessas divergências: esses passes não reconciliam a projeção Markdown.

**Correção mínima:** manter a observação antiga identificada como histórica e
acrescentar um estado atual consistente, com referência ao envelope vigente.
Definir uma fonte do estado atual e verificar suas projeções, preservando os
relatos antigos. Não “corrigir” promovendo o JSON a APPROVED ou renovando hashes.

### A02 — Alta: a skill de commit executa uma seleção legada diferente da regra atual

[commit-governance/SKILL.md](../../../.codex/skills/commit-governance/SKILL.md),
linha 111: `bash scripts/automate.sh --scope full`.
[AGENTS.md](../../../AGENTS.md), linhas 29–41: toda verificação completa autorizada
neste checkout usa Toolbox/Cargo explícitos e `./scripts/automate.sh run --scope complete`.
[scripts/README.md](../../../scripts/README.md), linhas 93–105, confirma o comando
atual e identifica a forma sem subcomando como compatibilidade legada.

**Observação reproduzida somente com plan:** o full legado selecionou 16 checks;
o complete atual selecionou 26. Os dez adicionais são `coverage`, `geiger`,
`grype`, `history`, `malware`, `sbom`, `scripts-syntax`, `scripts-tests`,
`shellcheck` e `trivy`. Além disso, `scripts/automate.sh:109` só chama a preparação
automática de ambiente no ramo não legado. A receita da skill não fornece os
overrides exigidos pelo AGENTS.

**Efeito:** o “Sim” do gate leva a um escopo diferente do documentado como completo
e pode depender de um ambiente não preparado. Não se observou falha de scanner,
pois nenhum foi executado; o desvio de seleção é confirmado.

**Correção mínima:** a skill deve continuar dona da pergunta e do bloqueio de
commit, mas encaminhar o comando/ambiente para a autoridade operacional atual.
Não substituir apenas `full` por `complete` mantendo a sintaxe legada.

### A03 — Média: os templates geram links quebrados após a cópia recomendada

[templates/README.md](../../../sdd/templates/README.md), linhas 3–4, manda copiar
os templates para a feature. [templates/spec.md](../../../sdd/templates/spec.md):14
usa `../evidence.md`; [templates/tasks.md](../../../sdd/templates/tasks.md):13 e
[templates/checklist.md](../../../sdd/templates/checklist.md):10 usam `../workflow.md`.

Esses caminhos funcionam em `sdd/templates/`. Em `sdd/features/<feature>/`,
resolvem para `sdd/features/evidence.md` e `sdd/features/workflow.md`, inexistentes.
A resolução foi reproduzida sem alterar as fontes.

**Efeito:** um agente pode seguir o procedimento de criação e introduzir uma
falha de links no gate. A aprovação estrutural dos templates na origem não cobre
seu uso no destino.

**Correção mínima:** explicitar a adaptação de links na cópia e verificar o
destino, ou fornecer mecanismo de instanciação que os ajuste. Não criar cópias
concorrentes de workflow/evidence na pasta features para satisfazer os links.

### A04 — Média: o checker confunde limite de portabilidade com limite do projeto

[sdd/README.md](../../../sdd/README.md):12–14 orienta reutilizar a constituição e
os documentos existentes. Em [sdd/tools/validate.py](../../../sdd/tools/validate.py):426–442,
`markdown_errors(folder)` exige que todo link local permaneça dentro de `folder`;
a chamada em `audit`, linha 544, passa a pasta SDD, não a raiz do projeto.

**Reprodução isolada:** uma árvore temporária com `docs/constitution.md` válido e
`sdd/constitution.md` contendo um link Markdown para `../docs/constitution.md` recebeu
`Nonportable or missing link`. A referência permanece dentro do projeto.
O [relatório da instalação de agentes](../codex-agents-20261114/report.md) já
registra a mesma limitação e o contorno por caminhos em texto simples.

**Efeito:** links navegáveis para autoridades legítimas são recusados, incentivando
texto não clicável. É uma restrição real do checker; não implica quebra atual,
porque os documentos existentes já usam contornos.

**Correção mínima:** distinguir link ausente/escapando do projeto de dependência
externa ao pacote portátil. Tratar portabilidade como modo/contrato separado ou
documentar claramente os dois limites, preservando as verificações de escape.

### A05 — Média: a receita de adoção do SDD copia mais que o modelo portátil

[sdd/README.md](../../../sdd/README.md):9 manda copiar “this directory's contents”.
No checkout atual isso inclui as 39 features Ox, suas evidências, `project.md`
preenchido e as 31 pontes. O passo 4, linhas 19–21, manda escolher apenas as
pontes necessárias e não copiar todo o catálogo. A mesma página ainda descreve
o layout da biblioteca de origem `sdd/model/`, que não é o layout local atual.

**Efeito:** seguir literalmente o primeiro passo leva contratos e referências
específicos do Ox para o novo consumidor antes da seleção prometida. Não foi
realizada uma instalação de destino; o conjunto que seria copiado é observável.

**Correção mínima:** separar o guia de uso deste checkout da receita de extração
do modelo. Enumerar os arquivos-base e exigir escolha explícita de features e
pontes. Manter a proveniência da biblioteca identificada como histórica.

### A06 — Média: não há seleção automatizada de uma feature individual

[sdd/tools/validate.py](../../../sdd/tools/validate.py):355–423 só percorre os
diretórios filhos do argumento `--features`. Passar
`sdd/features/configuration-cohesion` com aprovação requerida retorna
`No feature directories found`; passar `sdd/features` aplica os gates a todas as
features. O conjunto atual tem 39 envelopes, com 130 requisitos INCONCLUSIVE,
77 UNVERIFIED e dois APPROVED. Essas contagens incluem todos os objetos de
requirements, não somente uma seleção de gates normativos.

O [procedimento dos agentes](../../development/codex-agents.md):166–172 já explica
a limitação e permite parecer manual para o recorte não selecionável.

**Efeito:** não é um bloqueio inevitável, pois há fallback documentado, mas exige
um caminho manual para uma necessidade comum: aceitar apenas a feature alterada.
As instruções repetidas para rodar `--require-approved --require-fresh` precisam
sempre recuperar essa exceção para não cobrar aprovação global indevida.

**Correção mínima:** oferecer filtro de feature/critério mantendo a validação dos
inputs e dos gates selecionados. Até lá, conservar explícita a distinção entre
parecer manual e aceite automatizado; não mover features para ocultá-las.

## Ambiguidades e custo de manutenção

### A07 — Média: o papel do triador mistura proibição geral e exceção da raiz

[ec_triador.toml](../../../.codex/agents/ec_triador.toml):8–10 diz que sua função
é somente classificar e que não deve criar agentes. O
[procedimento canônico](../../development/codex-agents.md):68–73 manda a raiz
aplicar diretamente esse papel e encaminhar a execução ao orquestrador, reservando
“sem filhos” ao triador chamado como especialista.

Há interpretação coerente: a raiz atua também como controlador e o especialista
não delega. Porém essa exceção não está na própria proibição do TOML; só o final
do perfil distingue “se estiver delegado”. **Risco, não deadlock observado:** um
cliente pode aplicar literalmente a proibição ao controlador raiz.

**Correção mínima:** qualificar a proibição como aplicável ao triador delegado e
explicitar a responsabilidade adicional da raiz, sem duplicar todo o procedimento.

### A08 — Média, decisão de processo: tarefas locais dependem da capacidade multiagente

O workflow oferece execução local proporcional. A configuração raiz e o
procedimento dos agentes, linhas 68–73, impõem encaminhamento ao orquestrador;
linhas 37–38 e 101–117 exigem independência de revisão/validação e bloqueio quando
o contexto/perfil necessário não estiver disponível. Não há exceção explícita
para correção documental trivial ou investigação sem implementação.

**Efeito deduzido da regra:** mesmo uma tarefa simples pode depender de capacidade
de criação/liberação de agentes. Isso é uma escolha de política, não evidência
de que o modelo está lento nem contradição automática com a rota SDD: o documento
separa as duas classificações. O custo real não foi medido.

**Decisão sugerida:** explicitar se tarefas de baixo risco podem ter execução
direta/revisão proporcional e quando independência exige outro contexto. Alterar
isso muda o contrato escolhido para os agentes e precisa ser tratado como tal;
não deve ser removido como mera limpeza editorial.

### A09 — Baixa: regras comuns continuam distribuídas em muitas cópias

Contagem exata por linha no corpus atual:

- 26 pontes repetem o bloco de conclusão que remete a workflow/evidence.
- 13 pontes repetem o preâmbulo de consulta da skill.
- 13 SKILL.md repetem o mesmo parágrafo sobre especialistas opcionais.
- As nove especializações repetem quatro parágrafos comuns de inputs, evidência,
  handoff e proveniência; suas tabelas adjacentes ainda repetem parte do handoff.
- `prompt.md` e `distributed-systems.md` nas pontes conservam a seção antiga de
  conclusão e também o novo bloco compartilhado ao final.
- Os validadores TOML repetem comandos e exceções de verificação já mantidos no
  procedimento comum, que por sua vez reproduz a tabela por rota de evidence.md.

**Efeito:** mais locais precisam mudar juntos; A02 demonstra concretamente a
classe de drift de comando. A repetição por si só não comprova perda de qualidade.
Skills distribuídas isoladamente precisam conservar limites e método suficientes;
eliminar todos os avisos comuns criaria dependências ocultas.

**Correção mínima:** centralizar comandos e política Ox em suas autoridades;
manter nos perfis responsabilidades e nas pontes contribuições específicas.
Conservar contexto mínimo nas skills portáteis. Remover primeiro as duplicações
dentro do mesmo arquivo, evitando um “arquivo comum obrigatório” para toda skill.

### A10 — Média: o estado atual está misturado a uma cronologia extensa

[sdd/project.md](../../../sdd/project.md) tem 453 linhas/26.857 bytes. O trecho
“Current state”, linhas 55–61, ainda resume “a minimal window” e escopo
`product-bootstrap`; abaixo há sucessões para UI local, workbench visual e outras
entregas. Cabeçalhos “Active authorized slice” de outubro permanecem no corpo.
O [contexto arquitetural](../../architecture/context.md), seção “Visual composition
successor”, já registra 27 destinos e os limites atuais da composição.

**Efeito:** um leitor da entrada atual pode trabalhar com um resumo incompleto ou
tratar restrição histórica como proibição presente. A busca da regra vigente exige
reconciliar a cronologia. Não se deve apagar a história ou transformar seus pedidos
em nova autorização para esta sessão.

**Correção mínima:** manter no topo um resumo atual curto, com data, escopo e
links para sucessores; rotular claramente o restante como histórico. Preservar
identidades das observações antigas. O número de linhas não é, sozinho, um defeito.

## Pontos menores e falsos positivos descartados

- **`pending` versus `UNVERIFIED`:** a ponte
  [autonomous-verification-engineering.md](../../../sdd/chain/autonomous-verification-engineering.md):23
  pede “Separate states: pending, approved, rejected, inconclusive, justified not
  applicable”. A skill usa unverified e evidence.md define os cinco tokens exatos.
  Como a frase está na contribuição Plan/ADR de um motor de aceitação, pode ser
  vocabulário do domínio, não uma ordem de escrever `pending` no JSON SDD. Falta
  mapeamento explícito. O checker não aceita `pending`; nenhum envelope atual
  contendo esse token foi encontrado. Classificação: ambiguidade, não falha atual.
- **Detalhe versus concisão:** não há obrigação geral simultânea de escrever tudo
  e resumir tudo. Prompt escolhe extensão pelas decisões necessárias; software-testing
  resume a verificação mas pede lacunas materiais; relatórios técnicos pedem
  evidência proporcional. Essas instruções são compatíveis.
- **Rust e unsafe:** a skill genérica não impõe uma proibição universal; POL-01
  proíbe unsafe próprio no Ox e separa dependências/FFI. A autoridade e o escopo
  resolvem a diferença. Não remover o método genérico nem enfraquecer POL-01.
- **Três threads versus quatro nós:** a configuração documenta três subagentes
  além da raiz. Não é um conflito numérico. Reciclagem de vagas e modelo efetivo
  de todas as invocações não foram demonstrados por esta auditoria.
- **Skills opcionais não instaladas:** referências a postgresql/kotlin/gleam e
  aos estudos de origem são condicionais/históricas, sem instalação automática.
  Não são, por si, dependências quebradas.
- **Logs de duas datas versus evidência histórica:** a política local explicita
  retenção finita de logs operacionais; registros versionados têm outro ciclo.
  Não foi demonstrado nesta análise que um artefato necessário foi apagado por
  rotação. Não confundir retenção finita com autorização geral de apagar evidências.
- **Modelos configurados e disponíveis:** os TOMLs são coerentes com a matriz
  declarada. A instalação já distingue parsing/configuração de ensaio da equipe.
  Não há base nesta auditoria para chamar um modelo de depreciado ou afirmar
  desempenho superior; isso exigiria observação própria e fontes atuais.

## Verificações observadas

Todas ocorreram a partir da raiz do checkout em 14/11/2026:

| Método | Resultado | Limite |
|---|---|---|
| `PYTHONDONTWRITEBYTECODE=1 python3 sdd/tools/validate.py --root . --structure-only` | exit 0 | Não verifica aceitação nem uso de templates no destino |
| `PYTHONDONTWRITEBYTECODE=1 python3 sdd/tools/validate.py --root .` | exit 0 | Aceita pendências; não reconcilia texto livre de converge |
| `PYTHONDONTWRITEBYTECODE=1 python3 tools/governance/scripts/check-ox.py` | exit 0 | Governança/links/archives; não prova comportamento de agentes/produto |
| Parsing por `tomllib` e confronto dos conjuntos de nomes | 13 perfis + config válidos; 31 skills = perfil = 31 pontes | Configuração, não execução dos modelos |
| `bash scripts/automate.sh --scope full --plan` | exit 0; 16 checks | Plano legado, não execução |
| `bash scripts/automate.sh plan --scope complete` | exit 0; 26 checks | Plano atual, não execução |
| Resolução de links dos templates no destino | Três links inválidos confirmados | Nenhuma feature real criada |
| Fixture temporária de autoridade fora de sdd | Link existente dentro do projeto recusado | Teste direto de `markdown_errors`, não suíte completa |
| Chamada de `feature_errors` com uma feature como diretório e aprovação/freshness requeridas | `No feature directories found` | Contrato atual já documentado |
| Inventário de estados e busca converge/JSON | Divergências em formas explícitas de aprovação identificadas; exemplos A01 revisados | Busca textual não interpreta toda cronologia automaticamente |

Os dois planos usaram `TOOLBOX_BIN=/home/rodrigo/Projetos/dev_audit/shared-toolbox/bin/toolbox`,
`TOOLBOX_SELINUX_LABEL=shared` e `CARGO_HOME=$PWD/.cache/ox/cargo-home`. Não houve
Cargo, scanners, chamadas a modelos, downloads ou alterações externas. As fixtures
ficaram em `TemporaryDirectory` sob `/tmp`, removido ao encerrar o teste. Os checks
acima antecedem a criação deste relatório; não são apresentados como validação
do próprio relatório.

## Prioridade de correção e fechamento documental

Ordem sugerida: A01 e A02; depois templates/portabilidade/seleção (A03–A06);
então escopo de papéis e estado atual (A07, A08, A10); por último redundância
editorial e mapeamento de vocabulário. A08 exige uma escolha de processo; as
demais correções podem preservar o contrato central de evidência e autorização.

Superfícies revisadas: AGENTS, perfis/config dos agentes, guias de agentes e
integração, catálogo/perfil/metadados/entradas de skills, workflow/evidence/project,
templates/pontes/checker, registros de convergência citados, constituição,
arquitetura e receitas de scripts/commit. Disposição: diagnóstico documentado
aqui; nenhuma dessas fontes foi alterada porque o pedido foi de análise. Não foi
criada uma nova feature nem reescrito o histórico de aceitação para concluir a
auditoria. Os achados permanecem abertos até correção autorizada e verificada.

## Identidade dos inputs no encerramento

SHA-256 agregado por grupo, calculado sobre linhas ordenadas por caminho no
formato `caminho-relativo + NUL + SHA256(bytes) + LF`. Esses digests identificam
o corpus observado no encerramento; não representam reexecução de evidências
antigas nem garantem a completude semântica da auditoria.

| Grupo | Arquivos | SHA-256 agregado |
|---|---:|---|
| agents/config | 14 | `3f222d0940470ce942f5766d2ce3d72dd3ab124714df077da3230ca433cbda5a` |
| skills completas | 183 | `32dd468aa869540cee0e86fa846a123027489df243cc9247f8d761e5ad3bf26a` |
| pontes e índice | 32 | `678ad55618f352e5a8c06be6cde73b4cd84e54697ceca82290ea5132d3a12e8f` |
| templates | 6 | `5a2874224b4d5fd722a84d3ddb42a7741dc723417c993fcd6a077b09290c2362` |
| SDD raiz e checker | 7 | `847f2d3645c6f0620b788c2f30ebefa322ae24591d10d3ccd2055ad3e85f6bdd` |
| envelopes e convergências | 77 | `47ba9476dd3d2c4d81b270cb7405598bd63d89e683868b6f4a6b28d74d29da8e` |
| autoridades e consumidores dirigidos | 13 | `d7218ee8b9975f7430be3b02c218de035a47d67cc7412465792a45026a4891b1` |

Verificação própria do relatório: todos os links Markdown locais resolvidos
para arquivos existentes; revisão dos locadores dos achados, escopo e limites.
Não houve reexecução dos gates de produto ou correção dos problemas relatados.
