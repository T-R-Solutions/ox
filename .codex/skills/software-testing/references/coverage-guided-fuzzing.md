# Coverage-guided fuzzing of a real target

Use for a parser, codec, native boundary or similarly broad hostile-input surface
when coverage-guided exploration fits the risk. Generated inputs still need an
independent oracle; more executions do not establish correctness.

## Establish the harness contract

Identify the actual entry point, accepted representation, meaningful states and
observable failure: memory fault, violated invariant, wrong result, resource excess
or differential disagreement. A no-crash oracle misses semantic errors. A round
trip alone can let two mutually wrong operations agree.

Discover the destination project's language, toolchain, target and existing engine.
Use supported instrumentation and sanitizer combinations for that configuration;
check current engine documentation before selecting flags. Instrument the code
under test, not merely the driver. No specific engine or new dependency is mandatory.

Make the driver invoke and observe the intended operation. Inspect filtering,
early returns, swallowed failures and unreachable parser branches. Reset relevant
state between inputs, control nondeterminism and join owned work. Isolate file,
network and credential access; arbitrary input must not trigger real external effects.

## Explore within a reproducible budget

1. Seed valid and malformed representatives and important boundaries. Use a
   dictionary or structured generator when raw mutation cannot reach deeper states.
   Record corpus provenance and avoid private production inputs without authority.
2. Define time, memory, input-size, output and concurrency limits from the test's
   purpose. Record revision, build options, engine/version and dependencies.
3. Observe coverage of meaningful target paths, rejected inputs and execution cost.
   Confirm a known reachable fault or invalid result can be detected in an isolated
   version. A driver returning before the parser is insufficient even if runs finish.
4. Save the exact failing input and configuration. Reproduce outside the fuzz loop,
   minimize while preserving the same failure, and distinguish target defects,
   harness errors, environment failures and out-of-contract cases.
5. Turn a confirmed defect into a readable regression with its oracle; retain a
   minimized input/corpus case when useful. Verify the repair and continued reach.

Report budgets, relevant paths reached, findings and unobserved states. A testing
build that relaxes checks must remain separate from production artifacts. Sanitizers
and fuzzing cover their configured scope, not all undefined behavior or protocols.

Basis: *Building Secure and Reliable Systems*, physical 313–338; *Effective Rust*,
item 30, and *Rust for Rustaceans*, chapter 6. The official
[libFuzzer target/corpus guidance](https://llvm.org/docs/LibFuzzer.html) supports
the harness constraints; adapt mechanics to the selected engine rather than copying
LLVM flags into unrelated platforms.
