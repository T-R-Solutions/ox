# Integration and evolution

Read only for cross-context contracts, historical models, or changes to established domain boundaries. Source locators use one-based physical pages in Learning Domain-Driven Design (`docs/system/Domain-Driven_Design.pdf`), first edition. Recommendations are contextual synthesis unless explicitly identified as documented platform behavior.

## Keep model boundaries and deployment boundaries separate

**Action/context:** Where the same term has different meanings, define a context-specific model and explicit translations. Begin with logical boundaries when the domain is uncertain; introduce separate deployment only for demonstrated autonomy, operational, or organizational needs.

**Evidence/rationale:** Chapters 3-4 pp79-135, chapter 10 pp288-305, chapter 14 pp396-424. Small service interfaces can still create excessive global coordination; size alone is a poor decomposition criterion.

**Exceptions/costs:** A shared kernel can be justified when co-evolution costs less than duplicating the same volatile rule. Keep its scope and ownership explicit. Translation layers add code and operational cost; use a conforming model when its semantics fit safely.

**Validation:** Walk a likely rule change through every consumer and writer. Check contract compatibility, ownership, translation loss, and independent change feasibility. A module diagram does not demonstrate independent deployment.

## Publish committed facts reliably

**Action/context:** When a transaction changes business state and must notify an independent consumer, identify the dual-write failure window. Where appropriate, persist state and an outgoing message atomically, then relay the message with retries and deduplication at the consumer.

**Evidence/rationale:** Chapter 9 pp268-287 and chapter 15 pp425-452 describe outbox delivery, compensation, and private/public event separation. Publishing before commit may advertise rolled-back facts; publishing after commit without durable intent can lose the notification.

**Exceptions/costs:** An outbox is unnecessary for purely local work without durable messaging requirements. It adds lag, retention, relay monitoring, ordering, and duplicate-handling responsibilities. Its eventual progress depends on recovery and retention assumptions; it does not magically guarantee exactly-once external effects.

**Validation:** Exercise crash before commit, after commit/before publish, and after publish/before acknowledgment. Re-deliver the same message and attempt concurrent consumption. Confirm one intended business effect, explicit retry limits, and recoverable stalled work.

## Model workflow recovery as business behavior

**Action/context:** For a process spanning independent transactions, define durable workflow state, step outcomes, correlation, retry policy, compensation, and manual recovery. Treat a compensation as a new business action with its own possible failure.

**Evidence/rationale:** Chapter 9 pp274-287 distinguishes sagas and process managers; chapter 15 pp443-447 demonstrates why arbitrary delays cannot establish dependency ordering.

**Exceptions/costs:** Prefer a local transaction when it satisfies the requirement. Saga terminology differs across sources; define the concrete mechanism. Compensation may not undo externally visible effects or restore isolation, and some actions are irreversible.

**Validation:** Check duplicate, delayed, out-of-order, missing, and conflicting responses; simulate failure during compensation and recovery after restart. Verify business-visible intermediate states are acceptable.

## Adopt historical state only for a concrete need

**Action/context:** Compare an event-sourced model with an ordinary state model plus a reliable audit/history mechanism when replay, audit, or alternate projections matter. Specify event schema/versioning, source of truth, projection lag, rebuild, retention, deletion, and recovery.

**Evidence/rationale:** Chapter 7 pp190-218 and chapter 11 pp321-324. Event sourcing preserves transitions but introduces migration and operational work. The book's fixed event-count performance thresholds are not adopted; measurement depends on workload and implementation.

**Exceptions/costs:** Logging alone is not an atomic audit guarantee, but a carefully designed transactional history can be appropriate. Key destruction is a possible technical privacy mechanism, not proof of legal erasure or compliance; copies, backups, indexes, metadata, and key lifecycle require separate review.

**Validation:** Rebuild from known events and compare state; test duplicate/out-of-order projection input, old schemas, snapshot invalidation, and deleted/redacted information. Use explicit import events for unknown legacy history rather than inventing past facts.

## Avoid unsafe checkpoint assumptions

**Action/context:** If a projection polls changing records, require a checkpoint that cannot skip a transaction that commits later. Consider deletion tracking, snapshots, retention, and restart semantics as part of the design.

**Evidence/rationale:** Chapter 8 pp246-250 requires consistent checkpoint progression. Microsoft documents that `@@DBTS` can miss changes still active at synchronization time and explains `MIN_ACTIVE_ROWVERSION` ([SQL Server 17 documentation](https://learn.microsoft.com/en-us/sql/t-sql/functions/min-active-rowversion-transact-sql?view=sql-server-ver17), consulted 2026-10-17). This supports a platform-specific warning, not a universal polling algorithm.

**Exceptions/costs:** A high-water mark that only increases is not necessarily commit-ordered. Change tracking/CDC or another database feature may fit better; verify the actual engine/version and retention configuration. Polling and log-based capture each have operational costs.

**Validation:** Hold an earlier write uncommitted while a later write commits and the consumer advances; then commit the earlier write. Verify it is not skipped. Repeat with delete, rollback, restart, and retention expiry. No SQL Server example was executed in this research environment.

## Modernize incrementally

**Action/context:** Choose an affected behavior slice, protect it with observable checks, gather its rules, then refactor or route it to a replacement. Record temporary coupling and its removal condition.

**Evidence/rationale:** Chapter 13 pp368-395 permits incremental DDD adoption and a temporary shared database during a strangler migration. Appendix A pp497-525 illustrates the cost of duplicated rules across organizational boundaries.

**Exceptions/costs:** A rewrite may be justified by concrete constraints; compare migration risk and verification costs. Moving types can break reflection, serialization names, database objects, and externally referenced contracts even when method bodies are unchanged.

**Validation:** Compare old/new behavior on representative inputs, verify data migration and rollback, and check all actual entry points. Record intentional contract differences separately from refactoring.
