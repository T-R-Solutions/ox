# Independent criterion validation — 2026-11-17

Validator context: `/root/correcoes_analise/validacao`, independent of implementation
and review. Ownership was limited to this new record; no implementation, policy,
requirement or gate input was changed by the validator. Read AGENTS, codex-agents,
workflow/evidence, constitution, architecture, project authorization, shell ADR,
local-artifacts, the feature contract and current implementation/oracles.

## Verdict by criterion

| Criterion | Verdict | Evidence and limit |
| --- | --- | --- |
| AC-01 | INCONCLUSIVE, preserved | Earlier reference/migration acceptance was not reobserved; report-ID coverage does not renew it. |
| AC-02 | INCONCLUSIVE, preserved | Bounded catalog/adapter inspection does not renew complete centralization acceptance. |
| AC-03 | INCONCLUSIVE, preserved | Current unit regressions do not renew the broad historical operational observation. |
| AC-04 | INCONCLUSIVE, preserved | Current selection/CLI regressions support the repair, not a new complete Ec parity comparison. |
| AC-05 | INCONCLUSIVE, preserved | No complete native analyzer policy/detection reevaluation. |
| AC-06 | INCONCLUSIVE, preserved | Production member-guard and selection tests are not a new qualified Geiger/native execution. |
| AC-07 | INCONCLUSIVE, preserved | Documentary successor tests do not constitute new independent export acceptance of all current bindings. |
| AC-08 | APPROVED, bounded manual criterion verdict | Confirmed defects have current behavioral evidence, report findings have explicit dispositions, independent review has no open findings, and unexecuted operational checks remain explicit. This is not whole-feature automated approval or scanner/product certification. |

AC-08 was examined by these components:

| Component | Observation |
| --- | --- |
| Report completeness | Compared source IDs with matrix rows: 87 mentioned IDs, 89 rows, no missing ID. K-15/T-13 explicitly record absence; K-08/K-24 are not invented findings. Read the dispositions against relevant code and authorities. |
| Observable corrections | Independently ran all 15 focused regressions; inspected summary records, aggregate precedence, Deny raw-mask normalization, environment defaults, selection baseline, CLI validation, structured reasons, typed argv, canonical manifests and path guards. Tests exercise actual entries/functions and independent expected values. |
| Error and test sensitivity | First full log retains 17 JSON-oracle consumer errors. The shell branch now catches ShellError and checks 1/5 while the Python parser remains independent. Independently reran that oracle. Original-defect sensitivity log shows four expected failures against preimages (environment, Deny, local CLI, summary), supporting regression discrimination. |
| Consumer and lifecycle regressions | Final full log: 132 tests, OK, one explicitly opt-in real-scanner skip. Reviewed cancellation/publication, current-assessment identity, production Geiger member validation and external consumer evidence. Review's corrected import/consumer/timeout issues remain recorded. |
| Policy preservation | Compared catalog against captured preimage: only 17 existing static bindings changed. Checked each old/new digest and current file; Bandit baseline unchanged. Native Grype/Ruff policy changes are comments only. Narrow exceptions, offline Cargo arguments, raw diagnostics and fail-closed gates remain. |
| Documentary succession | Independently ran six successor tests. Inspected exact two-document scope, authenticated preimages, unknown/downgrade and symlink rejection. Existing historical acceptance is not renewed by this mapping. |
| Documentation and residual work | Final tasks/report and scripts/rules/fixture guides distinguish prepared fixtures from native matching. E-11 cleanup claim is correctly limited to automate.sh; standalone early-init cleanup is not newly certified. Reviewed closure disposition is concrete. |

## Commands and observations

Executed independently from the Ox root:

