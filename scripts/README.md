# Verificações do Ox com execução nativa central

Bash 4.4+, jq 1.6+ e utilitários GNU executam a automação modular. A CLI
Shared Toolbox usa Python 3.11+ e Docker; o Ox não instala scanners durante gates.
As regras do guia canônico de integração são obrigatórias neste consumidor.

## Configurar o ambiente consumidor

A documentação da instalação fica em `shared-toolbox/README.md`, dentro do
workspace `dev_audit/`. O procedimento canônico é
`shared-toolbox/docs/consumer-integration.md`; operação e preparo pertencem a
`shared-toolbox/docs/application.md`. Os antigos guias temáticos encaminham para
esses dois documentos. Esta integração foi conferida contra seus bytes em
09/11/2026; o [registro da adaptação](../docs/validation/toolbox-consumer-rules-20261109/report.md)
separa inspeção de execução.

Configure no ambiente local ou no CI, substituindo o caminho da instalação:

```bash
export TOOLBOX_ROOT="/caminho/da/shared-toolbox"
export TOOLBOX_BIN="$TOOLBOX_ROOT/bin/toolbox"
# Alternativa: disponibilizar toolbox no PATH, sem definir TOOLBOX_BIN.
```

`TOOLBOX_ROOT` é apenas uma conveniência para montar o caminho acima; o wrapper
do Ox descobre exclusivamente `TOOLBOX_BIN` ou PATH. Nenhum caminho pessoal,
scanner de `tools/` ou volume é selecionado diretamente pelo consumidor.
`tools/<ferramenta>/` contém receitas/documentação e `volume/` operacional da
plataforma; a entrada pública é `bin/toolbox exec`. `TOOLBOX_STATE`/`--state`
mudam índices/locks gerais e não deslocam esses volumes nem criam uma instalação
isolada. Quando usado, `--state` precede o subcomando da CLI.

O operador fornece Linux/amd64 no mesmo host dos bind mounts, Python 3.11+,
Docker acessível e imagens/bases preparadas, qualificadas e ativas. Para inspecionar
essa instalação, quando a tarefa autorizar comandos operacionais:

```bash
bash scripts/toolbox.sh doctor
bash scripts/toolbox.sh central list
bash scripts/toolbox.sh central status --tool ruff
```

`doctor` consulta Docker; list/status não homologam scans, e status não inspeciona
o daemon. Versões centrais ativas podem mudar: não copie o inventário datado da
plataforma para um pin no Ox. Rust/Cargo, dependências e testes do produto continuam
no consumidor. Imagens e bases pertencem ao operador. A exceção operacional
prevista no guia é a renovação automática central de OSV descrita abaixo.

## Executar as operações escolhidas pelo Ox

A interface padrão é a mesma do Ec, a partir da raiz:

```bash
./scripts/automate.sh plan --scope complete
./scripts/automate.sh run --scope complete
```

`plan` produz JSON sem executar Cargo/scanners ou preparar recursos. `run` prepara
o ambiente temporário e executa a mesma seleção. Sem `--scope complete`, todas
as superfícies são incluídas, exceto Grype, Bandit, Syft e YARA-X. `complete`
inclui esses quatro e rejeita `--surface`/`--check`, como no Ec.

Superfícies: `docs`, `scripts`, `application` e `security`. `--surface` e `--check`
são repetíveis; governança (`docs`) permanece obrigatória. Sem superfície explícita,
o check determina sua superfície; `coverage` exige `--surface application`.
Aliases: `fmt`, `check`, `build`, `test`, `clippy`, `syntax`, `tests`, `secrets`,
`sast`, `dependencies`, `syft` e `yara-x`. Os nomes anteriores também são aceitos.
`secrets` seleciona arquivos atuais e histórico. A aceitação gráfica permanece
um protocolo separado.

