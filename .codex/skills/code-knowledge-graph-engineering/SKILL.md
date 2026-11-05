---
name: code-knowledge-graph-engineering
description: Design typed code knowledge graphs with evidence-backed edges, incremental invalidation and bounded impact queries. Use for code relationship semantics; skip static diagrams and embedding similarity presented as resolved calls.
---

# code-knowledge-graph-engineering

## Responsibility and selection

Model and query graphs of symbols, calls, files, tests, rules and tasks, distinguishing verified relationships from hypotheses and avoiding displays of stale data.

Select: Node/edge schema, provenance, impact analysis, paths, clusters and subgraph/density visualization.

Do not select: Do not select for a marketing graph or static presentation; use design-system/design-review. Do not replace a compiler/LSP with embeddings.

## Inputs and gaps

stable identities, extracted/inferred relationships, snapshots, impact queries, cardinality and layout limits.

Inspect actual contracts and resources before execution. A missing version requires consulting the corresponding documentation; a missing permission prevents the dependent effect. Record the gap, its impact and how to resolve it while continuing independent work. Examples in this package are evaluation contracts, not APIs or policies imposed on all consumers.

## Operating procedure

1. Define node identity, edge type, direction, cardinality and evidence requirements before choosing a graph store. Separate structural relations, semantic resolution and inference with incompatible labels when appropriate.

2. Attach snapshot, source range, extraction method/version and originating evidence to every edge. A numeric similarity score cannot upgrade an inferred edge to verified. Validate endpoint existence in the same generation.

3. Publish incremental updates coherently: remove or invalidate edges dependent on changed/deleted evidence, then add replacements. Retain historical generations for traceability without exposing them as current.

4. Define query semantics and bounds: permitted edge classes, direction, depth, node/edge limits, timeout, cancellation and truncation metadata. Traverse with visited sets to handle cycles and deduplicate stable identities.

5. Keep logical graph data separate from layout. Structural and dense exploratory views should project the same snapshot with different filters; cluster membership/layout position is not a new factual edge. Pause expensive layout when hidden.

6. Test known calls, mislabeled inferences, deleted sources and a deterministic dense cyclic graph. Check provenance, orphan handling and explicit truncation. Deliver schema, bounded queries, before/after fixtures and UI-performance gaps separately.

## Deliverables and acceptance

versioned graph contract, bounded queries, edge traceability, invalidation policies, structural/dense modes.

Bind each conclusion to observed inputs, method, result and limitations. Run the normal, boundary and failure cases from the [evaluations](references/evaluation-cases.md) in the authorized environment; distinguish review, simulation and integration results. Written cases remain unexecuted until run. Skill text neither proves effectiveness nor grants authority.

## Boundaries and handoff

`code-context-engineering` — Can the edge's origin be verified in the indexed code snapshot?

Hand off only the distinct unresolved technical question, including scope, criterion IDs, facts, gaps and required evidence. Confirm availability before consultation. A mention does not install, delegate, execute or recursively load other skills. The consumer's contract owns behavior; the skill provides the method.

## Specialized references

- [graph-schema-and-evidence](references/graph-schema-and-evidence.md): consult for Evidence-bearing graph schema.
- [incremental-graph-updates](references/incremental-graph-updates.md): consult for Remove stale relationships deliberately.
- [graph-queries-and-visualization](references/graph-queries-and-visualization.md): consult for Bounded traversal and honest views.

Official sources accessed on 2026-10-26 are cited alongside claims. A consulted version is not a version adopted by the consumer. Operational summaries and example schemas are methodological decisions of this skill, without a promise of implementation or future compatibility.

## Adjacent responsibilities

The specialized capability above does not replace the general methods below. Consult them only when the corresponding question remains unresolved; no handoff is mandatory.

| Capability | Adjacent technical authority |
|---|---|
| `ai-engineering` | models, RAG, agents using tools, diagnostics and outcome evaluation |
| `database-engineering` | persistence, schemas, transactional invariants and migrations |
| `design-system` | tokens, components, states and UI contracts |
| `domain-modeling` | domain rules, invariants, task/agent/policy concepts |
| `performance-engineering` | benchmarks, profiling, reproducible comparisons and regressions |
| `software-architecture` | boundaries, integration, quality attributes, ADRs |
| `software-design` | interfaces, cohesion, coupling, local refactoring |
| `software-testing` | cases, oracles, automated tests, suites and regressions |
