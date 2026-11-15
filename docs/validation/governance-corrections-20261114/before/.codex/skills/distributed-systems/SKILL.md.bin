---
name: distributed-systems
description: Analyze and implement guarantees across independently failing processes, stores, replicas, or regions. Use for consistency, concurrent updates, replication, partitioning, ordering, messaging, distributed transactions, and recovery; skip local changes with no distributed guarantee question and do not introduce distribution by default.
---

# Distributed Systems

Make assumptions, failure windows, and externally visible guarantees explicit before choosing a mechanism.

## Scope and evidence

Collect the required invariants, accepted intermediate states, topology, writers/readers, deployed versions and configuration, durability/acknowledgment semantics, workload/skew, retention, timeout budgets, and recovery ownership. Identify authoritative state and derived copies. Unknown guarantees remain unknown until verified.

This skill owns cross-node consistency and coordination. Domain modeling establishes what must remain true; architecture decides whether the boundaries should exist; reliability engineering handles broader failure containment and recovery; performance engineering validates measured costs. Consult another skill only when a concrete unanswered question needs it. Baseline security and correctness always apply.

## Workflow

1. **Check whether distribution is needed.** Compare a local operation or transaction with the distributed proposal. Preserve simpler boundaries when they meet the requirement.
2. **Specify the contract.** State safety properties (what must never happen), progress expectations, and the fault assumptions under which they hold. Separate durability, atomicity, isolation, linearizability, causal order, and eventual convergence.
3. **Trace the operation.** Draw or enumerate state changes, messages, acknowledgments, durable writes, visibility points, and retry boundaries. Distinguish accepted, persisted, replicated, applied, and business-complete.
4. **Explore failure schedules.** Consider request loss, response loss after commit, delay, duplication, reordering, crash/restart, concurrent writers, network partitions, expired leases, and lag. A timeout does not prove an operation failed.
5. **Choose a mechanism that covers the invariant.** Prefer maintained platform primitives with verified configuration. Match transaction scope, isolation, conditional writes, durable messaging, deduplication, fencing, or reconciliation to specific failure windows. Read [guarantees and failures](references/guarantees-and-failures.md) for the relevant case.
6. **Bound resources and recovery.** Define deadlines, retry ownership, backoff/jitter where appropriate, capacity/backpressure, retention, replay, poison-message handling, and operator escalation. Do not amplify overload with nested or unbounded retries.
7. **Plan evolution.** Define mixed-version contracts, state migration, old message handling, rollout/rollback limits, and recovery after retention expires. Data deletion and authorization changes must reach relevant copies.
8. **Verify independently.** Use appropriate concurrency histories, deterministic schedules, crash-window checks, integration tests, or bounded fault injection in an authorized environment. Check invariants and recovery outcomes, not just successful responses. Record the tested configuration and untested assumptions.

## Essential constraints

For CDC, projection rebuilds or replay after downtime, read the snapshot/change-log
handoff in [guarantees and failures](references/guarantees-and-failures.md). Verify
snapshot position and deletion retention before treating the new view as complete.

- Exactly-once claims must name their boundary and assumptions. Broker deduplication or transactional offsets do not automatically cover email, payments, other databases, or duplicate source events.
- Compensation is a new action that may fail; it does not restore atomic visibility or isolation. Distributed ACID transactions are possible, with availability, latency, and recovery costs.
- Quorum overlap alone does not establish linearizability. Replication is not a backup. A leader label does not prove exclusive authority.
- Clocks and leases require explicit uncertainty assumptions. Fencing must be enforced by every protected resource; generating a token alone is insufficient.
- Append order, causal order, real-time order, and business order differ. Partitioning an ordered stream narrows its ordering scope.
- Do not implement a consensus protocol from a book sketch. Verify the selected system's read modes, membership/reconfiguration, persistence, and failover behavior.
- Do not conduct production fault injection or intrusive external testing without corresponding authorization.

## Completion and report

Present the business-visible guarantee, assumptions, selected mechanism, important failure windows, trade-offs, implementation, and validation actually performed. Include residual failure modes, recovery ownership, and evidence needed to close uncertainty. Do not claim universal correctness from a finite simulation or one successful integration run.

Other named skills are optional specialist suggestions. Use them only when available and needed for a specific unresolved question; their absence does not prevent using this skill. Report any expertise or verification gap without claiming a handoff occurred.

## Adjacent responsibilities

Database-engineering can resolve a local persistence mechanism; software-evolution can orchestrate version coexistence. Keep cross-node guarantees here and avoid a second specialist for a question already answered.
These are optional available capabilities, not dependencies of this folder.
