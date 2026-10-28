# Review a custom concurrent primitive

Use when implementing or reviewing an owned unsafe synchronization or shared-memory
abstraction. Prefer supported safe primitives when their contract fits. This is a
review procedure, not an instruction to write a lock or reference counter.

## Inventory the capabilities and states

Record MSRV/target, safe public operations, owner/guard/reference types, trait bounds,
lifetimes, aliasing and permitted threads. Check Send and Sync separately for each
type, including derived/auto traits, Deref/DerefMut and guard transfer/drop behavior.
Do not infer guard bounds from the owner. Exclusive access can make an owner of a
Send-but-not-Sync payload shareable while a shared guard exposing that payload
still requires the relevant Sync bound. A guard over Cell must not accidentally
enable concurrent unsynchronized shared access; do not reject every Mutex<Cell>
owner merely to avoid reviewing the guard. The exact abstraction determines bounds.

List all operations affecting state: creation, clone, upgrade, downgrade, lock,
unlock, cancellation, drop and failure. Define valid bit patterns, counts, margins,
reserved values and sentinels. Check every increment/decrement and combined
transition against that global invariant; safe arithmetic in one CAS loop does
not prove that another operation cannot exhaust the remaining margin.

## Separate publication from lifetime and progress

Use [atomic publication](atomic-publication.md) for observed release/acquire edges
and success/failure orderings. Then track payload lifetime separately from backing
allocation lifetime: which strong/weak/read references remain, who destroys the
payload and who can finally release storage. Publication alone cannot establish
safe dereference, protect a reclaimed address from reuse or prevent ABA.

Review losing allocations, partially initialized state and unwind paths. A payload
destructor can panic; determine who still owns each allocation and which safe
operations remain possible. Safe callers can leak/forget a guard; memory safety
must not depend on a destructor always running, even when leaking harms progress
or resource availability. Do not catch a panic and resume using invalid state.

State the progress contract separately: blocking, deadlock conditions, fairness,
starvation and any lock-free claim. A bounded counter or data-race-free program
does not establish timely completion. A wakeup count or arbitrary sleep does not
prove that an operation actually blocked.

## Falsify the relevant invariant

Choose a small state model that reaches combined counter boundaries and sentinel
transitions without billions of allocations. Include allowed and rejected trait
uses, contested acquisition/release, panic during destruction, forgotten guards
and readers that outlive retirement. Use supported compiler checks, controlled
schedules, model checking or sanitizers where applicable; record their assumptions
and untested target behavior. Do not treat one stress run as a memory-model proof.

Return separate conclusions for type/capability safety, state invariants,
publication/reclamation, progress and cost, with the evidence for each. Follow
[concurrency and safety](concurrency-and-safety.md) for the shared unsafe obligations.

Basis: Bos, *Rust Atomics and Locks*, chapters 4, 6 and 9, reconciled with
*Effective Rust* and *Rust for Rustaceans*. The official
[Rustonomicon Send/Sync discussion](https://doc.rust-lang.org/nomicon/send-and-sync.html)
clarifies auto-trait and interior-mutability boundaries; confirm API details against
the destination toolchain. No source teaching primitive is copied here.
