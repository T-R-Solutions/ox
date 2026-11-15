---
name: autonomous-verification-engineering
description: Design criterion-based acceptance gates for autonomous work, binding verdicts to observed inputs and independent oracles. Use for evidence and approval engines; skip ordinary unit-test authoring without acceptance orchestration.
---

# autonomous-verification-engineering

## Responsibility and selection

Turn requirements and acceptance criteria into executable checks and traceable verdicts while preserving oracle independence and authorization policies.

Select: Systems that accept/reject agent deliverables; evidence, criteria, gates, autonomous execution and false acceptance risk.

Do not select: Do not use solely to create unit tests or investigate flaky tests; software-testing owns those methods. Do not produce an uncalibrated “confidence score.”

## Inputs and gaps

normative criteria, code snapshots, authorized tests/checkers, change risk, approval policy.

Inspect actual contracts and resources before execution. A missing version requires consulting the corresponding documentation; a missing permission prevents the dependent effect. Record the gap, its impact and how to resolve it while continuing independent work. Examples in this package are evaluation contracts, not APIs or policies imposed on all consumers.

## Operating procedure

1. Enumerate normative acceptance criteria and identify their authority. For each, name the implementation surface, oracle, execution permission and expected failure. Do not derive expected results solely from the candidate implementation or an agent explanation.

2. Model authorization, execution outcome and acceptance as separate controls. A permitted test can fail; an accepted artifact may still lack deployment permission. Treat skips, missing tools and absent evidence explicitly instead of folding them into success.

3. Capture immutable observations with command/method, environment, exit/result, artifact hash and hashes of implementation, oracle, configuration and contract. Include dirty/untracked inputs when relevant. A Git commit alone is insufficient.

4. Evaluate each criterion against its declared oracle. Use approved, rejected, unverified, inconclusive and justified not-applicable states, mapped to the consumer vocabulary. Contradictory observations require investigation, not majority voting among agents.

5. Build a dependency map from observed inputs to criteria. Change one input in a disposable fixture and confirm only dependent observations become stale; changing the oracle or criterion itself also invalidates affected acceptance.

6. Introduce representative defects into a controlled candidate and confirm the oracle rejects them. Preserve the failing and repaired results separately. Deliver a per-criterion verdict table, residual work and exact replay instructions; stop retries when they require missing authority or an unchanged external dependency.

## Deliverables and acceptance

gate model, auditable states, requirement-evidence-snapshot bindings, implementation/oracle separation, replay procedures.

Bind each conclusion to observed inputs, method, result and limitations. Run the normal, boundary and failure cases from the [evaluations](references/evaluation-cases.md) in the authorized environment; distinguish review, simulation and integration results. Written cases remain unexecuted until run. Skill text neither proves effectiveness nor grants authority.

## Boundaries and handoff

`software-testing` — Does the chosen oracle actually fail when a representative defect is introduced?

Hand off only the distinct unresolved technical question, including scope, criterion IDs, facts, gaps and required evidence. Confirm availability before consultation. A mention does not install, delegate, execute or recursively load other skills. The consumer's contract owns behavior; the skill provides the method.

## Specialized references

- [acceptance-verdicts](references/acceptance-verdicts.md): consult for Verdicts and authorization.
- [evidence-provenance](references/evidence-provenance.md): consult for Content-bound observations.
- [independent-oracles](references/independent-oracles.md): consult for Challenge the oracle.

Official sources accessed on 2026-10-26 are cited alongside claims. A consulted version is not a version adopted by the consumer. Operational summaries and example schemas are methodological decisions of this skill, without a promise of implementation or future compatibility.

## Adjacent responsibilities

The specialized capability above does not replace the general methods below. Consult them only when the corresponding question remains unresolved; no handoff is mandatory.

| Capability | Adjacent technical authority |
|---|---|
| `ai-engineering` | models, RAG, agents using tools, diagnostics and outcome evaluation |
| `api-testing` | verification of protocols, effects, permissions and consumer compatibility |
| `reliability-engineering` | failures, cancellation, limits, degradation, recovery |
| `software-testing` | cases, oracles, automated tests, suites and regressions |
| `application-security` | trust boundaries, secrets, authorization and threats |
| `domain-modeling` | domain rules, invariants, task/agent/policy concepts |
| `software-architecture` | boundaries, integration, quality attributes, ADRs |
