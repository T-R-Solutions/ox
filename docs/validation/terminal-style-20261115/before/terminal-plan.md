# Plan: terminal progress

## Authority and route

Follow the constitution, SDD workflow/evidence and canonical development agents
procedure. Baseline: clean HEAD 015ff14 observed before edits. This is the full SDD
route and high-complexity coordination because rendering intersects stream capture,
process supervision, cancellation and publication evidence. No new authority to
run scanners, install tools, commit or publish is inferred from repository data.

## Decisions and risks

| Decision/risk | Requirements | Choice and consequence | Verification |
| --- | --- | --- | --- |
| D-01 / R-01 | REQ-01, REQ-02 | N = selected checks + preparation + finalization; equal phase weight. Geiger member completion plus final assessment are observable subunits. Unknown internal work is unavailable, not zero or estimated. | Variable-selection and monotonic boundary fixtures. |
| D-02 / R-02 | REQ-03, REQ-04 | Separate human projection on stderr; fixed trusted labels plus validated structured records, conservative causal fallback and raw locators. Do not replay arbitrary tool text in the human console. | State/diagnostic/adversarial fixtures and independent review. |
| D-03 / R-03 | REQ-05, REQ-06 | Preserve existing raw capture and nested replay; only the outer presentation suppresses replay. Heartbeat owns no tool process and is reaped. Publication 100% depends on actual publisher success. | Byte comparison, JSON compatibility, signals, publication failures. |
| D-04 / R-04 | REQ-06 | Keep shell-only production and existing catalog/parsers/retention. A failed publication may retain an emergency diagnostic log outside the removed run, explicitly identified. | Existing focused regressions and filesystem assertions. |
| D-05 / R-05 | REQ-06 | New subprocess fixtures can produce Bandit CWE78 candidates. Review concrete native occurrences independently; only justified fixture calls may join the existing exact-source static review registry/baseline. Preserve rule/severity coverage and rejection of changed source/policy. | Focused native Bandit before/after, source-bound rejection regressions and independent occurrence review. |

Alternatives rejected: fixed phase totals; invented timer percentages; parsing
arbitrary stderr as causal authority; executing scanners twice for progress;
changing gate expectations; replacing raw logs with summaries; broad lifecycle
rewrite. Revisit when catalog execution becomes parallel or tools expose new
versioned progress contracts.

## Selected methods actually consulted

- Primary: `.codex/skills/tool-output-engineering/SKILL.md`, bridge
  `sdd/chain/tool-output-engineering.md` version 1; consulted raw/normalized/compact
  separation and `references/loss-aware-transformations.md`. Contribution: preserve
  bytes/codes while treating diagnostics as untrusted and disclosing missing causes.
- Supporting: `.codex/skills/agent-runtime-engineering/SKILL.md`, bridge
  `sdd/chain/agent-runtime-engineering.md` version 1; consulted
  `references/process-supervision.md` for heartbeat ownership, signal forwarding,
  drain/reap and distinction between reported completion and confirmed publication.
- Supporting: `.codex/skills/software-testing/SKILL.md`, bridge
  `sdd/chain/software-testing.md` version 1; consulted by test specialist and
  coordinator for independent scenario partitions and controlled process fixtures.
  The independent validator also consulted its case-design and boundary-evidence
  references to assess byte, EOF, signal and retained-locator oracles.
- Supporting: `.codex/skills/application-security/SKILL.md`, bridge
  `sdd/chain/application-security.md` version 1; consulted by the independent
  reviewer and coordinator for the concrete Bandit CWE78 candidates. Contribution:
  trace each subprocess argument to fixed internal fixtures and document each
  source-bound false-positive disposition, without disabling scanner rules.
Skill content versions are captured by input hashes in the final evidence.

## Ownership, capabilities and sequence

Root controller is the communication bridge and read-only advisor. High-profile
coordinator `/root/terminal_progress` owns feature/docs integration and acceptance
coordination. `implement` owns automate.sh, lib/process.sh, new lib/progress.sh,
checks/run.sh and approved production helper additions. `tests` owns the new
test_terminal_progress.py and dedicated fixtures. Writers preserve others' edits.
No specialist delegates. Agent creation by profile and independent context was
observed; four active slots allow root, coordinator and two specialists. Fresh
review and validation contexts follow writers sequentially as slots become free.
No implementer is reused as independent reviewer or validator.

The coordinator owns any D-05 integration in scripts/config/automation.json and
scripts/config/native/bandit/bandit-baseline.json after independent review of the
final test source and observed native occurrences. This narrow disposition does
not change selection, executable identity, argv, severity rules or parser gates.

Review relevant ADRs scripts-shell-refactor, scripts-task-closure and
repository-maintenance, including their dated successors. Existing historical
feature evidence stays historical; new focused observations cannot renew its
hashes or approve native/product results.

## Acceptance wording successor — 2026-11-15

The maintainer requested clarification of “Execução não aceita o produto.”
The two fixed sentences now state that functional acceptance is evaluated
separately. This is a presentation-only successor under REQ-03/D-02; state/code
contracts and criteria are unchanged. The same request reviews history false
positives in the separate history-scanner-correction feature. Current terminal
fixtures and regression checks are reobserved because progress.sh and the history
configuration digest changed. Prior envelopes remain under
docs/validation/history-correction-20261115/coordinator/.
