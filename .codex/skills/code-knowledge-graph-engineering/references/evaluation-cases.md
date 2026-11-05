# Skill evaluations

Case contract; execution must be recorded separately. These are not completed tests.

## Preserved technical scenarios

- AC-01 → REQ-01: A valid call edge can be traced to its location and method; oracle: known synthetic corpus.
- AC-02 → REQ-02: An inferred relationship incorrectly marked as verified is rejected; oracle: provenance schema/assertion.
- AC-03 → REQ-03: A change removes a stale edge in the new snapshot; oracle: before/after fixture.
- AC-04 → REQ-03: A subgraph query applies limits and reports truncation; oracle: deterministically generated large graph.

## Evaluation protocol

Give an agent a concrete request and minimal inputs in an authorized isolated directory. In the selection round, show only the catalog/descriptions, without the expected answer. In the behavior round, provide the selected skill and adversarial data. Preserve the prompt, raw response, known agent identity/configuration, input hashes, outcome review and limitations. Do not run services or tools requiring new permissions.

Positive selection: request the specialized deliverable described in this entry. Negative selection: use the explicit exclusion; the response should identify a more suitable capability without loading this skill. Failure: provide input that contradicts the technical scenario and require evidence before approval. Concrete prompts in the consumer package must include sufficient data and an independent oracle.

## Concrete prompts

### code-knowledge-graph-engineering-positive

Define a code-edge schema and bounded impact queries with two projections of the same graph.

### code-knowledge-graph-engineering-negative

Create a static marketing diagram without relationships extracted from code.

### code-knowledge-graph-engineering-failure

An inferred edge with similarity 0.98 was marked verified=true; its file changed. A query traverses a cycle and a hub with ten thousand edges. Specify validation, invalidation and limits without assuming performance.

Review oracle: positive selects this specialized capability; negative routes to design-system (or a justified adjacent capability). In the failure case, check: reject false verified; snapshot invalidation; visited plus limits and truncation. Review this answer key after the response; do not provide it to the evaluator during selection.
