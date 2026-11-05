# Specification: product-agent-runtime

Actor: local application caller using explicitly supplied local fixtures.
Scope: bounded Linux x86_64 library slice, no UI integration or remote services.

- REQ-01: A controlled local adapter runs to success or nonzero failure with observed process exit and ordered lifecycle events.
- AC-01 → REQ-01: A controlled local adapter runs to success or nonzero failure with observed process exit and ordered lifecycle events.
- REQ-02: Cancellation enters Cancelling before an observed terminal Cancelled outcome and reaps the owned child.
- AC-02 → REQ-02: Cancellation enters Cancelling before an observed terminal Cancelled outcome and reaps the owned child.
- REQ-03: Wrong-generation, duplicate, out-of-order and late completion events cannot corrupt terminal or current session state.
- AC-03 → REQ-03: Wrong-generation, duplicate, out-of-order and late completion events cannot corrupt terminal or current session state.
- REQ-04: Execution deadlines stop a hanging local adapter and recovery creates a fresh attempt with no old events or grants.
- AC-04 → REQ-04: Execution deadlines stop a hanging local adapter and recovery creates a fresh attempt with no old events or grants.
- REQ-05: Runtime and controlled adapter preserve a workspace sentinel; output and supervision limitations are explicit.
- AC-05 → REQ-05: Runtime and controlled adapter preserve a workspace sentinel; output and supervision limitations are explicit.

No sandbox, remote-provider integration, production readiness or F0 completion is claimed.
