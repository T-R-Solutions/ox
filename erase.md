# Preparação temporária — apagar após preparar o ambiente

Este documento foi solicitado para as soluções externas necessárias aos checks
reintegrados. Nenhuma instalação, aquisição de base ou pull foi executado. Não é
configuração nem guia permanente; o contrato duradouro está em scripts/README.md.
Não entra na allowlist da distribuição. Fontes oficiais consultadas nesta correção.
Versões abaixo são candidatas verificadas no upstream, não ferramentas executadas
localmente nem novos pins do produto. A compatibilidade operacional local permanece
UNVERIFIED até executar cada ferramenta sobre o workspace real.

Todas as instalações abaixo são ações separadas. Downloads/releases, crates.io,
PyPI e aquisição de bases exigem rede autorizada. Verifique origem, assinaturas e
checksums publicados; nenhum hash/digest foi inventado. Copiar binários para um
PATH do usuário ou instalar em ambiente virtual/CARGO_HOME do usuário não precisa
de root; instalar em /usr/local/bin pode exigir privilégios administrativos.
Não execute os exemplos durante checks. Não é necessário instalar tudo globalmente.

As ferramentas baseline são obrigatórias quando security/quality/full ou o check
correspondente for selecionado. Complementares são opcionais por método; uma vez
selecionadas, a ausência bloqueia o check. Docker não é imposto nem usado por estes
adapters; executá-los em container exigiria mapear sources/cache/logs, preservar
UID/permissões e impedir acesso de rede. Sem esse método validado, prefira binários
locais. Cobertura/testes em container não provam aceitação gráfica X11/Wayland.

## Gitleaks

