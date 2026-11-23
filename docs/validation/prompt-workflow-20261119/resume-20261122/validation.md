# Independent validation — 2026-11-22

Task: PROMPT-WORKFLOW-20261119, resumption revision 2. Validator operates in a separate context and writes only this verdict and validation-inputs.json. No implementation, requirements or gate inputs were changed.

## Route and observed evidence

Full route, manual acceptance expressly selected by spec.md under sdd/evidence.md. No automated feature is being accepted: `--features/--feature --require-approved --require-fresh` is not applicable to this manual task; unrelated feature approval is not required. Check-ox and the complete governance unittest suite remain mandatory under AC-05 and workflow. Full scanners are outside this request.

Manual method: read current AGENTS, workflow, evidence, agent procedure, constitution, architecture, project, prompt skill, task spec/plan/tasks/review/scenarios, ADR, ledger section parser/validation and six focused test oracles. Compare current bytes with observed-inputs.json using Python SHA-256 (exit 0). All six recorded inputs match. The review of 19 November remains relevant for its five reviewed inputs; project was only captured by the coordinator and is not promoted to independently reviewed historical evidence. Current independent semantic inspection additionally covers project context. Exact observed versions and pre-closure log prefixes are in validation-inputs.json.

The focused tests actually reject missing, changed, duplicate and unknown prompt sections, previous authority downgrade and changed protected sections. They preserve the historical terminal digest. Their oracle checks contract integrity, not prompt execution by models. The recorded independent run of six tests on 19 November is reused only for unchanged inputs; global checks are pending below.

## Criterion verdicts before final records

| Criterion | State | Method and result | Limitation / resumption |
| --- | --- | --- | --- |
| AC-01 | APPROVED | Manual reading of AGENTS entry and workflow construct/persist: mandatory prompt skill, exactly five named sections, append before described execution. Skill selection remains coherent because Ox explicitly requests prompt creation. | Instruction adoption only; no universal future client compliance claim. |
| AC-02 | APPROVED | Workflow explicitly accounts for analysis, planning, execution, tests and validation; proportional inspection for prose; append-only history with stable IDs and revisions. Current planning log contains original entry, analysis, plan and resumption revision. | Semantic contract and inspected local record; no runtime interception. |
| AC-03 | INCONCLUSIVE | Workflow requires post-validation outcome, unfinished items/reasons, documentation disposition and separate root activity record. Existing task_completed entry closes only the status question. | Root must append this task outcome and activity record after validation; verify captured prefixes and final content before closure. |
| AC-04 | APPROVED | Independently compare all 12 scenario rows with workflow clauses: ordinary/read-only/prompt-only, narrowing correction, resume, status, delegation, forbidden writes, missing files, concurrent history, missing validation and untrusted source. Required outcomes agree. Original request remains authority; dependent persistence blocks on unsafe paths or denial. | Semantic scenario inspection, not twelve observed model invocations or OS isolation. |
| AC-05 | INCONCLUSIVE | Historical independent review has matching implementation inputs; present validation is independent. Mandatory check-ox and whole governance suite results are not yet final in this observation. | Require raw outputs, final exits, absence/disposition of failures/skips, stable inputs and final closure observation. |

## Critical risks and documentary disposition

No blocking contract contradiction found. Explicit limitations prevent false approval from filenames, historical hashes, agent agreement or structural exits. The ledger remains a code-review trust boundary: hardcoded section hashes alone are not an independent semantic oracle. Here semantic inspection of requirements/consumers and negative test design provides the separate check. Generated instructions cannot expand authority; delegated messages do not recurse into new user tasks. Prefix preservation is checked against captured bytes after closure, not inferred from append-only prose.

Reviewed documentary paths: AGENTS.md, sdd/workflow.md, sdd/evidence.md, docs/development/codex-agents.md, docs/constitution.md, docs/architecture/context.md, sdd/project.md, .codex/skills/prompt/SKILL.md, task spec/plan/tasks/review/scenarios and prompt-execution-contract ADR. No authority edit is needed from this inspection; only current evidence and closure records remain. Existing results of failed/interrupted runs must stay historical.

Overall: INCONCLUSIVE until AC-03/AC-05 receive final evidence. Return missing evidence to coordinator; no criterion is reduced. Reevaluate only changed inputs and newly supplied closure/global observations.

## Check-ox observation

Inspected check-ox.result.json, check-ox.stdout.log and empty check-ox.stderr.log. Command: `PYTHONDONTWRITEBYTECODE=1 python3 tools/governance/scripts/check-ox.py`; exit 0; 146.343 seconds; runner reports no changed inputs. Stdout reports profile/catalog/bridges/skill copies/SDD/normative IDs/links/archive inspection PASS and explicitly no product acceptance. This satisfies the check-ox portion of AC-05, not the remaining full suite or closure.

## Independent continuation — 23 November 2026 UTC

