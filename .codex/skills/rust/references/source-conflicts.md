# Source conflicts and version-sensitive advice

Use the [inventory](sources.md) for edition information, page numbering, and full-text coverage. These resolutions are a synthesis of the cited passages and official contracts, not a blanket endorsement or rejection of a book.

For language/library semantics, prefer the applicable official contract over contradictory teaching prose. Then check whether the required API and syntax exist on the project's edition and MSRV. A current stable feature is not necessarily available on an older supported compiler. Repository policy and requirements determine choices among valid designs.

## Factual corrections

| Source passage | Finding and decision | Primary check |
| --- | --- | --- |
| SP p. 63: reference cycles | Strong `Rc`/`Arc` cycles can retain values indefinitely. Use non-owning `Weak` edges where the ownership model permits, and handle failed upgrades. | [TRPL 15.6](https://doc.rust-lang.org/stable/book/ch15-06-reference-cycles.html), [Arc cycles](https://doc.rust-lang.org/stable/std/sync/struct.Arc.html#breaking-cycles-with-weak) |
| SP pp. 50–51: destructor ordering | The prose conflicts with its displayed output. The enclosing custom destructor runs before its fields; fields drop in declaration order. Do not generalize the reverse order of local bindings to struct fields. | [Drop](https://doc.rust-lang.org/stable/std/ops/trait.Drop.html) |
| SP pp. 19–20 and 53: explicit drop | `mem::drop` is a safe consuming function. For `Copy` inputs it receives a copy, leaving the original usable; it does not create the stated dangling reference or inherently cause a double free. Distinguish it from explicitly calling the forbidden `Drop::drop` method. | [mem::drop](https://doc.rust-lang.org/stable/std/mem/fn.drop.html), [TRPL 15.3](https://doc.rust-lang.org/stable/book/ch15-03-drop.html) |
| SP pp. 8–9: smart-pointer costs | Do not treat all smart pointers as having zero runtime overhead. Reference counts, atomic operations, runtime borrow checks, and locks have costs. Choose according to ownership and synchronization needs and measure relevant hot paths. | [Arc thread safety](https://doc.rust-lang.org/stable/std/sync/struct.Arc.html#thread-safety), [TRPL 15.5](https://doc.rust-lang.org/stable/book/ch15-05-interior-mutability.html) |
| ER p. 161: UTF-8 conversion | `String::from_utf8_unchecked` skips validation and imposes a safety precondition; it is not an ordinary panicking alternative. Use `String::from_utf8` for bytes that have not been proven valid. | [String safety contract](https://doc.rust-lang.org/stable/std/string/struct.String.html#method.from_utf8_unchecked) |
| ER p. 260: reconstructing a box | A non-null pointer alone is insufficient for `Box::from_raw`. Establish the complete allocation/layout/ownership contract, including avoiding duplicate ownership and double reclamation. | [Box::from_raw](https://doc.rust-lang.org/stable/std/boxed/struct.Box.html#method.from_raw) |
| RFR p. 202: nullable pointer optimization | Do not rely on `Option<*mut T>` being layout-compatible with a nullable C pointer. The documented guarantee covers specified types, including `NonNull<U>` with its stated conditions, not arbitrary raw-pointer options. | [Option representation](https://doc.rust-lang.org/stable/std/option/index.html#representation) |

## Additional findings from full reading

These findings correct decisions, rather than reproduce or repair every pedagogical listing. Locators are printed pages unless marked PDF.

| Source | Resolution and operational consequence |
| --- | --- |
| SP pp. 28–31: `Box` examples | Returning owned data does not require a box; large `Box::new` inputs can involve stack temporaries. The enum's `[0; 1024]` field syntax is not a type. Recursive indirection fixes type size, not arbitrary-depth destruction. Use a valid representation chosen for the actual ownership/size requirement. |
| SP pp. 55–60: `Deref` examples | `Target` is an associated type, not a type parameter on `Deref`; mismatched identifiers and passing the wrong reference are example defects. Follow the trait contract and compile adapted examples. Do not implement dereferencing solely to disguise an unrelated domain object. |
| SP pp. 64–69: custom pointers | Unchecked reference-count increment can overflow, allowing premature reclamation. `PhantomData` neither repairs invalid pointers nor supplies runtime ownership. Use the standard pointers unless implementing a pointer is the actual task and its whole invariant is justified. |
| ER pp. 63, 71; TRPL 15.4–15.5 | Shared ownership permits exclusive mutation when uniqueness is established through `get_mut`; `Arc::make_mut` additionally has cloning/weak-pointer behavior. `Cell` is not a runtime borrow checker. `RefCell<T>` is `!Sync` but can be `Send` when `T: Send`. Check [Arc](https://doc.rust-lang.org/stable/std/sync/struct.Arc.html#method.get_mut) and [RefCell](https://doc.rust-lang.org/stable/std/cell/struct.RefCell.html). |
| ER Item 9; TRPL 13.2 | `scan` is an adapter; `next()` returning `None` does not guarantee permanent exhaustion for every iterator. Require the fused contract if needed. [Iterator contract](https://doc.rust-lang.org/stable/std/iter/trait.Iterator.html#tymethod.next). |
| ER pp. 190–191 versus RFR p. 74 | Different direct versions are possible through dependency renaming. Workspace lockfiles can retain multiple versions. Do not rewrite a dependency graph based on the single-version simplification. [Cargo dependency renaming](https://doc.rust-lang.org/stable/cargo/reference/specifying-dependencies.html#renaming-dependencies-in-cargotoml). |
| ER p. 248 | Formatting an allocation-failure error can allocate again. If OOM recovery is a requirement, check size arithmetic, use a supported fallible allocation API, and keep the failure representation allocation-free. |
| RFR p. 156 | Shared-reference immutability is not automatically transitive through arbitrary raw-pointer fields. Apply the actual aliasing/liveness contract; do not infer write permission or prohibition from an address alone. [Reference rules](https://doc.rust-lang.org/stable/reference/behavior-considered-undefined.html). |
| RFR pp. 158–159, 166 | Writing uninitialized `T` through an `&mut T` already violates validity. Track initialization with appropriate raw/`MaybeUninit` operations and panic-safe length handling. A debug-only assertion cannot be the sole safety enforcement in release builds. |
| RFR p. 207 | `c_void` represents the C void-pointer target, not a general zero-sized opaque-resource layout promise. Keep foreign opaque resources behind their documented pointer interface. [Official c_void](https://doc.rust-lang.org/stable/std/ffi/enum.c_void.html). |
| RFR pp. 203–205 | Do not infer complete foreign-resource cleanup from a sample comment. Verify every native handle's release contract, callback lifetime, and panic boundary against the actual library. The source corpus does not establish all foreign API contracts. |
| RFR p. 220 | A safe `static mut` singleton constructor needs a genuine single-thread/nonreentrant guarantee or synchronization. The example's target assumptions must not be generalized to arbitrary callers. |
| RFR p. 229 | Shared Cargo artifacts use the target-directory setting, not a target triple setting; prefer the existing project configuration and verify the selected Cargo version's option. Do not rewrite global Cargo configuration during a local change. |
| RFR p. 235 | The drop-guard example refers to out-of-scope `lock` and stores `true` instead of unlocking through `self.0`. Preserve the useful RAII principle, not the broken listing. A named guard binding must live across the protected operation. |
| TRPL 2, 3.2 and 4.1 | The guessing loop needs an EOF policy; arithmetic overflow depends on configured checks; `Copy` is not a stack-placement or cheap-copy guarantee. Make input termination, arithmetic and performance contracts explicit. |
| TRPL 6.3 and 10.3 | `let ... else` must diverge, not necessarily return. A borrowed output can come from genuine static storage as well as an input; annotations do not extend local storage. Excessively unified lifetimes can be restrictive while still sound. |
| TRPL 11.3 and 12.5 | A thin `main` still has testable CLI contracts. `env::var` can fail for non-Unicode values as well as absence; use `var_os` for a presence-only check. |
| TRPL 13.1 | `sort_by_key` does not promise one key call per element. `sort_by_cached_key` offers at most one evaluation with extra storage; select by contract and measurement. `Fn` also does not imply purity or thread safety. [Sorting contracts](https://doc.rust-lang.org/stable/std/primitive.slice.html#method.sort_by_key). |
| TRPL 16.3 | A poisoned standard mutex is not permanently inaccessible. Choose explicit invariant recovery or error propagation; do not blindly erase poisoning. |
| TRPL 17; ZTP pp. 417–418 | An immediately ready await need not yield. Tutorial `trpl` wrappers and runtime-specific fairness/cancellation behavior are not general language guarantees. Bound blocking work and verify the actual runtime contract. |
| TRPL 18.1 | Replacing a vector by a set can change duplicates and ordering even with unchanged signatures. Its average example also needs empty-input and overflow policy. Review semantics, not signatures alone. |
| TRPL 20.1 | A foreign call cannot be declared safe merely because it accepts numbers: all admitted inputs, result representability and target C types need review. Do not copy the unconditional safe `abs(i32)` declaration as a general FFI pattern. Invalid reference creation itself can be undefined behavior, before any later access. |
| TRPL 21 | The demonstration server has deliberately limited parsing, buffering, queue/lifecycle and failure behavior. Do not deploy it as a production HTTP server or assume `Drop` joins cannot fail. |

## Stale or version-dependent passages

- **ER pp. 26 and 244:** `core::error::Error` is now stable since Rust 1.81. Use it in an appropriate `no_std` design only when the project's MSRV permits; the book's earlier instability statement is historical. [Official stability annotation](https://doc.rust-lang.org/stable/core/error/trait.Error.html).
- **ER p. 168:** the anticipated stabilization of trait-object upcasting is not a reliable version requirement. Release notes place stabilization in Rust 1.86. Test the required coercion against the project's compiler. [Rust 1.86 release notes](https://doc.rust-lang.org/stable/releases.html#version-1860-2025-04-03).
- **ER pp. 258–261 and RFR ch. 11:** old FFI declarations need edition-aware adaptation. Rust 2024 requires `unsafe extern` blocks and forms such as `#[unsafe(no_mangle)]`; the syntax is available from Rust 1.82. A syntax migration does not verify signatures or symbol uniqueness. [Unsafe extern blocks](https://doc.rust-lang.org/edition-guide/rust-2024/unsafe-extern.html), [unsafe attributes](https://doc.rust-lang.org/edition-guide/rust-2024/unsafe-attributes.html).
- **ER p. 261 and RFR p. 204:** unwinding across FFI is ABI-dependent. A Rust panic reaching a non-unwinding boundary aborts; a foreign exception entering through a non-unwinding boundary can cause undefined behavior. `C-unwind` and the panic strategy require explicit review; `catch_unwind` does not catch aborting panics. [Nomicon: FFI and unwinding](https://doc.rust-lang.org/nomicon/ffi.html#ffi-and-unwinding).
- **ER Items 29–32:** distinguish compiling examples, executing examples, documentation tests, and benchmark harnesses. Do not assume one Cargo command executes all of them or that every benchmark requires nightly. Inspect manifest target/harness settings and the existing workflow. [Cargo test](https://doc.rust-lang.org/cargo/commands/cargo-test.html).
- **ZTP throughout:** version pins and framework-specific code belong to the supplied snapshot, which includes Rust 1.72.0 examples. They do not establish current APIs, recommended dependency versions, deployment defaults, or authentication parameters. Preserve the project's stack and validate against its installed versions.

## Stable availability checks

Verified against official documentation on the research date. Apply both the edition and MSRV checks; do not infer availability from an edition alone.

| Mechanism | Verified availability and decision | Official source |
| --- | --- | --- |
| Native async methods / return-position `impl Trait` in traits | Stable since 1.75; this does not automatically provide dyn compatibility or `Send` futures. Preserve required dispatch/bounds. | [1.75](https://doc.rust-lang.org/stable/releases.html#version-1750-2023-12-28), [dyn compatibility](https://doc.rust-lang.org/reference/items/traits.html#dyn-compatibility) |
| Let chains | Stable since 1.88, edition 2024 only; use compatible nested conditions otherwise. Corrects TRPL 19.1's blanket prohibition. | [Edition Guide](https://doc.rust-lang.org/edition-guide/rust-2024/let-chains.html) |
| Local `pin!` | Stable since 1.68; prefer supported safe pinning before manual unsafe projection. | [pin macro](https://doc.rust-lang.org/stable/std/pin/macro.pin.html) |
| `black_box` | Stable since 1.66; const use since 1.86. It is a best-effort optimization barrier, not a constant-time or correctness guarantee. | [black_box](https://doc.rust-lang.org/stable/std/hint/fn.black_box.html) |
| HTML Cargo `--timings` | Stable since 1.60; historical `-Z timings` does not mean this supported mode requires nightly. Check other output modes separately. | [1.60](https://doc.rust-lang.org/stable/releases.html#version-1600-2022-04-07), [timings](https://doc.rust-lang.org/cargo/reference/timings.html) |
| `Iterator::try_find` | Nightly-only on the checked stable docs; use an ordinary loop or supported fallible iterator operation on stable. | [try_find](https://doc.rust-lang.org/stable/std/iter/trait.Iterator.html#method.try_find) |
| Generic never type, e.g. `Result<T, !>` | Still feature-gated in the checked docs; function return `!` is a separate stable use. Use `Infallible` where an uninhabited error is needed on the supported compiler. | [never](https://doc.rust-lang.org/stable/std/primitive.never.html) |
| Associated-type `impl Trait` | Still unstable; distinct from stable return-position syntax in traits. | [feature status](https://doc.rust-lang.org/unstable-book/language-features/impl-trait-in-assoc-type.html) |
| Explicit negative impls, e.g. `impl !Unpin` | Still unstable user syntax. Prefer established safe pinning abstractions; use `PhantomPinned` only in a justified pinned-type design. | [negative impls](https://doc.rust-lang.org/unstable-book/language-features/negative-impls.html) |
| Procedural macro input errors | Stable procedural macros may emit `compile_error!`; they need not panic as TRPL 20.5 suggests. | [Reference](https://doc.rust-lang.org/reference/procedural-macros.html) |

## Context-dependent differences

| Apparent tension | Resolution used by this skill |
| --- | --- |
| Borrowing avoids copies, but owned data simplifies lifetimes. | Borrow for views and inspection; own for retention, transfer, or independence. ZTP's temporary serialization payload (p. 242) benefits from borrowing; that does not imply every long-lived domain struct should borrow. ER Items 14–15 and RFR ch. 1 support the ownership trade-off. |
| ER Item 18 discourages panic; introductory examples use it freely. | TRPL 9.3 and RFR ch. 4 distinguish expected failures from programmer-contract violations and test assertions. Assess each call's contract; retain useful `expect` in tests and documented invariants. Prefer fallible validation for external inputs, as ZTP ch. 6 ultimately does. |
| Concrete errors support matching; ZTP uses opaque unexpected errors. | Select variants according to the caller's recovery needs. Preserve causes and context without exposing every implementation error as a public enum variant. RFR ch. 4 and ZTP ch. 8 are compatible under this criterion. |
| Generics and iterators can avoid abstraction overhead, but still affect compile time and code size. | Use the simplest expressive abstraction and measure relevant costs. TRPL 13.4 demonstrates a workload, not a universal speed guarantee; RFR ch. 2 and 6 discuss broader costs. |
| A small lock scope reduces contention, but split updates can violate an invariant. | Protect the complete invariant and avoid unrelated work while locked. Choose channels, locks, or atomics by the coordination requirement, not a universal preference. ER Item 17 and RFR ch. 10. |
| Tutorials build pointers, thread pools, and HTTP parsers by hand. | They expose mechanisms for learning. Prefer existing safe facilities for production unless the requested component genuinely requires implementation of those mechanisms. TRPL ch. 21 explicitly limits its server example; SP's educational pointer code is not an audited library. |

## Research boundaries

The sources do not settle all unsafe provenance/aliasing questions, all runtime cancellation semantics, exhaustive web security, current crate health, or every `no_std` target's capabilities. Use the [resolution procedure](validation-and-maintenance.md#resolve-missing-or-conflicting-evidence) to obtain the required contract, choose a safe alternative, or stop only the dependent change before making a concrete claim. Within this skill's research, stay on the exact host `doc.rust-lang.org`; do not follow external links merely because a book cites them.

## Service tutorial completion gates

ZTP ch. 10 explicitly teaches insecure intermediate states; ch. 11 ends with additional exercises. Full reading reveals these concrete completion requirements:

| ZTP printed location | What the supplied text/code establishes | Decision used in the skill |
| --- | --- | --- |
| 309, confirmation tokens | Lookup/update alone does not consume the token despite single-use wording. | Specify replay/expiry behavior and enforce it atomically when required; test repeats and expired inputs. |
| 357–359, error design | Opaque unexpected errors and typed actionable variants serve different audiences. | Choose by recovery needs, preserve causes/context, log once at handling boundaries. |
| 378–383, stored records | Earlier validation may no longer match current rules. | Explicitly migrate, reject, quarantine/skip, or process historical data; no invariant `unwrap` justified solely by old validation. |
| 398–414, password walkthrough | Plaintext and fast hashes are deliberately replaced; numeric parameters are historical. | Use the project's reviewed password mechanism/policy, never the insecure stages or stale parameter recommendations. |
| 410–412, PHC format | The prose schematic reverses salt/hash while the library parses the real representation. | Let the selected library serialize/parse the supported format; do not implement the schematic manually. |
| 425–426, dummy hashing | Addresses one timing difference under chosen parameters. | Do not claim universal indistinguishability, especially across hash migrations; enforce and test the project's broader abuse policy. |
| 451, 476, 489, 505 | Simplified HMAC and direct HTML interpolation are not complete security recipes. | Use vetted protocol implementations and contextual output encoding; signing does not sanitize content. |
| 488, 501, internal error helper | Opaque-body behavior is asserted but depends on the actual framework conversion. | Construct/test the safe public response and retain internal cause; no unverified redaction claim. |
| 491–492 | TypedSession is a newtype wrapper; lack of async trait syntax is historical. | Choose a wrapper for real type/key invariants; use edition/MSRV-aware trait facilities. |
| 496, 508, 514 | Public seed credentials, password policy exercise and dated hashing settings. | Require private provisioning and an established policy before an authentication-sensitive change; do not deploy demo defaults. |
| 531 | Same-key/different-payload detection explicitly omitted. | Define equivalence and reject conflicting reuse before side effects when claiming those idempotency semantics. |
| 537 | The implementation accepts 1–49 bytes while prose says characters. | Specify units and boundary inclusivity; test multibyte and boundary values. |
| 544 | Intermediate replay code constructs but does not send the flash message. | Test observable replay behavior; use the final intended flow. |
| 552, 559–560 | Delay encourages overlap; database reasoning assumes the demonstrated isolation. | Control the race point; handle actual conflict/serialization outcomes for the configured database. |
| 564, 572–573 | Atomic enqueue is implemented, but failed delivery is logged and the task deleted; retry remains an exercise. | Distinguish acceptance from delivery and implement/test retry or terminal discard according to the contract. |
| 574 | A held transaction plus another pool acquisition can consume multiple connections per worker. | Budget nested acquisitions or reuse the transaction; do not assume separate pools or unlimited connections. This is a derived resource analysis. |
| 576–580 | Task errors can be logged while main returns success; direct drain tests omit supervision. | Specify exit status and coordinated shutdown; test lifecycle separately from delivery behavior. |
| 581 | Idempotency expiry is an exercise, not implemented. | Define and test retention/cleanup before claiming bounded deduplication storage. |

The books supply neither a universal security standard nor a complete distributed-systems specification. The [service reference](service-engineering.md) turns these source boundaries into explicit prerequisites and validation gates; it does not leave them as implementation TODOs.
