# Validation and maintenance

## Establish the project contract

Inspect the affected manifest and workspace, including inherited `edition`, `rust-version`, dependencies, resolver, feature definitions, targets, and custom profiles. Read the toolchain file, CI matrix, build scripts, and repository commands. Follow the build system in use; do not create a Cargo workspace solely to validate code managed another way.

Record separately:

- The language edition and MSRV promised to users.
- The development toolchain and installed validation tools.
- The production and CI targets and supported feature configurations.
- The runtime/platform requirements, including `no_std`, allocation, native libraries, and service fixtures where applicable.

Edition, compiler version, and dependency versions are different constraints. Check stabilization of new syntax and APIs against the MSRV; use that compiler for a meaningful compatibility check when available. `rust-version` declares support but does not prove it. Missing MSRV information should be reported as unknown rather than replaced by the local or latest stable version.

Sources: ER Items 21, 24–26, 31; RFR ch. 5; TRPL [editions](https://doc.rust-lang.org/stable/book/appendix-05-editions.html); Cargo's [rust-version](https://doc.rust-lang.org/cargo/reference/rust-version.html).

## Resolve missing or conflicting evidence

Use this procedure whenever a recommendation depends on a fact not established by the project or these sources:

1. Identify the exact decision and required fact: for example an API's stabilization version, a task handle's cancellation semantics, or who frees a foreign pointer. Consult applicable instructions, manifests, CI, callers, tests, and the installed version's documentation/source. Evidence must match the version, feature set, target, and operation involved.
2. Separate intended policy from observed behavior. A test may describe an existing bug; an installed compiler is not a support promise. Reconcile conflicting project documents with the task's acceptance criteria before changing a public contract.
3. If a missing fact does not affect the change, preserve the established implementation and state the limit in the report. If the fact matters but a simpler safe implementation avoids depending on it, choose that implementation and explain the cost.
4. If the change depends on an unresolved safety, security, compatibility, or domain requirement and no valid fallback exists, stop that affected change, identify the missing contract and ask a targeted question or request the necessary evidence. Continue independent authorized work. Do not ship a guessed invariant, a placeholder, or a claim that the affected requirement is complete.
5. Close each material decision with the chosen behavior, evidence or explicit project requirement, and a validation result. A failed required check means the affected requirement is not complete; unavailable optional checks are reported as unverified, not silently counted as passed.

For an undocumented MSRV, preserve the edition/toolchain and avoid introducing a newer requirement without evidence. If the proposed feature or dependency requires establishing a support floor, resolve that policy before adopting it. Do not write a new `rust-version` from the local compiler number. When no project commands exist, choose the smallest commands supported by the actual build entry point and record them; do not add unrelated tooling.

For research performed under this skill's source restriction, only HTTPS on the exact host `doc.rust-lang.org` is allowed; check redirect destinations before following. Local installed crate sources remain usable. If essential external contracts are unavailable within the permitted evidence, follow step 4. This is a defined decision outcome, not permission to invent evidence or an instruction to ask on every routine edit.

## Select checks by impact

Use repository commands first. The commands below are alternatives to adapt after identifying the package and configuration; they are not a mandatory batch to run on every change.

| Change or question | Useful validation | What it does not establish |
| --- | --- | --- |
| Formatting | Existing format check; commonly `cargo fmt --all -- --check` for a workspace | Behavior or compatibility; broad formatting can also flag pre-existing files. |
| Types and local compilation | `cargo check -p <package>` with relevant features/target | Linking, test execution, or runtime behavior. |
| Behavior change or bug fix | Focused regression tests, then the affected suite with `cargo test -p <package>` | Unsupported feature combinations or unexercised failure paths. |
| Public API or examples | Integration tests, `cargo test -p <package> --doc`, and the existing documentation build | Source compatibility for every downstream consumer. |
| Lints | Existing Clippy command, or `cargo clippy -p <package>` with the affected target/feature scope | Correctness, absence of undefined behavior, or a reason to adopt every stylistic suggestion. |
| Dependency, feature, or target changes | Relevant CI configurations, including no-default-features or explicit feature sets where supported | `--all-features` does not cover configurations with features disabled and may enable incompatible choices. |
| MSRV-sensitive changes | Existing MSRV job or `cargo +<msrv> check/test ...` on an available supported toolchain | A successful latest-compiler build is not an MSRV check. |
| Unsafe/concurrent code | Boundary/error-path tests plus configured Miri, model checking, fuzzing, or sanitizers when relevant | These tools are not a complete proof and may require a separate toolchain. |
| Performance claim | Representative optimized benchmark/profile against a baseline | A debug timing or single small input does not establish general improvement. |

Use existing lockfile and network policies, including `--locked` or `--offline` when appropriate. A cache miss in offline mode is an environment limitation, not proof of a code defect. Do not upgrade dependencies or install a nightly toolchain merely to make an optional check available.

Respect target selection: `--all-targets` is useful when supported but is not a substitute for a documentation-test run. Compiling an example is not executing its `main`; use the existing example runner or `cargo run --example <name>` when its behavior needs validation. Inspect custom harness settings. Benchmarks can use a stable custom harness; the unstable built-in `#[bench]` facility does not make all benchmarking nightly-only.

Resolve new warnings according to existing policy. Do not introduce `-D warnings` globally as part of an unrelated fix. A narrow justified lint allowance can be correct; broad suppression to avoid understanding a diagnostic is not.

Sources: ER Items 29–32; RFR ch. 6 and 9–10; TRPL [tests](https://doc.rust-lang.org/stable/book/ch11-00-testing.html), [tools](https://doc.rust-lang.org/stable/book/appendix-04-useful-development-tools.html), [profiles](https://doc.rust-lang.org/stable/book/ch14-01-release-profiles.html); Cargo's [test target semantics](https://doc.rust-lang.org/cargo/commands/cargo-test.html).

## Write tests that can detect the defect

- Test observable behavior and invariants, including expected failures and boundary values. For a bug fix, add a regression case that fails for the original reason when practical. Do not merely mirror implementation steps.
- Put focused unit tests near the implementation when private state or helpers matter. Use integration tests as external users of the public API. `#[cfg(test)]` helpers in the library are not automatically available to a separately compiled integration-test crate.
- Test CLI argument, exit-status, stdout and stderr contracts through the executable when they change, even with a thin `main`. Use documentation tests for promised usage. For `compile_fail` cases, confirm the intended restriction causes failure rather than an unrelated syntax/import error. Use `should_panic` only for an intentional panic contract and constrain the expected reason when useful.
- Keep parallel tests independent: isolate temporary paths, ports, database state, environment changes, and global initialization. Avoid timing sleeps as synchronization. Serial test execution alone does not isolate background threads or other processes. Use `args_os`/`var_os` when operating-system strings need not be Unicode; environment mutation is a process-wide concern and can be unsafe on the project edition. Use controlled barriers/events or the runtime's testing facilities where available.
- Use property tests or fuzzing when the input space and invariants make them valuable, especially parsers and unsafe boundaries. Preserve meaningful failing inputs as regressions, including random seeds or minimized cases. Generated samples do not prove all possible inputs and do not replace explicit boundary tests. Add a testing dependency only when the benefit justifies it.
- For service boundaries, test through the actual protocol and configuration when that integration is at risk. See [service engineering](service-engineering.md).

Sources: ER Items 30 and 32; RFR ch. 6; ZTP ch. 3, 6–7 and 11; TRPL [test organization](https://doc.rust-lang.org/stable/book/ch11-03-test-organization.html).

## Dependencies and public compatibility

Prefer an existing dependency or standard facility that satisfies the requirement. Before adding a crate, identify the missing capability and assess its relevant feature surface, MSRV, target support, transitive cost, maintenance, and the project's license/security policy. The local books do not establish any crate's current maintenance or vulnerability status. Do not infer it from a historical recommendation.

Scope development/build/runtime dependencies correctly. Enable only required features and retain the existing resolver and lockfile policy unless the task requires changing them. Avoid broad `cargo update` during an unrelated implementation. Review manifest and lockfile diffs together when a dependency change is intended.

Treat feature combinations as part of the supported interface. Additive features generally compose more predictably; test important disabled/default/explicit configurations according to the project's support contract, not every mathematical combination indiscriminately. Libraries must consider the versions that consumers may resolve, not only one local lockfile. A workspace lockfile can contain multiple versions when constraints require them; renamed dependencies can deliberately select different versions. A lockfile does not pin native compilers, environment, external services, or every build input. `cfg!` chooses a boolean, so both ordinary branches must still type-check; use conditional compilation for unavailable APIs. Inspect workspace default members rather than assuming an unqualified command checks every package.

For public changes, review downstream source usage, trait bounds/implementations, auto traits, enum exhaustiveness, error matching, and exposed dependency types. Record required migration or versioning consequences. Do not publish, change release policy, or raise the MSRV as an incidental validation step.

Sources: ER Items 21–28; RFR ch. 3 and 5; TRPL [Cargo workspaces](https://doc.rust-lang.org/stable/book/ch14-03-cargo-workspaces.html). For supply-chain status, licensing decisions, and specialized compatibility contracts not established by these books, apply the evidence-resolution procedure above. Historical crate lists are not current endorsements.

## Report evidence precisely

List the actual toolchain, configurations, commands, and outcomes that matter to the change. State missing tools, unavailable service fixtures, skipped targets, and untested MSRV explicitly. Separate pre-existing failures from regressions when evidence allows. Stop broadening checks after the required scope passes unless a new change or unresolved concern justifies more work.
