# Specification: product-plugin-host

Actor: local application caller using explicitly supplied local fixtures.
Scope: bounded Linux x86_64 library slice, no UI integration or remote services.

- REQ-01: A real local plugin process negotiates protocol 1.0 and completes a correlated echo request.
- AC-01 → REQ-01: A real local plugin process negotiates protocol 1.0 and completes a correlated echo request.
- REQ-02: An incompatible major version is rejected before any operation.
- AC-02 → REQ-02: An incompatible major version is rejected before any operation.
- REQ-03: Echo requires both plugin-advertised support and caller grant; denied operations are not sent.
- AC-03 → REQ-03: Echo requires both plugin-advertised support and caller grant; denied operations are not sent.
- REQ-04: Malformed, oversized and mismatched response frames fail the host without approval.
- AC-04 → REQ-04: Malformed, oversized and mismatched response frames fail the host without approval.
- REQ-05: A silent plugin times out within the configured deadline and an unexpected exit is distinguished.
- AC-05 → REQ-05: A silent plugin times out within the configured deadline and an unexpected exit is distinguished.
- REQ-06: Shutdown closes admission, reaps the child and releases its socket; recovery starts a new independent host.
- AC-06 → REQ-06: Shutdown closes admission, reaps the child and releases its socket; recovery starts a new independent host.

No sandbox, remote-provider integration, production readiness or F0 completion is claimed.
