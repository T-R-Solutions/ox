# Criterion review: agent-usage-accounting AC-01

Usage without available pricing returns unknown cost, not zero; oracle: model fixture without a rate.

APPROVED in the following evaluated scope: Synthetic provider contract: cached tokens are a subset of input; integer rates; provider/event identity; explicit UTC-03:00 fixed offset at 02:59:59/03:00:00 UTC. No real provider pricing, timezone database or DST acceptance.

Observed: usage_ac01_missing_price: no rate returns None; explicit rates return 230 integer units, distinguishing unknown from zero.

Method: inspect the independent assertions and concrete implementation, execute commands captured in replay/receipt.json or environment.json/gui-02/result.json, and inspect their full logs. Expected values are independently specified fixture values; exit zero alone is insufficient. The original criterion and skill contracts are unchanged.

Consumer: tools/governance/consumers/models.rs; oracle: tools/governance/consumers/model_tests.rs. Broader contracts/exclusions: tools/governance/consumers/README.md. All prior envelopes are byte-preserved in previous/. This does not accept a production Ox subsystem or infer new agent effectiveness.

Final input stabilization: rustfmt joined two lines in model_tests.rs without changing behavior. The exact previous source, reviews and envelopes are preserved in before-format/. All 16 model tests, seven process/filesystem tests, isolation controls and the complete graphical flow were rerun successfully with the stabilized file set: replay-final/ and gui-final/. This is a new observed execution, not a hash-only renewal. No original skill criterion or product source changed.
