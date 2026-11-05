# Authoring and evaluation of agent-runtime-engineering

Historical origin: external study; the current contract is self-contained in this spec. The study is not part of distribution or validation. Actor: skill maintainer/evaluator. Precondition: authorized authoring and evaluation in a permitted environment. This feature belongs to the library; it is not an Ox product feature.

## Preserved technical contracts

The declarations below retain the proposed IDs, scenarios and oracles. REQ-01..03 are capabilities the skill must teach. AC-01..04 require exercising concrete deliverables; text review alone does not approve them. Product/platform integrations remain future work when unavailable.

- REQ-01: Sessions and tasks have legal states, stable identifiers and rejected transitions.
- REQ-02: Cancellation, shutdown and restart release resources without changing permission scope.
- REQ-03: Observed actions and agent-declared conclusions have distinct provenance.

- AC-01 → REQ-01: An out-of-order event does not cause an unwarranted completion; oracle: transition test with an adversarial sequence.
- AC-02 → REQ-02: Process death produces a status and cleanup of associated resources; oracle: controlled process with an injected failure.
- AC-03 → REQ-02: Cancellation during heavy output leaves no orphaned tasks; oracle: harness with streams and a deadline.
- AC-04 → REQ-03: A “done” message without a validated artifact does not change the verdict to approved; oracle: deterministic adversarial case.

## Additional authoring criteria

- REQ-04: Provide a reusable method with precise selection, inputs, references and verifiable scenarios.
- AC-05 → REQ-04: Content review and local validation confirm a complete entry, substantive references, boundaries and a valid bridge.
- AC-06 → REQ-04: An observed agent trial distinguishes positive requests, negative requests and adversarial behavior; limitations and raw response are preserved.

Do not replace AC-01..04 with AC-05/06. Consumer versions, platform, data and authorization must be known before integration. Skill approval does not approve product subsystems.
