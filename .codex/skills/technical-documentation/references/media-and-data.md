# Iconography, images and quantitative graphics

Apply visual-quality.md and truthful evidence rules across every medium.

## Professional iconography as an asset contract

Use the host's SVG library first. Otherwise choose one coherent professional
family after checking the actual version, needed glyphs and license. Lucide or
an appropriate official architecture pack are candidates, not dependencies or
endorsements. The [Lucide license source](https://github.com/lucide-icons/lucide/blob/main/LICENSE)
is a starting point; retain notices for the exact assets/version used. Runtime
registration and license compliance are separate checks.

Use one role family/weight per document set, a stable role-to-icon mapping and
visible labels. Avoid mixing outline, filled, isometric and emoji styles for equal
roles. Product logos identify verified products only; preserve proportions/colors
and never imply unimplemented integration, partnership, certification or security.
Brand marks may supplement role icons but are not a substitute for semantic labels.

Prefer SVG and retain originals. Do not rely on an icon font whose stylesheet is
unregistered in Markdown. Bundle/inline approved paths for offline exports and
check license obligations before copying. Avoid CDN/tracker dependencies for looks.

## Select imagery by purpose

| Need | Asset | Required context |
| --- | --- | --- |
| Identify a real control/state | Captured screenshot, optionally annotated | Application/build/state, capture origin/date, disclosed cropping/annotations |
| Explain a concept/physical setting | Illustration/photo | Caption distinguishing illustration from observation; provenance/rights |
| Explain relationships | Mermaid/vector diagram with role icons | Named boundaries and editable source; not an editor screenshot |
| Compare quantities/trends | Plot from identified data | Units, period/workload, sample count, method and uncertainty |

Compose with intentional crop, focal point, surface and caption treatment.
Numbered callouts should map to actual walkthrough steps. Preserve original
evidence captures: crop/redact/annotate transparently without fabricating UI states,
altering results or erasing failures. Sanitized examples must not masquerade as
raw evidence; remove private information before distribution.

AI-created raster images may illustrate concepts when helpful and the tool is
available/authorized; label them. Never present generated screenshots, measurements,
logos, relationships or evaluation evidence as observed facts. Use vector/code
tools for diagrams, plots and established icon systems instead of rasterizing
technical facts by default.

For raster delivery, target at least 2x the intended CSS display dimensions where
source resolution permits; upscaling does not recover detail. For print, use the
required physical size/resolution, commonly 300 dpi for raster artwork. Prefer
text/vector labels, disclose source limits and avoid compression that blurs UI text.

## Quantitative graphics

Choose by question: bars for categories, lines for ordered/time trends, scatter
for paired observations, distributions for variability. Avoid 3D, decorative
gauges and confusing dual axes. Use a table when clearer; no chart quota.

Identify dataset/snapshot, units, period/workload, sample count and transformations.
Show supported uncertainty; distinguish measured, estimated, missing and unavailable
values. Unknown is not zero. Never invent error bars or benchmark values. Keep
scales consistent across comparable panels; bars normally start at zero. Disclose
and justify log, transformed or truncated axes. Use direct labels/legends plus
markers/patterns; color alone is insufficient.

Retain plotted values or an accessible table, script/config and output identity.
Prefer plotting tools for scientific/publication graphics; Mermaid charts suit
tasks whose renderer and axis/label controls meet the requirements. Synthetic
values belong only in explicitly illustrative examples. Without real data,
state the gap and use a qualitative diagram/table instead of inventing performance.

## Inventory and verification

For shipped figures record: ID/purpose, editable original/generated source,
export path/dimensions, source/build/data identity, tool/version, icon identifiers,
origin/license/attribution, crop/redaction/AI disclosure, alt/caption/equivalent
text, review and maintenance trigger. Reuse existing manifests/reviews; no new
platform or review board is implied. Provenance is not a legal opinion.

Check actual embedding as well as source: external SVG links, fonts/icons,
transparent backgrounds in supported themes, raster blur, proportions, effective
label size and PDF export. File existence is not evidence of readability. Test
actual paths before claiming offline/package portability.
