# Historical links and terminal diagnostic repair — 2026-11-15

## Authorization and ownership

The maintainer's new instruction **“implemente”** authorizes local implementation
of the [reviewed plan](../governance-link-repair-plan-20261115/plan.md), focused
verification, documentation and independent review/validation. Its planning-only
record remains historical and unchanged. No complete pipeline, download, central
maintenance, commit or publication is included.

High coordination applies because origin authentication affects an integrity gate.
The coordinator owns this directory's common documents/registries, ADR and feature
artifacts. Governance and terminal implementers own disjoint assigned code/test
paths and their own evidence subdirectories; neither subdelegates. Review and
validation use contexts independent of implementation. Existing dirty/untracked
work is preserved. No extra-high effort is selected.

## T001 — observed baseline, provenance and presence

All 45 planning input hashes still match. `inputs-before.json` identifies exact
preimages captured as `.bin` before editing; no displaced Markdown copies are
created. `presence-and-links.json` records current distribution membership and
resolved links for the five historical snapshots. Both source snapshots and their
two original paths are included by the current distribution; all 22 local references
exist when resolved from those origins. No excluded-target expansion is needed.
T001 closes this compatibility decision before implementation. Actual independent
copy execution is a subsequent test, not inferred from this inspection.

Provenance was reviewed from the existing retained documents and their surrounding
capture records, not inferred only from filenames. The three convergence copies
identify themselves as Terminal progress convergence, contain the same six criteria,
and link to their owning envelope. Their wording/style states correspond to the
wording and pre-final-style observations in terminal-style/history-correction reports.
They resolve from `sdd/features/terminal-progress/converge.md`; no claim is made that
their current target envelope preserves its historical contents. The two README
copies describe the scripts CLI and its relative documentation links, matching the
documentary changes recorded in those reports. Their SHA-256 values are bound as
`scripts/README.md` inputs in retained terminal evidence: `a3d7dcd...` in
terminal-style/before/terminal-evidence.json, and `47e8177e...` in
history-correction/coordinator/terminal-evidence-before.json. The new registry
contains the complete hashes and exact reviewed paths. These observations support
origin attribution, not a renewed historical acceptance.

`origins.json` is additive, bounded to these five pairs and linked to the unchanged
prior registry. The adopted [ADR](../../decisions/governance-historical-links.md)
records decisions and alternatives. No future snapshot gains an exception implicitly.

## Methods and criteria

Primary autonomous-verification-engineering and supporting tool-output-engineering
were actually consulted through version-1 bridges during planning and are applied
to current evidence/negative gates and conservative stream projection. Paths and
editorial hashes are in the planning inventory. Their contributions remain those
recorded in the plan; skills do not authorize execution. GL-01–07 map to the full
configuration-cohesion and terminal-progress criteria; current results will be
recorded after observed verification, with previous envelopes retained as preimages.

## Execution and documentation disposition

Project authorization is recorded here and in the affected feature successors;
`sdd/project.md` remains unchanged because this repair adds no product phase,
architecture or operational permission policy. The feature is the authorized scope
record. Configuration-cohesion adds REQ-16/AC-16/D-15/R-15/T019; the complete prior
15 criteria remain UNVERIFIED as observed before this task. Terminal-progress
retains all six criteria with explicit diagnostic/publication cases and T012.

The first public check (`check-ox-integration-01.txt`, exit 1) no longer reported
any of the 22 broken historical links. It exposed a new prose line beginning with
an AC token, corrected to ordinary prose, and an existing history-scanner-correction
AC-03 evidence binding to the now-changed progress.sh. That prior envelope and
projection were preserved as .bin; only the wording observation was invalidated.
Its two native scanner criteria remain UNVERIFIED and untouched. This is an
affected consumer of the terminal change, not authorization to execute history scans.

The shell-only production contract in `docs/decisions/scripts-shell-refactor.md`
was also reviewed. An initially proposed Python projection helper conflicted with
its D-01. That attempt was discarded, retained only as explicitly rejected .bin
inputs under terminal/rejected-python-attempt, and replaced with Bash/jq in the
existing renderer. Tests from the discarded attempt do not support acceptance.
No Python production implementation or policy change is introduced under scripts.

`scripts/README.md` now describes actual-stream selection, bounded safe metadata
and confirmed retained references. It and the four changed configuration-cohesion
contract files are bound by `successors.json` to their exact preimages. The previous
authenticated registry is unchanged. README.md, AGENTS.md, sdd/project.md,
docs/development/governance.md and docs/development/local-artifacts.md were reviewed:
their entry commands, authorities, distribution boundary and two-date retention
remain accurate, so no successor to those documents is needed. The ADR adds the
requirement to review future snapshot origin before acceptance; it grants no
automatic registry extension. Verification and independent dispositions follow.

## Rejected first succession guard and corrective iteration

Independent source review found one low-severity oracle gap: the original mutation
removed a raw line instead of removing a projected diagnostic. A new disposable
parser mutation keeps all 22 raw lines, drops one displayed group without changing
omission accounting, and is rejected by the independent displayed-plus-omitted
count oracle. Its focused test and current 14-test diagnostic suite passed; the
reviewer reexamined and closed that finding. Production terminal bytes did not change.

