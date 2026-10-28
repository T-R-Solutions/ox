# Model and transaction decisions

Read for relational modeling or integrity under concurrency. These are portable
engineering decisions; verify enforcement, syntax and isolation in the actual engine.

## Represent the invariant

Record entity identity and candidate keys before choosing a surrogate; keep business
uniqueness explicit. Normalize dependencies that must remain consistent; denormalize
only for a measured access need with an owner and repair path. Choose integer range,
exact decimal scale/rounding or approximate arithmetic from the domain. Test overflow
and driver conversion. NULL, empty, unknown and absent are distinct policy decisions;
verify three-valued predicates and whether CHECK accepts unknown. Use NOT NULL when
absence is prohibited. Define foreign-key update/delete behavior and import order;
application authorization remains separate from referential integrity.

Distinguish an instant, local calendar value, duration and recurring zoned schedule.
Store required zone identity separately when an instant type does not retain it.
Round-trip through the actual driver across DST and precision boundaries. Database
default time, application time and commit order need not agree.

Map each rule to enforcement and a negative check. Row checks cannot generally enforce
arbitrary cross-row sums or external policy; a trigger also needs concurrency analysis.
Validation near the user improves feedback but does not cover bypassing writers.

## Protect the decision and retry boundary

Two sessions can read “two active doctors” and each deactivate a different row.
Snapshot consistency does not by itself preserve “at least one remains.” Compare a
constraint if expressible, locking a common guard observed by every writer, and a
serializable transaction with whole-transaction retry. Locking only returned rows
may not protect absent rows or ranges. Acquiring a guard does not itself refresh an
old snapshot: the protocol must force a fresh decision or a conflict/abort under the
actual isolation level, and must cover every writer. Keep lock order consistent and transactions
short; test deadlocks, phantom insertion and bypass writers, not just lost updates.

Classify errors by engine codes and operation semantics. Retry fresh reads, decisions
and writes together, after rollback; bound attempts and elapsed time and avoid retry
multiplication across layers. A permanent constraint violation is not automatically
transient. On response loss after commit, query a durable operation identity/outcome
or reconcile; do not assume failure from a timeout.

An external payment inside a retried callback can execute twice even if SQL rolls
back. Couple committed intent and local state atomically where possible, then deliver
with stable identity and duplicate-safe receiver. An outbox alone does not make an
arbitrary external effect exactly once. Retain outcome/deduplication for the real
replay horizon and handle inconsistent ID reuse. Test failure after effect and before
acknowledgment as well as success. Compensation, undo and restore have different
observable histories and may lose data; record that cost before relying on them.

Basis: [PostgreSQL constraints](https://www.postgresql.org/docs/18/ddl-constraints.html),
[numeric types](https://www.postgresql.org/docs/18/datatype-numeric.html),
[date/time](https://www.postgresql.org/docs/18/datatype-datetime.html) and
[transaction isolation](https://www.postgresql.org/docs/18/transaction-iso.html).
These concretize relational pitfalls, not a claim that all engines implement PG semantics.
The external-effects protocol above is engineering synthesis and must be verified
against the actual receiver/transport contract.