O runner respeita `TOOLBOX_BIN`, depois `TOOLBOX_ROOT`, PATH e os caminhos relativos
locais declarados em `config/automation.json`, incluindo `../dev_audit/shared-toolbox`.
Override explícito inválido não recebe fallback. O runner usa o label SELinux
`shared` por padrão (altera os xattrs dos mounts) e reutiliza `.cache/ox/cargo-home`
quando disponível; overrides do operador prevalecem. Não instala ferramentas nem
baixa crates. `scripts/toolbox.sh` continua portátil: somente `TOOLBOX_BIN` ou PATH,
com label controlado pelo chamador. Geiger pode precisar de dependências de outras
plataformas já presentes no cache.

Plugins Cargo sem seleção explícita no catálogo seguem a descoberta do Ec: o `PATH` do chamador tem prioridade;
o runner acrescenta `OX_CARGO_BIN` ou `${CARGO_HOME:-$HOME/.cargo}/bin` ao final
da busca. `OX_CARGO_BIN` permite selecionar o diretório de plugins separadamente
do cache de dependências; um valor explicitamente vazio é rejeitado. Para usar
uma instalação específica mesmo quando há outro plugin no `PATH`, coloque seu
diretório no início do `PATH`. Os testes de adaptadores usam `CARGO_HOME` e
plugins descartáveis, sem depender dos scanners instalados no ambiente do mantenedor.

O check Geiger tem seleção explícita em `checks.geiger.executable` no catálogo:
usa `.cache/ox/cargo-home/bin/cargo-geiger` com o SHA-256 da versão local corrigida
`0.14.0+ox.1`. O adapter verifica o caminho relativo, recusa symlinks e exige arquivo
executável com hash idêntico antes de invocá-lo. Essa seleção precede o `PATH`
somente nos checks que declaram `executable`; os outros plugins mantêm a descoberta
acima. Ausência, permissões inválidas ou hash divergente bloqueiam o check, sem
fallback para outro Geiger. O planejamento mostra o caminho declarado sem executar
nem preparar a ferramenta. Não é necessário exportar um `PATH` especial para a
execução normal; outra instalação exige seleção e revisão explícita do caminho/hash.

Geiger e a descoberta de membros usam todas as features. O parâmetro
`runtime.geiger_stack_bytes=16777216`, como no Ec, define `RUST_MIN_STACK` somente
no processo do scanner. Os relatórios continuam em JSON, com validação estrita
de omissões e tentativa de todos os membros, preservando os códigos e logs nativos.

Neste checkout, a seleção explícita do mantenedor para verificações completas
continua sendo:

```bash
TOOLBOX_BIN=/home/rodrigo/Projetos/dev_audit/shared-toolbox/bin/toolbox \
TOOLBOX_SELINUX_LABEL=shared \
CARGO_HOME="$PWD/.cache/ox/cargo-home" \
  ./scripts/automate.sh run --scope complete
```

Compatibilidade: as chamadas antigas `--scope governance|rust|security|quality|full|complete`
e `--plan` continuam aceitas sem subcomando, com sua seleção e filtragem anteriores.
Elas não definem mais o padrão recomendado; `run --scope full` é inválido.

Somente `history` usa `scripts/config/native/gitleaks/gitleaks-history.ignore`: 1.606 fingerprints
históricos revisados, com commit, arquivo, regra e linha. O adapter verifica os
bytes desse conjunto antes de executar. São hashes de evidência, identificadores
SQLite, prosa e um teste sintético; nenhum diretório ou regra foi excluído.
Novos commits não herdam essas exceções; `gitleaks` sobre arquivos atuais não as
usa. A revisão está em `docs/validation/complete-repair-20261111/history-review.json`.
Trivy recebe o cache e o Checks Bundle da Toolbox; não redefine `--cache-dir`.
Geiger continua recusando relatórios com arquivos usados sem métricas, inclusive
Rust gerado: obter exit zero da ferramenta não basta para aprovar a medição.
Bandit usa `--quiet` para manter stdout como JSON, sem barra de progresso.
As ocorrências de subprocesso dos auxiliares nativos e testes de retenção também
estão vinculadas por hash à revisão estática; estilos e imports foram corrigidos
diretamente. O relatório acima registra os casos e os controles de detecção.

