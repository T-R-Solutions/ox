# Criterion review: workspace-integrity-engineering AC-01

An attempted write outside the root through .. or a symlink is rejected; oracle: adversarial path fixture.

APPROVED in the following evaluated scope: Owned Linux temporary fixtures, static paths, cooperating cross-process writers and a single transaction. Exact bytes represent snapshots. Polling hint plus actual read. No hostile path replacement/noncooperating write-race guarantee, PID reuse recovery or power-loss durability.

Observed: workspace_ac01_paths: ../ and symlink writes fail, inside/outside sentinels remain unchanged; normal in-root edit succeeds as positive control.

Method: inspect the independent assertions and concrete implementation, execute commands captured in replay/receipt.json or environment.json/gui-02/result.json, and inspect their full logs. Expected values are independently specified fixture values; exit zero alone is insufficient. The original criterion and skill contracts are unchanged.

Consumer: tools/governance/consumers/operations.rs; oracle: tools/governance/consumers/operation_tests.rs. Broader contracts/exclusions: tools/governance/consumers/README.md. All prior envelopes are byte-preserved in previous/. This does not accept a production Ox subsystem or infer new agent effectiveness.

Final input stabilization: rustfmt joined two lines in model_tests.rs without changing behavior. The exact previous source, reviews and envelopes are preserved in before-format/. All 16 model tests, seven process/filesystem tests, isolation controls and the complete graphical flow were rerun successfully with the stabilized file set: replay-final/ and gui-final/. This is a new observed execution, not a hash-only renewal. No original skill criterion or product source changed.
