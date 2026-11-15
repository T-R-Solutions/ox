# Plan: corrections for audit findings A01–A10

Date: 2026-11-14. Status: DRAFT FOR MAINTAINER REVIEW.
Authorized now: inspect sources, design all ten corrections, write and check this
planning supplement. Applying corrections requires the user's subsequent decision.
See [proposed requirements](spec.md), [tasks](tasks.md) and [current observations](converge.md).

## Route, boundaries and planning record

The proposed implementation uses the full SDD route with high complexity: checker
contracts, evidence projections, compatibility and agent execution policy change
together. The size of the documents is not the reason. This dated supplement
extends the existing configuration-cohesion topic without editing its bound spec,
plan, tasks or evidence during planning. It is a manual proposal, not a new feature
hidden from the automated gate. All existing parent gates remain in effect.

After approval, integrate the adopted requirements into the parent feature,
preserving AC-01–03 and adding the approved AC-04–15. Update its traceability and
evidence with actual implementation/oracle paths. Reevaluate the parent criteria
whose contract inputs changed. Do not claim acceptance of only the new criteria
while old applicable gates remain undecided.

Keep the audit report immutable as the diagnostic baseline. Record implementation
observations in a new bounded validation record. No product source, Cargo files,
global Codex configuration, central Toolbox source, hooks, commits or publication
belong to this correction scope. No blanket permission to run complete automation
is implied by approving a plan for configuration corrections.

The current planning session did not spawn agents: effective instructions restrict
new delegation. No named orchestration profile or independent review is claimed.
The target execution profile after approval is `ec_orquestrador_alta`, subject to
actual permission/capability; planning documents cannot enable it themselves.

## Consulted methods and identities

Primary method: engineering-productivity, to compare process rules with observable
failure and maintenance cost. Supporting methods address separate questions:
software-design for checker interfaces/knowledge ownership, software-testing for
rejection cases and compatibility oracles. No other skill is activated by mention.
All three bridges use format version 1; SHA-256 identifies the exact content read.

| Entry | SHA-256 | Applied contribution |
|---|---|---|
| `.codex/skills/engineering-productivity/SKILL.md` | `35dc54ead1b8bd7bcc0fa2dc348aa154cf3d11137bcdf38f972d74441416feac` | Workflow alternatives, bounded measurements and no invented productivity gains |
| `sdd/chain/engineering-productivity.md` | `39980241b4a2a71c92f3ac1ea275d7b5822e50504a853b84ed399da8655468d7` | Map process decision to requirements, tasks and observations |
| `.codex/skills/software-design/SKILL.md` | `4e214fd5dbf141ee437814a5c817b6924a05e8ad75cf6bc208281155204f6143` | Preserve callers, distinguish contract changes from deduplication |
| `sdd/chain/software-design.md` | `e15827b753ed1faa8df77e1c1f07ce06e362535dd207f46758c7bcc8d0268794` | Interface decisions and explicit ownership |
| `.codex/skills/software-testing/SKILL.md` | `2d2fbc0b44e19a2d4428eb98b8602fc7dc58884294a9f6902606423959f34aba` | Risk-based tests, independent expected outcomes and non-execution limits |
| `sdd/chain/software-testing.md` | `df02545b33d6953e9e2578eea88ed216e9b204e7f480f8c1d407583ba2cbdef5` | Trace criteria to scenarios and remaining evidence gaps |

## Decisions and risks

All decisions below are proposed, not adopted. A bounded new ADR is planned at
`docs/decisions/governance-instruction-reconciliation.md`; old ADRs remain historical.

