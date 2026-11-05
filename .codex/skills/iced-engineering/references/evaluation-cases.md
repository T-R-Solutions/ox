# Skill evaluations

Case contract; execution must be recorded separately. These are not completed tests.

## Preserved technical scenarios

- AC-01 → REQ-01: A simulated slow operation does not block navigation/interaction; oracle: integration test with a UI heartbeat.
- AC-02 → REQ-02: An expanded/collapsed pane preserves the defined content and focus; oracle: functional state test.
- AC-03 → REQ-02: Extreme resizing does not lose essential actions; oracle: layout review at documented sizes.
- AC-04 → REQ-03: A hidden graph does not schedule continuous relayout; oracle: instrumentation under a controlled workload.

## Evaluation protocol

Give an agent a concrete request and minimal inputs in an authorized isolated directory. In the selection round, show only the catalog/descriptions, without the expected answer. In the behavior round, provide the selected skill and adversarial data. Preserve the prompt, raw response, known agent identity/configuration, input hashes, outcome review and limitations. Do not run services or tools requiring new permissions.

Positive selection: request the specialized deliverable described in this entry. Negative selection: use the explicit exclusion; the response should identify a more suitable capability without loading this skill. Failure: provide input that contradicts the technical scenario and require evidence before approval. Concrete prompts in the consumer package must include sufficient data and an independent oracle.

## Concrete prompts

### iced-engineering-positive

Add an Iced component that stays interactive during indexing and preserves focus when collapsing panes.

### iced-engineering-negative

Evaluate the visual hierarchy of a web journey without Iced code.

### iced-engineering-failure

An Iced UI receives an old search result after switching panes. A hidden graph keeps scheduling layout. No lockfile was provided. Propose state, effects, focus and a trial, identifying APIs that need confirmation.

Review oracle: positive selects this specialized capability; negative routes to design-review (or a justified adjacent capability). In the failure case, check: version gap; generation guard; suspend work; measure UI not assert responsive. Review this answer key after the response; do not provide it to the evaluator during selection.