- Consumidor/finalidade: `gitleaks / history` via scripts/checks/run.sh e scripts/automate.sh; versão candidata **8.30.1**, [origem oficial](https://github.com/gitleaks/gitleaks/releases/tag/v8.30.1).
- Preparação: `binário Linux x86_64 da release oficial; colocar em diretório do PATH revisado`.
- Verificação: `gitleaks version`.
- Bases e limites: não usa base remota; regras built-in e configuração local.
- Licenciamento: MIT; revisar também termos das bases e componentes distribuídos. Rede/privilégios e limites de container: conforme as condições comuns acima.

## OSV Scanner

- Consumidor/finalidade: `osv` via scripts/checks/run.sh e scripts/automate.sh; versão candidata **2.7.0**, [origem oficial](https://github.com/google/osv-scanner/releases/tag/v2.7.0).
- Preparação: `binário Linux da release; alternativa upstream Go: go install github.com/google/osv-scanner/v2/cmd/osv-scanner@v2.7.0`.
- Verificação: `osv-scanner --version`.
- Bases e limites: base crates.io offline em osv-scanner/crates.io/all.zip; --offline não faz download.
- Licenciamento: Apache-2.0; revisar também termos das bases e componentes distribuídos. Rede/privilégios e limites de container: conforme as condições comuns acima.

## Opengrep

- Consumidor/finalidade: `opengrep` via scripts/checks/run.sh e scripts/automate.sh; versão candidata **1.33.1**, [origem oficial](https://github.com/opengrep/opengrep/releases/tag/v1.33.1).
- Preparação: `binário autocontido Linux da release, sem executar instalador remoto durante checks`.
- Verificação: `opengrep --version`.
- Bases e limites: regras locais Rust/Python; nenhuma regra de registry remoto.
- Licenciamento: LGPL-2.1; revisar também termos das bases e componentes distribuídos. Rede/privilégios e limites de container: conforme as condições comuns acima.

## cargo-audit

- Consumidor/finalidade: `audit` via scripts/checks/run.sh e scripts/automate.sh; versão candidata **0.22.2**, [origem oficial](https://github.com/RustSec/rustsec/releases/tag/cargo-audit/v0.22.2).
- Preparação: `cargo install --locked --version 0.22.2 cargo-audit`.
- Verificação: `cargo audit --version`.
- Bases e limites: clone local revisado de https://github.com/RustSec/advisory-db; scanner usa --no-fetch --no-yanked.
- Licenciamento: MIT OR Apache-2.0; revisar também termos das bases e componentes distribuídos. Rede/privilégios e limites de container: conforme as condições comuns acima.

## cargo-deny

- Consumidor/finalidade: `deny` via scripts/checks/run.sh e scripts/automate.sh; versão candidata **0.20.2**, [origem oficial](https://github.com/EmbarkStudios/cargo-deny/releases/tag/0.20.2).
- Preparação: `cargo install --locked --version 0.20.2 cargo-deny`.
- Verificação: `cargo deny --version`.
- Bases e limites: cache Cargo e política .local/security/deny.toml revisada para licenças/bans/fontes; não inferir compatibilidade jurídica.
- Licenciamento: MIT OR Apache-2.0; revisar também termos das bases e componentes distribuídos. Rede/privilégios e limites de container: conforme as condições comuns acima.

## cargo-machete

- Consumidor/finalidade: `machete` via scripts/checks/run.sh e scripts/automate.sh; versão candidata **0.9.2**, [origem oficial](https://github.com/bnjbvr/cargo-machete/releases/tag/v0.9.2).
- Preparação: `cargo install --locked --version 0.9.2 cargo-machete`.
- Verificação: `cargo machete --version`.
- Bases e limites: não usar --with-metadata/--fix; falsos positivos exigem revisão de uso indireto.
- Licenciamento: MIT OR Apache-2.0; revisar também termos das bases e componentes distribuídos. Rede/privilégios e limites de container: conforme as condições comuns acima.

## Ruff

- Consumidor/finalidade: `ruff` via scripts/checks/run.sh e scripts/automate.sh; versão candidata **0.17.4**, [origem oficial](https://github.com/astral-sh/ruff/releases/tag/0.17.4).
- Preparação: `binário Linux da release ou ambiente virtual: python3 -m pip install ruff==0.17.4`.
- Verificação: `ruff --version`.
- Bases e limites: sem base externa; --isolated evita regras herdadas, não usa --fix.
- Licenciamento: MIT e avisos de terceiros no upstream; revisar também termos das bases e componentes distribuídos. Rede/privilégios e limites de container: conforme as condições comuns acima.

## Bandit

- Consumidor/finalidade: `bandit` via scripts/checks/run.sh e scripts/automate.sh; versão candidata **1.9.4**, [origem oficial](https://github.com/PyCQA/bandit/releases/tag/1.9.4).
- Preparação: `ambiente virtual: python3 -m pip install bandit==1.9.4`.
- Verificação: `bandit --version`.
- Bases e limites: sem base externa; --ignore-nosec impede supressão silenciosa por comentários.
- Licenciamento: Apache-2.0; revisar também termos das bases e componentes distribuídos. Rede/privilégios e limites de container: conforme as condições comuns acima.

## cargo-llvm-cov

- Consumidor/finalidade: `coverage (complementar)` via scripts/checks/run.sh e scripts/automate.sh; versão candidata **0.9.1**, [origem oficial](https://github.com/taiki-e/cargo-llvm-cov/releases/tag/v0.9.1).
- Preparação: `cargo install --locked --version 0.9.1 cargo-llvm-cov; separadamente: rustup component add llvm-tools-preview --toolchain 1.99.1`.
- Verificação: `cargo llvm-cov --version`.
- Bases e limites: exige componente LLVM da toolchain atual e cache Cargo; gera target/LCOV novos, sem limiar adotado.
- Licenciamento: MIT OR Apache-2.0; revisar também termos das bases e componentes distribuídos. Rede/privilégios e limites de container: conforme as condições comuns acima.

## cargo-geiger

- Consumidor/finalidade: `geiger (complementar)` via scripts/checks/run.sh e scripts/automate.sh; versão candidata **0.13.0**, [origem oficial](https://github.com/geiger-rs/cargo-geiger/releases/tag/cargo-geiger-0.13.0).
- Preparação: `cargo install --locked --version 0.13.0 cargo-geiger`.
- Verificação: `cargo geiger --version`.
- Bases e limites: upstream experimental, MSRV 1.85/Cargo interno 0.86; integração exata com Ox 1.99.1 continua pendente de execução.
- Licenciamento: MIT OR Apache-2.0; revisar também termos das bases e componentes distribuídos. Rede/privilégios e limites de container: conforme as condições comuns acima.

## Trivy

- Consumidor/finalidade: `trivy (complementar)` via scripts/checks/run.sh e scripts/automate.sh; versão candidata **0.76.2**, [origem oficial](https://github.com/aquasecurity/trivy/releases/tag/v0.76.2).
- Preparação: `binário Linux da release oficial`.
- Verificação: `trivy --version`.
- Bases e limites: cache DB adquirido separadamente; scanner filesystem offline, não usa Docker nem Java DB.
- Licenciamento: Apache-2.0; revisar também termos das bases e componentes distribuídos. Rede/privilégios e limites de container: conforme as condições comuns acima.

## Syft

- Consumidor/finalidade: `sbom (complementar)` via scripts/checks/run.sh e scripts/automate.sh; versão candidata **1.57.0**, [origem oficial](https://github.com/anchore/syft/releases/tag/v1.57.0).
- Preparação: `binário Linux da release oficial`.
- Verificação: `syft version`.
- Bases e limites: sem DB de vulnerabilidades; usar filesystem dir:, sem imagem/container.
- Licenciamento: Apache-2.0; revisar também termos das bases e componentes distribuídos. Rede/privilégios e limites de container: conforme as condições comuns acima.

## Grype

- Consumidor/finalidade: `grype (complementar)` via scripts/checks/run.sh e scripts/automate.sh; versão candidata **0.121.2**, [origem oficial](https://github.com/anchore/grype/releases/tag/v0.121.2).
- Preparação: `binário Linux da release oficial`.
- Verificação: `grype version`.
- Bases e limites: base Grype adquirida/importada e revisada separadamente; auto-update e update-check desabilitados.
- Licenciamento: Apache-2.0; revisar também termos das bases e componentes distribuídos. Rede/privilégios e limites de container: conforme as condições comuns acima.

## YARA-X

- Consumidor/finalidade: `malware (complementar)` via scripts/checks/run.sh e scripts/automate.sh; versão candidata **1.23.0**, [origem oficial](https://github.com/VirusTotal/yara-x/releases/tag/v1.23.0).
- Preparação: `binário yr Linux da release oficial`.
- Verificação: `yr --version`.
- Bases e limites: somente indicadores locais; achado exige investigação, não executar amostras.
- Licenciamento: BSD-3-Clause; reconfirmar texto do LICENSE antes de redistribuir (consulta do arquivo indisponível); revisar também termos das bases e componentes distribuídos. Rede/privilégios e limites de container: conforme as condições comuns acima.

## ShellCheck

- Consumidor/finalidade: `shellcheck (complementar)` via scripts/checks/run.sh e scripts/automate.sh; versão candidata **0.11.0**, [origem oficial](https://github.com/koalaman/shellcheck/releases/tag/v0.11.0).
- Preparação: `binário Linux x86_64 da release oficial`.
- Verificação: `shellcheck --version`.
- Bases e limites: não exige DB; lê scripts Bash, não os executa.
- Licenciamento: GPL-3.0; revisar também termos das bases e componentes distribuídos. Rede/privilégios e limites de container: conforme as condições comuns acima.

## Bases e revisão local

OSV: [modo offline oficial](https://google.github.io/osv-scanner/offline-mode.html)
e [implementação/documentação](https://github.com/google/osv-scanner/blob/main/docs/offline-mode.md).
A base crates.io pode ser adquirida separadamente da origem
`https://osv-vulnerabilities.storage.googleapis.com/crates.io/all.zip` e colocada
na estrutura esperada. Isso não é feito pelo check. A licença da ferramenta não
relicencia todos os registros da base; revisar os termos/proveniência OSV.

RustSec: [advisories](https://github.com/RustSec/advisory-db), clone local e data
revisados antes de registrar validade/digest. Sem --stale e sem exceções herdadas.
Yanked crates não são consultados: --no-yanked impede atualização do registry.

Trivy: [air-gap](https://trivy.dev/latest/docs/advanced/air-gap/). Preparar cache DB
fora dos checks, preservando termos dos fornecedores de advisories. Grype:
[configuração offline](https://github.com/anchore/grype), base e validade revisadas;
nenhuma importação/download durante o check. Cada adapter usa cópia local dos dados
para separar caches de execução da base revisada.

Registrar SHA256 observado, origem, termos e valid_until adotado em
`.local/security/datasets.json`; o comando --inspect-data apenas mede bytes,
não aprova origem ou atualidade. Não aplicar prazos arbitrários de outro projeto.
A configuração cargo-deny também depende da revisão de licenças/fontes do Ox;
OPEN-07 permanece sem parecer jurídico geral. Não gerar uma allowlist permissiva
apenas para obter resultado verde.

## Interfaces e exclusões verificadas

[Flags offline cargo-deny](https://embarkstudios.github.io/cargo-deny/cli/common.html),
[comandos cargo-audit](https://github.com/RustSec/rustsec/blob/main/cargo-audit/src/commands/audit.rs),
[CLI Opengrep](https://github.com/opengrep/opengrep),
[cobertura](https://github.com/taiki-e/cargo-llvm-cov),
[Bandit](https://bandit.readthedocs.io/en/latest/man/bandit.html),
[YARA-X JSON](https://virustotal.github.io/yara-x/docs/cli/commands/).
A listagem Qodana [oficial](https://www.jetbrains.com/help/qodana/linters.html) não
oferece linter Rust. A imagem RustRover/Qodana customizada do projeto de origem,
seus tokens e docker build --pull não serão reativados. Qodana Python é alternativa
possível; não é pré-requisito desta entrega, coberta por Ruff/Bandit/Opengrep.
Graphify, JVM, frontend web e Tauri continuam fora da stack adotada.
