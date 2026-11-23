# Review and corrections of claude_analisys.md — 2026-11-17

## Authorized scope and criteria

The maintainer requested analysis of the report and implementation of corrections.
This continuation of scripts-centralization T008 covers confirmed shell-runner,
reporting, selection and test-oracle defects. Preserve existing uncommitted work,
public compatibility, scanner coverage, raw diagnostics and fail-closed boundaries.
No commit, publication, download, central maintenance or complete scanner run.

AC-08: the report receives an explicit disposition; confirmed defects are repaired
and tested against their observable contract. Security, compatibility and storage
recommendations are decided against existing authorities, not adopted as permissions.
Independent review and validation judge the final changes; synthetic adapter tests
establish contracts, not real scanner effectiveness.

## Route and ownership

Full route/high coordination: changes affect gates, evidence and integrity.
Root delegates to ec_orquestrador_alta; coordinator owns production scripts,
automation catalog and common documentation. ec_implementador owns existing
scripts/tests Python files; coordinator owns test_claude_regressions.py. Independent
ec_revisor and ec_validador_alta receive fresh contexts after implementation.
Root owns bounded corrections in rules documentation/YARA license marker and native
Grype/Ruff comments. No overlapping writes are authorized.

Observed capabilities: named-profile spawn succeeded for coordinator and implementer;
message return is functional. Host advertises four total slots, list/status and
interrupt; no close operation. Slot reuse remains to be observed before depending
on it. All writers preserve existing edits. Source preimages and SHA-256 manifest:
/tmp/ox-claude-corrections-20261117 (local recovery, not acceptance evidence).

## Decisions and limitations

Implementation and focused independent review are recorded below. Final criterion
validation remains separate. Historical observations retain their original hashes;
full native/scanner acceptance is not claimed.

## Disposition of the supplied analysis

Source: `claude_analisys.md`, preserved without edits. The original mixes confirmed
bugs, estimates and design alternatives. “Retained” below is a reasoned decision,
not a claim that the concern is nonexistent. “Limited” identifies the exact residual
scope; it is not certification of unexecuted scanner behavior.

| ID | Disposition against observed code and contracts |
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

The numbered formatting recommendation is not adopted: adding shfmt or a new
formatter gate changes tooling and acceptance dependencies; no installation was
requested. Existing syntax checks remain mandatory for this change.

## Verification and observed limitations

- Focused new regressions: 15 tests passed after batching, covering current-run
  reports, code precedence, explicit environment values, selection omissions,
  CLI rejection, Deny masks, structured failures, schema rejection, reason-code
  redaction, argv boundaries, real inspect/output guards and canonical manifests.
- The independent reviewer exercised 7 capture/status, 4 lifecycle/TTY/publication,
  13 documentary gate and 4 governance consumer tests successfully; initial missing
  `os` import and ShellError consumer failures were found and corrected.
- Root exercised new documentary successor 6, audit 7 and OSV 6 tests successfully;
  initial rejection-order incompatibilities were corrected without allowing unknown
  content. Existing successor registries remain byte-for-byte unchanged.
- Final scripts unit suite: 132 tests in 176.790s, exit 0, one explicit opt-in scanner
  skip. `scripts-tests-final.log` preserves output. The first full run had 17 errors
  in one unmigrated JSON consumer; `scripts-tests.log` preserves that failure.
  After correction the full suite passed. Post-review catalog/static-rejection
  tests: 5 passed in 4.852s, exit 0, against updated semantic bindings.
- Four current behavioral regressions failed on the preserved original scripts
  (environment, Deny mask, local CLI, real result summary), exactly as expected;
  `original-defect-sensitivity.log` preserves exit 1/four failures. Current tests
  pass. This is defect sensitivity, not an invented production run.
- Independent final review has no open implementation findings; `review.md`
  records the read-only review result and identities. Final criterion validation
  is separate in `validation.md`; evidence.json/converge.md own acceptance states.
- A bounded tree_identity comparison measured 80 files × 72 bytes, three observations
  per version, identical canonical digest. Before:0.292–0.298s; after:0.016–0.017s.
  `manifest-benchmark.json` records method/inputs; this is not a full-run estimate.
- ShellCheck through the installed central Toolbox was attempted against a private
  temporary script copy. The sandbox rejected its central execution-record write.
  Escalation approval was pending and then aborted; ShellCheck did not execute.
  No download, installation or native scanner acceptance is claimed.

## Documentary closure disposition

Reviewed/updated: scripts/tests/rules/README.md and expectations/fixture inventory,
scripts/README.md (runner outcomes, ownership, summary and CLI),
scripts/rules/README.md and own YARA SPDX (provenance), native Grype/Ruff comments,
sdd/project.md authorization, scripts-centralization spec/plan/tasks/traceability/
evidence/converge and this report. Constitution, architecture, local-artifacts,
script migration ADRs, root NOTICE and dependency-policy were reviewed; their
product/coverage/storage/exception authorities remain intact. New documentary
successor binds exactly README/project to authenticated preimages and rejects
unknown/downgraded bytes. Historical scanner/evidence hashes are not refreshed.

All nine feature envelopes referencing scripts had no active `.evidence` records
for those paths at entry; their script references were already historical. They
remain historical. This task adds only its own current observations; broad earlier
scripts-centralization AC01–07 remain INCONCLUSIVE unless independently reexamined.

## Reproduction and final boundary

Executed from the Ox root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s scripts/tests -v
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=scripts/tests python3 -m unittest test_catalog test_backends.Backends.test_static_review_rejects_changed_source_and_policy test_backends.Backends.test_static_review_missing_registry_is_rejected -v
bash scripts/check.sh
```

The full unit run preceded the 17 binding update; the affected five tests were
reexecuted afterward, and the independent validator compared each binding to the
reviewed bytes. No historical execution was renewed by a hash change. Current
inputs are enumerated in inputs.json; the independent validation record binds
its final verdict. Whole-feature approval remains unavailable while AC01–07 are
INCONCLUSIVE; passing structure/freshness alone is not product acceptance.
