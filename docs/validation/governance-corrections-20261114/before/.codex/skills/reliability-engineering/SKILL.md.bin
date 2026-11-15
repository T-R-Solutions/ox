---
name: reliability-engineering
description: Design or verify failure containment, bounded retries and resources, degradation, service objectives, and recovery. Use when behavior under dependency failure, overload, restart, or rollout needs a reliability decision; ordinary errors, background code, telemetry plumbing, or measured tuning alone do not trigger this workflow.
---

# Reliability engineering

Make essential behavior survive specified faults and recover predictably. Attach every mechanism to an observed or credible failure mode and a verifiable user outcome.

## Activation and boundaries

Use when slow or failing dependencies, resource exhaustion, restart/failover, background work or rollout raise a concrete containment, service-objective or recovery question. Telemetry plumbing alone belongs to instrumentation; quantitative tuning alone belongs to performance investigation. A small pure-function edit does not need a resilience program. Ordinary correctness, resource cleanup, security and accessibility remain required without this skill.

Start from existing requirements, contracts, incident evidence and acceptance criteria. Separate the required outcome from the proposed mechanism, implementation and validation. Do not invent a service-level objective or impose continuous deployment, microservices, a control plane, circuit breakers or chaos experiments.

Own propagation, containment and recovery. Consult `performance-engineering` only when measurements or capacity limits need deeper investigation; `distributed-systems` for consistency, ordering or delivery guarantees; `application-security` when threats or degraded authorization need specialized analysis; `api-testing` for protocol compatibility; `software-testing` for broader suite strategy. These are conditional handoffs, not prerequisites.

## Operational workflow

1. **Define success and acceptable loss.** Identify the user operation, required correctness, latency/availability target, allowed degradation, data loss/recovery bounds and affected population. Record uncertainties and criticality. Use a short note for a small change.
2. **Trace the failure path.** Collect relevant topology, runtime/client versions, configuration, deadlines, retries at every layer, queues, pools, state ownership and shared dependencies. Distinguish symptoms, measured facts and hypotheses. Examine recent changes and historical incidents without assuming a single root cause.
3. **Model consequences.** Consider unavailable, slow, intermittently failing and malformed responses; partial completion; duplication; cancellation; resource leakage; startup and recovery. Include how a local failure can overload peers or downstream services. Check existing mechanisms before adding another.
4. **Choose the smallest adequate intervention.** Bound waiting and retained work; classify retry safety; limit amplification; isolate competing resources; define truthful degradation. Read [failure controls](references/failure-controls.md) only for the relevant decision. Compare at least the existing behavior and a feasible alternative when costs or guarantees change.
5. **Implement the transition.** Preserve observable contracts or explicitly document the change. Specify default/configuration ownership, cleanup, cancellation, restart behavior and safe rollback or forward recovery. For persisted-state or mixed-version changes, use [deployment and recovery](references/deployment-and-recovery.md).
6. **Verify failure and recovery.** Define evidence and stop conditions before injecting faults. Start with a deterministic local or controlled test. Check the intended outcome, bounded resource use, dependency load, data correctness, degraded behavior and return to steady state. A timeout response alone does not prove cancellation or cleanup.
7. **Connect operation to evidence.** Expose enough safe metrics/logs/traces to detect the failure, diagnose its path and verify recovery. Prefer user outcomes plus relevant saturation/backlog signals; avoid logging secrets or uncontrolled cardinality. Define what observation calls for action and how that action is reversed.

For reliability signals, SLOs or recovery alert quality, read
[operational signals](references/operational-signals.md): population and error-budget
definitions, sampling limits, diagnostic context and detection/recovery validation.

## Essential decisions and constraints

- A waiting timeout does not prove that remote work failed or stopped. Reconcile ambiguous writes before retrying without a proven idempotency contract.
- Budget attempts, elapsed time and aggregate retry load. Include SDK, proxy, transport and job retries. Backoff alone does not bound total work.
- Queue bounds need admission, expiry and cancellation semantics. Adding threads, connections or replicas can move overload to another dependency.
- Degraded results must preserve essential invariants and disclose meaningful staleness or incompleteness. Never bypass authorization to appear available.
- Separate readiness, liveness and user-visible health. Removing every overloaded instance can amplify an outage.
- Experiments affecting shared, production or external systems need corresponding authorization, bounded exposure, an abort mechanism and a recovery plan. Silence is not authorization.

## Completion and reporting

Report the failure mode and evidence, changed behavior, relevant configuration/assumptions, alternatives and costs, checks actually run, results, recovery evidence and remaining gaps. Label simulations, illustrative examples and unexecuted checks. Do not promise availability from a pattern name or a passing test.

Source provenance and disagreements are maintained separately in research notes (historical library source: `system/research/operations-reading-progress.md`; not required at runtime) and official-source scope (historical library source: `system/research/operations-official-sources.md`; not required at runtime); do not load these during routine work unless attribution or a conflict needs investigation.

## Additional investigation references

For resource leaks, cancellation cleanup or compartment recovery, read
[resource lifecycle](references/resource-lifecycle.md).

For recovery after relevant compromise, security-version rollback or trust/key
rotation, read [trust-preserving recovery](references/trust-preserving-recovery.md).
This adds trust ordering and revocation checks to the existing recovery workflow.

Other named skills are optional specialist suggestions. Use them only when available and needed for a specific unresolved question; their absence does not prevent using this skill. Report any expertise or verification gap without claiming a handoff occurred.

## Adjacent responsibilities

Observability-and-diagnostics can own a substantive instrumentation/investigation question; software-delivery can own build/artifact release mechanics and software-evolution a long-lived coexistence plan. Keep failure containment, recovery policy and user outcome targets here.
These are optional available capabilities, not dependencies of this folder.
