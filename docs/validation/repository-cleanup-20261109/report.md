# Limpeza conservadora do Ox — 09/11/2026

Pedido adaptado expressamente pelo mantenedor: trabalhar somente no Ox. Ec foi
consultado inicialmente em leitura para esclarecer a divergência de contexto;
nenhum arquivo dele foi alterado. Não foram importadas suas regras, stack ou
política de commit. `docs/development/task-verification.md` não existe no Ox;
nesta tarefa prevaleceu a proibição expressa de testes, verificadores e
`automate.sh`. Não houve commit, publicação, download, execução de scanners,
build, acesso a serviços ou alteração de bancos, volumes e recursos externos.

## Escopo e método efetivamente observados

Foram lidos AGENTS, projeto, constituição, arquitetura, workflow, evidências e
catálogo. As decisões pertinentes incluem scripts-task-closure,
scripts-shell-refactor, scripts-security-quality, scripts-toolbox-native,
scanner-toolbox-ownership, governance-layout, maintenance-001 e open-questions.
O escopo vigente é desktop Rust/Iced com 16 crates; Server, Agent de CI e
frontend Vue são conceitos do pedido original Ec, não superfícies do Ox.

A coleta por `os.walk`, sem seguir links, inventariou **136.584 arquivos/entradas**
fora de `.git`, sem erros de leitura reportados. Foram identificados por SHA-256
**697 arquivos de fontes/contratos ativos**, incluindo 77 em application, 45 em
scripts, 55 em tools, 257 em sdd, 182 em .codex e 71 em docs fora dos históricos.
Esse inventário não significa leitura semântica integral de cada linha.

| Superfície | Inspeção e decisão |
| --- | --- |
| Aplicação | Manifesto virtual, 16 manifests, exports `mod`/`pub mod`, referências de binários e testes, contratos e fluxo desktop/Controller/Runtime/Engine. Manter módulos previstos: storage, contexto, grafo, output, observabilidade, SDD e skills não são código morto por ainda não integrarem a UI. |
| Dependências | Iced e referências locais seguem os manifests; x11rb atende testes desktop. Cargo.lock conserva o grafo transitivo. Nenhuma dependência foi removida por falta de chamada direta. Não foi executado cargo metadata/machete nem revisado semanticamente todo o código transitivo. |
| Testes | Descoberta Cargo de bins/tests e `CARGO_BIN_EXE_*`; unittest `test*.py`, imports de support, consumers Rust/Python, fixtures de regras e testes reais opt-in. Fontes e dados preservados; somente bytecode derivado foi excluído. |
| Scripts | Todos os 45 arquivos funcionais/documentais enumerados em [scripts-map.json](scripts-map.json); fluxo e consumidores detalhados abaixo. |
| Configuração e governança | Perfil, catálogo/ponte, allowlist do empacotador, transient, sucessores por conteúdo e preservação de preimagens examinados. Não alterar catálogo, hashes históricos, licenças ou regras para facilitar a limpeza. |
| Documentação | Guias vigentes, ADRs, features e índices distinguidos de resume.md, erase.md, propostas, imagens de referência e relatos datados. Corrigida orientação de runner antigo; relatos históricos mantidos. |
| Artefatos locais | Inventário de .local, checks, security, security-tools, build, dist e application/target. Diretórios volumosos contêm snapshots, dependências, candidatos e recuperação; tamanho e idade não justificam descarte. Bases e ferramentas não foram removidas. |

As buscas usaram `rg --files`, `rg -n` e leitura direta. A inspeção dos bytes usou
somente stdlib para inventário, hash, cópia, exclusão da lista fechada e comparação
com preimagens. Nenhum módulo do projeto foi importado para executar validadores,
testes ou comandos encontrados nos documentos. Git status/diff foram usados como
contexto; o diff revisado contra os bytes preexistentes está na recuperação local,
pois scripts/ já era untracked e a árvore continha muitas alterações anteriores.

Rota local após a análise: remoções delimitadas, sem mudança de contrato, política
ou comportamento esperado; recuperação definida antes da exclusão. Skill primária
selecionada, lida e aplicada: `.codex/skills/workspace-integrity-engineering/SKILL.md`,
SHA-256 `3156e92baceb75376182423952607da665ff2c8db0d8cdc4296b44431b5c915a`,
ponte `sdd/chain/workspace-integrity-engineering.md`, bridge_version 1. Contribuição:
limites de caminhos, preimagens não dependentes do Git, comparação da base observada,
journal e restauração sem overwrite. Casos executáveis da skill não foram rodados.

## Scripts: consumidores e resíduos de migração

`automate.sh` lê `common`, `process`, `registry` e `backends` por source; seleciona
escopos e checks pelo registro único. Delega scanners a `checks/run.sh`, que lê
também files/reports e chama o transporte Toolbox. Rust e governança continuam
com comandos próprios: Cargo e tools/governance/sdd. Não há runner Python ativo
em scripts. A referência remanescente em application/README foi corrigida.

