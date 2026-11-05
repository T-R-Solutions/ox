# Skill evaluations

Case contract; execution must be recorded separately. These are not completed tests.

## Preserved technical scenarios

- AC-01 → REQ-01: Usage without available pricing returns unknown cost, not zero; oracle: model fixture without a rate.
- AC-02 → REQ-02: Replaying an event with the same ID does not double the total; oracle: replay test.
- AC-03 → REQ-03: Cached, input and output tokens are aggregated according to the observed contract; oracle: provider fixture.
- AC-04 → REQ-03: The daily interval uses an explicit timezone and does not alter current context usage; oracle: day/hour boundary.

## Evaluation protocol

Give an agent a concrete request and minimal inputs in an authorized isolated directory. In the selection round, show only the catalog/descriptions, without the expected answer. In the behavior round, provide the selected skill and adversarial data. Preserve the prompt, raw response, known agent identity/configuration, input hashes, outcome review and limitations. Do not run services or tools requiring new permissions.

Positive selection: request the specialized deliverable described in this entry. Negative selection: use the explicit exclusion; the response should identify a more suitable capability without loading this skill. Failure: provide input that contradicts the technical scenario and require evidence before approval. Concrete prompts in the consumer package must include sufficient data and an independent oracle.

## Concrete prompts

### agent-usage-accounting-positive

Model a token/cache/cost ledger by session and day with idempotency across providers.

### agent-usage-accounting-negative

Instrument CPU/RAM and process latency without tokens or billing.

### agent-usage-accounting-failure

Event r1/e1: input_total=100 including cached=30, output=20, repeated twice. Pricing is absent. Another request reports cumulative snapshots 10 and 15. An event arrives after midnight but occurred before. Define totals and uncertainties without looking up prices.

Review oracle: positive selects this specialized capability; negative routes to observability-and-diagnostics (or a justified adjacent capability). In the failure case, check: 120 not 150/240; cumulative15; missing cost unknown; event timezone; context separate. Review this answer key after the response; do not provide it to the evaluator during selection.
