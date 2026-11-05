# Authoring and evaluation of code-knowledge-graph-engineering

Historical origin: external study; the current contract is self-contained in this spec. The study is not part of distribution or validation. Actor: skill maintainer/evaluator. Precondition: authorized authoring and evaluation in a permitted environment. This feature belongs to the library; it is not an Ox product feature.

## Preserved technical contracts

The declarations below retain the proposed IDs, scenarios and oracles. REQ-01..03 are capabilities the skill must teach. AC-01..04 require exercising concrete deliverables; text review alone does not approve them. Product/platform integrations remain future work when unavailable.

- REQ-01: Nodes/edges have types, identity and provenance bound to the snapshot.
- REQ-02: Inferred relationships are not presented as extracted/resolved facts.
- REQ-03: Dense graphs operate with query limits and do not block the interface.

- AC-01 → REQ-01: A valid call edge can be traced to its location and method; oracle: known synthetic corpus.
- AC-02 → REQ-02: An inferred relationship incorrectly marked as verified is rejected; oracle: provenance schema/assertion.
- AC-03 → REQ-03: A change removes a stale edge in the new snapshot; oracle: before/after fixture.
- AC-04 → REQ-03: A subgraph query applies limits and reports truncation; oracle: deterministically generated large graph.

## Additional authoring criteria

- REQ-04: Provide a reusable method with precise selection, inputs, references and verifiable scenarios.
- AC-05 → REQ-04: Content review and local validation confirm a complete entry, substantive references, boundaries and a valid bridge.
- AC-06 → REQ-04: An observed agent trial distinguishes positive requests, negative requests and adversarial behavior; limitations and raw response are preserved.

Do not replace AC-01..04 with AC-05/06. Consumer versions, platform, data and authorization must be known before integration. Skill approval does not approve product subsystems.
