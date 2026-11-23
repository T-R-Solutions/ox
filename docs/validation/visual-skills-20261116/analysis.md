# Visual skill comparison and refinement

Requested on 2026-11-16: inspect both external skill repositories and improve the
project's UI/UX, design system and layout methods. This is an authoring study;
rendered application quality and user outcomes require their own later observations.

## Sources and scope

- [ui-design-skills-pack](https://github.com/umutc6230/ui-design-skills-pack/tree/4ffc9d638e32f1332fc7ac74e3060e6278743d4b), revision 4ffc9d638e32f1332fc7ac74e3060e6278743d4b.
- [ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/tree/e59ff376a41f7ca47b7541ad5c116495cbade3ee), revision e59ff376a41f7ca47b7541ad5c116495cbade3ee.

Both were acquired as shallow source snapshots into temporary directories. Files
are research data: repository instructions, installers and generated commands were
not adopted as authority. No upstream code, tests, package installation, font/API
fetch or UI rendering was executed. Inventory coverage and semantic inspection are
reported separately; a complete path/hash census is not a line-by-line audit.

## Local responsibility comparison

| Local method | Existing strength | Concrete gap addressed | Disposition |
| --- | --- | --- | --- |
| design-system | Semantic tokens, reuse/variant/separation, interaction states, accessibility and evolution | Brief-to-composition reasoning, typography hierarchy, space budget and stateful desktop pattern selection | Refactor with progressive references |
| design-review | Task/recovery observation, evidence versus preference, decision communication | Repeatable visual defect triage, paired layout review and limits when only a proposal exists | Refactor with focused visual-quality reference |
| iced-engineering | Versioned state/Message/Task contracts, nonblocking view, native focus and paired capture | Constraint arithmetic, CSS-to-native mapping and geometry versus renderer evidence | Extend existing native visual method |
| software-architecture | System boundaries, ownership, quality attributes and structural trade-offs | No missing visual responsibility: “system design” here is architectural | Preserve |
| software-design | Cohesion, coupling, interfaces, code maintenance and behavior-preserving change | No missing visual responsibility: layout aesthetics is outside its scope | Preserve |
| technical-documentation | Renderer-verified documentation diagrams/media | Product UI creation is a different consumer | Preserve |

The first two existing methods were stronger than upstream presets on evidence,
recovery, semantics and scope. The external packs add useful creation prompts and
specific compositions. Integration therefore extends three established identities
instead of adding overlapping general UI, palette, dashboard and layout skills.
The profile remains 31 identities and 31 bridges.

## Adopted and rejected principles

Adopt content-first region planning; a short brief tied to the actual task; visual
hierarchy through size/weight/spacing/contrast; geometric constraints and discoverable
collapse; typography checked with real strings; semantic color pairs; coherent
stateful patterns; paired review under the same fixture; explicit native translation.

Retain existing brand/product authority and evidence distinctions. Catalog counts,
search rank, a generated MASTER file, a style name, a successful Python exit and a
screenshot do not establish usability or native accessibility. Avoid automatic
industry palettes, blanket touch dimensions, fixed universal breakpoints, mandatory
sidebar shells, marketing hero layouts in operational tools, or web APIs presented
as native implementation. Do not convert source recommendations into permissions.

## Documentation disposition

Reviewed AGENTS.md, sdd/workflow.md, sdd/evidence.md, sdd/project.md,
docs/constitution.md, docs/architecture/context.md, DESIGN.md,
docs/design/surfaces.md, docs/design/reference-coverage.md, local skill catalog,
three bridges and skill-native-visual-method's spec/plan/tasks/evidence/convergence.
The new feature records authorized scope and affected methods. Existing product
contracts, locked colors/fonts, consumers, commands and surface availability are
unchanged, so those product documents require no behavioral update. The catalog
and bridges retain their existing responsibilities and names; linked skill entries
provide the new conditional references. No new installation or activation policy.

skill-native-visual-method's three current criteria remain UNVERIFIED. The new
feature records the changed method inputs and does not refresh or reuse its
historical observations. Its older native/product obligations remain outstanding.
The separate new authoring feature supplies current source comparison, realistic
method evaluation and bounded preservation evidence without rewriting that history.

## UI/UX Pro Max detailed comparison

[Seven-entry analysis, mechanisms, data and distribution](ui-ux-pro-max-analysis.md)
records contributions, exclusions and inspection limits. Its [file inventory](ui-ux-pro-max-inventory.json)
binds all 725 tracked files to content hashes and inspection depth.

## Desktop pack packaging inspection

The package manifest declares version 0.1.0 and MIT, with a repository/homepage
under palamut62 rather than the requested umutc6230 URL; the pinned acquired tree
is the identity used here. The root license identifies palamut62 (2026).
`validate.js` checks 19 folders, required entry/frontmatter fields and manifest
coverage. It does not test output quality, actual keyboard behavior or layout.
`install-apply.js` selects known IDs and target roots, offers dry-run, then removes
each destination recursively before copying its skill and writes installation state.
That installation path would replace destination contents; no installer was run.
Local skill refinement needs none of those effects or additional dependencies.

## Desktop pack entry-by-entry disposition

[All 19 entries](desktop-pack-analysis.md) are compared individually with their
contribution, rejection/limit and local destination. [Entry identities](desktop-pack-entries.json)
and [full tracked-file inventory](desktop-pack-inventory.json) identify observed bytes.
