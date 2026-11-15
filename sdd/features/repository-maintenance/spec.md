# Repository maintenance

## Context and authorization

Explicit maintainer request of 2026-11-09: diagnose the repository, then sequentially
remove proven redundant/obsolete content, integrate documentation closure, consolidate
local artifact lifecycle, and reconcile documentation. No product functionality,
commits, publication, external repository writes or global installation.
Historical evidence, unique data and pre-existing work must survive.

## Requirements and acceptance

- REQ-01: Classify duplicates and obsolete material using observed consumers and provenance; remove only proven disposable content.
- AC-01 → REQ-01: Inventory covers source, governance, documentation and local artifacts; removal receipts verify the empty obsolete directory and explain retained distinct observations.
- REQ-02: Task closure includes affected documentation or a concrete no-impact rationale, with one normative authority.
- AC-02 → REQ-02: Workflow, templates and shared skill integration agree; behavior-changing, documentation-only and no-impact examples satisfy the rule.
- REQ-03: Store only diagnostic logs under `.local/logs/YYYY-MM-DD/`; discard temporary scanner work at completion and keep operational caches outside `.local`.
- AC-03 → REQ-03: Producer fixtures preserve raw logs and failure reports, remove temporary work and use the documented layout.
- REQ-04: Retain at most two dates without backups or retained-copy prerequisites.
- AC-04 → REQ-04: Fixtures cover third-date eviction, same-day executions, dry-run, symlink refusal and clock rollback.
- REQ-05: Documentation and evidence reflect final implementation and actual verification.
- AC-05 → REQ-05: Focused script regression checks and inventory results are recorded; historical acceptance is not renewed without reexecution.

## Successor authorization — 2026-11-11

The maintainer explicitly replaces the prior backup-preserving lifecycle. Delete
local backup/experimental copies, retain only two dates of diagnostic logs, move
operational caches and original supplied design inputs outside `.local` without
copying them. Preserve unrelated source changes. No commit or publication.
