# Concurrency and safety

## Choose the execution and ownership model

Use concurrency for a demonstrated responsiveness, throughput, or coordination requirement. Distinguish concurrent progress from parallel execution. Preserve the existing runtime; an async function does not itself spawn a task or a thread. Prefer ordinary functions when asynchronous execution adds no benefit.

Move owned data through channels when transferring responsibility fits the design. Use shared state when coordinated access to a common object is required. Neither channels nor locks universally win. Define queue bounds or another resource limit when producers can outpace consumers, and decide what shutdown, disconnection, timeout, and overload mean to callers.

| Mechanism | Appropriate use | Review concern |
| --- | --- | --- |
| `Rc<T>` | Shared ownership within one thread | Not `Send` or `Sync`; strong cycles can leak. |
| `Arc<T>` | Shared ownership across threads where `T` satisfies the required traits | Atomic ownership management does not make the payload thread-safe. |
| `Cell<T>` / `RefCell<T>` | Interior mutation within their supported single-thread sharing model | `Cell` uses replacement/copy operations; `RefCell` checks borrows at runtime. Both are `!Sync`, but can be moved between threads when `T: Send`. Use fallible borrow methods when conflicts are expected. |
| `Mutex<T>` | Protect an invariant over shared mutable state | Guard lifetime, lock ordering, poisoning policy, and work performed while locked. |
| `RwLock<T>` | Concurrent readers where workload evidence supports it | More complexity does not guarantee higher throughput or fairness. |
| Atomics | A small, specified synchronization protocol | Document memory-ordering and visibility reasoning; isolated atomic fields do not make a multi-field invariant atomic. |

Let `Send` and `Sync` derive from correctly composed types whenever possible. `Send` concerns transfer between threads; `Sync` means shared references can cross threads. Adding an unsafe implementation to bypass an error requires an actual soundness argument, not confidence that a test happens to pass.

Do not use poisoning as the safety boundary of an unsafe abstraction: it is advisory and may be bypassed by safe recovery. Keep critical sections short enough to avoid unnecessary contention, but long enough to preserve the complete invariant. Use a consistent lock order. Avoid calling unknown user callbacks while holding a lock. Explicitly release guards before expensive unrelated work. If a lock is poisoned, decide whether the invariant can be restored, the error must propagate, or the operation should terminate; do not automatically discard poison information.

Track worker handles and outcomes. Shutdown must stop new work, signal completion/cancellation, and join or otherwise account for outstanding work according to the contract. A channel receiver can wait indefinitely if an unintended sender clone remains alive. Safe Rust does not prevent deadlocks or business-level races. A poisoned standard mutex is not permanently inaccessible; recovery is a deliberate invariant-restoration decision.

For atomics, write the state machine and the required visibility relation before choosing an ordering. `Relaxed` can serve independent counters but cannot by itself publish associated non-atomic data. Acquire/release synchronization depends on the actual operation and observed value; `SeqCst` is not a proof that a multi-step algorithm is correct. Account for retry loops, spurious weak-CAS failures, ABA where relevant, and reclamation. If the protocol cannot be justified, use a lock or an existing proven abstraction. Volatile access is not thread synchronization.

