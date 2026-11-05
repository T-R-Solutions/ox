# Criterion review: plugin-protocol-engineering AC-02

An incompatible or malformed plugin receives an explicit failure without persistent mutation; oracle: compatibility harness.

APPROVED in the following evaluated scope: Frozen local Host and plugin fixture for protocol rejection; separate bwrap read-probe process for actual filesystem/PID/network namespace isolation. Disposable files only. Neither result adopts or approves an Ox production sandbox.

Observed: plugin_ac02_no_mutation: frozen host rejects incompatible handshake and malformed response; oracle compares working-directory entries and sentinel bytes, and confirms transport directories are removed after both failures.

Method: inspect the independent assertions and concrete implementation, execute commands captured in replay/receipt.json or environment.json/gui-02/result.json, and inspect their full logs. Expected values are independently specified fixture values; exit zero alone is insufficient. The original criterion and skill contracts are unchanged.

Consumer: tools/governance/consumers/plugin_host.rs; oracle: tools/governance/consumers/operation_tests.rs. Broader contracts/exclusions: tools/governance/consumers/README.md. All prior envelopes are byte-preserved in previous/. This does not accept a production Ox subsystem or infer new agent effectiveness.

Final input stabilization: rustfmt joined two lines in model_tests.rs without changing behavior. The exact previous source, reviews and envelopes are preserved in before-format/. All 16 model tests, seven process/filesystem tests, isolation controls and the complete graphical flow were rerun successfully with the stabilized file set: replay-final/ and gui-final/. This is a new observed execution, not a hash-only renewal. No original skill criterion or product source changed.
