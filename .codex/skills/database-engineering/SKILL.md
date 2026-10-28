---
name: database-engineering
description: Design and change application persistence, relational schemas, transactional invariants, query access paths, and data migrations. Use for substantive database decisions across engines; skip analytical platforms, routine field mapping, and edits without persistence consequences.
---

# Database Engineering

Own application persistence decisions independently of a specific database product.
Discover the engine/version, topology, schema, actual SQL, drivers/ORM, all writers,
data distribution, workload, invariants, compatibility and recovery requirements.
Distinguish confirmed policy from assumptions. Do not prescribe a new database.

## Procedure

1. State the operation and invariant, authoritative data, rejected states and effects.
   Separate business meaning from its persistence mechanism. Identify direct SQL,
   imports and jobs that bypass application validation.
2. Choose keys, types and relations from identity, precision, absence and time semantics.
   Read [model and transactions](references/model-and-transactions.md) when designing
   storage or protecting a concurrent invariant. Prefer an enforceable constraint or
   atomic operation; pre-write checks alone do not serialize concurrent writers.
3. When transaction or concurrent-integrity behavior is relevant, trace reads,
   locks, commit and external effects. For a concurrent invariant, construct
   a violating schedule. Compare constraints, conditional writes, a shared guard,
   appropriate isolation and a deliberate redesign; state contention and failure costs.
   Reexecute the entire safe transaction on retryable failures with fresh reads and
   bounded attempts/deadline. Resolve uncertain commit before duplicating effects.
4. For query or capacity work, read [access and change](references/access-and-change.md).
   Inspect emitted SQL and round trips; compare plans and representative measurements
   before adding indexes or changing ORM fetch strategy.
5. For schema/data evolution, define intermediate version pairs, writer authority,
   bounded resumable backfill and independent reconciliation. Choose maintenance
   window or compatible expansion based on actual requirements. A code rollback
   cannot restore deleted or newly uninterpretable data.
6. Implement and validate normal and invalid paths, plus concurrent or interrupted
   paths where relevant, against the real engine when available. Record versions,
   configuration, commands, initial
   state, result and cleanup; a schedule model is useful but is not integration evidence.

## Boundaries and output

Deliver the schema/query/migration change, rationale, invariant-to-mechanism mapping,
observed checks, recovery path and unverified assumptions. Keep a small change small.
PostgreSQL specifics, release orchestration, domain semantics and distributed
coordination may warrant available specialists only for unresolved questions.
No other skill or SDD is required. This does not authorize production mutation or
create an analytics/data-lake/training pipeline mandate. Local tests establish only
the tested engine, schedules and data, not universal integrity or performance.