`check_properties` seleciona TOOL, DATA, RULE, CONFIG e SNAPSHOT por nome;
`native_command` mantém os argv centrais. Configurações não precisam de uma
referência literal em cada caller: nomes vêm do registro. bandit.ini e o arquivo
trivyignore, inclusive vazio, possuem papéis explícitos e foram mantidos.

`files.sh` observa/copía fontes e modos por manifesto, recusa links e exclui
.local, target, dist, caches e docs/validation. ShellCheck descobre `.sh` pelo
manifesto efetivo; Ruff/Bandit recebem Python selecionado. `support.py` carrega
as bibliotecas por nomes de módulos e expõe comandos/parsers aos testes.
unittest descobre test*.py: retirar um cache não retira o teste correspondente.

`TOOLBOX_BIN` ou PATH selecionam a CLI pública; override inválido não permite
fallback. `OX_TOOLBOX_BIN` e `OX_SCANNER_BACKEND` continuam rejeitados.
`TOOLBOX_SELINUX_LABEL`, CARGO_HOME, a toolchain fixada e opções de root/output
continuam com os consumidores existentes. Não foram registrados valores privados
de ambiente. A disponibilidade atual de ferramentas centrais não foi consultada.

Preservados como interfaces próprias: security/analyzers/check-report.sh,
validate-exceptions.sh, reports/summarize.sh e security/prepare-datasets.sh.
O preparo é explícito e hoje aceita somente RustSec; os gates não o invocam.
Os parsers extras, regras YARA/Opengrep/Gitleaks e fixtures Rust/Python não foram
eliminados por não aparecerem no escopo padrão. check_command conserva as
definições consumidas por planos/testes; não foi confundido com runtime sem uso.

## Remoções executadas e fontes mantidas

O [inventário por caminho](inventory.json) foi escrito antes das remoções e contém
finalidade, razão, evidência, consequências, fonte mantida, SHA-256, modo, tamanho,
tempos/identidade observados e caminho da cópia recuperável. O
[journal incremental](operations.jsonl) registra intenção/ação/resultado com data.

| Grupo | Remoção e fundamento | Fonte canônica mantida / efeito |
| --- | --- | --- |
| 35 `.pyc`, 429.822 bytes | 11 em scripts/tests, 12 em tools/governance/tests, 11 em tools/governance/scripts e 1 em sdd/tools. Todos têm `.py` correspondente, cuja identidade foi registrada. source_snapshot e transient excluem __pycache__; ADR adoption distingue cache de fonte/contrato. Nenhum loader de bytecode avulso foi encontrado nas superfícies ativas pesquisadas. | Cada fonte correspondente consta no inventário, incluindo support e todos os test*.py. Imports podem regenerar cache. Diretórios foram mantidos; nenhum cache dentro de histórico/snapshot/.local foi removido. |
| Ramo local de scripts/checks/run.sh | Retiradas versão especial Syft/Grype, caches OSV/Grype, preflight Git de history, input adicional Bandit/Trivy e ignore Opengrep situados **depois** de o ramo Toolbox sair. select_backend só permite native para audit/deny/machete/coverage/geiger; nenhum desses nomes satisfaz as condições removidas. | native_command/run_toolbox preservam os mesmos scanners/configurações, incluindo validação Git mais forte para history e ignore Opengrep no snapshot central. CLI, argumentos públicos, tratamento de falhas, logs e cinco utilitários Cargo preservados. O substituto já existe no fluxo; sua eficácia real não foi reexecutada. |
| scripts/lib/reports.sh | Retirado o segundo `if name == coverage`, idêntico ao que envolve o bloco, sem alteração de name entre ambos. | Mesma validação de exit e fim de registro LCOV, STATE=recorded e return. Nenhuma expressão de validação foi retirada. |

Nenhum arquivo-fonte funcional completo foi removido. A limpeza não fabricou
desuso para ampliar o número de exclusões. As duas remoções de código são de
blocos comprovadamente redundantes/inalcançáveis, não uma refatoração de scanners.

## Preservados e dúvidas registradas

- A única duplicata exata entre os 697 inputs ativos é portable-sources.md em
  application-security e reliability-engineering. São recursos de dois pacotes
  autocontidos com perfil e consumidores próprios; ambos permanecem. Identidades
  em [duplicates.json](duplicates.json).
- Logs, falhas, auditorias, manifests e snapshots de runs em docs/validation,
  docs/structure, .local/checks e dist permanecem. Capturas duplicadas em
  docs/assets têm papel de publicação distinto da evidência original.
- Baselines de manutenção, preimagens das migrações, cópias de scripts e candidatos
  de Toolbox são recuperação/evidência; não foram apagados como duplicatas.
- Binários locais antigos de Opengrep/OSV não são fallback do fluxo atual, mas
  sua necessidade para reprodução histórica não foi descartada. Foram preservados,
  assim como RustSec, gerações e artefatos de preparo. Bancos não são alvo desta tarefa.
