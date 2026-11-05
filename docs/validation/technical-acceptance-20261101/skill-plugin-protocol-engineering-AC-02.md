# Criterion review: skill-plugin-protocol-engineering AC-02

An incompatible or malformed plugin receives an explicit failure without persistent mutation; oracle: compatibility harness.

Observation: Incompatible/malformed/oversized frames are rejected and later calls fail closed, but tests do not independently compare persistent state before/after.

Scope/limits: Add a persistent-state sentinel oracle around incompatible and malformed startup/requests.

Verdict: INCONCLUSIVE. New Cargo/consumer runs are in cargo.log and consumer.log. For partial UI criteria the previous product observations were inspected as partial evidence only; no new graphical run is claimed. The evaluated subjects are the frozen files identified by consumer-snapshot.json, compared byte-for-byte to the source used in the runs. This skill verdict is not acceptance of a later live product. Toolchain 1.99.1 on Linux; system libraries/environment are not fully snapshotted. Oracle suitability was assessed from test assertions, not from exit zero alone.
