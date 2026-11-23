# Desktop navigation refinement — 2026-11-17

Status: implemented; DN-01–05 independently APPROVED in bounded observed scope. Explicit user feedback requests
icon-only Settings/chrome, real tooltips, no UI mascot, semantic destination icons,
unique navigation grouping and genuinely draggable/resizable/collapsible sidebar.
DN-01–05 are scoped in the existing feature. Original current bytes preserved
under before; prior enterprise acceptance remains historical for changed inputs.

## Iterations and independent findings

Initial sandbox attempt could not bind the private session socket; host-approved
private Mutter execution followed. No primary desktop input was used.
`preliminary-wide-host` showed correct icon-only hover, no mascot, distinct icons
and rail, but pixel detection stopped before the10-unit scrollbar gutter and
misdirected drag into the scrollbar. No drag success is inferred from its exit0.
`pointer-calibrated` corrected the coordinate and observed real resize/min/max/
restore; sources changed during tests, so it remains preliminary. Grab offset
was then preserved to eliminate the3-unit handle-start shift.

First stable `final-wide` and `final-small` (binary dbd5bbca…) have passing pixel
oracles and actual event journeys:256→336 wide, max420/min200; narrow max314;
rail52 and preferred-width restoration; buttons reduced280→256 then restored280.
Motion after release, titlebar-outside release, Escape and wide window-resize
during drag do not continue resizing. Ctrl+Alt+arrows were consumed by the WM;
visible shrink/grow buttons, traversed with Tab/Enter, are the reliable alternative.
The initial narrow background scan501 is a search-range cap, not a sidebar width;
entry has no resizable workbench pane. Later harness records entry pane edge null.

Independent P2 DN-04: lower navigation focusID survived a toggle but its scroll
position could reset when the expanded header changed the widget tree. Worker
adds actual-bounds reveal after toggle, resize and keyboard adjustment. A dedicated
last-focus rail→expanded→rail capture is required after correction. Independent
P3 rail56 documentary mismatch was corrected to actual52. User's literal Settings
text-only-on-hover is preserved by suppressing its forced keyboard label overlay;
focus border remains. Other icon controls/rail retain identifying focus overlays.

## Final implementation and observations

Final source/binary bindings: implementation-final03.json, binary
55bb67c7a76ca36b4dac9e8c48931fe814627dfeae9b6c6ac3b337d5ef818a23.
46 unit tests +4 integrations +1 shell contract passed;1 subprocess helper is
intentionally ignored as a direct test. final03 test/build exit0; final02 Clippy
exit0 preceded only the final one-line removal of Settings' focused footer label.
The effective source changes stay in desktop.rs/views/icons/identity, with new
hint.rs/splitter.rs. No domain/history/runtime behavior or dependency changed.

final03-wide (1366×768) and final03-small (640×480) record stable source and
binary inputs, actual window configuration and natural exit0. Pointer pixel
oracles passed: default256, wider336 on wide/314 on narrow, max420/314, min200,
release keeps width, rail52, preferred280 restored, keyboard shrink280→256→280.
Escape ends at296 and further motion is inert; wide window resize during held
drag cancels and returns296. These are actual rendered measurements calibrated
against the10-unit scroll gutter, with screenshots independently inspectable.

Root/coordinator inspected Settings hover and keyboard captures: text appears on
hover only; keyboard retains focus border without forced label/footer. Toolbar
and27 semantic destination icons are native, groups occur once, no mascot is
rendered. Final small last-focus-expanded and last-focus-collapsed show Appearance
focused and visible in both states after actual Ctrl+B toggles, resolving P2.
Native Dark/HC and rail navigation remain legible. Width preferences are session-only.

### Capture anomaly and bounded limits

final02-small is invalid: after the initial Ox frames, one capture shows an image
viewer containing a historical screenshot, and pixel assertions subsequently fail.
That corpus is excluded. Cause is not established. Inspection of probe-session.py
shows a separate dbus-broker and private Wayland display; its application log
records pointer enters/buttons delivered to the launched Ox client. These facts
do not prove complete capture isolation or explain the unexpected frames. No
primary-desktop input was intentionally addressed; do not claim an isolation repair.
Final03 result/capture inputs are stable and inspected frames show the correct Ox
with matching requested states/geometry. Acceptance is bounded to those observations.

No AT/X11, extra scale factors or full historical AC/WC matrix is established.
WindowUnfocused cancellation is source/test-covered, not a separate native focus-loss
replay. Ctrl+Alt+arrows are supplementary and were intercepted in this compositor;
the actual Tab/Enter resize buttons passed. No commit or full scanner was run.

## Documentation disposition

Reviewed/updated DESIGN.md, docs/design/components.md and surfaces.md for chrome,
icons, rail/drag/focus and session-only geometry; application/README.md for usage;
identity/README.md records preserved-but-unloaded mascot artwork. Project and
feature spec/plan/tasks/converge/evidence record authorized scope and current
limits. Constitution/architecture and original identity/font/palette provenance
were reviewed: no architecture, domain, token/font or artwork byte changes.
The skill entries/bridges used are recorded in plan; additionally consulted
Iced layout-and-custom-widgets and design-system accessibility verification for
native focus/capture semantics. Selected full-feature gates remain unchanged.

## Scoped acceptance and closure

Independent review returned no unresolved finding; independent validator approved
DN-01–05 on final03 inputs. Detailed criterion verdicts and limits are transcribed
in independent-review.md and independent-validation.md. T027–T030 complete.
Whole-feature freshness/convergence checker0; adding require-approved1 solely for
six historical INCONCLUSIVE ACs. WC remainsUNVERIFIED. No product/harness inputs
changed after final03 native observation; closure edits transcribe verdicts only.
All delegated writers/reviewers/validator and owned native processes completed.
