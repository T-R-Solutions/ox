# Acceptance review: controlled local task UI

AC-01: Controller process integration tests reject nonexistent and mode-000 directories
before attempt creation; actual Wayland and X11 windows accept the valid fixture root.
Selection canonicalizes/enumerates off-thread; exclusive directory creation tests write
access before spawning. This is not confinement or a grant to arbitrary commands.
AC-02: Real producer processes return Success/Failed(17)/TimedOut. Human screenshots
show those distinct terminal messages; Success stays UNVERIFIED until oracle execution.
AC-03: Runtime tests observe Cancelling before reaped exit; UI stays busy on cancellation.
Controller tests and explicit native observer reply confirm Cancelled. Kill alone never
sets the terminal outcome. An already-observed exit wins the cancellation race.
AC-04: The reducer test rejects duplicate starts, workspace edits while busy, old-generation
and duplicate terminal responses. Editing a path advances generation before another
selection. Closed scenario strings and operation admission prevent arbitrary commands.
AC-05: All spawn/wait/capture/evaluate work lives on a named worker. update/view never
lock Controller or wait; the identical dispatch mechanism handles task and verification.
Real Iced verification produced visible approved/rejected states; human interaction and
X11 frames demonstrate details changing while a task runs. No latency SLO or arbitrary
long-filesystem-load measurement is claimed; this is the controlled local fixture slice.
AC-06: Actual producer writes exclusively into the attempt-owned directory. Oracle
independently reconstructs request identity and result=42 from immutable check arguments.
Process tests exercise incorrect bytes; direct fixture checks reject wrong identity.
Wayland observer confirmed APPROVED and REJECTED; X11 captured both real verdicts.
AC-07: Successful producer exit does not approve. Controller starts without observations;
missing result is explicitly UNVERIFIED. Engine tests show completion claims create no
approval. Native screenshots preserve missing-evidence diagnostics before/after improvement.
AC-08: Actual X11 input flow approves, mutates only its owned result, refreshes to stale,
and re-verifies to REJECTED. Captures retain the original approved bytes and run:1 history.
The process integration test independently proves the same invalidation/history behavior.
AC-09: create_dir and create_new fail instead of overwriting; controlled producer writes
only request/result under that new directory. Binary sentinel bytes remain intact in
process tests and real graphical fixture. This is not an OS-level hostile-code guarantee.
AC-10: Native observer confirmed X close during an active hanging task; exit 0, no supervisor
termination. Current-run Sair also exited 0 with no sampled child left. X11 closes during
active execution and both ordinary exit paths pass. While verification is active, the
same closing admission gate waits for its worker completion under Engine's existing
deadline; reducer and Engine timeout tests cover that path without claiming a separate
slow-verification graphical capture. Forced external kill is outside graceful shutdown.
AC-11: Five Verdict variants map exhaustively to SDD labels. Captures show criterion,
run, current inputs, oracle command, recorded prior content and observation timestamp.
Explicit Refresh re-observes content; there is no continuous monitor. Memory-only Engine
retains at most 32 observations; a new process starts without acceptance/history.

All 11 criteria are supported for this bounded slice by combined source review, domain
and process tests, actual native Wayland interaction, and captured X11 interaction.
New source/lockfile changes were tested; only unchanged library implementations and
native production inputs are reused with explicit comparison. Prior envelopes, failed
sandbox/graphical checks, expired manual session and snapshot-format failure are retained.
No F0 completion, remote provider, marketplace, persistence, sandbox or platform expansion.
