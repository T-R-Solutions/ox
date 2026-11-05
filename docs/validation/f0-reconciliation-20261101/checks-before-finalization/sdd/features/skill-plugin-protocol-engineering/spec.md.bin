# Authoring and evaluation of plugin-protocol-engineering

Historical origin: external study; the current contract is self-contained in this spec. The study is not part of distribution or validation. Actor: skill maintainer/evaluator. Precondition: authorized authoring and evaluation in a permitted environment. This feature belongs to the library; it is not an Ox product feature.

## Preserved technical contracts

The declarations below retain the proposed IDs, scenarios and oracles. REQ-01..03 are capabilities the skill must teach. AC-01..04 require exercising concrete deliverables; text review alone does not approve them. Product/platform integrations remain future work when unavailable.

- REQ-01: Negotiate version and capabilities without performing operations that are not yet authorized.
- REQ-02: Reject invalid messages, plugins and calls without corrupting host state.
- REQ-03: Define compatibility and recovery when a plugin crashes, disconnects or changes version.

- AC-01 → REQ-01: A compatible, authorized plugin negotiates only granted capabilities; oracle: client/provider fixture and message assertions.
- AC-02 → REQ-02: An incompatible or malformed plugin receives an explicit failure without persistent mutation; oracle: compatibility harness.
- AC-03 → REQ-03: A plugin exits during an operation and the host recovers/expires resources without blocking; oracle: crash and timeout test.
- AC-04 → REQ-03: An unauthorized plugin attempts to read a protected path and the host blocks the effect; oracle: sandbox integration on the target OS.

## Additional authoring criteria

- REQ-04: Provide a reusable method with precise selection, inputs, references and verifiable scenarios.
- AC-05 → REQ-04: Content review and local validation confirm a complete entry, substantive references, boundaries and a valid bridge.
- AC-06 → REQ-04: An observed agent trial distinguishes positive requests, negative requests and adversarial behavior; limitations and raw response are preserved.

Do not replace AC-01..04 with AC-05/06. Consumer versions, platform, data and authorization must be known before integration. Skill approval does not approve product subsystems.
