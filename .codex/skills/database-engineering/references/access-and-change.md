# Access paths and recoverable change

Read for query tuning, ORM behavior or migrations. Begin with actual statements,
parameters, row counts/skew, concurrent load, connection waits and caller contract.

## Match work to access

Choose indexes from filters, joins, ordering and projected values. Compare selectivity,
correlated columns, NULLs, hot values and read/write mix; account for write amplification,
space, maintenance and build cost. A sequential scan may be appropriate. Compare
estimated rows with actual rows and statistics before forcing a plan; use sanitized
representative data/cache states and account for observer overhead.

Measure queries per operation to expose N+1 and lazy loads. Compare joins, batch fetches
and bounded streaming, checking duplicate rows, Cartesian expansion and memory.
Inspect transaction/autocommit, flush order, cancellation, prepared statements and pool
release through the actual ORM/driver. Pool capacity must include replicas, workers
and administrative access; more connections can worsen contention. Bound queue time,
query duration and lifetime without inventing universal limits.

Pagination needs a unique total order. Offset can be sufficient for small stable data;
for deep traversal compare a cursor/keyset tied to the full ordering, NULL policy and
filters. Concurrent changes can cause omissions/duplicates: specify snapshot or
continuation semantics rather than promising a stable export from unrelated pages.

## Make movement resumable

Separate schema expansion, compatible readers/writers, data movement and contraction.
Define one authority for each field during the transition. Backfill stable-key chunks
with bounded transactions, conditional/versioned updates and durable checkpoints.
Commit data and progress consistently; a maximum ID alone is not proof all earlier
writes committed. On interruption, replay safely without overwriting newer values.
Include deletes, malformed historical data and empty batches in reconciliation.

Validate keys and transformed values against an independent invariant/oracle, not
only equal counts. For CDC, establish a consistent snapshot/log handoff, duplicates,
ordering and retention; resnapshot or repair a gap instead of silently advancing.
Uncoordinated dual writes can diverge on either failure window. A single-store change
need not introduce CDC or a broker.

Before removal, prove consumers and rollback windows no longer need the old shape.
Rehearse restore separately from code rollback, state tolerated loss and external
reconciliation. Backups that exist but have never restored leave recovery unverified.

Basis: [query pagination](https://www.postgresql.org/docs/18/queries-limit.html),
[index access](https://www.postgresql.org/docs/18/indexes.html),
[plans](https://www.postgresql.org/docs/18/using-explain.html),
[PITR](https://www.postgresql.org/docs/18/continuous-archiving.html).
Version-neutral migration/driver decisions are synthesis; discover the concrete
product contract before implementation. No ORM-specific API is prescribed.
