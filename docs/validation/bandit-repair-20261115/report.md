# Complete-run failure diagnosis and correction

Scope and acceptance criteria are in [plan.md](plan.md). The original run is
`ox-run-OQzMt04y`, retained in `.local/logs/2026-11-15/`; its temporary directory
has been removed by the documented lifecycle. Original file identities are in
original-manifest.json and phase records in original-results.json.

## Original run and coverage

All 26 check results are accounted for, plus preparation/finalization (28 phases).
Twenty checks passed, three reported findings and three recorded measurements.
The failures were Bandit (8), Ruff (3) and ShellCheck (3), not Bandit alone.
Original results, native exits and assessments agree. No additional operational
failure was identified in this retained run; this is not proof that no other
defect exists.

Bandit 1.9.4 selected 71 Python files and reported metrics for all 71, with no
parser errors and no skipped tests. Its pre-baseline metrics counted 119
occurrences; eight remained in `results`. The existing baseline contains 109
records, but native matching is not a one-record/one-occurrence subtraction.
The baseline compares rule/file/text/severity/confidence/CWE/test, not line or
code. Exact source and policy hash validation before execution is therefore an
essential containment boundary, not an optional bookkeeping detail.

The two flagged test files are active executable automation/governance sources.
They launch processes and verify rejection behavior, so they remain scanned.
Current source scanning excludes generated builds/caches, virtual environments,
dependency trees and historical `docs/validation` artifacts. Adversarial scanner
rule fixtures use `.py.txt`/`.rs.txt` and are materialized in disposable trees for
positive controls. Gitleaks history checks committed secrets; it does not perform
Bandit's Python vulnerability analysis on old validation snapshots. No scan-root,
exclusion, severity threshold, `nosec` behavior or global rule selection changed.

Opengrep reported 143 scanned source files, no errors and no skipped rules. Its
stderr warns that the existing `--x-` option is not a stable public API; this is
an upgrade/compatibility limitation, not a hidden failed scan in this run.
All 16 Geiger member reports have empty `packages_without_metrics` and
`used_but_not_scanned_files`. Sixteen repeated parse warnings concern the same
intentionally invalid `pin-project-1.1.13/tests/ui/pinned_drop/invalid-self.rs`
dependency test, whose source explicitly expects Rust syntax errors. Geiger,
coverage and SBOM are `recorded`, not sufficient acceptance gates.

The original governance suite ran 317 tests and scripts suite 110; each reported
one opt-in real-scanner test skip (the same scripts test appears in both suites).
Rust reported six ignored X11 graphical tests and one subprocess helper that
parent tests launch separately. These limits remain explicit; the complete
pipeline does not replace graphical or functional product acceptance.

## Corrections and independent rejection

The eight Bandit records were individually reviewed: two subprocess imports,
five controlled subprocess calls using fixed Bash/Python entrypoints and private
fixture paths, and one `/tmp/origin` literal used only as rejected path data.
The implementation retains the 109 prior baseline objects and appends exactly
the eight objects from a real post-Ruff Bandit report. Source hashes for both
tests and the policy hash bind the reviewed bytes. No test is removed or weakened.

Ruff's three findings were fixed by removing unused `sys` and ordering two local
import blocks. ShellCheck's two status findings were fixed by materializing and
checking the bounded sample before hashing/parsing it. Its jq literal receives
only a local, explained annotation because shell expansion would be incorrect.

Independent review rejected the first ShellCheck repair: a named-file sha256sum
output escaped backslash/newline paths and produced an invalid projected hash.
That candidate and verdict are retained. The repair now reads the sample through
stdin; a persistent regression first demonstrated rejection of the old candidate
and now tests ordinary, backslash and newline directory names. This illustrates
why a clean lint result alone would not have been sufficient.

## Execution boundary and remaining work

A real Bandit run after Ruff, before the baseline addition, returned exit 1 with
exactly the eight expected current findings and no errors. Run identity:
`ox-security-bandit-yvDa5lcI`; raw report is bandit-post-ruff.json.bin.
The preceding sandboxed attempt failed on Toolbox's mandatory central diagnostic
write and is not treated as a scanner result. The focused rerun was explicitly
approved by the host. A later combined native/control script approval was aborted
before execution; it produced no output directory or acceptance evidence.

Final focused native observations are retained in native/results.json and its
per-tool raw reports, input manifests and backend diagnostics:

