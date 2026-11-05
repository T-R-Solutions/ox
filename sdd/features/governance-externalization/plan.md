# Plan — full workflow

Contracts and recovery change; the local route is insufficient. No Git was present.
Previous full baseline: /tmp/ox-before-externalization-zj4erab3/before.tar.gz;
inputs.json identifies observed bytes. Restore only into an empty directory and
compare, never overwrite subsequent work. The temporary external backup is not
a package dependency. Local feature history: previous-features.tar.gz.

| ID | Requirements | Decision / risk | Alternative and trigger |
|---|---|---|---|
| D-01 | REQ-01, REQ-04 | Incrementally replace readers; remove studies and old authoring tools; package with explicit manifest | Keeping dependencies or renaming studies violates the request; revisit if the scanner finds content |
| D-02 | REQ-02 | Local POL/GOV IDs, individual mapping of 72 IDs historical only; versioned profile | Copying all research duplicates authority; revisit on profile/policy changes |
| D-03 | REQ-03 | Separate immutable history; new observation after testing or explicit invalidation | Updating old hashes falsifies execution; review every affected input |
| D-04 | REQ-04 | Local ZIP, temporary extraction outside the source, five commands and mutations | Permissive copying of all Markdown would hide dependency |
| R-01 | REQ-01 | Content hidden in an archive or old script | Recursive inspection by name, hash and line sequence |
| R-02 | REQ-02 | Weakened checker or coverage of nonexistent IDs | Inventory, ID, path and link mutations; SDD preserved byte for byte |
| R-03 | REQ-03 | Stale evidence presented as current | Immutable snapshots, new states, contract/implementation/oracle inputs |
| R-04 | REQ-04 | Extraction uses parent directory, symlink or undistributed file | Processes run inside extraction, access audit and manifest |

| Capability | Bridge/version | Consulted entry | Role, question and deliverable |
|---|---|---|---|
| software-evolution | sdd/chain/software-evolution.md / 1 | .codex/skills/software-evolution/SKILL.md | Primary: how to remove dependencies without falsifying history? Migration, cutover order and recovery |
| software-testing | sdd/chain/software-testing.md / 1 | .codex/skills/software-testing/SKILL.md | Supporting: how to demonstrate independence and sensitivity to faults? Adversarial cases and smoke test |

Both were selected, identity-confirmed, consulted and used. The primary skill's
transition/migration references were read. No delegation or external agent.

Compatibility: old configuration retains its historical records, but its authoring
tools/validators are unsupported in the new revision. The new consumer uses only
the local tree. There is no concurrent runtime, database, service or deployment.
The rollback point is the full external backup; do not mix evidence across revisions.

Affected files: README, context/constitution/ADRs, profile/coverage fixtures,
check-ox, tests, runner, packaging and feature evidence. Technical skill entries,
bridges and the SDD core are preserved. Current tests must detect defects
characterized before cutover; failures from every round will be retained.
