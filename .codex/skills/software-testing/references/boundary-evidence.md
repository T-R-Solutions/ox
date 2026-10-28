# Evidence across asynchronous and application boundaries

Use this reference when a test can pass while the promised work has not occurred, when persistence or framework behavior matters, or when several test layers duplicate effort. These are contextual engineering recommendations synthesized from the sources below. PDF locations are physical, one-based pages.

## Observe completion, not merely scheduling

**Action and context:** Await the actual result or a bounded observable condition. For callbacks, prove the callback occurred and propagate assertion errors to the test runner. For timers, test the relevant before/after boundary and restore timer state with failure-safe cleanup. Control time through a value or narrow clock capability when useful.

**Evidence and rationale:** Osherove with Khorikov, *The Art of Unit Testing*, third edition (2024), chapter 6 PDF 149-174, explains asynchronous seams, logic extraction and fake timers. Its listing 6.27 tests an unawaited `findByText` promise, which cannot prove that the element appeared. [Jest asynchronous documentation](https://jestjs.io/docs/asynchronous) requires returning or awaiting asynchronous work; [Testing Library async methods](https://testing-library.com/docs/dom-testing-library/api-async/) documents promise-returning queries. These documented semantics take precedence over the defective example.

**Exceptions and costs:** A synchronous fake helps force an error but cannot establish actual scheduling, races, cancellation or network behavior. Real scheduler tests cost time and may require controlled synchronization. Do not classify all asynchronous tests as flaky or as integration tests. A single timestamp suits a business operation's effective time; deadline tests need progressing elapsed time.

**Validation:** Make the operation never complete, reject, or produce the wrong result in an isolated check; the test must fail rather than silently pass. Confirm cleanup on the failure path. For Jest, select APIs for the project's installed version; [timer documentation](https://jestjs.io/docs/timer-mocks) distinguishes advancing, clearing and restoring timers. Do not copy a historical `resetAllTimers` call without verifying its existence.

Illustrative before/after, not an executed framework example: checking that `findByText(...)` is truthy observes a promise; awaiting the query and checking the resolved element observes the intended UI outcome.

## Observe persistence independently

**Action and context:** For database-backed behavior, arrange known data, execute the actual operation with its intended transaction lifetime, then read committed results through a fresh context or another independently justified observation path. Cover relevant constraints, nulls, joins, ordering, concurrency and rollback/commit failures.

**Evidence and rationale:** Khorikov, *Unit Testing* (2020), chapter 10 sections 10.2-10.3 PDF 256-268, explains how a reused ORM context can return cached objects and conceal missing persistence. Aniche, *Effective Software Testing* (2022), chapter 9 PDF 244-267, supplies systematic query cases. Mohan, *Full Stack Testing* (2022), chapter 5 PDF 141-174, extends the risks to batch jobs, caches and event processing.

**Exceptions and costs:** Use the production-relevant engine/version/configuration when their semantics are the claim. A substitute can give faster partial feedback but leaves a compatibility gap. Select rollback, cleanup, schema partitioning, snapshots or containers based on isolation, commit semantics and measured cost; no universal ban on parallel integration tests. A controlled real file system with per-test temporary directories can be simpler than an elaborate fake.

**Validation:** Remove the save/commit or inject a relevant failure in an isolated copy and verify detection. Check failure-safe resource disposal and confirm the cleanup target is disposable. Do not equate engine vendor alone with compatibility. A fresh ORM context is not necessarily a new database transaction; verify the actual framework lifecycle.

The CRM examples in Khorikov chapter 10 publish messages before database commit. Their local test does not establish atomic external publication. If that risk matters, test publication/commit failure and recovery against the application's actual design. Request distributed-systems or reliability expertise only when guarantees or recovery design are unresolved.

## Allocate evidence across layers

**Action and context:** Map each scenario to the boundary where the defect becomes observable. Keep dense pure logic cases local, and add integration or complete journeys for wiring, authorization, serialization, delivery and platform behavior. Distinguish duplicated assertions from useful independent evidence at different boundaries.

**Evidence and rationale:** Osherove with Khorikov chapter 10 PDF 222-240 proposes scenario-to-layer recipes. Mohan chapters 3-4 PDF 69-140 and chapter 12 PDF 361-370 connect feedback to delivery risks. Khorikov chapters 4 and 8 PDF 89-113 and 207-237 explicitly describe exceptions to a conventional pyramid. These sources support a risk map, not mandatory ratios or documents.

**Exceptions and costs:** A small API dominated by database behavior may need mostly integration tests. Multiple assertions and state transitions can form one coherent scenario; property and state-machine tests are not invalid because they contain loops or sequences. Fail-fast behavior still needs evidence for the promised error, absence of partial effects and recovery. Do not remove a test simply because the failure would be obvious in production.

**Validation:** For each selected test, state the defect it can expose and the important behavior it cannot establish. Confirm discovery and relevant release gates. A green pipeline is evidence, not deployment authorization. Keep visual snapshots, accessibility checks, performance measurements and exploratory observations distinct: none proves the others.

## Make doubles and abstractions earn their cost

**Action and context:** Use controlled real collaborators where practical; introduce doubles for specific missing control. Put assertions at a stable observable boundary, and use independent expected data. A recording double at an outbound message boundary can exercise real serialization without sending externally.

**Evidence and rationale:** Khorikov chapters 5,7,9,11 PDF 114-140,173-204,238-250,281-296 emphasizes behavioral contracts, explicit seams and independent oracles. Osherove with Khorikov chapters 3-5 PDF 89-148 discusses incoming stubs and outgoing mocks. Aniche chapter 6 PDF 169-199 supplies a different preference for mocks versus fakes. Their vocabularies and preferences differ; the engineering criterion is control, fidelity, fault detection and maintenance.

**Exceptions and costs:** Queries can have authorization, resource-budget or access-order contracts; interaction checks are justified when those are the claim. A narrow interface may be valuable with one implementation, and not every language needs an interface for a double. Partial mocking may be a temporary legacy seam. A wrapper adds code and requires real adapter validation. Do not convert entities into value objects merely to shorten assertions, or impose a hexagonal architecture on simple code.

**Validation:** Explain the omitted real behavior and verify the adapter assumptions separately. Count calls only when cardinality matters; one call to a mock does not prove exactly-once delivery. Confirm an implementation-preserving refactor stays green and an actual contract defect fails. Test diagnostic-log redaction and required observability even if logs are intended only for developers.

## Preserve fidelity and CI evidence when applying large-organization lessons

**Action and context:** Use the smallest boundary that supplies the required evidence, and record its omitted production behavior. Keep CI results tied to the tested revision, artifact, configuration and selected checks. Treat quarantined or disabled tests as explicit missing evidence with an owner and restoration criteria when quarantine is authorized.

**Evidence and rationale:** *Software Engineering at Google* (first edition, 2020), chapters 11–14, physical PDF 235–338, separates resource size from behavioral scope and discusses maintained fakes and larger-test fidelity. Chapter 23, PDF 509–531, covers staged feedback and CI limitations. Figure 23-4 on PDF 529 counts disabled tests toward a green result; green therefore does not mean every test passed. The research synthesis (historical library source: `system/research/google-synthesis.md`; not required at runtime) explains conflicts and precise limits without requiring routine loading.

**Exceptions and costs:** Google's rough test ratios, process boundaries and preferred fake strategy reflect its context. Reconcile fake preferences with the other authors through control, fidelity, maintenance and reuse. An in-memory database does not establish production database semantics; chained contracts do not prove every end-to-end interaction. More infrastructure is justified only by relevant risk and recurring value. A flaky failure can be a real regression, and hermeticity does not eliminate scheduling races.

**Validation:** Verify real adapters where their semantics matter. Distinguish tests passed, failed, skipped and quarantined. Confirm failure diagnostics identify the relevant artifact and environment. Reruns aid investigation but cannot prove a failure harmless. Historical Google percentages and example graphs are not measured gains for this skill.
