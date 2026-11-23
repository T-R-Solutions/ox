# Finding dispositions — Claude analysis remediation (2026-11-17)

Source: `claude_analysis.md`, SHA-256 `9fd14c6ffd2f0ec15ea374860a44ffc4e6ca84f14fa145d040083b20635edb28`.
The original report was observed externally truncated to zero during execution.
An exact reconstruction matches the initial SHA-256 above and is retained as
`source-analysis.md.bin`; root restored the exact bytes after explicit user authorization, preserving the unexpected empty version. IDs below are namespaced by report part:
Part 1 `T-01` differs from Part 2 `T01-1`.

This matrix records decisions, including explicit residual work. Implementation labels are bounded by observed checks and explicit limits; final commands, review and validation
are in [report.md](report.md). A deferred or blocked executable defect is not
silently considered corrected. Historical claims are not new observations.

## Part 1 — complete historical disposition index

The previous [correction report](../claude-analysis-20261117/report.md) records
89 dispositions. Those observations remain historical on their original inputs.
The following reproduces each decision as a historical decision, not renewed
verification. Part 2 rows identify present follow-up, particularly E-05/T06-3,
A-06/T06-1, R-03/T06-5, K-19/T06-6 and T-18/T02-1. Omitted number findings in
the original report are explicitly identified rather than invented.

