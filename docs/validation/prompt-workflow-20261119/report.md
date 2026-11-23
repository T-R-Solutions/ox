# Prompt workflow implementation and verification

Task PROMPT-WORKFLOW-20261119. Resumption revision 2 began on 22 November 2026 and the complete governance suite ended on 23 November UTC. The implementation inputs reviewed on 19 November remain unchanged. This report records observed results; the final independent verdict and closure observation are in [validation.md](resume-20261122/validation.md).

## Delivered behavior

AGENTS.md and sdd/workflow.md require each Ox request to consult the prompt skill, create the five prescribed divisions, append the prompt and analysis/plan before executing the described work, and respect the original request's authority. The contract covers ordinary and read-only requests, prompt-only requests, corrections, resumption, internal delegation and unavailable or unsafe writes. After validation, the coordinator appends work, outcome, unfinished items and reasons to .ai/task_completed.md and preserves the separate append-only task_finalizada.md activity record.

The generic prompt skill already requires explicit and observable completion criteria. The Ox consumer policy requests prompt creation for every request without broadening that reusable skill's selection semantics. No skill or profile installation was needed. The document ledger accepts the reviewed additive contract while preserving historical terminal authentication and rejecting changed, missing, duplicate, arbitrary or downgraded authority sections. Six focused regression tests cover those boundaries.

The original implementation affected AGENTS.md, sdd/workflow.md, tools/governance/scripts/document_ledger.py, tools/governance/tests/test_prompt_execution_contract.py, docs/decisions/prompt-execution-contract.md and the authorized task context in sdd/project.md. The resumption changed no implementation, requirement, skill, test or configuration input. It completed the outstanding checks and acceptance evidence. Existing unrelated work was preserved.

## Verification on observed inputs

The six historical input hashes in [observed-inputs.json](observed-inputs.json) and the selected prompt skill hash match the current files. The broader [input manifest](resume-20261122/inputs-before.json) covers the gate scripts, tests, configuration and task inputs. Both runner results report no changed inputs; the post-suite comparison recomputed the same manifest hashes.

| Check | Observed result | Evidence |
| --- | --- | --- |
| Independent review and focused contract tests, 19 November | No blocking findings; six tests, exit 0. Reused only for the five reviewed implementation inputs whose bytes still match. Project context was not part of that historical five-file review. | [review](review.md) |
| Current check-ox | Exit 0 in 146.343 seconds. Profile, catalog, bridges, skill copies, SDD, normative coverage, links and archive inspection passed. | [metadata](resume-20261122/check-ox.result.json), [stdout](resume-20261122/check-ox.stdout.log), [stderr](resume-20261122/check-ox.stderr.log) |
| Complete governance suite | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools/governance/tests -v`, exit 0. `Ran 296 tests in 30259.185s`, `OK`. No failures, errors or skips. | [metadata](resume-20261122/governance-suite.result.json), [stdout](resume-20261122/governance-suite.stdout.log), [stderr](resume-20261122/governance-suite.stderr.log) |
| Discovery coverage audit | All 296 ordered executions match a fresh discovery without running tests again. There are 287 distinct IDs because test_project_revision imports nine ReadmeImportTests that unittest collects again. All six prompt contract cases executed successfully. | [coverage](resume-20261122/suite-coverage.json) |
| Independent acceptance | AC-01, AC-02 and AC-04 passed the initial semantic inspection. Current complete gate evidence and the actual closure records are assessed separately in the dated independent continuation. | [validation](resume-20261122/validation.md), [observed validation inputs](resume-20261122/validation-inputs.json) |

The full suite ran serially after check-ox. Its long mutation case exercised all 580 retained fixture entries and completed successfully. Progress was observed through current fixture writes rather than treating a silent unittest line as a hang. The duplicate ZIP-name warning comes from the deliberately malformed package rejection case, which ended `ok`; it is retained in the raw stderr. The suite ran once to completion. The earlier failed/interrupted logs and binary preimages remain historical evidence and were not rewritten or promoted to success.

## Documentation and closure disposition

Reviewed authorities and consumers include AGENTS.md, sdd/workflow.md, sdd/evidence.md, docs/development/codex-agents.md, docs/constitution.md, docs/architecture/context.md, sdd/project.md, the prompt skill and bridge, task spec/plan/tasks/review/scenarios and the prompt-execution-contract ADR. Their existing candidate content remains appropriate. This report and the current validation evidence complete the documentary disposition of this resumption. The root coordinator owns the local planning/completion logs and task_finalizada.md and will append the actual task result after validation, followed by an independent prefix and content check for AC-03.

No product, architecture, scanner pipeline, central installation, package, commit or publication change belongs to this task. Those areas need no documentation edit because the change governs agent entry and local task records only. Manual acceptance under sdd/evidence.md applies; unrelated automated product feature approvals are outside this acceptance boundary.

At this report's initial observation, the only remaining work is independent assessment of the complete gate evidence, root append-only closure records and final AC-03 verification. No external blocker or implementation repair was found. Final acceptance must not be inferred from the successful commands alone.

## Limits

The installed instructions and structural tests do not establish universal future model compliance or install a runtime interceptor. Semantic review of the twelve scenarios supplies evidence about the contract; it is not a claim that twelve model sessions were executed. Hash equality supports reuse only for the identified inputs. The successful governance suite is not product or full-scanner acceptance.

## Final acceptance — 23 November 2026 UTC

The independent validator approved AC-01 through AC-05 after inspecting the actual
post-validation records in all three root-owned logs and confirming their captured
prefix hashes remained intact. The earlier pending observations above remain part
of the history. The root also confirmed the original 45,603-byte task_finalizada.md
snapshot remains an unchanged prefix.

The proportional check of new outcome documentation and closure records completed
with exit 0 in 128.726 seconds, empty stderr and no changed implementation inputs.
Its [result](resume-20261122/closure-check-ox.result.json),
[stdout](resume-20261122/closure-check-ox.stdout.log) and
[stderr](resume-20261122/closure-check-ox.stderr.log) were inspected by the independent
validator. The complete suite was not repeated because its bound inputs did not
change. All required technical and acceptance work is complete. The root's final
confirmation append records that the former AC-03 observation is resolved and no
authorized task work remains pending; it does not expand the acceptance boundary.
