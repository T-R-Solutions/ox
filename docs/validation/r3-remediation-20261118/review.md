# Independent review observations (consolidated by the coordinator)

Reviewer: ec_revisor in an independent context, with no product, test or authority
edits. This file consolidates the reviewer's returned messages; it is not a claim
that the implementer independently reviewed its own work. Final acceptance remains
pending complete verification and the validator's assessment.

## Contract review and corrections

The reviewer traced ledger → Claude correction → audit → Windows → OSV →
instruction/closure → project/skill preservation and the copied checker consumers.
The existing ledger seam was accepted as a proportional location for the change;
an unanchored mutable registry would allow source/metadata self-registration.

Independent probes found and drove these corrections:

1. Indented/tab/closing-hash ATX headings could bypass duplicate-section checks.
   The parser now recognizes those forms; Setext ambiguity and incomplete fences
   or comments reject. The reviewer reexecuted the alias cases and observed rejection.
2. Initially every project section remained frozen. The revised contract protects
   only the title, Authorities and Features and methods; current summary and
   contextual entries are mutable, with explicit summary/history structure.
3. Complete older projects could be projected into the new contract. A versioned
   project format marker now rejects complete pre-version documents before
   projection. The reviewer verified two non-immediate historical preimages.
4. Mixed/invalid/duplicate version declarations were initially accepted. The final
   marker-family count rejects all such declarations, including duplicate v2 at EOF
   without newline. Independent probes confirmed these cases.

The marker is a format contract, not authenticated chronological freshness of
contextual prose. An old narrative deliberately edited into the current format
cannot be distinguished from another permitted contextual edit by this checker.
Historical observation integrity and normative section integrity remain separate.

The reviewer executed 13 ledger tests successfully in 0.118 s against ledger
SHA-256 `be36873fcebaaaf4c3ecdeaf9b3c98bf96aa96ba2fa0db4f01d39f20869994e2`.
This does not replace full-suite, copied-checker or feature-gate evidence.

## Static-source review

The three changed sources bound in automation.json were compared in full with the
preserved task baseline. The reviewer found no new subprocess boundaries, commands
or suppressions; their subprocess ASTs retained 3, 5 and 2 calls respectively.
Reviewed identities are retained in static-review.json. Only these three source
bindings were updated, without renewing historical scanner observations.

## Follow-up negative oracles

The first final-suite attempt exposed old tests that still reject any contextual
project append. The reviewer confirmed that changing only the live-project mutation
to corruption of the normative Authorities section preserves the new rejection
contract. Unknown supplied-buffer tests (without modifying the live file), exact
preimage hashes, metadata, missing/symlink and downgrade negatives must remain.
Affected tests identified by inspection: audit_revision, claude_analysis_revision,
osv_acquisition_revision, windows_design_revision, instruction_succession,
project_revision and readme_skill_integration. These follow-up changes remain
pending while the current integral observation finishes; no final-suite pass is claimed.

## Methods

Actual skill consulted by reviewer: .codex/skills/autonomous-verification-engineering/SKILL.md,
without a declared semantic version, for historical/current/freshness oracle separation.
Baseline source preimages are now retained under baseline-sources; the operational
copy originally used for comparison was released after hash verification to relieve
the observed temporary-storage quota. See baseline-release.json.

## Historical authentication under non-strict projection

Independent reviewer confirmed a medium-severity local defect: the ValueError catch
in predecessor also catches missing, corrupt or symlinked historical terminals when
strict=False, returning the live buffer. A temporary-fixture reproduction rejected
corruption under strict=True but returned under strict=False. No false check-ox
approval was demonstrated. Authentication must occur outside that catch, preserving
non-strict unknown-live and unknown-supplied-buffer behavior. The fix and explicit
negative regressions remain pending while governance-final-01 observes unchanged
source inputs. This finding is not waived by earlier successful checks.

## Final mechanism review after transitive oracle constraint

The independent reviewer inspected the implemented schema-2 protocol in the same
document_ledger module, the active registry, ADR and bound oracle review. The
reviewer executed 21 ledger tests (exit 0, 0.490s) and 16 additional temporary-fixture
observations: missing/symlinked active registry, before snapshot, decision and review
all rejected under strict=False and strict=True. No new findings were identified
within the explicitly documented trust model. A prior implementation finding about
normalizing both live and supplied data for legacy destinations was corrected and
has a dedicated passing regression.

Observed ledger SHA-256: 039fdd67cf192de1c70e8fbac97c104cb361ec9991060dd26729bd54a5a56340.
Observed tests SHA-256: 4dd9bd4b339c2abbff2fa1eaf0ccf905d211448acd74cae762f33a5ca11cfc1f.
Registry SHA-256: 459b42423eb3e996d6015e0c5de67b3f97f7c142c451deee8e3599db0c9d5d4f.
ADR SHA-256: d7f95b6bc0e6834bf528a7698994396c8d1c46cfa63b30cc522990f9e94edbc7.
The exact independent source verdict was consolidated as oracle-review-v1.json
from the read-only reviewer's response; the coordinator did not invent that verdict.

The active data registry verifies declared identities/continuity, not authorization
or reviewer identity. Coherent tail removal plus source rollback is not authenticated
by this protocol alone. The ADR explicitly distinguishes this changed future trust
boundary from the still-authenticated historical registry. The reviewer did not
approve global task acceptance or unexecuted integration/copy/package checks.

Additional static review: test_project_revision.py changes only the conditional
Authorities mutation and assertNotEqual, with zero subprocess AST calls before/after.
Its current static binding was updated to 13bfb669bdc34bc719df09762f8d9cca45290ba8f00d6e38b9668483219ac679
after that independent review; no historical scanner result was renewed.

## Distribution findings retained

Seven failures in the completed first candidate suite share 36 absent application
references in the distributed product-ide-shell feature. The reviewer found that
excluding only the feature and its evidence would break docs/design/ide-shell.md
links; tokens.json also declares that page as current_shell_contract. No generic
link exemption, source deletion or product edit was authorized by this finding.

The generated package exceeded the existing 128 MiB inspection budget. Large
historical corpora have mixed dependency closures; excluding a few large prefixes
is not a validated smaller profile and still leaves more than 500 MB. An independent
export can test copy behavior but cannot be represented as successful package
extraction. Both residuals remain open, separately from the repaired named fixtures.
