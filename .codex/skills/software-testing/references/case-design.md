# Designing cases and trustworthy oracles

Read this reference when deriving cases, reviewing test adequacy, or considering generated tests. Recommendations below are contextual engineering synthesis from the cited analyzed sections, not universal rules imposed by a book. PDF page numbers are physical, 1-based; printed pages in *Effective Software Testing* are 28 lower.

## Partition before enumerating

**Action and context.** For behavior with several inputs or states, identify meaningful equivalence classes: accepted and rejected inputs, empty/single/multiple collections, absent/present/duplicate values, and valid state transitions. Add output classes and input interactions that could reveal a missing rule. Select representative values only after explaining the assumed equivalence.

**Evidence and rationale.** Aniche, *Effective Software Testing* (2022), chapter 2, PDF 58-90, demonstrates that specification-derived cases find missing behavior even when existing branches are covered. The addition example reveals omitted carry propagation. Requirements describe behavior the implementation may not contain.

**Exceptions and costs.** Do not test null or malformed data at every internal function when the type system or a verified upstream boundary makes it unreachable. Still test the actual boundary. Combining every partition can explode; prioritize consequential interactions and disclose exclusions. Invalid-input combinations may matter when error precedence, authorization, or partial writes are contractual.

**Validation.** Map each case to a requirement or assumption, check expected output independently, and verify the test fails for the defect it targets. For stateful behavior include the state before the operation and observable state afterward, not only the method parameters.

## Test transitions and representation limits

**Action and context.** Test both sides of each meaningful boundary and the boundary itself as needed. Derive neighboring values from the actual representation: an integer step, next representable float, timestamp precision, or length unit. Consider inclusive versus exclusive limits, equality, empty-to-nonempty transitions, overflow, and ordering where relevant.

**Evidence and rationale.** Aniche chapter 2 sections 2.1.4 and 2.4, PDF 65-67 and 82-87; chapter 3 section 3.8, PDF 110. Off-by-one errors often preserve behavior elsewhere. The source's printed-page-38 equality example has an inconsistent off-point; the appendix (PDF 311) correctly gives 9 and 11 around integer equality to 10.

**Exceptions and costs.** A neighboring value may be invalid by construction. Do not fabricate unreachable states merely to satisfy a template. Extreme values and combinations are chosen by risk rather than always included.

**Validation.** Confirm each input reaches the intended condition; a prior validation or early return can prevent it. Assert both the chosen outcome and relevant absence of side effects.

## Treat coverage as a question generator

**Action and context.** After designing behavior-based tests, inspect uncovered branches and conditions. Explain why each significant gap exists: omitted requirement, implementation-only behavior, infeasible path, or deliberate exclusion. Choose stronger condition analysis for consequential complex decisions.

**Evidence and rationale.** Aniche chapter 3, PDF 91-124, compares line, branch, condition, and MC/DC criteria. The clump-counting example reaches branch coverage while missing meaningful cases. Section 3.10.4 qualifies MC/DC's N+1 count as a lower bound rather than a universal guarantee.

**Exceptions and costs.** Instrumentation semantics differ among tools, especially short-circuit expressions, generated code, and assertions. Infeasible combinations and equivalent conditions do not justify impossible tests. Do not change readable production logic only to improve a percentage.

**Validation.** Inspect the tool's current definition and denominator. Confirm assertions observe the behavior executed. A high number can coexist with an empty or irrelevant oracle; a low number does not identify the precise missing risk.

## Use properties where they express a stronger claim

**Action and context.** For broad input domains or state sequences, express invariants, round-trip relations, ordering, conservation, or agreement with an independently justified reference. Generate both meaningful normal and adverse populations; record seeds and minimized failing examples. Keep readable examples for critical boundaries and regressions.

**Evidence and rationale.** Aniche chapter 5, PDF 145-168, develops grade, unique-values, search, and stateful basket examples. Sections 5.6.1-5.6.2 explain the effort and limitations of generators, distributions, and boundaries.

**Exceptions and costs.** Property tests can duplicate the same bug as production or become vacuous after filtering. A round trip alone can let two mutually wrong transformations agree. A check that all input values occur in output does not exclude extra output values. Ensure generators can produce their requested domain and reach relevant states. Use the installed framework's documentation rather than historical jqwik defaults.

**Validation.** Inspect generated distributions and rejected cases; inject a representative wrong implementation in an isolated evaluation. Check deterministic replay, shrinking behavior, and required limits. Random sampling is not exhaustive proof.

## Evaluate oracle sensitivity

**Action and context.** For a high-risk regression or apparently strong suite, introduce a small representative defect in a disposable copy, or apply targeted mutation if tooling already exists. Classify survivors before adding tests.

**Evidence and rationale.** Aniche section 3.11, PDF 118-121, and sections 9.4.3/10.1.6, PDF 283 and 289-290, distinguish executed code from defect-sensitive assertions. A mutation can survive because it has no observable effect.

**Exceptions and costs.** Mutation costs execution time and manual interpretation. Equivalent, unreachable, and out-of-contract mutations do not necessarily reveal a test gap. Never leave a deliberate defect in the delivered code, and do not mutate shared live systems.

**Validation.** Record the defect, detecting test, failure reason, restoration, and final passing run. Do not equate a mutation score with overall correctness.

## Short illustrative example

For an integer quantity limit of 10 inclusive, examples 9, 10, and 11 distinguish the boundary. A test checking only that accepted quantities return a boolean says little. A stronger oracle specifies acceptance for 9 and 10, rejection for 11, and no reservation after rejection. If rejected requests may return an existing reservation by contract, change that assertion to the documented behavior; do not invent a universal rule.

This is a conceptual example, not an executable application or a benchmark.
