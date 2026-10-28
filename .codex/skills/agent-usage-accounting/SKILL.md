---
name: agent-usage-accounting
description: Model and reconcile agent token, cache and cost usage with provenance, idempotency and explicit uncertainty. Use for multi-session usage ledgers; skip generic CPU metrics and task-progress scoring.
---

# agent-usage-accounting

## Responsabilidade e seleção

Modelar métricas de agentes e modelos (tokens, cache, contexto, custos, períodos e sessões) com origem, precisão, unidades, idempotência e regras de agregação auditáveis.

Selecionar: Contagem de tokens por chat/dia/projeto, custos multimodelo, janela de contexto, cache, preços e relatórios de uso.

Não selecionar: Não selecionar para instrumentar CPU/RAM genericamente; observability-and-diagnostics. Não confundir progresso funcional com consumo de contexto.

## Entradas e lacunas

eventos de provedores/agentes, tipos de tokens/caches, tarifas versionadas, intervalos, identidade de sessão/tarefa.

Inspecione os contratos e recursos reais antes de executar. Ausência de versão exige consulta à documentação correspondente; ausência de permissão impede o efeito dependente. Registre a lacuna, seu impacto e como resolvê-la, continuando partes independentes. Os exemplos deste pacote são contratos de avaliação, não APIs ou políticas impostas a todos os consumidores.

## Procedimento operacional

1. Inventory actual provider/adapter events and distinguish reported totals, deltas, local estimates and absent fields. Record units, source, request/session/attempt identity, event time, observation time and timezone policy.

2. Define an idempotency key at the provider/account/request/event scope. A replay of the same event must not add usage; a retry that consumed a new request may legitimately add usage. Duplicate IDs with conflicting payloads require reconciliation, not silent overwrite.

3. Normalize token categories without double-counting subsets. Determine whether cached input is included in total input and whether streaming records are cumulative snapshots or deltas. Preserve raw reports and correction events.

4. Calculate cost only with a versioned tariff, currency, unit denominator and applicability interval. Missing price or usage yields unknown or explicitly partial totals. Use exact decimal arithmetic and a defined rounding policy for currency.

5. Aggregate by explicit half-open time intervals and timezone, retaining event-time versus arrival-time distinctions. Keep current context occupancy, cumulative consumption, monetary cost and functional progress separate.

6. Replay duplicates, partial streams, cache-inclusive totals, missing tariff and a day-boundary event. Reconcile with the observed provider contract without exposing content/credentials. Deliver ledger schema, aggregation examples and uncertainty labels; telemetry conventions alone do not certify an invoice.

## Entregáveis e aceitação

esquema de ledger de uso, regras para duplicação e gaps, visões por período, proveniência e precisão das estimativas.

Vincule cada conclusão a input observado, método, resultado e limite. Execute casos esperados, de borda e de falha de [avaliações](references/evaluation-cases.md) no ambiente autorizado; diferencie resultado de revisão, simulação e integração. Casos apenas escritos continuam não executados. O texto da skill não prova eficácia nem concede autoridade.

## Fronteiras e encaminhamento

`observability-and-diagnostics` — O evento de uso chega integralmente e pode ser correlacionado sem violar privacidade?

Encaminhe somente a pergunta técnica distinta ainda não resolvida, com escopo, IDs de critérios, fatos, lacunas e evidência requerida. Confirme disponibilidade antes da consulta. Uma menção não instala, delega, executa nem carrega recursivamente outras skills. A autoridade de comportamento pertence ao contrato do consumidor; a skill oferece o método.

## Referências especializadas

- [usage-event-schema](references/usage-event-schema.md): consultar para Usage event identity.
- [accounting-and-reconciliation](references/accounting-and-reconciliation.md): consultar para Replay, corrections and totals.
- [context-and-cost-estimates](references/context-and-cost-estimates.md): consultar para Time, context and price.

Fontes oficiais acessadas em 2026-10-26 são citadas junto às afirmações. Versão consultada não é versão adotada pelo consumidor. Sínteses operacionais e esquemas de exemplo são decisões de método desta skill, sem promessa de implementação ou compatibilidade futura.

## Responsabilidades adjacentes

A competência própria acima não substitui os métodos gerais abaixo. Consultar apenas quando a questão correspondente permanecer aberta; nenhum encaminhamento é obrigatório.

| Competência | Autoridade técnica adjacente |
|---|---|
| `ai-engineering` | modelos, rag, agentes com ferramentas, diagnóstico e avaliação de resultados |
| `observability-and-diagnostics` | instrumentação, logs, métricas, traces, investigação causal |
| `application-security` | fronteiras de confiança, segredos, autorizações e ameaças |
| `database-engineering` | persistência, esquemas, invariantes transacionais e migrações |
| `engineering-productivity` | avaliação de fluxos e ferramentas de trabalho com evidência |
| `performance-engineering` | benchmarks, profiling, comparações reproduzíveis e regressões |
| `software-testing` | casos, oráculos, testes automatizados, suites e regressões |
