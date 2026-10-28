# Design decisions

Use these criteria when the corresponding code is being changed. Source IDs and coverage are defined in [sources](sources.md).

## Ownership and borrowing

| Need | Starting choice | Trade-off or exception |
| --- | --- | --- |
| Inspect existing data | `&T`, `&str`, `&[T]` | Require a concrete container reference only for container-specific operations. |
| Mutate an existing value exclusively | `&mut T` | Keep the borrow as short as the operation permits; split independent data when necessary. |
| Consume, retain, or transfer a resource | An owned `T`, `String`, or `Vec<T>` | Moving an owned input can avoid cloning it; borrowing everything can spread lifetime constraints throughout the design. |
| Return a view into an input | A borrowed slice/reference | Tie the output only to the input it actually borrows; use lifetime elision when sufficient. |
| Return newly created or independent data | An owned value | Do not return references to locals or add `'static` to disguise an ownership problem. |
| Duplicate data or retain a shared handle | `clone` with understood semantics | A `String` clone copies data; `Arc::clone` shares an allocation and updates a count. Neither cost nor independence follows from the method name alone. |

First try smaller scopes, borrowing fields separately, consuming iteration, or `Option::take`/`mem::replace` when resolving a borrow error. Use replacement only when the temporary state preserves invariants, including on early return or panic. A deliberate clone can improve lifetime independence and clarity; avoid replacing a small clone with a complicated ownership graph without evidence.

Lifetimes describe relationships; annotations do not extend a value's life. Distinguish a `&'static T` reference from a `T: 'static` bound, which excludes shorter borrowed contents but does not require the owned value to live forever. Choose `Cow` only when real borrowed and owned paths justify its extra API complexity. An immutable binding or `&T` does not prohibit interior mutation through a sound cell/lock abstraction. Avoid giving a method receiver the full lifetime of its struct unless that long borrow is actually required. Before returning a lazy iterator, account for every captured reference, including a search predicate; removing a `collect` can change lifetime requirements and when errors or side effects occur.

Keep one owner where possible. Use `Box` for necessary indirection, recursive types, or owned dynamically sized data. Use `Rc` for shared ownership confined to a thread and `Arc` when cross-thread sharing or an API contract requires it. Model non-owning graph edges with `Weak`, or consider indices/IDs with an explicit invalidation policy. Reference counting has costs and strong cycles can leak. `Rc::get_mut`/`Arc::get_mut` can provide exclusive access when their uniqueness conditions hold; copy-on-write mutation has different cloning and weak-reference semantics. Returning an owned value does not alone require boxing it. See [concurrency and safety](concurrency-and-safety.md) before adding interior mutability.