A política de licenças e as duas exceções temporárias de manutenção ficam em
[dependency-policy-20261109.md](../docs/licensing/dependency-policy-20261109.md).
Audit/OSV ignoram somente os dois IDs aprovados, mantendo os outros avisos ativos.

```bash
./scripts/automate.sh plan --surface security
./scripts/automate.sh run --surface security
./scripts/automate.sh run --surface scripts
./scripts/automate.sh run --surface scripts --check shellcheck
bash scripts/checks/run.sh --check history
bash scripts/toolbox.sh exec --tool ruff --project-root "$PWD" --timeout 120 -- check --config scripts/config/native/ruff/ruff.toml --no-fix --no-cache scripts/
python3 -m unittest discover -s scripts/tests -v
OX_REAL_SECURITY=1 python3 -m unittest discover -s scripts/tests -p test_real_security_backends.py -v
```

`TOOLBOX_BIN`, quando definido (inclusive vazio), precisa ser executável. Caso
ausente, o wrapper procura `toolbox` no PATH. Um override inválido falha sem
fallback. O wrapper deriva do template `templates/consumer/toolbox-native.sh`.
Mantém dois guards locais já existentes: Bash 4.4+ e recusa de override vazio.
O template aceita vazio como ausência; no Ox, remova a variável com
`unset TOOLBOX_BIN` para usar PATH. Não há fallback para um override inválido.
`OX_TOOLBOX_BIN` e `OX_SCANNER_BACKEND` foram removidos: os checks rejeitam essas
variáveis para evitar uma segunda autoridade. Remova-as dos ambientes anteriores.

| Check | Ferramenta / comando nativo | Papel |
| --- | --- | --- |
| gitleaks | gitleaks dir, redact=100, ignore-gitleaks-allow, exit-code 10 | obrigatório security |
| history | gitleaks git, log-opts=--all, mesma política | opcional; Git completo |
| osv | osv-scanner scan source --offline --all-packages --lockfile | obrigatório security |
| opengrep | opengrep scan, regras locais, strict, no-git-ignore, disable-nosem | obrigatório security |
| bandit | bandit, YAML + INI explícitos, ignore-nosec, arquivos explícitos | obrigatório security |
| ruff | ruff check --ignore-noqa --no-fix --no-cache | obrigatório quality |
| shellcheck | shellcheck --format=json, rcfile explícito | opcional |
| trivy | trivy fs --scanners vuln, offline, skip-db-update e skip-java-db-update | opcional |
| grype | grype dir:/project -o json | opcional |
| sbom | syft scan dir:/project -o syft-json | inventário sem aprovação |
| malware | yara-x (entrypoint yr), scan JSON recursive | indicadores locais; sem detecção universal |
| audit / deny / machete | cargo-audit / cargo-deny / cargo-machete locais | security / quality |
| coverage / geiger | cargo-llvm-cov / cargo-geiger locais | medições opcionais |

`config/automation.json` conserva escopos security/quality/full/complete/governance/rust, a lista
de opcionais e os parâmetros dos scanners. `lib/registry.sh` lê o catálogo e monta argv nativo por scanner central. Comandos
locais ficam restritos à governança e às ferramentas Cargo do consumidor. `automate.sh` seleciona checks; `checks/run.sh` prepara entradas e
assessment; `lib/backends.sh` apenas transporta argv via exec e avalia diagnóstico;
`lib/files.sh` conserva snapshots/manifests; `lib/reports.sh` valida relatórios.
ShellCheck seleciona todos os scripts .sh do manifesto efetivo, inclusive
security/prepare-datasets.sh e toolbox.sh, sem lista estática paralela.

A plataforma controla versões, imagens imutáveis, runtimes, instalação, bases e
cache. O Ox controla comandos, regras, configurações, fontes, dependências,
serviços e aprovação. Não há config/lock de consumidor no novo fluxo; os dois
arquivos obsoletos foram removidos de scripts/config. Evidências históricas
continuam intactas. Nenhum adapter ou import privado Python é necessário.

