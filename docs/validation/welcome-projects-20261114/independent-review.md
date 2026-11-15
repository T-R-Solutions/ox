# Independent review — welcome/projects

Reviewer: independent ec_revisor context `/root/welcome_review`, separate from both
implementers. This record is transcribed by the documentation coordinator from
the reviewer verdict relayed by root; the reviewer role is read-only and did not
edit product files. It is not coordinator self-review.

## Initial candidate verdict

Source review found one open P1 finding, R-WC-01. The reviewed candidate is bound
to implementation-inputs.json and binary SHA-256
1188b7c64eec612a7116d87cd687fe5f51612e6d3a77e9a281bd37c8aa0bd07a.
Pre-correction source bytes are retained in before-enter-fix/.

R-WC-01 — Unexpected project creation after mouse focus in an unchanged input.
Locations in that source: desktop/views.rs385,394 and desktop.rs935,1102. The name
and parent inputs emit changes but do not capture Enter; mouse focus without an
edit leaves the separate logical focus at control293. Global Activate then invokes
CreateProject. The real native-input-enter-review replay confirmed this: after
button focus, click the name input and Enter; assert_absent for
parent/must-not-create failed and after-input-enter.png displays Tasks.
This contradicts WC-04 explicit creation confirmation and WC-06 keyboard acceptance
(and the coordinated WC-05 interaction guard). Correct input focus/Enter routing
and replay before approval.

No other source finding was reported for snapshot lock/read-modify-publish, bounded
corruption/future-version recovery, exclusive directory creation, cancellation or
stale replies. The reviewer read the test logs but did not execute tests. Initial
native creation/restart captures were available; full narrow/theme/removal/missing/
picker journeys were still pending. Absence of another source finding is not
graphical acceptance or a guarantee outside the documented cooperative Linux scope.

## Follow-up

P1 correction, source re-review and native regression replay are pending. No final
independent approval has been recorded yet.

## Source follow-up and native-evidence correction

The reviewer independently confirmed the initial source identities matched
implementation-inputs.json and read the corrected sources desktop.rs ee975db8…,
views.rs516a6e9f…, binary f2674f14…. The transparent TrackedInput delegates Iced0.14
Widget behavior and emits InputFocused after captured native input click; name,
parent and draft on_submit only update focus. The real tree/layout/input event
regression covers six fields and captured Enter/Tab. Raw41+4+1 tests/Clippy/build
were read, not reexecuted by this reviewer. No additional source finding reported.

The earlier reviewer/root/coordinator interpretation “confirmed by GUI” is
**superseded**: Wayland protocol inspection showed the first click was lost before
wl_pointer binding, with no delivered enter/motion/button. Both native-input-enter-
review and native-input-enter-fixed therefore do not establish input focus and
do not refute the correction. Original results/captures are retained. Source
mechanism and real widget regression are valid separate evidence; the revised
harness primes pointer and waits before launch. R-WC-01 remains open until that
properly delivered native interaction is replayed.

Reviewed source scope included Controller.select, desktop/views/workbench/store,
Cargo and UI preimages; storage cap/locks/atomic publication/bounded reset/future
versions/create_dir collision, async late replies and no automatic tasks. No
power-loss/ENOSPC/NFS/hostile-writer/AT/X11 claim. Remaining native journey scope
was still pending at this review stage.

## R-WC-01 resolved for the corrected delivered-click scenario

The independent reviewer matched current source/binary identities to the corrected
f2674f14… candidate, read native-input-enter-fixed-pointer/result.json (observed,
exit0), and inspected after-input-enter.png: S02 persists with name input focused
and assert_absent passes. Combined with source and real widget-event regression,
R-WC-01 is resolved within this observed scenario. Earlier failed GUI interpretations
remain superseded as described above. No additional source finding remains; broad
GUI final-wide/narrow observations still need review before complete scoped acceptance.

## Final independent review verdict

The same independent reviewer completed the full scoped source/preimage/log/capture
review:19 final-wide,18 final-small,8 recovery screenshots plus fixed-pointer replay.
Recovery inputs matched all ten current source hashes. The reviewer directly read
backup `damaged-history\n`, final one-entry history, matching task request/result42
and sentinel bytes; inspected manual error/repair/open, actual empty project and
reset confirmation. It compared restored candidate and original baseline at the
same1288×860 outer geometry/x79y23/1440 monitor/scale1/Light/Comfortable/empty state.
The new hierarchy meets project-entry needs with neutral reading space and clear
actions/recent paths. Final verdict: **no open finding** on desktop ee975db8…,
views516a6e9f… and binary f2674f14…. R-WC-01 is resolved; prior misattributed
GUI interpretation remains explicitly corrected.

Limits: cooperative Linux local filesystem; isolated Wayland1×; GUI1–2 recent
projects with cap20 tested separately. No AT/X11/fractional-DPI/all-state-contrast,
ENOSPC/power-loss/NFS or hostile-confinement acceptance. Reviewer performed no
product edits or test execution. This review does not replace independent final
criterion/evidence/document validation.
