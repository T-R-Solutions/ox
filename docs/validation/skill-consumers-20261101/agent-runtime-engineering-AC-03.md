# Criterion review: agent-runtime-engineering AC-03

Cancellation during heavy output leaves no orphaned tasks; oracle: harness with streams and a deadline.

APPROVED in the following evaluated scope: Controlled direct child continuously writes stdout/stderr; bounded retained output, observed kill/wait and two joined reader threads. No arbitrary process tree/grandchild-pipe supervision.

Observed: runtime_ac03_cancel_output: final replay observes over 1 MiB on each stream before cancellation, retains 4096 bytes per stream, reaps the PID and joins both readers in under two seconds.

Method: inspect the independent assertions and concrete implementation, execute commands captured in replay/receipt.json or environment.json/gui-02/result.json, and inspect their full logs. Expected values are independently specified fixture values; exit zero alone is insufficient. The original criterion and skill contracts are unchanged.

Consumer: tools/governance/consumers/operations.rs; oracle: tools/governance/consumers/operation_tests.rs. Broader contracts/exclusions: tools/governance/consumers/README.md. All prior envelopes are byte-preserved in previous/. This does not accept a production Ox subsystem or infer new agent effectiveness.

Final input stabilization: rustfmt joined two lines in model_tests.rs without changing behavior. The exact previous source, reviews and envelopes are preserved in before-format/. All 16 model tests, seven process/filesystem tests, isolation controls and the complete graphical flow were rerun successfully with the stabilized file set: replay-final/ and gui-final/. This is a new observed execution, not a hash-only renewal. No original skill criterion or product source changed.
