# Skill methods and bounded preservation verification — 2026-11-17

Implementation scope: three existing skill entries and three existing progressive
references; consumer product policy stays in DESIGN.md. No profile, metadata,
bridge identity, toolkit or product code changed by this subtask. The host-approved
`python3 /tmp/ox-windows-skills-edit.py` was executed by root after the initial
approval wait was interrupted. Root reported exit 0; this writer subsequently
inspected the resulting bytes and bound them in succession.json.

## Observed inputs and checks

The eight-path registry records exact current/predecessor SHA-256 and reversible
byte edits for six skill files, AGENTS.md and sdd/project.md. Predecessors were
captured from the dirty checkout before this task, not inferred from HEAD. No
historical registry/digest was edited and no predecessor backup was added to the
repository. governance-inputs.json binds final authored code/tests/registry.

Executed from repository root with PYTHONDONTWRITEBYTECODE=1:

| Method / command | Observed result | Limit |
| --- | --- | --- |
| `python3 /home/rodrigo/.codex/skills/.system/skill-creator/scripts/quick_validate.py .codex/skills/design-system` | exit 0, Skill is valid | Metadata/scaffold check only |
| Same quick_validate for `design-review` | exit 0, Skill is valid | No usability claim |
| Same quick_validate for `iced-engineering` | exit 0, Skill is valid | No native execution |
| `python3 -m unittest discover -s tools/governance/tests -p test_windows_design_revision.py -v` | exit 0, 5 tests | Exact reconstruction; all eight live mutations/deletions/symlinks/downgrades; missing/tampered registry; authenticated invalid scope/schema/ranges; duplicate keys/parent symlink |
| `python3 -m unittest discover -s tools/governance/tests -p 'test_*visual*revision.py' -v` | exit 0, 7 tests | Existing preservation behavior after new normalization |
| `python3 -m unittest discover -s tools/governance/tests -p test_instruction_copy.py -v` | exit 1, 5 pass and 1 fail | Required preexisting project terminal mismatch, below |
| `python3 -m unittest discover -s tools/governance/tests -p test_osv_acquisition_revision.py -v` | exit 1, 5 pass and 1 error | Required preexisting project terminal mismatch; no missing-registry error after fixture correction |

## Preserved preexisting project mismatch

The observed original `/tmp/ox-windows-before/project.md` hashes to
`97f5a391e32e49cf6bfa5c1b28622cb27c8ab10a3b7119520347646e2ac8cb28`.
It already contains enterprise-desktop/navigation/project-entry scope additions.
The immutable OSV successor requires terminal
`7ecff339f506d569c0210a1aa5f060f970fb1c051c9bb38a934dd385093a5de8`.
The new Windows successor reconstructs exactly the observed original, so older
strict checks continue to reject that earlier mismatch. The initial fixture run
also revealed a missing new registry in the isolated OSV fixture; fixture_paths
was corrected to include the closed registry/input inventory and rerun. The
remaining failure is the digest mismatch, not fixture absence.

This task does not approve those prior edits by normalizing them to the older
OSV terminal. The rejection behavior remains active. A separate authorized
reconciliation can examine those earlier changes and their evidence.

## Documentary disposition

Reviewed existing six skill methods, AGENTS/project scope, three preservation
callers and isolated fixture consumers. Skill methods now distinguish source
lineage, product adoption, toolkit support and observed rendering/behavior;
Windows/Fluent guidance is conditional, with role mapping, density, state,
material fallback and native accessibility limits. Existing identities and
references remain discoverable. Added focused tests exercise boundary rejection
rather than require specific prose. Product rendering, AT support and UX outcomes
remain unverified by this instruction-authoring subtask.

## Final root governance observation

`PYTHONDONTWRITEBYTECODE=1 python3 tools/governance/scripts/check-ox.py`
ran once after freeze and exited 1. Full unmodified output: check-ox.log.
The output retains preexisting project and product-visual-workbench current-digest
failures and snapshot-relative links. It also correctly reports stale inputs in
prior visual-skill-refinement evidence because this task changed bound methods
and preservation code. No old evidence hash was refreshed to imply reexecution.
The coordinator must record that affected feature disposition separately; this
subtask does not own its evidence. The global gate is not claimed as passing.
