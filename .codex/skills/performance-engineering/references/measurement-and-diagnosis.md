# Measurement and diagnosis

Use this reference when choosing metrics, instrumentation, or a causal investigation. Local source: Brendan Gregg, *Systems Performance*, Second Edition (2021), `docs/system/Systems Performance_ Enterprise and the Cloud.pdf`. PDF physical pages are one-based; body printed page = physical page minus39. These are context-dependent engineering recommendations synthesized from the cited sections, not platform guarantees.

## Define the operation and workload

**Action/context:** Before investigating slow requests or expensive capacity, define the affected user operation and its observation boundary. Record input size/distribution, request mix, concurrency or arrival process, data/cache state, errors and relevant deadlines. Separate offered work from successful completions.

**Evidence:** Chapter1 §§1.4-1.11, physical43-58; chapter2 §§2.4,2.5.5,2.5.11, physical76-84,93; chapter5 §5.1, physical210-214.

**Reason:** Equal requests per second can hide more expensive requests, failed work, or a constrained generator. End-user latency can differ from a server timer that excludes queues, transport or retries.

**Exceptions/costs:** A bounded single-function investigation may need a smaller workload model. Detailed production traces can expose data and cost storage; capture only the information needed and protect it. Historical data may be the only baseline: disclose confounding changes.

**Validation:** Reproduce the symptom or establish its time window, verify that the selected measurements include the affected population, and confirm generator/observer headroom. Include canceled, failed and unfinished work in the accounting rather than silently excluding it.

## Combine workload and resource evidence

**Action/context:** Inspect rate, errors and duration alongside utilization, saturation and errors of resources along the actual request path. Include thread/connection pools, file descriptors and imposed quotas when relevant. Check individual instances/cores and short intervals when aggregate values conceal contention.

**Evidence:** Chapter2 §§2.4,2.5.9-2.5.13, physical76-96; chapter5 §§5.4.4-5.4.5, physical232-236.

**Reason:** Resource busy time is not capacity, a low host average can hide a throttled tenant or one saturated worker, and a resource anomaly may not explain the user symptom.

**Exceptions/costs:** USE/RED are investigative starting points, not proof of complete coverage. Caches need hit/miss/cost analysis rather than treating full capacity as unhealthy. Unavailable counters remain explicit unknowns; do not fabricate them.

**Validation:** Quantify whether the suspected resource contributes to the relevant delay or cost. Check queue waits and affected operations, not a universal60%/80% utilization threshold. Confirm that a proposed capacity change moves the predicted limit under the same workload.

## Attribute time to the critical path

**Action/context:** Split operation time into meaningful execution and waiting components, then investigate the dominant relevant component. For CPU-bound work, inspect sampled code paths; for waits, distinguish scheduling delay, I/O, lock ownership and idle workers. Track overlapping/asynchronous work separately.

**Evidence:** Chapter2 §§2.5.12-2.5.15, physical94-97; chapter5 §§5.4.1-5.4.6, physical226-237.

**Reason:** CPU samples show CPU consumption, not off-CPU delay. Aggregated worker wait time is often dominated by idle workers. Summing parallel spans overstates elapsed latency; removing an off-path event does not directly save its duration.

**Exceptions/costs:** Off-CPU tracing can be expensive; filters can remove important long waits or short repeated events. Application-level tracing may provide better request context while missing kernel delays. Kernel profiling may miss language context or permissions. Choose by question rather than a mandatory profiler hierarchy.

**Validation:** Confirm symbol/stack completeness, sample population, event loss and units. A flame graph's width represents its configured weight; horizontal ordering is not a timeline. Correlate profiles with the affected requests and investigate lock-holder behavior when lock wait dominates.

## Treat instrumentation as a measurement system

**Action/context:** Identify each metric's source, interval, scope, unit, accumulation/reset behavior and collection overhead. Prefer bounded sampling or summaries when full event traces are unnecessary; use deeper tracing for a specific unresolved question.

**Evidence:** Chapter4 §§4.1-4.6, physical168-207; chapter5 §§5.5-5.6, physical238-255.

**Reason:** A collector can alias periodic work, overflow buffers, misparse units, perturb scheduling, or produce incomplete stacks. Different tools reading the same counter are not independent corroboration.

**Exceptions/costs:** Cross-checking every metric is disproportionate. Prioritize consequential or surprising observations. Debuggers, tracefs changes and privileged collectors can affect other workloads; use the authorized scope. Historical book commands are illustrative and unexecuted here.

**Validation:** Compare an appropriate independent source or known controlled workload when feasible. Verify actual tool/kernel/runtime support and cleanup. Record missing symbols, dropped events, sampling exclusions and observer effect instead of treating absent observations as zero.

## Preserve distributions and assumptions

**Action/context:** Report sample counts, useful latency quantiles and distribution/time behavior, not only an average. Use histograms or timelines to investigate modes, tails, periodic load and overlap; state bucket resolution and time range.

**Evidence:** Chapter2 §§2.6-2.10, physical101-124.

**Reason:** Means conceal mixtures and bursts; a p99 leaves the worst1% undescribed. Percentiles remain mathematically valid for multimodal data, despite the book's wording. Model fits require validated assumptions and cannot alone identify mechanisms.

