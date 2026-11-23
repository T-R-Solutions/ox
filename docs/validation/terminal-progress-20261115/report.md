# Terminal progress — 2026-11-15

## Scope and method

Authorized: local implementation and focused controlled fixtures for the human
output of `./scripts/automate.sh run --scope complete`. No full real scanner run,
downloads, commits or publication. Baseline clean HEAD 015ff14. The high-profile
coordinator assigns production and test files to separate writers, followed by
independent read-only review and independent validation.

The feature [specification](../../../sdd/features/terminal-progress/spec.md) owns
six bounded criteria; [plan](../../../sdd/features/terminal-progress/plan.md)
records decisions, selected skills and ownership. Current acceptance belongs to
its evidence envelope, not to this narrative or historical scanner observations.

## Observed contracts before implementation

- The runner selects checks from the catalog and executes them sequentially.
  `plan` emits JSON and performs no resource preparation or scanner execution.
- `execute` captures stdout/stderr separately and replays only after process exit;
  nested adapters use the same execution helper. The human view can be separate
  without replacing those raw records.
- Geiger enumerates actual Cargo workspace members, records each result and rejects
  incomplete reports. Its selected executable identity remains unchanged.
- `run_complete` publishes retained logs and removes temporary scanner sources even
  on publication failure. The human total must depend on the publisher result.
- Existing feature observations affected by these paths are already historical;
  their active evidence lists do not contain bindings to the modified paths.
  This change cannot make their INCONCLUSIVE states APPROVED.

## Verification and examples

The first stable terminal suite observed 17 passing tests, exit 0, in 23.080 s
(final-01.txt; exact inputs in final-01-inputs.json). A separate run of seven
existing modules observed 49 passing tests, exit 0, in 130.166 s (regressions-01).
These are historical on their observed inputs; later review repairs are verified
separately, without rebinding these records. The initial check-ox observation
returned 0 and PASS (governance-01.txt); this is structural governance, not product
acceptance.

Independent review found and reproduced three defects in the initial implementation:

1. TERM during final publication could leave the activity watcher alive and abandon
   cleanup. The correction records the cancellation, lets publication/cleanup finish,
   and reaps the watcher; publication failure still takes precedence.
2. A diagnostic sourced from tool/stdout.log had only a temporary locator, removed
   on publication. The correction registers those references across the subshell
   boundary and renders the corresponding retained paths.
3. Absent warnings/skips metadata was rendered as zero. Absence now means
   unavailable; only an observed empty array means zero.

The independent reviewer reproduced the repaired transitions, including exit 143,
CANCELADA, no 100%, retained results and no remaining temporary run after TERM.
Four dedicated regression additions passed independently after the repairs; the
final suite includes 21 cases. The final independent acceptance is recorded below
when its inputs and observations have stabilized. Failed lints are preserved: the initial ShellCheck returned 1 with
30 SC2312 producer-status findings; Ruff returned 1 with three UP012 findings.
ShellCheck then returned 0 (shellcheck-02) after producer-status propagation;
Ruff returned 0 (ruff-02) after removing redundant UTF-8 arguments. Neither fix
weakens gates or excludes rules.

Earlier exploratory tests taken while production was being written are not
acceptance: three failures came from an incomplete snapshot, one exposed a genuine
counter regression, and one was an invalid UTF-8 bytes assertion. The counter
handoff now persists the observed maximum. The oracle uses decoded text; no product
expectation was reduced. These attempts are distinguished from stable final runs.

## Documentation disposition

Reviewed AGENTS.md, docs/development/codex-agents.md, sdd/project.md,
docs/constitution.md, docs/architecture/context.md, sdd/workflow.md,
sdd/evidence.md, README.md and scripts/README.md. Relevant decisions:
scripts-shell-refactor, scripts-task-closure and repository-maintenance, including
their successors. Updated scripts/README.md and this feature/report. Project scope
is recorded in the feature; sdd/project.md needs no authority-content modification.
Application architecture, scanner selection/configuration, report parsers and
historical acceptance are preserved; no product design/documentation change.

## Limits

Fixtures establish runner presentation contracts, not installed scanner correctness,
Docker cleanup under arbitrary external failure, full-pipeline completion or product
acceptance. No original .local logs are used as mutable test fixtures. Unknown
internal progress and diagnostic causes remain explicitly unavailable/undetermined.

## Static review of the new fixture code

Native Bandit reported eight CWE78 candidates in the new controlled test file:
one subprocess import (B404) and seven explicit calls (B603). The independent
review-security.json examines every occurrence: fixed absolute /bin/bash argv,
shell=False, internal operation values, disposable fixture roots, and no tool text
as execution authority. static-integration.json records the exact eight appended
native results, prior/current baseline identities, and source hash. All previous
baseline records remain unchanged, no rules/severities were disabled, and source
or policy drift still rejects execution. This is a source-bound false-positive
disposition, not a clean native scan without the reviewed baseline. The new native post-policy run returned exit 0 / parser 0 with no input drift
(bandit-after). The source-bound rejection regressions also pass; this does not
extend the disposition to changed source bytes.

## Evidence retention

