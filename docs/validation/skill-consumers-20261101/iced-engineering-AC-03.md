# Criterion review: iced-engineering AC-03

Extreme resizing does not lose essential actions; oracle: layout review at documented sizes.

APPROVED in the following evaluated scope: Separate Iced 0.14 graphical consumer under dedicated Xwayland; actual XTEST input, widget focus query, captures at 240x180/1600x1000 and relayout counters. Detail text persists; collapse routes focus to command input, expand restores detail. No product UI/native Wayland or arbitrary-size acceptance.

Observed: iced_four_criteria plus pixel review: full labels/actions remain visible at actual 240x180 and 1600x1000; Slow/Pane/Graph work at both sizes, Quit exits at minimum. Initial clipped Quit failure is preserved in gui-01; fixed run and reviewed captures are gui-02.

Method: inspect the independent assertions and concrete implementation, execute commands captured in replay/receipt.json or environment.json/gui-02/result.json, and inspect their full logs. Expected values are independently specified fixture values; exit zero alone is insufficient. The original criterion and skill contracts are unchanged.

Consumer: tools/governance/consumers/gui.rs; oracle: tools/governance/consumers/gui_tests.rs. Broader contracts/exclusions: tools/governance/consumers/README.md. All prior envelopes are byte-preserved in previous/. This does not accept a production Ox subsystem or infer new agent effectiveness.

Final input stabilization: rustfmt joined two lines in model_tests.rs without changing behavior. The exact previous source, reviews and envelopes are preserved in before-format/. All 16 model tests, seven process/filesystem tests, isolation controls and the complete graphical flow were rerun successfully with the stabilized file set: replay-final/ and gui-final/. This is a new observed execution, not a hash-only renewal. No original skill criterion or product source changed.
