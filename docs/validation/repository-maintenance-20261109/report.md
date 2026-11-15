# Repository maintenance observations — 2026-11-09

## Initial diagnosis

Initial Git status was clean before this work. Read-only recursive source inventory:
16,666 files outside .git/.local/target/dist/__pycache__, 1,217 nonempty exact-hash
sets. The tracked nonhistorical inventory has only two duplicate sets: portable-sources
in application-security/reliability-engineering (independently portable imported
resources protected by copy provenance), and two historical structure reviews.
Neither is disposable. Most repeated bytes belong to immutable validation/preimage
corpora; retaining them is required for recovery and exact-input evidence.

The application has 16 Rust crates; no proven redundant product implementation was
found. Cargo duplicate generations already have explicit dependency-hygiene dispositions;
this maintenance does not reopen those compatibility decisions. Skill profile has 31
entries and 31 bridges; imported copies serve separate portable consumers.

`local-before.json` records per-child counts, apparent and allocated file bytes,
without content disclosure. .local/build accounts for 38,399,773,532 apparent bytes
and checks for 6,181,012,995. Build includes isolated dependency work and unique
recovery/intervention scripts, so space alone does not authorize disposal. Checks
contains 148 prior runs, without lifecycle ownership metadata: retain as legacy evidence.

| Class / path | Observation and impact | Action / verification |
| --- | --- | --- |
| Similar logs: .local/toolchain-unit.log and scanner-tests.log | Equal size but different elapsed measurements; byte comparison rejected deletion | Preserve both unique observations |
| Obsolete: .local/detached-toolchain | Empty placeholder; no toolchain files | rmdir only if still empty |
| Historical: docs/validation, docs/structure/revisions | Hash-bound evidence and recovery | Preserve; governance preservation checks |
| Fragmentation: loose .local logs | Generated prior intervention records | Consolidate into records/legacy with byte identities and mapping |
| Repeated path knowledge: scripts/lib/common.sh, files.sh, checks/run.sh, prepare-datasets.sh | checks/security paths defined in multiple producers/consumers | One shared resolver, regression checks |
| Missing lifecycle: checks/new_run | No ownership, lease, release or cleanup contract | Add metadata and explicit lifecycle retention; protected legacy defaults |
| Governance: workflow/templates/skill integration | Closure mentions evidence but lacks explicit per-task documentation disposition | Add shared normative closure and three examples |
| Inconclusive: .local/build, recovery, scanner interventions, security-tools | Embedded old paths, provenance or unique bytes | Pin in place; no speculative removal |

## Stage 1

Byte comparison rejected deletion of two same-sized test logs: elapsed measurements differ.
No loose top-level file has an identical SHA-256 peer. Both logs remain intact.
The obsolete detached-toolchain directory was verified empty and removed by rmdir only.
Receipt: stage1.json. No file bytes freed; directory allocation is filesystem-dependent.
No product source, dependency, skill resource or historical evidence was removed.

## Stage 2

Semantic inspection: workflow owns per-task closure; templates, catalog, bridge index
and skill integration link to that authority. Reviewed three cases: behavior changes
require caller/usage/evidence updates; documentation-only changes require checking
the actual entry; unchanged regression fixtures can explain no impact by identifying
the preserved contract. This is contract/example review, not observed autonomous
agent compliance. The catalog/profile and individual technical skills are unchanged.
T001 documentation disposition: inventory, spec, plan, tasks and this report reflect
the rejected duplicate hypothesis and actual empty-directory removal.
T002 disposition: workflow, task/checklist templates, catalog, bridge index and skill
integration updated; behavioral implementation and executable checks follow in T003+.

## Stage 3 implementation

The shared resolver in scripts/lib/common.sh owns operational category paths. Existing
checks/security/Cargo locations remain compatible. All maintained source producers
were searched, including dynamic new_run calls, dataset generations, CARGO_HOME and
source snapshots. Product task output belongs to the user's selected workspace, not
.local; it remains unchanged. The snapshot temporary listing uses system mktemp and
is removed by its existing producer. Local intervention scripts are historical inputs,
not promoted operational interfaces.

