# Verification limits — 2026-11-06

Inputs: commit-choice-inputs.json and E-COMMIT-CHOICE in evidence.json.

- Skill quick_validate.py: exit 0, skill valid (repeated after final skill edits).
- SDD validate.py --root . --structure-only: exit 0 after AC-04 traceability repair.
- SDD validate.py --root . --features sdd/features/scripts-task-closure --require-fresh:
  exit 0; predecessor undecided criteria are not approved by this command.
- git diff --check: exit 0.
- Active-guide search/assertion: no automation command remains in AGENTS, root
  README, workflow, evidence, project context or skills interchange guide.
- check-ox.py: exit 1. Log: .local/commit-choice-check-ox.log. Current policy edits
  differ from pinned project/README/skill/UI succession digests; toolchain feature
  observations referencing those documents are stale. This run also found the
  missing AC-04 oracle input binding; it was added afterwards. Global governance
  remains unvalidated: those historical registries/evidence were not rewritten to
  claim approval of the new inputs. The full checker was not repeated after this
  bounded binding correction; its other reported blockers remain applicable.

Omissions: no automation, Rust build/tests, scanners, X11/Wayland checks or actual
Git commits for this instruction-only change. This verifies the documentary
choice contract, not future agent execution. No application/scanner sources,
hooks or unrelated existing modifications were changed. Historical observations
retain their original inputs and results. Registry succession and re-observation
of affected toolchain criteria remain necessary for a global governance pass.