| Check | Version | Result | Run |
| --- | --- | --- | --- |
| Bandit | 1.9.4 | exit 0, zero findings/errors/skips, 71 selected = 71 measured Python files | ox-security-bandit-cSbse9pL |
| Ruff | 0.11.13 | exit 0, zero findings | ox-security-ruff-UFZh5sSG |
| ShellCheck | 0.11.0 | exit 0, zero findings | ox-security-shellcheck-DmfWz8L1 |

Independent validation compared the native reports, assessment/backend exit
codes and current relevant source hashes. Both guard controls also passed:
an added B603-equivalent call in the reviewed source and a changed baseline
returned exit 3/blocked before any scanner invocation. Inputs, raw results and
method are in guard-controls/. The independent source reviewer reran 15
diagnostic tests, six injected failure cases and Bash syntax, then closed P2;
review-final.json records the delivered independent judgment.

BS-04 remains INCONCLUSIVE because the positive native control for a new Python
file was not executed. Its separate host approval was aborted before execution;
the disposable fixture has no run logs. This is not a failed scanner result or an
automatic-approval rejection. The exact cause, command and resumption condition
are in blocked-control.json. Do not replace this missing proof with clean native
reports or mock scanner results.

The independent regression run executed 61 tests: 59 passed and two public-copy
cases initially failed solely because three feature envelopes still bound the
prior source versions. Those predecessor envelopes and projections were retained
as .bin, their stale evidence archived without renewing hashes, and dependent
states temporarily marked UNVERIFIED for current reexamination. Only the two
affected methods require rerun; the earlier failing observation remains retained.
Both affected methods subsequently passed (2/2, exit 0). Their original failure
logs and successful rerun remain separate, with unchanged executed source hashes.

The independent [current verdict](validation/verdict-current.json) approves
BS-01/02/03 and the eight affected terminal/governance criteria. BS-04 remains
INCONCLUSIVE only for the unexecuted new-file control. New schema-2 evidence
references this current observation and its 151 observed inputs; it does not
relabel any old execution as current.

Final [gate receipt](validation/gate-receipt.json):

- `terminal-progress --require-approved --require-fresh --check-convergence`: exit 0.
- Explicit selection of `terminal-progress`, `history-scanner-correction` and `configuration-cohesion` with `--require-fresh --check-convergence`: exit 0. No global approval flag, because the 17 unrelated criteria remain UNVERIFIED.

Both commands use `PYTHONDONTWRITEBYTECODE=1 python3 sdd/tools/validate.py --root .
--features sdd/features` and the named repeatable `--feature` selections. Exact
argv, stdout, stderr, inputs and results are preserved in the receipt/logs.

## Documentation disposition and limits

Reviewed scripts/README.md, README.md, sdd/project.md, docs/architecture/context.md,
the scanner/toolbox ADRs, scripts-shell-refactor.md, local-artifacts.md and the
affected feature evidence. Public CLI, tool selection, scan scope, retention and
product architecture are unchanged. The maintained scripts README already
requires source-bound reviewed exceptions and scanning active tests; this report
adds the native baseline matching limitation without editing an authenticated
README merely to duplicate the existing contract. Project authorization is in
the affected feature T030/plan and this task plan; no new product phase or broad
permission is implied.

Updated scripts-toolbox-native plan/tasks with this bounded scope. Its broad
AC-01/02/03 remain UNVERIFIED. Changed terminal-progress, configuration-cohesion
and history-scanner-correction observations are reexamined separately; the 15
unrelated configuration criteria and two native history criteria retain their
existing UNVERIFIED states. Prior evidence and the rejected P2 candidate remain
available, with no fabricated refresh of their hashes.

No complete pipeline rerun, product acceptance, downloads, central maintenance,
commit or publication has occurred. All three originally failing scanners passed
focused real retests; the pending new-file detection control limits the complete
BS-04 acceptance claim, not the observed clean results.

Final governance closure: `PYTHONDONTWRITEBYTECODE=1 python3 tools/governance/
scripts/check-ox.py` returned exit 0; receipt in closure-check.json. A first final
check correctly rejected this task's redundant append to the authenticated broad
scanner convergence document. Only that exact append was removed using its
preimage/content precondition, then the check passed. Its rejected bytes/log remain
retained. Scope, outcomes and disposition stay in the feature plan/tasks and this
report; no new documentary authentication exception was introduced.
