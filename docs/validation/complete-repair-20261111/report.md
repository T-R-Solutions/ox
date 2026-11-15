# Complete-scope repair — 2026-11-11

Authorized request: examine the recent complete run exhaustively and correct its
errors. Full-route extension of scripts-toolbox-native, D-29/R-29.

Observed run: ox-run-eujcD5Sa, published under .local/logs/2026-11-11 at 16:50.
Twenty-four checks: ten successful/recorded, fourteen failed/error. Eleven central
scanners could not discover Toolbox; their absent diagnostic also triggered awk
noise. Geiger could not resolve android-activity 0.6.1 offline. Governance reported
stale authority inputs, outdated export/link contracts and obsolete test consumers
of .local/checks and .local/security. Rust build/check/test/fmt/clippy succeeded.

Acceptance criteria: preserve raw failure classification with missing Toolbox;
migrate test consumers to actual retained logs/cache; authenticate exact reviewed
documentary changes and reject unknown mutations; maintain independent governance
exports without product acceptance; verify affected checks with explicit installed
Toolbox and Cargo cache. No threshold reduction or blanket exclusions.

## Exhaustive original-run inventory

original-log-inventory.json identifies all 292 published files (5,938,004 bytes),
including empty streams, reports, per-member Geiger results and input manifests.
original-results.json records every check and adapter reason. Original logs remain
under the maintainer's two-date retention policy; the inventory preserves their
identities, not a promise of indefinite local-log retention.

| Original outcome | Checks | Cause and correction |
| --- | --- | --- |
| passed | sdd-structure, rust-fmt, rust-check, rust-build, rust-test, rust-clippy, audit, machete, deny | No original failure; Rust desktop's six ignored tests require separate graphical execution. |
| recorded | coverage | Measurement succeeded; no coverage threshold or product approval inferred. |
| error | gitleaks, osv, opengrep, bandit, ruff, history, trivy, sbom, grype, malware, shellcheck | Toolbox absent from PATH and no explicit override. Use the documented installation/SELinux/Cargo environment. Preserve wrapper exit 125, native exit null and a useful diagnostic without an awk missing-file error. |
| failed | ox | Stale AGENTS/project bindings and exact documentary succession. Reviewed current cache path, appended scope and prior guide changes; archived stale observations and added new documentary inspections. |
| failed | governance-tests | 162 tests: 15 failures, eight errors, one opt-in skipped. Obsolete log/cache paths, missing succession fixtures, product-dependent export criteria and nondeterministic resource selection. These consumers were repaired; checks remain active. |
| error | geiger | Sixteen metadata resolutions failed offline for android-activity 0.6.1 in the default Cargo cache. The dedicated cache already has it; no acquisition required. |

## Failures exposed after restoring real execution

- History: 1,606 findings. Every occurrence was compared with its Git blob/line:
  1,600 SHA-256 evidence inventory values, three SQLite API identifiers, one SQLite
  constant, one prose fragment and one deliberate synthetic fixture. Exact
  commit-qualified fingerprints are reviewed in history-review.json, and the
  redacted original report is retained. The adapter pins the disposition file's
  SHA-256; absence/mutation fails before execution. No rule, directory or whole
  commit is exempted. A new synthetic commit remains detected.
- Trivy: the consumer's explicit --cache-dir conflicted with the central external
  Checks Bundle contract. Remove that override, retain central mounts and request
  --skip-check-update. No database age or vulnerability policy was relaxed.
- YARA: encoded_powershell matched its own rule source. An equivalent regex
  spelling avoids self-matching while preserving case-insensitive detection.
- ShellCheck: corrected the local.sh source annotation, disambiguated the
  completed-run local variable and replaced two AND/OR chains with explicit
  conditions. The sourced backend module declares only its input/output variable
  interface exemptions (SC2034/SC2154); no global ShellCheck codes were disabled.
- Governance-only export: includes DESIGN.md as documentation and omits the two
  visual feature envelopes that require application sources. Only two exact
  product references in the reviewed DESIGN bytes are permitted to be absent;
  unknown document mutations and arbitrary missing targets remain rejected.