- resume.md, erase.md, propostas de persistência e marcos futuros foram mantidos.
  A existência de uma proposta não prova abandono. SOURCES deixou de orientar o
  uso operacional de erase.md, sem alterar o relato histórico em si.
- Consumers de governança e crates de fundação não foram retirados por aparente
  semelhança com a aplicação: validam métodos e contratos distintos.

## Documentação e aceitação afetadas

application/README aponta para Bash e distingue execução autorizada de simples
disponibilidade do comando. scripts/README liga este inventário. A introdução de
security/SOURCES classifica suas versões como histórico da pesquisa e encaminha
pré-requisitos atuais ao guia de scripts. Nenhuma seção histórica datada foi
reescrita para representar uma execução nova.

As convergências scripts-toolbox-native e scripts-toolchain-config recebem somente
um sucessor de inspeção. Os três vínculos de observações correntes diretamente
afetados estão em [affected-observations.json](affected-observations.json).
evidence.json e seus hashes originais não foram renovados. AC-01/02 da feature
nativa ficam INCONCLUSIVE nos novos inputs; AC-03 continua UNVERIFIED.
Toolchain conserva AC-01..04 INCONCLUSIVE e AC-05..07 UNVERIFIED do sucessor nativo.
Não há aprovação operacional nova por inspeção ou por ausência de testes.

## Evidências e limites da conclusão

| Critério | Método e inputs | Resultado / limite |
| --- | --- | --- |
| Toda exclusão tem justificativa e preimagem | inventory.json, recovery-manifest local, comparação de bytes, modos e fontes antes do unlink | Cópias feitas antes de remover; somente lista fechada de caches. Identidades finais em [inspection.json](inspection.json). |
| Remoções de código preservam os caminhos vigentes | Diff contra preimagens, leitura de select_backend, branch Toolbox/exit, native_command e bloco coverage | Argumento estático de fluxo/identidade de condição; não equivale a Bash syntax, testes ou scan real. |
| Alterações preexistentes preservadas | Comparação de metadados da árvore e hashes previamente coletados contra sete arquivos editados/35 exclusões autorizadas | Resultado em inspection.json; diff local usa base real, não HEAD. Sem isolamento de outros escritores; comparação detecta mudanças observadas, não prova ausência de corrida adversarial. |
| Logs e históricos existentes preservados | SHA-256 dos 40.230 inputs protegidos, incluindo 3.705 streams .log/.stdout/.stderr/.err; inventário antes/depois | Resultado em preservation.json. Abrange históricos fora de .git; arquivos grandes em .local/build têm somente metadados, exceto streams e históricos oficiais, que têm hash. |
| Guias e referências afetados ajustados | Leitura das sete edições e buscas do caminho antigo nas entradas vigentes | Referências restantes em ADR/inventários/convergências anteriores são históricas e permanecem; novo inventário distingue essas referências de instrução atual. |

A comparação final registrou exatamente 35 exclusões e sete edições, sem arquivo
preexistente inesperadamente ausente, sem alteração inesperada de metadados e sem
divergência dos hashes coletados. Os 40.230 arquivos protegidos, incluindo os
3.705 streams, permaneceram idênticos nos bytes e metadados comparados. As 42
preimagens conferiram em SHA-256, modo, mtime e proprietário/grupo. Estado da
preservação e recuperabilidade por cópia: APPROVED nesse método delimitado;
ensaio de restauração e validação funcional dos scripts: UNVERIFIED.

Não foram executados scripts de verificação, testes automatizados, automate.sh,
Cargo, scanners, ferramentas centrais, renderização ou aceitação gráfica. Não há
conclusão sobre vulnerabilidades, qualidade funcional, cobertura de testes, escala
ou funcionamento atual da Toolbox. A restauração fornecida foi inspecionada, não
ensaiada. Nenhuma lacuna de execução é tratada como aprovação.

A inspeção semântica foi dirigida a contratos, entradas, consumidores e candidatos;
não foi uma auditoria linha a linha de todo Rust/Python, conteúdo transitivo,
binários ou arquivos compactados. Archives foram preservados por hash, sem
extração recursiva. .git foi excluído da coleta e permaneceu sob permissão de
somente leitura; não há nova auditoria de seus objetos/reflogs. Recursos externos,
editor/IDE, scripts pessoais e acionamentos não presentes no repositório não
foram analisados. Nenhuma superfície local inacessível foi encontrada na coleta;
isso não certifica esses consumidores externos.

## Recuperação

Área excluída da limpeza e fora das superfícies funcionais:
`.local/recovery/repository-cleanup-20261109/`, protegida por diretório 0700 e já
excluída por `.gitignore`, snapshots e distribuição via a regra geral de .local.
Contém before/ com caminhos originais, recovery-manifest.json, baseline.jsonl,
active-before.jsonl, protected-before.jsonl, collection.json e reviewed-changes.diff.
Nenhum registro depende exclusivamente do Git. Consulte
[instruções de restauração sem sobrescrita](recovery.md).