Sources: ER Items 8, 14–15; RFR ch. 1, 3 and 13; SP ownership and smart-pointer chapters, subject to the [corrections](source-conflicts.md); TRPL [ownership](https://doc.rust-lang.org/stable/book/ch04-01-what-is-ownership.html), [slices](https://doc.rust-lang.org/stable/book/ch04-03-slices.html), and [lifetimes](https://doc.rust-lang.org/stable/book/ch10-03-lifetime-syntax.html).

## Model valid states and useful abstractions

- Use a struct for related data and an enum for mutually exclusive cases with different payloads. Prefer exhaustive matching when adding a variant should force reconsideration; use `if let` or `let ... else` when ignoring other cases or exiting early is intentional and supported by the MSRV.
- In patterns, distinguish a new binding from a comparison, `_` from a named `_value` that can still move a value, and borrowed destructuring from consumption. Match guards do not establish exhaustiveness. A `let ... else` else branch must diverge; use syntax supported by the edition/MSRV.
- Use a private-field newtype with validated construction for a meaningful invariant or distinction between units/identifiers. A type alias does not create a new type. Preserve the invariant through mutation, deserialization, and conversion as well as the main constructor.
- Implement `From` for infallible conversions and `TryFrom` for fallible ones. Do not hide lossy numeric conversion behind `as` unless the loss is intended and justified. Choose checked, saturating, or wrapping arithmetic according to the required behavior rather than depending on debug/release overflow differences.
- Use a builder when optional/configurable arguments or staged validation make a constructor hard to use. Keep mandatory construction requirements and the final validation point explicit; avoid a builder for a trivial two-field value.
- Start with concrete functions and types. Add a trait or generic parameter for actual interchangeable behavior, reuse, or a useful testing boundary. Use only bounds the implementation needs; an unnecessary `Clone`, `Send`, or `'static` restricts callers.
- Choose generics/static dispatch for compile-time polymorphism; choose `dyn Trait` for runtime heterogeneity or deliberate type erasure. Consider compilation time and code size as well as call overhead. Check dyn compatibility when trait objects are part of the API.
- Use the least restrictive callable bound that works: `FnOnce` for one invocation, `FnMut` when repeated invocation may mutate captures, and `Fn` when shared repeated access is required. `move` specifies capture ownership; it does not by itself mean the closure is only `FnOnce`. `Fn` does not imply purity, absence of interior mutation, or `Sync`. Do not rely on a callback invocation count unless its consumer documents it.
- Derive standard traits when fieldwise behavior matches the contract. Keep equality, hashing, and ordering consistent. For `PartialOrd`, decide how incomparable values such as NaN are handled; do not assume every domain has a total order. `Copy`, `Default`, serialization, and `Debug` are semantic decisions; `Copy` does not guarantee inexpensive copies, and derives can add unnecessarily strong generic bounds; a default must be valid and debug output must not expose secrets.
- Use `AsRef` for a view; implement `Borrow` only when the borrowed and owning forms also preserve the required equality, ordering, and hashing semantics. Implement `Deref` for transparent pointer-like behavior, not to simulate arbitrary inheritance or expose invariant-breaking mutation.
- Prefer explicit composition to reproducing an inheritance hierarchy. A state enum is often sufficient; typestate can prevent invalid transitions when that benefit outweighs additional types and API complexity. Introduce macros only when functions, generics, or existing derives cannot express the needed reuse clearly.

Sources: ER Items 1–7, 10, 12–13; RFR ch. 2–3; ZTP ch. 6; TRPL ch. [6](https://doc.rust-lang.org/stable/book/ch06-02-match.html), [10](https://doc.rust-lang.org/stable/book/ch10-02-traits.html), [13](https://doc.rust-lang.org/stable/book/ch13-01-closures.html), [18](https://doc.rust-lang.org/stable/book/ch18-03-oo-design-patterns.html), and [20](https://doc.rust-lang.org/stable/book/ch20-02-advanced-traits.html).

## Errors and panics

Use `Option` for meaningful absence and `Result` for an operation that can fail. Preserve both meanings when needed, for example `Result<Option<T>, E>` for a lookup that can fail or find nothing. Propagate with `?` when the caller should decide; handle locally when the layer can actually recover or translate the failure into its own contract.

Choose error variants by the distinctions a caller needs to act on. Concrete errors often help public libraries; an opaque error with preserved causes can suit an application boundary. This is a decision about recovery and compatibility, not an absolute library/application rule. Keep the project's existing error approach unless there is a demonstrated shortcoming; do not add an error crate for a trivial case.

Add context at meaningful abstraction boundaries and preserve the underlying error through `Error::source` or the established equivalent. Avoid flattening errors into strings when callers need classification or cause chains. Log at the handling boundary rather than at every propagation step. Separate operator diagnostics from safe user-facing messages.

`unwrap` and `expect` are appropriate for tests, clearly marked prototypes, and invariants whose failure would be a bug. For a production invariant, document why failure is impossible; use an explanatory `expect` where that helps diagnosis. Expected malformed input, unavailable files, network failures, and cancellation normally require an error path. A startup failure may deliberately terminate the application, but still deserves a useful diagnostic.

Use `panic!` for violated programmer contracts when continuing would be invalid and the API deliberately specifies that behavior. Document public panic conditions. Review indexing and hidden panics as well as explicit macros. Avoid panicking in `Drop`; unwinding and aborting have different cleanup behavior. Do not use unsafe unchecked operations as substitutes for ordinary error handling.

Sources: ER Items 4, 18; RFR ch. 4; ZTP ch. 6, 8 and 9; TRPL [Result](https://doc.rust-lang.org/stable/book/ch09-02-recoverable-errors-with-result.html) and [panic decisions](https://doc.rust-lang.org/stable/book/ch09-03-to-panic-or-not-to-panic.html). See [examples](examples.md) for a fallible newtype and deliberate error-preserving iteration.

## Modules, public APIs, and documentation

Group code by coherent responsibility and invariants. Keep implementation details private; choose `pub(crate)` or narrower visibility when that suffices. Follow the repository's supported module-file convention. Re-export intentionally when a stable public path should differ from internal organization. Extract library logic from a CLI binary when reuse or integration testing benefits from it, not as an obligatory layout for every small program.

Review changes from a downstream caller's perspective. Public fields, enum variants, trait implementations and bounds, error variants, auto traits such as `Send`/`Sync`, and exposed dependency types can become compatibility commitments. Even apparently more general signatures can break inference. Review observable ordering, duplicates, blocking, and error behavior as well as signatures. `#[doc(hidden)]` does not make an item private; `#[non_exhaustive]` and sealed traits are deliberate extensibility trade-offs, not retroactive compatibility fixes. Avoid accidental foreign types in public APIs; use a wrapper or intentional re-export when warranted.

Document public purpose and contracts with `///`; use `//!` for crate/module context. Add applicable examples, `# Errors`, `# Panics`, and `# Safety` sections. Explain ownership, side effects, and important cost characteristics when callers need them. Prefer runnable examples with assertions; document the reason for `no_run` or `ignore` instead of using them to conceal broken examples.

Sources: ER Items 21–24, 27; RFR ch. 3 and 5; TRPL [module privacy](https://doc.rust-lang.org/stable/book/ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html) and [public documentation](https://doc.rust-lang.org/stable/book/ch14-02-publishing-to-crates-io.html).

## Collections, text, and performance

Use collection behavior to drive the choice: contiguous sequence, lookup, ordering, or queue operations. Start with standard collections; a `Vec` often suffices for small sequences. Use `VecDeque` for efficient work at both ends and a sorted structure when key order is part of the contract. Do not assume `HashMap` iteration order is stable. Moving from `Vec` to a set changes duplicate and ordering behavior even if method signatures remain identical. Consider `entry` when lookup and insertion are one operation. Use `get` when a missing index is expected; indexing is reasonable when the bounds are established.

Rust strings are UTF-8. Distinguish bytes, Unicode scalar values, and user-perceived characters. A byte count is not a character count; slicing must respect UTF-8 boundaries. Choose byte or character iteration deliberately. Keep paths and operating-system arguments in `Path`/`OsStr` forms when Unicode cannot be assumed. Full grapheme segmentation, normalization, and language-sensitive case matching need additional domain evidence; the introductory examples do not establish their complete behavior.

Choose `iter`, `iter_mut`, or `into_iter` to match borrowing, mutation, or consumption. Use readable iterator chains for transformations and loops for clearer branching or stateful work. Avoid intermediate `collect` calls unless materialization is needed. `flatten` and `filter_map(Result::ok)` discard errors: do that only when skipping failures is the intended policy. Otherwise collect into a `Result` or handle the errors explicitly. Adapters are lazy: unconsumed transformations do no work. A general iterator may yield `Some` after `None`; require the fused contract or use `fuse()` if permanent exhaustion matters. `scan` is an adapter, not a terminal consumer.

For a performance change, identify the workload and bottleneck, establish a baseline, and measure the affected behavior with the project's optimized configuration. Examine algorithmic complexity and I/O before micro-optimizations. Reuse buffers, reserve capacity, borrow, or move values where the expected workload supports it; account for retained memory and API complexity. An iterator or generic abstraction can optimize well but is not a benchmark result. Reference-count updates, locks, bounds checks, and clones still deserve measurement when hot. Do not trade correctness for an unmeasured speed claim. For capacity calculations, check arithmetic before allocation; if allocation failure is recoverable, use a supported fallible allocation path and an error representation that does not itself require another allocation. Large `Box::new` inputs are not a portable guarantee against temporary stack use.

For CLI or file processing, define EOF, encoding, size, and output-stream behavior. A zero-byte `read_line` is EOF; repeatedly treating it as invalid input can spin forever. Use whole-file reads only within the intended memory budget; a lazy iterator over an already loaded string is not streaming I/O. Separate normal stdout data from stderr diagnostics and preserve the required exit status.

Sources: ER Items 8–9, 14, 17, 30; RFR ch. 2, 6 and 10; ZTP pp. 242 and 380; TRPL [collections](https://doc.rust-lang.org/stable/book/ch08-00-common-collections.html), [strings](https://doc.rust-lang.org/stable/book/ch08-02-strings.html), [iterators](https://doc.rust-lang.org/stable/book/ch13-02-iterators.html), and [performance](https://doc.rust-lang.org/stable/book/ch13-04-performance.html).

Additional contract checks: [Borrow laws](https://doc.rust-lang.org/stable/std/borrow/trait.Borrow.html), [Iterator::next](https://doc.rust-lang.org/stable/std/iter/trait.Iterator.html#tymethod.next), and [Arc mutation](https://doc.rust-lang.org/stable/std/sync/struct.Arc.html#method.get_mut). See [source conflicts](source-conflicts.md) for the source-specific reasons for these qualifications.
