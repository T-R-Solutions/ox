# Resource lifecycle, isolation and recovery runbook

Use for a reproducible leak, overload or cancellation risk. Sources: Adkins et al., Building Secure and Reliable Systems, ch. 8 pp. 159–161, ch. 9 pp. 186–188 and ch. 10 pp. 220–224 (B05); Jones/Hosking/Moss, GC Handbook, ch. 1 pp. 5–13 (B02); existing failure-controls supplies retry/cancellation reasoning. [Reading scope](portable-sources.md).

## Preconditions and hypothesis

Identify resource (FD, socket, pool slot, task, heap object), owner, acquire/release sites, abort paths and authorized disposable environment. Record workload, initial count, runtime, quota and abort bound. Missing ownership on exception is a hypothesis until observed.

## Procedure

1. Observe successful lifecycle and failed acquisition separately. Release only acquired resources, exactly once, on success, error and cancellation. A collector reclaiming memory does not establish prompt release of external resources.
2. Reject excess work before allocating expensive state. Define admitted, queued, active, completed, rejected and cancelled populations; bounds and deadlines belong in spec. A bounded queue alone says nothing about processing progress.
3. Stop arrivals, cancel an owned operation, wait for its actual termination and check resources return to baseline. Then admit new work and verify useful completion. An error response without termination is insufficient.
4. Cross-check lifecycle counters with OS handles/FDs when available; counters maintained by the same buggy code are not independent. On Linux a bounded fixture can inspect `/proc/self/fd`; document platform limits.
5. Check competing tenants/processes and dependency load if isolation is part of the claim. Separate process identity, privilege and resource quota: a process boundary alone proves none of these. Do not change shared kernel settings merely to run a local check.
6. For process/IPC changes, verify caller identity, descriptor inheritance, child termination/reaping, path/symlink handling and failure permissions using the actual platform contract. These are conditional investigative checks; current platform APIs were not verified in this restricted research.

## Validation and limits

The pilot has real temporary-file handles and asyncio tasks, synthetic identities and no external service. The authoring-library check `PYTHONDONTWRITEBYTECODE=1 python3 src/scripts/run_sdd_checks.py` (run from that repository root; unavailable and not required in an isolated skill copy) checks repeated success/error cleanup and blocked-worker cancellation under bounded admission, with seeded leaks/orphan work rejected. A soak test of another workload, real service isolation and OS sandbox enforcement remain separate checks. Stop if resource count grows past the fixture budget; cleanup in finally even when an assertion fails.

## Containment and recovery beyond the fixture

When the affected system has multiple compartments, record the enforcement point, caller identity, allowed crossings and shared dependencies. Test the declared failure boundary; a diagram or process label is not isolation evidence. Keep degraded authorization at least as restrictive as the required policy.

Separate recovery capability from the policy controlling rate and blast radius. Rehearse the normal mechanism at bounded scale rather than relying on an untested emergency path; verify that containment does not cut off authorized recovery access. Do not copy the book's separate rate-limiting microservice as mandatory architecture. A real recovery exercise needs actual environment/authority and remains unexecuted here.
