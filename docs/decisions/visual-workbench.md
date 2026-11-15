# Native visual workbench consolidation

Status: local implementation decision, 2026-11-11; native acceptance tracked separately.
Authority: explicit visual-development request; full SDD product-visual-workbench.

Use root DESIGN.md as the single maintained English visual contract. v4 supplies
broader component/state/handoff coverage; v3 supplies legacy detail. Neither package
may override constitution or domain truth. Preserve Light legacy values; neutral
canvas is a semantic surface choice. R13 category B and alternative typefaces remain
proposals. IBM Plex is the implementation baseline, with bundled OFL notice.

Keep 31 skill identities and bridges: absorb reusable native methods into the existing
Iced specialization; do not create eleven overlapping Ox-specific skills. Existing
metadata/profile needs no membership change. New reference has no executable dependencies.

Presentation owns theme, density, navigation, command search and drafts. Controller
owns effects and evidence; unavailable capabilities expose integration boundaries.
Revisit when real providers, document services, storage, graphs or AT support arrive.
