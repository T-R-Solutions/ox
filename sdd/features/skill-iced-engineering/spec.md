# Authoring and evaluation of iced-engineering

Historical origin: external study; the current contract is self-contained in this spec. The study is not part of distribution or validation. Actor: skill maintainer/evaluator. Precondition: authorized authoring and evaluation in a permitted environment. This feature belongs to the library; it is not an Ox product feature.

## Preserved technical contracts

The declarations below retain the proposed IDs, scenarios and oracles. REQ-01..03 are capabilities the skill must teach. AC-01..04 require exercising concrete deliverables; text review alone does not approve them. Product/platform integrations remain future work when unavailable.

- REQ-01: The UI does not block on processes, search, indexing or agent events.
- REQ-02: States, focus, resizing and navigation are predictable and accessible.
- REQ-03: Custom views and graphs do not perform expensive processing while hidden.

- AC-01 → REQ-01: A simulated slow operation does not block navigation/interaction; oracle: integration test with a UI heartbeat.
- AC-02 → REQ-02: An expanded/collapsed pane preserves the defined content and focus; oracle: functional state test.
- AC-03 → REQ-02: Extreme resizing does not lose essential actions; oracle: layout review at documented sizes.
- AC-04 → REQ-03: A hidden graph does not schedule continuous relayout; oracle: instrumentation under a controlled workload.

## Additional authoring criteria

- REQ-04: Provide a reusable method with precise selection, inputs, references and verifiable scenarios.
- AC-05 → REQ-04: Content review and local validation confirm a complete entry, substantive references, boundaries and a valid bridge.
- AC-06 → REQ-04: An observed agent trial distinguishes positive requests, negative requests and adversarial behavior; limitations and raw response are preserved.

Do not replace AC-01..04 with AC-05/06. Consumer versions, platform, data and authorization must be known before integration. Skill approval does not approve product subsystems.
