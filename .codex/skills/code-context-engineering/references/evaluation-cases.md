# Skill evaluations

Case contract; execution must be recorded separately. These are not completed tests.

## Preserved technical scenarios

- AC-01 → REQ-01: A symbol query reports file, range, snapshot and method; oracle: fixtures with verified positions.
- AC-02 → REQ-02: A rename/edit invalidates old entries and updates affected ones; oracle: controlled repository mutations.
- AC-03 → REQ-03: An ambiguous call without semantics is not labeled a verified reference; oracle: same-name code and imports.
- AC-04 → REQ-03: An absent LSP results in explicit degradation without invented results; oracle: deliberately unavailable server.

## Evaluation protocol

Give an agent a concrete request and minimal inputs in an authorized isolated directory. In the selection round, show only the catalog/descriptions, without the expected answer. In the behavior round, provide the selected skill and adversarial data. Preserve the prompt, raw response, known agent identity/configuration, input hashes, outcome review and limitations. Do not run services or tools requiring new permissions.

Positive selection: request the specialized deliverable described in this entry. Negative selection: use the explicit exclusion; the response should identify a more suitable capability without loading this skill. Failure: provide input that contradicts the technical scenario and require evidence before approval. Concrete prompts in the consumer package must include sufficient data and an independent oracle.

## Concrete prompts

### code-context-engineering-positive

Design an incremental symbol index with offsets, per-snapshot provenance and fallback without LSP.

### code-context-engineering-negative

Test whether embeddings improve code location compared with text search, without changing the indexing mechanism.

### code-context-engineering-failure

Two modules define run; the AST found an unresolved run call. The file was renamed and a multibyte character was added before the symbol; LSP is unavailable. Define query results and invalidation.

Review oracle: positive selects this specialized capability; negative routes to ai-engineering (or a justified adjacent capability). In the failure case, check: syntax not resolved; byte/encoding bounds; rename invalidation; explicit fallback. Review this answer key after the response; do not provide it to the evaluator during selection.