**Exceptions/costs:** A small sample cannot establish a rare tail reliably. Averages can still be useful for resource accounting. Retaining every event may be too costly; disclose aggregation losses. Do not sum or average percentiles as if they were additive measurements.

**Validation:** Check units, weighting, axes, population and model residuals; test predictions against observations outside the fit where feasible. The book's physicalp75 runtime expression uses rates times latency and is not adopted as a runtime formula. Capacity extrapolations remain estimates until validated.


## Select evidence for the resource boundary

Use only the row relevant to the established symptom. These are investigative actions, not a mandatory tool checklist. Source ranges are physical PDF pages.

| Context and action | Rationale and precise evidence | Exceptions, costs and validation |
| --- | --- | --- |
| CPU delay: distinguish execution, runnable delay, topology, quotas and per-core skew. | Busy time, clock rate and IPC do not measure useful work. Chapter6, pp258–341. | Affinity, priority and extra workers can worsen starvation/locality. Validate request latency and successful work under the actual quotas. Linux load average includes uninterruptible tasks and is not a waiting fraction or speedup formula; reject the derivation on pp825/831. |
| Memory growth: separate virtual mappings, resident/shared memory, allocation requests, retention, reclaim and cgroup limits. | Growth or low free memory alone does not establish a leak or pressure. Chapter7, pp342–397. | Heap dumps expose data and perturb workloads; deliberate memory shrinking is an experiment. Check retained ownership, stalls/OOM and application impact. Page faults times page size do not universally equal net RSS growth. |
| File/storage delay: correlate logical operations with physical fanout, metadata, caching, writeback and actual completion boundaries. | Application, OS queue and device timings include different work; hidden device queues remain inside issue-to-completion time. Chapters8–9, pp398–537, especially pp466–467,493–494. | Direct I/O is not a durability guarantee; separate volumes may share bottlenecks. Compare size, direction, locality, concurrency and acknowledgement semantics. A busy parallel device is not necessarily at capacity. Raw-device writes and cache dropping are disruptive experiments. |
| Network delay: separate resolution, connection establishment, response timing, transfer, queues and endpoint capacity. | ICMP timing, application latency and throughput measure different paths. Chapter10, pp538–617. | Capture may expose payloads and drop packets; offload changes what is observed. Correlate both directions/endpoints and retain capture-loss evidence. Do not infer application health from ping or tune buffers without latency/capacity trade-offs. |
| Cloud/container limits: inspect guest/host visibility, hierarchy, CPU bandwidth, shares, storage/network limits and startup. | Host spare capacity can coexist with tenant throttling; replicas add downstream demand. Chapter11, pp618–679. | Provider visibility may be unavailable. State unknowns, cost and noisy-neighbor confounders; verify actual controls and request outcomes. CPU weights are relative, not reservations; cpusets alone do not establish exclusivity. |

For Linux pressure evidence, verify [PSI semantics](https://docs.kernel.org/accounting/psi.html): `some` and `full` cover different stalled populations; system CPU `full` is undefined and reported as zero for compatibility since Linux5.13. Record the resource, system/cgroup scope, averaging window and total-time unit. Do not derive per-request wait probability from these aggregates. This is documented behavior; no PSI monitoring program was executed here.

For current platform interpretation, [Kubernetes metrics documentation](https://kubernetes.io/docs/tasks/debug/debug-cluster/resource-metrics-pipeline/) defines CPU usage as an average rate over a window; `m` is millicores, not accumulated milliseconds. The [nstat manual](https://man7.org/linux/man-pages/man8/nstat.8.html) distinguishes userspace history from absolute counters; resetting history does not reset kernel counters. Verify [cgroup v2 CPU controls](https://www.kernel.org/doc/html/latest/admin-guide/cgroup-v2.html) against the actual kernel and parent hierarchy. These corrections resolve historical examples, not a requirement to use these platforms. Exact consulted scope is in the separate research ledger.

## Make deep tracing answer a bounded question

**Action/context:** When simpler evidence cannot discriminate the mechanism, select a supported event and verify its ABI, arguments, signed return values, correlation keys, timing boundary and aggregation weight. Preserve prior shared tracing configuration and define cleanup.

**Evidence/reason:** Chapters13–15, physical710–821, cover perf, Ftrace and BPF. Entry events may count attempts rather than successful calls, requested bytes differ from completed bytes, syscall and function ABIs differ, and keys can collide across devices/threads or recursion. Missing starts, lost events, unwinding gaps and full maps can bias results.

**Exceptions/costs:** Tracing can expose memory, paths and secrets, consume file descriptors/buffers, and alter scheduling or I/O. A verifier does not make every probe harmless. Avoid active mechanisms such as return-value override or interrupt-disabling latency measurement unless explicitly authorized for the experiment. [Linux perf security](https://docs.kernel.org/admin-guide/perf-security.html) documents privilege and resource controls; choose the least privilege sufficient for the actual observation instead of defaulting to unrestricted root access.

**Validation:** Test event meaning against a controlled known operation where feasible, distinguish requested/completed/failed effects, inspect loss/cardinality, and compare measurement overhead. Record exact kernel/tool/build support, collection duration and cleanup. Historical book one-liners have known typos and assumptions; none are shipped as executable recipes.
