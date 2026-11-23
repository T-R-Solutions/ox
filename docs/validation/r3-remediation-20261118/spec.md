# Part 3 remediation — 2026-11-18

Authorized request: repair R3-1, R3-2 and R3-3 of claude_analysis.md Part 3,
record every R3-4 disposition, and execute all supported verification suites and
entries without errors before completion. No commits, publication, central
Toolbox maintenance or implicit downloads. Existing unrelated edits are preserved.

## Requirements and acceptance

- REQ-01: Governance fixtures and supported entry points agree with current contracts.
- REQ-02: Distribution remains self-contained, including the append-only task log.
- REQ-03: Routine document updates do not require code hash pin changes; protected contracts and historical evidence remain verified.
- REQ-04: Every mandatory verification is executed on identified final inputs and passes.
- AC-01 → REQ-01: The complete governance suite passes, with failures from the baseline accounted for.
- AC-02 → REQ-02: Both named distribution regressions pass and an independent package extraction verifies.
- AC-03 → REQ-03: Baseline and legitimate project/log append pass; protected-contract mutation, corrupt history, downgrade, unsafe paths and conflicting copy contexts reject.
- AC-04 → REQ-04: Full matrix, opt-ins/native tests and affected feature gates pass; missing prerequisites or mandatory observations block completion.

This is material governance work under sdd/workflow.md. Review and validation
require contexts independent of implementation. Historic analysis and observations
are retained, never silently relabeled as current acceptance.
