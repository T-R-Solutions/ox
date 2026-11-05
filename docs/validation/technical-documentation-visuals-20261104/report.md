# Technical documentation visual skill revision

Date: 2026-11-04. Request: refactor technical-documentation for Mermaid,
professional visual deliverables and technical/measurable definitions of beauty,
enterprise and modern presentation. Full-route artifacts are in
`sdd/features/technical-documentation-visuals/`.

## Delivered

- Revised skill entry retains source-grounded writing, API contracts, executable
  examples, maintenance and authorization boundaries; adds visual planning,
  renderer-aware Mermaid, professional SVG role icons and render inspection.
- Four progressively loaded references: visual-quality, mermaid, media-and-data,
  evaluation-cases. They distinguish standards from configurable editorial defaults.
- Measurable type/spacing/color/icon/density defaults, effective embedded label
  size, contrast, 360/768/1280 CSS-pixel/200%-zoom checks, source/data/license
  traceability, text equivalents and zero clipping/missing glyphs. Applicable
  blockers must pass individually; aesthetic ratings cannot average them away.
- Diagrams select architecture/sequence/state/ER/flow views by semantics; charts
  need data, units and uncertainty; screenshots retain real capture provenance.
  Unsupported icon rendering uses verified export or an explicit unverified gap.
- Exact-content skill/bridge successor registry plus minimal preservation-consumer
  integration, with historical hashes and manifests unchanged. Profile count and
  agents/openai.yaml are unchanged. The current entry is English per convention.

## Observed verification

| Method | Result | Limits |
| --- | --- | --- |
| skill-creator/scripts/quick_validate.py on the skill directory | Exit0, Skill is valid | Metadata/scaffold validation, not behavioral or visual proof |
| Five new preservation tests | All pass, including independent-copy imported-byte recovery and mutation/escape/symlink/scope denial | Bounded consumer behavior, not complete global acceptance |
| Fast governance suite | 38 tests,37 pass,1 fails for inherited README current-byte guard | Preserved fast-tests.log; failure is not hidden or called success |
| Independent isolated guide generation using the skill | Correct source-grounded Portuguese guide, two editable Mermaid views/text equivalents; missing renderer/icons and absent measurements explicitly pending | No rendering, chart data, image creation or reader study; actual outputs preserved in forward-test/*.bin |
| Rubric boundary arithmetic | 21:1 black/white passes;2.323:1 gray170/white fails; half-size14px source label is7px and fails default | Checks the numerical rule examples, not a rendered image's colors/geometry |
| Scoped verification through actual validator functions | Four decided authoring criteria have current schema2 bindings; four local skill links resolve | checks.json; this is not the unsupported CLI single-feature selection |
| Standard SDD validator, --root . | Exit0 | sdd-check.log; structural/content checks, not application execution |
| Global checker compared with pre-edit baseline | Same sole inherited README failure; no new diagnostic | current-governance-check.log vs baseline-check.log; global exit remains1 |
| Maintenance recovery | 485 governed files preserved and439/439 layout inputs reconstructed; inherited README failure remains | recovery-check.json; no false green recovery verdict |

The attempted CLI selection `--features sdd/features/technical-documentation-visuals
--require-approved --require-fresh` returned `No feature directories found` because
that flag takes a parent containing feature directories. The scoped verifier uses
the actual schema/trace/input validators against the existing feature without moving
it or bypassing other checks; it also compares global diagnostics byte-for-byte.
No code change to the SDD validator was made.

## Evidence succession and preservation

Pre-edit skill/bridge/consumer bytes and complete affected evidence envelopes are
in before/*.bin. dependency-remapping.json records66 historical input relocations
across25 features. Each old digest remains unchanged; new scoped dependency reviews
are separate observations. Previously appended convergence text from this turn was
removed back to exact pre-edit bytes when its downstream F0 input binding was
observed. Existing convergence content and operational product inputs are untouched.

The inherited README failure came from the preceding application-documentation
revision; this task neither repairs nor waives it. No acceptance state is upgraded
because the global checker has an error. New AC approvals apply to skill authoring
and bounded successor behavior only. Original integration AC-04 remains UNVERIFIED
for the changed README as before this task.

No Rust changes, image generation, renderer/package installation, publication,
commit, global setup or external source upload. The sandbox required permission
to create the skill's new references directory; it was granted for that exact path.
Official Mermaid and W3C sources were consulted; no external dependency was adopted.

Maintenance: reexamine affected method/resources and visual evidence when source
behavior, renderer, icon assets, fonts, themes, intended dimensions or export
requirements change. Future actual deliverables must perform their own render and
visual gates; this revision does not certify their appearance in advance.
