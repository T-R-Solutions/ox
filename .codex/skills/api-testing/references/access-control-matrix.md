# Authorization matrix and effect oracle

Use when identity, object ownership or delegated permissions change. Source: Madden, API Security in Action, ch. 3 §3.6 pp. 87–97 (B04 in [reading record](portable-sources.md)). The existing boundary scenarios cover denial; the additional gap is delegation escalation and a reproducible state oracle.

1. Obtain the actual policy from spec. Enumerate actor × tenant × object × action, including unauthenticated, owner, same-tenant nonowner, other tenant, read-only and delegator cases. Keep token authentication separate from object authorization.
2. For permission grants, ask whether a reader can create another identity with higher authority. Derive the permitted grant ceiling from product policy; do not copy the book's moderator rule as a universal requirement.
3. Snapshot state and observable outgoing effects before each call. Assert expected status/payload and exact permitted state change; denial must reveal no protected content and produce no prohibited write/event.
4. Include valid access so denying everything fails. Include revoked/expired credentials and alternate routes when supported. Use real adapters for claims about middleware, serialization or persistence.
5. Restore disposable state and prove the oracle rejects a seeded missing ownership check. Record which dependencies were simulated.

Local illustration: the authoring-library check `PYTHONDONTWRITEBYTECODE=1 python3 src/scripts/run_sdd_checks.py` (run from that repository root; unavailable and not required in an isolated skill copy) exercises AC-01 in the bounded-work pilot. It is an in-process API fixture, not HTTP authentication or production authorization validation.
