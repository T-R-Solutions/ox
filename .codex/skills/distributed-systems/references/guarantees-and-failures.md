# Guarantees and failures

Read only sections relevant to the operation. Locators are inclusive, one-based **physical PDF pages**, including front matter: **I** = `docs/system/Designing_Data_Intensive_Applications_2nd_Edition.pdf` (second edition, 2026); **H** = `docs/system/Software_Architecture_Hard_Parts.pdf` (first edition, 2021 release); **D** = `docs/system/Domain-Driven_Design.pdf` (first edition, 2021 release). Recommendations are contextual synthesis unless explicitly marked as documented platform behavior.

## Snapshot and change-log handoff

For a new or rebuilt projection, establish a consistent snapshot and its corresponding
log position before applying later changes. Verify the actual connector/database
contract; an arbitrary timestamp or offset captured after a copy can omit writes.
Use an equivalent supported reconciliation protocol if no atomic snapshot/position
mechanism exists. Define checkpoint persistence, duplicate handling and cutover.

Compaction keeps current per-key state, not all historical facts. Define deletion
tombstone retention and the maximum offline/replay horizon together; otherwise a
stale consumer can resurrect deleted records. If the required log history expired,
rebuild from an authoritative snapshot rather than silently skipping the gap.

Validation: insert, update and delete while snapshotting; stop between snapshot and
replay; duplicate changes; resume an old consumer beyond retention. Reconcile keys,
values and deletions independently before making the rebuilt view authoritative.
Counts alone cannot show correctness. Additional storage and retained history cost
capacity; a local stable dataset with no concurrent writers needs no CDC machinery.
Basis: DDIA 2nd ed., ch. 12 “Initial snapshot” / “Log compaction”, physical PDF 529;
handoff and retention checks are engineering synthesis, not connector API guarantees.

## Specify the guarantee before the mechanism

**Action/context:** For an operation touching concurrent or independent state, write the invariant, success/unknown/failure outcomes, visibility expectations, and fault model. Distinguish atomic commit, isolation/serializability, real-time ordering/linearizability, durability, and eventual convergence.

**Evidence/rationale:** I chapters 8-10 pp301-474. A transaction label, consensus algorithm, or majority response does not specify all these properties. Safety and liveness can require different assumptions.

**Exceptions/costs:** A short statement suffices for a small change; formal models are useful when consequential protocol states remain difficult to reason about. Stronger coordination can cost latency and availability, while weaker guarantees transfer complexity to the business and recovery paths.

**Validation:** Construct a schedule that would violate each invariant. Check the exact database, isolation/read mode, durability configuration, and API semantics against official documentation. Validate uncertainty and failures, not just the happy path.

Example: “A reservation is never sold twice” differs from “all replicas eventually display the same reservations.” A convergent merge that retains both sales satisfies the latter while violating the former.

## Treat uncertain completion as a first-class state

**Action/context:** If a caller may retry after losing a response, assign a stable operation identity and durably couple duplicate detection, the intended mutation, and the retained outcome when feasible. Bind identity to the authenticated scope and request semantics; reject inconsistent reuse.

**Evidence/rationale:** I chapter 8 pp301-368, chapter 9 pp369-424, chapter 13 pp587-596. The server may have committed before a timeout. A content hash alone can collapse two legitimate identical operations; a new ID for every retry cannot suppress duplicates.

**Exceptions/costs:** Naturally idempotent replacement operations may not need a deduplication table, but still need concurrency protection and authorization. Retained results consume storage and may contain sensitive data. Define a retention horizon covering retries, late attempts, broker redelivery, and allowed replay; deleting an ID after one acknowledgment can re-enable old effects.

**Validation:** Repeat the same request concurrently, lose the response after commit, restart the worker, and reuse the ID with a different payload or tenant. Verify one intended effect and a stable observable result. Test behavior after expiry explicitly; do not claim an unlimited guarantee from finite retention.

## Make state-to-message transitions recoverable

**Action/context:** When committed state must trigger independent work, identify the dual-write gap. Use an appropriate atomic outbox, transactional change capture, or supported cross-resource transaction; make relay and consumer recovery explicit.

**Evidence/rationale:** D chapter 9 pp268-286; I chapter 12 pp511-562. Persisting state and outgoing intent atomically prevents missing intent after commit, but a relay can still publish duplicates. Consumer state, outgoing effects, and progress need their own atomic or idempotent coverage.

**Exceptions/costs:** Local work without durable notification needs no broker/outbox. These mechanisms add lag, capacity, retention, connector schema contracts, and monitoring. A dead-letter queue can unblock work while violating per-key order; retain original evidence and define approved repair semantics.

**Validation:** Crash before commit, after commit/before publication, after publication/before acknowledgment, and after consuming/before checkpoint. Test concurrent delivery, out-of-order events, replay, poison messages, and retention expiry. Observe oldest pending work, lag, retry exhaustion, and reconciliation failures.

Illustrative before/after: `save(order); publish(event)` can lose the event after a crash. Persisting order and outgoing intent in one local transaction closes that gap, but delivery remains subject to relay recovery and duplicate-safe consumers. This is an algorithm sketch, not runnable code or an exactly-once external-effects claim.

## Protect concurrent invariants with the actual isolation boundary

**Action/context:** For a check-then-write invariant, cover all relevant records and writers using a suitable database constraint, atomic conditional operation, locking/isolation, or coordination protocol. On a serialization conflict, retry the whole transaction when safe, with bounded attempts and fresh reads.

