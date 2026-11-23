# Sources, inventory, and coverage

## Research scope and completion

Research date: **2026-10-17**. All four PDFs found in `docs/languages/rust` were inventoried before synthesis. **The full extracted text of all 1,255 PDF pages was read**, including front matter, chapters, code, diagnostics, footnotes, exercises and back matter. Blank pages contribute to the PDF count but contain no text. The entire official Rust Book print view was read: **111 nonempty section units**, covering its front matter, chapters 1–21 and appendices A–G. Retrieval/extraction alone was not counted as reading. Truncated inspection output was reread in smaller or overlapping chunks.

This revision replaces the earlier selective-reading analysis. The primary agent read all of ER, RFR, SP and ZTP PDF pages 1–450. After explicit user authorization, a second reader read ZTP PDF pages 451–601, and two readers read Rust Book section units 1–60 and 61–111 respectively. Their complete-coverage reports and findings were consolidated into the decision references and conflict register. No required text range remains pending.

All online access stayed on the exact HTTPS host `doc.rust-lang.org`. External footnotes, repositories, providers, linked translations and other hosts were not visited. Source content was treated as reference, not instructions to install tools, change credentials, publish crates or deploy examples. The skill contains synthesis and original examples rather than redistributed book text.

**Coverage is full-text analysis, not a claim of complete visual or executable verification.** PDF extraction preserves page boundaries but may alter typography and code wrapping. Figure captions and surrounding explanations were read; every rendered diagram/page was not separately visually audited. The ZTP cover was inspected to identify its author. The books' complete listing suites were not executed; many listings intentionally fail or represent incomplete stages. These validation boundaries do not become invented guarantees: consequential facts were checked against official contracts, and target-specific prerequisites have a defined [resolution procedure](validation-and-maintenance.md#resolve-missing-or-conflicting-evidence).

## Local inventory

Printed page numbers are used in recommendation references. PDF numbering includes cover/front matter.

| ID | Original and title | Author, edition and snapshot evidence | Format / extent |
| --- | --- | --- | --- |
| ER | Effective_Rust.pdf (historical library source: `docs/languages/rust/Effective_Rust.pdf`; not required at runtime), *Effective Rust: 35 Specific Ways to Improve Your Rust Code* | David Drysdale; O'Reilly; First Edition, April 2024; first release 2024-04-01; preface uses edition 2018 and Rust 1.70 | PDF, 296 pages; printed p. 1 = PDF p. 13 |
| RFR | Rust_for_Rustaceans.pdf (historical library source: `docs/languages/rust/Rust_for_Rustaceans.pdf`; not required at runtime), *Rust for Rustaceans: Idiomatic Programming for Experienced Developers* | Jon Gjengset; No Starch Press; copyright 2022; first-printing number line; back cover says current as of Rust 2021; no numbered edition identified | PDF, 283 pages; printed p. 1 = PDF p. 27 |
| SP | Smart_Pointers_in_Rust.pdf (historical library source: `docs/languages/rust/Smart_Pointers_in_Rust.pdf`; not required at runtime), *The Accelerated Guide to Smart Pointers in Rust* | Tim McNamara; Accelerant Press; copyright 2023; afterword May 2023; no numbered edition identified | PDF, 75 pages; printed page + 1 = PDF page |
| ZTP | Zero_To_Production.pdf (historical library source: `docs/languages/rust/Zero_To_Production.pdf`; not required at runtime), *Zero to Production in Rust: An Opinionated Introduction to Backend Development* | Luca Palmieri, confirmed on the rendered cover; no numbered edition/publication date established; code includes Rust 1.72.0 pins and edition 2021, which identify code assumptions rather than a publication date | PDF, 601 pages; printed p. 1 = PDF p. 20 |

SHA-256 fingerprints of the supplied PDFs:

```text
ER   a14fda8b13c583d1af0a1163b023372b38428da5318c5f0791db7195605b2c72
RFR  c6d10d26e51a1ff7708d801a2bde2db5f0a72ab757bf6175fd1a34534d8acd81
SP   71ed038ce18b4e61803117d1cd0ba990a506ece23c19f575b0cb52da318eca93
ZTP  54958877803b11e56f2ad09e00b710eb420f9ba0f40684bfc5ebb950c3b9ec50
```

## Effective Rust

**Complete:** PDF pages 1–296, all 35 items, front/back matter. Ranges below partition the substantive items; chapter introductions and remaining matter were also read. Labels summarize the decision subjects rather than copy the item titles.

