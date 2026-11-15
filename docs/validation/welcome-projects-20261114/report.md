# Project welcome — 2026-11-14

## Scope and proposal

Implementation, scoped verification and independent validation are complete.
WC-01–06 are APPROVED within the methods and limits below. Current states are
recorded in evidence.json. Earlier pending statements in chronological sections
describe their original observation stage; the six broad feature ACs remain INCONCLUSIVE. Explicit request
authorizes a dedicated IDE welcome page, persistent recent paths, and real empty
project-folder creation. Contracts are in product-visual-workbench spec/plan.
General persistence experiments and D5/D6 are unchanged.

Baseline inspected: visual-workbench-20261111/welcome-baseline-1440-20261114/initial.png.
It shows a wide branded top/bottom chrome, extensive sidebar and technical validation
form as primary content. Proposal: neutral entry, small Ox identity, Settings access,
short presentation, Open folder/New project, readable recent names/paths and secondary
manual entry. No dashboard or marketing illustration. The user identified IntelliJ IDEA and supplied /tmp/pasted-image-.png, inspected
by root and coordinator. SHA-256: 64a5901d7c862240c763e0010e2b69aee8125dd7cdc8bd7bb4c7926f510ab663.
The screenshot shows neutral project navigation, centered welcome/actions, broad
reading space and a separate onboarding promotion. Ox adopts the project/action
hierarchy; onboarding advertisement, clone and remote entries are outside this scope.
No version, runtime interaction or exact visual fidelity is established by that image.

Captured monitor sizes are 1440×900 and 640×480; root observed actual window geometry
1288×860 and 573×430 respectively. These are real baseline captures, not claims of
maximized logical dimensions. Candidate comparison must match or disclose difference.

## Documentation disposition

Before implementation, updated project.md, feature spec/plan/tasks; retained originals
under before/. DESIGN, constitution, architecture, previous start-screen/folder-picker
reports and persistence ADR inspected. Final behavior and acceptance updates remain open.

## Execution capabilities and ownership

Observed profile-based spawning: ec_orquestrador_alta coordinates documents; two
ec_implementador contexts own disjoint backend/UI files. Root is native executor.
All four tree slots are occupied with useful work. Messages and status listing work.
No explicit close operation is offered; a later successful fresh-context spawn must
establish slot reuse. Reviewer and validator will be independent contexts; current
implementation declarations alone do not approve criteria.

Structural observation before implementation: from repository root,
`PYTHONDONTWRITEBYTECODE=1 python3 sdd/tools/validate.py --root . --features
sdd/features --feature product-visual-workbench --structure-only` returned 0.
This checks structure only; WC criteria remain UNVERIFIED.

## Backend implementation observation (pre-integration)

The backend implementer delivered project_store.rs with a fixed std-only API.
Coordinator inspected source and raw standalone test output: 17 passed, 0 failed,
1 subprocess helper intentionally ignored by the parent runner and invoked by
parent cases. Source/harness/log bindings: backend-observation.json. Strict rustc
forbids unsafe and warnings; rustfmt passed. Integrated Cargo initially failed on
UI use of Iced advanced APIs before enabling that feature, so it is not a passed
integration observation. Full details and initial failures are retained in
backend-implementation.md. No backend acceptance follows from the implementer's report.

Schema: 8-byte OXRECENT magic, little-endian version 1/count, length-prefixed UTF-8
paths; cap 20, 16384 bytes per path, 327776-byte snapshot. OS lock is per operation,
with fresh reread and sync/stage/rename/sync publication. Explicit unlock guards
against a concurrent fork retaining the lock before exec. Reset preserves bounded
corrupt bytes; oversized/future schemas refuse reset without modifying originals.
Crash-window tests arrange publication primitives then process::exit, rather than
injecting failure inside production publish. No power-loss, ENOSPC, hostile-writer
or network-filesystem claim. Interrupted stages and explicit corrupt backups can
accumulate; no destructive cleanup policy is introduced.

## Integrated Rust candidate

The finalized UI/backend candidate compiles with Iced's existing advanced feature,
used for exact focused-widget geometry. No dependency version or lockfile changed.
Raw Cargo logs were inspected by coordinator and all current input hashes compared
with implementation-inputs.json: identical. `cargo test --manifest-path
application/Cargo.toml --offline --locked -p ox-ui` returned 0 with 40 unit, 4 local-task
integration and 1 shell contract passed; 1 helper is intentionally ignored in the
parent runner and executed by subprocess tests. Clippy/all-targets with warnings
denied, ox-app build, rustfmt and tracked-path diff checks returned 0. Commands,
first failures and limits remain in ui-implementation.md and rust-observation.json.

