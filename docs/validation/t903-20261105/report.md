# T903 current-input revalidation — 2026-11-05

T903 remains OPEN. Current controlled functional journeys and the adopted small GUI
matrix pass; a reproduced full-count history draw failure was corrected and its
rendering reobserved. Full-count GUI RSS is INCONCLUSIVE against the adopted scope:
all twelve new 32-observation runs exceed64MiB (maximum133.69MiB). The contract
separately adopts256MiB for a fixed renderer-free two-15-MiB-input corpus, which
passes, but does not explicitly assign that envelope to this graphical full-count
workload. Neither silently extend that allowance nor declare the full-count workload
accepted. Under a64MiB interpretation these observations are REJECTED. This is the
remaining acceptance oracle dependency, not an unavailable measurement.

Exact next step: maintainer resolves which **existing** adopted RSS corpus applies
to full-count graphical history, with written authority. If64MiB applies, investigate
retained snapshot/layout memory and repair within authorized scope; replay affected
resource/render/functional observations on changed inputs. A broader budget would
be a separate contract decision, not this execution's acceptance. If neither adopted
corpus covers it, obtain an explicit corpus/oracle before acceptance. Do not rerun
unchanged timings merely to obtain lower numbers. T903 is unchecked in all three
features; current F0 AC-05 INCONCLUSIVE, historical F0 approval preserved.

## Authority, identities and changes

Read root AGENTS/project/constitution/architecture/workflow/evidence, affected F0,
UI and Engine features, robustness report, F0 boundary and resumption contract/
methods/matrix, and persistence ADR/feature/protocol. Full route reuses those features.
Initial Git workspace was clean at d9de8ca2801d1f51878e72f35f4a83e0c4fe4b57.
`before/` preserves touched feature/source preimages; historical-input-map.json and
history-source-succession.json resolve old digests to identical bytes. Earlier
proposal/open/provisional closure → withdrawn history failure → raster closure →
robustness UNVERIFIED → this successor is the explicit lineage. No historical
corpus or previous artifact digest was overwritten/renewed as a current execution.

`product-inputs.json` identifies the robustness input; `current-product-inputs.json`
identifies all77 current application files, including Cargo.lock, toolchain/profile,
Engine/controller/Runtime/fixtures and desktop correction. Only product change here:
`application/crates/ox-ui/src/desktop.rs` composes the complete status in newline-
preserving zero-spacing text children so installed Iced Column culls offscreen text.
No eviction/truncation, state/message, Engine API, dependency or storage change.

Primary performance-engineering, supporting iced-engineering and rust were actually
read/used; paths/unversioned entries/bridge1/contributions are recorded in plan.md.
No delegation. Sources are pinned Rust1.99.1/edition2024/MSRV1.99/Iced0.14.0;
dev first-party code unoptimized, existing tiny-skia0.11.4 opt-level3 retained.
Mutter actually reports51.1 in current logs (the historical50.5 prerequisite is not
a current version assertion), native isolated headless session with AMD GBM render
nodes; X11 is Xwayland inside that isolated compositor. This does not establish
primary-session, other-host/OS or physical-scanout support. Hardware/toolchain/mount
identity is environment.json; per-run environment/display state, binary SHA-256,
protocol/X-window observations and logs identify actual execution. Cargo test can
relink diagnostic Ox through feature unification; native per-run hashes record both
observed binary identities, with stable source inputs. Original uninstrumented and
instrumented native journeys corroborate the source change separately.

`instrumentation/` preserves initial deltas; before-diagnostic-desktop.rs.bin and
current instrumentation snapshots identify the rendering successor. Temporary app
and target are /tmp/ox-t903-app and /tmp/ox-t903-target; installed registry is never
modified. Local iced_winit timer patch measures client draw through presentation-
call return; no earlier layout or scanout claim. Native response uses compositor
PipeWire pixels, ordinary X11 tests use client get_image; additional32/FIFO X11
runs use compositor pixels and explicit private-X-server focus. Poll waits20ms,
asynchronous capture and100Hz CPU ticks limit interpretation. Filesystem calls
remain cooperatively observed, never universally interruptible.

