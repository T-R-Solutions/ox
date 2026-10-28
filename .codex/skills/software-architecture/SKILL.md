---
name: software-architecture
description: Choose or review system boundaries, ownership, integration styles, and quality-attribute trade-offs. Use for structural decisions and migrations that change them; local interfaces belong to code design, and coexistence or cutover without an unresolved structural choice does not alone require architecture work.
---

# Software Architecture

Choose and validate the smallest structure that satisfies the actual problem. Treat architectural style as a consequence of constraints and evidence.

## Scope and required evidence

Read the relevant requirements, acceptance criteria, existing decisions, code and deployment boundaries, data ownership, contracts, operational incidents, workload evidence, and team constraints. Distinguish observed behavior from diagrams, estimates, and assumptions. Preserve existing decisions unless new evidence warrants changing them.

This skill owns structural choices and their consequences. Local interfaces and implementation complexity belong to software design; business meaning and invariants belong to domain modeling; failure/consistency guarantees across nodes belong to distributed systems. Bring in those skills only for a specific unresolved question. Security and accessibility remain baseline obligations.

## Workflow

1. **Frame the problem independently of a solution.** State the behavior needed, hard constraints, affected stakeholders, and consequences of failure. Reuse existing specifications. A small decision can fit in a paragraph.
2. **Make quality requirements observable.** Describe stimulus, environment, affected operation, expected response, and measurable acceptance condition. Identify workload, scope, measurement window, and who owns the threshold. Do not invent SLOs, legal requirements, or reliability guarantees.
3. **Map the current boundaries.** Identify modules, processes, deployments, data stores, trust boundaries, synchronous paths, asynchronous paths, and shared resources. Logical ownership, deployability, and runtime fault isolation are different properties.
4. **Compare viable options.** Include retaining or simplifying the existing structure. Evaluate required capabilities, failure propagation, data consistency, change coordination, migration, operation, cost, and reversibility. Eliminate options that violate hard requirements before comparing preferences. Use [architecture decisions](references/architecture-decisions.md) for specific decision criteria.
5. **Resolve the most consequential uncertainty.** Inspect real dependencies, run a bounded prototype or representative measurement, or ask the appropriate owner about a material requirement. A weighted matrix is a reasoning aid; counting favorable cells does not select an architecture.
6. **Implement incrementally where feasible.** Choose an observable slice; define compatibility, transition ownership, rollback/roll-forward, reconciliation, and removal of temporary bridges. Do not call an irreversible data change reversible because code can be redeployed.
7. **Verify the decision.** Trace important requirements to checks. Test critical paths, interfaces, migration, and relevant failures using the available environment. Verify resource and dependency assumptions. Record checks that could not run and their impact.
8. **Record the result proportionally.** For consequential decisions, capture context, options, selected approach, evidence, consequences, status, and revisit trigger. Do not create a formal ADR for every implementation detail.

## Essential constraints

- Do not infer independent scalability, deployment, security, or fault isolation from a service label. Verify the actual topology and shared bottlenecks.
- Do not split business invariants across transactions merely to achieve smaller services or database ownership purity.
- A queue shifts temporal coupling and creates retention, capacity, ordering, and recovery responsibilities; it does not remove dependencies.
- Prefer stable semantic contracts over shared storage details. JSON, gRPC, GraphQL, and events all permit coupling and incompatible changes.
- Treat style scorecards, metric thresholds, example service sizes, and historical performance figures as hypotheses, never acceptance evidence.
- Diagrams must distinguish actors, boundaries, relationships, direction, and abstraction level. Use only useful views; do not mandate all C4 or UML levels.
- Verify current official documentation for every recommendation that depends on a product version, runtime, protocol, or deployment setting.

## Completion and presentation

Report the requirement and resulting behavior first, then the selected structure, meaningful alternatives, trade-offs, implementation/migration steps, validation results, and unresolved risks. Separate specification, technical decision, implementation, and validation. Attach a small diagram or decision record when it makes the result easier to review.

For an important recommendation, include its context, evidence, rationale, exception, cost, and validation method. A successful build proves neither architectural quality nor operational readiness.

## Additional investigation references

When an architectural decision needs repeatable drift detection or automated
governance, read [fitness functions](references/fitness-functions.md), including
known-violation checks, ownership and exception costs.

Other named skills are optional specialist suggestions. Use them only when available and needed for a specific unresolved question; their absence does not prevent using this skill. Report any expertise or verification gap without claiming a handoff occurred.

## Adjacent responsibilities

Database-engineering can resolve persistence enforcement; software-evolution can resolve an incremental transition. Keep structural selection here and load either only for a concrete unresolved question.
These are optional available capabilities, not dependencies of this folder.
