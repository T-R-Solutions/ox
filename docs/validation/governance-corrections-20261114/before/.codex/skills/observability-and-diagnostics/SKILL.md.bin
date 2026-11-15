---
name: observability-and-diagnostics
description: Design telemetry or investigate operational symptoms using correlated signals and discriminating observations. Use for missing diagnostic context, instrumentation correctness, or an evidence-led runtime investigation; skip routine logging edits, straightforward local defects, and tuning or recovery policy with no diagnostic question.
---

# Observability and Diagnostics

Own the measurement path and evidence-led investigation. Discover the affected
operation, symptom/window/cohort, topology, versions, existing logs/metrics/traces,
SDK/collector/backend contracts, access, retention and cost constraints. Reuse the
project's tools. No mandatory backend, distributed deployment or universal SLO.

## Procedure

1. State the operational question and what observation could distinguish competing
   explanations. Map question → necessary signal → instrumentation → investigation.
   Do not add every available metric merely because collection is possible.
2. For instrumentation read [signal design](references/signal-design.md). Establish
   boundaries, context propagation, schema/units, cardinality, sampling, redaction,
   overhead and loss behavior before implementation.
3. For investigation read [hypothesis and evidence](references/hypothesis-and-evidence.md).
   Build a timeline, preserve sanitized raw evidence, compare plausible hypotheses
   and obtain the smallest discriminating observation. Mitigation may precede a
   confirmed cause; label that distinction.
4. Implement the needed probe, correlation, alert or diagnostic fix. Use bounded
   authorized collection and handle telemetry/export failures without uncontrolled
   application latency or memory growth.
5. For instrumentation changes, validate a known success/error workload and affected
   asynchronous or exporter-failure paths when available. For diagnosis alone, check
   the discriminating observation; do not build instrumentation without a need. Reconcile independent counts, redaction, units, context,
   sampling gaps, alert fire/reset and useful runbook steps. A dashboard's existence
   is not proof of detection or diagnostic usefulness.

## Output and limits

Deliver working instrumentation or a supported diagnosis, signal definitions,
evidence, rejected hypotheses, observed checks and remaining uncertainty. Correlation
and a span parent relationship do not alone prove a defect's root cause. Missing
telemetry is not zero failures. State whether a proposed experiment actually ran.
Reliability policy, profiling and product-specific database mechanics have separate
owners; available specialists are conditional and never mandatory dependencies.
This skill works alone and requires no SDD or research ledger at runtime.
