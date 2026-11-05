# Criterion review: skill-plugin-protocol-engineering AC-03

A plugin exits during an operation and the host recovers/expires resources without blocking; oracle: crash and timeout test.

Observation: Crash and timeout are distinct and bounded below 3 seconds; separate shutdown/recovery test observes socket directory removal and a fresh instance.

Scope/limits: Direct child and local fixture only.

Verdict: APPROVED. New Cargo/consumer runs are in cargo.log and consumer.log. For partial UI criteria the previous product observations were inspected as partial evidence only; no new graphical run is claimed. The evaluated subjects are the frozen files identified by consumer-snapshot.json, compared byte-for-byte to the source used in the runs. This skill verdict is not acceptance of a later live product. Toolchain 1.99.1 on Linux; system libraries/environment are not fully snapshotted. Oracle suitability was assessed from test assertions, not from exit zero alone.
