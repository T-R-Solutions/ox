# Governance log repair — 2026-11-15

Scope: proven ox/governance-tests failures from ox-run-52R94IoD.
Owner: governance_repair for governance modules/tests and sdd/project.md.
Other writers own UI and test_instruction_validator.py. Preserve existing edits.

Criteria: exact reviewed successors resolve to authenticated predecessors; unknown
mutation, downgrade, corrupt/missing/symlink snapshots remain rejected. Historical
Markdown links resolve from exact observed original paths; no blanket directory
exclusion. Receipt fixture includes explicit copy context. Portable-evidence test
distinguishes current observations from historical observations with undecided ACs.

Full route under coordinator: material evidence/integrity changes. Primary consulted
entry .codex/skills/autonomous-verification-engineering/SKILL.md via
sdd/chain/autonomous-verification-engineering.md bridge_version 1; contribution:
separate authorization, execution and acceptance, immutable input bindings and
negative mutation oracles. Previous bytes retained under before-governance.

Tasks: G1 inventory/review current deltas; G2 exact successor and historical-origin
registry; G3 repair consumers and run focused regressions; G4 independent review
and validation by fresh contexts. Risks: unintended historical exemption, accepting
unknown bytes, renewing obsolete observations. No full run, log rotation, downloads,
central maintenance, publication or commits.

Observed source review: architecture appends only the bounded welcome metadata
contract. Product convergence appends scoped start/picker/welcome observations
while preserving broad INCONCLUSIVE gates. Project adds dated authorizations and
current welcome scope; this log repair qualifies changed-source acceptance.
Historical source links are resolved from 16 exact source-hash/origin pairs in
governance-origins.json, never by a prefix-wide exception. Current docs links
continue using their actual location. Unknown Markdown stays unmodified.

The scripts-centralization portable-observation test incorrectly demanded a
nonempty current observation after legitimate invalidation. It now checks preserved
current+historical portable bindings, and requires all criteria undecided (or
justified inapplicable) whenever current evidence is absent. No observation hash or
criterion was promoted. The copy-boundary fixture now expects the exact existing
versioned receipt bytes in addition to allowlisted files; no export expansion.

Focused original-location tests: python3 -m unittest discover -s
tools/governance/tests -p test_log_repair_revision.py -v: 3 passed (0.009s), exit0.
Includes exact origins, unlisted source, source mutation with escaping link, missing
source, same-byte symlink and recalculated origin-registry escape rejection.

Focused fixture checks (PYTHONDONTWRITEBYTECODE=1, PYTHONPATH=tools/governance/tests:tools/governance/scripts):
python3 -m unittest test_governance.GovernanceTests.test_script_configuration_evidence_is_portable
test_reconciliation.GitBoundaryTests.test_nested_git_directories_and_worktree_files_excluded -v:
2 passed (1.079s), exit0. These do not validate current feature acceptance.
Initial current check-ox after source edits: exit1, expected exact-successor drift
remains. Historical link failures disappeared. An initial nonnormative WC projection
was rejected; removed WC rows from normative AC projection, retaining WC states in
evidence.json and separate current prose. Recheck pending after source stabilization.

The exact14 November project terminal82c57 is unavailable (search and candidate
reconstruction failed), explicitly UNVERIFIED in governance-successors.json.
Independent review authorized a new exact project terminal->available authenticated
a0d9 original branch; the complete delta is retained in governance-project-proposal.diff.
Original14 November registry/pin remains unchanged. Every other new successor
normalizes through its exact prior terminal. Registry authenticity and preimage
hashes/symlinks are checked before normalization, including old registry tamper.
The helper rejects both available-original and replaced-terminal live downgrades.
This new review does not claim replay of missing82c57 bytes.

Reviewer P2 found SourceFileLoader may read cached bytecode or reread changed source
after hash validation. VerifiedSourceLoader now validates once and get_code compiles
only captured bytes through source_to_code. It never reads source/cache again.
The negative test changes source and poisons get_data; execution still uses validated
bytes, while new loader construction rejects drift. The original old/new checker
comparison remains exercised. No dynamic exec call or scanner rule disabled.

Five exact Bandit native findings from fixed-argv subprocess fixtures were added to
the baseline only after independent source review. No shell, command string from
untrusted inputs or global rule suppression; changed sources/policy retain exact
preflight hashes. Source pins for package-ox.py, test_governance.py and validate.py
were reviewed against before bytes; new routes/validator fixture pins bind the
reviewed occurrences. These are new observations, not historical scanner renewal.

Focused instruction/copy/native/validator cases:38 passed (3.841s), exit0.
New historical-origin/successor negatives:7 passed (0.076s), exit0.
The final stabilized focused aggregate and check-ox result follow below.

## Final copy-boundary correction and documentation disposition

The original nine-regression run failed five cases after local checker success.
A detached-copy diagnostic isolated12 missing references from four immutable
snapshots to deliberately excluded product/application targets. The source-origin
resolver was correct; copy-mode treatment had omitted those historical pairs.
Original failed logs remain governance-regressions.*. They do not establish failure
of subsequent source bytes. No broad product/path exclusion was added.

The origin registry now binds only these12 source-hash/target-path/target-hash pairs
as a new15 November metadata observation. Target hashes identify locally observed
files; absent-copy target bytes are not checked at runtime, and historical14 November
target state is not claimed. A valid exact governance-copy receipt is required.
Only absence can receive that reference disposition; present files and symlinks
(including lexical ancestors before resolve) fail. All16 preserved source bytes
are authenticated before any reference disposition, even when a removed snapshot
would be invisible to rglob. Missing origin metadata with current successor
metadata present fails closed. Changed source/metadata, unlisted target/source,
escape, live checkout and receipt tampering cannot receive the disposition.

Independent reviewer examined the bounded extension and verified all12 target
identities against local observed files. The final focused helper/copy negatives
pass12 tests (governance-copy-negatives.log, command unittest discover -s
tools/governance/tests -p test_log_repair_revision.py -v, exit0). They include
lexical dangling/ancestor symlinks and missing origin metadata with successor present.
Current instruction_revision.errors(root) returned[] (exit0) after these changes.
The previous local check-ox passed; full final checker, nine regressions and scanners
will be executed by the coordinator/root only after this writer has stopped.

Reviewed/updated documentation: sdd/project.md authorized scope, current/historical
acceptance qualification; configuration-cohesion plan/tasks/converge/evidence;
product-visual-workbench converge/evidence; this implementation record, proposal
and metadata. Previous evidence and source bytes retained in before-governance,
historical_evidence and original successor metadata snapshots. No historical hash
was renewed to imply rerun. Configuration15AC and product WC01–06 remain UNVERIFIED,
with broad product AC01–06 INCONCLUSIVE; focused repairs are not blanket reacceptance.
README/AGENTS/constitution/workflow and ADR instruction reconciliation reviewed:
existing routing, exact preservation, independent review and evidence contracts
already govern this correction. No policy/CLI/retention/dependency change needed.
Missing82c57 project replay remains UNVERIFIED; recovery of those bytes is the
condition for replay. New terminal-to-available-original branch is a distinct
independently reviewed observation, not restoration of that intermediate.
