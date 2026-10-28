---
name: software-testing
description: Plan, implement, or review risk-based software tests; diagnose weak or flaky suites and preserve behavior during changes. Use for test strategy, case design, test doubles, or meaningful regression coverage, rather than unrelated edits or a requirement to add tests to every change.
---

# Software Testing

Select tests that can expose consequential incorrect behavior at an appropriate cost. Work from existing requirements and acceptance criteria; distinguish specified behavior, observed legacy behavior, and an unresolved product decision.

## Scope and evidence

Collect the changed behavior, consumers, relevant failure history, existing test conventions and commands, dependency boundaries, and available test environment. Inspect actual repository tooling before proposing a command or dependency.

This skill owns case selection, test implementation, suite quality, and the strength of the evidence. Protocol compatibility and API-specific contracts may justify `api-testing`; domain ambiguities may justify `domain-modeling`. Structural redesign belongs to `software-design` when a small test seam is insufficient. Do not load those skills merely because they are named here. Ordinary correctness, security, and accessibility remain required without specialist invocation.

A documentation correction or simple reversible edit may need direct inspection rather than new automated tests. Do not introduce a test framework solely to exercise this skill.

## Workflow

1. **Define the claim.** State what must remain true, what intentionally changes, and what would constitute a failure. Identify an independent oracle: requirement, invariant, reviewed example, protocol contract, or trusted reference. Current implementation output alone is not proof of correctness. Characterization tests preserve observed behavior pending a separate decision about whether it is desirable.
2. **Choose boundaries.** Map each consequential risk to the smallest scope that actually exposes it. Pure decision logic usually permits fast local tests; SQL, serialization, framework lifecycle, and component wiring may require real integration. Reserve complete journeys for risks involving the assembled system. Avoid prescribed pyramid ratios and class-per-test rules.
3. **Derive cases.** Identify input and output partitions, boundary transitions, prior states, invalid cases, and relevant interactions. Include representative normal behavior as well as failures. Explain omitted combinations where their risk matters. Read [case design](references/case-design.md) when choosing partitions, properties, coverage or mutation requires more detail.
4. **Control the environment.** Make time, randomness, asynchronous completion, and external state explicit. Use isolated fixtures and cleanup even after failure. Replace a collaborator only when the loss of realism is justified; validate real adapters separately. Read [suite quality](references/suite-quality.md) when deciding double fidelity, integration setup or flake diagnosis. For asynchronous, database, or layered application risks, selectively read [boundary evidence](references/boundary-evidence.md).
5. **Implement proportionally.** Preserve existing conventions. Keep setup, action, and assertions legible; assert the whole relevant outcome, including prohibited side effects. Shared builders should expose decisive inputs and keep irrelevant defaults local. Multiple assertions are appropriate for one cohesive behavior.
6. **Verify the tests.** Run the relevant configured checks. For a regression, establish that the test detects the original defect when safely feasible. For a consequential oracle, consider a small deliberate fault or targeted mutation in an isolated copy. Restore changes and rerun. Do not require mutation tooling for every edit.
7. **Assess residual uncertainty.** A passing example establishes only its observations in its environment. Coverage measures execution; it does not establish adequate assertions, requirement coverage, or absence of defects. Generated cases require meaningful properties and input distributions.

## Decision constraints

When screenshot comparison is selected, read
[visual regression](references/visual-regression.md) for reference provenance,
capture state, masks and reviewed updates. For coverage-guided exploration of a
parser/codec or similar input boundary, read
[coverage-guided fuzzing](references/coverage-guided-fuzzing.md) for harness reach,
instrumentation, corpus and reproducible failures. Neither is required for routine tests.

- Preserve public behavior during refactoring; explicitly identify contract changes and affected consumers.
- TDD is an optional feedback technique. It does not replace systematic case analysis or user validation.
- Prefer observable behavior over private calls or incidental ordering. Verify a call or sequence when the interaction itself is the contract.
- Do not expose mutable internals, require an interface for every dependency, or restructure a simple domain solely to make mocks convenient.
- Do not turn missing infrastructure, repeated retries, quarantined failures, or skipped tests into a passing result. Distinguish environment failure, test defect, and product defect.
- Use authorized local/sandbox resources. Destructive fixture reset belongs only to a verified disposable test environment.

## Report

Complete the requested tests and inspect their results; fix failures caused by the change within scope. Summarize the behavior protected and commands/results. Explain risk and scope choices only when they affect acceptance; a focused regression needs no suite inventory. Identify blocked or skipped checks, remaining gaps, and any intentional contract change. Report coverage or timing only when measured and include its scope. Keep proposed checks separate from completed validation.

The shared research record (historical library source: `system/research/testing-progress.json`; not required at runtime) tracks source reading and limitations; it is provenance, not required operational context. The coverage matrix (historical library source: `system/research/testing-coverage.json`; not required at runtime) distinguishes textual analysis, selected visual inspection, source defects, and unexecuted examples.

Other named skills are optional specialist suggestions. Use them only when available and needed for a specific unresolved question; their absence does not prevent using this skill. Report any expertise or verification gap without claiming a handoff occurred.

## Adjacent responsibilities

For engine-specific concurrency/migrations, postgresql can supply the mechanism while tests here retain an independent oracle. A simulated schedule does not become a real database integration.
These are optional available capabilities, not dependencies of this folder.
