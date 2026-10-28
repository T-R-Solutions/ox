# Review atomic publication and lock ownership

Use when a changed Rust algorithm publishes data between threads. Source: Mara Bos, Rust Atomics and Locks, EPUB OEBPS/ch03.html, “Happens-Before Relationship”, “Release and Acquire Ordering”, “Common Misconceptions” (B08 in [reading record](portable-sources.md)).

1. Identify shared data, writer/reader, ownership, lifetime and atomic variable that publishes readiness. Draw the required happens-before edge; atomics on a flag do not make arbitrary shared access safe.
2. Name the actual write observed by the acquiring read. A release store and an acquire load synchronize when the load observes the corresponding write/release sequence, not merely because both orderings appear in code.
3. For compare_exchange, examine success and failure orderings separately: the failure path may consume a pointer published by another thread. Identify losing allocations and reclaim them without freeing the winning allocation.
4. Prefer existing safe synchronization. SeqCst cannot repair a logically incorrect algorithm; Relaxed may suit an independent counter but does not publish unrelated data. Stronger ordering is not a wall-clock visibility deadline.
5. Check panic/cancellation and lock release, lock ordering, progress and starvation independently from data-race safety. Preserve target/MSRV constraints before selecting model checking or sanitizers.
6. Validate functional invariants with controlled schedules and supported tools; stress passing on one CPU is not a memory-model proof. Record which interleavings and targets were not tested.

The book's unsafe/static-mut teaching code was not copied or executed. Current compiler/API compatibility is not inferred from its 2022/2023 examples.
