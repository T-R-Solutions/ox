# Criterion review: tool-output-engineering AC-02

ANSI, partial UTF-8, binary output and unexpected formats receive explicit fallback; oracle: adversarial corpus.

APPROVED in the following evaluated scope: Known ok:/error: command fixture plus adversarial raw bytes; exit status and complete raw files; byte-count heuristic only. No general CLI/streaming parser or billing measurement claim.

Observed: output_ac02_fallback: ANSI, incomplete UTF-8, binary NUL/FF and unknown format all explicitly fall back; no raw terminal escape remains in display; raw bytes match.

Method: inspect the independent assertions and concrete implementation, execute commands captured in replay/receipt.json or environment.json/gui-02/result.json, and inspect their full logs. Expected values are independently specified fixture values; exit zero alone is insufficient. The original criterion and skill contracts are unchanged.

Consumer: tools/governance/consumers/models.rs; oracle: tools/governance/consumers/model_tests.rs. Broader contracts/exclusions: tools/governance/consumers/README.md. All prior envelopes are byte-preserved in previous/. This does not accept a production Ox subsystem or infer new agent effectiveness.

Final input stabilization: rustfmt joined two lines in model_tests.rs without changing behavior. The exact previous source, reviews and envelopes are preserved in before-format/. All 16 model tests, seven process/filesystem tests, isolation controls and the complete graphical flow were rerun successfully with the stabilized file set: replay-final/ and gui-final/. This is a new observed execution, not a hash-only renewal. No original skill criterion or product source changed.
