# Criterion review: skill-plugin-protocol-engineering AC-01

A compatible, authorized plugin negotiates only granted capabilities; oracle: client/provider fixture and message assertions.

Observation: Host tests negotiate echo and reject denied/unsupported CALLs using a peer that exits 21 on any unauthorized CALL.

Scope/limits: Local trusted ASCII fixture only; no sandbox or third-party interoperability.

Verdict: APPROVED. New Cargo/consumer runs are in cargo.log and consumer.log. For partial UI criteria the previous product observations were inspected as partial evidence only; no new graphical run is claimed. The evaluated subjects are the frozen files identified by consumer-snapshot.json, compared byte-for-byte to the source used in the runs. This skill verdict is not acceptance of a later live product. Toolchain 1.99.1 on Linux; system libraries/environment are not fully snapshotted. Oracle suitability was assessed from test assertions, not from exit zero alone.
