# Plan: product-local-task-ui

Full route. Product implementation follows governance-reconciliation AC-01..04.
D-01 / R-01: Validate a manually entered existing directory by canonicalization
and directory enumeration on a worker. Test writable access by exclusive attempt-
directory creation at Start, before spawning; avoid creating probe files on selection.
Do not equate lexical absolute paths with access or confinement. Reject unreadable
paths before launching. Each attempt owns a newly created directory; never reuse,
overwrite or recursively delete a preexisting path. Keep generated artifacts on exit.
D-02 / R-02: One active task and one verification at a time. Correlate session,
task, attempt, workspace generation and verification run. Reject duplicate actions
and stale result messages. Disable workspace changes while work is active.
D-03 / R-03: Adapter produces a result in its attempt directory using create_new.
Independent oracle compares the result against a controller-created request carrying
the attempt identity; it must not approve unrelated sample content. Bind request,
result, adapter and oracle bytes in verification inputs. Separate process success,
task result availability and criterion approval. Provide controlled good/bad/failure/
hang scenarios without a command text field.
D-04 / R-04: Dedicated worker owns Runtime and Engine; no blocking spawn, wait,
snapshot or verification in update/view. Reuse the existing maximum ten-second
process deadline and snapshot/history bounds; these are fixture bounds, not latency
SLOs or OS resource isolation. Close stops admission, requests task cancellation,
waits for worker cleanup and observed child exit; in-flight verification finishes
under its existing deadline before exit. Forced external termination is outside
this graceful-close guarantee. No child descendants are introduced.
D-05 / R-05: Explicit Refresh action re-observes inputs off-thread and timestamps
the observation. Display approval as of that observation, never as continuous
monitoring. Detected change removes current approval and retains historical evidence;
Verify again creates a new observation. Restart loses in-memory history and starts
UNVERIFIED; retained files alone do not restore acceptance.
D-06 / R-06: Real Wayland interaction and protocol/backend/process diagnostics are
required for graphical acceptance; domain calls do not replace it. Keep X11 checks
separate. Preserve failures and request human observation if automation is blocked.

Primary skill: .codex/skills/iced-engineering/SKILL.md, bridge
sdd/chain/iced-engineering.md version 1: generation-aware messages, worker ownership,
responsive view and actual graphical interaction. Supporting .codex/skills/rust/SKILL.md,
bridge sdd/chain/rust.md version 1: safe process ownership and bounded shutdown.
Entries have no semantic version; consulted content SHA-256 is in skills.json.

T001 specifies; T002 reconciles governance; T003 implements; T004 validates;
T005 records acceptance. Plans are not evidence of implementation.

## Implementation decisions

D-07 / R-07: Controller in ox-ui owns Engine; each admitted operation gets one named
OS worker, with a oneshot result into Iced Task. The UI never locks the controller.
At most one operation is admitted; cancellation is an AtomicBool observed by Runtime
polling every 10ms (fixture polling cadence, not a responsiveness SLA). Runtime owns
and reaps its child even on worker unwind. A worker completion means process work
is over; graceful close waits for that message. Verification completes under its
existing 10s deadline. Channels disappearing yield UNVERIFIED, never approval.
Session nonce in artifact identity uses current epoch nanoseconds; Runtime session
uses app PID, with task=1 and the same monotonic attempt. These are distinct namespaces
within the in-memory controller; neither claims global persistent identity.
Engine retains at most 32 observations across workspace selections; attempt results
remain in exclusive directories, with no deletion. No file picker dependency added.

D-08 / R-08: request.txt contains ox-task-v1:<session>:1:<attempt> and newline.
local-task creates result.txt exclusively, echoing identity plus result=42 newline
(or controlled result=41). task-oracle independently reconstructs both expected
byte sequences from the immutable check argument. Snapshot inputs include request,
result, producer binary and oracle binary. Modes are a closed enum at the UI boundary.
Real fixture processes are trusted local binaries, not confinement enforcement.

