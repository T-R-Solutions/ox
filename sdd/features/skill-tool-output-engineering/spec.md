# Authoring and evaluation of tool-output-engineering

Historical origin: external study; the current contract is self-contained in this spec. The study is not part of distribution or validation. Actor: skill maintainer/evaluator. Precondition: authorized authoring and evaluation in a permitted environment. This feature belongs to the library; it is not an Ox product feature.

## Preserved technical contracts

The declarations below retain the proposed IDs, scenarios and oracles. REQ-01..03 are capabilities the skill must teach. AC-01..04 require exercising concrete deliverables; text review alone does not approve them. Product/platform integrations remain future work when unavailable.

- REQ-01: Each transformed output preserves exit code, error signals and a reference to raw output.
- REQ-02: Parser failure neither converts failure into success nor removes critical evidence.
- REQ-03: Reported savings distinguish actual counts from estimates and preserve method limitations.

- AC-01 → REQ-01: Output with a relevant error is summarized while preserving failure and location; oracle: command fixtures.
- AC-02 → REQ-02: ANSI, partial UTF-8, binary output and unexpected formats receive explicit fallback; oracle: adversarial corpus.
- AC-03 → REQ-02: Truncation is indicated with the location of complete raw output; oracle: output exceeding the limit.
- AC-04 → REQ-03: An estimated count is not shown as billed tokens; oracle: case without provider information.

## Additional authoring criteria

- REQ-04: Provide a reusable method with precise selection, inputs, references and verifiable scenarios.
- AC-05 → REQ-04: Content review and local validation confirm a complete entry, substantive references, boundaries and a valid bridge.
- AC-06 → REQ-04: An observed agent trial distinguishes positive requests, negative requests and adversarial behavior; limitations and raw response are preserved.

Do not replace AC-01..04 with AC-05/06. Consumer versions, platform, data and authorization must be known before integration. Skill approval does not approve product subsystems.