The original captured .log files remain under their observed /tmp paths. Copies
under this report use .txt, preserving the exact bytes and SHA-256, because the
repository ignores .log. retention-manifest.json identifies each renamed copy.
This makes normative evidence available in a future checkout without changing
ignore policy or renewing any observation. Historical snapshots and their input
hashes retain their original meanings.

## Final observed checks

| Method | Result | Scope |
| --- | --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s scripts/tests -p test_terminal_progress.py -v` | 0; 21/21; 24.006 s | Current production, helpers, oracle and all configuration bytes stable before/after; final-02 inputs/receipt. |
| `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=scripts/tests python3 -m unittest -v test_process_lifecycle test_capture_status test_backends test_geiger_selection test_defaults test_automation test_native_reports` | 0; 49/49; 135.533 s | Current runtime/configuration/oracles; regressions-02 preserves its original manifest. |
| Focused native ShellCheck via the prepared Toolbox | 0; parser 0 | Four changed/new production shell files; shellcheck-02 exact command and observed inputs. |
| Focused native Ruff via the prepared Toolbox | 0; parser 0 | New test file; ruff-02 exact command and observed inputs. |
| Focused native Bandit with reviewed baseline | 0; parser 0 | New test file under current policy; bandit-after exact command and observed inputs. |
| `./scripts/automate.sh plan --scope complete` parsed as JSON | 0; 26 checks, therefore 28 phases | Read-only planning of the real catalog, not a run. |

During the 49-test run, report.md and retention-manifest.json changed while
observations were being collected. The original regression receipt records that
drift. Both documents are excluded from scanner source snapshots and are not
runtime/test inputs to those scenarios; their final content is reviewed separately
at documentation closure. No historical hash was updated to conceal the drift.

ShellCheck-02's broad snapshot also predates the final test file and static-review
registry/baseline. Those files are not consumed by the focused shell analysis;
its four shell targets and shell parsing configuration remain identical. Ruff-02
predates the static-review registry/baseline integration, while its Python target
and Ruff configuration are unchanged. Their original receipts are preserved;
the native post-policy Bandit snapshot has no differences. Current acceptance binds
the inputs actually consumed by each method, rather than declaring these entire
earlier snapshots current.

## Current fixture output examples

The complete byte-preserved stderr transcripts are current-example-*.stderr.txt;
current-examples.json identifies the disposable roots, commands, exits and hashes.
Their stdout streams are empty. These excerpts are observed fixture data, not a
claim of a successful full repository run:

```text
[2/3] Geiger (geiger) | total: 44% | fase: 33% | atividade: membros: 1/2; validação final pendente | decorrido: 00:01
[2/3] Geiger (geiger) | total: 55% | fase: 66% | atividade: membros: 2/2; validação final pendente | decorrido: 00:02
[2/3] Geiger (geiger) - REGISTRADO - duração: 00:02
```

```text
1. Achado F401; ocorrências relacionadas: 2
   Onde: ruff, arquivo "scripts/demo.py", linha 12.
   Causa: causa não determinada.
   Código: 1.
```

The five current fixture exits are success 0, recorded Geiger 0, finding 1,
publication failure 2 and TERM during publication 143. The cancellation transcript
shows CANCELADA, retains results, removes the run and stays at total 66%.
A final synchronization can repeat one Geiger progress line before its permanent
block; this is bounded, does not simulate progress and does not emit thousands of
lines. Non-TTY opaque activity emits at most a 30-second heartbeat plus phase/event
updates. A PTY updates the current line each second without changing percentages.

## Current acceptance boundary

The independent validation receipt and feature evidence/convergence own the final
criterion verdicts. Earlier failed checks and review defects remain above and in
retained receipts. The application, native scanner coverage, external environments,
SIGKILL/host death and full-pipeline/product acceptance are outside this bounded
change. No original logs were rotated, no downloads or commits were performed.

## Acceptance observation and closure

Independent validation (validation.json) judged AC-01 through AC-06 APPROVED
against current code, oracles and evidence. The selected feature command
`PYTHONDONTWRITEBYTECODE=1 python3 sdd/tools/validate.py --root . --features sdd/features --feature terminal-progress --require-approved --require-fresh --check-convergence`
returned 0 and PASS (gate-01.txt). Closing the T005 checklist and this observation
changes only documentary inputs; the independent addendum and final gate bind
those final bytes. No runtime/configuration/oracle bytes changed.
The closing records are validation-addendum.json and gate-final.txt; they preserve
this initial gate observation rather than overwriting it.

The controller compared the original log inventory with the final checkout:
743 originals, 743 current, no additions, missing files or changed bytes
(log-preservation.json). All implementation/test/review writers are finished;
only independent final validation remains during this administrative closure.

## Later wording successor — 2026-11-15

The maintainer subsequently requested clearer acceptance wording and review of
history false positives. The two fixed sentences now explain that functional
acceptance is evaluated separately. New observations and independent disposition
are in ../history-correction-20261115/report.md; the preceding envelope is retained
there in coordinator/terminal-evidence-before.json. Earlier observations above
remain tied to their original bytes.