D-09 / R-09: Graphical human session permits up to 600s for the multi-step checklist
(ten prior 60s interaction slots); each task/oracle still has the existing 10s bound.
The supervisor timeout is not successful shutdown. At the maintainer request to
photograph results, subsequent manual sessions allow 1800s; this extends only the
human observation window, never the task or verifier deadline. Record exact human replies and
protocol/exit diagnostics independently. X11 input interference remains separate.

D-10 / R-10: Final X11 harness uses the existing 15s observation bound to wait
for actual pointer placement (still fails when placement is not observed), preserves
80ms event settling and pointer restoration, and uses an alphanumeric relative
fixture path with app cwd=/tmp to avoid layout-dependent slash synthesis. This
changes only the harness, not application input or assertions. The captured run
proves all three scenarios; main-session XTEST remains outside that result.

D-11 / R-11: User photographs exposed an unclear missing-evidence error after
verification of a timed-out attempt. Retain the failure and show attempt/path and
explicit no-approval guidance. Display small recorded input bytes in history so
current changed files are not confused with prior observations. Regular Cargo
tests, final X11 frames and subsequent native human replies validate the change.


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


## T903 revalidation plan — 2026-11-05

Authorized full-route resumption of D-ROBUST/R-ROBUST, REQ-05 (UI feature uses its corresponding requirements). Before trials: preserve exact feature records in docs/validation/t903-20261105/before and identify current product bytes. Primary selected/read/used skill: .codex/skills/performance-engineering/SKILL.md, no declared version, sdd/chain/performance-engineering.md bridge 1. Contribution: workload equivalence, raw samples and measurement boundaries. No delegation.

Reuse adopted f0-boundary-20261102 and decision-proposal contract unchanged: separate native Wayland/X11, scales 1/1.5/2, logical 640x480/900x700. Per cell 3 warmups +20 response/client samples, max response 120 ms, full-corpus client draw/present-return 125 ms including history counterexample, sampled GUI RSS 64 MiB, three 10-second idle windows <=5% one core. Backend execution/verification <=50 ms, cancel-to-direct-exit <=100 ms (3+20); harness RSS32 MiB; large retained history128 MiB with prelaunch refusal, stress RSS256 MiB in three runs. Never infer scanout from client timing.

Build a fresh disposable diagnostic tree from current sources, port only preserved instrumentation, size selectors and input bridge; identify all deltas. Run serial real isolated compositor interaction; correlate screenshots with artifacts/process exit. Add own FIFO-without-writer Refresh/Verify journeys and held verification/close observations. Preserve failures; absent interaction/oracle leaves gates UNVERIFIED. No product contract, dependency or persistence change. Documentary successor must inspect AC-01..04 clauses independently; operational AC-05 stays open unless all obligations supported.

T903 rendering successor: see D-T903-HISTORY in product-f0-gate/plan.md.
Thirty-two real verification observations exposed >125 ms native client draw.
The bounded correction composes the same newline-delimited status as zero-spacing
text children, allowing installed Iced Column viewport culling; no truncation,
eviction, state/message or Engine change. Supporting iced-engineering and rust
entries were read (unversioned, bridges1). Candidate 200%/900x700 retained all32
runs and reduced full-corpus max draw to73.24ms; product promotion requires all
rendering-dependent observations anew. Exact source predecessor is archived in
t903-20261105/before/application; prior observations retain original digests.


## T903 memory correction successor

Protocol recorded before new trials: docs/validation/t903-memory-20261105/plan.md. Apply adopted GUI64MiB to full-count history; keep fixed large-history256MiB separate. Preserve public inputs/equality/logical admission and historical evidence. Skills: performance-engineering primary, Rust/Iced supporting, actual entries read, unversioned and bridge v1; contributions in protocol. T903 remains open until final observations and checks.
