# Authoring and evaluation of code-context-engineering

Historical origin: external study; the current contract is self-contained in this spec. The study is not part of distribution or validation. Actor: skill maintainer/evaluator. Precondition: authorized authoring and evaluation in a permitted environment. This feature belongs to the library; it is not an Ox product feature.

## Preserved technical contracts

The declarations below retain the proposed IDs, scenarios and oracles. REQ-01..03 are capabilities the skill must teach. AC-01..04 require exercising concrete deliverables; text review alone does not approve them. Product/platform integrations remain future work when unavailable.

- REQ-01: Queries return context bound to an identifiable repository version.
- REQ-02: Incremental changes invalidate dependent results without requiring a full scan by default.
- REQ-03: Syntactic, semantically resolved and inferred data remain distinguishable.

- AC-01 → REQ-01: A symbol query reports file, range, snapshot and method; oracle: fixtures with verified positions.
- AC-02 → REQ-02: A rename/edit invalidates old entries and updates affected ones; oracle: controlled repository mutations.
- AC-03 → REQ-03: An ambiguous call without semantics is not labeled a verified reference; oracle: same-name code and imports.
- AC-04 → REQ-03: An absent LSP results in explicit degradation without invented results; oracle: deliberately unavailable server.

## Additional authoring criteria

- REQ-04: Provide a reusable method with precise selection, inputs, references and verifiable scenarios.
- AC-05 → REQ-04: Content review and local validation confirm a complete entry, substantive references, boundaries and a valid bridge.
- AC-06 → REQ-04: An observed agent trial distinguishes positive requests, negative requests and adversarial behavior; limitations and raw response are preserved.

Do not replace AC-01..04 with AC-05/06. Consumer versions, platform, data and authorization must be known before integration. Skill approval does not approve product subsystems.
