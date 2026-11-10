# Native exec governance reconciliation — 2026-11-08

Scope: Ox only, full-route continuation of scripts-toolchain-config and
scripts-toolbox-native. No commits, central edits, downloads or installations.
All preexisting unrelated changes retained.

## Diagnosis and authority

Baseline rerun: `python3 tools/governance/scripts/check-ox.py`, exit 1, 32
failures (baseline.stdout; stderr separate). Original
`docs/validation/scripts-toolbox-native/check-ox.stdout` is unchanged.

Four document failures originate in readme_revision.errors,
project_revision.errors and skill_revision integration checks reached by
check-ox/governance_support. Their chained registries stopped at the reviewed
scanner remediation/ownership bytes. README changed TOOLBOX discovery; project
appended authorized native migration. These are authorized documents lacking
registered succession, not permission to accept arbitrary hashes.

The remaining 28 errors originate in sdd/tools/validate.py input_errors:
four current ownership observations bind prior backend, dispatcher, backend tests,
security quality tests and project bytes, plus deleted consumer config/lock.
Those observations describe historical bytes correctly but lost current validity.
The native migration ADR supersedes consumer snapshots/adapters/locks; deleted
configuration is an obsolete operational dependency, not a reason to recreate it.
This was a representation gap, not a defective hash comparison. No stale-hash
exception was added to the validator.

Authority: user authorization, docs/decisions/scripts-toolbox-native.md,
sdd/workflow.md and sdd/evidence.md. REQ-05/06 retain policy/integrity obligations;
old snapshot/adapter mechanisms are superseded. Insufficient current operational
qualification keeps AC-05/06 UNVERIFIED. AC-07 stays UNVERIFIED.

## Implementation and preserved records

closure_revision.predecessor now first resolves an exact native documentary
transition. succession.json is pinned by its complete SHA256 in code and binds a
review plus two verified preimages. Unknown content is not projected, recalculated
registry content is rejected, active downgrade raises, and missing/corrupt/symlink
preimages fail. Existing historical chains remain unchanged. Adjacent diffs show
the exact reviewed README and project changes. No live document was rewritten.

Four E-OWNERSHIP observations moved verbatim from evidence to historical_evidence,
the existing project representation. Their IDs, methods, results, artifacts,
hashes and input lists are unchanged. Current references resolve only from
`evidence`; historical observations cannot approve inputs. New
E-NATIVE-RECONCILIATION and successor-observation.md map each original observation
to current reexamination and explicit limits. They bind actual current bytes and
new test logs. No previous test result received updated input hashes.

Affected files: tools/governance/scripts/closure_revision.py;
tools/governance/tests/test_scanner_succession.py;
new tools/governance/tests/test_native_exec_succession.py;
sdd/features/scripts-toolchain-config/{spec.md,plan.md,tasks.md,converge.md,evidence.json};
and this validation directory (registries, preimages, reviews, raw logs).

The scanner succession test originally failed twice because its ownership unit
fixture used today's later terminal project bytes and its integration path omitted
the new transition. Retry uses ownership's actual terminal preimage for its unit
fixture and composes native then ownership then remediation in the integration
case. This preserves each transition's contract; it does not relax rejection.
Initial failures remain in scanner-tests.stderr.

## Executed verification

Commands ran from Ox; stdout and stderr are separate adjacent files.

| Command | Exit | Observation |
| --- | --- | --- |
| python3 tools/governance/scripts/check-ox.py (baseline) | 1 | 32 reconciliation failures |
| python3 tools/governance/scripts/check-ox.py (final) | 0 | Structural/profile/content checks pass; explicitly no product acceptance |
| python3 sdd/tools/validate.py --root . | 0 | Evidence/schema validation |
| python3 sdd/tools/validate.py --root . --require-fresh | 0 | Current bindings match |
| python3 -m unittest discover -s scripts/tests -p test_backends.py | 0 | 7 cases |
| python3 -m unittest discover -s scripts/tests -p test_automation.py | 0 | 10 cases, including public dispatch failure behavior |
| python3 -m unittest discover -s tools/governance/tests -p test_document_succession.py | 0 | 4 cases |
| python3 -m unittest discover -s tools/governance/tests -p test_native_exec_succession.py | 0 | 4 cases; exact successors, unknown content, registry tampering, downgrade, preimage loss/corruption/symlink, historical preservation |
| python3 -m unittest discover -s tools/governance/tests -p test_scanner_succession.py | 1 then 0 | 4 cases; initial fixture failures preserved, retry passes |

A scoped diagnostic of feature_errors(require_approved=True, require_fresh=True)
returns the eight unmet criteria in approval.stdout and exits 1. This is a Python
API diagnostic, not a new public approval command: native AC-03; toolchain
AC-01..04 INCONCLUSIVE and AC-05..07 UNVERIFIED. The baseline public check also
propagated failures with exit 1. check-ox is structural and must not grant approval
merely because its final exit is zero. No approval semantics were modified.

## Remaining blockers and recovery

No scanner homologation: real active central revisions/tool operation, public
OSV/Trivy age mechanism, actual expired RustSec maintenance, and Docker command,
report and cleanup qualification remain unverified. No external prerequisite was
reclassified as NOT APPLICABLE. Historical deletion is not current cleanup proof.
This task did not rerun a detached distribution or qualify real scanners.

Recovery: stop concurrent edits; compare current files with this report and the
bound inputs before restoring. recovery/ holds exact pre-edit bytes for every
existing file changed here; restore those files individually only if no later
edit occurred. Restore the previous scanner test from its .bin. Remove the newly
added test only after comparison with its recorded input hash. Retain this whole
validation directory and all original history as audit records. Rolling back the
succession code restores the original check failures, not approval. No git reset,
central database manipulation or fallback executor is needed. To resume operational
acceptance, satisfy external prerequisites under separate authorization, execute
real methods and add new observations without rebinding this history.
