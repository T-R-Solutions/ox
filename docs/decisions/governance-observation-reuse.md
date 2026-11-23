# Reuse of authenticated succession within one observation — 2026-11-18

Status: proposed implementation; independent review and final executions required.
Scope: R3-1/R3-3 repeated validation of the same documentary succession inputs.

## Observed problem and alternatives

A real isolated historical-link test failed after its existing 120-second checker
deadline (one test, 124.905 seconds, TimeoutExpired). The standalone checker also
completed successfully after several minutes. These results do not establish the
cause of the separate complete-run exit 143; that cause remains unknown.

A bounded profile of three preservation_digest(README.md) operations observed 132
active-registry validations and 180 historical-ledger validations. Active validation
accounted for 1.914 of 2.909 profiled seconds. The predecessor chain repeatedly
requests the same authenticated historical facts within one public operation.
The observed unprofiled comparison used five sequential operations per version,
same root and README bytes: before 0.404–0.424 seconds, candidate 0.132–0.133 seconds,
with identical returned digests. Run order was before then after; this establishes
the narrow observed workload, not cold-cache performance or whole-suite throughput.

Raising the deadline would retain repeated work and would not address its growth.
A persistent cache based on path, size or mtime would weaken content and path
validation. Removing historical bindings or changing acceptance assertions is not
an alternative. Reuse is instead bounded to one explicit public observation.

## Decision

Keep the implementation in document_ledger.py. An explicit observation context
around preservation_bytes reuses only fully validated records/succession_records
results, with immutable nested containers. It never caches predecessor decisions,
unknown caller buffers, mutable authority validation or live-file bytes.

The first validation discovers every input used by those two registry results:
registries, historical preimages, active before/decision/review bindings and both
supported historical anchors, including the log-repair instruction registry and
preimages. Capture these bytes through the existing safe file function, validate
again and require unchanged read set/bytes before exposing a complete cache.
No partially initialized cache is visible during this process.

Bind the state to both the lexical absolute root and its canonical identity,
plus the operation context; a symlink alias cannot borrow validated state. Nested observations
of another root validate their own inputs; same-root nested use belongs to the
outer observation. A shared lifetime is revoked by its owning scope, including
for retained copies of a ContextVar context. A borrowed scope must reject exit
after its owner expires. At exit, including body exceptions, discard the state and
reopen every captured path through file(), comparing bytes and rechecking lexical
parents, symlinks and containment. Changed, missing or unsafe evidence rejects the
operation. This exit rejection is outside strict=False projections. No result may
be published before successful context exit. Outside the explicit scope, registry
calls retain fresh validation on each invocation.

This changes when repeated immutable-history validation happens within a bounded
operation; it is not a new authorization layer or a new succession registry. The
helper transition is recorded as the next version in the existing data registry,
with its prior exact bytes, this decision and independent review. Existing data
records and historical observations remain unchanged.

## Guarantees and limits

Persistent corruption, unsafe paths, downgrade, contract changes and checkout/copy
conflicts remain rejected. Live inputs are read and judged on every projection.
Before/after observations are not an atomic filesystem snapshot: a hostile writer
that transiently changes and restores evidence within the operation may evade the
boundary comparison. Repeated reads previously offered no general atomicity either;
this design specifically defers repeated historical checks to the boundary and
must not claim equivalent detection timing under hostile concurrent mutation.
No OS sandbox, authentication of human declarations or cross-process cache is added.

Required regressions include immutable results; ordinary and strict=False behavior;
changed, missing and symlinked evidence across every input class; symlinked parents;
same-size mutation with restored mtime; body exceptions; fresh later observations;
nested-root isolation, copied contexts after owner exit and borrowed scopes that
start before but finish after their owner. Preserve both matching and unknown-input oracles.
Compare equivalent results and actual checker/test execution under the unchanged
120-second deadline. Focused tests and a microbenchmark do not replace the full
required inventory, independent copied commands or final feature gates.

Recovery restores only the helper/ledger/test delta and its active registry version
from retained preimages. Do not rewrite prior reports, delete evidence or update a
Python hash constant to accept routine documentary evolution.