| Decision / risk | Requirement | Recommendation and alternative | Cost / revisit trigger |
|---|---|---|---|
| D-04 / R-04 | REQ-04 | JSON owns current automated status; a delimited Markdown projection is checked. Reject free-prose parsing or a second editable status source. | Migrate projections once; revisit on evidence schema change |
| D-05 / R-05 | REQ-05 | Skill owns commit choice/gate; AGENTS owns local full-run recipe; scripts own CLI semantics. Reject another hard-coded command copy. | Cross-links must remain valid; revisit if gate/CLI changes |
| D-06 / R-06 | REQ-06 | Document exact link adaptation during template copying and test the reader's complete procedure. Avoid a new scaffolding executable for three links. | One explicit copy-time step; reconsider only if recurring misuse warrants automation |
| D-07 / R-07 | REQ-07 | Separate project and portable link scopes; project SDD uses project boundary, standalone skills retain folder boundary. Reject globally disabling containment. | Explicit compatibility transition for callers expecting old portable scope |
| D-08 / R-08 | REQ-08 | Allowlisted adoption recipe plus destination-owned context. Reject copying the populated Ox sdd tree. | An isolated adoption test is required when the recipe changes |
| D-09 / R-09 | REQ-09 | Add repeatable `--feature NAME` filtering under unchanged `--features DIRECTORY`. No criterion-level filtering. | CLI/API tests; revisit if selected-feature usage reveals another concrete need |
| D-10 / R-10 | REQ-10 | Root controller and delegated triager are distinct contexts; only delegated triager is childless/read-only by role. | Update all applicable config/profile references together |
| D-11 / R-11 | REQ-11 | Permit explicitly bounded direct routes; preserve independent review for material-risk work. Reject both unconditional delegation and silent fallback for high risk. | Maintainer policy approval and route-case review; actual host limits still prevail |
| D-12 / R-12 | REQ-12 | Deduplicate project policies and within-file repetition; preserve minimum portable safety context. | Semantic preservation review; no word-count reduction quota |
| D-13 / R-13 | REQ-13 | Current summary first, clearly labeled history afterward. Avoid initially moving all history to a new tree. | Existing markers/anchors and succession consumers need verification |
| D-14 / R-14 | REQ-14–15 | Bounded succession, affected-input review and one final stable-input check. | Failures remain visible; no generic hash refresh or global approval demand |

## A01 — Reconcile current acceptance and prevent renewed divergence

1. Inventory every current feature envelope and convergence document (39 envelopes
   at the audit baseline). Compare normative criterion IDs, current states, missing
   records and claims presented as current. Inspect chronology before classifying
   a historical approval as a conflict. The confirmed minimum is the parent feature
   and nine specialized-skill features; inventory determines additional affected files.
2. Preserve each changed convergence's predecessor as required by the existing
   evidence/succession contract. Add a clearly delimited current-status table with
   criterion ID and exact normalized state, referencing the evidence envelope.
   Put preceding conclusions under an explicit historical scope; preserve their
   meaning, dates and observed inputs. Do not promote JSON states to match prose.
3. Define this machine-readable projection in `sdd/evidence.md`. Automated JSON
   status is authoritative only for features that adopt automation; manual Markdown
   consumers remain supported. The projection is a view, not a second verdict.
4. Add a read-only `--check-convergence` check to `sdd/tools/validate.py`, opt-in
   for portable consumers and explicitly enabled by the Ox governance caller.
   It requires exactly one current block, exactly the declared AC set, valid state
   tokens and agreement with current JSON. Reject combination with structure-only
   mode because evidence is needed. Do not interpret arbitrary historical prose.
5. Migrate the Ox automated-feature projections before enabling the Ox-wide check.
   Normal validation never writes or silently repairs a projection. Manual edits
   are reviewed against JSON; a standalone generator is not required for this scope.

Files: `sdd/evidence.md`, `sdd/tools/validate.py`, current affected
`sdd/features/*/converge.md`, `tools/governance/scripts/check-ox.py`, parent feature
records, bounded succession consumers and new focused tests.
Tests: correct agreement; approved-vs-unverified mismatch; missing/duplicate/unknown
criterion; duplicate/missing block; invalid status; historical approved text below
an unverified current block; JSON untouched by the check; manual workflow unaffected.
Acceptance: AC-04 and AC-14. Baseline old implementation should miss a controlled
projection mismatch; new check must detect it. This does not reaccept product behavior.

## A02 — Repair commit verification routing

Update `.codex/skills/commit-governance/SKILL.md` so the affirmative path obtains
the complete command and local environment from `AGENTS.md`, checks actual CLI
semantics in `scripts/README.md`, and retains the requirement to inspect results.
The current resolved command is:

```bash
TOOLBOX_BIN=/home/rodrigo/Projetos/dev_audit/shared-toolbox/bin/toolbox \
TOOLBOX_SELINUX_LABEL=shared \
CARGO_HOME="$PWD/.cache/ox/cargo-home" \
  ./scripts/automate.sh run --scope complete
```

This block is the reviewed current plan, not a new operational authority. The skill
should link to the maintained recipe rather than maintain another executable copy.
Keep the existing yes/no question, no-answer handling, failure gate, scope checks
and no implied commit/push authority. User instructions that already resolve the
choice still take precedence; do not create another approval ritual.

Inspect current commit-choice tests in `tools/governance/tests/test_task_closure.py`
and `sdd/features/scripts-task-closure/commit-choice-*`. Add a focused semantic
route check if existing coverage cannot detect the command drift. Verify selection
with plan only: current complete is 26 checks, legacy full is 16; assertions should
use actual catalog membership, not freeze the number 26 forever. No scanner or Git
effect is needed to establish this repair. AC-05; historical command records stay dated.

## A03 — Make template use correct in its destination

Keep template-origin links valid. Change `sdd/templates/README.md`, the relevant
instructions in `spec.md`, `tasks.md`, `checklist.md`, and `sdd/README.md` to define
copy plus destination-relative link adaptation as one instantiation procedure.
For the standard `sdd/features/<name>/` destination, the current template links
`../evidence.md` and `../workflow.md#documentation-before-task-closure` become
`../../evidence.md` and `../../workflow.md#documentation-before-task-closure`.
For another location, calculate relative paths from that destination rather than
blindly inserting `../../`. Preserve fragments and destination instructions.

Use an isolated regression that performs the published steps and checks all local
links in the resulting documents. Include the three known broken links, checklist
as optional, a custom nested directory and an intentionally unadapted copy that
must fail link inspection. Do not create duplicate workflow/evidence authorities
to make links pass. Templates still contain placeholders and do not constitute
completed spec/traceability/evidence merely because their links resolve. AC-06.

## A04 — Separate project validity from portability

Refactor link validation to receive an explicit allowed boundary. Preserve the
callable `markdown_errors(folder)` default for standalone consumers and introduce
an optional boundary argument; update `audit` without breaking existing positional
callers. Add CLI `--link-scope project|portable`: the project audit's recommended
and default scope is project, while portable scope restricts links to the model
package. `--skill` always retains the skill folder boundary and rejects irrelevant
mode combinations. Explain the deliberate change to the former implicit default.

Project mode must accept `sdd/constitution.md` linking to `docs/constitution.md`
inside the root. Both modes reject escape, missing targets and symlink traversal,
including intermediate link components; do not merely resolve a symlink then trust
its result. External URLs are not fetched. Existing fragment handling is preserved;
this correction is not a general Markdown/parser or external-link crawler project.

Update `sdd/tools/validate.py`, `sdd/README.md`, affected checker callers and tests.
Check the independent governance copy with its own root; missing authorities in
that copy remain failures. Test sibling authority, package-contained reference,
`..` escape, percent-encoded path, missing target, file/parent symlink and standalone
skill escape. AC-07; no widening of package export allowlists is needed by default.

## A05 — Correct standalone adoption

Rewrite `sdd/README.md` into clearly distinguished local-use and reuse procedures.
Describe a deliberate allowlist: workflow, evidence contract, applicable templates
and optionally the stdlib checker. Create destination-owned README/project context
and a constitution pointer; do not copy the populated Ox project or its evidence.
Create an empty bridge area or copy only explicitly selected bridges with verified
skill paths. Skills are separate complete directories, selected independently.

Exclude by default `features/`, `codex-agents.md`, this correction supplement,
Ox-specific project history, all existing acceptance records and the full bridge
catalog. Explain that an Ox governance export is a different contract from adopting
a clean SDD model. Label `sdd/model/` as source-library history, not a local command.