| Item | Printed pages | Decision extracted |
| --- | --- | --- |
| 1 | 2–9 | Types express valid data states |
| 2 | 10–19 | Traits and callable capabilities |
| 3 | 20–24 | Readable Option/Result transformations |
| 4 | 25–33 | Caller-oriented errors and propagation |
| 5 | 34–39 | Infallible/fallible and numeric conversion |
| 6 | 40–44 | Newtypes and semantic distinctions |
| 7 | 45–50 | Builders for genuinely complex construction |
| 8 | 51–63 | References, ownership and pointer choices |
| 9 | 64–76 | Iteration, laziness and error policy |
| 10 | 77–88 | Standard traits and coherent semantics |
| 11 | 89–92 | RAII and observable fallible cleanup |
| 12 | 93–102 | Generics versus dynamic dispatch |
| 13 | 103–105 | Minimal required trait methods |
| 14 | 106–122 | Lifetimes as relationships |
| 15 | 123–141 | Ownership refactoring before workarounds |
| 16 | 142–144 | Safe alternatives and unsafe obligations |
| 17 | 145–158 | Shared-state coordination and lock scope |
| 18 | 159–161 | Panic versus recoverable failure |
| 19 | 162–168 | Avoid unnecessary runtime reflection |
| 20 | 169–175 | Measure before complicating code |
| 21 | 176–180 | Public compatibility and version policy |
| 22 | 181–185 | Minimum necessary visibility |
| 23 | 186–187 | Clear imports with contextual exceptions |
| 24 | 188–190 | Public dependency types and re-exports |
| 25 | 191–196 | Dependency graph and version coexistence |
| 26 | 197–202 | Feature scope and compatibility |
| 27 | 203–208 | Public contracts and runnable documentation |
| 28 | 209–222 | Macros only for justified code generation |
| 29 | 223–226 | Project-compatible Clippy policy |
| 30 | 227–234 | Behavioral, integration and broader testing |
| 31 | 235–236 | Tooling matched to task and availability |
| 32 | 237–242 | CI configurations and meaningful checks |
| 33 | 243–248 | Conditional no_std portability |
| 34 | 249–260 | FFI contracts and unsafe interfaces |
| 35 | 261–264 | Bindings and generation trade-offs |

Use: [design](design.md), [concurrency/safety](concurrency-and-safety.md), [advanced boundaries](advanced-boundaries.md), [validation](validation-and-maintenance.md). Full reading identified outdated APIs, unsafe-contract defects and overbroad claims; their resolutions are in [source conflicts](source-conflicts.md).

## Rust for Rustaceans

**Complete:** PDF pages 1–283, all 13 chapters, front matter, index and back matter. End-page ranges include intervening blank/separator pages where present.

| Chapter | Printed pages | Analysis incorporated |
| --- | --- | --- |
| 1, Foundations | 1–18 | Ownership models, reference validity, lifetime relationships, variance and drop scope |
| 2, Types | 19–36 | Layout/representation, DSTs, static/dynamic dispatch and type bounds |
| 3, Designing Interfaces | 37–56 | Semantic derives, borrow/own APIs, dyn compatibility, typestate, documentation and hidden commitments |
| 4, Error Handling | 57–66 | Actionable versus opaque errors, causes, conversion, panic boundaries |
| 5, Project Structure | 67–84 | Features/resolution, manifests, workspaces, MSRV and dependency versions |
| 6, Testing | 85–100 | Unit/integration/doc tests, compile-fail intent, property/fuzz/model checks and benchmarks |
| 7, Macros | 101–116 | Expansion, hygiene, exported paths, procedural diagnostics and compile-time cost |
| 8, Asynchronous Programming | 117–140 | Polling, wakeups, runtimes, task lifetimes, cancellation and pinning |
| 9, Unsafe Code | 141–166 | Whole-abstraction invariants, initialization, aliasing, variance, panic safety and proof limits |
| 10, Concurrency (and Parallelism) | 167–192 | Communication, locks, atomics/orderings, contention and concurrent testing |
| 11, Foreign Function Interfaces | 193–210 | ABI, foreign ownership, callbacks, binding generation and build scripts |
| 12, Rust Without the Standard Library | 211–222 | core/alloc/std separation, platform contracts, initialization and final-link validation |
| 13, The Rust Ecosystem | 223–244 | Historical tools/crate catalog, profiling, ownership idioms, guards, indices and maintenance |

