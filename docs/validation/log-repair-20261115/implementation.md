# Log repair implementation — 2026-11-15

Authorized scope: repair proven failures in ox-run-52R94IoD without changing
acceptance criteria, removing checks, rotating logs, downloads or publication.
Owner: ec_implementador for ox-ui Rust sources and assigned governance code.
Existing unrelated dirty work is preserved; before/*.bin records session inputs.

Plan: fix Clippy findings preserving presentation and persistence behavior;
preserve eager worker startup before join in concurrent tests. Confirm OpenGrep
finding and static-review drift, propose dispositions before changing registries.
Criteria: existing Clippy -D warnings passes; existing relevant tests pass;
unchanged serialized format and rejection/concurrency contracts.

Skill actually consulted: .codex/skills/rust/SKILL.md (unversioned entry), with
references/concurrency-and-safety.md for eager worker startup and ownership.
Toolchain 1.99.1, edition 2024, MSRV 1.99, Iced 0.14.0 unchanged.
Focused checks: cargo fmt --check, offline Clippy and ox-ui tests.

Pending: independent review and validation, scanner/governance investigation.

## Implemented and observed

Rust: replaced bounded casts with checked conversions (unchanged serialized bytes),
const helpers/method references, eager array::map for both worker pairs;
separated welcome intro/recent views, welcome controls and input fixture helpers.
No suppression or lint-policy reduction. All original assertions remain.
OpenGrep: test now loads the fixed preimage through SourceFileLoader after a
literal SHA256 assertion (6df3b403...). Dynamic code remains a deliberate
repository-owned historical oracle, no externally supplied source.

Exact final Clippy command, cwd application/:
`CARGO_HOME="$PWD/../.cache/ox/cargo-home" CLIPPY_CONF_DIR="$PWD/../scripts/config/native/clippy" cargo clippy --workspace --all-targets --all-features --locked --offline --keep-going -- -W clippy::all -W clippy::pedantic -W clippy::nursery -W clippy::cargo -D warnings`: exit 0.
`cargo fmt --all -- --check`: exit 0.
`CARGO_HOME="$PWD/../.cache/ox/cargo-home" cargo test --offline --locked -p ox-ui`: exit 0 (see ox-ui-tests.log).
`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools/governance/tests -p test_instruction_validator.py -v`: exit 0.

Toolbox scanner observations use original per-check input inventory copied to
/tmp/ox-log-repair-scanners, current file bytes and native config. Commands and
raw diagnostic/results retained in scanner-observation/. Initial sandbox run
failed on central execution receipt write (EROFS); approved escalated retry
executed scanners, no downloads or maintenance. OpenGrep exit0/zero results;
Ruff exit1/16 findings; Bandit exit1/5 findings. These preceded final import
ordering and other writers: only OpenGrep behavior initially observed, results
need affected rerun after stabilization.

## Static-source review proposal for independent confirmation

Observed registered drift: package-ox.py adds explicit governance-copy receipt
into both archive content and manifest/current comparison; no shell subprocess,
network, secret or XML boundary introduced. validate.py adds no code execution:
contained path rejects symlinks before resolution; complete feature selection,
convergence/CLI checks add argument validation. Historical validator bytes remain
preserved. Registries must bind final bytes after independent review, not simply
recalculate hashes to reuse prior scan.

Bandit five new B404/B603 observations are imports and fixed argv execution in
new contract fixtures. validator.cli uses [sys.executable, fixed ROOT ENTRY,
--root, test TemporaryDirectory, test-only explicit args], capture_output/text,
check=False asserting expected rejection, no shell. Routes similarly uses
sys.executable + fixed validator/script and temporary fixture path. These may
receive occurrence-specific baseline entries under exact source hashes only
after final file review; no blanket subprocess/rule disable. Baseline/pins
not edited by this writer; ownership returns to coordinator/governance writer.

Documentation disposition: inspected application Cargo/toolchain and Rust
contracts; lint-only decompositions preserve presentation, version1 recent-store
format, exclusive creation and existing failure contracts. No new product
behavior to document. Coordinator must update affected feature evidence and
state because source inputs changed; no inherited product acceptance claimed.

## Closure successor (earlier pending notes are historical)

Independent review is complete with no open findings. The initial SourceFileLoader described above is superseded by VerifiedSourceLoader, which compiles exactly its captured/verified bytes; source/cache negatives passed independently. Final frozen-scanners contains current-input Ruff/Bandit/OpenGrep native/parser exit0. See report.md, independent-review.md and independent-validation.md for scoped final acceptance and limitations. Previous scanner/source manifests remain historical observations; they were not renewed.
