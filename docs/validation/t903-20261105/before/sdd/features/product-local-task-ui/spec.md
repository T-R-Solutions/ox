# Specification: product-local-task-ui

Actor: local desktop user. One active controlled task; no arbitrary commands, remote agents, sandbox claim or general persistence. Scope authorized in sdd/project.md.

- REQ-01: Existing accessible workspace accepted; missing or inaccessible directory refused before process launch.
- AC-01 → REQ-01: Existing accessible workspace accepted; missing or inaccessible directory refused before process launch.
- REQ-02: Real controlled task execution reaches coherent observed success, failure or timeout states.
- AC-02 → REQ-02: Real controlled task execution reaches coherent observed success, failure or timeout states.
- REQ-03: Cancellation remains pending until child termination is observed.
- AC-03 → REQ-03: Cancellation remains pending until child termination is observed.
- REQ-04: Duplicate actions, workspace changes while busy and late events cannot corrupt another attempt.
- AC-04 → REQ-04: Duplicate actions, workspace changes while busy and late events cannot corrupt another attempt.
- REQ-05: Execution and verification leave the actual interface responsive.
- AC-05 → REQ-05: Execution and verification leave the actual interface responsive.
- REQ-06: Independent oracle approves the correct task-produced result and rejects incorrect bytes or identity.
- AC-06 → REQ-06: Independent oracle approves the correct task-produced result and rejects incorrect bytes or identity.
- REQ-07: Absent evidence and completion claims never approve a result.
- AC-07 → REQ-07: Absent evidence and completion claims never approve a result.
- REQ-08: Changed inputs invalidate current acceptance while preserving prior observations.
- AC-08 → REQ-08: Changed inputs invalidate current acceptance while preserving prior observations.
- REQ-09: Exclusive task directories preserve all preexisting workspace content.
- AC-09 → REQ-09: Exclusive task directories preserve all preexisting workspace content.
- REQ-10: Window close supervises owned work through termination before application exit.
- AC-10 → REQ-10: Window close supervises owned work through termination before application exit.
- REQ-11: Five evidence states, criterion, attempt, verification run, inputs and observation freshness are visible.
- AC-11 → REQ-11: Five evidence states, criterion, attempt, verification run, inputs and observation freshness are visible.


## Bounded robustness clarification — 2026-11-05

Existing criteria include rejection of nonregular evidence with no approval;
regular files and symlinks to regular files retain the exact-byte behavior.
Metadata checks are not atomic capture. Linux nonblocking open covers FIFO
replacement at open, not universal filesystem cancellation. Deadline covers
subprocess supervision, not metadata/open/read/reap. Graceful close waits for
worker return; no universal close latency is promised. Every spawned direct
child has an owner through error cleanup; cleanup failures are visible alongside
the original error. No descendant or OS-isolation guarantee is introduced.
