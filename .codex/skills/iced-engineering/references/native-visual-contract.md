# Native visual contract and observation

Use for translating a visual prototype into native widgets or reviewing a redesign.
Adapted method from the supplied visual-method package; no prototype policy is imported.

1. Establish actual toolkit version, font assets/licenses, renderer and logical window
   geometry. Resolve CSS calculations to explicit native roles; preserve semantic names
   across themes. Check generated roles against the source, not against screenshots.
2. Inventory primary work area and auxiliary navigation/inspection. Define min/max,
   collapse and overflow constraints before shrinking text. Density changes spacing,
   not meaning. Make collapsed tools discoverable and return focus to a visible control.
3. Derive a state table from domain truth. Stress unknown/stale/partial/cancel-requested
   and failed-to-confirm states. Historical success must never color a current unknown
   result. Missing values are not zero; synthetic fixtures carry an explicit label.
4. Pair captures using identical content, lifecycle state, window, scale, theme, density,
   font files and stabilization. Record differences that prevent pairing. Review actual
   captures for clipping, role collisions and inaccessible controls before cosmetic polish.
5. Exercise keyboard routing separately: traversal, text editing, activation, modal
   confinement, Escape and return focus. Check hidden controls and resize during work.
   Widget styling cannot supply focus behavior or assistive-technology semantics.
6. Bind findings to source/binary/font hashes and method. Separate prototype interaction,
   native rendering, native action outcomes and assistive-technology observation. Report
   coverage and exact missing cases; do not inherit a prototype's quotas or approvals.

A useful handoff records component purpose/consumers, roles/states, sizing/overflow,
messages, focus entry/exit, backend ownership and evidence. Product-specific values
belong in the product design reference, not in this reusable method.
