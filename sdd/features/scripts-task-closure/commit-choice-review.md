# Commit preference documentary review — 2026-11-06

Criterion: AC-04 / REQ-04. Method: inspect the bounded diff against pre-edit bytes,
search current operational guides, and manually follow each instruction branch.
Observed input SHA-256 identities are in commit-choice-inputs.json; recoverable
preimages are under .local/commit-choice-before. Existing unrelated changes and
historical evidence are preserved. This is a full-route successor to the earlier
closure invocation policy; no commit was requested or created.

| Scenario/input | Observed instruction result |
| --- | --- |
| Request creates commits | Scope/grouping prepared, then explicit binary question before staging/commit |
| No answer or timeout | Wait; no inferred consent or commit |
| Affirmative answer, complete successful run | Continue scoped commit workflow |
| Affirmative answer, error/nonzero/findings/blocked/missing prerequisites/interruption | No commit; report failure |
| Negative answer | Skip automation, continue scoped workflow; no validation claim |
| Several commits in one request | One answer covers the group; a failed run blocks the group |
| Source changes after a successful run | Repeat validation before committing changed inputs |
| Inspect-only or tag-only request | No commit-creation question |
| General task completion | No duplicated automation mandate in AGENTS, workflow, evidence, root README or interchange guide |

Technical script documentation and historical references remain, including prior
command observations in feature records. Those records do not prescribe automatic
execution at task closure. Generic evidence requirements are unchanged.

Skill validator: `python3 /home/rodrigo/.codex/skills/.system/skill-creator/scripts/quick_validate.py .codex/skills/commit-governance`:
exit 0, `Skill is valid!`.
Initial structural SDD validation found missing AC-04 traceability; the successor
adds that traceability and the present criterion observation before rechecking.

Result: AC-04 APPROVED for the documentary instruction contract only. The review
is a manual scenario walkthrough, not an executed UI/agent or Git integration
test. No hook enforces the preference. No actual automation/commit was run. This
does not renew predecessor AC-01..03 or certify application/scanner behavior.
