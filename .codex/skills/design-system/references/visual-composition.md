# Visual direction and layout composition

Use when establishing shared visual language or composing screens from the system.
Keep an adopted brand, toolkit and functional model as inputs. An existing screen
repair usually needs a focused correction, not a fresh visual direction.

## Choose a direction that supports the task

Write a short design brief from actual requirements: audience and input methods,
main task, information priority, content volume, target window range, platform,
existing assets, theme/accessibility needs and decisions already adopted. Mark
unknowns. A product category is a search aid, not evidence that its users prefer
a particular palette, typeface or visual effect.

When direction is unresolved, compare a few materially different treatments of
the same content. Describe their typography, hierarchy, density, color roles,
surface/depth and motion choices; state the cost and task fit of each. A color
swap is not a structural alternative. Preserve the requested style and improve
its readability rather than substituting an unrequested aesthetic.

Treat glass, soft relief, retro chrome, clay, neon and bold borders as optional
surface languages. They do not determine navigation, data semantics or safety.
For translucent surfaces inspect the composed foreground against actual
backgrounds; provide a legible opaque treatment where blur/transparency is
unavailable or reduced. Shadows cannot be the sole control boundary or focus cue.
Use spectacle only when the task and brand justify it; evaluate reduced motion
and rendering cost before adding repeated effects to dense screens.

## Allocate space by content constraints

Map primary work, navigation, context inspection and transient tools. Include
only regions the task needs: neither a three-column shell nor a KPI grid is a
universal layout. Give each region a minimum usable size, preferred range,
flexibility, overflow rule and collapse/reopen behavior. Give each scroll region
an owner. A fixed toolbar must leave the last row and focused action reachable.

Calculate the budget: available width minus chrome, visible panes, dividers and
gutters must leave the primary region above its tested minimum. Do the same for
height, including toolbars, tabs, composer, keyboard or status strips where present.
Derive collapse thresholds from these constraints and real localized content.
Test around the threshold, not just at familiar device presets. Prefer stacking,
progressive disclosure or a recoverable auxiliary panel to shrinking essential
text. Do not turn a comparison table into cards if that removes the comparison.

Use consistent spacing relationships for inline items, control groups and sections.
Choose a base rhythm from existing tokens; allow documented optical adjustments.
Align text baselines and repeated label/value edges. Keep primary content dominant
through placement and area before increasing saturation, font size or decoration.
Choose density separately from font size: compact geometry still needs readable
labels, targets and visible focus. Hover/pressed feedback should preserve target
location and surrounding layout.

## Type, color and assets as a coherent system

Define type by roles: heading, body, control, metadata, numeric data and code.
Specify actual available family/fallback, weight, size and line height. Verify
licenses, glyph coverage, diacritics, ambiguous code characters and fallback metrics
before changing font families. Inspect long titles, orphaned heading words, wrapped
badges and tabular numbers with real strings. Ellipsis needs a usable route to
the full value; do not hide essential distinctions between similar paths.

Map brand, action, selection, focus, status and data categories independently.
Evaluate foreground/background pairs in each relevant state and theme, including
overlays. A palette recommendation does not establish accessible pairs. Use the
applicable criteria and exceptions in [accessibility](accessibility.md).
Use a consistent icon family, optical size and stroke; expose an accessible name
for icon controls and redundant text for consequential states. Library popularity
does not justify installing new dependencies or replacing existing assets.

For charts, start from the question (comparison, trend, distribution or relation),
units and available data. Choose an encoding that preserves that question at the
target size; label scales, missing/stale data and aggregation. Provide inspectable
values where the visual alone is insufficient. Avoid invented series, decorative
charts and automatic claims that a catalog's chart choice fits the task.

## Deliver a usable handoff

Record the chosen direction and rationale in the existing design authority; trace
tokens to reusable components, variants and consuming screens. Record geometry,
overflow, relevant states, focus behavior and content fixtures. Page exceptions
need a reason and boundary so they do not silently override shared semantics.
Avoid creating a competing generated master file beside an established authority.
Verify the same fixtures across representative sizes/themes; report what was
rendered, what was interacted with and what remains a proposal.

## Source basis

Original synthesis informed by [desktop design pack, pinned revision](https://github.com/umutc6230/ui-design-skills-pack/tree/4ffc9d638e32f1332fc7ac74e3060e6278743d4b/skills)
(particularly 01–08, 11–14, 16–19) and [UI UX Pro Max workflow](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/e59ff376a41f7ca47b7541ad5c116495cbade3ee/cli/assets/templates/base/skill-content.md),
inspected 2026-11-16. These are inspiration and candidate retrieval methods, not
validated design outcomes. No palettes, fixed geometry, generated framework code
or style catalog are imported. Product policy remains with the consumer.

## Translate a Windows or IDE reference

Use the consumer's maintained visual contract to identify the adopted product,
edition/version, source URL or capture, and which surfaces it governs. A generic
Windows guideline cannot identify a particular IDE's exact palette or geometry.
Distinguish source recommendations, deliberate consumer adaptations, existing
implementation and newly observed behavior. Keep product names and mandatory
brand choices in the consumer contract so this method remains reusable.

Build a source-to-role map: application chrome, primary document canvas, navigation,
context panes, tabs, commands, status and transient overlays. For an engineering
workbench, assess usable document area and discoverable tools before decorative
cards. Record compact-control and touch-target trade-offs per input mode; density
must not silently reduce text or keyboard reachability. Define selected, focused,
hovered, pressed, disabled and window-inactive states independently.

Treat typography, geometry, icons, color, layers, materials and motion as separate
translation decisions. Prefer semantic roles and theme-aware states to sampled
screenshots. Keep a readable opaque surface when platform effects are unsupported,
transparency is reduced or contrast requires it. Motion explains state/spatial
change; it must not delay work or become essential to understanding. Confirm
font/icon redistribution rights before adding source assets. Record deviations
from the reference with a task/accessibility/platform reason and a verification case.

Source basis: [Windows design](https://learn.microsoft.com/en-us/windows/apps/design/),
[materials](https://learn.microsoft.com/en-us/windows/apps/design/signature-experiences/materials)
and [inclusive design](https://learn.microsoft.com/en-us/windows/apps/design/accessibility/designing-inclusive-software),
consulted 2026-11-17. These are Windows-oriented guidance, not proof of a consumer's
native support, universal IDE styling or an instruction to change frameworks.