**Evidence/rationale:** I chapter 8 pp301-368 distinguishes lost updates, read/write skew, phantoms, two-phase locking, optimistic validation, and distributed commit. Snapshot isolation alone may permit write skew; locking only rows returned by a query may not protect an absent row or range.

**Exceptions/costs:** A single atomic operation can be enough for a single-object invariant. Wider transactions increase contention and failure coupling. A business-approved reservation/escrow design can reduce coordination, but cannot silently relax a hard invariant.

**Validation:** Run competing operations that individually pass their checks, include phantom insertion, and fail between writes. Check all access paths and unknown commit results. Tests require the real engine/configuration or an explicitly limited model; a mock transaction cannot establish isolation.

**Documented counterexample:** [PostgreSQL 18 two-phase transactions](https://www.postgresql.org/docs/18/two-phase.html) supports coordination through external transaction management and documents prepared-state recovery (consulted 2026-10-17). Therefore H chapter 9 pp267-300 must not be read as proving distributed ACID impossible. Two-phase commit alone does not supply every isolation or fault-tolerance property.

## Separate saga recovery from transaction rollback

**Action/context:** If a workflow deliberately spans independent commits, define its durable state machine, allowed intermediate observations, per-step identity, retry/cancellation rules, compensations, and terminal escalation. Compare a local transaction first.

**Evidence/rationale:** H chapters 11-12 pp317-382; D chapter 9 pp274-286; I chapter 13 pp587-598. Recovery steps can restore a business condition eventually; already observed effects remain observable.

**Exceptions/costs:** Irreversible actions may require reservation/confirmation, manual review, or a different boundary. A refund is not equivalent to an unobserved charge. Compensation itself can fail or race with another operation. The streaming transfer in I pp593-594 is not a production banking protocol and does not demonstrate atomic visibility or isolation.

**Validation:** Exercise failure at every transition, duplicate/late responses, concurrent changes, process restart, compensation failure, and abandoned work. Verify that the business accepts intermediate states and that an operator can safely resume or resolve the process.

## Read replication guarantees at the right boundary

**Action/context:** State whether acknowledgment means local receipt, durable write, replicated persistence, application, or final business completion. Select read modes and routing consistent with freshness needs; assess leader failure, lag, conflict resolution, and backup separately.

**Evidence/rationale:** I chapter 6 pp221-274 and chapter 10 pp425-474. Read-your-writes, monotonic reads, causal visibility, and linearizability solve different problems. Overlapping quorums alone do not prove linearizability; last-write-wins can discard valid updates.

**Exceptions/costs:** Stale views can be acceptable for noncritical presentation when their meaning is explicit. Safety, authorization revocation, and inventory decisions may require stronger handling. Synchronous replication costs latency/availability; asynchronous replication permits lag and possibly acknowledged-write loss under the configured failure model.

**Validation:** Fail a leader after acknowledgment, delay one replica, move a session between replicas, and create conflicting updates. Verify the configured recovery point, fencing, routing, and reconciliation. Restore a backup: replicated corruption or deletion is not recoverable merely because copies exist.

## Account for time, authority, and ordering

**Action/context:** Use monotonic elapsed-time measurements where supported; treat wall-clock values as uncertain observations. For lease-based authority, require durable increasing epochs/fencing enforced atomically by the protected resource. Identify the scope of ordering and causal metadata propagation.

**Evidence/rationale:** I chapters 9-10 pp369-474. A paused former owner can resume after its lease expires; delayed writes can arrive after newer authority. An ID can be unique without reflecting commit order, causality, or real time.

**Exceptions/costs:** Some systems have documented bounded-clock assumptions; verify them rather than importing generic bounds. Fencing may require storage/API changes and cannot protect an external resource that ignores it. Logs give order only within their configured scope and do not automatically order business events produced concurrently elsewhere.

**Validation:** Pause an owner beyond expiry, elect a successor, then deliver the old write. Test stale fencing metadata after restart and every side-effect path. Check clock jumps, delayed messages, cross-partition dependencies, and ordering after rebalancing. Do not build consensus from informal pseudocode.

## Partition and process data without hiding recovery costs

**Action/context:** Choose partition keys from actual query patterns, skew, locality, and isolation needs. Plan hot keys, secondary indexes, routing changes, rebalancing, and cross-partition invariants. For derived data, define authoritative inputs, snapshots/log positions, checkpointing, lateness, and publication.

**Evidence/rationale:** I chapter 7 pp275-300 and chapters 11-13 pp475-608. Even key distribution does not imply even load. Reproducible batch/stream processing requires stable inputs and compatible transformations; event-time completeness is an assumption, not guaranteed by a watermark alone.

**Exceptions/costs:** Vertical scaling, an index, batching, or bounded concurrency may avoid sharding. Salting hot keys distributes writes but increases read/merge work. Global indexes trade query convenience for coordinated maintenance or staleness. Data mesh and streaming platforms add ownership and operational costs; they are not prerequisites for analytics.

**Validation:** Use skewed workloads, interrupted movement, stale routing, late/duplicate events, checkpoint restart, and replay beyond retention. Verify manifest completeness and atomic reader cutover. Independently reconcile business invariants; replaying the same defective transformation is not an independent oracle. Measure improvements with performance-engineering methods rather than extrapolating microbenchmarks.
