# Compatibility and failure windows

Test host N/plugin N, host N/plugin N+1 and host N+1/plugin N only when the declared compatibility range promises them. Include unknown optional fields and missing required fields. Reject incompatible semantics rather than parsing a new value into an old default.

Track request admission, effect start, durable effect, reply delivery and resource release. A crash after the effect but before the reply creates an uncertain outcome: replaying a non-idempotent request may duplicate it. Use an operation key with a documented reconciliation lookup, or return uncertain and require inspection. Do not promise exactly-once from message IDs alone.

Recovery tests need a deadline, captured exit reason, remaining handles and persistent before/after state. Terminate a test peer at each window, then verify that admission closes, requests resolve or expire and restart does not inherit old grants. Upgrades need rollback behavior for both protocol and plugin-owned state.
