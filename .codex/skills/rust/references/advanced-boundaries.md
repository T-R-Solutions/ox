# Advanced boundaries

Read only the sections relevant to the change. Start with [design](design.md) and the [unsafe gate](concurrency-and-safety.md#unsafe-and-ffi-decision-gate); these topics do not justify introducing advanced mechanisms by themselves.

## Layout, initialization, and custom ownership

Use documented representations when crossing a binary boundary. `repr(Rust)` field order is not a serialization format; `repr(C)` still involves target ABI, padding and endianness. `repr(transparent)` has specific field/alignment rules, not a promise that every wrapper has its inner type's ABI. Do not generalize a niche optimization observed in one type to nested wrappers or arbitrary `Option<T>`.

A raw pointer's address, provenance, allocation extent, alignment, initialization and ownership are distinct facts. Shared references restrict mutation through the applicable reference/ownership graph; the mere presence of a raw-pointer field does not freeze every allocation it could point at. Use the exact reference and pointer contracts rather than extrapolating diagrams. Never create an intermediate unaligned reference to a packed field; use a supported raw-borrow operation and an appropriate access primitive when the layout genuinely requires it.

For partially initialized storage, use `MaybeUninit` or the existing safe facility. Track exactly which elements are initialized, update length only after initialization, and clean up the initialized subset on every failure path. Assignment through an `&mut T` requires a valid `T`; it is not a way to initialize uninitialized storage. Do not use `ManuallyDrop`, `transmute`, or handwritten reference counting merely to avoid ordinary ownership refactoring. A custom count must handle overflow without permitting premature reclamation.

For pointer-backed types, review variance, drop checking, auto traits, and pinning across every safe method. `PhantomData` communicates a type-level relationship; it creates no runtime validity. Safe trait implementations, accessors, or future changes can break an unsafe invariant even outside the unsafe block. Recursive structures may need bounded depth or iterative destruction when adversarial depth can exhaust the stack.

Sources: ER Items 8, 14–16; RFR ch. 1–2 and 9; SP pointer implementations with [corrections](source-conflicts.md); official [layout](https://doc.rust-lang.org/stable/reference/type-layout.html), [undefined behavior](https://doc.rust-lang.org/stable/reference/behavior-considered-undefined.html), and [Option representation](https://doc.rust-lang.org/stable/std/option/index.html#representation).

## FFI and build scripts

Before changing bindings or a safe wrapper, record the foreign function's ABI and the ownership contract for each argument/result. Use the target's C types. Check nullability, buffer length units, termination/encoding, maximum lengths, integer conversions, allocation origin, and exactly which function releases which resource. Do not use a layout guessed from a Rust example or a destructor guessed from a library name.

Keep unvalidated raw operations behind an appropriate unsafe interface; expose a safe wrapper only after enforcing every precondition safe callers could violate. For callbacks, specify who owns the context, how long callbacks can continue, whether they can run concurrently or reentrantly, and how unregistering synchronizes with in-flight calls. A manual `Send`/`Sync` implementation requires the foreign library's actual threading contract.

Preserve the project's established bindings. Generated bindings can reduce declaration mistakes but do not prove lifetime, ownership, synchronization, or panic safety. Do not add a generator or sys crate for an unchanged small boundary. If generating bindings, make target headers/flags and native-library versions reproducible. Build scripts run on the host: distinguish host from target, place generated artifacts in `OUT_DIR`, declare rebuild triggers, and avoid ambient machine-specific paths in published artifacts. Validate the final linked target, not just the Rust declarations.

For an exported operation, select explicit success/error representations and a panic/unwind policy compatible with its ABI. `catch_unwind` handles only unwinding Rust panics; it neither catches aborts nor establishes how arbitrary foreign exceptions behave. See the [FFI safety gate](concurrency-and-safety.md#unsafe-and-ffi-decision-gate).

Sources: ER Items 34–35; RFR ch. 11; TRPL 20.1; [FFI unwinding](https://doc.rust-lang.org/nomicon/ffi.html#ffi-and-unwinding). Foreign-library-specific contracts are an input requirement: use the [resolution procedure](validation-and-maintenance.md#resolve-missing-or-conflicting-evidence) if unavailable.

## Macros and public traits

Prefer a function, generic, or existing derive when it expresses the operation. Use a macro for syntax-level repetition or code generation that those mechanisms cannot represent clearly. A macro's expansion is part of its interface.

Review expression evaluation count/order, moves and borrows, generated names, paths, hygiene, visibility, and control flow. In exported declarative macros, use robust paths such as `$crate` for defining-crate items; test expansion from a downstream crate with renamed dependencies and without assumed imports when supported. Test invalid inputs for useful diagnostics and intended rejection, as well as valid syntax. An unused macro definition compiling does not prove every expansion compiles.

For procedural macros, preserve useful spans and report input errors as diagnostics rather than arbitrary panics. Consider build cost and target separation before introducing a proc-macro crate. Do not emulate reflection with `Any` when an enum or trait expresses a known closed set; use runtime type identification only for an actual open-ended requirement and respect its `'static` constraint.

For traits, associated types express a type determined by an implementation; generic parameters allow different implementations where coherence permits. Default methods should derive from the required operations without mutual-recursion traps. Review dyn compatibility and downstream implementation obligations when adding methods. Sealing is an intentional restriction on implementors, not a blanket guarantee that later additions cannot break callers.

Sources: ER Items 12–13, 19 and 28; RFR ch. 3 and 7; TRPL [advanced traits](https://doc.rust-lang.org/stable/book/ch20-02-advanced-traits.html) and [macros](https://doc.rust-lang.org/stable/book/ch20-05-macros.html).

## no_std and constrained targets

Choose `no_std` only for a stated portability or platform requirement. Separate `core` availability, optional `alloc`, operating-system services, atomics, threading, and the final binary's allocator/panic/runtime requirements. A `#![no_std]` crate attribute does not prove that enabled dependencies avoid `std` or allocation.

Inspect default features and the resolved dependency graph for the intended target; use `default-features = false` only where needed and verify what another dependency can re-enable. Keep platform-independent logic separate from hardware/OS adapters when that reduces actual coupling. Test the promised target/configuration and final link; a host library check alone is insufficient.

Avoid introducing an allocator, spinlock, interrupt masking, inline assembly, or a global singleton without the platform contract. Volatile MMIO does not imply atomicity or mutual exclusion. A safe singleton constructor using `static mut` is unsound if concurrent or reentrant calls can violate uniqueness; use the target's established synchronization/initialization mechanism. Validate resource exhaustion, panic strategy, alignment, and execution-context constraints relevant to the component.

The books do not specify every hardware ABI or a real-time scheduling guarantee. If such a guarantee is required, obtain the target contract and measurements through the [resolution procedure](validation-and-maintenance.md#resolve-missing-or-conflicting-evidence); do not label a generic Rust implementation real-time or interrupt-safe by inference.

Sources: ER Item 33; RFR ch. 12; [core::error::Error availability](https://doc.rust-lang.org/stable/core/error/trait.Error.html). Version-specific syntax and library availability are recorded in [source conflicts](source-conflicts.md).