Snapshots privados incluem fontes selecionadas, configurações e regras. `.git`,
`.local`, target/dist, ambientes Python e docs/validation são excluídos da análise
de arquivos. Escopo: arquivos raiz reconhecidos e application/tools/scripts/sdd/
config/docs/.github/.codex; conteúdo fora dele não recebe certificação.
Links, especiais e ignores não revisados nas fontes selecionadas bloqueiam.
Os hashes e modos são conferidos antes/depois; cada execução tem pasta exclusiva.
History copia .git completo e verifica origem/destino; shallow, alternates,
commondir, links e worktrees externos bloqueiam. Não faz fetch.

Fontes ficam em /project:ro, resultados explicitamente em /out:rw; /db, /cache
e /data pertencem à plataforma. Não há project-write, rede, socket, devices ou
credenciais de host implícitos. Correção é operação separada e requer autorização
explícita de escrita restrita. Não há eval nem reescrita heurística de paths.

O diretório de `--project-root` é montado em `/project`; caminhos nativos relativos
partem dali, ou do `--workdir` explícito. Paths absolutos do host após `--` não são
convertidos. `--results` monta `/out`; `--stdout-file`/`--stderr-file` redirecionam
streams para arquivos novos no host, sem tee. Os gates Ox já capturam os streams
separados em diretórios exclusivos, portanto não precisam desses redirecionamentos.
O diagnóstico JSON permanece separado do relatório nativo. Rede default é none;
OSV recebe também --offline e os outros scanners conservam seus controles offline.

Antes de cada análise OSV por `exec`/`run`, o gerenciador central baixa e valida
a base se ela estiver ausente ou tiver aquisição de mais de 12 horas. Se a
aquisição necessária falhar, a análise não prossegue. Isso pode usar rede no
gerenciador, embora o scanner receba `--offline` e o container use rede `none`.
A idade de aquisição não substitui a data dos advisories nem o limite Ox de 24h.
Não há pin, bloqueio ou atualização local de OSV em scripts; os demais scanners
continuam com manutenção explícita. CI e operadores precisam prever esse efeito
antes de executar os gates que selecionam OSV.

