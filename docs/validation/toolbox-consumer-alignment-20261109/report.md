# Alinhamento do consumidor Ox com Shared Toolbox — 09/11/2026

## Fontes observadas e escopo

O caminho solicitado `/home/rodrigo/Projetos/dev_audit/README.md` não existe.
O README real é `/home/rodrigo/Projetos/dev_audit/shared-toolbox/README.md`.
Foram lidos esse README, docs/consumer-integration.md, docs/application.md,
docs/native-execution.md, templates/consumer/README.md, o template nativo e os
guias dos módulos Trivy/OSV. Seus hashes estão em
[external-inputs.json](external-inputs.json). O conteúdo externo foi somente lido.

O README central agora concentra navegação em dois guias: aplicação/operação e
integração de consumidores. native-execution.md tornou-se um encaminhamento.
tools/<ferramenta>/ contém módulos e armazenamento operacional; o consumidor
acessa a CLI pública bin/toolbox, não os executáveis/volumes por caminhos internos.
Versões ativas e homologação são estados distintos. O inventário das 12 ferramentas
publicado no README é uma observação datada da plataforma, não uma execução Ox.

O pedido autoriza adaptação somente do Ox, estendendo a feature existente
scripts-toolbox-native (REQ-01/02, D-25/R-25, T025). Rota completa proporcional
à mudança do contrato de ambiente SELinux. A skill software-evolution e a
referência transition-decisions foram consultadas/aplicadas, conforme identidade
e contribuição registradas em plan.md. Nenhuma delegação foi realizada.

## Comparação e mudança implementada

| Tema | Estado anterior / decisão |
| --- | --- |
| Interface | Ox já usa exec, argv nativo, diagnóstico separado e ausência de fallback. Preservados; não foram copiados JSON/locks/STIC legados. |
| Descoberta | TOOLBOX_BIN ou PATH já são usados. Exemplo com caminho pessoal substituído por TOOLBOX_ROOT configurável no ambiente e TOOLBOX_BIN derivado. TOOLBOX_ROOT não cria um novo mecanismo de descoberta. |
| Guards | Bash 4.4+ e override vazio recusado continuam como contratos locais documentados; o template central admite vazio como ausência. No Ox, usar unset TOOLBOX_BIN para selecionar PATH. |
| SELinux | O wrapper atribuía shared quando ausente. Removida essa atribuição: ausente/vazio permanece sem relabel automático, como recomenda a seleção explícita do guia. Teste de contrato adaptado para esperar unset; overrides e encaminhamento de falha permanecem. |
| Paths/resultados | Guia explica /project ro, /out rw quando --results é escolhido, ausência de conversão de paths host, workdir, streams novos no host e diagnóstico separado. Os gates já preservam seus próprios streams. |
| Estado/volumes | Esclarecido que TOOLBOX_STATE/--state altera índices/locks e não move tools/*/volume nem isola instalação. Sem escrita direta nesses recursos. |
| Ferramentas/preparo | Imagens/bases/ativação são do operador; configs, regras, política e dependências Rust permanecem no Ox. OSV offline e limites de idade existentes permanecem. Trivy mantém o escopo vuln escolhido no registro; não foi ampliado para novas categorias nem adicionado scanner pela disponibilidade no catálogo. |

A mudança de SELinux exige ação nos ambientes que dependiam do padrão anterior:
após revisar snapshots e volumes dedicados com o operador, configurar
`export TOOLBOX_SELINUX_LABEL=shared` no ambiente local/CI. Contextos já adequados
podem permitir execução sem essa seleção. shared/private afetam xattrs no host
mesmo com mounts ro; esta tarefa não executou relabel ou modificou permissões.

scripts/README.md contém os comandos de configuração e consulta. A introdução de
scripts/security/SOURCES.md aponta aos guias consolidados, preservando as seções
históricas. ADR, spec, plan, tasks, traceability e converge receberam o sucessor
delimitado. O README principal já encaminha para scripts/README e permaneceu
idêntico à preimagem. Não foram alterados código Rust, dependências, regras de
scanner, bases, dados operacionais ou fontes da plataforma.

## Inspeção e limites

| Critério | Método/inputs e resultado | Estado delimitado |
| --- | --- | --- |
| Documentação de configuração corresponde ao guia | Leitura das oito fontes externas identificadas; confronto com wrapper, registro, backends, process e testes atuais; diff contra preimagens | APPROVED por inspeção documental; não comprova execução |
| Escolha SELinux explícita | Inspeção do wrapper sem export automático e teste fonte esperando unset; encaminhamento "$@"/exec preservado | Implementado; AC-01/02 INCONCLUSIVE sem execução de testes |
| Transporte/report/política operacional | Consumidores existentes inspecionados; nenhuma instalação ou novo scanner introduzido | AC-03 UNVERIFIED; requer qualificação real do Ox nos novos inputs |
| Recuperação e preservação | Preimagens conferidas por SHA-256; mudanças enumeradas em changes.json e changes.diff | APPROVED para existência/integridade das cópias; restauração não ensaiada |

Não foram executados scripts de verificação, testes automatizados, automate.sh,
doctor, central list/status, Docker, scanners, builds, downloads ou manutenção.
Foi mantida a restrição de execução anteriormente solicitada. A inspeção usou
leituras, buscas e comparação de bytes; não é resultado de teste automatizado.
Nenhum commit ou publicação foi feito. Logs/históricos anteriores não foram
reescritos e evidence.json não recebeu hashes renovados. A alteração de spec,
plan, tasks, traceability, wrapper e teste invalida a atualidade de observações
anteriores dependentes desses inputs; converge registra os estados não decididos.
O histórico original continua disponível, sem promoção de evidência da plataforma
para aceite do produto. Não há garantia sobre disponibilidade atual do daemon,
idade das bases, plataformas diferentes ou consumidores externos não observados.

## Artefatos e recuperação

- [before.json](before.json): inventário das preimagens, com hashes e caminhos .bin.
- [changes.json](changes.json): identidades antes/depois; inclui o README raiz observado e mantido.
- [changes.diff](changes.diff): somente diferenças desta adaptação, não diferenças para HEAD.
- [external-inputs.json](external-inputs.json): identidade das fontes externas consultadas.

Para reverter, preserve qualquer trabalho posterior e compare a versão atual ao
after_sha256 de changes.json. Se diferir, reintegre manualmente somente os trechos
desejados a partir de before/, sem substituir o arquivo inteiro. Para reversão
por contexto, da raiz Ox, use primeiro
`git apply --reverse --check docs/validation/toolbox-consumer-alignment-20261109/changes.diff`.
Somente se a aplicação integral for aceita, execute o mesmo comando sem --check.
Não force conflitos, não use reset/checkout ou --reject. As cópias .bin permitem
recuperação por comparação manual sem depender do histórico Git. Retornar ao
wrapper anterior também retorna ao relabel implícito: revise essa consequência
antes de restaurar. Nenhum comando de restauração foi executado nesta tarefa.