Exercise the exact adoption recipe in an isolated destination with no access assumed
to the original checkout: no skills, then one selected skill/bridge, then a
destination constitution in a sibling `docs/` directory. Inspect included files
and runnable instructions. Test missing selected skill as a diagnosed configuration
gap. A portable package boundary must contain the referenced authorities; otherwise
the guide explicitly selects project validation. AC-08; no real package publication.

## A06 — Select complete features explicitly

Add repeatable `--feature NAME`, interpreted as direct child names of the existing
`--features DIRECTORY` container. Preserve no-filter behavior. Resolve and report
the selected set before validation; deduplicate repeated names deterministically.
An unknown name, zero match, path separator/escape, invalid container or symlink
must fail explicitly. A mistaken container that is itself a feature should yield
an actionable diagnostic, without silently changing the argument's meaning.

Filter feature schema/traceability/evidence/acceptance checks to the selected set.
Shared model, bridge and link checks remain applicable and are disclosed; selection
does not promise to ignore a broken shared authority. No per-criterion skip/filter
is added, and selected features retain every normative gate, schema-2 input binding
and oracle review. Keep existing Python API positional arguments compatible by
adding optional selection parameters at the end or by keyword.

Proposed command, NOT available until implemented:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 sdd/tools/validate.py --root . \
  --features sdd/features --feature configuration-cohesion \
  --require-approved --require-fresh --check-convergence
