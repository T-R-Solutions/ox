# Deployment and recovery decisions

Source: Michael T. Nygard, *Release It!*, Second Edition, local EPUB (historical library source: `docs/system/Release It.epub`; not required at runtime). XHTML paths are precise archive locations. Examples below are illustrative, not executed applications.

## Design the intermediate states

**Action/context:** For a rollout that changes state, contracts or resource requirements, enumerate old/new code, schema, configuration, assets and clients that can coexist. Separate preparation, traffic drain, activation/readiness and cleanup. Choose rolling, canary, replacement or a deliberate maintenance window according to impact and available capacity.

**Evidence/rationale:** Ch12 f_0112; Ch13 f_0113–0120, especially f_0118 “Phases of Deployment” and its nested timeline. Failures occur during transitions that a final-state design ignores. A canary reduces exposure; it still exposes some traffic.

**Exceptions/costs:** Zero downtime is not free or always required. Parallel capacity, compatibility code and longer migrations cost money and maintenance. A long-lived session may outlast an instance. A green process probe is not readiness. Do not infer that container startup means the application is warm.

**Validate:** Exercise the chosen transition, interrupted deployment, drain expiry, startup failure and restoration of traffic. Define stop thresholds from relevant user outcomes before rollout. Verify the previous version can operate against changed state, or explicitly choose forward recovery.

## Expand, migrate, contract with data evidence

**Action/context:** Where continuous operation matters, add compatible storage structures, deploy readers/writers able to coexist, migrate with version/concurrency checks, verify completeness, then remove old structures after consumers and recovery windows allow it. Use authorized representative historical fixtures, including irregular data.

**Evidence/rationale:** f_0118 “Relational Database Schemata,” “Schemaless Databases,” “Cleanup,” and translation/trickle diagrams. Schema-free storage still has application expectations. A read-triggered migration must not lose concurrent writes or recurse indefinitely.

**Exceptions/costs:** Additive DDL can lock, alter client behavior or consume capacity; adding a trigger is not automatically safe. Lazy migration increases request latency and leaves cold records; batch migration creates load. Bidirectional shims can loop or diverge. Destructive cleanup can eliminate rollback even when binaries are retained.

**Validate:** Test old/new readers and writers with old/new data, duplicates, crashes mid-migration and concurrency. Compare counts plus semantic invariants, not counts alone. Verify constraint enforcement and completion before contraction.

**Before/after example:** Renaming a required field immediately breaks old readers. An explicit transition accepts the old representation, writes or translates the new one under a defined ownership rule, records migration progress and removes compatibility only after consumer evidence permits it. Exact dual-write/transaction mechanics depend on the store and invariants.

## Verify compatibility as observable behavior

**Action/context:** Inventory request/response syntax, semantics, errors, authorization, routing and timing obligations. Test consumer creation of valid requests and handling of every allowed response; separately verify the provider. For a necessary breaking change, define coexistence, migration and retirement criteria.

**Evidence/rationale:** Ch14 f_0121–0124, inbound/outbound and split-test diagrams. A mock cannot prove the actual provider still honors its contract; an integration happy path cannot prove the consumer handles all permitted responses.

**Exceptions/costs:** Added fields can break strict consumers; relaxed validation can violate security or business invariants. Existing permissiveness signals migration risk, not an obligation to preserve a vulnerability forever. Contract suites add maintenance and cannot replace live integration/operational evidence. Versions may use URLs, headers, media types or protocol-native mechanisms; do not impose HTTP on non-HTTP APIs.

**Validate:** Run mixed-version interactions on the same logical records and failures allowed by the contract. Check caches, assets, redirects and old clients where relevant. Report which compatibility claims remain untested.

## Rehearse faults as bounded experiments

**Action/context:** State a hypothesis about an observable invariant, establish a baseline, identify a discriminating fault, define exposure and abort thresholds, confirm authorization and rehearse recovery. Start with a controlled environment and a fault relevant to the task; expand only with evidence and permission appropriate to the environment.

**Evidence/rationale:** Ch17 f_0140–0146, especially f_0144 prerequisites/design/injection/automation. Study successful containment and near misses as well as outages. Combine signals across dependencies; monitoring can fail with the service.

**Exceptions/costs:** Random production termination is not a prerequisite. Fault combinations may be meaningful but can exceed tolerable loss. Experiments can cause data loss, customer disruption and cleanup work; the useful result may be a documented limitation. A simulation's pass does not establish production availability or universal resilience.

**Validate:** Record fault start/end, cohort, system version, workload, observation method, result, abort behavior and recovery. Check lingering effects after stopping injection. Distinguish a supported conclusion from a hypothesis, and turn a demonstrated defect into an appropriately scoped regression check.