Inspected complete raw governance stderr/stdout, terminal runner metadata and suite-coverage.json. Independently rediscovered tests without executing them and compared their ordered IDs against raw stderr. Result: 296 expected and 296 observed executions in identical order; all 296 result chunks finish `ok`; no FAIL, ERROR, skip, expected failure or unexpected success. All six prompt-contract cases are present. Nine ReadmeImportTests are discovered twice because test_project_revision imports their class; thus there are 287 unique IDs, not 296 unique tests. The loader code and import explain this duplication without evidence of an omitted test.

Mandatory command: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools/governance/tests -v`. Runner exit 0; raw terminal `Ran 296 tests in 30259.185s`, `OK`. The duplicate ZIP-name warning is retained inside a package rejection case that finishes `ok`. Independently recomputed all raw hashes recorded by suite-coverage.json and all inputs in inputs-before.json and historical observed-inputs.json: no mismatch. Independent inspection command exited 0. No tests were rerun by the validator.

Read report.md and the appended plan/tasks continuation. They preserve prior claims, distinguish instruction adoption from universal compliance, identify command evidence and remaining AC-03 closure, and retain scope exclusions. Their documentary changes do not alter implementation, criteria or test oracles; their new observed bytes are recorded in validation-inputs.json under subsequent_observations. A proportional check-ox of new documentation is still planned by the coordinator; its result should be inspected before final closure.

| Criterion | Current state | Basis / remaining condition |
| --- | --- | --- |
| AC-01 | APPROVED | Prior semantic inspection remains valid; bound authority inputs unchanged. |
| AC-02 | APPROVED | Prior semantic inspection remains valid; appended plan/tasks agree with actual verification. |
| AC-03 | INCONCLUSIVE | Root outcome/activity records for this task still require actual append, followed by independent prefix/content verification. |
| AC-04 | APPROVED | Prior scenario inspection remains valid; no scope or permission changes. |
| AC-05 | APPROVED | Independent historical review with unchanged inputs, present independent validation, check-ox exit 0 and complete governance suite exit 0 with independently verified exhaustive coverage and raw results. |

No blocking implementation finding. Root may now append the post-validation task outcome and activity records under existing authorization. The records must accurately state the candidate's accepted criteria and pending AC-03 observation; this permission to proceed is not a substitute for that observation. Final task closure remains pending AC-03 plus the announced proportional documentation check. Earlier INCONCLUSIVE observations and failed/interrupted attempts remain historical.

## Final independent verdict — 23 November 2026 UTC

AC-03 closure method: read actual new bytes in .ai/task_planning.md, .ai/task_completed.md and task_finalizada.md, and recompute SHA-256 over each original prefix captured before closure in validation-inputs.json. All three original prefixes are intact. Appends observed: planning 1285 bytes, completed 2744 bytes, root activity 2744 bytes. The outcome/activity entries identify PROMPT-WORKFLOW-20261119 revision 2, actual implementation paths and work, command results, independent validation, documentation disposition, scope limitations, and the then-pending final AC-03 inspection. They follow the candidate validation and do not claim that the pending inspection had already happened. Their statement that no implementation repair or full-suite test remains agrees with observed evidence. The planning continuation links the outcome to this task. This directly supports AC-03; filenames or writer declarations were not used as proof.

Proportional documentation check inspected after terminal completion: `PYTHONDONTWRITEBYTECODE=1 python3 tools/governance/scripts/check-ox.py`, exit 0, 128.725844 seconds; stdout PASS for local profile, catalog, bridges, skill copies, SDD, normative IDs, links and archive/content inspection; stderr empty. Metadata reports no changed inputs. Independently recomputed the original inputs-before manifest once more: all hashes unchanged. Prefix/hash inspection command exited 0. No suite rerun was needed because executable/contract inputs remain unchanged; this final verdict and its input record are observation artifacts.

| Criterion | Final state | Supporting observation |
| --- | --- | --- |
| AC-01 | APPROVED | Installed prompt-entry contract, skill compatibility and unchanged authority inputs; prior independent semantic review. |
| AC-02 | APPROVED | Five stages and append-only history contract; actual analysis/planning/resumption records and preserved prefix. |
| AC-03 | APPROVED | Actual post-validation outcome and root activity entries, explicit work/result/documentation/remaining-work disposition, and independent byte-prefix preservation. |
| AC-04 | APPROVED | Twelve contract scenarios inspected against authority boundaries; no changed scope/permission inputs. |
| AC-05 | APPROVED | Independent review and validation, complete check-ox and governance suite with raw terminal success, coverage audit, stable inputs and successful proportional closure check. |

All five criteria are APPROVED for this instruction-adoption task. No blocking acceptance condition remains. Root should append the final confirmation of this verdict, resolving the previously recorded pending AC-03 inspection and stating that no task work remains unfinished, then return the scoped result to the user. Preserve the inspected log prefixes when adding that confirmation. This administrative confirmation does not require another full suite or recursive acceptance cycle; changed implementation, criteria or authority inputs would require affected reevaluation.

Limits remain: instruction adoption and tested governance contracts do not prove universal future model/client compliance, OS isolation, product acceptance or full-scanner verification. Prior pending and failed observations are retained above and in historical artifacts, not rewritten.