Pre-correction candidate binary SHA-256: 1188b7c64eec612a7116d87cd687fe5f51612e6d3a77e9a281bd37c8aa0bd07a.
The unit tests validate message guards, empty/filled history state, failed-save
selection, cancellation and geometry operation. Filesystem tests validate persisted
bytes, collision/sentinel preservation and cooperating lock behavior. They do not
substitute for real GUI restart/picker/focus/capture observations.

## Documentation before graphical acceptance

Reviewed and updated application/README.md (entry/create/recent paths/recovery),
docs/design/surfaces.md (S01/S02 backend and composition),
docs/design/reference-coverage.md (actual IntelliJ reference and exclusions),
docs/architecture/context.md (limited persistence boundary), sdd/project.md and
feature spec/plan/tasks/converge/evidence. DESIGN remains unchanged: neutral roles,
Plex,24/22px headings and explicit themes are applied; existing shared token values
need no change. Root README delegates usage to application/README and needs no
command change. General persistence ADR/D5/D6 and its product acceptance remain
unchanged because this snapshot contains only recent paths.
Independent source/native review, graphical observations and final validation are
still outstanding; T018/T019 implementation is present but T020/T021 remain open.

## Native continuation after host approval

The host approval wait delayed native execution while product implementation
continued. Consequently, `native-before-small-escalated` is a **candidate** capture
despite its directory name: its recorded binary hash is1188b7c64eec612a7116d87cd687fe5f51612e6d3a77e9a281bd37c8aa0bd07a
and all ten recorded product source hashes matched implementation-inputs and the
then-current files at coordinator inspection, before the P1 correction.
It is not a pre-change baseline. Valid old baselines remain under
visual-workbench-20261111/welcome-baseline-1440-20261114 and welcome-baseline-640-20261114.

Coordinator inspected candidate maximized.png: neutral entry with Ox/Settings,
concise introduction, Open folder/New project, secondary manual entry and a quiet
empty recents section, all visible in the640×480 outer window at scale1 (including
native title decoration). Blue is concentrated in the primary action; typography
and separators use existing roles. The isolated Mutter display reports640×480,
scale1 and no primary-desktop input. Application natural exit0 is recorded.
This is first-use rendering/capture evidence only; the plan contains screenshots,
window-maximize interaction and exit, not the full required behavioral journey.
The preceding non-escalated attempt failed compositor readiness before launching
the application and remains recorded as failed setup.

## First native creation and restart observation

`native-wide-create` exercised real keyboard input: enter S02, type project name
and absolute parent, inspect destination, focus/activate Create and open, then
return to S01, close naturally and launch again. Both launches exited0 with
binary1188b7c64eec612a7116d87cd687fe5f51612e6d3a77e9a281bd37c8aa0bd07a.
The harness independently asserted an actual empty created directory. Coordinator
inspected creation-preview.png and persisted-after-restart.png and read the snapshot
bytes: OXRECENT/version1/count1 with the exact created canonical path. The directory
remains empty on direct inspection, confirming no automatic task artifact creation.
Restart shows the real name/full wrapping path without opening it automatically.
The1440×900 maximized outer window differs from the1288×860 old baseline; a matched
restored capture is still required for geometry-comparable presentation evidence.

Independent reviewer raised a pending P1 hypothesis: a mouse click into an unchanged
creation input may leave custom focus on Create, allowing Enter to confirm unexpectedly.
Root is reproducing it graphically. These positive creation/restart observations
do not dismiss that distinct interaction case or establish WC acceptance.

## Confirmed interaction counterevidence

`native-input-enter-review` confirmed the independent reviewer's P1 hypothesis on
binary1188b7c64eec612a7116d87cd687fe5f51612e6d3a77e9a281bd37c8aa0bd07a:
after keyboard focus on Create, a mouse click into the unchanged project-name input
and Enter created `parent/must-not-create`. The harness's independent assert_absent
failed; result.json records that failure. Coordinator inspected button-focused.png
and after-input-enter.png, which show the before/Create focus and resulting Tasks
view. This violates the explicit creation-confirmation/keyboard contract (WC-04/05),
not a cosmetic issue. UI correction and regression replay are required; positive
creation/restart observations above remain historical for their original inputs.

## Correction to the native P1 interpretation

The preceding assertion that native-input-enter-review **confirmed a delivered
mouse click** is superseded. Root inspected the Wayland event sequence: pointer
capabilities appeared on the first click, before wl_pointer binding; no enter/motion/
button delivery reached the application. The attempted click was lost. The original
and first fixed replay therefore demonstrate Enter on the still-focused Create
button, not Enter in an actually mouse-focused input. Their assert_absent failures
are retained as harness counterevidence and do not prove the patched product failed.

