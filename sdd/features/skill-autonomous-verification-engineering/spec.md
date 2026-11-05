# Authoring and evaluation of autonomous-verification-engineering

Historical origin: external study; the current contract is self-contained in this spec. The study is not part of distribution or validation. Actor: skill maintainer/evaluator. Precondition: authorized authoring and evaluation in a permitted environment. This feature belongs to the library; it is not an Ox product feature.

## Preserved technical contracts

The declarations below retain the proposed IDs, scenarios and oracles. REQ-01..03 are capabilities the skill must teach. AC-01..04 require exercising concrete deliverables; text review alone does not approve them. Product/platform integrations remain future work when unavailable.

- REQ-01: Every verdict is bound to an explicit criterion, method and input snapshot.
- REQ-02: Failures, non-execution and stale evidence are not promoted to approved.
- REQ-03: Execution permission and result acceptance are independent controls.

- AC-01 → REQ-01: A criterion with a real test and versioned input can be marked APPROVED; oracle: bound execution artifact.
- AC-02 → REQ-02: A skipped or unavailable test remains UNVERIFIED; oracle: fixture without an executable.
- AC-03 → REQ-02: A change after validation invalidates only criteria dependent on changed inputs; oracle: freshness test.
- AC-04 → REQ-03: An agent without deployment authorization cannot publish even after verification passes; oracle: boundary mock plus permitted integration.

## Additional authoring criteria

- REQ-04: Provide a reusable method with precise selection, inputs, references and verifiable scenarios.
- AC-05 → REQ-04: Content review and local validation confirm a complete entry, substantive references, boundaries and a valid bridge.
- AC-06 → REQ-04: An observed agent trial distinguishes positive requests, negative requests and adversarial behavior; limitations and raw response are preserved.

Do not replace AC-01..04 with AC-05/06. Consumer versions, platform, data and authorization must be known before integration. Skill approval does not approve product subsystems.
