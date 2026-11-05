# Specification: product-verification-engine

Actor: local application caller using explicitly supplied local fixtures.
Scope: bounded Linux x86_64 library slice, no UI integration or remote services.

- REQ-01: Approval requires a real local execution matching an explicit exit-code oracle and unchanged observed inputs.
- AC-01 → REQ-01: Approval requires a real local execution matching an explicit exit-code oracle and unchanged observed inputs.
- REQ-02: Missing evidence and agent/task completion claims never produce approval.
- AC-02 → REQ-02: Missing evidence and agent/task completion claims never produce approval.
- REQ-03: Observed failures remain in immutable history and contradictory same-input observations cannot silently replace rejection.
- AC-03 → REQ-03: Observed failures remain in immutable history and contradictory same-input observations cannot silently replace rejection.
- REQ-04: Changed implementation inputs, criterion or oracle invalidate dependent acceptance without invalidating unrelated criteria.
- AC-04 → REQ-04: Changed implementation inputs, criterion or oracle invalidate dependent acceptance without invalidating unrelated criteria.
- REQ-05: Five SDD states remain distinct and each observation exposes execution identity, command, result and evaluated content.
- AC-05 → REQ-05: Five SDD states remain distinct and each observation exposes execution identity, command, result and evaluated content.

No sandbox, remote-provider integration, production readiness or F0 completion is claimed.


## Bounded robustness clarification — 2026-11-05

Existing criteria include rejection of nonregular evidence with no approval;
regular files and symlinks to regular files retain the exact-byte behavior.
Metadata checks are not atomic capture. Linux nonblocking open covers FIFO
replacement at open, not universal filesystem cancellation. Deadline covers
subprocess supervision, not metadata/open/read/reap. Graceful close waits for
worker return; no universal close latency is promised. Every spawned direct
child has an owner through error cleanup; cleanup failures are visible alongside
the original error. No descendant or OS-isolation guarantee is introduced.