| ID | Historical disposition (not renewed) |
| --- | --- |
| E-01 | Fixed: summary consumes actual `check/state/exit_code` records, never argv; real disposable-run output is tested. `argv_recorded:false` retained as explicit provenance. |
| E-02 | Fixed: failure handlers attach to producers; redundant unreachable returns removed. Snapshot producer failures remain nonzero. |
| E-03 | Fixed: common defaults preserve explicit operator values, including empty; Cargo argv remains locked/offline. |
| E-04 | Fixed: BASE contains complete selected surfaces before filtering, so omitted records excluded checks. Mandatory governance is preserved. |
| E-05 | Fixed: producers supply stable reason categories, assessment retains `reason_code`, presentation translates codes; raw reason remains available without terminal echo. Legacy reason strings remain a compatibility fallback. |
| E-06 | Fixed: validated cargo-deny native masks classify findings as code1; raw code is retained separately. |
| E-07 | Fixed: local.sh parses before action, validates missing/conflicting arguments and root, independent of argument order. |
| E-08 | Fixed in single-field array consumers using `for`; empty exclusion arrays produce no invented predicate. NUL key/value pair readers remain paired streams intentionally. |
| E-09 | Fixed: shared aggregate_results owns precedence error2 > blocked3 > findings1 > passed0 for both interfaces and summary. |
| E-10 | Environment divergence fixed. Selection difference retained as documented compatibility: legacy24 versus surface26; removal would break supported callers. |
| E-11 | Missing analyzer files now emit error JSON; manifest temporary leak removed; automate.sh run cleanup armed immediately after creation; reviewed paths reject traversal segments rather than legitimate `a..b`; Bash4.4 checked. GNU utilities remain documented prerequisites and fail nonzero when absent. Optional warning/skip fields remain defensive projections, not invented counts. `set -E` in the independent retention helper is harmless; no cosmetic rewrite required. |
| R-01 | Fixed: toolbox_command is the single transport argv constructor for planning and execution; native argv takes explicit check/output/plan arguments. |
| R-02 | Lifecycle ownership isolated, but duplicate log-name encoding and owner tokens retained pending a dedicated compatibility migration; existing publication identity tests guard their equality. No rollback/trap generalization was needed for the confirmed bugs. |
| R-03 | Dead command construction removed; per-file jq mode lookup replaced by one associative map, retaining before/after stat checks. Other repeated identities guard different time windows and are retained. Native diagnostic validation intentionally checks schema and execution agreement separately. |
| R-04 | Fixed single-field array roundtrips in files/registry/selection/run; paired NUL streams retained. |
| R-05 | Retained parsers/report entry points are callable shell interfaces with tests; absence from default checks is insufficient evidence of dead public behavior. Empty directory is not versioned implementation. No broad parser retirement. |
| R-06 | Rejected global disable of SC2310/SC2016: existing per-call review is intentional. No linter rule weakened. |
| A-01 | Improved: scanner inputs are explicit, scratch arrays/local variables no longer leak in touched helpers. Named shared result variables remain the current shell-module contract; wholesale nameref redesign was not required for observable corrections. |
| A-02 | Fixed for principal automate/run entries with main functions; automate still rejects source by its documented public contract. Thin fixed helpers remain direct entries. |
| A-03 | Retained internally initialized true/false flags; no external/catalog string is executed through them. Converting all booleans is style/refactor work without a demonstrated externally controlled command path here. |
| A-04 | Retained guarded AND/OR expressions where failure of either predicate must reject; no changed semantic branch demonstrated. |
| A-05 | Common startup effects remain intentional shared entry initialization. Scanner signatures now expose their inputs, and lifecycle/presentation ownership is explicit. No generic library lifecycle introduced. |
| A-06 | Fixed publication/cleanup/final outcome ownership by extracting lifecycle.sh from presentation. Governance text projection remains conservative; changing the separate checker to a new JSON protocol requires a distinct consumer migration. |
| A-07 | Catalog owns selection/metadata; shell owns typed argv adapters, explicitly stated in registry header. Retained this split rather than executing arbitrary JSON commands. Labels and builtin names still duplicate some identifiers; schema/tests enforce current selection. |
| A-08 | Explicit scanner branches retained as small typed adapters. Dynamic hook discovery would add an implicit dispatch contract without resolving a confirmed functional defect. |
| A-09 | Added a dedicated schema stage and diagnostic for input/path/database/review data. Existing selection/schema stages remain; field-by-field diagnostic DSL was not introduced. |
| A-10 | Rejected Python production replacement: shell-only operational scripts is an explicit adopted ADR. Existing strict JSON rejection tests remain; GNU environment is documented. |
| A-11 | Retained encoded flat logs and two-date retention, explicitly required by local-artifacts.md; changing to tar/tree would change locators and recovery behavior. |
| A-12 | Unknown log-directory entries fail closed by ownership contract; mixed human/raw language is deliberate. Legacy CLI compatibility remains; Ec origin is documented in scripts README. |
| O-01 | Cosmetic cat substitutions retained outside modified code; no correctness claim. |
| O-02 | Applied `prune[-1]` with an empty-array guard. |
| O-03 | Legacy small selection loops retained to preserve stable order and compatibility. |
| O-04 | JSON accumulation retained except existing manifest JSONL path; no measured end-to-end benefit or atomic publication redesign claimed. |
| O-05 | Removed the consequential per-file mode jq lookup; remaining bounded field reads retained for clarity. |
| O-06 | No message-style-only rewrite of the portable Toolbox wrapper. |
| O-07 | Wrapper relative path already resolves from the sourced module reliably; no correctness defect. |
| O-08 | Quoted array-count arithmetic is valid and not an execution defect. |
| O-09 | Error return style retained where producer status must propagate; replacing every return with1 would lose status. |
| O-10 | Local declaration lengths are style only; touched functions gained missing local declarations. |
| P-01 | Improved tree_manifest with batched GNU sha256sum -z and one jq stream; verify_inputs caches modes once. Exact canonical identity and failed-producer rejection tested. Source-copy before/copy/after hashes remain per file to preserve observed mutation guards. Full-run 6–8minute estimate is not accepted as measurement. |
| P-02 | Full Git copy retained for self-contained historical scanning and change detection. Batched tree_identity also accelerates its manifests, but no 945MB history benchmark or cache-safety redesign was performed. |
| P-03 | Rejected persistent target/TMPDIR migration: local-artifacts.md requires disposable system-temp snapshots/builds. Operator TMPDIR remains supported. |
| P-04 | Batched tree manifest and mode map reduce repeated jq; bounded plan/heartbeat field reads remain. No unmeasured overall throughput claim. |
| K-01 | Retained narrow commit/file/rule/line fingerprints. Replacing them with a broad hex-pattern allowlist would suppress unseen future findings and contradict reviewed policy. |
| K-02 | Retained native Bandit baseline and source/policy hash review; its file/rule matching scope is already documented. Changed reviewed inputs require semantic re-review before updated bindings. |
| K-03 | Retained explicit docs/validation exclusion and certification limit; history separately scans commits. Evidence sources are not claimed certified. Moving retained evidence would break history and links. |
| K-04 | Retained Geiger exact local executable/hash: deliberate 15/11 repair, fail closed elsewhere; no automatic installation/fallback. |
| K-05 | Same disposition as A-07: typed adapters and declarative selection have distinct responsibilities. |
| K-06 | Retained schema compatibility metadata and reusable callable properties; unused by one adapter does not authorize removing fields from the public catalog without a migration. Long review rationale remains provenance. |
| K-07 | Legacy/current lists intentionally differ; selection compatibility is tested and documented. |
| K-08 | No separately identified K-08 finding exists in the supplied body; no invented correction. |
| K-09 | Source-bound static review hashes are an intentional fail-closed control. Fixtures now bind their own isolated bytes and reject subsequent mutation. |
| K-10 | Retained gate Clippy policy; moving policy into product Cargo manifests changes product authority beyond a scripts bug. No claim IDE/local cargo invocation applies gate flags. |
| K-11 | Retained cross-platform dependency graph; setting Linux-only targets would narrow established dependency review. |
| K-12 | Temporary advisory exceptions have an event-based review trigger (next upgrade/resumption) in dependency-policy-20261109.md; calendar expiration was not the adopted contract. No new advisory exception added. |
| K-13 | Corrected false Grype comment: scan source is dir:/project; Syft is independent inventory. Multiple vulnerability scanners remain complementary controls, not redundant proof of acceptance. |
| K-14 | Explicit residual limitation: yanked-version checking is disabled/offline and requires an authenticated index strategy; no network/index acquisition implied. |
| K-15 | No K-15 finding exists in the supplied body. |
| K-16 | Prepared annotated positive/negative fixtures for all three Rust reference rules and their alternatives, with an expectations manifest. Native detector execution remains UNVERIFIED; README distinguishes authored fixtures from exercised rules. |
| K-17 | Unsafe scanning complements compiler forbid and dependency metrics; intentionally retained. |
| K-18 | INFO findings still require review by policy; severity is not permission to ignore them. |
| K-19 | Prepared six YARA positive/negative fixtures and expected rule IDs. Bytes are hex-encoded in the repository because YARA scans all extensions; materialize only in disposable targets. Manifest/path/hex consistency checked; actual scanner matching remains UNVERIFIED, with no suppressions or efficacy claim. |
| K-20 | YARA matches are indicators, not proof of malware; names reflect check/tool/config layers. No detector broadening or suppression. |
| K-21 | Corrected own Ox rules license prose/SPDX to GPL-3.0-only per root NOTICE/security NOTICE. Adapted Ec rust.yml provenance retained separately. |
| K-22 | Excluded cache/credential/ecosystem names remain explicit source-scope limits; no unintended credential inclusion or certification claim. |
| K-23 | Local runner discovery reflects adopted installation; portable wrapper override/PATH contract retained. |
| K-24 | Mentioned only in the report introduction, with no finding body; no invented correction. |
| K-25 | Explicit coverage surface and test/tests aliases are adopted selection contracts, covered by tests. |
| K-26 | Corrected Ruff comment: line-length is configured, formatter is not a gate. No new formatter dependency or mandatory rule added. |
| K-27 | Added shape/path/digest validation for inputs/paths/databases/reviews. Unknown fields elsewhere remain compatible; not a wholly closed schema. Trivy consumer and native age checks intentionally enforce the same 120h boundary. |
| T-01 | Fixed ShellError retains returncode/stdout/stderr; rejection asserts expected code. Missing function127 differs from producer17/19. External governance consumers also migrated. |
| T-02 | Fixed assessments must be newly published by the invocation, not previous latest files. |
| T-03 | Fixed tautological assertion using an explicit inequality; controlled text mutant still exercises diagnostic rejection and is not presented as production success. |
| T-04 | Fixed preparation side-effect assertion to actual .cache/ox/security path. |
| T-05 | Fixed synthetic Machete parser tests execute independently of installed binary. |
| T-06 | Corrected test name to native adapters it actually exercises; Toolbox adapters have their own suite. |
| T-07 | Removed duplicated Python member guard and migrated consumer to production shell member validator, including escape/symlink rejection. |
| T-08 | Controlled default test environment, Git configuration isolation; explicitly opt-in real tests retain required host settings. |
| T-09 | Default subprocess timeouts added, invalid-argument tests use disposable root. Real scanner opt-in budget derives from native timeout plus 600s for wrapper cleanup. |
| T-10 | Fixed-sleep heartbeat tests retained with current timing observations; event-driven rewrite is a residual flake-maintenance opportunity, not claimed solved. |
| T-11 | Fixture static bindings regenerated only for copied fixture bytes; later mutations still fail. Production bindings receive independent semantic review. |
| T-12 | Existing TestCase fixture reuse retained; no parallel cleanup failure demonstrated. |
| T-13 | No T-13 finding exists in the supplied body. |
| T-14 | Git preparation timestamps use UTC consistently. Explicit encoding expanded where edited; no repository-wide mechanical encoding pass. |
| T-15 | Repeated tiny shims/builders retained where local to distinct boundary tests; no framework migration. |
| T-16 | Inline fixture programs remain isolated test data; no broad formatter rewrite or claim that Ruff sees embedded strings. |
| T-17 | Text mutations remain only for deliberate fault injection/contracts; main functions and member validator provide real production seams. No claim all text-dependent tests were removed. |
| T-18 | Added local CLI, inspect-data, external-output rejection, source guard, dataset lock/date/lifetime tests. Existing TERM/publication tests retained; dedicated INT/HUP and all mutation-message scenarios remain unexecuted. |
| T-19 | E501/formatter expansion not adopted merely because a line-length value exists; inaccurate comment corrected under K-26. |