## Expected contract and current observations

Plan recorded before trials. Adopted matrix: X11/native Wayland separately ×
100/150/200% × logical640x480/900x700, twelve cells. Native monitors1200x900 times
scale; X11 logical and physical window geometry asserted in tests (up to1800x1400),
compositor2400x1800. Per cell3 warmups+20 measured response/client samples;
max response120ms, client draw/present-return125ms, sampled small-corpus GUI RSS64MiB,
three10-second idle windows <=5% one core. Every raw client frame is inspected,
including startup, full journey/history; toggle-only samples never override failures.
Backend3+20: execute/verify50ms each, cancel to observed direct exit100ms,
harness32MiB. Separate retained content128MiB prelaunch refusal/no eviction;
fixed two-15-MiB-input history stress RSS256MiB over3 runs.

| Criterion / expected | Method, current result and artifacts | Acceptance / limits |
| --- | --- | --- |
| Controlled task produces exact attempt-bound artifact, explicit independent verification, incorrect bytes rejected | Six current native matrix journeys,42 actual X11 graphical tests, current-original; request+result byte assertions and retained captures/logs. current-checks.json selects the explicit native focus replay. | APPROVED in controlled corpus; original binary corroboration is distinct from diagnostic logs. No real agent/plugin desktop claim. |
| States/history and stale invalidation | X11 correct/stale/incorrect captures and native approved/rejected retained-history captures; current32 runs retain all32 observations and reach bottom run32. | APPROVED; five-state Engine API regressions support semantics, not all five GUI states. Graphical APPROVED/REJECTED/UNVERIFIED/INCONCLUSIVE observed; UI does not generate an applicability disposition. |
| FIFO without writer: Refresh/Verify cannot approve | Own task result renamed, mkfifo at its exact path; current-fifo-native/current-fifo-x11. Refresh Done and pixels show UNVERIFIED with historical run1; Verify shows explicit regular-file error. Restoring original bytes and Refresh exposes retained history again. Sentinel unchanged. | APPROVED; FIFO mode/writer absence, actions, protocol/X focus, captures and exit0 correlated. Observer delays in result.json include deliberate key pacing and are not adopted response samples. No universal regular-I/O bound. |
| Cancel/close while executing/verifying, worker and direct process terminate | Six native hang-cancel cases and six X11 flow/held cases; current-held records live ox-local-task TID and oracle /proc stat with application parent, then worker absence, direct PID absence, second held oracle/close exit0. Original binary native flow corroborates. | APPROVED; cancellation is cooperative, close waits for Done. Direct child differs from descendants. Harness cleanup of its compositor/Xwayland is not product descendant containment. App process exit removes its threads; no arbitrary FS cancellation or universal ten-second close claim. |
| Adopted small GUI matrix | current-checks.json, current-final-analysis.log: response max58.517ms, all-client-frame max80.313ms, GUI RSS max55.723MiB, idle max0.500% one core; all12 pass. RSS sampled20ms plus VmHWM. | APPROVED on its exact corpus. No extrapolation to full-count memory; zero CPU tick delta is not zero work. |
| Full-count graphical history drawing/response | Before: history-native-*-900 max159.935ms rejects125ms. Candidate200%900 max73.241ms. Current-history-checks.json: all12 retain32 runs; all-frame draw max74.384ms, response max65.377ms,20 samples after3 warmups; top/scroll/bottom captures. | Draw/response APPROVED; failure preserved. All raw frames, not only sampled toggles, checked. |
| Full-count graphical history RSS | Same current32 runs:90.63–133.69MiB lifetime high-water, all >64MiB. Engine stores complete immutable before/after Vec snapshots for each observation; the two helper binaries alone imply about58.4MiB raw content for32 before/after captures, before GUI/layout. This byte-size calculation is explanatory, not an allocation profile. | INCONCLUSIVE applicability oracle, REJECTED if64MiB applies. No deduplication/API rewrite or128MiB retention reduction introduced to hide it; fixed256MiB stress acceptance is not transferred. T903/F0 remain open. |
| Backend latency/harness memory | backend-direct.log,20 samples after3 warmups: execute15.936ms, verify3.885ms, runtime cancel0.112ms, verify cancel2.427ms; RSS7468KiB (7.294MiB). | APPROVED. Initial cargo-run RSS55672KiB includes launcher and is excluded from direct-harness RSS; kept intact. Rendering change does not change backend sources; this Engine-input reobservation is retained. |
| Fixed large-history corpus/admission | history-0/1/2.log: actual two15MiB inputs,2 retained observations, refusal before another effect with old history retained. All runs exit0 and peak below256MiB (see raw /usr/bin/time). | APPROVED for that renderer-free corpus only, not full-count GUI RSS. Sparse inputs/caches/host FS limitations remain. |
| Coverage and regression/current Rust checks | current-test/fmt/clippy/build logs; coverage-current and coverage summary:975/1047 total lines,115/127 changed, Engine65/72 robustness lines and desktop6/6 new lines. Actual instrumented native journey merged separately,371 profiles/42 objects; artifacts list excluded lines. Defective FIFO reproduction remains in robustness corpus, current regressions pass. | APPROVED for adopted >=80% changed-line target and bounded critical scenarios. Killed processes may omit counters; injected syscall errors are not real syscall failure. Ordinary suite's six ignored graphical cases are separately run by matrix, not mislabeled as ordinary-suite execution. |
| Documentary AC-01..04 | documentary-review.md and documentary-scenarios.json review36 records, seven F0 rows/successors, common persistence obligations and exact preimages. Checks/limitations in checks.json/logs. | Documentary preparation separate from F0 operational acceptance. Hashes do not authenticate observations or establish oracle completeness. |

