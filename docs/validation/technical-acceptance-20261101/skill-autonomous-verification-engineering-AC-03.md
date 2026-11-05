# Criterion review: skill-autonomous-verification-engineering AC-03

A change after validation invalidates only criteria dependent on changed inputs; oracle: freshness test.

Observation: Mutation test invalidates changed candidate/contract while independent criterion remains approved and rejected history is retained.

Scope/limits: Declared local inputs only.

Verdict: APPROVED. New Cargo/consumer runs are in cargo.log and consumer.log. For partial UI criteria the previous product observations were inspected as partial evidence only; no new graphical run is claimed. The evaluated subjects are the frozen files identified by consumer-snapshot.json, compared byte-for-byte to the source used in the runs. This skill verdict is not acceptance of a later live product. Toolchain 1.99.1 on Linux; system libraries/environment are not fully snapshotted. Oracle suitability was assessed from test assertions, not from exit zero alone.
