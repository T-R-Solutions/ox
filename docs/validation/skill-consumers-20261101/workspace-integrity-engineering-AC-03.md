# Criterion review: workspace-integrity-engineering AC-03

An injected failure between temporary-file creation and rename leaves no incorrect “done” record; oracle: crash test.

APPROVED in the following evaluated scope: Owned Linux temporary fixtures, static paths, cooperating cross-process writers and a single transaction. Exact bytes represent snapshots. Polling hint plus actual read. No hostile path replacement/noncooperating write-race guarantee, PID reuse recovery or power-loss durability.

Observed: workspace_ac03_crash: child exits 91 after PREPARED/before rename; original is unchanged, no DONE is recorded; after reaping, recovery preserves the unapplied proposal and records RECOVERED_UNAPPLIED.

Method: inspect the independent assertions and concrete implementation, execute commands captured in replay/receipt.json or environment.json/gui-02/result.json, and inspect their full logs. Expected values are independently specified fixture values; exit zero alone is insufficient. The original criterion and skill contracts are unchanged.

Consumer: tools/governance/consumers/operations.rs; oracle: tools/governance/consumers/operation_tests.rs. Broader contracts/exclusions: tools/governance/consumers/README.md. All prior envelopes are byte-preserved in previous/. This does not accept a production Ox subsystem or infer new agent effectiveness.

Final input stabilization: rustfmt joined two lines in model_tests.rs without changing behavior. The exact previous source, reviews and envelopes are preserved in before-format/. All 16 model tests, seven process/filesystem tests, isolation controls and the complete graphical flow were rerun successfully with the stabilized file set: replay-final/ and gui-final/. This is a new observed execution, not a hash-only renewal. No original skill criterion or product source changed.
