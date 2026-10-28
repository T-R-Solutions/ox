# Choose and verify a transition

Read when changing contracts, replacing a component or modernizing a system.

Characterize inputs, outputs, errors, ordering, identity, serialization, timing and
external effects at real entry points. Use historical fixtures and caller inspection,
not merely tests that repeat the proposed implementation. Mark unknown business rules.
A rename can affect reflection, serialized names or persisted identifiers even when
source callers compile. Include transitive/runtime dependency contracts and old data.

| Option | Choose when / cost to verify |
| --- | --- |
| Retain | Current behavior meets requirements; compare cost of tolerated limitation with migration |
| Refactor | Behavior can stay stable and a local seam solves maintenance; characterize before/after |
| Incremental replacement | A separable slice and coexistence path exist; temporary routing and dual implementations cost maintenance |
| Rewrite | Concrete constraints outweigh lost behavior knowledge and cutover risk; require data/consumer transition evidence too |

Use branch by abstraction when one interface can support old and replacement suppliers.
Move a bounded caller slice through the seam, compare outcomes and switch gradually;
delete the obsolete supplier and unnecessary seam after completion. An adapter should
isolate a specific semantic difference, not hide inconsistent authority.
[Fowler, Branch By Abstraction](https://www.martinfowler.com/bliki/BranchByAbstraction.html).

Use strangler fig when traffic/entry points can be intercepted and slices replaced
while the original remains usable. The routing facade can become a bottleneck or
single failure point; price its complexity and removal. If traffic cannot be intercepted
or full replacement is small and lower-risk, compare another transition.
[Microsoft, Strangler Fig](https://learn.microsoft.com/pt-br/azure/architecture/patterns/strangler-fig).
Neither technique mandates services or a cloud vendor.

Make a matrix of producer/consumer, reader/writer and configuration versions for each
transition phase. Added fields, new enum values, relaxed validation and changed defaults
can break strict consumers. Events can outlive deployments; test replay and retention
horizons. Record intentional breaks and the version/order needed before emitting them.
Use agreed versioning policy, not version labels as proof of behavioral compatibility.
[SemVer](https://semver.org/spec/v2.0.0.html) communicates public API intent only.

For shadow traffic, select a representative permitted sample and compare normalized
semantic outputs, errors and cost. Suppress or sandbox writes, payments, notifications
and downstream effects; replaying a read can still invoke stateful behavior. Do not
send sensitive data to a new destination without existing authorization. Define how
nondeterminism/time differences affect the oracle before scoring differences.
A successful shadow path does not prove cutover, failover or all data compatibility.