Sources: ER Item 17; RFR ch. 10; SP pointer and locking discussions with [corrections](source-conflicts.md); TRPL ch. [16](https://doc.rust-lang.org/stable/book/ch16-00-concurrency.html), [shutdown](https://doc.rust-lang.org/stable/book/ch21-03-graceful-shutdown-and-cleanup.html), and the official [Arc contract](https://doc.rust-lang.org/stable/std/sync/struct.Arc.html).

## Async, cancellation, and pinning

An async function produces a future whose body progresses when polled. `await` yields to the executor only when progress returns `Pending`; a sequence of immediately ready awaits can monopolize a worker. Sequential awaits usually express sequential work; use the runtime's existing coordination facilities when operations should overlap. Values held across an await become part of suspended state and can affect `Send` requirements and memory use.

Do not block executor threads with blocking I/O or long CPU work. Use the established blocking facility or compute pool where needed and bound concurrency according to the workload. For asynchronous work, release a synchronous lock guard before an await; restructure the operation or select an appropriate async-aware primitive when the contract really requires it. An async mutex still needs lock-order and cancellation reasoning.

For cancellation or timeout, identify which state transitions and external side effects may already have happened. Dropping a future does not roll back a database commit or an external request; dropping a task handle may have different semantics from cancelling the task. Check the actual runtime API. Preserve errors from both task completion and the operation performed inside the task. A timeout does not preempt arbitrary non-yielding code; a `Future` may remain pending indefinitely. Define unfinished-work behavior for join versus race/select operations.

Use safe pinning facilities supported by the MSRV when pinning is required by an API. `Pin` constrains movement of a pointee that needs it; it is not a substitute for ownership or lifetime reasoning, and moving a pointer is different from moving its pointee. Avoid handwritten executors, unsafe projections, or self-referential types unless the task requires them and their contracts have been reviewed. If implementing `Future`, a `Pending` result must arrange a wakeup when progress becomes possible, without a lost-wakeup race; respect the waker contract and completion state. A stream produces multiple items through polling; a method such as `next()` returns an individual future. Do not assume every stream is itself a future.

Sources: RFR ch. 8; ZTP ch. 10–11; TRPL ch. [17](https://doc.rust-lang.org/stable/book/ch17-00-async-await.html), especially [async traits](https://doc.rust-lang.org/stable/book/ch17-05-traits-for-async.html). The sources do not establish every runtime's cancellation, fairness, or shutdown guarantees; inspect the version actually used.

## Unsafe and FFI decision gate

Before introducing unsafe code, identify the requirement that safe existing facilities cannot satisfy. For an optimization, establish evidence that the safe alternative is inadequate. Keep the unsafe operation narrow, but review the entire safe abstraction and private code that can affect its invariants.

For each unsafe function or block:

1. State the obligations: allocation provenance and layout, alignment, initialization and validity, bounds, aliasing, lifetime, ownership, synchronization, and ABI as applicable.
2. Explain how each obligation is established at that operation. Put a local `SAFETY` comment next to the block and caller obligations in `# Safety` documentation for an unsafe API. “The pointer is non-null” is not a complete proof of validity. Creating an invalid reference is already a violation, even if it is never dereferenced. Pointer arithmetic uses element units and must satisfy its allocation/range contract.
3. Consider safe callers with arbitrary inputs, early returns, unwinding, cancellation, and resource cleanup. A safe public API must preserve memory safety for all safe inputs. Even a caller violating an ordinary logical contract must not cause undefined behavior. A `debug_assert!` that disappears in optimized builds cannot be the only safety check. Do not rely on destructors running: safe code may forget a value.
4. Use explicit unsafe blocks inside unsafe functions and syntax compatible with the edition/MSRV. Do not disable borrowing checks through raw pointers simply to silence a compiler error.
5. Add focused regression and boundary tests. Run Miri or other existing specialized checks when applicable and available; record their limits. Tests exercise executions and do not prove soundness.

Prefer the standard library's audited implementations over educational implementations of `Rc`, allocation, slices, or synchronization. `PhantomData` affects type-system analysis; it does not validate a pointer or perform runtime ownership management.

For FFI, verify signatures, calling convention, representations, ownership transfer, allocation/deallocation pairing, callback lifetime, and error/unwind behavior. Check integer extrema and target C types, not only common values. A declaration marked safe must admit no safe Rust argument that violates the foreign preconditions. Review callback reentrancy, concurrent access, and unregister-before-free ordering. Follow [advanced boundaries](advanced-boundaries.md) for the full boundary workflow. Use only documented layout guarantees. In particular, do not assume `Option<*mut T>` has a nullable C-pointer representation. A `Box::from_raw` conversion must satisfy its full ownership and allocation contract and occur exactly as permitted, not merely receive a non-null address.

Rust 2024 requires unsafe extern blocks and unsafe annotations on attributes such as `no_mangle`. Existing earlier-edition code may need different syntax for its MSRV. Consult the [conflict register](source-conflicts.md) before adapting old FFI examples. Do not permit an unwinding path across a boundary without verifying its ABI and panic strategy.

Sources: ER Items 16 and 34; RFR ch. 9 and 11; TRPL [unsafe Rust](https://doc.rust-lang.org/stable/book/ch20-01-unsafe-rust.html); official [Box raw ownership](https://doc.rust-lang.org/stable/std/boxed/struct.Box.html#method.from_raw), [Option representation](https://doc.rust-lang.org/stable/std/option/index.html#representation), and [FFI unwinding](https://doc.rust-lang.org/nomicon/ffi.html#ffi-and-unwinding).

## Cleanup

Use RAII to tie resources to owners. Provide an explicit fallible finish/close/commit operation when callers must observe a cleanup error; `Drop` cannot return a `Result`. Avoid panic-dependent correctness because aborts skip unwinding cleanup. Leaks, process exit, and forgotten values can also skip destructors; cleanup is not a soundness assumption. Keep a guard in a binding for the required scope: `let _ = acquire_guard();` drops a newly returned guard immediately.

A custom `Drop::drop` runs before its fields are dropped; fields follow declaration order, while local variables generally drop in reverse declaration order. Use safe `std::mem::drop` to release an owned guard early. Dropping a reference or a copy of a `Copy` value does not dispose of the original owner. Do not call `Drop::drop` directly.

Sources: ER Item 11; RFR ch. 1 and 9; TRPL [Drop](https://doc.rust-lang.org/stable/book/ch15-03-drop.html); official [Drop order](https://doc.rust-lang.org/stable/std/ops/trait.Drop.html) and [mem::drop](https://doc.rust-lang.org/stable/std/mem/fn.drop.html).

Additional official contracts: [RefCell auto traits](https://doc.rust-lang.org/stable/std/cell/struct.RefCell.html), [undefined behavior](https://doc.rust-lang.org/stable/reference/behavior-considered-undefined.html), and [forget safety](https://doc.rust-lang.org/stable/std/mem/fn.forget.html).
