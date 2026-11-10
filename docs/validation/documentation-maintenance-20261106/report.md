# Documentation maintenance — 2026-11-06

Local route under sdd/workflow.md, authorized by the maintainer's request to update
documentation, ignores, SDD and operational entry points where necessary.
Goal: make current automation discoverable, distinguish local generated data from
versioned material, and reconcile stale SDD observations without renewing hashes.

Method: inspect the dirty workspace, project/constitution/architecture authorities,
automation ADRs, current README/AGENTS and evidence input bindings. Primary method:
.codex/skills/readme-lifecycle-engineering/SKILL.md (current unversioned entry;
SHA256 in observed-inputs.json), used for navigation, command-path and drift review.
No full feature or policy change is needed. Existing unrelated changes are preserved.

## Changes and observed inputs

before.json identifies exact previous bytes, retained under before/ as .bin files.
The documentation index and feature index now expose the Bash/security successors.
The governance guide includes the maintained scripts subtree in copy boundaries and
routes Bash prerequisites to scripts/README.md. The portable SDD README retains
its library-origin example; this checkout uses sdd/tools/validate.py as documented
in project.md. A trial clarification was reverted after check-ox identified this
file as a protected core input (SDD core modified: README.md); no guard was relaxed.

The root ignore now excludes all root .local/ scratch, snapshots and runtime data,
consistent with the shell ADR. This includes local usage notes and tool downloads;
reviewed source/configuration belongs outside .local/, and retained official
evidence belongs in docs/validation/. No files were deleted or removed from Git.
Existing application/.gitignore already covers its target directory.

AGENTS.md, the root README.md and sdd/project.md were reviewed and require no
additional instructions for this bounded change: they already describe the active
scope and link the canonical automation guide. Their preexisting edits and any
historical digest mismatches are preserved. No commit invocation policy is added.

## Evidence succession

The initial validator failed on preexisting stale records in scripts-task-closure
and scripts-toolchain-config. The ignore edit additionally changes an input bound
by scripts-security-preparation. affected-evidence.json enumerates each observation
and changed input. Those observations are preserved verbatim in historical_evidence;
dependent decided criteria are INCONCLUSIVE, and convergence records expose the
current states. Earlier execution logs are unchanged. This is an explicit loss of
current acceptance, not a new scanner run or technical rejection.

## Acceptance and limits

Criteria: new navigation targets exist; Git ignores local scratch while leaving
maintained source/configuration/SDD and official evidence eligible; SDD records
contain no stale active input bindings. Methods and exact exits are in checks.json
and raw check outputs. observed-inputs.json binds the reviewed final files.

The initial check-ox run also failed on preexisting exact-content succession guards
for README.md, sdd/project.md and commit-skill metadata. Repairing those executable
guards is outside this local documentation change. They remain explicit limitations;
no hashes or guard code were changed to hide them. No product tests, GUI runs,
scanner re-execution, packaging, network acquisition or commits were performed.
Revisit these records when their technical inputs or canonical command paths change.

Observed local results: navigation target inspection APPROVED (navigation.json);
ignore/versionability cases APPROVED (ignored-runtime.txt/versionable-inputs.txt);
whitespace check APPROVED; SDD evidence/schema/input checking APPROVED (exit 0,
sdd.txt). These approvals cover only the stated documentary criteria. Exact
preservation comparison passes (preservation.json). Source command paths exist;
no onboarding/build/scanner instructions were executed as product validation.

Overall governance acceptance remains INCONCLUSIVE because check-ox rejects the
preexisting README/project/commit-skill succession mismatches. The intermediate
protected-core diagnostic is retained in ox-intermediate.txt; the SDD README was
restored to its exact preimage before the final check. Operational product and F0
observations are unaffected. All real-scanner successor work remains scoped to the
changed-input inventory; optional native Trivy/Grype acceptance stays UNVERIFIED.
