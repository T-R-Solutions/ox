---
name: agent-usage-accounting
description: Model and reconcile agent token, cache and cost usage with provenance, idempotency and explicit uncertainty. Use for multi-session usage ledgers; skip generic CPU metrics and task-progress scoring.
---

# agent-usage-accounting

## Responsibility and selection

Model agent and model metrics (tokens, cache, context, costs, periods and sessions) with provenance, accuracy, units, idempotency and auditable aggregation rules.

Select: Token counts by chat/day/project, multi-model costs, context windows, caching, prices and usage reports.

Do not select: generic CPU/RAM instrumentation; use observability-and-diagnostics. Do not confuse functional progress with context consumption.

## Inputs and gaps

provider/agent events, token/cache types, versioned rates, intervals, session/task identity.

Inspect actual contracts, resources and versions; consult documentation for missing versions. Missing permission blocks only its dependent effect; record gaps and continue independent work. Examples are evaluation fixtures, not consumer policy.

## Operating procedure

1. Inventory actual provider/adapter events and distinguish reported totals, deltas, local estimates and absent fields. Record units, source, request/session/attempt identity, event time, observation time and timezone policy.

2. Define an idempotency key at the provider/account/request/event scope. A replay of the same event must not add usage; a retry that consumed a new request may legitimately add usage. Duplicate IDs with conflicting payloads require reconciliation, not silent overwrite.

3. Normalize token categories without double-counting subsets. Determine whether cached input is included in total input and whether streaming records are cumulative snapshots or deltas. Preserve raw reports and correction events.

4. Calculate cost only with a versioned tariff, currency, unit denominator and applicability interval. Missing price or usage yields unknown or explicitly partial totals. Use exact decimal arithmetic and a defined rounding policy for currency.

5. Aggregate by explicit half-open time intervals and timezone, retaining event-time versus arrival-time distinctions. Keep current context occupancy, cumulative consumption, monetary cost and functional progress separate.

6. Replay duplicates, partial streams, cache-inclusive totals, missing tariff and a day-boundary event. Reconcile with the observed provider contract without exposing content/credentials. Deliver ledger schema, aggregation examples and uncertainty labels; telemetry conventions alone do not certify an invoice.

## Deliverables and acceptance

usage ledger schema, duplicate and gap rules, period views, provenance and estimate accuracy.

Bind conclusions to inputs, method, result and limits. Exercise relevant [normal, boundary and failure cases](references/evaluation-cases.md) within authorization; distinguish inspection, simulation and integration. Written cases are not execution evidence.

## Boundaries and handoff

`observability-and-diagnostics` — Does the usage event arrive in full, and can it be correlated without violating privacy?

Consult another available skill only for a distinct unresolved question, with scope, criteria, facts and evidence needs. Mentions never trigger installation, delegation or recursive activation; the consumer contract owns behavior.

## Specialized references

- [usage-event-schema](references/usage-event-schema.md): consult for Usage event identity.
- [accounting-and-reconciliation](references/accounting-and-reconciliation.md): consult for Replay, corrections and totals.
- [context-and-cost-estimates](references/context-and-cost-estimates.md): consult for Time, context and price.

Official sources accessed on 2026-10-26 are cited alongside claims. A consulted version is not a version adopted by the consumer. Operational summaries and example schemas are methodological decisions of this skill, without a promise of implementation or future compatibility.

## Adjacent responsibilities

Adjacent methods are optional; consult only for an unresolved responsibility.

| Capability | Adjacent technical authority |
|---|---|
| `ai-engineering` | models, RAG, agents using tools, diagnostics and outcome evaluation |
| `observability-and-diagnostics` | instrumentation, logs, metrics, traces, causal investigation |
| `application-security` | trust boundaries, secrets, authorization and threats |
| `database-engineering` | persistence, schemas, transactional invariants and migrations |
| `engineering-productivity` | evidence-based evaluation of workflows and tools |
| `performance-engineering` | benchmarks, profiling, reproducible comparisons and regressions |
| `software-testing` | cases, oracles, automated tests, suites and regressions |
