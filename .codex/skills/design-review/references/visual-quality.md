# Visual quality review through actual content

Use for composition and visual hierarchy findings. Keep the task, existing brand
and adopted design contract as the evaluation frame. A style name or trend rank
is not a quality criterion.

Inspect the captured interface at its real size before proposing polish. Identify
the main task and first relevant action; verify that placement, scale, grouping and
contrast make them findable. Compare repeated regions for baseline alignment,
spacing rhythm, type roles, icon weight and consistent emphasis. Ask whether
surface treatments explain grouping or merely compete for attention. Distinguish
reproducible defects from aesthetic preferences and untested audience assumptions.

Use the same content and state for alternatives. Include long translated labels,
similar paths, large numbers with units, missing data, partial errors and wrapped
headings. Inspect narrow and short windows, large text, relevant themes and the
points where regions collapse. Record clipping, unstable row/control positions,
unreachable overflow, hidden focus and truncated information needed for decisions.
Changing fixtures between captures prevents a fair visual comparison; identify
that limitation rather than attributing all differences to the redesign.

Inspect typography at reading size, including fallback glyphs and code characters.
Check foregrounds against the actual composed background, especially with blur,
images and overlays. Evaluate light/dark independently; a uniform inversion cannot
establish state contrast. Verify focus, selection, error and disabled semantics
through interaction separately from appearance. Reduced-motion and keyboard paths
need actual exercise; a screenshot supports neither claim by itself.

Prioritize findings by consequence: inaccessible/unreachable task, misleading state
or lost content; legibility/navigation friction; repeated system inconsistency;
then cosmetic refinement. For each material finding record artifact/state, observed
condition, affected task, proposed repair and a replay that could falsify the fix.
Do not fabricate scores or a required count of defects. Report inspected coverage
and missing behavior instead of a blanket “professional” or “accessible” verdict.

Source basis: original synthesis informed by the [desktop pack](https://github.com/umutc6230/ui-design-skills-pack/tree/4ffc9d638e32f1332fc7ac74e3060e6278743d4b/skills)
and [UI UX Pro Max review workflow](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/e59ff376a41f7ca47b7541ad5c116495cbade3ee/cli/assets/templates/base/skill-content.md),
inspected 2026-11-16. Their checklists and style labels are prompts for inspection,
not proof of usability, conformance or consumer acceptance.

## Review Windows or IDE reference fidelity

Start from the consumer's explicit reference identity, applicable surfaces and
approved deviations. A claimed edition-specific appearance needs edition-specific
source evidence; shared product-family screenshots support only that shared scope.
Compare shell hierarchy, primary-work area, pane/tab/command organization, density,
type/icon roles, theme states and transient layers using matched task fixtures.
Do not substitute a generic Fluent demonstration for the chosen IDE composition.

Classify reference mismatches separately from functional defects. Check compact
chrome at large text/DPI, keyboard-only pane navigation, visible focus after resize,
long localized paths, inactive windows and unavailable commands. Evaluate opaque
fallbacks, high-contrast presentation and reduced motion where supported. Record
which cases were actually rendered or exercised; visual likeness does not prove
native accessibility, resizable docking or persistence. Reject claims of complete
reference coverage when only the landing page or a single theme was inspected.

Method informed by [Windows design](https://learn.microsoft.com/en-us/windows/apps/design/)
and [inclusive design](https://learn.microsoft.com/en-us/windows/apps/design/accessibility/designing-inclusive-software),
consulted 2026-11-17; the consumer selects its actual reference and acceptance scope.
