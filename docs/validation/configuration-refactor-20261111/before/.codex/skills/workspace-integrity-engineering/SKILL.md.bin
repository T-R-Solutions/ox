---
name: workspace-integrity-engineering
description: Protect multiauthor workspaces through content preconditions, path boundaries, conflict detection and crash recovery. Use for concurrent file edits, watchers and Git worktrees; skip ordinary schema migrations.
---

# workspace-integrity-engineering

## Responsibility and selection

Ensure the integrity of project files modified by concurrent processes, editors and agents, using snapshots, worktrees, conflict detection and recovery.

Select: Concurrent editing, watchers, write atomicity, Git/worktrees, rollback, paths and symbolic links.

Do not select: Do not activate to add a SQLite column or review UI formatting; use database-engineering/design-system. Do not reimplement Git merely for convenience.

## Inputs and gaps

workspace tree, exclusion policy, authorized roots, edit plan, Git state, OS events.

Inspect actual contracts and resources before execution. A missing version requires consulting the corresponding documentation; a missing permission prevents the dependent effect. Record the gap, its impact and how to resolve it while continuing independent work. Examples in this package are evaluation contracts, not APIs or policies imposed on all consumers.

## Operating procedure

1. Inventory authorized roots, existing dirty and untracked files, symlinks, external writers, filesystem and Git availability. Capture a recoverable content baseline for the intended write set; Git status alone does not preserve unstaged or untracked bytes.

2. Bind each proposed edit to an observed base hash and destination identity. Compare immediately before commit; a mismatched base becomes a conflict, never a blind overwrite. A merge requires independent verification and retention of both inputs.

3. Constrain path resolution and the actual operation. Reject traversal and escaping symlinks; consider case normalization, mount boundaries and races. Canonicalizing once before opening is not a complete defense against TOCTOU. Use suitable platform primitives or explicitly narrow the threat model.

4. Prepare staging, a journal and recovery points. Distinguish atomic replacement of one path from durability and from a multi-file transaction. Record which writes are committed, uncertain or still staged when a crash interrupts the sequence.

5. Treat watcher events as hints. Reconcile from file contents after overflow, rename bursts or restart; invalidate snapshots of changed files and downstream indices. If worktrees are used, inspect shared repository metadata and serialize conflicting Git operations.

6. Exercise path escape, two writers from one base, failure before/after replacement and external mutation with missed watcher events. Deliver a conflict policy, restoration procedure and observed platform limits; never restore a baseline over newer unrelated work.

## Deliverables and acceptance

validated file transactions, loss prevention, change trails, snapshot and recovery strategy.

Bind each conclusion to observed inputs, method, result and limitations. Run the normal, boundary and failure cases from the [evaluations](references/evaluation-cases.md) in the authorized environment; distinguish review, simulation and integration results. Written cases remain unexecuted until run. Skill text neither proves effectiveness nor grants authority.

## Boundaries and handoff

`application-security` — Are there alternative paths/symlinks that escape the root granted to the agent?

Hand off only the distinct unresolved technical question, including scope, criterion IDs, facts, gaps and required evidence. Confirm availability before consultation. A mention does not install, delegate, execute or recursively load other skills. The consumer's contract owns behavior; the skill provides the method.

## Specialized references

- [file-operations](references/file-operations.md): consult for Safe write boundaries.
- [git-worktrees-and-conflicts](references/git-worktrees-and-conflicts.md): consult for Git is context, not a backup of all bytes.
- [watcher-and-recovery](references/watcher-and-recovery.md): consult for Reconcile after lost events.

Official sources accessed on 2026-10-26 are cited alongside claims. A consulted version is not a version adopted by the consumer. Operational summaries and example schemas are methodological decisions of this skill, without a promise of implementation or future compatibility.

## Adjacent responsibilities

The specialized capability above does not replace the general methods below. Consult them only when the corresponding question remains unresolved; no handoff is mandatory.

| Capability | Adjacent technical authority |
|---|---|
| `application-security` | trust boundaries, secrets, authorization and threats |
| `reliability-engineering` | failures, cancellation, limits, degradation, recovery |
| `software-evolution` | compatibility, migrations, coexistence and older versions |
| `database-engineering` | persistence, schemas, transactional invariants and migrations |
| `rust` | ownership, crates, concurrency, compatibility, Rust validation |
| `software-architecture` | boundaries, integration, quality attributes, ADRs |
| `software-design` | interfaces, cohesion, coupling, local refactoring |
| `software-testing` | cases, oracles, automated tests, suites and regressions |