The source defect remains valid: before correction, non-submitting inputs did not
consume Enter or synchronize native mouse focus with the custom tab order. The
implementer added TrackedInput forwarding Iced operations and reporting actual
post-click focus, plus effect-free explicit submit handling for name/parent/draft.
The real Iced widget-tree/layout/event regression executes captured clicks/Enter
and Tab across six inputs; it is stronger than injected messages but remains
different from actual desktop input delivery. All41 unit +4 integration +1 shell
tests, Clippy, build and formatting passed; detailed results are in
ui-enter-correction.md and hashes in enter-correction-inputs.json. Coordinator
compared all those source/binary identities with actual bytes and found no drift.
New binary:f2674f14b64de94a6f0b889a8e5ff10b3635f3cf9453ffb000f5d30bc8636d83.

The independent reviewer reexamined the patched sources and widget regression,
read the new logs, and reported no additional source finding. R-WC-01 remains open
for native replay. Root is priming the pointer before application launch and waiting
for binding; native-input-enter-fixed-pointer will test actual delivery separately.

## Correctly delivered input replay

`native-input-enter-fixed-pointer` passed on binary f2674f14… with natural exit0.
Root's protocol inspection confirms pointer enter/motion/button were delivered
after pre-launch pointer priming. Coordinator inspected after-input-enter.png: S02
remains open, name field has actual focus, and the independent assert_absent for
parent/must-not-create passed. The independent reviewer compared exact final source
and binary hashes, inspected this capture/result and resolved R-WC-01 for this
scenario. The full wide/narrow journey remains a separate pending observation.

Raw corrected-test logs remain in /tmp/welcome-ui-enter-tests.log,
/tmp/welcome-ui-enter-clippy.log and /tmp/welcome-ui-enter-build.log. Coordinator
read these outputs and recorded hashes in rust-enter-observation.json. Root directed
that this task not rotate/remove unrelated retained logs or introduce a third local
log date. Temporary availability is explicit; these paths are not a durable archival
guarantee. Independent reviewer/validator can inspect the actual logs during this run.

## Final-source native wide journey

`native-final-wide` completed the real isolated Mutter/Wayland journey at maximized
1440×900/scale1 on binary f2674f14…; all three application launches exited0.
Coordinator compared all ten source hashes with actual files and inspected the
real GTK dialog, unavailable-project feedback, creation collision and verified-task
captures. Root inspected the remaining journey captures. This run observed:

- Settings opens existing preferences; Open folder maps the real GTK chooser,
  cancel returns focus, confirm opens the exact selected existing folder. Both
  helper PIDs are recorded and chooser disappearance was required before continuing.
- New project Escape cancellation creates nothing. Existing-name collision preserves
  sentinel bytes; absent parent fails without creating a destination. Explicit
  creation produces an empty directory, then opens Tasks without running a task.
- S01 shows actual recent paths. Natural exit/relaunch preserves both references.
  Moving the newest project causes recoverable open feedback; removing its row
  leaves the moved directory intact. Another exit/relaunch confirms removal persists.
- Reopening the remaining recent project reaches Tasks. Explicit execution and
  verification show “Critério aprovado”. Independent filesystem inspection found
  request `ox-task-v1:1794739120520546197:1:1` and matching result identity plus
  `result=42`; the original sentinel is still exactly `preserve\n`.

Snapshots/events/plan/environment are retained in native-final-wide/. Test-only
GTK portal/a11y/settings overrides and readiness waits follow the earlier isolated
chooser method; no default-portal startup-latency, X11, AT or fractional-DPI claim.
The run supplies functional native evidence; the separate final narrow/themes and
matched-geometry comparison remain pending at this point.

## Final-source native narrow/themes journey

`native-final-small` passed on the same f2674f14… binary with natural application
exit0. The outer maximized window is640×480 at scale1, including title decoration.
Coordinator inspected create-focus, remove-keyboard-focus, name-shift-tab-focus,
Dark, High Contrast and Compact captures and compared all ten source identities.
Real Tab focuses Settings/Open/New; S02 traversal reveals parent picker and Create,
Shift+Tab returns to the name input, explicit confirmation creates an actual empty
folder. Recent open/removal focus is revealed with the wrapping path readable;
Shift+Tab returns to the row. The unchanged20-row traversal has a state-test oracle;
this native narrow run contains one actual project, not20 independently opened rows.

Theme/density changes are real preference interactions. Light's entry avoids
large blue chrome/panels; Dark/HC retain their existing shared slate/theme roles
and blue action/focus semantics, with no new per-page color constants. Compact
changes spacing rather than font identity. Ctrl+K overlay and Escape return were
captured. These observations cover selected states at scale1; no fractional-DPI,
assistive-technology conformance or all-theme/all-state contrast certification is
inferred. The screenshot denominator is the actual saved corpus, not a prototype
quota. Narrow raw screenshots can scroll earlier headings/labels out of view while
revealing the active control; no hidden-action fix relies on shrinking text.

## Final recovery and comparable capture

