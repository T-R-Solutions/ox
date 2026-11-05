# Authoring and evaluation of workspace-integrity-engineering

Historical origin: external study; the current contract is self-contained in this spec. The study is not part of distribution or validation. Actor: skill maintainer/evaluator. Precondition: authorized authoring and evaluation in a permitted environment. This feature belongs to the library; it is not an Ox product feature.

## Preserved technical contracts

The declarations below retain the proposed IDs, scenarios and oracles. REQ-01..03 are capabilities the skill must teach. AC-01..04 require exercising concrete deliverables; text review alone does not approve them. Product/platform integrations remain future work when unavailable.

- REQ-01: All file changes respect the authorized root and observed version.
- REQ-02: Concurrent edits are detected before silent overwrites.
- REQ-03: A crash during writing allows partial-state detection and recovery without silent loss.

- AC-01 → REQ-01: An attempted write outside the root through .. or a symlink is rejected; oracle: adversarial path fixture.
- AC-02 → REQ-02: Two agents edit the same version: the second write conflicts or applies a verified merge; oracle: concurrency test.
- AC-03 → REQ-03: An injected failure between temporary-file creation and rename leaves no incorrect “done” record; oracle: crash test.
- AC-04 → REQ-03: An externally changed file invalidates the hash/snapshot; oracle: watcher plus actual-read verification.

## Additional authoring criteria

- REQ-04: Provide a reusable method with precise selection, inputs, references and verifiable scenarios.
- AC-05 → REQ-04: Content review and local validation confirm a complete entry, substantive references, boundaries and a valid bridge.
- AC-06 → REQ-04: An observed agent trial distinguishes positive requests, negative requests and adversarial behavior; limitations and raw response are preserved.

Do not replace AC-01..04 with AC-05/06. Consumer versions, platform, data and authorization must be known before integration. Skill approval does not approve product subsystems.
