# Criterion review: skill-iced-engineering AC-02

An expanded/collapsed pane preserves the defined content and focus; oracle: functional state test.

Observation: Existing expand/collapse evidence checks content/pixels; no complete keyboard-focus restoration oracle for the specialization.

Scope/limits: Exercise focused controls through collapse/expand and assert visible focus fallback/restoration.

Verdict: INCONCLUSIVE. New Cargo/consumer runs are in cargo.log and consumer.log. For partial UI criteria the previous product observations were inspected as partial evidence only; no new graphical run is claimed. The evaluated subjects are the frozen files identified by consumer-snapshot.json, compared byte-for-byte to the source used in the runs. This skill verdict is not acceptance of a later live product. Toolchain 1.99.1 on Linux; system libraries/environment are not fully snapshotted. Oracle suitability was assessed from test assertions, not from exit zero alone.
