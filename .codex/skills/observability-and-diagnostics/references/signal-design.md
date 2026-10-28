# Signals that answer a question

Read before adding instrumentation or changing a telemetry contract.

For each operational question define observation boundary, event population, fields,
unit, aggregation/window, expected query and owner. Structured logs can retain discrete
state/error detail; metrics summarize populations; traces describe request paths.
Correlate with service/version, time and safe trace/span/operation identifiers without
making those identifiers unbounded metric labels. Clock order alone is not causality.
[OpenTelemetry concepts](https://opentelemetry.io/docs/concepts/).

Inject/extract context at HTTP/RPC boundaries and message publication/consumption;
check queues, task schedulers, thread switches and retries. Use parent/links according
to actual asynchronous and batch relationships. W3C traceparent/tracestate describe
trace context, not authorization. Validate incoming context, trust boundaries and
privacy; baggage may propagate sensitive data. Verify failed/duplicate deliveries
and context isolation across concurrent requests.
[OTel propagation](https://opentelemetry.io/docs/concepts/context-propagation/),
[W3C Trace Context §§3–6](https://www.w3.org/TR/2021/REC-trace-context-1-20211123/).

Discover API/SDK, instrumentation and semantic-convention versions independently;
stability is signal/component-specific. Renaming attributes, units or metrics can
break alerts even if application APIs compile. Verify actual telemetry and update
queries/consumers with coexistence where needed; do not assume automatic schema
transformation guarantees. [OTel stability, semantic conventions](https://opentelemetry.io/docs/specs/otel/versioning-and-stability/).

Estimate label combinations and churn from dimensions before selecting labels.
Use bounded operation/route categories instead of raw URL/user/request IDs; retain
needed individual detail in access-controlled logs/traces where supported. Backend
budgets are project facts; numeric examples from Prometheus are not universal limits.
[Instrumentation, labels and overhead](https://prometheus.io/docs/practices/instrumentation/).

Preserve count, sum and distribution when needed. Choose histogram buckets/resolution
from the question and range; aggregation needs compatible schemas and populations.
Do not average p99s to obtain a global p99. Specify interval/rate/reset semantics and
sparse-traffic behavior. [Histograms and summaries](https://prometheus.io/docs/practices/histograms/).

Head sampling cannot guarantee retention of errors learned later. Tail selection needs
buffering, trace routing and bounded decision delay; it cannot recover discarded
upstream spans. Compare sampled paths with independent error counts, handle late spans
and do not treat biased samples as exact denominators.
[Sampling, head/tail](https://opentelemetry.io/docs/concepts/sampling/).

Minimize sensitive payloads, redact before export and apply actual retention/access
rules. Bound queues, retries, payload size and overhead; choose loss vs backpressure
with application consequences explicit. Monitor queue occupancy/age, rejected/dropped
items and export failures independently where feasible. Collector restart, retry
exhaustion, queue overflow or disk failure can lose telemetry even with persistence.
[Collector resiliency](https://opentelemetry.io/docs/collector/resiliency/).
Exercise a known lost/export-failed event and check that the observer reports the gap
instead of turning an empty result into success.
