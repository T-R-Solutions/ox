# Architecture decisions

Read the applicable section only. Locators are inclusive, one-based **physical PDF pages**, including front matter: **F** = `docs/system/Fundamentos-da-arquitetura-de-software.pdf`, second edition (2025, supplied Portuguese translation); **H** = `docs/system/Software_Architecture_Hard_Parts.pdf` (first edition, 2021 release); **D** = `docs/system/Domain-Driven_Design.pdf` (first edition, 2021 release); **I** = `docs/system/Designing_Data_Intensive_Applications_2nd_Edition.pdf` (second edition, 2026). Recommendations below are contextual engineering synthesis, not normative compliance requirements.

## Quality scenarios before style selection

**Action/context:** When choosing a structure, translate relevant quality goals into observable scenarios with workload, failure conditions, thresholds, and ownership. Separate hard constraints from preferences. Compare at least one simpler feasible alternative.

**Evidence/rationale:** F chapters 4-6 pp98-162 and 19 pp597-616; H chapter 15 pp417-434; I chapters 1-2 pp25-88. A named attribute such as scalability does not specify what must scale or at what cost.

**Exceptions/costs:** A local change with established constraints needs no new quality catalog. Unknown thresholds can remain explicit assumptions pending a material decision; an arbitrary number is worse than acknowledged uncertainty. Measurement and prototypes cost time; target uncertainties that could reverse the decision.

**Validation:** Trace each hard requirement to a check or evidence source. Measure representative operations and failure modes; review assumptions with the responsible owner. A provider SLA is a contract input, not proof that the application meets its SLO.

Illustrative improvement: replace “use microservices for scale” with “the existing import path must process the agreed peak dataset within the acceptance window while interactive requests remain within their existing latency target.” Compare bounded background work, isolation within the deployment, and separate services using that scenario. Numbers must come from the project.

## Choose boundaries using change and runtime evidence

**Action/context:** Map semantic responsibilities, co-change, static dependencies, runtime calls, shared data, and organizational ownership before extracting modules or services. Keep a logical boundary in-process when it provides sufficient autonomy.

**Evidence/rationale:** F chapters 3 pp72-97, 7-8 pp163-216, 11 pp268-287, 14 pp332-361, 18 pp545-596; H chapters 2-5 pp43-148 and 7 pp203-236; D chapters 3-4 pp79-134 and 14 pp396-424. Static separation and runtime independence differ; splitting a cohesive operation can increase distributed coordination.

**Exceptions/costs:** Independent scaling, isolation, regulation, ownership, or deployment needs may justify distribution. Sharing a stable library may be cheaper than a remote service. A small controlled shared kernel can be legitimate; similar code does not necessarily represent the same business rule.

**Validation:** Walk a likely change and a dependency failure through the proposed boundary. Check all consumers, data writers, release coordination, resources, and recovery ownership. Compilation misses reflection, serialization names, jobs, scripts, and external callers. Coupling metrics are clues rather than universal thresholds.

## Select interaction and state together

**Action/context:** For each cross-boundary workflow, state who owns the decision, which reads must be fresh, which writes must be atomic, and when success is visible. Compare direct calls, queued commands, events, projections, and orchestration using those needs.

**Evidence/rationale:** F chapters 15 pp362-462, 18 pp545-596 and 20 pp617-640; H chapters 9-13 pp267-398; I chapters 8 pp301-368 and 12-13 pp511-608. Interaction syntax does not determine transactional guarantees. Events make past facts available; commands request actions that can fail.

**Exceptions/costs:** A local call or database transaction often suffices. Asynchrony can isolate temporary unavailability but adds lag, duplicate handling, queues, replay, and failure recovery. Orchestration centralizes workflow knowledge; choreography disperses it and can obscure end-to-end state. Neither wins universally.

**Validation:** Trace success, uncertain completion, partial failure, compensation failure, restart, and contract evolution. Specify allowed intermediate states. Do not describe a saga as ACID rollback or assume synchronous calls establish isolation. Use distributed-systems expertise only if the guarantee analysis actually requires it.

## Choose data models and infrastructure from access patterns

**Action/context:** Identify authoritative records, derived views, transaction and query shapes, data volume/skew, retention, freshness, and recovery requirements. Compare existing storage and managed services before adding a new database or processing platform.

**Evidence/rationale:** I chapters 1 pp25-56, 3-4 pp89-184, 11-13 pp475-608; H chapters 6 pp149-202, 10 pp301-316 and 14 pp399-416. Relational/document/graph/columnar structures and batch/stream processing optimize different workloads; polyglot storage creates integration work.

**Exceptions/costs:** A specialized index or engine can earn its cost for a demonstrated query or scale need. An event log, warehouse, lake, or data mesh is not mandatory. Columnar storage differs from wide-column models. Cloud services shift operating responsibilities and control; they do not eliminate failure, security, quotas, or lock-in.

**Validation:** Use representative data distributions and queries; verify durability, isolation, backup restoration, deletion propagation, and data ownership. Compare total operating/migration costs, not just request latency or storage price. Keep historical benchmark figures out of current claims.

## Evolve contracts and migrate without losing evidence

**Action/context:** Plan mixed-version operation and data migration before cutover. Identify writer/reader compatibility, unknown-field round trips, semantic defaults, checkpoints, reconciliation, and the point beyond which rollback cannot recover prior data.

**Evidence/rationale:** H chapters 4-6 pp81-202 and 13 pp383-398; D chapter 13 pp368-393; I chapter 5 pp185-220 and chapter 13 pp563-608. Schemas and behavior can break consumers independently of transport; data copying and dual writes introduce gaps and divergent updates.

**Exceptions/costs:** A coordinated downtime migration may be safer than elaborate live replication when the accepted availability requirement permits it. Expand/contract and shadow reads cost storage, implementation effort, and careful privacy controls. Compatibility is directional, not simply a version number.

**Validation:** Check old/new writers against old/new readers and retained records. Exercise interruption, repeated migration steps, delayed events, and restart. Reconcile counts and business invariants; counts alone miss wrong associations. Publish completed derived datasets through an explicit manifest or equivalent atomic switch; a completion notification alone proves no completeness.

## Make decisions inspectable and revisit them deliberately

**Action/context:** For a consequential choice, record the problem, constraints, feasible alternatives, chosen option, evidence, consequences, owner/status, and revisit trigger. Add a context, container, dynamic, or deployment diagram only when it answers a reviewer question.

**Evidence/rationale:** F chapters 21-23 pp641-714 and 27 pp801-816; H chapter 1 pp19-42 and chapter 15 pp417-434. [Official C4 diagrams guidance](https://c4model.com/diagrams) identifies context, containers, components, and **code**, and explicitly permits using only useful levels (consulted 2026-10-17).

**Exceptions/costs:** A small reversible choice may require only a review comment. Avoid permanent bureaucracy, unmeasured style ratings, and retroactively invented rationales. Existing decisions are evidence about prior context, not authority to ignore changed requirements.

**Validation:** Can a reviewer identify what would falsify the decision and what must be checked before release? Keep requirements separate from chosen mechanisms. ISO/IEC/IEEE 29148:2018's public [abstract and status page](https://www.iso.org/standard/72089.html) was consulted, not its paid normative text; this skill makes no claim of compliance.
