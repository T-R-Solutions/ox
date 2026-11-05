---
name: iced-engineering
description: Implement and review Iced desktop interfaces using explicit state, messages, tasks, subscriptions and widget contracts. Use for Iced-specific rendering and interaction; skip non-Iced UIs and visual strategy alone.
---

# iced-engineering

## Responsibility and selection

Implement desktop GUIs with Iced using message modeling, state, Tasks/Subscriptions, custom components, panes and responsive performance.

Select: Iced code, update/view models, custom widgets, split panes, themes, accessibility and graph visualization.

Do not select: Do not select for projects without Iced; do not replace design-review/design-system when deciding visual hierarchy.

## Inputs and gaps

Iced version and features, GUI state, flows, events, size constraints, accessibility and latency.

Inspect actual contracts and resources before execution. A missing version requires consulting the corresponding documentation; a missing permission prevents the dependent effect. Record the gap, its impact and how to resolve it while continuing independent work. Examples in this package are evaluation contracts, not APIs or policies imposed on all consumers.

## Operating procedure

1. Read the actual manifest, lockfile, enabled features and Iced version before naming APIs. Compare that version with documentation. If no consumer exists, provide version-scoped design guidance and mark compilation/integration unverified instead of inventing a Cargo workspace.

2. Define state and Message transitions independently of widgets. Route effects through tasks and results through messages with request/generation identity. Ignore stale results after navigation or cancellation. Keep process/session state outside presentation state.

3. Keep view construction free of blocking IO and expensive layout algorithms. Task-based scheduling alone does not make CPU-bound work cooperative: choose a worker strategy compatible with the configured executor. Bound queues and coalesce render-only updates without dropping evidence.

4. Design subscription lifetime from active state and stable identity. Remove or suspend expensive producers when their view is inactive; explicitly cancel independently owned work. Guard late replies so a hidden or reopened panel cannot apply obsolete results.

5. Prefer composition of existing widgets. For custom widgets verify the selected version's layout, event propagation, focus, accessibility, operation and drawing contracts. Define pane IDs and layout persistence separately from content, with safe restoration on smaller screens.

6. Test slow work with a UI heartbeat, keyboard focus across collapse/expand, extreme window sizes, loading/error/empty states and hidden-view work counters. Report platform/hardware and measurement limits; no universal latency or accessibility guarantee follows from Iced.

## Deliverables and acceptance

components/update contracts, testable UI, empty/error/loading states, rendering budget and benchmark.

Bind each conclusion to observed inputs, method, result and limitations. Run the normal, boundary and failure cases from the [evaluations](references/evaluation-cases.md) in the authorized environment; distinguish review, simulation and integration results. Written cases remain unexecuted until run. Skill text neither proves effectiveness nor grants authority.

## Boundaries and handoff

`design-system` — Does the reusable component preserve the defined tokens, variants, states and interaction contract?

Hand off only the distinct unresolved technical question, including scope, criterion IDs, facts, gaps and required evidence. Confirm availability before consultation. A mention does not install, delegate, execute or recursively load other skills. The consumer's contract owns behavior; the skill provides the method.

## Specialized references

- [message-update-state](references/message-update-state.md): consult for Message, update, effects.
- [layout-and-custom-widgets](references/layout-and-custom-widgets.md): consult for Layout, panes and custom widgets.
- [desktop-performance-and-accessibility](references/desktop-performance-and-accessibility.md): consult for Responsiveness and accessibility evidence.

Official sources accessed on 2026-10-26 are cited alongside claims. A consulted version is not a version adopted by the consumer. Operational summaries and example schemas are methodological decisions of this skill, without a promise of implementation or future compatibility.

## Adjacent responsibilities

The specialized capability above does not replace the general methods below. Consult them only when the corresponding question remains unresolved; no handoff is mandatory.

| Capability | Adjacent technical authority |
|---|---|
| `design-review` | visual hierarchy, flow and usability audit |
| `design-system` | tokens, components, states and UI contracts |
| `rust` | ownership, crates, concurrency, compatibility, Rust validation |
| `observability-and-diagnostics` | instrumentation, logs, metrics, traces, causal investigation |
| `performance-engineering` | benchmarks, profiling, reproducible comparisons and regressions |
| `software-design` | interfaces, cohesion, coupling, local refactoring |
| `software-testing` | cases, oracles, automated tests, suites and regressions |
