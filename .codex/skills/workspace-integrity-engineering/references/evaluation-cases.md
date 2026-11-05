# Skill evaluations

Case contract; execution must be recorded separately. These are not completed tests.

## Preserved technical scenarios

- AC-01 → REQ-01: An attempted write outside the root through .. or a symlink is rejected; oracle: adversarial path fixture.
- AC-02 → REQ-02: Two agents edit the same version: the second write conflicts or applies a verified merge; oracle: concurrency test.
- AC-03 → REQ-03: An injected failure between temporary-file creation and rename leaves no incorrect “done” record; oracle: crash test.
- AC-04 → REQ-03: An externally changed file invalidates the hash/snapshot; oracle: watcher plus actual-read verification.

## Evaluation protocol

Give an agent a concrete request and minimal inputs in an authorized isolated directory. In the selection round, show only the catalog/descriptions, without the expected answer. In the behavior round, provide the selected skill and adversarial data. Preserve the prompt, raw response, known agent identity/configuration, input hashes, outcome review and limitations. Do not run services or tools requiring new permissions.

Positive selection: request the specialized deliverable described in this entry. Negative selection: use the explicit exclusion; the response should identify a more suitable capability without loading this skill. Failure: provide input that contradicts the technical scenario and require evidence before approval. Concrete prompts in the consumer package must include sufficient data and an independent oracle.

## Concrete prompts

### workspace-integrity-engineering-positive

Design concurrent writes by an editor and agents with snapshots, a watcher and file recovery.

### workspace-integrity-engineering-negative

Plan migration of a local SQLite column after a crash, without external filesystem writers.

### workspace-integrity-engineering-failure

Two writers read H0; A published H1; B tries to write H2. One destination uses a symlink outside the root, and a crash occurred between staging and rename with missed watcher events. Explain permitted operations and recovery; do not write outside the evaluation directory.

Review oracle: positive selects this specialized capability; negative routes to database-engineering (or a justified adjacent capability). In the failure case, check: conflict; reject escape; read actual contents; no blind rollback or TOCTOU claim. Review this answer key after the response; do not provide it to the evaluator during selection.