16 loose records migrated by same-filesystem rename under records/legacy; see
migration.json for exact old/new mapping, hashes and bytes. These files are not inputs
of current operational scripts. Historical references retain the observed old paths;
the manifest resolves them without rewriting history. No payload bytes were deleted.
Build, recovery, old checks, scanner interventions, audit-config, security-tools and
usage.md stay pinned due to embedded paths, acquisition provenance or unique evidence.
No automatic migration replays those interventions. CARGO_HOME remains unchanged.

New runs own metadata, an exclusive lease and complete/pinned state. The explicit
collector is dry-run by default. Release requires a full byte-identical retained copy;
apply rechecks retention and acquires the lease before rename/deletion. Trash tickets
survive interruption and permit checking remaining bytes against the retained copy.
Two cleanup receipts (current/previous) bound operational audit growth. Permanent
acceptance observations remain in docs/validation outside this cleanup mechanism.
No age/space heuristic is adopted: the measured 44+ GB predominantly contains unique
historical/experimental material, whose safety cannot be inferred from size or age.
The deletion trigger is an explicit apply after evidence retention/release.

## Stage 4 and measured outcome (final regression in progress)

README, documentation index, scripts usage and the canonical local-artifact guide
now expose actual commands and shared authorities. Full-verification environment
keeps all three explicit maintainer overrides. No full Cargo/scanner gate was run:
this change affects governance/scripts and does not modify product Rust/Cargo inputs.

The final measured local inventory has 31 -> 16 direct entries, including the new
maintenance lock. Sixteen loose records (86,414 bytes) now live under records/legacy;
renaming preserved all payload bytes. Stage 1 removed an empty directory only: no
file bytes were freed, and no unmeasured filesystem directory-block saving is claimed.
New producer records add a few KB; local-after.json records actual totals separately
from migration/cleanup receipts. There is no claimed 44 GB space reclamation.

Deeper size inspection identifies toolbox-completion/candidate/tools as the dominant
legacy volume (approximately 38 GB allocated). The candidate also has central
preconditions, promotion and recovery-rehearsal scripts referring to that exact local
installation. This is not proven to be a redundant byte-identical current installation:
leave it pinned. Revisit only after reviewing candidate revisions, retained datasets
and recovery consumers; this maintenance does not replay central operations.

Real checkout dry-run: 138 protected-unreleased plus 12 protected-name entries, zero
eligible deletions. This protects all 148 legacy runs and the two new producer runs.
Real destructive operations were exercised only in disposable filesystem fixtures.

Focused native tools: ShellCheck 0.11.0, Ruff and Bandit via prepared Toolbox images,
explicit shared SELinux labeling and bounded source copies. ShellCheck first timed
out twice; after folding path functions into the existing common module (avoiding a
nested source inclusion), it completed with zero findings/exit 0. Ruff initially
reported E402 in a new test; the import was corrected, then Ruff and Bandit returned
zero. Reports/diagnostics preserve tool image identity, native exits and cleanup.
No rule was globally disabled and no new finding suppressions were introduced.

Main governance check and feature freshness check passed with AC-05 still pending
broad regression. Earlier broad-run failures exposed missing new-feature evidence,
manual succession fixtures missing the new transition, and an in-flight registry
change; they are retained as failed observations, not accepted results. Fixtures now
include the current transition while retaining corruption/downgrade assertions.

T003/T004 documentation disposition: canonical local-artifact guide, script usage,
migration and this report updated. T005 remains open until the stable broad suite
and final content-bound acceptance are observed.

## Final successor — 2026-11-10

This section supersedes the in-progress closure statements above. T001..T005 are
implemented, with documented dispositions. All five adopted maintenance criteria
have supporting bounded observations; no unresolved failure remains in those gates.

