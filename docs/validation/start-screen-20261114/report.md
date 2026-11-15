# Start-screen delivery — 2026-11-14

## Scope and source analysis

The requested initial screen continues the existing visual workbench. DESIGN.md
§1/7/9 selects R4 entry/project composition, native adaptive geometry and honest
workspace/resume availability. The R4 first-use screenshot supplies a central
existing-folder entry area and an auxiliary context inspector. Returning-use and
R12's R11 start-center captures supply selection context, not real project data.
The source hero, fictional recent projects, dates, branch, tasks and decisions are
not adopted. Native headings remain 22–24; reading surfaces stay neutral.

Observed originals: `.inputs/design/r4.zip` and `.inputs/design/r12.zip`; actual
selected images inspected by root and coordinator in `/tmp/ox-start-reference-review/`.
Screenshots establish composition only; native interactions require separate replay.

## Scoped acceptance observations

| Criterion | Method / expected result | Current status |
| --- | --- | --- |
| SC-01 | Inspect R4/R12 and native capture: clear workspace entry, truthful empty/resume state, no invented history | APPROVED |
| SC-02 | Tests + native keyboard: validation, errors, resume and disabled/busy controls preserve domain effects | APPROVED |
| SC-03 | Inspect wide/narrow native captures, themes/density and visible keyboard focus | APPROVED |
| SC-04 | Focused Rust checks, independent review/validation, source-bound evidence and documentation disposition | APPROVED |

The feature-wide AC-01–06 remain INCONCLUSIVE until their broader evidence is
sufficient. Scoped completion does not transfer historical F0 acceptance.

## Documentation disposition

Updated: sdd/project.md; product-visual-workbench spec/plan/tasks/converge/evidence;
docs/design/surfaces.md and reference-coverage.md; application/README.md. These
record the actual folder/validation/resume flow and source disposition. Reviewed
DESIGN.md, docs/constitution.md, docs/architecture/context.md and the visual-workbench
ADR: no edit required because this slice applies the existing native presentation
and Controller ownership contracts, adding no persistence or backend. The root
README delegates usage to application/README.md and needs no command change.
Historical observations and broad incomplete feature gates remain preserved.

## Review-driven corrections

Independent code review identified a narrow-screen keyboard risk: Start actions
could receive focus below the viewport. A first END-scroll implementation would
still hide them if a long diagnostic followed the actions. The final composition
places path/context/optional diagnostics before a bounded final action group; Start
traversal scrolls to that group and back to the form. Native replay must verify
actual visibility. The explicit 1024 logical-pixel stacking boundary follows DESIGN.

## Documentary checks observed

`PYTHONDONTWRITEBYTECODE=1 python3 sdd/tools/validate.py --root . --features
sdd/features --feature product-visual-workbench --structure-only`: exit 0.
This checks structure, not semantic/native acceptance.

The same selection with `--require-approved --require-fresh --check-convergence`
returned exit 1: AC-01 through AC-06 are INCONCLUSIVE, as already recorded before
this slice. No broader gate was waived or silently approved. New scoped observations
will be recorded without converting incomplete historical feature coverage to PASS.

## Focused Rust observation

Pre-toolbar-correction `cargo test --offline -p ox-ui` with the repository Cargo cache passed:
9 unit tests, 4 local-task integration tests and 1 shell contract test, zero failed
or ignored. The integration cases exercise inaccessible workspace rejection, FIFO
rejection, artifact/history freshness and cancellation/timeout observed exit. The
new unit cases exercise Start resume visibility, draft invalidation, recoverable
selection error and the 1024-pixel boundary. These are state/controller checks, not
proof of visible keyboard focus. Raw output identity is in rust-observation.json;
product source/manifest/lock/font identities are in product-inputs.json.

Implementer also observed fmt, Clippy without warnings and the final application
build; those reports supplement, rather than replace, the raw test/native evidence.

## Pre-toolbar-correction native wide observation

`python3 /tmp/ox-start-native-review.py --name native-wide --flow --monitor 1440x900`
completed with exit 0 in an isolated Mutter Wayland session; the application exited
naturally with code 0. The 1440×900 capture shows a 2:1 folder/context composition,
neutral reading areas, 24px heading and retained Signature Blue chrome/Plex.
Invalid-path feedback is visible; a valid folder opens Tasks; returning to S01
presents the actual session path and a keyboard-focused resume action. Editing the
path removes resumption. Light, Dark, High Contrast and compact captures were
inspected. The real task artifact contains the matching request identity and
`result=42`; the preexisting sentinel is unchanged. Verification is visible in
task-verified.png. Result/events and artifact hashes are under native-wide/.

The earlier baseline was captured at an observed 1288×860 application size, while
the candidate is maximized to 1440×900. They support a qualitative hierarchy
comparison, not a geometry-identical pixel comparison. No X11, assistive technology
or historical F0 performance claim follows from this Wayland observation.

