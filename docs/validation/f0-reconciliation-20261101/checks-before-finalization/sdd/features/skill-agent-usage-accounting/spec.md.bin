# Authoring and evaluation of agent-usage-accounting

Historical origin: external study; the current contract is self-contained in this spec. The study is not part of distribution or validation. Actor: skill maintainer/evaluator. Precondition: authorized authoring and evaluation in a permitted environment. This feature belongs to the library; it is not an Ox product feature.

## Preserved technical contracts

The declarations below retain the proposed IDs, scenarios and oracles. REQ-01..03 are capabilities the skill must teach. AC-01..04 require exercising concrete deliverables; text review alone does not approve them. Product/platform integrations remain future work when unavailable.

- REQ-01: Records distinguish provider-supplied measurements, derivations and estimates.
- REQ-02: Duplicate events do not improperly increase token/cost totals.
- REQ-03: Context, cumulative consumption, cost and progress are independent metrics.

- AC-01 → REQ-01: Usage without available pricing returns unknown cost, not zero; oracle: model fixture without a rate.
- AC-02 → REQ-02: Replaying an event with the same ID does not double the total; oracle: replay test.
- AC-03 → REQ-03: Cached, input and output tokens are aggregated according to the observed contract; oracle: provider fixture.
- AC-04 → REQ-03: The daily interval uses an explicit timezone and does not alter current context usage; oracle: day/hour boundary.

## Additional authoring criteria

- REQ-04: Provide a reusable method with precise selection, inputs, references and verifiable scenarios.
- AC-05 → REQ-04: Content review and local validation confirm a complete entry, substantive references, boundaries and a valid bridge.
- AC-06 → REQ-04: An observed agent trial distinguishes positive requests, negative requests and adversarial behavior; limitations and raw response are preserved.

Do not replace AC-01..04 with AC-05/06. Consumer versions, platform, data and authorization must be known before integration. Skill approval does not approve product subsystems.
