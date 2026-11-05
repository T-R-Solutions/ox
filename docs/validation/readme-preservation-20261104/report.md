# README preservation repair — 2026-11-04

The maintainer requested repair of the inherited exact-byte README integration
failure. Full route in the existing readme-skill-integration feature covers the
preservation consumer change, with scoped spec/plan/tasks and independent-copy
verification. Primary method: software-design (actual entry read, no declared
version); its contribution is the single-file normalization seam. No delegation.

## Changes and evidence boundaries

The original readme-skill-integration-001 files/profile registrations are unchanged.
A separate exact README successor maps the current README to the original
integration preimage, authenticated against that registration. Existing documentary
intermediate versions remain in their prior reports. The predecessor chain then
continues through the original integration and older preservation layers.

Unknown current bytes, rollback to the old integration README, corrupt/missing
preimages, duplicate properties/records, unexpected scope/version/decision, escapes
and symlink components are rejected. No broad Markdown exception is introduced.
Application sources, Cargo manifests, lockfile, toolchain and operational F0 evidence
are unchanged. No GUI, usability, public distribution or product acceptance claim.

## Criterion / method / inputs / result / limitations

| Criterion | Method and observed inputs | Result and limit |
| --- | --- | --- |
| AC-03 exact history and rejection | Run readme integration tests, including current corruption/deletion, exact predecessor, invalid registries, symlinks and downgrade | Results in checks.json and raw logs; passing tests approve only these bounded preservation scenarios |
| AC-03 independent copy and recovery | Existing distribution test, maintenance verification and complete governance suite | Results in checks.json; export is governance-only and not product distribution |
| AC-04 current claims and navigation | Inspect README, 31-entry catalog/profile/bridge routing, accepted local F0 report and linked application guide; run check-ox and SDD freshness | Current README separates controlled fixture from real agents, in-memory history from persistence, and governance package from product; no new operational claims |
| Unrelated input preservation | Compare before hashes with current application/authority/registry inputs in protected-inputs.json | Comparison in checks.json; source equality does not itself prove runtime correctness |

Exact commands, exit codes and raw logs are retained in checks.json and *.log.
Inputs are identified in inputs.json; immediate pre-edit bytes are under before/.
Evidence records affected by changed documents/consumer code retain their original
hashes, resolving to saved preimages. New inspections bind the current contract
and explicit test observations instead of renewing old results.

Historical failure reports are unchanged. The active governance guide now links
this correction; old reports continue to describe their own failed observations.
Maintenance trigger: README bytes, successor scope or preservation consumer changes.
Owner: contributor and Ox maintainer. No commit, publication, installation or
application modification was performed. Test results describe the local filesystem
and Python environment, not authenticity of arbitrary future registries.