## Pre-toolbar-correction native narrow observation

`python3 /tmp/ox-start-native-review.py --name native-narrow --monitor 640x480`
completed with exit 0 and application exit 0. The context stacks below the folder
form. Real Tab reaches the last action and reveals its focus outline; Shift+Tab
returns to the path field at the top. Light/Dark/HC, comfortable/compact and
command-overlay Escape return were captured and inspected. Rendering and keyboard
observations cover these two logical sizes at scale 1, not every size/DPI/platform.

## Independent review

An ec_revisor context independent of implementation inspected exact preimage diffs,
Controller consumers, guards, tests, R4/R12 references and actual wide/narrow captures.
The reviewer initially reported no open findings on the source hashes in product-inputs.
The later button-3 counterevidence below reopened that scoped conclusion.
The earlier hidden-focus hypothesis was corrected and replayed; an inconsistent
command/cwd record was corrected to the actual argv/environment. The reviewer read
the raw 14-test output but did not execute tests or edit product files. The final
validator is a separate ec_validador_alta context.

## Counterevidence and correction follow-up

The additional native-narrow-details run exited 0 and demonstrated last-action
and input focus visibility, but root/coordinator inspection found a missed case:
expanded toolbar wrapping consumes a second row at 640×480, leaving the validation
button below the viewport when its focus handler snaps to START. The previously
positive last-action check does not cover that button. At that point SC-02/03 remained INCONCLUSIVE
pending a bounded toolbar correction and explicit button-3 replay. Original captures
and identities are retained; new source bytes need new native observations.

The toolbar correction omits the disabled Cancel action only on idle S01. A running
operation retains its cancellation control, and traversal already excluded the idle
button. All other screens retain their toolbar. No source except views.rs changed
relative to product-inputs.json; product-inputs-final.json records the final bytes.
The final-source unit suite was observed separately (9 passed, toolbar-fix-unit.json).
The preceding 14-test observation remains bound to its original sources; Controller
consumers/oracles are unchanged and native functional replay exercises the final build.

Final documentary structure selection and `git diff --check` on changed tracked
product/project/application-guide paths returned exit 0. Untracked native view and
feature files are covered by source compilation/document inspection rather than by
Git's tracked-only diff check.

## Final native correction replay

`python3 /tmp/ox-start-native-review.py --name native-narrow-final --monitor 640x480
--details` returned exit 0; application exit 0; binary SHA-256
`655047c26ffab8ba9124528d871452316a9ce759156d84e80fc5f10dc3b223f2`.
The explicit input2 → Tab button3 → Shift+Tab input2 replay shows the validation
button, label and focus outline above the footer, including expanded details and
a long rejected path. Last-action focus also remains visible. Root, coordinator
and independent validator inspected actual captures; source hashes match
product-inputs-final.json. The former narrow focus finding is resolved for this
observed size/state. Original counterevidence remains in native-narrow-details/.

The final wide replay (`--name native-wide-final --flow --monitor 1440x900`) also
returned exit 0/application exit 0 with the same final binary. It reobserved empty
entry, path error, validation→Tasks, session resumption, actual correct execution
and verification, draft invalidation, themes/density and command Escape. Native
result.txt matches request identity with result=42 and the existing sentinel remains
unchanged. Both final runs bind current desktop/views hashes.

The reproducible native harness is preserved as native-harness.py; the preceding
version remains native-harness-before-toolbar.py. It uses the identified historical
Session mechanism without driving the maintainer's primary desktop. Final capture
sets are native-wide-final/ and native-narrow-final/; preceding directories are
historical iterations and counterevidence.

Coverage: final native sessions at logical 1440×900 and 640×480, scale1; Light/Dark/HC
and both densities, actual keyboard traversal/activation/Escape, invalid input,
selected session and correct task+verification. Busy/stale/hidden controls, rejected
artifact/FIFO and cancellation/timeout are supported by the stated Rust test methods;
not every scenario was replayed graphically. X11, assistive technologies, fractional
DPI and historical F0 performance budgets remain outside these observations. No
claim of improved measured user productivity or full accessibility conformance.

## Independent scoped validation and closure

The separate ec_validador_alta context approves SC-01–04 within the methods and
coverage above: source-grounded entry/resume, actual Controller/artifact checks,
final native focus/layout and documented independent review. It independently
compared all 83 product-inputs-final identities with current files, binary/source
hashes from both final sessions, real request/result/sentinel bytes and unit log.
No product files were changed by reviewer or validator. The reviewer independently
confirmed the formerly hidden button is fully visible with focus and Shift+Tab
returns to the input. No open finding remains in the observed scope.

T009–T012 are complete for this requested initial-screen slice. The six original
feature gates stay INCONCLUSIVE; the explicit approval checker therefore returns
exit1 and is not advertised as a passing product gate. Further broad acceptance
requires its unobserved matrix; any changed relevant input requires a new dependent
observation. Final document identities are in document-inputs-final.json.