## Preserved failures, observer corrections and checks

probe-native failed with EPERM on Unix socket in sandbox; explicitly authorized
unrestricted isolated runners followed. First FIFO X11 observer called absent
xwininfo, then xprop-only run timed out without keyboard focus; both raw attempts
remain. focus-x11.py now identifies/focuses only Ox in its own X server. This fixed
all current extra X11 journeys; no primary desktop input. Initial current native
100%900 run logged wl_keyboard.leave during idle and received no later keys;
current-replay-native-1-900 restores focus explicitly outside timing samples and
passes. Initial current-matrix-analysis failure remains; current-final-analysis is
the successor, not deletion of the failed observation. No source change occurred
between that failure and focus replay. Scripts can exit0 while result.json has an
error; acceptance checks inspect both, not process exit alone.

All commanded scripts/examples were inspected and exist. Product checks are recorded
in current-runs.json and raw logs; final governance/structure/freshness/whitespace
outcomes reside in checks.json with exact commands and exits. These checks do not
approve GUI performance or resolve the RSS scope oracle. No further repeated tests
without changed inputs or a discriminating observer correction are claimed.

## Persistence decision preparation

After revalidation, reviewed existing ADR and all persistence feature artifacts.
[persistence-decisions.md](persistence-decisions.md) is the concrete D2/D3/D4/D4-deps
packet: common contract/failure envelope; disposable paired E01..E08 including
experimental Iced shell; proposed XFS directory/corpora/repetitions/quotas/deadlines/
fault permissions; mandatory isolated native-source/driver/lock/config/license
freeze review. D1 placement remains adopted. Next decision is the maintainer's
explicit disposition of those four items, then T009's independent manifests and
pre-run dependency freeze. No experiment, dependency acquisition, candidate/store
implementation, D5 choice or D6 integration occurred. All persistence ACs UNVERIFIED.
No commits, staging, publication, global installation, destructive user-file
operations, remote agents or code transmission occurred.
