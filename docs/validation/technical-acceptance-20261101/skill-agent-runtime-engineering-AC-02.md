# Criterion review: skill-agent-runtime-engineering AC-02

Process death produces a status and cleanup of associated resources; oracle: controlled process with an injected failure.

Observation: Real failure returns Failed(17); additional Linux consumer asserts the PID disappears from /proc after observed completion.

Scope/limits: Direct-child/no-output fixture; descendants and stream resources absent.

Verdict: APPROVED. New Cargo/consumer runs are in cargo.log and consumer.log. For partial UI criteria the previous product observations were inspected as partial evidence only; no new graphical run is claimed. The evaluated subjects are the frozen files identified by consumer-snapshot.json, compared byte-for-byte to the source used in the runs. This skill verdict is not acceptance of a later live product. Toolchain 1.99.1 on Linux; system libraries/environment are not fully snapshotted. Oracle suitability was assessed from test assertions, not from exit zero alone.