## Part 2 — individual findings

Baseline inspection reproduced 13 checker failures (coordinator log
`/tmp/ox-remediation-before-check.txt`, provisional until retained with final
observations). Implementation and focused-result states below do not replace the final
independent verdict in report.md/validation.md. Each decision names affected paths.

| ID | Disposition | Decision / remaining step | Paths |
| --- | --- | --- | --- |
| T01-1 | PENDING | BS-04 requires the real detector and reviewed fixture; synthetic success cannot establish new-file B603 detection. Resume with the recorded detector control when executable. | `scripts/config/native/bandit; docs/validation/bandit-repair-20261115` |
| T01-2 | DEFERRED | Consolidating all subprocess boundaries is a test architecture change; retain source-bound review and separate scenario contracts rather than bulk rewriting callers. | `scripts/tests/support.py; scripts/config/automation.json` |
| T01-3 | REJECTED ACTION | Do not delete retained corpora to reduce volume: this request gives no cleanup permission. Curate a publication selection only when publication is requested. Size estimates are not fresh measurements. | `docs/validation` |
| T01-4 | INFORMATIONAL | Historical observation, not a current defect or new proof. Preserve the underlying record. | `claude_analysis.md` |
| T02-1 | VERIFIED (BOUNDED) | Independent six-scenario signal regressions passed for execution/publication (INT130, TERM143, HUP129). Capture/publication failure still has operational-error precedence2; no stronger guarantee claimed. | `scripts/lib/process.sh; scripts/lib/lifecycle.sh; scripts/tests/test_terminal_progress.py` |
| T02-2 | PARTIAL / DEFERRED | Shared log-name encoder removes one duplicate. Findings/count projection and checker text protocol still couple presentation; structured protocol migration is deferred with compatibility characterization required. | `scripts/lib/progress.sh; scripts/lib/logs.sh; scripts/lib/reports.sh` |
| T02-3 | IMPLEMENTED / FOCUSED CHECKS PASS | Deduplicate exact report locator; presentation/publication/governance focused group22 passed. Final checks and independent limits in report.md. | `scripts/lib/progress.sh` |
| T02-4 | IMPLEMENTED / CHECKS PASS | Stop permanent unavailable warnings/skips noise without manufacturing counts; final script suite138tests passed with1real-scanner skip. | `scripts/lib/progress.sh` |
| T02-5 | VERIFIED (BOUNDED) | Independent process-lifecycle tests passed including inherited flag without callbacks; no orphaned unsupervised callback failure. | `scripts/lib/process.sh; scripts/tests/test_process_lifecycle.py` |
| T02-6 | DOCUMENTED | terminal-progress plan records lifecycle/process ownership; AC02/06 traceability names lifecycle/T090; tasksT090 and converge now state all6UNVERIFIED and mark old approval historical. This is documentary reconciliation, not broad feature acceptance. | `sdd/features/terminal-progress/plan.md; sdd/features/terminal-progress/tasks.md; sdd/features/terminal-progress/traceability.json; sdd/features/terminal-progress/converge.md` |
| T02-7 | INFORMATIONAL | Historical observation, not a current defect or new proof. Preserve the underlying record. | `claude_analysis.md` |
| T03-1 | DEFERRED | Timing sensitivity remains explicit; event-driven heartbeat test synchronization is a separate test maintenance improvement, not proof of a production failure. | `scripts/tests/test_terminal_publication.py` |
| T03-2 | INFORMATIONAL | Historical observation, not a current defect or new proof. Preserve the underlying record. | `claude_analysis.md` |
| T04-1 | IMPLEMENTED / FOCUSED CHECKS PASS | Use ASCII label for consistent padding under C locale; included in22 focused presentation checks. | `scripts/lib/progress.sh` |
| T05-1 | REJECTED ACTION / ALTERNATIVE PENDING | Do not broaden Gitleaks allowlists or rewrite historical evidence. Use path/sha256 record shapes for new manifests; migrate current machine consumers only with compatibility coverage. | `scripts/config/native/gitleaks; docs/validation` |
| T05-2 | PENDING | Persistent wording regression remains separate from detector efficacy; do not claim the phrase tested based only on current text. | `sdd/features/history-scanner-correction` |
| T05-3 | DEFERRED | Expiry policy changes scanner acceptance and requires explicit policy/owner decisions; no automatic expiry or new fingerprints here. | `scripts/config/native/gitleaks/gitleaks-history.ignore` |
| T06-1 | PARTIAL / DEFERRED | Moving lifecycle code did not fully decouple presentation. Correct the earlier overstatement; a new structured renderer/checker protocol needs its own compatibility migration. | `scripts/lib/lifecycle.sh; scripts/lib/progress.sh; scripts/lib/reports.sh` |
| T06-2 | DOCUMENTED | terminal-progress plan records lifecycle/process ownership; AC02/06 traceability names lifecycle/T090; tasksT090 and converge now state all6UNVERIFIED and mark old approval historical. This is documentary reconciliation, not broad feature acceptance. | `sdd/features/terminal-progress/plan.md; sdd/features/terminal-progress/tasks.md; sdd/features/terminal-progress/traceability.json; sdd/features/terminal-progress/converge.md` |
| T06-3 | IMPLEMENTED / FOCUSED CHECKS PASS | UNKNOWN replaces false INPUT_INVALID fallback; production UNKNOWN regression included in final138-test script suite. Safe localized cause and raw diagnostic remain distinct. | `scripts/checks/run.sh; scripts/lib/progress.sh; scripts/tests` |
| T06-4 | DEFERRED | Library bootstrap defaults and runner catalog defaults still overlap. Removing either may change standalone source consumers; preserve overrides pending a single initialization contract. | `scripts/lib/common.sh; scripts/config/automation.json` |
| T06-5 | IMPLEMENTED / FOCUSED CHECKS PASS | Remove duplicate selection JSON calculations; script suite138tests exit0 with1real-scanner opt-out, preserving selection order. | `scripts/lib/selection.sh` |
| T06-6 | PENDING | Authored expectations are not executed rule coverage. Resume by exercising fixtures with actual YARA/Opengrep and recording exact matches; no download implied. | `scripts/tests/rules/expectations.json; scripts/tests/rules/yara; scripts/rules` |
| T06-7 | REPAIRED / NATIVE CHECK PASS | Native Toolbox ShellCheck executed offline on19files: initial34diagnostics exit1, intermediate8parser diagnostics, final exit0 with empty JSON findings. Input hashes matched live sources after the scan; raw observations retained separately. | `scripts/check.sh; scripts/config/native/shellcheck` |
| T06-8 | DEFERRED | Per-file source-copy guards cover distinct mutation windows. Further batching requires preserving race and integrity rejection and a representative measurement. | `scripts/lib/files.sh` |
| T06-9 | RETAINED CONTRACT | Shared documented aggregation precedence is retained; selection compatibility does not require keeping an erroneous outcome precedence. No legacy CLI removal. | `scripts/reports/summarize.sh; scripts/automate.sh; scripts/README.md` |
| T07-1 | IMPLEMENTED / INDEPENDENT REVIEW PASS | Use one incremental declarative ledger for new documentary successors, retaining historical protocols. Full retirement of 14 modules is deferred for compatibility. Exact-content/missing-path/downgrade rejection passed final68revision tests and independent review; whole historical-module retirement remains deferred. | `tools/governance/scripts; docs/validation/claude-remediation-20261117/document-ledger.json` |
| T07-2 | PARTIAL / FOCUSED CHECKS PASS | Separate immutable historical fixtures from live succession projection; present changes do not establish that every historical test is hermetic. | `tools/governance/tests` |
| T07-3 | PENDING | Memoization must preserve fresh mutation rejection; no speed claim without measured final checker and sensitivity tests. | `tools/governance/scripts/audit_revision.py` |
| T07-4 | IMPLEMENTED / FOCUSED CHECKS PASS | Prefer nonempty stderr, otherwise stdout; included in22 focused presentation checks. | `scripts/lib/progress.sh` |
| T07-5 | HISTORICAL CORRECTION | Prior route/ownership declarations cannot be made true retroactively. This work uses high coordination, explicit ownership and independent acceptance. | `docs/validation/claude-remediation-20261117/plan.md` |
| T08-1 | BLOCKED | Attribution of past external shared Toolbox writes cannot be reconstructed from local assertions. Resume with external audit/provenance; do not modify central files. | `docs/validation/osv-acquisition-20261116` |
| T08-2 | BLOCKED | Central reacquisition behavior is outside the writable/authorized scope; provide the malformed-timestamp case to its owner. No automatic update-db or download. | `docs/decisions/osv-acquisition-validity.md` |
| T08-3 | DEFERRED | Consumer capability/freshness negotiation is a public wrapper compatibility decision; do not add a duplicate acquisition clock contrary to the adopted ADR. | `scripts/toolbox.sh; docs/decisions/osv-acquisition-validity.md` |
| T08-4 | IMPLEMENTED / REVIEWED | Use OSV-specific diagnostic, retaining failure behavior; final governance observations in report.md. | `tools/governance/scripts/osv_acquisition_revision.py` |
| T08-5 | INFORMATIONAL | Historical observation, not a current defect or new proof. Preserve the underlying record. | `claude_analysis.md` |
| T09-1 | IMPLEMENTED / FOCUSED CHECKS PASS | Portuguese user-facing task captions now covered by final local-task integration4passes and ox-ui56passes/1helper ignored. Machine tokens stay stable. | `application/crates/ox-ui/src/local_task.rs; application/crates/ox-ui/tests/local_task.rs` |
| T09-2 | PREEXISTING REPAIR / NOT RENEWED | Report itself identifies T10 repair and role-color regression. Preserve it and include final Rust checks; do not count the older repair as newly implemented. | `application/crates/ox-ui/src/design.rs` |
| T09-3 | IMPLEMENTED / INDEPENDENT REVIEW PASS | Use one incremental declarative ledger for new documentary successors, retaining historical protocols. Full retirement of 14 modules is deferred for compatibility. Exact-content/missing-path/downgrade rejection passed final68revision tests and independent review; whole historical-module retirement remains deferred. | `tools/governance/scripts; docs/validation/claude-remediation-20261117/document-ledger.json` |
| T09-4 | IMPLEMENTED / REVIEWED | Replace Ox-specific dependency assertion with generic version/features/platform verification requirement; exact preimage and next identity retained. Independent review includes the four skill corrections. | `.codex/skills/iced-engineering/SKILL.md; skill-portability-inputs.json` |
| T09-5 | IMPLEMENTED (BOUNDED) | Repair software-delivery grammar and make Rust example command relative to installed skill. Both editions2021/2024 rustdoc checks passed3examples each. No blanket claim every repeated phrase removed. Recovery retention was preexisting. | `.codex/skills/software-delivery/SKILL.md; .codex/skills/rust/references/examples.md; skill-checks.md` |
| T10-1 | IMPLEMENTED / FOCUSED CHECKS PASS | Portuguese user-facing task captions now covered by final local-task integration4passes and ox-ui56passes/1helper ignored. Machine tokens stay stable. | `application/crates/ox-ui/src/local_task.rs; application/crates/ox-ui/tests/local_task.rs` |
| T10-2 | IMPLEMENTED / INDEPENDENT REVIEW PASS | Use one incremental declarative ledger for new documentary successors, retaining historical protocols. Full retirement of 14 modules is deferred for compatibility. Exact-content/missing-path/downgrade rejection passed final68revision tests and independent review; whole historical-module retirement remains deferred. | `tools/governance/scripts; docs/validation/claude-remediation-20261117/document-ledger.json` |
| T10-3 | DOCUMENTED | Current authorized scope is recorded in project.md and authenticated by terminal successor; older omission remains historical. | `sdd/project.md` |
| T10-4 | CORRECTED BY ADDENDUM | Historical wording is retained; current report adds legible editorial correction rather than silently rewriting past observations. | `docs/validation/audit-followup-20261117/report.md; report.md` |
| T11-1 | REPAIRED / CHECKS PASS | Baseline checker exit1 reproduced with 13 FAILs for AGENTS/workflow/project/prompt. Exact documentary succession repaired; final check-ox exit0 and68revision tests passed, with independent targeted validation. | `AGENTS.md; sdd/workflow.md; sdd/project.md; .codex/skills/prompt/SKILL.md; tools/governance` |
| T11-2 | IMPLEMENTED / CHECKS PASS | Include the linked append-only log in governance copy selection and test independent-copy links. Portable-core status needs explicit reviewed successor. | `tools/governance; task_finalizada.md; sdd/workflow.md` |
| T11-3 | HISTORICAL CORRECTION | Prior route/ownership declarations cannot be made true retroactively. This work uses high coordination, explicit ownership and independent acceptance. | `docs/validation/claude-remediation-20261117/plan.md` |
| T11-4 | REJECTED ACTION | Explicit user instruction requires preservation of every prior byte. A recommendation cannot authorize redaction. If an actual disclosure occurs, obtain a specific authorized incident procedure. | `AGENTS.md; task_finalizada.md` |
| T11-5 | RETAINED LIMITATION | Do not fabricate historical task execution or backfill as if contemporaneous. This entry records current work; append-only policy is not claimed OS enforcement. | `task_finalizada.md` |
| T12-1 | IMPLEMENTED / FOCUSED CHECKS PASS | Actual PNG decode/dimension regressions included in56passing UI unit tests; image version pinned to already locked version without acquisition. | `application/crates/ox-ui/src/desktop/identity.rs; application/crates/ox-ui/Cargo.toml; application/Cargo.lock` |
| T12-2 | IMPLEMENTED / FOCUSED CHECKS PASS | Actual PNG decode/dimension regressions included in56passing UI unit tests; image version pinned to already locked version without acquisition. | `application/crates/ox-ui/src/desktop/identity.rs; application/crates/ox-ui/Cargo.toml; application/Cargo.lock` |
| T12-3 | REJECTED ACTION | Unreferenced supplied identity artwork remains retained; deleting it is unnecessary for defect recovery and not authorized cleanup. | `application/crates/ox-ui/assets/identity` |
| T13-1 | HISTORICAL CORRECTION | Current editing cannot prove the older design.rs modification claim. Preserve snapshot and disclose attribution limitation. | `docs/validation/enterprise-visual-20261116` |
| T13-2 | DEFERRED | Declarative control/sidebar/settings extraction is a broad UI refactor. Preserve IDs while fixing actual event/focus transitions; migrate tables with its own behavioral characterization. | `application/crates/ox-ui/src/desktop.rs; application/crates/ox-ui/src/desktop/views.rs` |
| T13-3 | IMPLEMENTED / VERIFIED (BOUNDED) | Remove IBM Plex footer branding, preserve theme label. Root formatting exit0; independent validator reran ox-ui library56passed1helper ignored after edit. | `application/crates/ox-ui/src/desktop/views.rs` |
| T13-4 | REJECTED ACTION | Do not delete retained corpora to reduce volume: this request gives no cleanup permission. Curate a publication selection only when publication is requested. Size estimates are not fresh measurements. | `docs/validation` |
| T14-1 | IMPLEMENTED / FOCUSED CHECKS PASS | Drag-only subscription and testable event mapper with shortcut capture/surface gating and unfocus cancellation; final UI unit56passes1helper ignored and build/clippy/fmt exit0. No measured redraw improvement or native input claim. | `application/crates/ox-ui/src/desktop.rs` |
| T14-2 | IMPLEMENTED / FOCUSED CHECKS PASS | Drag-only subscription and testable event mapper with shortcut capture/surface gating and unfocus cancellation; final UI unit56passes1helper ignored and build/clippy/fmt exit0. No measured redraw improvement or native input claim. | `application/crates/ox-ui/src/desktop.rs` |
| T14-3 | DEFERRED | Declarative control/sidebar/settings extraction is a broad UI refactor. Preserve IDs while fixing actual event/focus transitions; migrate tables with its own behavioral characterization. | `application/crates/ox-ui/src/desktop.rs; application/crates/ox-ui/src/desktop/views.rs` |
| T14-4 | IMPLEMENTED / FOCUSED CHECKS PASS | Drag-only subscription and testable event mapper with shortcut capture/surface gating and unfocus cancellation; final UI unit56passes1helper ignored and build/clippy/fmt exit0. No measured redraw improvement or native input claim. | `application/crates/ox-ui/src/desktop.rs` |
| T14-5 | PARTIAL / DEFERRED | Dead content_visible local removed in touched code. Minimum-window and tooltip-delay design choices remain deferred until explicit layout/native characterization; no native acceptance claimed. | `application/crates/ox-ui/src/desktop.rs; DESIGN.md` |
| T14-6 | REJECTED ACTION | Do not delete retained corpora to reduce volume: this request gives no cleanup permission. Curate a publication selection only when publication is requested. Size estimates are not fresh measurements. | `docs/validation` |
| T15-1 | VERIFIED (BOUNDED) | Independent ox-ui library56passed1helper ignored exercises real FolderChosen error, manual field availability/focus, selected path and parent-picker recovery. Native GUI remains unverified. | `application/crates/ox-ui/src/desktop.rs; application/crates/ox-ui/src/desktop/views.rs` |
| T15-2 | DEFERRED | Current guarded unreachable arms are maintenance risk rather than reproduced panic. Consolidate settings drawing only with exhaustive icon behavior checks. | `application/crates/ox-ui/src/desktop/icons.rs` |
| T15-3 | DEFERRED | Icon differentiation and regional traversal-order redesign need explicit UX composition and native characterization. Recovery/focus repair does not claim these design decisions solved. | `application/crates/ox-ui/src/desktop.rs; application/crates/ox-ui/src/desktop/icons.rs; docs/design/surfaces.md` |
| T15-4 | DEFERRED | Icon differentiation and regional traversal-order redesign need explicit UX composition and native characterization. Recovery/focus repair does not claim these design decisions solved. | `application/crates/ox-ui/src/desktop.rs; application/crates/ox-ui/src/desktop/icons.rs; docs/design/surfaces.md` |
| T16-1 | IMPLEMENTED / FOCUSED CHECKS PASS | Settings IDs/reveal and welcome-sidebar-specific scroller routing are tested in final56passing UI unit tests. Actual640x480 native focus visibility remains unverified. | `application/crates/ox-ui/src/desktop.rs; application/crates/ox-ui/src/desktop/views.rs` |
| T16-2 | IMPLEMENTED / FOCUSED CHECKS PASS | Settings IDs/reveal and welcome-sidebar-specific scroller routing are tested in final56passing UI unit tests. Actual640x480 native focus visibility remains unverified. | `application/crates/ox-ui/src/desktop.rs; application/crates/ox-ui/src/desktop/views.rs` |
| T16-3 | DEFERRED | Toolbar immediate-apply versus saved preference semantics, origin-none behavior and title terminology need a coherent settings contract/native scenarios; do not change preference semantics incidentally to focus recovery. | `application/crates/ox-ui/src/desktop.rs; application/crates/ox-ui/src/desktop/views.rs` |
| T16-4 | DEFERRED | Toolbar immediate-apply versus saved preference semantics, origin-none behavior and title terminology need a coherent settings contract/native scenarios; do not change preference semantics incidentally to focus recovery. | `application/crates/ox-ui/src/desktop.rs; application/crates/ox-ui/src/desktop/views.rs` |
| T17-1 | PARTIAL / FOCUSED CHECKS PASS | Separate immutable historical fixtures from live succession projection; present changes do not establish that every historical test is hermetic. | `tools/governance/tests` |
| T17-2 | IMPLEMENTED / FOCUSED CHECKS PASS | Assert baseline clean and require path-specific mutation diagnostics in visual/windows successor tests. Independent review found initial NameError, corrected before final group7visual+5windows passed. | `tools/governance/tests/test_visual_skill_revision.py; tools/governance/tests/test_windows_design_revision.py` |
| T17-3 | IMPLEMENTED / REVIEWED | Horizontal fixture1200-240-280-24=656 width; vertical800-48=752 height. No consumer-specific fact or native acceptance inferred. Exact bytes recorded. | `.codex/skills/iced-engineering/references/native-visual-contract.md; skill-portability-inputs.json` |
| T17-4 | HISTORICAL CORRECTION | Current scope is recorded; cannot retroactively turn an absent earlier project entry into contemporaneous evidence. Retain inventory; no claim its size is newly measured. | `sdd/project.md; docs/validation/visual-skills-20261116` |
| T18-1 | DOCUMENTED / REVIEWED | Current radius/chrome/inspector targets and welcome sidebar rules reconciled with code, superseded prose marked historical. Native geometry not re-observed. | `DESIGN.md; docs/design/surfaces.md` |
| T18-2 | DOCUMENTED / REVIEWED | Current radius/chrome/inspector targets and welcome sidebar rules reconciled with code, superseded prose marked historical. Native geometry not re-observed. | `DESIGN.md; docs/design/surfaces.md` |
| T18-3 | RETAINED / DEFERRED | Cross-references and generic skill closure wording are not independently defective behavior. Further authority consolidation must avoid deleting consumer instructions. | `DESIGN.md; AGENTS.md; .codex/skills/prompt/SKILL.md` |
| T18-4 | PENDING | Do not invent license attribution. Verify upstream license and provenance before changing NOTICE; alternatively produce a derived path list with retained source hash under reviewed retention policy. | `NOTICE; docs/validation/windows-design-20261117` |
| T18-5 | RETAINED LIMITATION | Missing versioned web snapshots and independent historical scenario observation cannot be manufactured. Current independent contexts establish only this work; no historical renewal. | `docs/validation/windows-design-20261117` |
| T19-1 | REPAIRED / CHECKS PASS | Baseline checker exit1 reproduced with 13 FAILs for AGENTS/workflow/project/prompt. Exact documentary succession repaired; final check-ox exit0 and68revision tests passed, with independent targeted validation. | `AGENTS.md; sdd/workflow.md; sdd/project.md; .codex/skills/prompt/SKILL.md; tools/governance` |
| T19-2 | RETAINED / DEFERRED | Cross-references and generic skill closure wording are not independently defective behavior. Further authority consolidation must avoid deleting consumer instructions. | `DESIGN.md; AGENTS.md; .codex/skills/prompt/SKILL.md` |
| T19-3 | INFORMATIONAL | Historical observation, not a current defect or new proof. Preserve the underlying record. | `claude_analysis.md` |

