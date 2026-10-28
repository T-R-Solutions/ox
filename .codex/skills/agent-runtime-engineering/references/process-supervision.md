# Supervision and resource ownership

Assign an owner to process handles, output drainers, temporary files and permissions. Maintain a cleanup ledger so a failure can identify resources still owned. [Rust Child documentation](https://doc.rust-lang.org/std/process/struct.Child.html) states that dropping a Child does not stop it; waiting is also relevant to resource reclamation. Verify corresponding semantics for the selected async runtime instead of assuming equivalence.

Prevent pipe deadlocks by consuming both streams while the child runs. Bound memory without silently discarding evidence: spill raw output under a retention policy or fail visibly when storage is exhausted. Cancellation must remain deliverable while output queues are full.

Test with a controlled emitter that writes both streams, then ignores cooperative cancellation. Record deadlines, escalation, exit, drainer completion and descendants still alive. Killing the parent alone is not a portable guarantee about descendants. Termination strategy requires OS-specific validation; do not claim it from a pure state-machine test.