`native-final-recovery` passed on f2674f14… with two natural exit0 launches and
unchanged source identities. Injected corrupt bytes are a deliberate test fixture;
restart shows a recovery message, explicit reset confirmation clears the list, and
a retained corrupt-backup contains exactly `damaged-history\n`. Manual entry then
rejects a missing path, accepts the repaired actual folder and adds its real recent
reference. That project remains empty, without any automatic task. Coordinator,
reviewer and validator inspected the relevant captures and actual backup bytes.

The restored candidate capture matches the earlier real baseline: monitor1440×900,
outer window1288×860 at x79/y23, scale1, Light/Comfortable, first-use empty state.
Both use the same bundled Plex resources and native renderer. Application title
text/session label differ intentionally; this is a controlled composition comparison,
not a claim of pixel equality or measured productivity gain.

| Before | After |
| --- | --- |
| [Original entry](../visual-workbench-20261111/welcome-baseline-1440-20261114/initial.png) | [New welcome, matching geometry](native-final-recovery/comparable-restored.png) |

Useful final captures: [recent projects](native-final-wide/recent-restarted.png),
[creation with keyboard focus at640×480](native-final-small/create-focus.png),
[missing project recovery](native-final-wide/unavailable-project.png),
[real folder chooser](native-final-wide/folder-dialog.png).

## Final independent review and criterion handoff

The independent ec_revisor context completed source/preimage/log review plus all
19 final-wide,18 final-small and8 recovery screenshots and the delivered-pointer
regression. It found no remaining issue on the final source/binary identities.
Exact review provenance, initial P1 and corrected GUI interpretation are retained
in independent-review.md. The reviewer did not edit or execute tests.
The independent ec_validador_alta context has separately checked source identities,
raw test logs, actual artifact/backup bytes and native journeys and found sufficient
operational support; final documentary/evidence binding validation is pending.

| Criterion | Evidence method | Current disposition |
| --- | --- | --- |
| WC-01 entry composition | matched real captures, actual reference, native themes/tokens | APPROVED by independent scoped validation |
| WC-02 actual durable recents | filesystem tests + native create/open/restart/move/remove/restart/reopen | APPROVED by independent scoped validation |
| WC-03 bounded storage/recovery | source/lock/process tests + real corrupt reset and retained bytes | APPROVED by independent scoped validation |
| WC-04 real safe creation | exclusive-create/collision tests + native cancel/errors/empty folder + focus regression | APPROVED by independent scoped validation |
| WC-05 chooser/settings/no automatic tasks | native picker confirm/cancel/child absence, manual repair, Settings, actual empty folders | APPROVED by independent scoped validation |
| WC-06 acceptance and closure | final Rust/native identities, independent review, updated docs and final validator/checker | APPROVED by independent scoped validation |

Coverage limits: Linux local cooperative storage; isolated Mutter Wayland at scale1;
GUI lists contain1–2 genuine projects while cap20/concurrency/truncation/future-schema
boundaries are filesystem/state tests. Crash windows use controlled primitive
publication/process-exit tests, not power-loss/OS-crash injection. No ENOSPC, NFS,
hostile path replacement, default portal, AT, X11, fractional DPI or universal
contrast/performance claim. No complete scanners, downloads, commits or publication.
The six original broad ACs remain INCONCLUSIVE and historical F0 is not renewed.

Independent validator interim verdict: WC-01–05 APPROVED within the stated scope.
WC-06 has sufficient operational evidence and awaits this final documentary binding
review. The validator independently matched source/binary/corpus/log identities,
inspected source/fonts/tokens and comparable captures, actual snapshot/backup/task
bytes and native wide/narrow/recovery journeys. It did not reexecute Rust tests.
The explicit approval checker still returns1 solely for the six preexisting broad
AC-01–06 INCONCLUSIVE gates; it is not advertised as full product approval.

## Final scoped validation and documentation closure — 2026-11-15

The independent ec_validador_alta context examined final report/review/validation/
tasks and schema2 evidence with208 bound inputs (sources, Plex fonts, manifests,
lockfile, binaries, imported native oracle and actual corpora). It approved WC-06,
therefore **WC-01–06 are APPROVED** within the explicitly bounded methods above.
It independently ran freshness/convergence successfully; adding require-approved
returned1 solely for the six preexisting broad ACs marked INCONCLUSIVE. Neither
result is presented as full application/F0/visual-workbench acceptance.

T017–T021 are complete for this requested successor. Final documentation disposition
covers project/feature artifacts, application usage, architecture context, surface
and source-reference maps and this report; DESIGN/token/font rules were applied
without palette/font replacement. Original dirty work, old evidence and corrected
interpretations remain preserved. Final closure changes only documentary verdicts
and their current bindings; it does not refresh historical operational inputs or
repeat unaffected product observations. No material issue remains in this scope.