Native fingerprint semantics were checked against the installed Gitleaks 8.24.3
[AddFinding implementation](https://github.com/gitleaks/gitleaks/blob/v8.24.3/detect/detect.go#L538-L560).
The central Trivy contract was inspected in the installed Toolbox checks.py and
consumer guide. No shared-toolbox source was changed.

## Observed verification

- checks/scripts.log: 40 tests, 39 passed, one real-scanner opt-in skipped.
- checks/security-contracts.log: all 16 contract tests passed.
- checks/succession.log: all 28 focused succession tests passed.
- checks/closure.log and checks/independent-copy.log: closure checks and all 11
  README/independent-copy tests passed, including unknown-reference rejection.
- Run ox-run-aPYiNfWY: history, Trivy, Grype, YARA and ShellCheck passed; SBOM
  recorded. Actual versions/image identities and outcomes are in native-results.json.
- Real positive controls: Gitleaks history and YARA both returned findings and
  Ox exit 1. The first probe used an upstream-ignored AWS example and a root .ps1
  outside source selection, so it was insufficient; the corrected non-example
  synthetic key and selected application fixture were detected. No real credential
  was used and no application-repository commit was created.
- Intermediate failures remain in dated logs. One early script suite preceded
  the updated static-review identities and was rerun after that review. The first
  real Geiger run overlapped staged edits and correctly rejected changed inputs;
  the stable successor below establishes the remaining failure.

## Remaining Geiger limitation

Run ox-security-geiger-qBl1Vmqj executes all 16 members with native exit zero.
Fourteen complete reports are recorded; ox-app and ox-ui remain incomplete.
Their unscanned lists include assets/non-Rust inputs and three generated Rust
files from thiserror, tiny-xlib and x11-dl. A pin-project deliberately malformed
compile-fail fixture also produces a parser diagnostic. The original cache failure
is resolved, but these missing metrics cannot be relabeled as clean measurement.
The complete scope therefore remains nonzero. Remedy requires a separately
verified scanner change that covers generated Rust and distinguishes non-Rust
inputs; no missing-source allowance or tool installation was introduced here.

## Documentation disposition

Reviewed AGENTS, README, scripts/README, workflow/evidence, sharing guide, feature
contracts and current architecture/documentation index. Updated scripts usage,
project scope, scripts-toolbox-native plan/tasks and affected documentary evidence.
The root README already delegates script usage; product behavior and graphical
instructions are unchanged. Exact succession/predecessors and historical evidence
are retained under before/ and before-evidence/. observed-inputs.json identifies
the implementation, tests, policies, authorities and unchanged Cargo inputs.
Documentation is not operational acceptance. Full-suite final result follows.

## Final successor and disposition

The full command was executed with the exact AGENTS environment in run
ox-run-i2efQ0dt. Its 163-test suite took 1341.743 seconds and finished with one
failure, one error and one opt-in skip. The failures were fixture alignment:
DESIGN.md absent from a synthetic export inventory, and an initially chosen
nonexistent acceptance.md resource. Both were corrected and individually rerun
successfully; the latter now names evaluation-cases.md, confirmed present in the
historical implementation-transition archive. No test/assertion was removed.

All five Rust checks and Gitleaks/OSV/Opengrep/Audit/Machete/Deny passed in that
full execution. Bandit progress contaminated JSON and Ruff found prior visual
helper style issues, so those two stages were corrected and rerun separately:
ox-run-zg3UnMU0 passed both. Production parsing remains strict; --quiet removes
progress at its source ([Bandit CLI](https://bandit.readthedocs.io/en/latest/man/bandit.html)).
Unused imports and compound one-line statements were corrected. zip now checks
the two fixed three-channel sequences. All 96 contrast checks passed. AST
comparisons and hashes are in python-helper-review.json; no graphical session
was rerun or approved by the formatting change.

The initial static-policy section in documentary-review.md is superseded by this
additional review: six native-helper/lifecycle subprocess import/call occurrences
are recorded in bandit-reviewed-occurrences.json. Native helpers launch the
operator-selected binary as one argv element with shell=False; the lifecycle
test executes an absolute /bin/bash with a fixed program and positional tempfile
paths. No externally sourced command text is evaluated. Baseline occurrences,
three per-file S603 dispositions and source identities are guarded together;
unrelated findings and altered policy/source still fail. New tests verify missing
or changed history dispositions and the CLI transport changes.

checks/scripts-final.log has 40 tests: 39 passed and one real-scanner opt-in skip.
checks/preservation-retest.log and checks/git-boundary.log contain the two focused
successful retests. The original full result remains failed; it was not rewritten
or claimed as a second green full execution. Coverage's original successful
observation was not rerun: all compiled Rust/Cargo inputs remain unchanged; the
three modified Python validation helpers are outside Cargo coverage. The initial
and final application-input comparisons make this distinction explicit.

Current conclusion: the identified configuration, transport, test, lint and
false-positive defects are corrected and supported by the recorded retests.
Complete-scope acceptance is still REJECTED by Geiger's incomplete metrics;
T029 remains open. AC-03's broader real failure/recovery matrix remains UNVERIFIED.
Do not infer a clean whole-product/GUI result or a successful final monolithic
complete/full command from this aggregate observation. No central source edits,
application Rust changes, tool installation or application-repository commit.

Closure review additionally covered application/README.md and the three Python
validation helpers. Invocation and native behavior are unchanged; only style,
unused import removal and strict fixed-size contrast pairing changed. Dependent
old native observations are preserved as historical, with their criteria still
INCONCLUSIVE. Final closure checks and input identities are recorded alongside
this report.

Final closure: check-ox exited 0 after evidence updates (checks/final-check.log),
git diff --check exited 0, and all final-inputs.json hashes matched the current
files. Contract AC-01/02, configuration-cohesion and retention AC-03/04 have
current bounded evidence; broader product/operational statuses were not promoted.
