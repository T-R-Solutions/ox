# Ox consumer migration to Docker toolbox

Maintainer request: toolbox prepares/version-controls and executes Trivy, OSV and
Grype; Ox supplies targets/configuration and snapshot/age policy. Only Ox changed.

Trivy 0.76.2, OSV 2.7.0 and Grype 0.119.0 now require toolbox execution. Native
overrides are rejected. Ox pins real imported external image/snapshot records;
policies are 120h, 24h and 120h respectively. Independent result parsing handles
Trivy/Grype exit 0 with findings and rejects substituted database identity.
The local preparation command now handles RustSec only, retaining reviewed import
and corruption denial. No download, Docker build/run/update or dev_audit write.

Observed acceptance:

- AC-05 APPROVED: tests.log records 30 tests, 25 passed and 5 real Docker probes
  skipped. Simulated subprocesses verify dispatch, policy forwarding, no local
  dataset requirement, native refusal, missing policies and identity disagreement.
  toolbox-validation.json records successful read-only validation by the actual
  installed toolbox. This does not establish real scanner coverage.
- AC-06 APPROVED: cleanup.json records 8 generated database directories removed
  under flock and verifies preservation of 1469 RustSec files and 78 adjacent
  report files by SHA256. cleanup-import.json records one additional redundant
  Grype import directory removed. The active dataset registry retains RustSec
  only. Historical receipts/reports remain; deleted generated databases cannot
  be replayed locally without explicit reacquisition from their recorded sources.
- AC-07 UNVERIFIED: no Docker execution; dev_audit is controlled by another agent.
  Real clean/findings/invalid-input tests are opt-in, including added Trivy cases.

Bash syntax checks passed. Focused SDD trace/evidence/freshness checks for both
affected features passed (sdd-validation.log); historical observations with changed
inputs were preserved without renewed hashes. contract-inputs.json records
read-only external contract identities and copied image/snapshot provenance.

Runtime requires toolbox on PATH or OX_TOOLBOX_BIN pointing to the installation's
bin/toolbox. After the Docker owner confirms preparation, execute the opt-in real
adapter suite in a jointly authorized environment; snapshots/locks must match the
actual prepared version. This report makes no claim that images or data remain
available/fresh, nor any product, license or security-audit acceptance.
