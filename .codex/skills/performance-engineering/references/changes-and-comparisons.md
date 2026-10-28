# Changes and comparisons

Use after an investigation identifies a relevant cost. Sources are Gregg, *Systems Performance*, Second Edition, chapter2 §§2.5.17-2.8 (physical98-116) and chapter5 §§5.1-5.6 (physical210-255), with correctness constraints synthesized from security and reliability research. Printed body pages are physical minus39.

## Choose an intervention with preserved semantics

| Candidate action and context | Technical reason | Exceptions and costs | Validation |
| --- | --- | --- | --- |
| Remove repeated or unnecessary work when a profile identifies it. | Avoiding work can reduce several resource demands together. | Authorization, audit, integrity, recovery and business effects may be necessary even when expensive. | Compare observable results and required side effects, then resource cost per successful operation. |
| Change an algorithm or data structure when measured input growth exposes excess work. | Growth rate may dominate at realistic scale. | Big-O omits constants, locality, allocation and input distributions; it does not establish a measured speedup. | Test representative and adverse sizes/distributions with equivalent results and memory limits. |
| Cache costly repeatable results when freshness and invalidation are defined. | Hits can avoid computation or downstream requests. | Memory, lookup/maintenance cost, warmup, invalidation, tenant/auth partitioning and stale data can outweigh gains. | Measure hit/miss counts and latency plus end-to-end cost, cold starts and correctness after updates/revocation. |
| Batch or buffer operations when fixed per-operation overhead dominates. | Amortizes setup and transfer costs. | Adds waiting, memory pressure, burstiness and potentially changes durability or failure handling. | Compare batch sizes under realistic traffic, tail latency, flush/deadline behavior and recovery. |
| Add concurrency when independent work waits or available resources are underused. | Can overlap waits or use additional execution capacity. | Contention, synchronization, queues and downstream saturation can erase gains; concurrency is not necessarily parallelism. | Preserve invariants; measure throughput, tails and resource cost across a range of concurrency levels. |
| Tune configuration or add capacity when the actual limiting resource is established. | Can remove an imposed limit or resource shortage. | Quotas, startup delay, cost, shared dependencies and workload drift remain; affinity and oversized pools may worsen contention. | Validate the combined configuration and relevant workload envelope, including recovery/headroom. |

Evidence: chapter2 §§2.5.18-2.5.20,2.7; chapter5 §§5.1.4,5.2,5.3.4. These are alternatives, not a compulsory optimization sequence. Thread/process, blocking/asynchronous, compiler, runtime, and operating-system choices depend on isolation, tooling and workload. Do not prescribe a language rewrite from a generic performance ranking. Do not disable required security mitigations, checksums, transaction logging or synchronization to improve a benchmark.

## Make the comparison answer the original question

If the decision depends on inferential uncertainty, equivalence or a practical
effect margin, use [benchmark inference](benchmark-inference.md) for the analysis
unit, exclusions and stopping rules before selecting a statistical method.

**Action/context:** Before executing a benchmark or optimization comparison, define success, equivalent behavior, measurement boundaries, representative workload, environment, warmup, duration, run order and a variability strategy. Keep revisions and input data identifiable. Capture failures and resource costs alongside successful throughput and latency. State whether the generator is open-loop or waits for responses; a waiting generator may suppress offered load during stalls. Include warmup, cache/compilation state, data distribution and generator resource limits.

**Evidence:** Chapter1 §1.11 (physical57-58), chapter2 §§2.5.16,2.5.19,2.6-2.8 (physical98-116), chapter5 §5.1 (physical210-214). Chapter12, physical680–709, adds benchmarking pitfalls, workload characterization and analysis; chapter16, physical822–833, supplies contextual case studies rather than transferable performance results.

**Reason:** A saturated generator, changed request mix, cache state, measurement unit or correctness failure can produce a plausible but irrelevant improvement. A narrow microbenchmark isolates a mechanism; system validation establishes whether it matters to the real objective.

**Exceptions/costs:** Production reproduction may be unsafe or unavailable. Use an authorized test environment or observation-based estimate and disclose its external-validity limit. Repetition is useful when noise affects the decision, not a fixed ritual or invented confidence percentage. Combining interventions may be necessary for a coherent change; explain attribution limits.

**Validation:** Run independent correctness checks appropriate to the changed behavior. Retain raw results and report variation, sample counts, setup and scope. Compare affected and neighboring workloads, inspect remaining bottlenecks, and distinguish an observed association from a tested causal mechanism. If a regression appears, investigate it rather than dropping that run without a stated reason. Verify the benchmark itself performs the claimed work; a phase with no physical I/O or one expensive worker can make a score misleading. Test enough steady-state and adverse conditions to support the decision, without imposing a universal run duration, language, repetition count or cost horizon.

## Illustrative decision example

A service meets its throughput target, but CPU time per successful request increases after a change. A generator that sends requests serially may conceal reduced capacity. First check the request mix, successful outcomes, generator concurrency/headroom and per-request CPU attribution. If profiling identifies repeated parsing, cache or reuse only when input identity, lifetime and mutation semantics permit it. Compare correctness and representative throughput/latency/resource cost before claiming improvement.

This is an illustrative reasoning example, not executed code, a benchmark result, or a promised gain.


## Resource changes require contract checks

**Action/context:** Before changing CPU affinity/governors, memory policy, caches, file-system layout, I/O batching, network buffers or cloud capacity, connect the setting to the measured limit and preserve isolation, security, durability and recovery. Read only the platform documentation needed for the actual setting.

**Evidence/reason:** Chapters6–11, physical258–679. A queue or cache moves cost across time/resources; it does not remove correctness obligations. Acknowledging writes sooner can improve measured latency by weakening durability. Larger pools or replicas can overload dependencies.

**Exceptions/costs:** More memory, redundancy, capacity or reserved resources can be the appropriate engineering choice despite higher cost. Conversely, a small bounded workload may not justify tuning. Cache warmup, failover, rebuild, noisy neighbors, storage write amplification and allocator retention can change steady-state results. Do not assume historical hardware tables, provider offerings or defaults remain current.

**Validation:** Recheck the relevant invariant and a representative workload after the coherent change. Include cold/startup and degraded conditions when they matter to the contract, record cost and residual limits, and maintain a feasible reversal or recovery path. No source example establishes a gain for a different environment.