Independent acceptance validation then demonstrated a material flaw not caught by
the first source review: public isolated check-ox accepted an unregistered append
to the newly registered scripts/README.md successor. Baseline and mutated copies
both returned exit 0. Unknown data was passed to older comparison layers, but this
new destination had no effective older content comparison. GL-02/GL-07 were
therefore REJECTED for that candidate, not approved from the passing helper tests.
The captured probe and preliminary verdict are preserved under
`validation/rejected-succession/`; earlier production/test bytes are preserved
under `governance/before-current-guard/`.

The broad regression attempt was interrupted with exit 130 before changing the
candidate, and its partial output remains historical. It is not a completed
200-test observation. One export test reported ERROR while the recorder wrote a
live log within the exported inventory. Concurrent source mutation is the concrete
hypothesis, not a proven cause: interruption preceded the final traceback. The
frozen replay with capture outside the tree passed without changing export or its
test. Neither observation justifies relaxing export integrity.

## Final bounded result and remaining limits

The corrected guard directly authenticates all five live documentary successors.
Independent source reexamination found no remaining issue and rejected 20 controlled
mutations (changed content, downgrade, missing file and symlink for each terminal),
while preserving all five normalizations. Its observed helper hash is
`ddab78d019456d460f4f8fcb9fd9854ed813751ac550d337bcb44ef247dd7d66`.
Independent acceptance replay then observed public baseline **0**, the same README
mutation formerly accepted now **2** with a specific current-content diagnostic,
and restored baseline **0**. The rejected observation remains preserved separately.

Final observed checks, with commands/inputs/raw retained in the named subdirectories:

| Observation | Result | Record |
| --- | --- | --- |
| Current governance fixtures and succession consumers | 52 tests passed | `governance/current-guard-focused-01.*` |
| Current public registry/unknown-successor methods | 2 methods passed | `governance/current-guard-public/public-current-guard-01.*` |
| Frozen clean export and recovery | 1 test passed | `governance/current-guard-public/clean-export-replay-01.*` |
| Terminal diagnostic/mutant-parser suite | 14 tests passed | `terminal/governance-diagnostics-mutation-02.*` |
| Terminal/style/publication regressions | 28 tests passed | `terminal/terminal-regressions.*` |
| Capture/process/local lifecycle regressions | 13 tests passed | `terminal/lifecycle-regressions.*` |
| Bash syntax | exit 0 | `terminal/bash-syntax.*` |
| Independent final helper and public mutation | 15 helpers passed; public 0/2/0 | `validation/current/` |
| Final real wrapper, only Ox check selected | exit 0; stable inputs; three retained locators exist | `wrapper-final/` |

The final wrapper is the documented legacy selection
`./scripts/automate.sh --scope governance --check ox`, with explicit maintainer
Toolbox/SELinux/Cargo environment. Plan inspection selected only check-ox; no
scanner, governance-test suite or complete pipeline was invoked by this command.
Final run: `ox-run-r4KmsbJ2`, retained under `.local/logs/2026-11-15/` for the usual
two-date policy. Earlier direct/wrapper exit 0 belonged to the candidate before
the independent successor counterexample; they are not substituted for this final
guarded observation. The terminal failure/locator cases are controlled runner
fixtures, not newly introduced real checkout failures.

The final independent [verdict](validation/current/verdict.json) approves GL-01–06,
configuration-cohesion AC-16, all six terminal-progress criteria and the affected
history-scanner-correction wording AC-03. The older terminal regression receipts
were not rewritten: their only listed-input drift is the new diagnostic test file,
which those selected suites do not execute. Independent dependency review and the
new 14-test observation reconcile that change without renewing old hashes.

## Broad regression completion and current closure

The subsequent complete governance regression ran with source writers paused and
all output captured outside the repository before publication. Its exact command,
raw output, selection and manifests are retained in
[governance/broad-final/report.md](governance/broad-final/report.md).
The command exited **0**: **207 successful executions, 198 distinct test IDs**,
with nine README test executions duplicated by existing discovery, no omissions,
skips, failures or errors. The 19,006 before/after input files matched exactly.
Unittest reported 2026.666 seconds; this is an observed completed suite, separate
from the preserved earlier attempt interrupted with exit 130.

Independent [broad-completion validation](validation/broad-completion/verdict.json)
confronted discovery multiplicities, selected IDs, raw outcomes, receipt hashes and
stable source manifests. It approves **GL-07 only for the integration and verification
obligation of this repair**. GL-01–06 retain their earlier independent approvals.
The fifteen previous configuration criteria and two native history criteria remain
**UNVERIFIED**. Whole-feature approval still reports those seventeen pending criteria;
the broad governance corpus does not execute or accept native scanners, a complete
pipeline or the product. Their own missing observations/permissions remain necessary.

T001–T008 are delivered for the bounded correction, including the previously missing
broad regression and independent GL-07 confrontation. Earlier independent verdicts
remain immutable. This successor changes only current report/limitation/projection
text; their exact preimages are retained as .bin under `before-broad-completion/`.
Existing criterion evidence bindings and statuses are preserved. The final sensitive
SDD gates and documentary comparison are recorded with the new independent verdict;
no repeat of the 207 executions is required for these documentary-only successors.
No unrelated criteria, historical snapshots, old registries, catalogs or existing
scanner policy were modified to obtain this result. No commits, downloads or
publication were performed.
