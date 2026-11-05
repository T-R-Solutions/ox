# Skill evaluations

Case contract; execution must be recorded separately. These are not completed tests.

## Preserved technical scenarios

- AC-01 → REQ-01: A criterion with a real test and versioned input can be marked APPROVED; oracle: bound execution artifact.
- AC-02 → REQ-02: A skipped or unavailable test remains UNVERIFIED; oracle: fixture without an executable.
- AC-03 → REQ-02: A change after validation invalidates only criteria dependent on changed inputs; oracle: freshness test.
- AC-04 → REQ-03: An agent without deployment authorization cannot publish even after verification passes; oracle: boundary mock plus permitted integration.

## Evaluation protocol

Give an agent a concrete request and minimal inputs in an authorized isolated directory. In the selection round, show only the catalog/descriptions, without the expected answer. In the behavior round, provide the selected skill and adversarial data. Preserve the prompt, raw response, known agent identity/configuration, input hashes, outcome review and limitations. Do not run services or tools requiring new permissions.

Positive selection: request the specialized deliverable described in this entry. Negative selection: use the explicit exclusion; the response should identify a more suitable capability without loading this skill. Failure: provide input that contradicts the technical scenario and require evidence before approval. Concrete prompts in the consumer package must include sufficient data and an independent oracle.

## Concrete prompts

### autonomous-verification-engineering-positive

Design an engine that assigns verdicts per criterion to agent deliverables, binding evidence to the snapshot.

### autonomous-verification-engineering-negative

Create unit tests for an addition function and diagnose a flaky test without an acceptance engine.

### autonomous-verification-engineering-failure

Criterion A had a passing test on file X; X changed. Criterion B tests unchanged file Y. C's test is missing. A build check passed, but there is no publication grant. Classify and propose resumption; do not publish.

Review oracle: positive selects this specialized capability; negative routes to software-testing (or a justified adjacent capability). In the failure case, check: invalidate A not unrelated B; C unverified; no deploy authorization. Review this answer key after the response; do not provide it to the evaluator during selection.
