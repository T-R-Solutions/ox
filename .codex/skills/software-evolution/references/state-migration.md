# Evolve state without losing authority

Read for schema/data evolution, dual writes, CDC or cutover.

1. Expand compatible structures and readers before new writers rely on them. Record
   old/new code × schema × data combinations and update order. A maintenance window
   can be simpler when permitted; additive DDL still needs engine-specific lock analysis.
2. Specify which representation/writer is authoritative in every phase. Backfill
   stable-key chunks with bounded resources, conditional writes/version checks and
   durable progress. Do not overwrite a concurrent update with a stale transformed
   value. Commit progress consistently with applied work and replay safely after crash.
3. Reconcile keys, transformed values, invariants and deletions independently. Counts
   can match while individual records differ. Define malformed-data handling without
   silently redefining requirements. Measure lag/load and stop on the project's limits.
4. Dual writes across independent stores can fail between commits in either direction.
   Choose local atomic intent/outbox, supported transaction, CDC or explicit repair
   protocol from the actual boundary. State duplicate/order/delete handling and who
   repairs divergence. “Write both” without reconciliation is incomplete.
5. For CDC, pair a consistent snapshot with a valid change-log position and retain
   sufficient history. A timestamp captured after the copy can omit changes. Test
   restart, replay, long transaction, delete and retention expiry; if a gap cannot be
   repaired from the authoritative log, resnapshot rather than advancing silently.
6. Cut over authority and traffic only after defined completeness/compatibility checks.
   Drain old writers and delayed work as required. Before return, check whether old
   code can read data written by new code; a new enum may make downgrade impossible.
   Translate only with a proven mapping; otherwise stop exposure and roll forward or
   restore with the accepted loss and external reconciliation explicitly recorded.
7. Contract after consumer/recovery windows close, with removal evidence, owner and
   verification. Retire temporary dual paths, old credentials, schedules and metrics;
   the transition is not complete while an unowned fallback is still necessary.

[PRISM](https://www.cs.ucla.edu/~zaniolo/papers/prism-vldb2008-cameraready.pdf)
illustrates query/schema mapping and limits of invertibility; its Wikipedia/MySQL
prototype is not an automatic PostgreSQL migration guarantee.
[F1](https://research.google/pubs/online-asynchronous-schema-change-in-f1/)
illustrates why intermediate schema versions matter under specific server/version
assumptions. Its protocol and online guarantees must not be transplanted to PostgreSQL.
The operational steps here are synthesis requiring the actual engine/connector contract.

Acceptance: stop/restart mid-chunk while a live writer changes the same key, replay a
change/delete, test old/new readers on old/new data, then attempt the planned return.
Report actual integration separately from paper/model reasoning and from production.
