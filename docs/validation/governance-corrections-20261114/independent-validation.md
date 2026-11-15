# Independent criterion validation — 2026-11-14

## Current final verdict — APPROVED

All configuration-cohesion AC-01–15 are APPROVED for the observed governance scope.
The independent validator executed the mandatory local source check followed by
the complete selected-feature gate, both exit 0. No other feature or product
behavior is approved by this verdict. The historical provisional decisions below
are superseded by this section, not erased.

| Method executed by this validator from the Ox root | Exit / observation |
| --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 python3 tools/governance/scripts/check-ox.py` | 0; local profile/catalog/bridges/SDD/normative IDs/links/archive inspection passed; local sources are required to match the 14 snapshots and exact profile inventory |
| `PYTHONDONTWRITEBYTECODE=1 python3 sdd/tools/validate.py --root . --features sdd/features --feature configuration-cohesion --require-approved --require-fresh --check-convergence` | 0; explicitly selected configuration-cohesion, schema 2 and every AC-01–15 checked with fresh bindings and matching projection |
| Python stdlib read-only hashes/counts/predecessor comparisons described below | 0; 201 preserved input hashes and 272 final input hashes matched; ten current changed-input byte/word measurements matched |

The final logs were read, not inferred from their exit fields. closure-01.log has
43 tests OK, no skips; closure-02.log has eight tests OK, no skips, including all
six earlier failures plus archive/export recovery. closure-03.log checks the full
adopted projection corpus; closure-04.log checks the local consumer. Their hashes
and the original logs' hashes match their observation manifests. The initial fast
run was 202 tests with one explicitly opt-in native-security skip; the initial
23-test integration had six failures. Those observations retain their original
inputs. The final affected-consumer run is not represented as a whole-suite rerun.

The reviewer independently exercised copy, recopy and ZIP extraction and rejected
an extra local profile, excluded product insertion and snapshot symlink. Its
extra-profile defect was fixed and retested. envelope-copy-check.json records the
new envelope copied byte-for-byte and accepted by the complete selected gate in
the explicit snapshot-only consumer; that is not live profile installation.

### Final criterion decisions

| Criterion | Decision | Evidence / oracle and applicable limitation |
| --- | --- | --- |
| AC-01 | APPROVED | Manual original nine procedure/31 contribution comparisons and current four bounded skill/bridge deltas; preservation tests in closure-01. No lost unique method observed; no claim to exercise every technical method. |
| AC-02 | APPROVED | Local check-ox and selected gate exit 0; succession/metadata/link and affected-copy negatives pass. Export snapshots do not replace required local-source equality. |
| AC-03 | APPROVED | Independently recomputed original/current byte and whitespace-word counts; historical AGENTS successor located exactly. Semantic coverage and remaining model limits stated; no token or efficacy claim. |
| AC-04 | APPROVED | closure-01 malformed/missing/duplicate/mismatch projections and old-checker regression; closure-03 full corpus and current selected gate. Historical conclusions are not reparsed as current approval. |
| AC-05 | APPROVED | closure-01 real plan-only CLI membership and static negative/no-answer/failure checks, plus manual skill diff. Complete environment routes through AGENTS; no full scanner run or commit asserted. |
| AC-06 | APPROVED | closure-01 isolated standard/custom template adaptation with retained fragments and rejected unadapted copy; README procedure manually compared with fixture. |
| AC-07 | APPROVED | closure-01 sibling/project versus portable/skill boundary tests; escapes, encoded paths, missing targets and intermediate/file symlinks rejected. No network or OS-sandbox claim. |
| AC-08 | APPROVED | closure-01 isolated clean adoption without/with selected skill, destination constitution and missing-skill diagnostic; manual allowlist review. Ox governance export is separately checked by closure-02. |
| AC-09 | APPROVED | closure-01 selection positives/rejections and retained schema/freshness/shared gates; real selected gate exit 0 across all 15 ACs. No unrelated global approval required. |
| AC-10 | APPROVED | Manual controller/delegated-triager role review; TOML/matrix tests and local check-ox equality/inventory. Fourteen snapshots authenticate observed config/profile bytes, not effective model behavior. |
| AC-11 | APPROVED | Independent source scenario review of read-only/local/material-risk/capability-absent routes; feature gates and independent contexts preserved. Live smoke supports only creation/context/return/slot reuse. |
| AC-12 | APPROVED | All 31 identities and contributions mapped, 30 skill bodies unchanged; changed skill/bridges inspected, current counts and corrected section maps checked. Shared standalone safety remains. |
| AC-13 | APPROVED | Manual project/architecture/current-envelope comparison, current-entry regression and bounded successor tests. Opening state and historical authorizations remain distinct. |
| AC-14 | APPROVED | 201 preimages/64 bounded successors; mutation/tamper/downgrade/symlink and explicit-copy negatives; 21 removed observations across 19 unique other features verified against preserved envelopes, no retained same-ID object changed. |
| AC-15 | APPROVED | Current focused and affected-consumer logs, independent initial/focal review, mandatory local check and complete selected-feature schema-2 gate. Original failures/skips retained with their limits. |

### Observed final identities

Source/config/contract identities: closure-inputs.json (272 entries), SHA-256
`71661e61443916817da301857da6032b46e5acffbb75d949d053d12d60b34af8`.
Preserved inputs: inputs-before.json (201 entries), SHA-256
`c1436ff8f3d6405b9e5cc126ee31577dd87c380ca9e4bde5e98b0646eb7a841f`.
Final deduplication.json: `cc5b1ee092564f3de3193fcff0cd43c9a51946adbf6d3b9aa4036dce65152030`.

| Observed artifact | SHA-256 |
| --- | --- |
| canonical evidence.json | `69c3a9bda8f21b7c4f2c71ff859a4dc288926fc4991d67d08a8a293a83fa9df7` |
| canonical spec.md | `1d799a527175bf6e55217ac5c030c6cbb479f9f03002e4125f243022b1dd6ffb` |
| canonical plan.md | `0ed131d912b7aaa43cdd62be6abcb1907a42992302666cf8a78d4d7190bcb056` |
| canonical tasks.md | `f28ea85a797545b9b6dcb4526fa7043410520991b9892b498cb344238a0c7197` |
| canonical traceability.json | `75001146ccba92f75ea0d039c909b0597cae7b02ff0eaf5821c1e83ff2c31550` |
| final-observations.json | `ed176d2badea128156959fe5f4c5f0820445312e35ea7829dc2e29293828dcd6` |
| independent-review.md | `972a210fed4c6a40881ebb3221fbb37d352a923d8246e2260f46ae78e0b2103c` |
| envelope-copy-check.json | `fff1cd8c406a9690cc4be8d8486282b823c87cfe46925bbc932decc71f0791db` |

Documentation disposition: reviewed updated AGENTS references, common agent guide,
SDD README/workflow/evidence/templates, project/architecture opening, adopted ADR,
canonical spec/plan/tasks/traceability/converge, implementation/review/observation
reports and affected-evidence map. Their route, adoption, current-state, copy and
resumption contracts agree with the observed scope. This validator wrote only this
report; the coordinator records final delivery in report.md. This report is a
post-gate output outside the envelope inputs, so its completion does not invalidate
the observed bindings or create a self-referential proof.

Limits: no Rust product execution, full Toolbox/scanner run, download, commit or
publication is accepted. The fast suite's disposable installed cargo-machete fixture
is not a product scan or dependency download. Public receipts describe copy mode;
they are neither provenance authentication nor authorization. Static role review,
client smoke and deterministic checks do not prove general agent obedience,
quality, cost or performance. No acceptance blocker remains for this scope.
Resume/revalidate only affected observations if source/config/contract/oracle bytes
change; failures return to the owner without weakening criteria. Other unfinished
features retain their own current non-approved states.

## Historical preliminary observation — 2026-11-14, before final execution

Historical status: INCONCLUSIVE pending stable inputs, final execution logs and selected-feature
acceptance. This is an independent validation context, not the implementation context.
Only this report is owned by this validator. No criteria, implementation, gate inputs,
historical evidence or permissions were changed. No subdelegation was performed.

## Scope and method

Read AGENTS, common agent procedure, workflow/evidence, constitution, architecture,
project, configuration-cohesion spec/plan/traceability and the adopted instruction
reconciliation ADR. The full route applies because acceptance and authorization
contracts change. All AC-01–15 apply; unrelated features need not be approved.
Reports from implementers were treated as leads, not proof of behavior.

Initial read-only Python stdlib comparisons (exit 0) checked all 198 entries of
inputs-before.json against actual preserved bytes: no missing file or hash mismatch.
Compared original 20261111 Operating procedure sections for nine changed technical
skills and all 31 bridge contribution tables against the 20261114 preimages: equal.
Read current deltas for commit-governance and prompt/distributed-systems/autonomous-
verification bridges: preserved methods, selection and handoff; intentional policy
changes are explicit user-choice precedence, current recipe routing and domain
pending versus the five SDD states. These are not claims of model obedience.

Recomputed UTF-8 byte and whitespace-word counts for original changes.json and
current deduplication.json. All ten current changed-input measurements and hashes
match. Historical AGENTS after-size is 2468 bytes / 266 words, authenticated by
complete-repair-20261111/before/AGENTS.md.bin SHA-256
60927db048a6f6c9a0498d022a73ca3d6f6fad059b0aa9334bc5ddd1c4902f73.
Later successors explain today's 2476 bytes / 266 words; historical measurements
must not be replaced with today's counts. No token/cost/speed claim is supported.

## Criterion matrix before final execution

| Criterion | Observation / applicable oracle | Current decision and remaining condition |
| --- | --- | --- |
| AC-01 | Original procedure/contribution comparisons plus today's four direct deltas preserve unique methods | Supported by manual inspection; await final bindings |
| AC-02 | Profile/link/freshness and configuration succession tests are relevant, including negative cases | INCONCLUSIVE until current consumer execution and selected gate |
| AC-03 | Historical/current byte-word counts recomputed, original historical AGENTS located, scope limits explicit | Supported by manual inspection; await final bindings |
| AC-04 | Projection oracle tests missing/duplicate/mismatched rows and old-checker defect sensitivity | INCONCLUSIVE until final full-corpus projection observation |
| AC-05 | Route tests compare real plan-only catalog membership; negative/no-answer/failure contracts inspected | INCONCLUSIVE until current execution log |
| AC-06 | Standard/custom copy adaptation preserves fragments, unadapted copy fails | INCONCLUSIVE until current execution log |
| AC-07 | Explicit project/portable scopes and encoded/escaping/symlink rejection scenarios identified | INCONCLUSIVE until current execution log |
| AC-08 | Manual README comparison confirms allowlisted isolated fixture follows the published prose procedure | INCONCLUSIVE until independent-copy execution log |
| AC-09 | Whole-feature selection retains schema, binding, all ACs and shared checks; invalid/empty selection tested | INCONCLUSIVE until current regression log and real selected gate |
| AC-10 | Common route distinguishes root controller from delegated childless/read-only triager | Supported as instruction review; await current TOML/profile checks |
| AC-11 | Read-only/local/material-risk/capability-absent cases preserve authorization and independent context requirements | Supported as instruction review; no general effectiveness conclusion |
| AC-12 | Thirty skill bodies unchanged; changed skill and three bridges have bounded semantic dispositions | Supported by comparisons; await current preservation execution |
| AC-13 | Opening summary separates implementation, acceptance and scope; history and anchors retained | Supported as manual source review; await consumer/succession checks |
| AC-14 | 198 preimages verified; succession oracle covers unknown bytes, tamper, downgrade and symlinks | INCONCLUSIVE until final affected-evidence mapping and consumer checks |
| AC-15 | Complete parent selection, schema 2, fresh inputs and independent review required | INCONCLUSIVE; final selected-feature gate intentionally not yet run |

## Limits and resumption

The adoption fixture encodes the prose recipe rather than parsing instructions;
manual comparison is part of its oracle. Static route tests do not invoke a model.
The live-client smoke claim is limited to profile/context creation, returned output
and successful slot reuse; no quality, cost or general instruction compliance follows.
Rust product behavior, scanners, downloads, commits and publication are outside scope.

Resume after coordinator confirms stable inputs, final logs and schema-2 envelope.
Inspect failures/skips and independent review, then execute from the Ox root:
`PYTHONDONTWRITEBYTECODE=1 python3 sdd/tools/validate.py --root . --features sdd/features --feature configuration-cohesion --require-approved --require-fresh --check-convergence`.
Record exit and exact observed identities before final verdict. If an input changes,
reevaluate only dependent observations; failures return to the coordinator without
relaxing criteria. Documentation disposition: this owned report records validation;
the coordinator owns feature/project/evidence disposition and closure.

## Subsequent integration observations, pending revalidation

Before the export repair, a read-only comparison of affected-evidence.json with
the preserved and current envelopes found 19 affected features and 20 removed
observations: each removed ID existed in its predecessor, none remained current,
and no observation retained under the same ID had changed its content or digests.
The 255 entries of stable-inputs.json and 62 current skill/bridge hashes also
matched at that observation. These checks exited 0; they do not certify later edits.

Read independent-review.md. Its corrected bridge-section mapping is a bounded
metadata correction, not technical-method execution. Its intermediate check-ox
failure is retained as a failure, not reinterpreted as successful final integration.

Coordinator subsequently reported failed export integration: product convergence
records, local agent configuration and a historical link were unavailable in the
deliberately smaller governance copy; a prior README successor also required
bounded handling. AC-02/08/10/14/15 remain INCONCLUSIVE until the repair's independent
review and current execution. Required discrimination includes tampered/missing
snapshots, local-source drift/absence, mandatory versus deliberately excluded
records, exact source/target/hash link exceptions and rejection of README edits
beyond the authorized successor. A portable snapshot does not establish installed
profiles or model behavior. AC-10 still needs actual local configuration coverage
even if its traceability implementation points to the exportable common guide.

The reported EOF-only cleanup of two bridges requires exact diff/measurement and
succession reevaluation; pre-cleanup fast/integration logs must retain their own
input identities. No final approval has been issued.
