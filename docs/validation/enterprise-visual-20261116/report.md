# Enterprise desktop visual reformulation

Status: implemented and independently APPROVED for scoped EV-01–04 on 2026-11-17; broader feature acceptance remains open. Scope/criteria and ownership
are in product-visual-workbench's 2026-11-16 enterprise successor. Original current
bytes are preserved under before; prior observations remain historical.

The supplied screenshots show IntelliJ Home with docked projects/actions and a
large neutral canvas. Their version and interactive behavior are not established.
They guide hierarchy and geometry, not capabilities or third-party assets.

## Observed iteration

The first native run is stored under `baseline-wide`, but it rendered the new
candidate and is not a pre-change baseline. Source editing overlapped that run;
its source-stability flag is false. It exposed P1: a vertical rule with thickness
20 and unconstrained height expanded the S01/S02 chrome to about 418 pixels at
1440×900. Root and independent reviewer observed the same defect. This failed
candidate is preserved; corrected sources require a fresh build and capture.
The previous identity corpus provides a historical 1440×900 Start comparison,
not a paired all-surface binary baseline for this task.

## Stabilized implementation and checks

Final code/binary bindings and exact commands/exits are recorded in
`final-implementation-checks.json`; logs are `final-test.log`, `final-clippy.log`
and `final-build.log`. Observed: 42 unit tests, 4 integration tests and 1 shell
contract passed; one subprocess helper is intentionally ignored as a direct test.
Clippy with warnings denied and ox-app build exited0 offline. The new native-layout
regression checks welcome chrome<=60 and operational height>=window height−100
at640×480,1440×900 and2560×1080, directly guarding the observed separator defect.
These widget/layout tests do not replace rendered or keyboard observations.

Source changes: desktop.rs, desktop/views.rs, desktop/icons.rs and design.rs.
No identity PNG/font/palette or persistence/runtime source changed in this successor.
Shared sections, chrome, navigation groups/markers and footer reach all27 destinations;
this does not mean all27 backend capabilities are implemented or graphically tested.

Selected SDD freshness/convergence check returned0. The same whole feature with
`--require-approved --require-fresh --check-convergence` returned1 exclusively for
AC-01–06 INCONCLUSIVE. No historical broad acceptance is claimed or weakened.

## Documentation disposition

Reviewed/updated: DESIGN.md (enterprise geometry successor), docs/design/surfaces.md
(surface contract successor), reference-coverage.md (supplied-reference contribution),
components.md (navigation/icons/chrome), application/README.md (current user entry),
sdd/project.md and product-visual-workbench spec/plan/tasks/converge/evidence
(authorization, criteria, ownership, observations/limitations). Constitution,
architecture/context.md and visual-workbench ADR were reviewed; no changes needed
because this presentation redesign introduces no engine, effect, persistence format
or architectural boundary. Identity README/assets and tokens/fonts remain valid
unchanged consumers. Original docs and implementation bytes are retained in before/.

### Independent selection correction

The independent reviewer found that removing the shared Navigation(selected)
border affected tabs, tree, tools and preferences, while the new side marker
existed only in the navigation list. Coordinator restored `selection_indicator`
for the shared variant; the side marker remains. This preserves non-color
selection cues and the established component contract. Source/binary and repeated
focused-test/build bindings are now in `final02-implementation-checks.json`,
with both commands exit0. Earlier logs/captures retain their original inputs.

## Final native observation

`native-wide-final/result.json` (1440×900) and `native-small-final/result.json`
(640×480) record the final02 binary, stable observed source hashes, real private
Wayland sessions and natural exit0. The harness traversed representative
S01/S02/S04/S08/S13/S14/W00/A01/A03/A04/TW03 destinations, command palette/Escape,
manual opening of a disposable directory, genuine MRU registration, focus,
theme cycling and last creation controls after scrolling. Direct filesystem
oracles confirm sentinel preservation and no task creation from opening.

Coordinator and independent reviewer inspected the actual final images. Header
is compact, actions/readable paths fit, narrow Create/Cancel and recent Remove
are revealed by keyboard scrolling. Dark/HC and selected borders are visible.
Final independent review has no unresolved scoped finding; see independent-review.md.

Limitations: no AT or X11 observation, no complete WC failure/restart/collision
matrix, one recent in the GUI corpus, no full27-surface backend acceptance.
The complete content hierarchy of every planned surface is not claimed accepted. This focused evidence does not establish full-product
acceptance. Initial failures and their original inputs are retained.

## Final03 preferences refinement

After final02 review the root requested a bounded product-flow refinement: S13/S14
now default to theme/density/session scope. The existing Details toggle discloses
color/type/state specimens; task evidence badges and backend notices are removed
from these preference views. No control IDs or effects changed. Only views.rs
changed after final02; final03-implementation-checks.json binds the fresh tests,
Clippy and build (all exit0), binary a18fccef93a03622ed9cf48e6bf770857a3aacea95c4892777edfeeb1712b822.
Independent final02 verdicts remain historical; final03 captures and focused
independent reassessment follow below.

## Final03 observed outcome — 2026-11-17

Work crossed local midnight; the directory retains the request/start date. All
three final03 runs completed with natural exit0, stable inputs and final03 binary
a18fccef93a03622ed9cf48e6bf770857a3aacea95c4892777edfeeb1712b822.
Actual initial window configurations, read from native protocol observations:
final03-wide1440×900, final03-small640×480, final03-ultrawide2560×1080.
The ultrawide run explicitly maximized; the earlier native-ultrawide-final corpus
was a1280×855 window on a larger monitor and is not app-ultrawide evidence.

Wide/small replayed keyboard/open/history/sentinel/no-task/theme/creation-focus
scenarios and Compact selection; ultrawide captured representative surfaces.
Root/coordinator inspected final S14 preferences, small Compact and creation focus,
and actual ultrawide Start/W00. No clipping of critical actions was observed;
preferences now default to relevant settings. Details previews remain source-reviewed,
without an independent interactive Details replay in this corpus.

Current evidence: final03-implementation-checks.json and final03-{wide,small,ultrawide}/
result.json; native records bind implementation/fonts/assets/Cargo plus harness and
shared session helper. contract-inputs.json binds reviewed contracts and selected
skill entries/bridges. Independent follow-up verdicts are transcribed separately.

## Acceptance and closure

Independent reviewer found no unresolved scoped finding; independent validator
approved EV-01–04 on final03 inputs. See independent-review.md and
independent-validation.md for methods and limits. Tasks T023–T026 are complete
for this authorized visual successor. The broader AC/WC states are preserved.
No source changed after final03 observation. Final task/report edits transcribe
the independently returned verdict and documentation disposition only.

## Supplementary Details observation — 2026-11-17

After the independent verdicts, root ran `python3
docs/validation/enterprise-visual-20261116/native-details.py` in a private
1440×900 Mutter session. Exit0, natural application exit0 and stable recorded
inputs; the binary remains final03 a18fccef93a03622ed9cf48e6bf770857a3aacea95c4892777edfeeb1712b822.
Root inspected `final03-preferences-details/preferences-details.png` and
`preferences-details-hidden.png`: keyboard activation reveals the color/type
specimens and "Ocultar detalhes", then restores the default theme/density view.
This supplements the earlier source-only Details observation; it does not expand
the independent verdicts or establish assistive-technology support. The focused
harness and result retain method/input identities beside the captures. No product
source changed. Documentation disposition: this report records the additional
method/result; the reviewed DESIGN/components/application guide already describe
the same Details behavior and require no contract change.
