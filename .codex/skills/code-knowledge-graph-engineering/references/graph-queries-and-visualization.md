# Bounded traversal and honest views

An impact query must name root, direction, edge classes, snapshot and maximum work. Keep visited nodes to terminate cycles; bound both nodes and edges because a small node set may still have many edges. Return a truncation flag, reason and continuation semantics when work is limited.

Use deterministic tie-breaking for repeatable tests. A corpus with a cycle, a high-degree hub and inferred links should produce a stable bounded result without hiding omitted neighbors. Depth zero and a missing root need explicit behavior.

Structural and dense views share graph identities and provenance; layout caches include snapshot and filter parameters. Selecting a node should resolve to its evidence, not a stale display index. A bounded query test does not establish responsive rendering: measure layout, input latency and cancellation on target hardware separately.