## Cross-cutting recommendations and final priority table

| Recommendation | Disposition / trace |
| --- | --- |
| P0 chooser fallback | T15-1; transition regression and final Rust evidence required. |
| P0 restore checker and governance suite | T11-1/2, T19-1; include independent-copy regressions, not only live-tree exit. |
| P0 require checker for authority/SDD/skill changes | Current closure successor must name the focused checker; no full scanner run implied. |
| P1 full replacement of 14 revision modules | Incremental single ledger selected; historical module retirement deferred for compatibility (T07-1). |
| P1 exact signal codes | T02-1/5; all three signals and raw child exit attribution. |
| P1 drag-only mouse subscription | T14-1/2/4. |
| P1 focus reveal in correct scrollables | T16-1/2; native viewport acceptance remains separately unverified. |
| P1 path/hash serialization or allowlist | Prefer typed records for new manifests; reject broader suppression and historical rewrites (T05-1). |
| P1 pt-BR local task messages | T09-1/T10-1. |
| P2 extract sidebar/settings/control tables | Deferred broad refactor; no demonstrated need to replace all control IDs for bounded repairs. |
| P2 unify native harnesses / replace obsolete X11 tests | Deferred separate native-test migration; do not enable stale coordinates or claim existing ignored tests exercised. |
| P2 terminal-progress artifacts / renderer split | T02-6/T06-1/2; documentary reconciliation and residual coupling distinguished. |
| P2 DESIGN/current surface rules | T18-1/2. |
| P2 redact append-only history / distribute task log | Redaction conflicts with explicit instruction and is rejected; include linked log in export (T11-2/4). |
| P3 delete old corpora / absolute paths | Cleanup not authorized; no corpus deletion (T01-3/T13-4/T14-6). |
| P3 BS-04 / ShellCheck / PNG / image pin | Each has separate detector/build evidence: T01-1,T06-7,T12-1/2. |
| P3 portable skills / grammar | T09-4/5,T17-3; local corrections must receive documentary succession checks. |
| Cross-cutting weak test oracles | T15-1,T02-1,T14-4,T17-2; assert actual transitions, exact exits and diagnostic deltas. |
| Cross-cutting independent acceptance | Actual new context identifiers and observations required in review/validation records; old narratives are not new proof. |
| Cross-cutting evidence volume / suppression growth | Preserve retained history and scanner coverage; no invented overall acceptance or efficacy. |
| Zero approved criteria in audit snapshot | Historical count only; final feature states must come from current envelopes, never task completion checkboxes. |

## Completion limit

This is an exhaustive disposition index, not a declaration that every proposed
refactor or remaining defect has been resolved. The execution remains incomplete
where mandatory verified corrections are pending. The final report must preserve
those limits, give the exact checks performed and distinguish compatible deferred
architecture choices from unresolved functional defects.


## Part 3 reassessment — 2026-11-18

The earlier T09-3 and T10-2 rows above are historical implementation/review
claims for the 17 November slice. Part 3 demonstrated that the live-document
cause remained; they do not establish resolution of R3-3. Current disposition
for both is **REOPENED / VERIFICATION IN PROGRESS**. The section-bound authority
repair, independent review and complete-suite outcomes are tracked in
[the R3 record](../r3-remediation-20261118/spec.md). No final acceptance is claimed.
