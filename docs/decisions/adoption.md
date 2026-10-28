# ADR de adoção da biblioteca e governança

Estado: adotado neste escopo pelo pedido explícito do mantenedor, em 2026-10-26. Não é aprovação geral da arquitetura de produto.

## Autoridade vigente

A adoção inicial utilizou estudos externos. Essa história não incorpora normas por referência. A revisão autorizada [governance-externalization](governance-externalization.md) substitui a dependência documental e os antigos AC-01/AC-03 da adoção. Políticas estão em docs/constitution.md; rotas e evidências em sdd/workflow.md e sdd/evidence.md; perfil em src/fixtures/profile.json. O catálogo continua com 17 gerais, 3 condicionais e 9 especializações. Os estudos não são distribuídos nem consultados em validação.

## Histórico da escolha inicial

Escolha: uma constituição em docs, SDD como contrato da mudança e skills reutilizáveis. Alternativas rejeitadas: duplicar políticas em skills, importar todo catálogo ou usar referências operacionais à biblioteca externa. Consequência: atualizações precisam comparar as cópias e preservar ajustes, mas Ox pode ser separado da origem.

A proibição de unsafe aplica-se a código próprio, sem exceção interna nesta configuração. A skill rust permanece genérica. Dependências com unsafe/C/FFI não são automaticamente proibidas nem aprovadas; avaliar por versão e risco. Uma futura mudança da regra exige decisão explícita anterior à exceção.

## Divergências entre proposta e árvore real

- Os caminhos `skills/skills/`, `skills/sdd/model/`, `skills/sdd/chain/` do ZIP resolvem para `skills/`, `sdd/model/`, `sdd/chain/` da biblioteca. `doc/structure/README.md` confirma a migração; rótulos antigos não são configuração.
- Há 23 skills e 23 pontes na origem; somente 20 pares entram no perfil. As nove especializações não existiam e foram autoradas, sem alegar consulta durante autoria.
- Inicialmente Ox tinha só os três documentos e nenhum arquivo de aplicação. Não há Git disponível; preservação usa bytes e hashes, incluindo árvore externa.
- As pontes propostas usam UNCONFIGURED; as operacionais recebem paths reais. O cache `__pycache__` encontrado no modelo não é fonte ou contrato e foi omitido.
- O validador resolve links Markdown do modelo dentro de sdd e de cada skill dentro da própria pasta. Referências à autoridade do projeto em sdd usam caminhos em código relativos à raiz, sem alterar o validador nem duplicar políticas.
- A seção 8 selecionava nominalmente a skill ainda futura. Na autoria, essa seleção foi corrigida para skill-creator efetivamente consultada; a nova competência fica disponível para avaliação e uso posteriores.

Reavaliar fronteiras após falha observada de seleção, atualização de contrato ou adoção de versões reais. Revisão de diff e hashes é feita pelo executor, sem alegação de revisão humana independente.

## Correção autorizada de localização

O pedido posterior do mantenedor substitui somente o destino das skills por `.codex/skills/`. A escrita nesse diretório de Ox foi explicitamente autorizada; não se alteram diretórios gerenciados da biblioteca externa. Origens e resultados históricos conservam seus caminhos da época, com mapa em `docs/validation/skills-location-001/relocation.json`.
