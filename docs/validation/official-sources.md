# Fontes oficiais consultadas

Consulta web pelo agente executor em 2026-10-26. Não foram instaladas bibliotecas ou executados exemplos de produto. Conteúdo técnico das novas skills distingue fatos documentados e síntese de método; versões consultadas não são escolhas aprovadas para Ox. URLs externas são fontes de pesquisa, não dependências dos validadores locais.

| Competência | Fonte consultada | Observação aplicável e limite |
|---|---|---|
| Plugin protocol | [JSON-RPC 2.0](https://www.jsonrpc.org/specification) | Envelope e correlação; não define transporte, autorização ou isolamento |
| Agent runtime | [ACP initialization v1](https://agentclientprotocol.com/protocol/v1/initialization), [cancellation](https://agentclientprotocol.com/protocol/v1/cancellation) | Negociação/cancelamento; v2 draft separado; nenhum peer real testado |
| Agent runtime | [Rust Child](https://doc.rust-lang.org/std/process/struct.Child.html) | Drop não termina processo; não extrapolar para todo runtime |
| Autonomous verification | [SLSA provenance 1.2](https://slsa.dev/spec/v1.2/provenance) | Origem de artefatos não é aceitação funcional ou certificação SLSA |
| Workspace | [Git worktree](https://git-scm.com/docs/git-worktree), [Rust rename](https://doc.rust-lang.org/std/fs/fn.rename.html) | Estado compartilhado e semântica por plataforma; sem promessa de transação multiarquivo |
| Iced | [Guia 0.14.0](https://docs.rs/iced/0.14.0/iced/), [widget](https://docs.rs/iced/0.14.0/iced/widget/index.html), [advanced](https://docs.rs/iced/0.14.0/iced/advanced/index.html) | Message/update/view, Task/Subscription; confirmar API no consumidor |
| Context | [LSP 3.17](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/), [Tree-sitter incremental parsing](https://tree-sitter.github.io/tree-sitter/using-parsers/3-advanced-parsing.html) | Portal LSP acessível, extração detalhada do portal incompleta; ranges/capabilities exigem schema real; parsing não é resolução |
| Graph | [W3C PROV-DM](https://www.w3.org/TR/prov-dm/) | Vocabulário de proveniência; não requer RDF nem valida arestas inferidas |
| Output | [Cargo external tools](https://doc.rust-lang.org/cargo/reference/external-tools.html#json-messages) | JSON do build não cobre arbitrariamente subprocessos/testes |
| Usage | [OpenTelemetry GenAI attributes](https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai/), [repositório GenAI indicado pela fonte](https://github.com/open-telemetry/semantic-conventions-genai) | Página antiga sinaliza mudança/depreciação de localização; contrato de cada provedor ainda precisa ser observado; sem preços inventados |

## Lacunas e retomada

URLs diretas de pane_grid e advanced Widget para Iced 0.14.0 falharam nesta consulta. As páginas de módulos superiores responderam. A referência de layout não afirma assinaturas dessas APIs; confirmar documentação/source da versão escolhida antes de implementar widgets. O portal LSP retornou principalmente navegação; consultar schema da versão do servidor e testar Unicode antes de afirmar ranges corretos. OTel migrou as convenções GenAI para repositório próprio; fixar uma revisão ao implementar adaptadores. Nenhuma dessas lacunas impede os métodos reutilizáveis escritos, mas impede alegar compilação ou compatibilidade do consumidor.

Skill-creator foi lida integralmente no ambiente; cópia histórica em adoption-baseline. Seu quick_validate usa PyYAML, disponível aqui (6.0.3), mas o fluxo portátil obrigatório usa somente stdlib e o validador do SDD. Não há dependência operacional da skill-creator instalada fora deste projeto.
