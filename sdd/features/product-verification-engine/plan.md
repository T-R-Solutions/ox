# Plan: product-verification-engine

Full route under the maintainer’s sequential local-delivery authorization.
D-01 / R-01: In-memory engine with explicit local CommandSpec and ExitCode oracle. No generic natural-language approval or self-reported pass API. Engine creates immutable observations only from spawned direct-child exit, with criterion id/description/oracle/command and before/after input bytes. Compare bounded exact bytes rather than introducing a hash dependency; no cryptographic identity/authenticity claim. Automatically include executable; caller supplies nonempty complete dependency list (max 8 + executable, total <=32MiB, file <=16MiB), max32 observations and max32 advisory completion claims. Absolute paths and explicit current directory; inherited OS environment is recorded as an uncontrolled limit, no remote-service authorization. Deadline >0 <=10s; timeout is INCONCLUSIVE, missing/stale evidence UNVERIFIED, wrong exit REJECTED, matching exit APPROVED only with stable inputs. Any current failure dominates a current pass until a changed-input rerun; prior failure retained. NOT APPLICABLE needs explicit nonempty rationale and is never APPROVED. Criteria with absent paths are UNVERIFIED; content/oracle/id change invalidates dependent results. No persistence, production evidence authenticity, dependency discovery or sandbox. Direct child only, stdout/stderr unavailable because this oracle uses exit status; no claim to preserve process output. Fixture independently reads supplied candidate bytes and returns 0 only for literal accepted content, enabling controlled fault injection. Completion notes are advisory and cannot create observations.

Primary skill: .codex/skills/autonomous-verification-engineering/SKILL.md; bridge sdd/chain/autonomous-verification-engineering.md, version 1. No semantic skill version; SHA-256 in skills.json.
Supporting rust skill (same path under .codex/skills/rust/SKILL.md, bridge version 1) addresses safe Rust API and bounded ownership.
Implementation: application/crates/ox-verification/src/engine.rs; oracle: application/crates/ox-verification/tests/engine.rs.
T001 specifies, T002 implements, T003 tests, T004 records acceptance.


## Robustness successor — 2026-11-05

D-ROBUST / R-ROBUST: same in-memory five-state contract; reject nonregular evidence
before read, open with Linux O_NONBLOCK then check opened handle. Metadata does
not prevent concurrent swaps or bound filesystem I/O. Deadline covers child
supervision; cancellation/close are cooperative. Direct-child guard owns cleanup
through errors/unwind, preserves primary error kind/message and appends cleanup
failures. Drop retries unconfirmed reap and emits diagnostic on failure; wait can
block after kill failure. No descendants/OS isolation guarantee. No UI layout change.
Primary for this repair: .codex/skills/rust/SKILL.md, sdd/chain/rust.md bridge 1,
no declared semantic version; concurrency-and-safety.md consulted for fallible
cleanup/RAII. Contribution: explicit ownership and error paths. Edition 2024,
MSRV 1.99, pinned 1.99.1; no dependency changes. Full route due to uncertain
cleanup/contract limits, affected feature reused. Current tests/report and input
manifest: docs/validation/robustness-20261105/. GUI/F0 reobservation remains pending.
