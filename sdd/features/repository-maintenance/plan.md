# Plan: repository maintenance

Authorities: spec, maintainer request, constitution, workflow and evidence contract.
Read governance-layout, scripts-task-closure and scripts-shell-refactor ADRs.

## Decisions and risks

- D-01 / R-01 / REQ-01: Preserve historical duplicates and portable skill copies;
  remove the empty detached-toolchain placeholder. Same-sized logs were
  compared and differ in elapsed measurements, so both remain. Names/age are not sufficient; preserve inconclusive material.
- D-02 / R-02 / REQ-02: Workflow owns closure; shared skill catalog/integration and
  task templates link to it. Avoid 31 copies of a product policy. Structural review
  cannot establish prose correctness.
- D-03 / R-03 / REQ-03: Keep checks/security/cargo-home stable for existing consumers;
  centralize paths in one shell resolver. Group unreferenced loose historical logs
  under records/legacy; preserve build/recovery and legacy interventions whose
  embedded paths or evidence consumers prevent safe relocation.
- D-04 / R-04 / REQ-04: Retain by lifecycle, not guessed age or quota. Owned runs
  remain pinned until explicit release after evidence promotion/review. Clean released
  inactive runs on explicit apply. Per-run leases and a collector lock coordinate
  cooperative writers; reject symlinks and special files. Rename into trash before
  deleting; resume trash on next apply. Keep latest and preceding cleanup receipt,
  enough to diagnose interrupted/current versus previous operation without unbounded logs.
- D-05 / R-05 / REQ-05: Record exact authority successors with authenticated preimages;
  preserve historical inputs. Run governance and relevant script regressions; no Rust
  behavior changed, so do not claim new product acceptance or run full scanners by default.

## Selected methods

Primary software-design: path responsibility and producer compatibility.
Supporting workspace-integrity-engineering: path boundaries, leases, preconditions
and recoverable migration. Entries consulted and methods applied to D-03/D-04.
- `.codex/skills/software-design/SKILL.md` SHA-256 `4e214fd5dbf141ee437814a5c817b6924a05e8ad75cf6bc208281155204f6143`; bridge `sdd/chain/software-design.md`, bridge_version 1.
- `.codex/skills/workspace-integrity-engineering/SKILL.md` SHA-256 `3156e92baceb75376182423952607da665ff2c8db0d8cdc4296b44431b5c915a`; bridge `sdd/chain/workspace-integrity-engineering.md`, bridge_version 1.

## Selected acceptance method

The CLI --features argument takes a parent directory of features, not one feature.
Do not relocate this feature or require global approval of intentionally unverified
product criteria. docs/validation/repository-maintenance-20261109/acceptance.py calls
the existing evidence_errors, trace_errors and input_errors(require_fresh=True), then
checks every declared applicable criterion is APPROVED. Global structure and main
governance checks remain separate. This is a read-only validation harness, not a new
validator contract or production CLI.

## Retention successor — 2026-11-11

Explicit request replaces D-03/D-04: `.local` stores only logs, two calendar dates,
oldest removed before a third is created; no retained-copy prerequisite or backup.
Temporary scanner inputs are working inputs, deleted at completion. JSON reports
are diagnostic logs. Serialize publication/pruning on the logs directory inode.
Primary consulted method: `.codex/skills/software-delivery/SKILL.md` (unversioned
entry, bridge `sdd/chain/software-delivery.md` v1), including build-inputs-and-trust:
identify cache/dataset consumers, preserve failure codes, test retention and cleanup.
Historical acceptance is not evidence for this changed contract.
