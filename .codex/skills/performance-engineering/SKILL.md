---
name: performance-engineering
description: Investigate software latency, throughput, resource consumption, capacity, and performance regressions using representative workloads, measurements, profiling, and controlled comparisons. Use for explicit performance objectives or evidence of a bottleneck; avoid speculative optimization during ordinary feature work.
---

# Performance Engineering

Make a measurable performance decision while preserving required behavior. Start from the task's requirements, contracts, and acceptance criteria; keep the problem, technical decision, implementation, and validation distinct.

## Activation and boundaries

Use this skill for a reported slowdown, capacity limit, performance budget, benchmark design, resource-cost investigation, or measured optimization. A naming change or ordinary feature with no relevant performance risk does not need this workflow. Basic correctness, resource bounds, security, and accessibility remain necessary without this skill.

Collect the affected operation, user impact, metric boundary, workload, environment/version, recent changes, existing baseline, and access constraints. Distinguish missing evidence from evidence of absence. Use existing project tooling before adding infrastructure.

Performance owns quantitative behavior under stated workloads. Reliability engineering can help with failure propagation, overload policy, recovery, and degradation; distributed systems with consistency and coordination; software design with maintainable changes; software testing with correctness oracles. Load another skill only when its distinct responsibility is needed. A faster result does not authorize weaker authorization, durability, consistency, or validation.

## Workflow

1. **Define success before measuring.** Specify the operation and population, latency distribution or deadline, successful throughput, resource/cost budget, workload range, and tolerated regression elsewhere. Keep requirements separate from a hypothesized solution. Avoid generic targets such as low CPU or fast enough.
2. **Record the baseline.** Capture revisions, runtime/compiler versions, configuration, hardware or quotas, topology, data size/skew, request mix, concurrency/arrival pattern, cache state, warmup, duration, and measurement method. Include errors, cancellations and timeouts. Check the load generator and observer for bottlenecks or interference.
3. **Localize the cost.** Combine request rate/errors/duration with utilization, saturation and errors of relevant resources, including software pools and tenant quotas. Check per-instance/thread skew and intervals. Follow the request's critical path: distinguish CPU execution, runnable delay, blocking, and legitimate idle time. Read [measurement and diagnosis](references/measurement-and-diagnosis.md) when selecting evidence.
4. **Test a hypothesis.** State the suspected mechanism, predicted observation and a discriminating measurement or controlled change. Prefer a bounded observation before disruptive experiments. Verify consequential or surprising metrics with an independent source where feasible. Correlation and an attractive graph do not establish causation.
5. **Choose a proportional change.** Compare eliminating unnecessary work, changing an algorithm/data access pattern, caching, batching, concurrency, configuration and capacity according to measured cost. State correctness constraints, exceptions, maintenance cost and expected effect. Read [changes and comparisons](references/changes-and-comparisons.md) for trade-offs. Do not introduce distribution or a new framework solely to improve a synthetic score.
6. **Validate equivalent conditions.** Run relevant correctness checks and a representative before/after comparison. Preserve raw measurements and units; examine variability, tails, errors, resource cost and remaining bottlenecks. Repetition and run order should address observed variability. A microbenchmark proves only its measured scope.
7. **Conclude honestly.** Report measured results separately from estimates, hypotheses and unmeasured production impact. If evidence is insufficient, provide the specific collection/experiment needed rather than claiming an improvement.

## Constraints and completion

Use tools appropriate to the actual platform and privileges; verify current official documentation before prescribing version-dependent commands or tunables. Do not copy historical hardware ratios, sampling rates or tuning thresholds as universal defaults. Bound profiling duration, event rate, buffers, output volume and sensitive data exposure. Stop or narrow collection when overhead invalidates the measurement or threatens the agreed operating limits.

A complete result identifies the objective, workload/environment, baseline, evidence for the mechanism, change and trade-offs, correctness checks, comparison method/results, limitations, and any needed rollback or follow-up. No measured baseline means no demonstrated gain. Investigation may validly conclude that no optimization is warranted.

## Supporting material

The references above are conditional operational guidance. Source locations and conflicts live in research notes (historical library source: `system/research/operations-reading-progress.md`; not required at runtime), separate from ordinary task context. Comparative skill efficacy has not been demonstrated; see validation record (historical library source: `system/research/operations-validation.md`; not required at runtime).

## Additional investigation references

For retention, allocation or input-growth risks, read
[memory and work](references/memory-and-work.md). For sampling, event loss,
probe validity or eBPF evidence, read
[observation boundaries](references/observation-boundaries.md).

When collection is a plausible mechanism, read
[GC diagnosis](references/gc-diagnosis.md). When a benchmark decision depends on
statistical uncertainty or equivalence, read
[benchmark inference](references/benchmark-inference.md). Load these for the
specific question; they impose no collector, package or universal significance level.

Other named skills are optional specialist suggestions. Use them only when available and needed for a specific unresolved question; their absence does not prevent using this skill. Report any expertise or verification gap without claiming a handoff occurred.

## Adjacent responsibilities

Postgresql can resolve a concrete PostgreSQL plan/statistics mechanism; observability-and-diagnostics a missing telemetry path. Keep quantitative workload comparison here and do not infer improvement from instrumentation alone.
These are optional available capabilities, not dependencies of this folder.
