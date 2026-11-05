# Robustness and persistence preparation — 2026-11-05

## Current state and scope

Inspected root instructions, project/constitution/workflow/evidence/architecture,
F0 boundary and persistence ADR, existing persistence artifacts and affected
Engine/controller/desktop/runtime/storage/contracts/tests/evidence. Rust/Iced,
controlled local task and independent verification exist. Engine observations and
controller history remain in memory; ox-storage contains only boundary types.
Plugin Host is an independent API, not desktop integration; no real agent exists.
F0 historical closure was recorded for the adopted local envelope, not persistence.
The source repair changes inputs of that closure: current GUI/performance acceptance
is UNVERIFIED pending reobservation, without deleting historical success or failures.

Full route: reuse persistence and affected verification/UI/F0 artifacts. Current
request authorizes robustness repair and preparation only. No commits/staging,
candidate implementation, dependency update, network agents or integration occurred.
Extensive preexisting tracked/untracked work was inspected and retained. Before
copies preserve touched feature records/Engine/tests/project/ADR/contracts. No
historical operational logs were overwritten. Executed project commands exist in README/project;
Rust 1.99.1, edition 2024, declared floor 1.99, current Cargo.lock unchanged here. Scope and contract clarification reside in affected feature artifacts; project.md and architecture/contracts.md were kept byte-identical to their starting state to preserve their independent documentary guards.

## Expected results and before/after observations

The user contract and regression test defined the desired result before the repair:
FIFO without writer must not hold capture/evaluate, unsupported evidence must not
approve/launch, direct child cleanup must remain owned on errors. Frozen defective
Engine is before/application/crates/ox-verification/src/engine.rs.bin. New regression
source is application/crates/ox-verification/tests/engine.rs.

| Criterion | Method / observed input | Before | After / state | Artifact and limitations |
|---|---|---|---|---|
| Capture and evaluate FIFO refusal | cargo test --locked -p ox-verification special_input_does_not_block -- --nocapture; real mkfifo, own temp directories, separate test processes, 2 s external watchdog | Both evaluate and execute blocked; harness killed/reaped both; exit101 | Both return successfully in the fixed full suite; unsupported execute error/zero observations, evaluate NotVerified: APPROVED | fifo-before.log, workspace-test-unrestricted.log. Watchdog is a regression detector, not adopted filesystem SLO. No stuck process was left alive; defective FIFO directories can remain in /tmp |
| Post-capture unsupported input | Test-only shell replaces own candidate with FIFO, exits0 | No prior live run claimed | Observation retained, current FIFO UNVERIFIED; restored regular bytes INCONCLUSIVE because post-capture absent: APPROVED | post_capture_fifo_is_incomplete_and_timeout_reaps_real_child in workspace log. Shell subprocess is controlled test setup, not descendant supervision guarantee |
| Regular/missing/special semantics | Regular fixture, regular symlink, directory, /dev/null, absent path; all prior verdict tests | Original tests/source preserved | Regular/symlink approve only after observation; absent/special never approve; five states retained: APPROVED | nonregular_missing_and_regular_symlink_inputs and existing tests. No arbitrary pseudo-filesystem or concurrent regular-content atomicity claim |
| Error cleanup ownership | Archived cancellation branch fault model: kill error then try_wait error; after: injected poll/kill/wait faults against private ChildOps boundary | Model returns poll error, omits wait, loses kill error | Cleanup attempts poll/kill/wait, retains primary kind/message plus all diagnostics, retries unconfirmed ownership: APPROVED for injected schedule | cleanup-before.rs/log and 2 ownership unit tests. All OS errors simulated, not observed failure of a real kill/wait syscall. Model copies archived branch, not a live old-process leak |
| Real cancellation and timeout reap | Oracle readiness PID marker; cancel flag, or 500 ms supervision timeout; /proc PID absence after return | Existing cancellation test retained | Cancelled/TimedOut remain non-approval and direct child reaped: APPROVED | cancellation_after_oracle_ready... and post_capture_fifo... in workspace log. /proc observation is Linux-specific; no descendant/isolation claim |
| UI caller Refresh/Verify | Real controlled task -> approve -> replace result with FIFO -> Controller Refresh and Verify | Source review: Refresh calls evaluate via worker; Verify has a metadata precheck | Refresh UNVERIFIED, Verify visible error, retained history: APPROVED at controller level | fifo_result_refresh_and_verify_cannot_approve; no actual rendered UI observation |
| Current UI response/close/display | desktop source review: worker owns Controller mutex; update/view do not capture; close sets cancel and waits Done | Historical F0 graphical matrix identified by old sources | UNVERIFIED for new build | No new X11/Wayland rendered or close observation, no performance rerun. T903 in affected features. API tests cannot accept this criterion |
| Persistence AC-01..07 | Source/spec review only, protocol prepared | UNVERIFIED | UNVERIFIED | No candidate/store/restart/backup/migration/GUI integration experiment |