| Command/method | Exit/result |
| --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s scripts/tests -p test_claude_regressions.py -v` | 0; 15 tests, 1.920s. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools/governance/tests -p test_claude_analysis_revision.py -v` | 0; six tests, 0.018s. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s scripts/tests -p test_json_guard.py -v` | 0; one test, 0.374s after consumer correction. |
| `bash scripts/check.sh` | 0 on stabilized scripts; syntax only. |
| Python read-only manifest comparison | 0; all 135 unique paths in inputs.json exist as regular nonsymlink files and current SHA-256 equals recorded SHA-256. |
| Python read-only catalog comparison against recovery preimage | 0; replacing exactly the 17 listed old static hashes with their observed new hashes makes the preimage catalog equal the current catalog; baseline hash agrees. |
| `PYTHONDONTWRITEBYTECODE=1 python3 sdd/tools/validate.py --root . --features sdd/features --feature scripts-centralization --require-approved --require-fresh --check-convergence` | 1, before applying this verdict: exactly AC-01–07 INCONCLUSIVE and AC-08 UNVERIFIED. No per-criterion selection or unrelated global feature approval requested. |

Inspected executor logs rather than duplicating the long suite: scripts-tests-final.log
records 132 tests in 176.790s, OK (skipped=1); post-review-tests.log records five
catalog/static-binding rejection tests in 4.852s, OK. The broad suite preceded the
binding update; those affected checks were rerun afterward. scripts-tests.log
preserves the failed predecessor run. Original-defect-sensitivity.log intentionally
records four failures, not a production pass. Review and coordinator command/exit
claims were checked against these actual outputs and code; agreement alone was
not used as proof.

## Initial observed input identities (retained)

The complete enumerated input set is inputs.json, SHA-256
`97bb74cd6b46da6b50bcb73d4de543d7db870fa0ff269adde549668b832f95cd`.
This includes the four feature contract files, implementation, oracles and
configuration. Its 135 bindings were independently compared after the coordinator
declared those bytes stable. Merely matching hashes does not authenticate execution.

| Artifact | SHA-256 |
| --- | --- |
| source-analysis.md.bin (same bytes as claude_analisys.md) | 1859924f154ddb164e08468a683f188e32035fc42870faeb8d20b22e01a92481 |
| report.md | 7d68eb4cad2b53a667921144d4bbcf0a44e348c58fe8cc9bed6797ed42dc947d |
| review.md | ffd651b6d3892b8e7da28ece8f02631c9d9561f31d2b78ebe7db4e4ef8e52774 |
| scripts-tests-final.log | 4652bad82f844ce51933ae24b9a09e49de29bcc8bd370200e4f453345eeb28bf |
| scripts-tests.log | 976d3e561cde146e0b494543e2331cdd3e915ee65788e2404b7050d7e9710b6a |
| post-review-tests.log | 4944a8cb8da05d76cd2050edbf264821a74eb243b1fcf54891871f7f637d0a4d |
| original-defect-sensitivity.log | 88a8b549ad882b49820c7ab0a316b88a440ecc73beb8e43b21806409c974ee58 |
| static-review-update.json | eff95ca61c60cc930147caa702cdd6f76cb729226006d2a0a6230a239655aba8 |

## Current documentary successor observation

Before evidence publication, the coordinator corrected the benchmark description
from 68 to 72 bytes per file in manifest-benchmark.json and report.md. Its explicit
metadata_correction preserves the earlier error. I independently checked that
`len(b'bounded benchmark\n' * 4) == 72`, inspected the corrected description and
confirmed the original six timing samples and content identities remain unchanged.
This is a description correction, not a new benchmark observation. It does not
affect the behavioral tests or the bounded AC-08 verdict above.

Recompared all 135 current manifest bindings (exit 0). The current identities
supersede only the corresponding initial identities above, which remain recorded:

| Artifact | Current SHA-256 |
| --- | --- |
| inputs.json | 3abf884e50d487684cebf9b518585af48e58c90a5eeb6423756a08e5e4cb2a43 |
| report.md | 63dc48d4655fc3c8ccae4c7bdb9867721c272181da714ce7468203b9c506ff95 |
| manifest-benchmark.json | 371a191dc35254f81cf3d1d9c9695fd30ffb3ff0bf61f0456c4c3e8710dc2aff |

## Limits and resumption

ShellCheck central did not execute: its execution-record write was denied and the
escalation request was aborted. Full scanner execution, new rules' native matching,
INT/HUP-specific acceptance and comprehensive mutation-message scenarios are not
proved. The small manifest benchmark is not a full-run performance claim. Existing
policy limits and residual dispositions remain as documented; no downloads,
installation, commit or publication were authorized by this verdict.

The coordinator may now bind this observation in schema 2 and project AC-08 into
converge.md, then rerun the same explicitly selected whole-feature checker. AC-01–07
must still prevent whole-feature approval. Record the post-verdict command/output;
do not hide those gates or promote them from this bounded repair. Reopen affected
observations if any bound inputs change. Operational gaps resume only with the
required tool capability/authorization and actual detector or signal observations;
historical criteria require their own current evidence, not refreshed old hashes.
