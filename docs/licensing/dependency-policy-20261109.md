# Política revista de dependências — 09/11/2026

O mantenedor autorizou a revisão/correção de licenças, a redução de versões
duplicadas e a aceitação temporária dos dois avisos de manutenção identificados.
A licença própria continua GPL-3.0-only; nenhuma dependência foi relicenciada.

## Licenças

A allowlist de scripts/config/native/cargo-deny/deny.toml admite GPL-3.0-only para os crates próprios
e MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC, Unicode-3.0 e Zlib nas
dependências revistas. Os demais identificadores continuam recusados por padrão.
Não foi adotada permissão automática por categoria OSI/FSF nem exclusão de crates
privados. A confiança de identificação permanece 0,95.

A revisão comparou 264 pacotes do lockfile candidato aos manifests e avisos da
revisão anterior autenticada por archives/checksums. Nenhuma divergência foi
encontrada. O inventário por pacote e arquivo está em
[license-review.json](../validation/dependency-hygiene-20261109/license-review.json).
Expressões OR permitem a escolha documentada; expressões AND mantêm ambas as
obrigações. Não foi escolhida GPL-2.0-only quando Apache-2.0 era alternativa.

Preservar textos de licença/copyright, avisos de terceiros e eventuais NOTICE
Apache na composição distribuída. Dez subcrates Iced não possuem aviso standalone
localizado no pacote: essa lacuna, já registrada no inventário, exige fechamento
do acervo de avisos antes de distribuição pública. Aprovar uso pelo build não
aprova redistribuição nem resolve a situação de outros materiais copiados do Ox.

Referências consultadas: [configuração cargo-deny](https://embarkstudios.github.io/cargo-deny/checks/licenses/cfg.html),
[compatibilidade Apache/GPLv3](https://www.apache.org/licenses/GPL-compatibility.html)
e [lista GNU](https://www.gnu.org/licenses/license-list.html).

## Exceções temporárias de manutenção

Autorizadas em 09/11/2026, aguardando a retomada pelo mantenedor:

| ID | Pacote observado | Motivo e revisão |
| --- | --- | --- |
| RUSTSEC-2026-0441 | pin-utils 0.1.1 | Aviso unmaintained; dependência transitiva via wasmtimer/iced_futures para wasm32. Rever na próxima atualização ou retomada do mantenedor. |
| RUSTSEC-2026-0192 | ttf-parser 0.25.1 | Aviso unmaintained; cadeia de fontes/renderização. Mantenedor investigará substituição; rever na próxima atualização ou retomada. |

Audit e OSV recebem somente esses IDs, com motivos explícitos. Pacotes inteiros
não são ignorados, nem a categoria unmaintained é desabilitada. Novos avisos e
vulnerabilidades continuam sujeitos aos gates. A exceção não significa correção
das bibliotecas. Fontes: [RustSec pin-utils](https://rustsec.org/advisories/RUSTSEC-2026-0441.html),
[RustSec ttf-parser](https://rustsec.org/advisories/RUSTSEC-2026-0192.html),
[configuração OSV 2.7.0](https://github.com/google/osv-scanner/blob/v2.7.0/docs/configuration.md).

## Duplicidades

O lockfile foi resolvido primeiro em cópia isolada/offline. A resolução compatível
unificou skrifa em 0.37.0, já exigida por cosmic-text, dentro do intervalo aceito
por swash 0.2.10. Foram removidas skrifa 0.44.0, read-fonts 0.41.0 e font-types
0.12.7, sem adicionar pacotes ou mudar Iced/toolchain/features.

O mantenedor escolheu preservar Iced 0.14 e documentar as duplicidades da
seleção conservada. Não foram apagadas entradas necessárias do lockfile nem foi
alterado multiple-versions=deny. Foram adotados nove skips por versão exata:
calloop 0.13.0, calloop-wayland-source 0.3.0, smithay-client-toolkit 0.19.2,
rustix 0.38.44, linux-raw-sys 0.4.15, rustc-hash 1.1.0, syn 2.0.119,
thiserror 1.0.69 e thiserror-impl 1.0.69. Cada entrada registra seus consumidores.

Isso aceita as gerações incompatíveis do grafo mantido, sem alegar que os pacotes
foram removidos ou que nenhuma migração futura poderia unificá-los. Não foram
feitos downgrades amplos de bibliotecas para eliminar contagens: conservaram-se
as versões existentes dos consumidores. Revisar cada exceção na próxima alteração
da stack; versões/famílias novas continuam negadas. Não foi usado skip-tree.
O Deny final passou com as licenças revistas e essas disposições explícitas.

## Revisão sucessora — 13/11/2026

O mantenedor solicitou tratar todos os achados de cargo-deny. A revisão dos
manifests e arquivos de licença locais confirmou BSL-1.0 (Boost Software License)
em clipboard-win 5.4.3 e error-code 3.4.0. BSL-1.0 passa a ser permitida de forma
explícita; preservam-se textos/avisos aplicáveis na composição distribuída. A
[lista GNU](https://www.gnu.org/licenses/license-list.html#boost) classifica a
licença como permissiva e compatível com GPL; o
[texto oficial](https://github.com/boostorg/boost/blob/master/LICENSE_1_0.txt)
orienta a preservação de avisos. Isto não aprova a distribuição do produto.

A resolução isolada/offline eliminou windows-sys 0.59.0: rustix 0.38 aceita
0.52, já exigida por winit. Nenhuma dependência nova foi adquirida. As demais
faixas incompatíveis foram revistas por aresta em
[duplicate-review.json](../validation/complete-repair-20261113/duplicate-review.json).
A política mantém multiple-versions=deny e adiciona apenas versões exatas de
bitflags, getrandom, jni-sys, objc2, objc2-foundation, r-efi, redox_syscall e
windows-sys. Clippy também reconhece a família objc2-quartz-core, presente no seu
grafo ampliado e ausente do grafo observado pelo Deny. O gate Deny rejeita
novas versões/famílias; os nomes adicionais em Clippy não substituem esse gate.
Rever na próxima alteração da stack Iced/plataformas. Nenhuma versão incompatível
foi forçada. O inventário original preserva a observação anterior à unificação.
