# Visual regression with a trustworthy reference

Use when screenshot comparison is selected for a visual contract. This supplements
[case design](case-design.md) and [suite quality](suite-quality.md); it does not
replace interaction, accessibility or semantic assertions.

## Define what a difference means

Record the screen/component, relevant state, viewport and expected behavior.
Identify the reference's revision and approval basis: a reviewed requirement,
accepted design or independently checked consumer. A newly captured screenshot is
an unreviewed candidate, not a passing UI simply because no prior baseline exists.

Fix or record browser/runtime, rendering environment, fonts, scale, theme, locale,
data, clock and relevant versions. Wait for observable state readiness, including
fonts/images/asynchronous content where relevant, rather than a fixed sleep. Match
the state under test; two stable screenshots of different states are not equivalent.
Use authorized fixtures with explicit real versus simulated effects.

## Compare, investigate and update

1. Retain reference, candidate, diff, revision and capture configuration. Inspect
   the changed region with its contract rather than approving a global score.
2. Explain masks and thresholds by the variation they intentionally tolerate.
   Do not hide important text, focus, error, consent or destructive-action content.
   A tiny clipped warning can matter more than a large harmless background change.
3. Separate an intended product change, a regression, nondeterminism and an
   environment difference. Repeated capture or wider tolerance is not a repair.
   Preserve the failed evidence while finding the cause.
4. Update the reference only after reviewing the intended change against its
   authority and the project's existing review process. Do not automatically accept
   all new output or introduce a new approval body solely for this technique.
5. Exercise sensitivity with a representative defect in a disposable copy: remove
   critical text or alter a required state and confirm failure. An authorized design
   change should be accepted through the reference-update route, not ignored by masks.

Report which states/environments were captured, what masks omit, why the reference
was accepted and what still needs interaction or accessibility evidence. No image
similarity score proves overall correctness. If visual checking adds little beyond
existing assertions, use the simpler evidence.

Basis: Mohan, *Full Stack Testing*, physical 188–195 and 350–352; Aniche's
independent-oracle and mutation principles remain the shared method. No comparator,
browser framework or fixed numerical threshold is required.