stdout/stderr são bytes da ferramenta, preservados em tool/*.log. A saída não é
JSON da plataforma. backend_record.json separado valida outcome native, código
nativo, versão, imagem sha256 e cleanup removed. Timeout/cancelamento/infra ou
cleanup incompleto nunca aprovam; o supervisor encaminha sinal e espera o prazo
de limpeza do executor. Não existe timeout externo que mate prematuramente a CLI.
assessment.json mantém tool_exit_code separado de runner_exit_code e exit_code
(classificação Ox). Achados precisam concordar com exit; schemas incompletos,
inventário ausente ou fontes omitidas falham. SBOM permanece recorded, sem aceitar
produto; todos os assessments têm product_acceptance=false.

Não registramos argv em process.json/command.json/assessment.json: comandos podem
conter credenciais. O transporte não seleciona env do host para containers.
Credenciais futuras devem usar --env KEY ou arquivos explicitamente montados ro,
com revisão específica. Streams brutos podem conter segredos impressos pela
ferramenta; ficam sob umask 077, sem truncamento e sem exclusão automática. Acesso
e remoção/retencão exigem revisão do proprietário. Gitleaks recebe redação nativa;
teste real com segredo sintético ainda depende de imagens ativas.

OSV exige idade máxima 24h; Trivy e Grype, 120h. O diagnóstico público de
exec vincula database_metadata à identidade da base realmente montada. OSV usa
a criação da geração publicada no GCS, com origem, geração e SHA256; Trivy usa
UpdatedAt nativo de cada base, nunca DownloadedAt. O Ox verifica todos os timestamps
e a igualdade com o mais antigo. Metadados ausentes, inválidos, futuros,
inconsistentes ou vencidos bloqueiam. Grype mantém validate-age=true e
max-allowed-built-age=120h no YAML nativo. Nenhum consumidor fixa snapshots.

Rust 1.99.1, fmt/Clippy/build/test e dependências Cargo continuam responsabilidade
do produto, sempre locked/offline. cargo-audit, cargo-deny, cargo-machete,
cargo-geiger e cargo-llvm-cov estão fora do catálogo central inspecionado e usam
preparo local separado com proveniência. Não há suporte central simulado.
RustSec usa prepare-datasets.sh --review ... --import ... --only rustsec ou
--download somente com autorização específica. Os comandos Cargo locais não fazem download, fetch ou instalação em gates;
a renovação central de OSV segue a regra acima. Cache não comprova cobertura.

A disponibilidade e as versões centrais devem ser conferidas na instalação.
Testes simulados validam somente o contrato.
A qualificação do Ox ainda precisa demonstrar, nos inputs atuais,
operações reais limpas/com achados/config inválida, supressões, segredos sintéticos,
concorrência, cancelamento, bases vencidas e integridade por Docker.

Recuperação de código usa o histórico Git. Não criar backups locais de scripts.
Logs seguem a retenção de duas datas descrita abaixo. Bases de ferramentas são
inputs operacionais em `.cache/ox/`, não cópias de recuperação.

### SELinux em hosts enforcing

O wrapper do Ox não seleciona rótulo automaticamente. Ausente/vazia, a variável
`TOOLBOX_SELINUX_LABEL` deixa os mounts sem relabel; os contextos já precisam
permitir acesso. Após revisar os caminhos dedicados com o operador, selecione
explicitamente `export TOOLBOX_SELINUX_LABEL=shared` no ambiente que executará
os gates: fontes e bases ro,z; resultados/cache rw,z. A Toolbox precisa
suportar esse modo. Rótulos compartilhados permitem leitores concorrentes sem
relabel privado conflitante; permissões Unix e mounts somente leitura continuam
válidos. Definição explícita vazia preserva --mount sem relabel; private usa Z e
é adequado somente a diretórios exclusivos. Relabel altera xattrs dos caminhos
montados no host: use snapshots/resultados limitados e volumes da ferramenta,
nunca /home ou /usr inteiros. Nenhuma política SELinux global é desativada.
Se exec retornar Permission denied, examine modos Unix, travessia, contextos e
AVCs autorizados; errno 13 isolado não identifica a causa. Não renove bases nem
ative imagens para contornar uma falha de acesso.

### Revisão de falsos positivos — 09/11/2026

Fixtures deliberadamente inseguras de regras são dados .py.txt/.rs.txt em
scripts/tests/rules, não fontes executáveis. Para testar detecção, copie-as para
uma árvore descartável com extensões .py/.rs e execute as mesmas regras.
Bandit usa baseline de ocorrências revistas e Ruff ignora somente códigos em
paths exatos. scripts/config/automation.json (reviews.static) vincula fontes e políticas por
SHA-256: qualquer mudança exige nova revisão antes da análise; ausência da
revisão com baseline presente falha. Não há corte global de severidade, nosec/noqa
ou exclusão geral de testes. Motivos e limites estão em
docs/validation/ox-operational-repair-20261109/static-review.md.

### Cache Cargo local desta instalação

O gate local usa `CARGO_HOME="$PWD/.cache/ox/cargo-home"`, conforme AGENTS.md.
O preparo explícito, fora dos checks offline, é:

```bash
CARGO_HOME="$PWD/.cache/ox/cargo-home" cargo fetch --manifest-path application/Cargo.toml --locked
```

O preparo de 09/11 importou archives já revistos e adquiriu os itens ausentes pelo
Cargo com lockfile preservado. Os checks continuam `--locked --offline`; não
fazem instalação, atualização de versões ou download implícito de crates.

## Caminhos e retenção local

`lib/common.sh` resolve caminhos; `lib/logs.sh` publica somente diagnósticos em
`.local/logs/AAAA-MM-DD/`, com arquivos por execução/ferramenta e no máximo duas
datas. Antes de publicar uma terceira data, apaga a mais antiga. Snapshots e builds
dos scanners ficam em diretórios temporários descartados ao encerrar a execução.
Use `bash scripts/local.sh` para simular a rotação ou `--apply` para aplicá-la.
Não há requisito de cópia preservada. Detalhes e limites no
[guia canônico](../docs/development/local-artifacts.md).

## Configuração centralizada — 13/11/2026

`config/automation.json` é a autoridade para escopos, opcionais, ferramentas,
executores, políticas, timeout nativo, idade das bases, seleção de fontes, caminhos
locais e revisões de exceções. `config/native/<ferramenta>/` contém os formatos
nativos; `rules/opengrep/` e `rules/yara-x/` contêm regras próprias. Não há cópias
ativas nos caminhos antigos. YAML/INI Bandit são complementares: o INI explícito
impede descoberta de configuração ambiente. O baseline permanece vinculado à revisão.

A organização segue Ec; suas credenciais, serviços web/PostgreSQL, suítes de
browser e exceções específicas não se aplicam ao desktop Rust/Iced. A interface padrão segue `plan|run`, com a sintaxe antiga preservada para compatibilidade. Mudanças no catálogo são dados, nunca código avaliado pelo shell.
Inventário, disposição de migração e verificação:
[relatório](../docs/validation/scripts-centralization-20261113/report.md).

As evidências atuais dessa feature usam entradas presentes na distribuição de
governança. Observações anteriores que também dependem de `application/`, bases
locais ou bytecode ficam preservadas como histórico, sem serem reusadas para
aprovar novos bytes. A feature continua incluída e verificada nas cópias
independentes. Detalhes e verificações da sucessão:
[paridade Cargo e evidências portáveis](../docs/validation/ec-cargo-parity-20261113/report.md).


## Padrões dos analisadores — sucessão de 13/11/2026

Ruff adota os grupos do Ec (segurança Python permanece no Bandit integral);
ShellCheck habilita todas as verificações opcionais; Clippy usa all/pedantic/nursery/cargo,
todas as features e keep-going. Bandit verifica também exceções tipadas vazias.
Syft amplia o inventário de arquivos/archives e Grype mantém achados não corrigidos.
Trivy habilita vuln/misconfig/secret, inclui dependências de desenvolvimento e
conta os três tipos de achado. Seu relatório persistido remove valores/trechos de
segredos, conservando hash/tamanho do bruto e indicação da perda. Relatório inválido
falha sem publicar seu conteúdo. Opengrep incorpora os indicadores Rust do Ec e
YARA-X inclui a assinatura de teste EICAR, além das regras existentes do Ox.

As políticas próprias de licenças, exceções Audit/OSV, fingerprints históricos e
baseline Bandit continuam específicas do Ox. Os catálogos externos adicionais e
o executor CodeQL do Ec são capacidades distintas e não estão implementados neste
runner. Não há alegação de equivalência da cobertura inteira dos dois produtos.
Padrões mais amplos podem revelar achados no código existente; a migração de
configuração não declara a suíte completa aprovada. Evidências e comparação:
[alinhamento dos padrões](../docs/validation/scripts-defaults-20261113/report.md).

## Correções da execução de 13/11

O planejamento legado também dispensa Rust/Cargo instalados. A sucessão de
paridade com Ec substitui a antiga prioridade do cache pela busca PATH primeiro,
descrita acima. Nenhum gate compila ou instala ferramentas. A correção de 15/11
declara o Geiger corrigido localmente por caminho/hash no catálogo, como descrito
acima; a antiga seleção manual por `PATH` fica substituída para esse check.
Fonte, patch, regressões e identidade estão no
[relatório de reparo](../docs/validation/complete-repair-20261113/report.md).
SC2310 foi revisto por chamada: predicados propagam falhas explicitamente; os
produtores de inventário têm seus códigos conferidos antes de carregar arrays.
As regras dos linters continuam ativas. As disposições de duplicidade/licença
estão na [política de dependências](../docs/licensing/dependency-policy-20261109.md).