Use: all implementation/review references. Chapter 13's crate catalog is historical context, not a current dependency endorsement. Source errors in raw-pointer transitivity, nullable representations, guards and configuration are explicitly reconciled.

## Smart pointers

**Complete:** PDF pages 1–75, every section, listing, recap, cheat sheet and afterword. This table uses PDF pages to avoid ambiguous unnumbered front matter.

| PDF pages | Subject | Decision incorporated |
| --- | --- | --- |
| 1–6 | Publication, introduction, contents | Inventory and teaching scope |
| 7–19 | Pointer definitions, Rust, ownership, borrowing, lifetimes | Ownership capabilities and lifetime relationships; no universal runtime-cost guarantee |
| 20–27 | Smart-pointer motivation | Resource ownership, sharing and explicit costs |
| 28–39 | Box, Rc, Arc | Indirection versus shared ownership, uniqueness and cycles |
| 40–47 | RefCell, Mutex, RwLock | Runtime borrow checks, guards, invariant scope and workload trade-offs |
| 48–62 | Drop, Deref, DerefMut | Cleanup order, pointer-like interfaces, invariant-preserving mutation |
| 63–70 | Cycles, custom Rc, PhantomData | Weak edges, count overflow, and type-level versus runtime guarantees |
| 71–75 | Recap, cheat sheet, afterword, author | Consolidation checked against the detailed contracts |

The [conflict register](source-conflicts.md) corrects its drop-order, Copy/drop, cycle, trait-definition and custom-pointer defects. Educational implementations were not adopted as production utilities.

## Zero to Production

**Complete:** PDF pages 1–601, including the entire security chapter and final exercises. Printed ranges include separator pages; chapter 10's summary ends on p. 523, followed by a separator.

| Chapter | Printed pages | Analysis incorporated |
| --- | --- | --- |
| 1, Getting Started | 1–10 | Historical pins, Cargo/tooling, CI and check-versus-execution distinctions |
| 2, Building an Email Newsletter | 11–14 | Explicit goals/non-goals, domain behavior and incremental delivery |
| 3, Sign Up a New Subscriber | 15–88 | Startup, protocol tests, port/database isolation, parameterized queries and persistence |
| 4, Telemetry | 89–132 | Structured spans/context, secrets, diagnostic layering and async instrumentation |
| 5, Going Live | 133–164 | Configuration, build/runtime compatibility, schema metadata and deployment assumptions |
| 6, Reject Invalid Subscribers #1 | 165–208 | Validated newtypes, Unicode units, fallible construction and generated tests |
| 7, Reject Invalid Subscribers #2 | 209–322 | Confirmation, HTTP-client reuse, mocks, timeouts, migration and transaction boundaries |
| 8, Error Handling | 323–360 | Reporting versus control flow, error causes, contextual conversion and one handling boundary |
| 9, Naive Newsletter Delivery | 361–386 | Stored-data evolution, partial failure, borrowed APIs and limits of functional-only tests |
| 10, Securing Our API | 387–524 | Full progression from insecure stages to password hashing, sessions, HTML output, middleware, password changes and logout |
| 11, Fault-tolerant Workflows | 525–582 | Retry semantics, idempotency, concurrent claims, atomic enqueue, worker failures, shutdown and explicitly omitted policies |

