# Failure controls and decision criteria

Read only the sections relevant to the current failure. These are contextual engineering recommendations synthesized from Michael T. Nygard, *Release It!*, Second Edition, P1.0 January2018, available locally as Release It.epub (historical library source: `docs/system/Release It.epub`; not required at runtime). Locations below are archive XHTML paths, not page numbers. Historical product defaults are not current implementation authority. Verify the selected runtime/client's official documentation before using its APIs.

## Bound waiting, then verify what stops

**Action/context:** For an operation crossing a process or scarce-resource boundary, identify its caller deadline and allocate budgets for queueing, acquisition, connection setup, request/response and cleanup. Propagate remaining budgets where supported. Measure with the runtime's suitable elapsed-time clock. Check DNS/TLS, streaming and pool waits separately; a similarly named socket option may cover only one phase.

**Rationale/evidence:** Unbounded waiting retains resources and transfers a dependency fault to callers. Nygard Ch2 f_0018–0025 and Ch4 f_0034/0038; Ch5 f_0048 “Timeouts.” [AWS timeout guidance](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/) also warns about uncovered connection phases.

**Exceptions/costs:** Long-running jobs can use durable asynchronous progress and leases instead of a short synchronous deadline. Tight deadlines reject legitimate slow work; loose ones retain resources longer. Cancellation may be cooperative or impossible after a remote commit. Do not assume killing the caller rolls back the callee.

**Validate:** Inject delayed connect, response, pool acquisition and cancellation at relevant points. Assert caller completion bounds, release of acquired resources and no continuing unbounded work. Test cold connections and startup separately from warm traffic.

## Retry only when both semantics and capacity permit

**Action/context:** Classify failures as permanent, transient, overload or ambiguous completion. Retry only operations whose repeated effects are acceptable or protected by an actual idempotency/deduplication contract. Assign retry ownership, total attempt/time limits, jitter and an aggregate budget. Stop when the result is no longer useful; obey documented server delay semantics without exceeding the caller budget.

**Rationale/evidence:** Retry storms can prevent recovery. Nygard f_0034, f_0042, f_0048, f_0058–0059; [AWS retries and jitter](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/) and [Google SRE Ch21, Deciding to Retry](https://sre.google/sre-book/handling-overload/). Do not copy their example attempt counts or ratios.

**Exceptions/costs:** A durable job may retry over a longer window with observable ownership and expiry. Idempotency needs a defined key scope, concurrent-attempt behavior, retention period and handling of the same key with different payloads. Read-only calls can still be expensive. Retries add load and latency; immediate retry needs evidence of spare capacity, not merely a server error code.

**Validate:** Count downstream attempts across all layers; test repeated, concurrent and delayed delivery, ambiguous acknowledgments, cancellation and budget exhaustion. Verify the business effect, not only the HTTP response.

**Illustrative example, not executed:** Before: a timed-out payment request is repeated with a new identifier. After: preserve the logical operation identifier, query/reconcile an unknown outcome, and retry only within the provider's documented idempotency contract. A timeout can still leave the user awaiting a final outcome; do not falsely report a failed payment.

## Choose breakers by failure mode

**Action/context:** Consider a circuit breaker for a dependency whose repeated failing/slow calls would consume essential capacity. Define failure classification, measurement window, trip/recovery thresholds, bounded half-open probes, concurrency behavior and per-dependency or per-tenant scope. Make the fallback explicit.

**Rationale/evidence:** Nygard f_0049 and its circuit-breaker diagram explain closed/open/half-open transitions. AWS's article cautions that additional states can delay recovery. The decision depends on avoided load versus state complexity; a retry budget/admission limit may suffice.

**Exceptions/costs:** Low traffic may yield poor estimates; shared state adds coordination and another dependency, while local state permits multiple probes across replicas. Business validation errors should not normally trip infrastructure protection. Breaking a critical operation can trade data freshness or functionality for resource survival.

**Validate:** Exercise every transition, concurrent probes, slow failures, stale state, restart and dependency recovery. Measure whether the intended load is actually removed and whether healthy traffic is unfairly rejected.

## Bound resources and contain propagation

**Action/context:** Inventory queues, in-flight work, pools, sessions, caches, file descriptors, storage and scheduled jobs along the path. Set capacity and expiry from workload/resource evidence. Reject, defer, coalesce or degrade work according to its contract. Separate competing workloads where shared resources allow one to starve another; inspect hidden database, broker, host and control-plane dependencies.

**Rationale/evidence:** Nygard f_0035–0045 (chain/cascade, scale, dogpile, result bounds), f_0050–0051 (bulkheads/steady state), f_0056–0059 (messaging, shedding, backpressure, governors). Google Ch21 explains that rejection and connections also consume capacity, and per-request resource cost can vary.

**Exceptions/costs:** Isolation can strand spare capacity and increase operational complexity. Durable queues shift pressure to storage and replay; they do not eliminate failure propagation. A bounded queue can still wait forever without service progress or expiry. Retention must respect domain obligations, not indiscriminately discard state. Autoscaling has lag and downstream limits.

**Validate:** Drive sustained overload, burst, tenant skew and slow consumption. Assert queue/resource ceilings, fairness, user outcome, rejection cost and recovery after input returns to normal. Include uncached and nonstandard request paths. Verify that another workload remains usable.

## Fail safely and recover deliberately

**Action/context:** Release independent resources even when another cleanup step fails. Isolate restartable units, bound restart rate and make startup/reintegration observable. Define degradation per operation: omit optional recommendations, serve explicitly permitted stale data, queue with truthful status or return a clear failure.

**Rationale/evidence:** Nygard Ch2 cleanup failure; f_0052–0054 fail-fast/crash/handshake; f_0081 transparency; f_0097–0100 control plane. Preflight checks do not eliminate races. A process that answers a ping can still fail its user task.

**Exceptions/costs:** Restart loses in-memory state and can cause a cold-cache surge; fallback may overload a secondary service. Fail-closed authorization takes precedence over stale policy availability. Diagnostic dumps help investigation but need data protection. More observability costs storage, CPU and privacy exposure.

**Validate:** Fail cleanup steps independently, exhaust restart budgets, test cold start and reintegration, compare requested and completed operations, and verify no state corruption or unauthorized response. Observe fallback use, backlog age, error outcome and successful recovery rather than only green instance probes.