```

Update README/evidence examples, common agent procedure and validator profiles to
point to the selected-feature contract. Tests cover approved target beside a valid
UNVERIFIED sibling, selected UNVERIFIED/stale/schema-1 targets, multiple names,
unknown/empty names, default all-feature behavior, custom container, missing
traceability, conflict with `--skill`, and unchanged structure/freshness exclusion.
AC-09; no feature directories are moved to manufacture a passing selection.

## A07 — Clarify triage versus controller responsibility

Adjust `.codex/agents/ec_triador.toml` to state that its read-only/no-children
restriction applies when delegated as the specialist. Define the root as a
controller that performs triage and follows the common execution-route policy.
Keep the detailed handoff in `docs/development/codex-agents.md`; make config,
replication guide and `sdd/codex-agents.md` consistent with the adopted successor.
Preserve the original installation observation as historical, rather than changing
its claimed results. No model/effort or concurrency changes are proposed.

Review four contexts: delegated triager, root controller with an available
orchestrator, root with delegation unavailable, and orchestrator changing risk
classification. TOML parsing and scenario review validate instruction consistency;
they do not prove live agent obedience. AC-10; depends on final A08 route wording.

## A08 — Adopt a proportional execution policy

Recommended policy, subject to maintainer approval:

| Situation | Execution | Review / acceptance |
|---|---|---|
| Read-only explanation, inventory or bounded diagnosis | Root may complete directly | Source-based checks and explicit limits; no claim of independent implementation review |
| Clear, reversible local repair with known consumers/oracle and no material risk | Root may execute directly when authorized | Focused verification and documentation disposition; existing feature gates still apply |
| Ordinary task benefiting from coordination or a distinct specialist question | Selected normal orchestrator when permitted and available | Independent contexts when the applicable acceptance contract requires them |
| Material changes to authorization, evidence/gates, integrity, concurrency, migration, compatibility or recovery | High profile orchestration with explicit ownership | Independent review and validation remain required |
| Required capability or independent context absent in material-risk work | Complete authorized independent analysis/planning; do not begin dependent risky execution | Record exact gap; keep affected acceptance unverified and resume when capability exists |

Direct local execution requires all local-route conditions, not a small diff alone.
Changing an agent rule or a validation contract, including this correction project,
does not qualify for the low-risk exception. Reclassify when new material risk is
found. A missing tool does not convert a high-risk task into a direct low-risk task.
Explicit user/host restrictions on delegation always prevail. Root may not claim
that self-review is independent validation or that it switched models in place.

Update common procedure, root config, relevant role descriptions, replication
guide and scope record; workflow remains the authority for local/full SDD routes.
Review read-only audit, typo/link repair, known local bug, schema migration,
permission change, acceptance-checker change, unavailable agent slots and unknown
scope. Conduct a bounded real-client handoff smoke check only when permitted and
available, reporting it separately from textual review. No quality/cost claim is
made from these cases. AC-11. Alternative retained for decision: mandatory
delegation everywhere, accepting its documented simple-task capability blockers.

## A09 — Deduplicate by responsibility

Map each repeated instruction to its owner before deleting text:

| Knowledge | Maintained owner | Other locations |
|---|---|---|
| Permanent product policy | `docs/constitution.md` | Short references |
| Local/full route and documentation closure | `sdd/workflow.md` | Entry-point references |
| States, bindings, projections and acceptance semantics | `sdd/evidence.md` | References and role-specific duties |
| Local complete-run environment | `AGENTS.md` | Skill/procedure references |
| CLI flags and compatibility | `scripts/README.md` plus implementation | Contextual examples, clearly dated if historical |
| Commit choice and failure gate | commit-governance skill | References |
| Agent roles/capabilities/handoff | common agent procedure | Minimal profile instructions |
| Technical method and standalone safety boundary | Individual skill | Bridge selection and artifact contributions |

First remove within-file duplicate closure rules in prompt/distributed-systems
bridges. Then shorten copied project-rule bodies in bridges and validator profiles.
Keep enough direct guidance that loading one profile/skill is safe and usable.
Do not delete the shared optional-specialist paragraph from every standalone skill
just because its text matches another folder. Consolidate redundant paragraphs
inside a skill while preserving its unique failure cases, selection boundaries,
references and optional dependencies. No new mandatory common skill is introduced.

Inspect 31 bridges/skills and edit only the explicit deduplication manifest; retain
catalog/profile identities and metadata. Compare before/after by semantic obligation
and resolvable dependency, not merely line count. Count bytes/words if useful;
do not claim token savings, faster agents or better outcomes without measurement.
Clarify the bridge's `pending` domain term versus SDD `UNVERIFIED` while reviewing
outcome ownership. AC-12 and parent AC-01/03. Depends on stable A01–A08 contracts.

## A10 — Present current project state first

Restructure `sdd/project.md` with a dated opening summary: phase, implemented
surfaces and limits, current evidence locations/states, unresolved work, applicable
commands and an authorization-history index. Distinguish implementation from
acceptance; do not copy a historic F0 approval into a current-source approval.
Compare evidence and `docs/architecture/context.md` before asserting each fact.

Keep chronology in the same file initially, below an explicit historical heading.
Qualify old "Current state"/"Active authorized slice" labels as dated historical
statements; preserve exact predecessors in the bounded succession record where
required. A move to separate history files is unnecessary for the first repair.
Keep existing phase/application-state markers used by `check-ox.py` and preserve
or deliberately map incoming anchors. Current commands should delegate to their
maintained usage authority rather than copy full script recipes again.

Record this planning request as planning only; after approval record the adopted
correction scope without reviving old unrelated permissions. Review entry points
in README/AGENTS/architecture and change only actual inconsistent current summaries.
Test known phase guards, succession and links; manually trace each current-state
claim to its source. AC-13. Final wording follows A01 and A09 ownership decisions.

## Shared preservation, ownership and execution order

T004 is this planning delivery. After explicit approval:

1. T005: refresh source/input inventory, establish read/write ownership and record
   approved scope. Detect concurrent changes before any overwrite.
2. T006: adopt the bounded ADR, extend parent criteria/traceability and prepare
   succession for affected bound authorities. Keep old tests available as baseline.
3. T007/A02: fix the commit recipe routing, independent of checker development.
4. T008/A01: reconcile current status and define/check its projection.
5. T009/A04 and T010/A06: change validator boundary and selection sequentially
   under the same code owner. T011/A03 and T012/A05 follow with copy/adoption checks.
6. T013/A08 then T014/A07: adopt route policy and align role/config wording.
7. T015/A09: deduplicate against the now-stable owners; T016/A10: update project entry.
8. T017: finish bounded succession and affected-evidence disposition; T018: stable-input
   verification, independent review/validation and final criterion-level report.

Ownership assignments are responsibilities, not already-created agents:
- Coordinator owns the parent feature, ADR, AGENTS/project and shared documentation.
- Validator implementer owns `sdd/tools/validate.py` and its focused implementation;
  changes for A01/A04/A06 are serialized. Coordinator transfers any shared-file edit
  explicitly rather than allowing two writers to merge assumptions.
- Instruction implementer owns assigned profiles/config/skills/bridges after the
  per-path manifest is agreed; common guide edits remain with the coordinator.
- Test author owns new/assigned tests and returns defects to the implementation owner.
- Reviewer and validator use contexts independent from implementation. With root
  and orchestrator occupying two slots, use at most two specialists at a time;
  finish/release useful slots and run later roles sequentially if needed.

Before edits, map changed files into current evidence bindings and authenticated
succession registries. Inspect `docs/structure/files.json`,
`config/governance/normative-coverage.json`, `closure_revision.py`,
`project_revision.py`, `skill_revision.py`, `governance_support.py` and their tests.
Only extend the consumers actually affected. Preserve predecessor identity and
unknown-mutation rejection; never accept any new hash simply because it is current.
Versioned evidence preimages are distinguished from prohibited operational backup
accumulation under `.local`; use the existing bounded history mechanism, no blanket
checkout copies. If existing preservation policy cannot support a required record,
surface that exact conflict before its dependent edit.

Recovery uses task-specific changes and observed base identities, not `git reset`
or restoring HEAD over uncommitted work. If an unexpected version appears, stop
the affected write, keep both observed inputs where permitted and reconcile with
its owner. Historical report/evidence is never deleted as cleanup.

## Verification plan and completion conditions

Introduce a focused stdlib test module such as
`tools/governance/tests/test_instruction_governance.py`; the name is proposed and
must be checked for collisions before writing. Keep fixtures small and isolated.
Reuse existing governance, task-closure, configuration/project succession and
metadata tests. Add independent-copy integration cases only for the adoption,
containment and history guarantees that require them; classify them appropriately
in the existing runner rather than labeling all copies as fast tests.

Commands already present, to be run at the appropriate implementation stage:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 sdd/tools/validate.py --root . --structure-only
PYTHONDONTWRITEBYTECODE=1 python3 sdd/tools/validate.py --root .
PYTHONDONTWRITEBYTECODE=1 python3 tools/governance/scripts/check-ox.py
PYTHONDONTWRITEBYTECODE=1 python3 tools/governance/scripts/run-tests.py --group fast
PYTHONDONTWRITEBYTECODE=1 python3 tools/governance/scripts/run-tests.py --group integration
```

