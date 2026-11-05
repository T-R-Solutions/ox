# Visual quality contract

Use for a new visual document or substantial redesign. Preserve the host's design
system. Values below are **editorial defaults**, not scientific thresholds,
universal accessibility requirements or proof of reader effectiveness. Record
justified adaptations to the destination. A short text fix needs no visual quota.

## Translate the brief into observable outcomes

| User language | Technical meaning | Observable acceptance |
| --- | --- | --- |
| Beautiful | Hierarchy, composition and consistent rhythm | One purpose per figure; consistent heading levels without skips; aligned containers; declared spacing/type/color tokens; no overlap, clipping or inconsistent treatments of equal roles |
| Enterprise | Semantic precision, visual vocabulary, provenance and reliable delivery | Named boundaries/roles; meaningful edges; one coherent icon family; all technical claims/data/assets traceable; renderer and licenses recorded; no missing icons or remote dependencies in offline output |
| Modern | Legible responsive vector presentation with restrained styling | SVG diagrams/icons where supported; readable embedded labels; explicit theme handling; editable sources; no fake 3D, ornamental gradients, emoji-as-component-icons or animation needed for understanding |
| Rich | Complementary representations answering distinct questions | Architecture, sequence, state, plots and annotated screenshots selected by need; no repeated graph to inflate visual count |

## Defaults when the host provides none

- **Type:** one sans-serif text family plus monospace for code; up to three
  weights. Body 16 px (12 pt print), diagram labels at least 14 CSS px (10.5 pt)
  **after embedding/scaling**, captions at least 12 px (9 pt). Prefer type levels
  16/20/28/36 px and line height 1.4–1.6. Native Markdown controls typography;
  measure the outcome instead of assuming custom CSS will apply.
- **Spacing:** 4 px base grid with 8/16/24/32 px roles. In authored vector layouts,
  alignment deviations within 2 px and clearance at least 8 px between unrelated
  text/edges at target scale. Automatic graph layout is judged on clearance and
  readability, not a fictitious manual grid. Use equivalent spacing in print.
- **Color:** neutral surfaces/text, one primary accent and up to three semantic
  accents per figure. Categorical data may need more, with labels/patterns.
  Keep role meanings stable. Color alone must not distinguish status or ownership.
  Do not invert brand marks or photographs to force dark mode.
- **Icons:** prefer an established SVG family, normally a 24-unit grid with one
  selected 1.5–2 unit stroke weight; no mixed outline/filled/isometric styles for
  equal roles. Render role icons at least 20–24 px where appropriate. Mermaid
  icon nodes may require larger dimensions: preserve that minimum. Every semantic
  icon has a visible label. A rectangle is a container, not the role illustration
  in a designed architecture overview.
- **Density:** start with at most 12 primary nodes/20 edges per overview, about
  six sequence participants and two label lines per node. These are split
  triggers, not model limits. Use linked overview/detail views rather than tiny
  labels; retain necessary error/recovery paths and actual relationships.

## Release gates: all applicable gates must pass

| Gate | Method | Pass condition |
| --- | --- | --- |
| Truth | Compare components, edges, states, values and screenshots with identified sources | No invented capability, relationship, measurement or UI state; illustrative material clearly labeled |
| Hierarchy/consistency | Inspect outline and equal semantic roles | No skipped heading level; figures near relevant text; token, line and icon conventions agree |
| Contrast | Measure actual rendered foreground/background pairs | Normal text at least 4.5:1; meaningful graphics at least 3:1 against adjacent colors; labels/patterns supplement color |
| Legibility/layout | Inspect final embedded size and zoom | No clipping, overlapping labels, missing glyphs, arrows through text or ambiguous endpoints; effective minimum label size met |
| Responsive reading | Web previews at 360/768/1280 CSS px and 200% zoom, or declared destination sizes | Prose reflows; diagrams remain readable by splitting or an explicit full-size/zoom route plus equivalent text; wide genuine 2D diagrams may scroll in a contained region |
| Theme/export | Inspect each declared theme/export | Text, edges and icons visible; light-only figures have a clearly bounded opaque surface; no false native-theme adaptation claim |
| Accessibility | Inspect source, SVG and delivery markup | Caption plus alt/accessible title/description as supported; equivalent prose/table for essential meaning; no icon/color-only states |
| Maintenance | Inspect inventory and reproduce selected render path | Editable source, data, renderer/version, origins/licenses, output paths and review recorded; offline output has no missing external icon/font load |

Contrast thresholds are grounded in W3C
[text contrast](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)
and [non-text contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html).
This profile conservatively uses 4.5:1 for normal labels; passing these gates does
not certify full WCAG conformance. Check adjacent colors in the rendered artifact,
not just palette swatches on white. Other numbers are configurable house defaults.

Do not average away blockers: invented facts, unreadable labels, unlicensed assets
and failed rendering cannot be excused by an aesthetic score. Record each gate
as passed, failed, not executed or not applicable with a reason. Optional ratings
can compare candidates but do not replace gates or reader studies.

## Review record

Use the project's existing evidence format. Useful fields: figure ID/question;
source/data identity; editable/export paths; renderer/version/config; icon family
and license; viewport/theme/export; measured contrast/effective label size;
observed defects/corrections; result/limits; owner/update trigger. Distinguish
manual inspection from automated checking and actual reader-task completion.
