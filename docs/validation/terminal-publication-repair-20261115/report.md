# Terminal publication and ShellCheck repair — 2026-11-15

Scope: explicit maintainer request to explain OSV selection and repair seven
ShellCheck findings and finalization code 2. Full SDD route/high coordination
applies because the defect intersects concurrent progress and retained evidence.
No complete pipeline, installation, central maintenance or commit is included.

Observed incident: `/tmp/ox-publication-dhE1Bz7i.log` reports `rm: cannot remove`
the run directory because it is not empty. The retained ShellCheck stream reports
SC2250 and SC2312 in progress.sh. The finalization watcher currently writes
progress-observed.json while run_complete/retain_logs enumerates and deletes the
run. The deterministic replay observed competing writes (inode/mtime changes),
then passed after repair; it does not reconstruct the incident's exact rm
interleaving. Source inspection connects that writer to the copy/delete race.

OSV: the current complete plan selects `osv` at phase 22/28 (26 checks plus
preparation/finalization), using osv-scanner scan source --offline with the
application/Cargo.lock. The original retained osv result is passed/code 0, zero
findings, scanner 2.7.1. This historical observation is not a new scanner run.

Implementation, focused observations, independent review/validation and final
documentation disposition are recorded below after each stage.

## Repair and focused evidence

Only progress.sh and the new regression oracle change production/test behavior.
Five variable expansions now use braces; phase name/action producers are captured
with explicit failure propagation. The finalization observer inherits a
synchronously reconciled snapshot and refreshes the terminal without accessing
the run. Other observers retain recording; retention and failure codes remain.

The implementation report records before/after regression (exit 1 then 0),
28 passing terminal/progress/style tests, 13 lifecycle/capture tests and passing
Bash syntax, with commands, versions and observed input hashes. Independent
read-only source review found no issues in frozen implementation; see review.md.
It did not claim the native run had completed.

## Documentation disposition

Reviewed/updated scripts/README.md, terminal-progress spec/plan/tasks/evidence/
convergence and this report. Reviewed README.md, sdd/project.md, shell-refactor,
task-closure and repository-maintenance ADRs: existing CLI, permission, two-date
retention and public wrapper contracts are preserved, so these authorities need
no modification. History-scanner-correction AC-03 depends on progress.sh and is
reevaluated only for wording/current terminal regressions; its AC-01/02 remain
UNVERIFIED and native history evidence is not renewed. The authenticated
test_terminal_progress.py and all scanner baselines/configuration remain unchanged.

Historical inputs/envelope remain in before/; no earlier execution is claimed
against changed bytes. Controlled process fixtures and scoped native ShellCheck
are not full pipeline or product acceptance.

## Native ShellCheck and execution limits

Targeted public command with maintainer Toolbox/Cargo selection:
`./scripts/automate.sh run --surface scripts --check shellcheck` selected
mandatory SDD/Ox/governance before ShellCheck. SDD structure passed; Ox failed
on preexisting relative links in history-correction's scripts-readme-before.md
and then-transitional freshness. Governance tests also reported failures. The
controller authorized stopping this broader attempt; host Ctrl-C returned130
before ShellCheck. The host interruption did not produce a finalization receipt;
the incomplete run/diagnostic is preserved, not called successfully published.

Standalone `bash scripts/checks/run.sh --check shellcheck` with explicit
TOOLBOX_BIN=/home/rodrigo/Projetos/dev_audit/shared-toolbox/bin/toolbox and
TOOLBOX_SELINUX_LABEL=shared initially failed exit2: sandbox blocked the central
execution-record write (Errno30). Required escalated retry was approved and
completed exit0: run Oo7MnFAU assessment passed, tool_exit_code0, finding_count0,
stdout empty JSON array. Native reports were retained and the owned temporary
scanner run was removed by the existing publisher. Copies are in native/.

During the approval wait the client queued coordinator messages; root independently
started a second approved retry. This duplicate run VvzAYO7j observed tool_exit0
and zero findings but correctly rejected source inventory changes during ongoing
documentary integration (exit2). It is preserved as invalidated, not accepted or
reexecuted. The completed Oo7MnFAU observation supplies native lint evidence for
the unchanged progress.sh bytes. The unrelated shared governance/link issues
remain outside this repair and no aggregate pipeline approval is claimed.

Independent semantic validation approved terminal AC-01–06 and history AC-03,
with original history AC-01/02 still UNVERIFIED; validation.md records attribution
and methods. Final selected freshness/approval gate is recorded separately.
