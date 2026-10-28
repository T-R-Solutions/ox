---
name: software-design
description: Implement, refactor, or review code by examining responsibilities, cohesion, coupling, interfaces, information hiding, and maintenance costs. Use for concrete code-level design decisions and behavior-preserving changes. Do not use for cosmetic edits alone or to choose system architecture without architectural requirements.
---

# Software Design

Improve the code's ability to express required behavior and accommodate plausible changes. Start with the current task and existing conventions. A smaller diff, fewer classes, or a named pattern is not by itself a better design.

## Scope and evidence

Collect the relevant requirements, callers, contracts, invariants, dependency boundaries, failure behavior, and existing checks. Inspect the actual change path before diagnosing complexity. Separate the problem specification, technical decision, implementation, and validation; a small change rarely needs separate documents for all four.

This skill owns code-level responsibilities and interfaces. Use software-architecture only when the unresolved decision concerns system boundaries or quality attributes; domain-modeling for disputed business invariants; software-testing for a substantive testing strategy question. Performance and distributed guarantees require their own evidence. Load another skill only for that specific need. Basic correctness, security, and accessibility remain mandatory without specialized skill selection.

## Workflow

1. **State the behavior.** Identify inputs, outputs, state changes, errors, ownership, ordering, and externally relevant side effects. Record intentional contract changes separately from refactoring. Identify callers that depend on undocumented behavior.
2. **Locate the maintenance problem.** Trace a representative change or failure through the code. Look for repeated domain knowledge, responsibilities that change independently, hidden dependencies, inconsistent concepts, and interfaces that require callers to understand implementation details. Avoid diagnosing by line counts alone.
3. **Compare proportional options.** Consider leaving a coherent design intact, a local simplification, and a boundary change when useful. Explain what knowledge each option hides and what coordination it introduces. Consult [design decisions](references/design-decisions.md) for abstraction, composition, duplication, and failure-contract trade-offs.
4. **Choose the smallest justified change.** Preserve contracts and project idioms. Consolidate knowledge that must stay consistent; keep superficially similar code separate when its reasons for change differ. Prefer explicit dependencies where they clarify control and ownership. Do not mandate classes, interfaces, inheritance, functional abstractions, or dependency-injection frameworks.
5. **Implement in reviewable increments.** Keep unrelated cleanup separate. Update names and comments that explain contracts, units, invariants, and non-obvious reasons. Verify that moving code has not changed evaluation order, exception propagation, concurrency, resource lifetime, or authorization checks.
6. **Validate the claim.** Run available checks appropriate to the changed behavior and boundary. Where needed, characterize existing behavior before changing it. Inspect real caller compatibility and relevant failure paths; mocks alone cannot establish integration. Use [refactoring evidence](references/refactoring-evidence.md) when the contract is subtle.

For custom algorithms or consequential data-structure choices, read
[algorithm decisions](references/algorithm-decisions.md) before implementation.
Use it to establish preconditions, correctness and resource bounds; ordinary local
algorithm work does not require a separate architecture or performance engagement.

## Essential decisions

- Apply KISS to the whole reasoning and maintenance burden, not merely typing effort. A helper can simplify or obscure depending on the knowledge it encapsulates.
- Apply YAGNI to speculative capability, while retaining known security, durability, compatibility, and operational requirements.
- Apply DRY to shared knowledge and invariants, not every repeated syntax fragment. Shared code also creates coordinated change and versioning costs.
- Hide volatile implementation decisions, but expose guarantees consumers need: failure outcomes, cancellation, durability, resource ownership, and relevant timing constraints.
- Testability is useful design feedback, not proof that a design is correct. Neither adopting nor rejecting TDD settles the design decision.
- Measure before claiming performance improvement. Historical book benchmarks are examples of investigation, not current platform facts.

## Completion and report

Describe the concrete responsibility or contract improved, the alternatives considered when material, and the maintenance cost accepted. Report behavior preserved or intentionally changed, affected callers, checks actually run, and remaining uncertainty. Distinguish illustrative examples from executed code and local validation from production evidence. Avoid claiming universal superiority or unmeasured speedups.

Other named skills are optional specialist suggestions. Use them only when available and needed for a specific unresolved question; their absence does not prevent using this skill. Report any expertise or verification gap without claiming a handoff occurred.

## Adjacent responsibilities

For a long-lived mixed-version or replacement transition, software-evolution can own the transition while this skill owns the local seam. Ordinary behavior-preserving refactoring stays here.
These are optional available capabilities, not dependencies of this folder.
