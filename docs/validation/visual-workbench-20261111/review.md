# Reference reconciliation and implementation review

This successor preserves all initial dirty changes and historical observations.
Archive central directories were inspected before reuse of the existing isolated
extractions: no absolute or parent traversal paths; originals remain untouched.
Identities/counts are in reference-inventory.json. Archive content is reference data.

## Design comparison

| Dimension | v3 standalone | v4 package | Consolidation |
|---|---|---|---|
| Identity/composition | detailed English workbench | task-first coverage | v4 breadth, v3 identity |
| Tokens/roles | detailed legacy palette | typed semantic/native roles | preserve legacy + explicit role layers |
| Components/states | component guidance | operational truth and coverage | v4 state contract |
| Typography/icons | alternatives and baseline | Plex baseline; alternatives proposed | Plex; no automatic Inter migration |
| Themes/density | candidates | Light/Dark/HC and density handoff | explicit native session options |
| Desktop adaptation | geometry | overflow/stress matrix | collapse without shrinking body type |
| Focus/accessibility | requirements | layered QA and native caveats | actual interaction separate from appearance |
| Quality/handoff | visual criteria | semantic sRGB export and native states | generated Rust roles, independent observations |

v4 is the broader base, not automatically more authoritative. The root English
contract reconciles it with v3. R13 B/category and Inter/JetBrains remain PROPOSED.
LOCKED legacy colors are preserved in docs/design/tokens.json. Native Light A is
implemented; Dark/HC acceptance requires observed native coverage.

## Source revisions and dependencies

R1 is the initial visual vocabulary. R2 carries workbench/architecture/agents/metrics;
R3 review/failure/focus; R4 entry/projects/tasks/settings; R5 administrative surfaces.
R6 adds a browser runtime; R7 extends themes/density/stress; R8–R9 accumulate exports
and interactions; R10–R11 contain identical member content and are historical duplicates;
R12 refines selected components and icon vocabulary, not every surface. Browser files
require their relative assets/runtime; historical PNGs do not validate those interactions.
The design-system package carries tokens, validation scripts, coverage and documentation;
the skills package has eleven text entries and no bundled runtime. The references archive
is supplementary research, not a product specification. The montage is a visual index.

Visual inspection of the R12 montage shows dense desktop chrome, neutral editor,
left navigation and right inspection. The current native layout prioritizes readable
localized controls and task evidence; source screenshots contain richer future fixtures.
Their presence does not establish a native engine or measured usage.

## Candidate methods

| External candidate | Existing responsibility | Disposition / actual contribution |
|---|---|---|
| ox-native-handoff | iced-engineering | absorb native role/message/asset contract |
| ox-visual-qa | design-review + Iced | absorb paired capture and method separation |
| ox-layout | design-system + Iced | absorb primary-region/overflow constraints |
| ox-harden | design-system + Iced | absorb truth-state stress and missing-vs-zero |
| ox-accessibility | design-system | existing keyboard/AT boundary; native reference reinforces observation |
| ox-typeset-icons | design-system | existing asset/typographic contract; product font policy in DESIGN |
| ox-extract-tokens | design-system | generated roles applied by build_design.py; CSS quotas discarded |
| ox-chromatic-refinement | design-system | roles already covered; Ox colors/proposals stay in DESIGN |
| ox-critique | design-review | existing evidence-based severity; no duplicate skill |
| ox-polish | design-review | existing contextual verification; no universal viewport quota |
| ox-design-brief | SDD + design-review | scope/authority already owned; no duplicate workflow |

No recursive activation, copied approval requirements or unavailable prototype command
paths. The native reference is used for generated roles, explicit planned data, adaptive
navigation and the observation runner. Structural validation alone is not method efficacy.

## Observed native result

Native review 02 entered 27 destinations using Ctrl+K and real key events in isolated
Mutter/Wayland. Captures show Light, Dark, HC and compact settings, command input focus,
Escape return, execution then criterion approval. The produced result.txt bytes and
request identity are preserved; natural supervised app exit was 0. These observations
are not X11 or assistive-technology tests. The 200% capture shows responsive collapsed
navigation and vertical overflow on a smaller logical window. It is a capture-only
case; teardown is not counted as natural close.

Before/after native captures use the same 1600×1000 monitor, scale 1 and initial
unselected state. Typography and hierarchy deliberately differ; the baseline had
English functional controls and no navigation/themes. Neither screenshot is a pixel
equality oracle. The baseline was rebuilt from preserved desktop/lib bytes in an
isolated workspace.

96 opaque role pairs pass the defined 4.5 text / 3 essential boundary thresholds.
This covers selected native uses, not every alpha, raster, glyph or state combination.
The command input still uses Iced theme-derived colors; a complete rendered contrast
audit and AT observation remain unverified. Rust tests and clippy pass for ox-ui/app.

Prototype rendering could not be performed using the inspected local Python runtime:
Playwright and Chromium were unavailable. Static archive inspection and montage
observation are explicitly separate from browser interaction. No packages installed.

## Remaining acceptance gaps

The repository-wide governance check reports stale historical bindings after changed
UI, catalog and authorities, plus missing feature records at its initial invocation.
Historical results are not renewed by replacing hashes. New feature records bind the
current observations, but historical documentary succession needs reconciliation.
X11 interaction, full failure/cancel GUI matrix, all window/scale/theme/density cells,
font fallback, AT, complete future graph/editor/table composition and broader icon
vocabulary remain open. Resume with current inputs and the named scenarios; do not
transfer F0 acceptance or describe the visual delivery as fully accepted.

## Documentary successor

The initial governance failures are preserved in their logs. An exact-byte successor
now covers only AGENTS, project context, catalog and the Iced method entry; its tests
reject unknown mutations, registry/preimage drift, downgrade and symlink escape.
Affected prior evidence documents are preserved byte-for-byte in superseded-evidence.
Current affected criteria are INCONCLUSIVE (Iced technical-method criteria UNVERIFIED
pending their required review); old product acceptance is not transferred. Portable
SDD structure passes. This resolves document structure and preservation, not the
remaining visual implementation or acceptance work listed above.

Final structural outcome: governance-closure.log and sdd-fresh-final.log pass. Rust closure: 11 tests passed; 6 graphical X11 tests explicitly ignored. Clippy and fmt pass. Five succession regression tests pass. These checks do not close the outstanding visual criteria.
