# Skill evaluations

Case contract; execution must be recorded separately. These are not completed tests.

## Preserved technical scenarios

- AC-01 → REQ-01: An out-of-order event does not cause an unwarranted completion; oracle: transition test with an adversarial sequence.
- AC-02 → REQ-02: Process death produces a status and cleanup of associated resources; oracle: controlled process with an injected failure.
- AC-03 → REQ-02: Cancellation during heavy output leaves no orphaned tasks; oracle: harness with streams and a deadline.
- AC-04 → REQ-03: A “done” message without a validated artifact does not change the verdict to approved; oracle: deterministic adversarial case.

## Evaluation protocol

Give an agent a concrete request and minimal inputs in an authorized isolated directory. In the selection round, show only the catalog/descriptions, without the expected answer. In the behavior round, provide the selected skill and adversarial data. Preserve the prompt, raw response, known agent identity/configuration, input hashes, outcome review and limitations. Do not run services or tools requiring new permissions.

Positive selection: request the specialized deliverable described in this entry. Negative selection: use the explicit exclusion; the response should identify a more suitable capability without loading this skill. Failure: provide input that contradicts the technical scenario and require evidence before approval. Concrete prompts in the consumer package must include sufficient data and an independent oracle.

## Concrete prompts

### agent-runtime-engineering-positive

Design a CLI adapter with streaming, cancellation, reconnection and process supervision.

### agent-runtime-engineering-negative

Compare the response quality of two models without tools or processes.

### agent-runtime-engineering-failure

Execution A declared completion, exited without tests, and its delayed event arrived after B started. B produces heavy stdout/stderr and ignores cooperative cancellation. Describe transitions, controls and evidence; do not run processes.

Review oracle: positive selects this specialized capability; negative routes to ai-engineering (or a justified adjacent capability). In the failure case, check: generation isolation; done not accepted; bounded drain and observed cleanup. Review this answer key after the response; do not provide it to the evaluator during selection.
