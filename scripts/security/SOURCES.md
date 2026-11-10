# Referências dos scanners do Ox

O [guia vigente](../README.md) concentra configuração do consumidor, comandos,
políticas e limites. Na instalação Shared Toolbox, consulte
`docs/consumer-integration.md`, `docs/application.md` e `tools/<ferramenta>/README.md`.
Versões/imagens são escolhidas centralmente; fontes por versão pertencem a
`docs/references.md` e `docs/references.json` da plataforma. Esses caminhos não
são dependências locais do pacote Ox nem comprovam execução do consumidor.

Para utilitários Cargo locais, permanecem as referências oficiais:

- [cargo-audit](https://github.com/RustSec/rustsec/tree/main/cargo-audit).
- [cargo-deny](https://embarkstudios.github.io/cargo-deny/).
- [cargo-machete](https://github.com/bnjbvr/cargo-machete).
- [cargo-llvm-cov](https://github.com/taiki-e/cargo-llvm-cov).
- [cargo-geiger](https://github.com/geiger-rs/cargo-geiger).

Regras e fixtures locais são descritas em [rules/README.md](rules/README.md).
Licenças e atribuições permanecem em LICENSE/NOTICE deste diretório.

A pesquisa anterior de interfaces/versões, preparo nativo de OSV/Trivy/Grype,
locks e estados de migração foi retirada da árvore operacional e preservada
integralmente na [preimagem histórica](../../docs/validation/scripts-document-cleanup-20261109/before/scripts/security/SOURCES.md.bin).
Esse registro conserva fontes consultadas e limites das observações antigas;
não é guia de preparo atual. A referência de aceitação a este arquivo continua
resolúvel, com acesso explícito às fontes históricas, sem renovar resultados.