Use: [service engineering](service-engineering.md), [errors/design](design.md), [concurrency](concurrency-and-safety.md), [validation](validation-and-maintenance.md). The final tutorial does **not** implement all stated production guarantees: see the exact [completion gates](source-conflicts.md#service-tutorial-completion-gates), including dropped failed deliveries, absent payload-conflict checking, expiry and lifecycle behavior.

## Official Rust Book

TRPL means *The Rust Programming Language*, by Steve Klabnik, Carol Nichols and Chris Krycho, with Rust community contributions. Entry: [stable Rust Book](https://doc.rust-lang.org/stable/book/index.html). The [complete print view](https://doc.rust-lang.org/stable/book/print.html) supplied all chapter text and code, mapped against its navigation. The downloaded title page specifies Rust **1.97.0 or later** and edition **2024**. This is a source baseline, not an instruction to raise any project's MSRV.

**Complete text coverage:** title, foreword, introduction, every chapter introduction and subsection listed below, and appendices A–G. Extracted section units 1–60 and 61–111 were read in full by the authorized readers; unit 0 is empty. The chapter links are navigation anchors for the analysis, not a restriction to only those excerpts. Additional official API checks resolve teaching simplifications and version changes.

| Chapters | Consulted chapter/section links | Subjects incorporated |
| --- | --- | --- |
| 1–3 | [Cargo](https://doc.rust-lang.org/stable/book/ch01-03-hello-cargo.html), [guessing game](https://doc.rust-lang.org/stable/book/ch02-00-guessing-game-tutorial.html), [data types](https://doc.rust-lang.org/stable/book/ch03-02-data-types.html), [control flow](https://doc.rust-lang.org/stable/book/ch03-05-control-flow.html) | Build versus run, input handling, types, loops and basic semantics |
| 4 | [ownership](https://doc.rust-lang.org/stable/book/ch04-01-what-is-ownership.html), [borrowing](https://doc.rust-lang.org/stable/book/ch04-02-references-and-borrowing.html), [slices](https://doc.rust-lang.org/stable/book/ch04-03-slices.html) | Moves/copies, reference restrictions and borrowed APIs |
| 5–6 | [structs](https://doc.rust-lang.org/stable/book/ch05-01-defining-structs.html), [methods](https://doc.rust-lang.org/stable/book/ch05-03-method-syntax.html), [enums](https://doc.rust-lang.org/stable/book/ch06-01-defining-an-enum.html), [match](https://doc.rust-lang.org/stable/book/ch06-02-match.html), [if let / let else](https://doc.rust-lang.org/stable/book/ch06-03-if-let.html) | Domain data, ownership of fields, optional values, exhaustive cases |
| 7 | [privacy](https://doc.rust-lang.org/stable/book/ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html), [use](https://doc.rust-lang.org/stable/book/ch07-04-bringing-paths-into-scope-with-the-use-keyword.html), [module files](https://doc.rust-lang.org/stable/book/ch07-05-separating-modules-into-different-files.html) | Public boundaries, imports and internal organization |
| 8 | [vectors](https://doc.rust-lang.org/stable/book/ch08-01-vectors.html), [strings](https://doc.rust-lang.org/stable/book/ch08-02-strings.html), [hash maps](https://doc.rust-lang.org/stable/book/ch08-03-hash-maps.html) | Indexing, UTF-8, ownership, entry API and iteration order |
| 9 | [panic](https://doc.rust-lang.org/stable/book/ch09-01-unrecoverable-errors-with-panic.html), [Result](https://doc.rust-lang.org/stable/book/ch09-02-recoverable-errors-with-result.html), [panic decisions](https://doc.rust-lang.org/stable/book/ch09-03-to-panic-or-not-to-panic.html) | Recovery, propagation and legitimate panic contexts |
| 10 | [generics](https://doc.rust-lang.org/stable/book/ch10-01-syntax.html), [traits](https://doc.rust-lang.org/stable/book/ch10-02-traits.html), [lifetimes](https://doc.rust-lang.org/stable/book/ch10-03-lifetime-syntax.html) | Bounds, shared behavior and reference relationships |
| 11 | [writing tests](https://doc.rust-lang.org/stable/book/ch11-01-writing-tests.html), [running tests](https://doc.rust-lang.org/stable/book/ch11-02-running-tests.html), [organization](https://doc.rust-lang.org/stable/book/ch11-03-test-organization.html) | Assertions, filters, unit and external integration tests |
| 12 | [arguments](https://doc.rust-lang.org/stable/book/ch12-01-accepting-command-line-arguments.html), [file input](https://doc.rust-lang.org/stable/book/ch12-02-reading-a-file.html), [refactoring](https://doc.rust-lang.org/stable/book/ch12-03-improving-error-handling-and-modularity.html), [testing](https://doc.rust-lang.org/stable/book/ch12-04-testing-the-librarys-functionality.html), [environment](https://doc.rust-lang.org/stable/book/ch12-05-working-with-environment-variables.html), [stderr](https://doc.rust-lang.org/stable/book/ch12-06-writing-to-stderr-instead-of-stdout.html) | Library/CLI boundary, borrowed results, Unicode limits and diagnostics |
| 13 | [closures](https://doc.rust-lang.org/stable/book/ch13-01-closures.html), [iterators](https://doc.rust-lang.org/stable/book/ch13-02-iterators.html), [I/O refinement](https://doc.rust-lang.org/stable/book/ch13-03-improving-our-io-project.html), [performance](https://doc.rust-lang.org/stable/book/ch13-04-performance.html) | Capture/consumption, readable transformations and measurement |
| 14 | [profiles](https://doc.rust-lang.org/stable/book/ch14-01-release-profiles.html), [documentation and publishing](https://doc.rust-lang.org/stable/book/ch14-02-publishing-to-crates-io.html), [workspaces](https://doc.rust-lang.org/stable/book/ch14-03-cargo-workspaces.html), [commands](https://doc.rust-lang.org/stable/book/ch14-05-extending-cargo.html) | Tooling, docs, re-exports and package boundaries; no publishing authorization |
| 15 | [Box](https://doc.rust-lang.org/stable/book/ch15-01-box.html), [Deref](https://doc.rust-lang.org/stable/book/ch15-02-deref.html), [Drop](https://doc.rust-lang.org/stable/book/ch15-03-drop.html), [Rc](https://doc.rust-lang.org/stable/book/ch15-04-rc.html), [RefCell](https://doc.rust-lang.org/stable/book/ch15-05-interior-mutability.html), [cycles](https://doc.rust-lang.org/stable/book/ch15-06-reference-cycles.html) | Indirection, sharing, runtime borrowing, cleanup and weak edges |
| 16 | [threads](https://doc.rust-lang.org/stable/book/ch16-01-threads.html), [channels](https://doc.rust-lang.org/stable/book/ch16-02-message-passing.html), [shared state](https://doc.rust-lang.org/stable/book/ch16-03-shared-state.html), [Send/Sync](https://doc.rust-lang.org/stable/book/ch16-04-extensible-concurrency-sync-and-send.html) | Ownership and synchronization across threads |
| 17 | [futures](https://doc.rust-lang.org/stable/book/ch17-01-futures-and-syntax.html), [concurrency](https://doc.rust-lang.org/stable/book/ch17-02-concurrency-with-async.html), [coordination](https://doc.rust-lang.org/stable/book/ch17-03-more-futures.html), [streams](https://doc.rust-lang.org/stable/book/ch17-04-streams.html), [traits](https://doc.rust-lang.org/stable/book/ch17-05-traits-for-async.html), [tasks/threads](https://doc.rust-lang.org/stable/book/ch17-06-futures-tasks-threads.html) | Polling, pinning, sequential versus concurrent work, runtime choices |
| 18–19 | [trait objects](https://doc.rust-lang.org/stable/book/ch18-02-trait-objects.html), [state design](https://doc.rust-lang.org/stable/book/ch18-03-oo-design-patterns.html), [refutability](https://doc.rust-lang.org/stable/book/ch19-02-refutability.html), [patterns](https://doc.rust-lang.org/stable/book/ch19-03-pattern-syntax.html) | Composition, representation, transitions and matching |
| 20 | [unsafe](https://doc.rust-lang.org/stable/book/ch20-01-unsafe-rust.html), [traits](https://doc.rust-lang.org/stable/book/ch20-02-advanced-traits.html), [types](https://doc.rust-lang.org/stable/book/ch20-03-advanced-types.html), [callables](https://doc.rust-lang.org/stable/book/ch20-04-advanced-functions-and-closures.html), [macros](https://doc.rust-lang.org/stable/book/ch20-05-macros.html) | Explicit safety boundaries and conditional advanced abstractions |
| 21 | [server](https://doc.rust-lang.org/stable/book/ch21-01-single-threaded.html), [thread pool](https://doc.rust-lang.org/stable/book/ch21-02-multithreaded.html), [shutdown](https://doc.rust-lang.org/stable/book/ch21-03-graceful-shutdown-and-cleanup.html) | Educational limitations, channel lifecycle and worker cleanup |
| Appendices A–G | [keywords](https://doc.rust-lang.org/stable/book/appendix-01-keywords.html), [operators](https://doc.rust-lang.org/stable/book/appendix-02-operators.html), [derives](https://doc.rust-lang.org/stable/book/appendix-03-derivable-traits.html), [tools](https://doc.rust-lang.org/stable/book/appendix-04-useful-development-tools.html), [editions](https://doc.rust-lang.org/stable/book/appendix-05-editions.html), [translations](https://doc.rust-lang.org/stable/book/appendix-06-translation.html), [nightly](https://doc.rust-lang.org/stable/book/appendix-07-nightly-rust.html) | Syntax, trait semantics, formatting/lints and stable/edition distinctions; linked translations were not visited |

## Additional official checks

These are targeted contract/stability checks, not claims of complete reading of the Reference, Cargo Book, Nomicon or standard-library manuals:

- Ownership and representation: [Arc](https://doc.rust-lang.org/stable/std/sync/struct.Arc.html), [RefCell](https://doc.rust-lang.org/stable/std/cell/struct.RefCell.html), [Mutex poisoning](https://doc.rust-lang.org/stable/std/sync/struct.Mutex.html#poisoning), [Drop](https://doc.rust-lang.org/stable/std/ops/trait.Drop.html), [mem::drop](https://doc.rust-lang.org/stable/std/mem/fn.drop.html), [forget](https://doc.rust-lang.org/stable/std/mem/fn.forget.html), [Option representation](https://doc.rust-lang.org/stable/std/option/index.html#representation), [Box::from_raw](https://doc.rust-lang.org/stable/std/boxed/struct.Box.html#method.from_raw), [layout](https://doc.rust-lang.org/stable/reference/type-layout.html), [undefined behavior](https://doc.rust-lang.org/stable/reference/behavior-considered-undefined.html), [c_void](https://doc.rust-lang.org/stable/std/ffi/enum.c_void.html), [unchecked UTF-8](https://doc.rust-lang.org/stable/std/string/struct.String.html#method.from_utf8_unchecked).
- API laws and iteration: [Borrow](https://doc.rust-lang.org/stable/std/borrow/trait.Borrow.html), [Iterator](https://doc.rust-lang.org/stable/std/iter/trait.Iterator.html), [slice sorting](https://doc.rust-lang.org/stable/std/primitive.slice.html#method.sort_by_key).
- Stability: [core Error](https://doc.rust-lang.org/stable/core/error/trait.Error.html), [black_box](https://doc.rust-lang.org/stable/std/hint/fn.black_box.html), [pin macro](https://doc.rust-lang.org/stable/std/pin/macro.pin.html), [never type](https://doc.rust-lang.org/stable/std/primitive.never.html), [associated-type impl Trait](https://doc.rust-lang.org/unstable-book/language-features/impl-trait-in-assoc-type.html), [negative impls](https://doc.rust-lang.org/unstable-book/language-features/negative-impls.html), and specific [release notes](https://doc.rust-lang.org/stable/releases.html) linked in the conflict register.
- Edition and trait boundaries: [unsafe attributes](https://doc.rust-lang.org/edition-guide/rust-2024/unsafe-attributes.html), [unsafe extern blocks](https://doc.rust-lang.org/edition-guide/rust-2024/unsafe-extern.html), [let chains](https://doc.rust-lang.org/edition-guide/rust-2024/let-chains.html), [dyn compatibility](https://doc.rust-lang.org/reference/items/traits.html#dyn-compatibility), [procedural macro diagnostics](https://doc.rust-lang.org/reference/procedural-macros.html), [FFI unwinding](https://doc.rust-lang.org/nomicon/ffi.html#ffi-and-unwinding).
- Cargo: [rust-version](https://doc.rust-lang.org/cargo/reference/rust-version.html), [test targets](https://doc.rust-lang.org/cargo/commands/cargo-test.html), [dependency renaming](https://doc.rust-lang.org/stable/cargo/reference/specifying-dependencies.html#renaming-dependencies-in-cargotoml), [build timings](https://doc.rust-lang.org/cargo/reference/timings.html).

Live stable pages may advance independently of this downloaded Book snapshot. Check each API's stabilization and the project's actual compiler; a current stable API is not necessarily an MSRV-compatible API.

## Cross-source agreement and decision coverage

| Required subject | Convergent evidence | Operational reference |
| --- | --- | --- |
| Ownership, borrowing, lifetimes | ER 8/14–15; RFR 1/3; SP 3–6; TRPL 4/10; ZTP 7/9 | [Design](design.md#ownership-and-borrowing) |
| Structs, enums, traits, generics, patterns | ER 1–7/10/12–13; RFR 2–3; TRPL 5–6/10/18–20; ZTP 6 | [Modeling](design.md#model-valid-states-and-useful-abstractions) |
| Result, Option, context, panics | ER 3–4/18; RFR 4; TRPL 9/12; ZTP 6/8–9 | [Errors](design.md#errors-and-panics) |
| Modules, visibility, APIs, docs | ER 21–24/27; RFR 3/5; TRPL 7/14; ZTP 3/7 | [API design](design.md#modules-public-apis-and-documentation) |
| Collections, strings, iterators, closures | ER 2/8–10; RFR 2/13; TRPL 8/13/19; ZTP 6/9 | [Collections/performance](design.md#collections-text-and-performance) |
| Threads, shared state, async | ER 17; RFR 8/10; SP 6; TRPL 15–17/21; ZTP 10–11 | [Concurrency](concurrency-and-safety.md) |
| Unsafe, FFI, layout and cleanup | ER 11/16/34–35; RFR 9/11; SP 7–8; TRPL 15/20 | [Safety gate](concurrency-and-safety.md#unsafe-and-ffi-decision-gate), [advanced boundaries](advanced-boundaries.md) |
| Measured performance | ER 9/12/17/20/30; RFR 2/6/10; TRPL 13.4; ZTP 9–11 | [Performance](design.md#collections-text-and-performance) |
| Unit, integration and documentation tests | ER 27/30/32; RFR 6; TRPL 11–14; ZTP 3/6–11 | [Validation](validation-and-maintenance.md) |
| Cargo, rustfmt, Clippy, compatibility and dependencies | ER 21/24–26/29/31–32; RFR 5/13; TRPL 1/14/appendices; ZTP 1/5 | [Maintenance](validation-and-maintenance.md#dependencies-and-public-compatibility) |
| Macros, no_std and build boundaries | ER 19/28/33–35; RFR 7/11–12; TRPL 20 | [Advanced boundaries](advanced-boundaries.md) |
| Service correctness and durable effects | ZTP 3–11; RFR 4/8/10; TRPL 9/17/21 | [Service engineering](service-engineering.md) |

Across sources, type invariants, deliberate ownership, caller-oriented errors, encapsulation, behavioral tests and measured optimization converge. Differences are resolved by contract and context, not votes: pedagogical versus deployable code, views versus retained ownership, recoverable variants versus diagnostic context, and historical syntax versus the supported edition/MSRV. See [source conflicts](source-conflicts.md).

## Boundaries with defined handling

No required text-reading task is deferred. The corpus does not establish every native ABI, hardware/real-time requirement, unsafe provenance question, runtime-specific cancellation/fairness guarantee, current dependency vulnerability, licensing decision, or comprehensive security policy. Those are project inputs, not omissions to fill with invented rules. The [resolution procedure](validation-and-maintenance.md#resolve-missing-or-conflicting-evidence) requires evidence, a compatible safe fallback, or an explicit unmet prerequisite for the dependent work. The skill contains no implementation placeholders.

Metadata not present in the supplied PDFs remains recorded as unidentified; no edition or publication date was guessed. Figure pixels and source listing execution are validation limits described above, not evidence of inaccessible text.

## Artifact verification

Verification completed on 2026-10-17:

- The installed `skill-creator/scripts/quick_validate.py languages/rust` returned **Skill is valid!** Metadata was also checked for consistency with the entry point.
- All **262 Markdown links** across the skill and root README were checked: **68 local paths/heading anchors** resolved; **194 remote link occurrences** used HTTPS and the exact permitted host. This is not a claim that every remote fragment was independently fetched.
- `rustdoc --test languages/rust/references/examples.md --edition=2021` and the corresponding `--edition=2024` command each passed **3/3 tests** on rustc **1.96.0** (ac68faa20, 2026-05-25).
- An independent agent applied the skill in an isolated, dependency-free parser project. Five behavioral tests covered whitespace/empty input, preserved order, original line numbers, invalid values and numeric bounds. The original implementation failed four tests; the completed implementation passed **5/5** with `cargo test --offline`, and `cargo fmt --all -- --check` passed. Public API, edition 2021 and declared MSRV 1.70 were preserved. The actual 1.70 toolchain was unavailable and was not installed; this was correctly reported as unverified.
- A separate read-through checked the entry point, all eight reference files and UI metadata for contradictory instructions, unsupported guarantees and ambiguous decision paths. Its concrete finding—an example-testing command without an edition—was corrected. This review and one forward test do not prove behavior in every Rust domain.

Reproducible structural and example commands are in the root README. No full source-book listing suite, older-compiler matrix, arbitrary target matrix, external service integration or comprehensive visual PDF audit was run. The skill makes no claim that those checks passed.