| Verification | Observed outcome / retained artifact |
| --- | --- |
| Broad governance/scripts suite | 165 cases, two documentation failures, one default opt-in skip; broad-regression.txt |
| Normative-hash regression after portable-link correction | 1 passed; normative-recheck.txt |
| Product/skill isolation regression after portable-link correction | 1 passed; isolation-recheck.txt |
| Final collector regressions after hardening | 23 passed, including all prior 20 cases; lifecycle-tests.txt |
| Maintenance succession adversarial cases | 6 passed; succession-tests.txt |
| Main check-ox | PASS; check-final.txt; no product acceptance inferred |
| Native static checks | ShellCheck 0.11.0, Ruff and Bandit: native exit 0, structured finding count 0, cleanup removed; native-summary.json |

The 165-case run is not relabeled as an entirely successful run: its two broken-link
failures remain in the raw output, and both exact cases passed after correction.
The original 20 collector cases were rerun with three added cases on the final code.
Other broad-run source inputs remain unchanged by collector hardening; broad-inputs.json
identifies completion-time source bytes, and before-final-hardening preserves the
changed collector/oracle versions and their original 20-case observation. The
portability link was corrected during that run, so its two affected observations were
replaced only by the dedicated rechecks. The default opt-in full scanner integration
was not enabled; focused real native scans are separately observed, not its substitute.

Final hardening rejects FIFO/special lock and audit paths, propagates tree-read/hash
failures, and preserves the retained destination/hash in eligibility receipts. Fresh
fixtures confirm these behaviors. Bandit INFO stderr was initially captured together
with JSON; that raw capture survives in bandit-merged-output.txt. Recapture separated
streams, then strict JSON parsing checked empty results/errors and coverage of all
seven selected Python files. Native source manifests compare 13 selected files against
the actual bounded scan copy; image identities and original commands are retained.

Original four in-progress observations and task/source/oracle bytes survive under
before-final-hardening. The subsequent 23-case/current-doc observation survives under
before-closure. Final evidence uses new observation IDs and a semantic review of
closed-task metadata; earlier results are not given new hashes to imply a replay.
Unchanged operational product observations and historical archives remain intact.

Reviewed closure dispositions: README, documentation index, scripts usage, canonical
artifact guide, SDD workflow/templates, shared skill integration, scope/decision and
affected feature evidence agree with actual interfaces. Completion checkbox changes
have no runtime effect; the final metadata review preserves test/oracle scope. The
final feature acceptance command checks the frozen criterion/input bindings rather
than interpreting completed documentation as proof of execution.

Measured file bytes: 45,886,126,196 -> 45,886,129,208 (+3,012 from new producer records).
Top-level entries: 31 -> 16, including the new maintenance lock. All 86,414 migrated
record bytes retained. No file payload space was freed; directory-block changes are
not claimed as measured reclaimed space. Approximately 38 GB of legacy candidate
volumes remain pinned pending candidate/recovery-consumer review. This is an explicit
preservation requirement and next review step, not an estimated reclaim amount.

Limits: cooperative same-user leases/path checks, not hostile-writer isolation or a
power-loss durable transaction. No product Rust/Cargo changes, new roadmap feature,
commit, publication, global install or central source edits. Toolbox native executions
created their own operational records under the separately approved execution scope.

### Selected acceptance scope correction

The initial --features sdd/features/repository-maintenance invocation selected no
child feature directories; its exit-zero freshness invocation established structure,
not feature acceptance. Adding --require-approved correctly exposed "No feature
directories found". Those invocations are not acceptance evidence. The existing main
check already audited the real feature/evidence, but selected approval is now checked
by acceptance.py using the unchanged validator's schema, traceability, input freshness
and status gates against the actual feature. No feature was moved, no global approval
was requested, and no validator rule was bypassed. Final output: feature-acceptance.txt.
