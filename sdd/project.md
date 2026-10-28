# Contexto do projeto Ox

## Identidade e fase

Projeto: Ox — aplicação desktop agent-first, local-first e extensível.
Fase atual: `implementation-foundation`.
Estado do aplicativo: `bootstrap-implemented`.
Status: implementação do produto autorizada por feature SDD delimitada;
nenhum componente do produto será tratado como implementado ou validado
sem evidência concreta.

O trabalho de governança e biblioteca foi registrado como etapa preparatória,
com observações históricas preservadas. A transição de governança é tratada
pela feature `sdd/features/product-foundation/` e não implementa código do aplicativo.
Entregas futuras usam features `product-*` independentes, com escopo autorizado.
Correções locais seguem a rota proporcional definida no workflow. Isso não autoriza automaticamente deploy,
acesso externo, gasto, alteração de políticas ou ações destrutivas.

## Autoridades

- `docs/constitution.md`: políticas permanentes do Ox.
- `AGENTS.md`: entrada operacional e referências.
- `sdd/constitution.md`: apontador para a constituição, sem segunda política.
- `sdd/workflow.md`: escolha da rota e ciclo de desenvolvimento.
- `sdd/evidence.md`: estados, evidências e aceitação.
- `docs/architecture/context.md`: componentes e marcos planejados.
- `docs/decisions/*.md`: decisões vigentes, históricas e pendentes.

## Features e métodos

`adoption-governance` e `governance-externalization` são históricas.
As nove features `skill-*` validam a autoria e a seleção da biblioteca,
não o funcionamento de módulos do produto.

Features do aplicativo usam prefixo `product-*`, permanecem diretamente
em `sdd/features/` e possuem requisitos, oráculos, evidências e estados
independentes dos SDDs das skills. A rota local segue `sdd/workflow.md`;
não abrir feature completa apenas para cumprir formalidade.

As 29 skills e 29 pontes continuam disponíveis conforme o perfil versionado.
Uma competência primária é selecionada somente quando pertinente;
auxiliares exigem perguntas técnicas distintas. Disponibilidade,
indicação, seleção, consulta e uso não são equivalentes.
O guia `docs/development/sdd-skills.md` mostra o intercâmbio com as pontes,
sem modificar o procedimento técnico das skills.

## Stack e situação técnica

Decidido para o código próprio do produto: Rust e Iced, com proibição de
`unsafe` próprio conforme `POL-01`. O armazenamento controlado pelo Ox será
local no MVP; LSP e capacidades avançadas serão integrados por plugins.

**Baseline histórica no pacote-base de 26/10/2026:** nenhum `Cargo.toml`,
lockfile ou crate de produto estava presente. Esta afirmação descreve a
baseline; o estado atual está descrito abaixo.
Estado atual: workspace em `application/`, 16 crates e janela mínima. Escopo autorizado:
`product-bootstrap`, execução do prompt v2.0. Linux x86_64 e toolchain stable
confirmados pelo mantenedor. Iced 0.14.0, edição 2024 e piso Rust 1.99 conforme
`docs/decisions/product-bootstrap.md`. Aceitação em `sdd/features/product-bootstrap/`;
F0 não concluída apenas por esta estrutura.

Ferramentas de governança atuais: Python 3.11+ e stdlib. O SDD 1.3.0 e
seu validador original permanecem preservados; essas ferramentas não são
o código Rust do aplicativo.

Organização vigente: ferramentas e testes em `tools/governance/`, dados de
avaliação em `tools/governance/tests/fixtures/`, perfil e cobertura normativa em
`config/governance/`; `application/` contém o workspace virtual Rust, separado da governança.
Fontes e testes ficam em `application/crates/<crate>/src/` e
`application/crates/<crate>/tests/`; a raiz do workspace não contém src/ ou tests/.
A ADR `docs/decisions/governance-layout.md` sucede somente
as decisões antigas de localização e allowlist, preservando seus registros.

## Comandos disponíveis — governança

Da raiz Ox, enquanto esses scripts existirem:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 sdd/tools/validate.py --root .
PYTHONDONTWRITEBYTECODE=1 python3 sdd/tools/validate.py --root . --structure-only
PYTHONDONTWRITEBYTECODE=1 python3 tools/governance/scripts/check-ox.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools/governance/tests -v
PYTHONDONTWRITEBYTECODE=1 python3 tools/governance/scripts/run-checks.py
```

Comandos do produto: `cd application`, `cargo check --workspace`,
`cargo test --workspace`, `cargo test --workspace -- --list`,
`cargo fmt --all -- --check`, `cargo clippy --workspace --all-targets -- -D warnings`
e `cargo run -p ox-app --bin ox`.
Nenhuma saída dos comandos Python valida o aplicativo Rust/Iced.

## Decisões pendentes e limites

Consultar `docs/decisions/open-questions.md` antes de selecionar plataforma,
versões, runtime, IPC, banco, sandbox, agentes ou distribuição.
Autorização de feature não substitui política de risco e permissões efetivas.
Não solicitar `--require-approved` global enquanto houver critérios técnicos
intencionalmente NÃO VERIFICADO.

## Histórico da biblioteca

O catálogo ativo está em `.codex/skills/`. As 29 pontes usam essa localização.
Registros históricos em `docs/validation/` preservam caminhos, hashes e limites
anteriores; não são fontes do estado atual do aplicativo. Os três estudos
externos não pertencem à distribuição nem ao processo de validação.
