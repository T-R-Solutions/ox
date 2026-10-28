# ADR — Bootstrap do produto

Adotada para a execução de iniciar-projeto-revisado.md v2.0. Linux x86_64 e
stable confirmados explicitamente pelo mantenedor em 28/10/2026.

Workspace virtual em application, 16 crates explícitos, edição 2024/resolver 3,
MSRV 1.99 como piso conservador desta entrega (não mínimo técnico demonstrado).
Toolchain stable móvel por preferência do mantenedor; registrar rustc/cargo reais
nas observações. Não instalar toolchain numerada. Iced =0.14.0, tiny-skia,
x11, wayland, fira-sans e thread-pool. Sem wgpu, Tokio, serde ou UUID próprios.
A primeira tentativa sem executor falhou: Iced exige thread-pool, tokio ou smol;
o executor padrão satisfaz a necessidade sem introduzir runtime adicional.

Fontes oficiais consultadas: https://docs.rs/iced/0.14.0/iced/,
https://docs.rs/crate/iced/0.14.0/features,
https://doc.rust-lang.org/cargo/reference/workspaces.html e
https://doc.rust-lang.org/edition-guide/rust-2024/index.html.

Alternativas: wgpu não necessário ao shell mínimo; versão antiga de Rust exigiria
uma matriz adicional. UUID v7 adiado porque não há entidades persistentes globais.
Path de workspace é identidade lexical absoluta, não prova de existência/confinamento.
PluginDescriptor/ProtocolVersion são contrato de compatibilidade em memória,
não wire format ou host executável. IPC, agentes, banco e sandbox permanecem pendentes.

A ADR de layout é sucedida apenas na localização do produto: application/ em vez
de src/. Scripts Python permanecem em tools/governance. O guard de fase aceita
bootstrap-implemented, sem confundir aceitação com implementação. A distribuição
continua exclusivamente de governança: exclui a feature product-bootstrap e seus
registros dependentes das fontes do produto. A feature permanece na raiz SDD e
é verificada integralmente na árvore de desenvolvimento; não é escondida dos checks.
Não publicar nem regenerar os archives históricos. Evidências históricas afetadas
são preservadas e invalidadas seletivamente; nenhuma aprovação antiga é transferida.

Revisar ao mudar toolchain mínima, renderer, plataforma, protocolo persistido ou
pipeline de distribuição. Não há promessa de ausência de unsafe transitivo.
