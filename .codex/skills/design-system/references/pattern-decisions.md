# Pattern and token decisions

These are contextual engineering recommendations synthesized from the books. PDF locations use one-based physical pages. Historical vendor screenshots are examples, not current product specifications or measured benefits.

## Reuse, variation or separation

**Action and context:** Inventory real instances by user purpose, content structure and behavior before consolidating a shared component. Reuse when these agree; use a variant for bounded differences; separate when goals or lifecycle differ.

**Evidence:** Kholmatova, *Design Systems*, chapter 8, PDF 185–212, especially book-item comparison PDF 199–201; MacDonald, *Practical UI Patterns*, chapters 1 and 3, PDF 19–39 and 109–158.

**Rationale:** A shared implementation reduces repeated decisions only when the shared concept is stable. Merging visually similar but semantically different controls transfers complexity into flags and callers.

**Exceptions and costs:** A small one-off may remain local. A shared component adds compatibility and ownership costs; separation duplicates some styling. Avoid premature generalization for imagined future consumers.

**Validate:** Compare representative consumers and change scenarios, not just the component gallery. Verify content, events, semantics and states before and after.

**Illustrative example, not executed:** A product-summary card and a promotional feature tile share a border but have different content hierarchy and navigation. Keep separate semantic components sharing surface tokens. Two product cards differing only in optional author metadata can share one component with documented missing-data behavior.

## Tokens carry meaning

**Action and context:** Define tokens around meaningful roles and relationships where repeated decisions need coordination. Preserve useful primitives beneath semantic roles; inspect foreground/background pairs, density and emphasis together.

**Evidence:** Kholmatova chapter 9, PDF 213–243; color relationships PDF 223–229 and motion examples PDF 235–236.

**Rationale:** A palette alone cannot express which color indicates an error or which surfaces it must work against. Naming by role decouples use from a particular visual value.

**Exceptions and costs:** Not every value needs a public token. Excessive layers make changes difficult to trace; brand and platform differences may need bounded variants. Example scales and animation durations are not universal defaults.

**Validate:** Trace changed tokens to consumers, inspect all applicable states and themes, and measure relevant contrast or motion behavior in the actual interface. Do not infer quality from token count.

## States are part of the public contract

**Action and context:** For a component with asynchronous work or user input, document its transitions and recovery policy alongside appearance.

**Evidence:** Kholmatova chapter 10, PDF 244–285, state matrix PDF 269; MacDonald chapters 2–3, PDF 40–158.

**Rationale:** Consistent appearance without a consistent recovery path leaves consumers to reinvent behavior.

**Exceptions and costs:** A static text component does not need an asynchronous state machine. Keep states and examples limited to actual behavior; elaborate fixtures become maintenance liabilities.

**Validate:** Trigger errors and empty results, preserve entered content where appropriate, prevent accidental duplicate actions, and test focus after removal or dismissal. A disabled style must agree with actual event handling.

**Illustrative before/after, not executed:** Before: submitting a form clears fields before a failed request. After: pending state retains values; failure identifies the problem and offers retry without losing edits. This intentionally changes the failure contract and needs acceptance criteria, not a claim of behavior-preserving refactoring.

## Maintain the system as a product

**Action and context:** Document purpose, usage constraints, working examples, ownership and changes at the point contributors use them. Select a taxonomy by findability. Define migration for externally consumed changes.

**Evidence:** Kholmatova chapters 5–7 and 10, PDF 108–184 and 244–285; MacDonald chapter 4, PDF 159–208.

**Rationale:** Shared understanding and maintenance practice determine whether a library remains useful. Centralization, strictness and modularity are separate choices.

**Exceptions and costs:** A small local library may need only concise inline documentation. Synchronizing a preview must not silently deploy production changes. Static screenshots can bootstrap documentation but become stale and omit interaction.

**Validate:** Have a representative contributor locate and apply the pattern; inspect existing consumers and migration instructions. Measure local adoption or task effort before asserting productivity gains.

### When maintaining an interactive gallery

Identify the component revision, example fidelity, data sources, navigation and
submission destinations. State which effects are simulated and which are real,
and which states or integrations the preview omits. Use data and destinations
authorized for that demonstration; a working submit button is not permission to
write to a real service. Do not report simulated success as completed integration.

Check that a contributor can identify what will be sent, where it goes and what
pending/error/success mean. Verify the real consumer separately; a static preview
cannot establish keyboard, network or recovery behavior it does not exercise.
Reuse the project's preview mechanism rather than adding a framework or approval
process. Basis: MacDonald chapter 4, physical PDF 180–193, especially 184;
these effect-boundary checks are engineering synthesis, not a claim of an incident.