Capture checks pathname metadata, uses Linux O_NONBLOCK (0o4000) and checks the
opened handle before reading. This prevents the reproduced FIFO wait and refuses
unsupported handles, including a FIFO substituted before open. It is not a complete
concurrent-file-swap defense. Concurrent regular-file changes, network/malfunctioning
filesystem metadata/open/read and pseudo-regular devices are not universally bounded.
Supported evidence is ordinary local regular files; regular symlinks remain supported.

Engine guard owns every post-spawn path. Normal try_wait(Some) marks reap observed;
poll errors run cleanup preserving original error; timeout/cancellation run cleanup
before terminal outcome. Cleanup tries poll, kill and wait even after errors. Errors
are appended, not silently discarded; if reap stays unconfirmed Drop retries and
logs failures to stderr. Persistent OS failures cannot guarantee successful bounded
reap; wait after failed kill may block until natural exit. Unwinding has the guard;
abort/SIGKILL does not. Post-capture occurs after the direct child is reaped.
Runtime caller has its existing Drop cleanup, and controller verifies on a dedicated
worker. No Runtime redesign or new process engine was introduced.

Cancellation is cooperative, observed before spawn and during supervision, not a
filesystem interrupt. Refresh has no subprocess to kill. Closing waits for the worker
and therefore can wait for filesystem calls; no universal ten-second close promise.
Subprocess deadline, cancellation flag and I/O limits remain distinct.

## Checks and limits

- build/check/fmt/Clippy: passed, logs build.log/check.log/fmt.log/clippy.log.
- cargo test --workspace --locked: initial sandbox run failed five Unix socket
  Plugin Host tests with PermissionDenied; workspace-test.log retained. Authorized
  unrestricted rerun passed; workspace-test-unrestricted.log. Six graphical tests
  ignored as designed; no claim that they ran. Engine: 12 integration tests plus
  two injected ownership unit tests; UI controller: four integration tests. A final error-wrapper refinement retains the original io::Error as the error source, including its raw OS detail. final-focused.log and final-clippy.log reobserve both affected packages and lint the final build; the workspace log precedes only this refinement.
- Initial probe setup used a wrong relative path; the filtered run executed zero
  tests and is excluded from evidence. The actual defective run is fifo-before.log.
- rustc --edition 2024 cleanup-before.rs -o /tmp/ox-cleanup-before-20261105 followed
  by that owned binary: passed the defective-branch model assertion, cleanup-before.log.
- Governance check outcomes are in governance.log and its recorded run/results.json;
  final validator output is in final-sdd-02.log and the final governance rerun. Governance checks do not
  accept product behavior. Initial checks failed because changed shared documents and old input references invalidated preservation guards. Shared documents were restored byte-identically; matching historical bindings now point to exact archived preimages, without changing hashes. final-check-ox-02.log passes; initial failures remain in governance.log.

No graphical/performance acceptance is transferred to the changed Engine. Existing
history budget and current code remain bounded but new measurements were not made.
No real permission-denied filesystem or real ENOSPC storage run was claimed.

## Prepared experiment and decisions

The existing persistence feature's experiment-protocol.md specifies logical identity,
immutable provenance, durable intent/effect/ack boundary, uncertain recovery,
idempotency/conflict, five-state revalidation, transactions/corruption, migration,
backup/restore, writer exclusion, UI error/resource contract. E01..E08/AC-01..07
remain unchanged. It specifies corpus sizes, repetitions/order, observed XFS target,
barriers, allowed proposed faults, metrics and elimination before speed. Numerical
limits are proposals, not adopted requirements. Primary technical sources are linked
there with version/applicability limits; no engine was evaluated or selected.

D1 placement is already adopted; do not request it again. D2 contract/failure envelope,
D3 disposable paired experiment (including experimental UI shell), D4 operational
parameters/fault permissions and D4-deps isolated dependency freeze need maintainer
decisions. Native engine source ID remains a mandatory pre-run freeze review. D5
technology follows results; D6 product integration is separately authorized later.
Next after approval: complete frozen hand-authored logical manifests and isolated
lock/source/config review, then implement/run only the approved disposable protocol.
The graphical/performance T903 work on the robustness build is independently pending.
