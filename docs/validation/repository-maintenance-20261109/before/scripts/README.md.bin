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

Neste checkout, toda execução **autorizada** da suíte completa segue a regra
local de AGENTS.md, com a instalação explicitamente selecionada:

```bash
TOOLBOX_BIN=/home/rodrigo/Projetos/dev_audit/shared-toolbox/bin/toolbox \
  bash scripts/automate.sh --scope full
```

A política de licenças e as duas exceções temporárias de manutenção ficam em
[dependency-policy-20261109.md](../docs/licensing/dependency-policy-20261109.md).
Audit/OSV ignoram somente os dois IDs aprovados, mantendo os outros avisos ativos.

```bash
bash scripts/automate.sh --scope security --plan
bash scripts/automate.sh --scope security
bash scripts/automate.sh --scope quality
bash scripts/automate.sh --scope quality --check shellcheck
bash scripts/checks/run.sh --check history
bash scripts/toolbox.sh exec --tool ruff --project-root "$PWD" --timeout 120 -- check --config scripts/config/ruff.toml --no-fix --no-cache scripts/
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

`lib/registry.sh` conserva escopos security/quality/full/governance/rust, a lista
de opcionais e uma única definição de argv nativo por scanner central. Comandos
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

Recuperação: preserve resultados e os diagnósticos UUID. Não remova imagens,
.local/security-tools, bases ou gerações por nome/idade. A cópia anterior de
scripts está em .local/build/toolbox-migration/before; restaure somente arquivos
afetados após conferir mudanças concorrentes. A Toolbox deve ser recuperada pelo
operador via revisão anterior, pela interface central, preservando preimagens e ponteiros por execução. Retornar
ao transporte legado exige revisão explícita; não é fallback de um gate.

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
paths exatos. scripts/config/static-review.json vincula fontes e políticas por
SHA-256: qualquer mudança exige nova revisão antes da análise; ausência da
revisão com baseline presente falha. Não há corte global de severidade, nosec/noqa
ou exclusão geral de testes. Motivos e limites estão em
docs/validation/ox-operational-repair-20261109/static-review.md.

### Cache Cargo local desta instalação

O gate local usa `CARGO_HOME="$PWD/.local/cargo-home"`, conforme AGENTS.md.
O preparo explícito, fora dos checks offline, é:

```bash
CARGO_HOME="$PWD/.local/cargo-home" cargo fetch --manifest-path application/Cargo.toml --locked
```

O preparo de 09/11 importou archives já revistos e adquiriu os itens ausentes pelo
Cargo com lockfile preservado. Os checks continuam `--locked --offline`; não
fazem instalação, atualização de versões ou download implícito de crates.