Inspect discovered tests and prerequisites first: the runner also discovers
`scripts/tests`; it is not only a validator unit suite. Run focused tests first,
then one affected integration pass after inputs stabilize. Plan-only complete
selection uses the AGENTS environment with `bash scripts/automate.sh plan --scope complete`.
It neither prepares resources nor runs checks. A real complete run requires its
own existing authorization; absent such authorization it is not a gate invented
by this correction plan. No download or central maintenance is implicit.

The new selected-feature command above is a future final gate only after A06.
Do not run global `--require-approved`: unrelated unfinished features remain
legitimate. Once parent acceptance is required, all of its applicable original and
new criteria must pass, not just selected new requirements. Run projection agreement
over the adopted corpus independently; unverified states can agree without being
approved. This separates consistency from actual acceptance.

Record criterion, method, observed inputs, result, artifacts and limits. Preserve
old observations and invalidate only dependent evidence. Stabilize task/document
content before collecting final bound observations; if it later changes, reexamine
only the affected observations, never refresh hashes to imply reexecution.
Review/validation failures return to the owner with a concrete repro or criterion.
The final report maps all ten findings to changed paths and evidence, names residual
limits, and records documentation disposition. Static profile review, real-client
smoke checks and model effectiveness remain different claims.

## Review request

The maintainer is asked to review the complete design, especially D-11 (direct
low-risk execution), D-07 (project/portable boundary) and D-04 (current projection).
Planning completion does not adopt these policies. Implementation stays pending
until the user approves or revises this proposal.
