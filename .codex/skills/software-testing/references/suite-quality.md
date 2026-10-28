# Keeping tests credible and maintainable

Read this reference for doubles, integration infrastructure, brittle assertions, or unreliable tests. Evidence uses physical PDF pages in Aniche, *Effective Software Testing* (2022); recommendations are contextual synthesis.

## Choose a double by the missing control

**Action/context:** Use a real simple value or collaborator when it is fast and controllable. Stub an expensive or nondeterministic answer; use a maintained fake when its behavior fits the test boundary; verify an interaction when the outbound effect is the contract. For an external adapter, retain tests against the actual protocol or implementation.

**Evidence/rationale:** Chapter 6, PDF 169-199, shows invoice queries, outbound SAP effects, captured arguments, and exceptions. A double can cheaply force failures, but a passing test with a stale double does not prove interoperability. Section 6.3.5 explicitly disputes another source's preference for fakes over mocks.

**Exceptions/trade-offs:** An adapter wrapper can concentrate library churn but adds another maintained abstraction. Do not introduce one for every API. A fake is useful only with credible fidelity; a mock reduces setup but can lock tests to internal calls. Prefer observable state if the call sequence is not itself significant.

**Validation:** State what the double omits and which integration test checks its assumptions. Exercise dependency errors that matter to the caller. Avoid globally asserting every call, count, or argument when only one effect is relevant.

## Create the smallest useful seam

**Action/context:** When a test cannot control time, randomness, a dependency, or state, consider passing a value, injecting a narrow capability, or separating decision logic from effects. Prefer existing seams and explicit result/state observation.

**Evidence/rationale:** Chapters 6-7, PDF 192-225, compare clocks, method parameters, dependency injection, and observable outcomes. Chapter 7 explicitly says interfaces are not required everywhere and examples should not be applied literally.

**Exceptions/trade-offs:** Passing a value simplifies the function but moves acquisition responsibility to callers. Injection may simplify callers but increases local setup. A getter can expose domain state but should not expose mutable implementation structures. Broad architecture changes require their own justification.

**Validation:** Preserve behavior with appropriate existing tests and exercise real integration across the new seam. Check callers, cleanup, and lifecycle ownership; compile using the project's actual toolchain when code changes.

## Exercise the real integration contract

**Action/context:** Use a production-compatible test engine for SQL dialect, transactions, constraints, migrations, or runtime lifecycle risks. Create minimal explicit fixtures, independently identify each test's resources, and clean up even after failures.

**Evidence/rationale:** Chapter 9 sections 9.1-9.2, PDF 244-267, shows composition, framework visitors, and SQL tests. Nulls, joins, duplicates, grouping, aggregate behavior, and database constraints cannot be inferred from a stubbed repository response.

**Exceptions/trade-offs:** Real infrastructure costs startup and maintenance. A simpler substitute can support local feedback but does not establish production-engine compatibility. Rollback-based cleanup may hide commit-time constraints and transaction behavior; include a real commit when that is the claim. Never apply the book's truncate examples to unverified shared data.

**Validation:** Record engine/version/configuration differences, migration path, data isolation, and transaction boundary. For shared integration environments distinguish environmental unavailability from product failure; skipped checks remain missing evidence.

## Keep journeys meaningful

**Action/context:** Automate a complete user journey when the risk spans UI and backend. Encapsulate repeated selectors or page behavior only when useful. Seed prerequisites through an existing safe interface, but traverse every step that is part of the actual claim.

**Evidence/rationale:** Chapter 9 sections 9.3-9.4, PDF 267-285, describes page objects, explicit readiness, test data setup, and supported browsers. Bypassing setup avoids redundant slow navigation; bypassing the feature under test invalidates the test.

**Exceptions/trade-offs:** Page objects add maintenance and should not obscure assertions. A test-only reset API is a powerful destructive capability: prefer existing isolated fixture mechanisms; if one is justified, prove it is absent outside the disposable test environment. Do not infer accessibility from DOM or screenshot similarity.

**Validation:** Wait for observable readiness with a bounded deadline instead of fixed sleeps. Keep assertions about visible outcomes in the test. Run against the relevant supported browser/runtime matrix and report untested combinations.

## Diagnose flaky and brittle tests

**Action/context:** Reproduce the failure while capturing seed, execution order, resource state, clock, concurrency, and environment. Compare isolated and suite execution. Investigate a product race as well as test setup before changing assertions or adding retries.

**Evidence/rationale:** Chapter 10, PDF 286-303, describes shared resources, asynchronous waits, hidden dependencies, resource optimism, general fixtures, and oversensitive assertions. Strong assertions must detect contract changes while tolerating irrelevant implementation changes.

**Exceptions/trade-offs:** Repeated runs are diagnostic evidence, not a repair. Statistical checks may intentionally have false-positive probability; document their statistical design and separate them from deterministic regression expectations. A temporary quarantine requires visible missing coverage and a repair path.

**Validation:** Establish a specific causal fix, then rerun in the conditions that exposed the defect. Check cleanup on failure and parallel isolation. Do not claim flake elimination from one passing rerun.

## Review test code as an explanation

A test should make the protected behavior, decisive input, expected result, and failure meaning apparent. Named builders can reduce irrelevant setup without hiding important values. A cohesive test may need several assertions; a single assertion is not inherently stronger. Keep helpers simpler than the behavior they verify, and test custom parsing/assertion helpers when a defect could systematically conceal failures. Preserve deliberate duplication where abstraction would obscure intent.

Evidence: chapter 10 sections 10.1.7-10.2.5, PDF 290-300. Validation: review the test without the implementation, then verify that an appropriate behavioral defect produces a clear failure. The benefit of these skill instructions versus an unaided agent remains experimentally unproven.
