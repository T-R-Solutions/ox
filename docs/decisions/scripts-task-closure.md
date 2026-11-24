# ADR — Local task closure checks

Adopted by the maintainer's explicit 2026-11-05 request for local scripts integration.
This is governance work, not a product delivery or a permission grant.

D-01: retire the unused imported multistack library after complete local recovery
and hash preconditions; implement a fixed Python entry delegating to actual Cargo
and existing Ox validators. No foreign thresholds, scanners or installation.
D-02: explicit governance/rust/full selection, offline checks, raw separate logs,
real exit codes and required-tool failures. Tests/builds do not approve a product.
D-03: closure evidence lives in the task/feature and follows the evidence rules
(then `ea3cf0f:sdd/evidence.md`; now [workflow](../../sdd/workflow.md#evidência-e-retomada));
missing mandatory observations prevent acceptance; graphical targets remain separate.
D-04: authenticate exact authority successors using a bounded registry and preserved
preimages. Archive observations affected by changed inputs, mark dependent criteria
INCONCLUSIVE and preserve unrelated operational observations. This does not approve
or reject previous product behavior on new inputs.
D-05: independent-copy consumers demonstrate that the new authority links and
feature traceability require the two local script files in governance copies.
Explicitly add only scripts/automate.py and scripts/README.md to ROOT_FILES;
retain the directory allowlist and exclude local recovery/logs and application.
This is a reviewed boundary adjustment, not automatic inclusion of imported scripts,
profile/catalog change or authorization to generate/publish a distribution package.
Governance selection works in this copy; Rust/full requires the complete checkout.

Alternatives and risks: `ea3cf0f:sdd/features/scripts-task-closure/plan.md` (Git history).
Revisit on new stacks, operational consumers, toolchain changes or package qualification.

## Preference successor — 2026-11-06

Explicit maintainer instruction supersedes the automatic task-closure invocation
policy (D-02/D-03) and its duplicated operational guidance. Keep the technical
capabilities and historical observations. The commit skill alone owns the
optional pre-commit question and failure gate. Declining execution permits the
authorized commit workflow without claiming validation. General evidence and
product acceptance requirements remain independent.

Alternative rejected: retaining automatic closure execution in other authorities,
which would defeat the requested choice. No hook or application UI is added.
Review when the maintainer changes the commit preference or the automation result
contract. Previous acceptance is historical on its recorded inputs.
