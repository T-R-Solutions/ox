---
name: design-system
description: Create or evolve shared UI tokens, components, variants, states, and usage contracts. Use when implementing reusable interfaces, resolving component inconsistency, or maintaining a design system. Do not use for unrelated backend work or a purely aesthetic opinion; use design-review for evidence-based journey evaluation.
---

# Design System

Make shared interface behavior understandable, accessible and maintainable within the existing product. Preserve established conventions unless task evidence justifies a change. Basic accessibility and correctness apply even when this skill is not selected.

## Scope and evidence

Inspect the existing component library, tokens, design references, consuming screens, target platforms, user tasks and acceptance criteria. Separate product requirements from technical decisions, implementation and validation. Identify missing evidence without inventing brand rules or user research.

This skill owns reusable interface contracts and their evolution. A one-off screen may need only existing components. Cross-screen usability investigation belongs to design-review; specialized threats belong to application-security; measured runtime bottlenecks belong to performance-engineering. Load another skill only for a concrete unresolved responsibility, never the whole library.

## Workflow

1. **Locate the contract.** Find the actual component entry points, token definitions and consumers. Record purpose, content constraints, semantics, inputs/events, state transitions and compatibility obligations. Start from the requested change rather than rebuilding the system.
2. **Compare reuse choices.** Reuse an existing pattern when purpose and behavior agree. Add a bounded variant when shared meaning remains stable. Separate components when divergent responsibilities produce interacting flags or incompatible semantics. Similar pixels alone are insufficient evidence for consolidation. Read [pattern decisions](references/pattern-decisions.md) for this choice.
3. **Specify relevant states.** Cover default, hover, focus, selected, disabled, loading, empty, error and success as applicable. Define entry/exit conditions, recovery, content preservation and concurrent-action behavior. Explain unavailable actions when users need that information. Do not add irrelevant states mechanically.
4. **Implement semantics and interaction together.** Prefer appropriate native controls; maintain accessible names, keyboard operation, focus transitions and announcements. A style token or ARIA role does not supply behavior. Use [accessibility verification](references/accessibility.md) when changing interaction or presentation.
5. **Evolve proportionally.** Use role-based tokens and explicit variants where they reduce meaningful duplication. Identify affected consumers; document migration and deprecation for breaking changes. Avoid a new framework, taxonomy or publishing pipeline without a concrete maintenance need.
6. **Verify in context.** Exercise representative consumers with realistic long/short, missing, translated and erroneous content. Check responsive layouts, interaction and recovery. Run existing relevant checks; record checks unavailable in this environment.

## Decision constraints

- Preserve user-visible and programmatic contracts during refactoring, or identify the intended change and migration.
- Visual consistency does not justify obscuring consequences, inferring consent, removing keyboard access or hiding error recovery.
- Treat component examples as demonstrations with stated limits. Static screenshots cannot prove focus behavior, assistive-technology support or performance.
- Do not copy historical library APIs or book timing/size constants without checking the actual target version and requirements.
- Shared vocabulary and ownership help only when contributors can find and maintain the pattern; no universal atomic-design hierarchy or centralized approval process is required.

## Completion and report

Report the changed contract and consumers, why reuse/variant/separation was chosen, exceptions and migration costs, and evidence from validation. Distinguish visual inspection, automated checks, manual keyboard tests and assistive-technology tests. Do not claim accessibility conformance from a component preview or scanner. Keep unresolved assumptions and concrete follow-up checks visible.

Other named skills are optional specialist suggestions. Use them only when available and needed for a specific unresolved question; their absence does not prevent using this skill. Report any expertise or verification gap without claiming a handoff occurred.
