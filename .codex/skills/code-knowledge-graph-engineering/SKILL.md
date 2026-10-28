---
name: code-knowledge-graph-engineering
description: Design typed code knowledge graphs with evidence-backed edges, incremental invalidation and bounded impact queries. Use for code relationship semantics; skip static diagrams and embedding similarity presented as resolved calls.
---

# code-knowledge-graph-engineering

## Responsabilidade e seleção

Modelar e consultar grafos de símbolos, chamadas, arquivos, testes, regras e tarefas, distinguindo relações verificadas de hipóteses e evitando visualização de dados obsoletos.

Selecionar: Schema de nós/arestas, provenance, análise de impacto, caminhos, clusters e visualização por subgrafo/densidade.

Não selecionar: Não selecionar para fazer um grafo de marketing ou apresentação estática; design-system/design-review. Não substituir compilador/LSP por embeddings.

## Entradas e lacunas

identidades estáveis, relações extraídas/inferidas, snapshots, consultas de impacto, limites de cardinalidade e layout.

Inspecione os contratos e recursos reais antes de executar. Ausência de versão exige consulta à documentação correspondente; ausência de permissão impede o efeito dependente. Registre a lacuna, seu impacto e como resolvê-la, continuando partes independentes. Os exemplos deste pacote são contratos de avaliação, não APIs ou políticas impostas a todos os consumidores.

## Procedimento operacional

1. Define node identity, edge type, direction, cardinality and evidence requirements before choosing a graph store. Separate structural relations, semantic resolution and inference with incompatible labels when appropriate.

2. Attach snapshot, source range, extraction method/version and originating evidence to every edge. A numeric similarity score cannot upgrade an inferred edge to verified. Validate endpoint existence in the same generation.

3. Publish incremental updates coherently: remove or invalidate edges dependent on changed/deleted evidence, then add replacements. Retain historical generations for traceability without exposing them as current.

4. Define query semantics and bounds: permitted edge classes, direction, depth, node/edge limits, timeout, cancellation and truncation metadata. Traverse with visited sets to handle cycles and deduplicate stable identities.

5. Keep logical graph data separate from layout. Structural and dense exploratory views should project the same snapshot with different filters; cluster membership/layout position is not a new factual edge. Pause expensive layout when hidden.

6. Test known calls, mislabeled inferences, deleted sources and a deterministic dense cyclic graph. Check provenance, orphan handling and explicit truncation. Deliver schema, bounded queries, before/after fixtures and UI-performance gaps separately.

## Entregáveis e aceitação

contrato de grafo versionado, consultas com limites, rastreabilidade de arestas, políticas de invalidação, modos estruturais/densos.

Vincule cada conclusão a input observado, método, resultado e limite. Execute casos esperados, de borda e de falha de [avaliações](references/evaluation-cases.md) no ambiente autorizado; diferencie resultado de revisão, simulação e integração. Casos apenas escritos continuam não executados. O texto da skill não prova eficácia nem concede autoridade.

## Fronteiras e encaminhamento

`code-context-engineering` — A origem da aresta pode ser verificada no snapshot de código indexado?

Encaminhe somente a pergunta técnica distinta ainda não resolvida, com escopo, IDs de critérios, fatos, lacunas e evidência requerida. Confirme disponibilidade antes da consulta. Uma menção não instala, delega, executa nem carrega recursivamente outras skills. A autoridade de comportamento pertence ao contrato do consumidor; a skill oferece o método.

## Referências especializadas

- [graph-schema-and-evidence](references/graph-schema-and-evidence.md): consultar para Evidence-bearing graph schema.
- [incremental-graph-updates](references/incremental-graph-updates.md): consultar para Remove stale relationships deliberately.
- [graph-queries-and-visualization](references/graph-queries-and-visualization.md): consultar para Bounded traversal and honest views.

Fontes oficiais acessadas em 2026-10-26 são citadas junto às afirmações. Versão consultada não é versão adotada pelo consumidor. Sínteses operacionais e esquemas de exemplo são decisões de método desta skill, sem promessa de implementação ou compatibilidade futura.

## Responsabilidades adjacentes

A competência própria acima não substitui os métodos gerais abaixo. Consultar apenas quando a questão correspondente permanecer aberta; nenhum encaminhamento é obrigatório.

| Competência | Autoridade técnica adjacente |
|---|---|
| `ai-engineering` | modelos, rag, agentes com ferramentas, diagnóstico e avaliação de resultados |
| `database-engineering` | persistência, esquemas, invariantes transacionais e migrações |
| `design-system` | tokens, componentes, estados e contratos de ui |
| `domain-modeling` | regras de domínio, invariantes, conceitos de tarefa/agente/política |
| `performance-engineering` | benchmarks, profiling, comparações reproduzíveis e regressões |
| `software-architecture` | fronteiras, integração, atributos de qualidade, adrs |
| `software-design` | interfaces, coesão, acoplamento, refatoração localizada |
| `software-testing` | casos, oráculos, testes automatizados, suites e regressões |
