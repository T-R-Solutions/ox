# Bandit and complete-run correction plan

## Authorized scope and route

The maintainer requests general analysis, planning and correction of the failures
reported by `automate.sh run --scope complete`, including whether selected paths
belong in the scan and whether other failures were overlooked. This authorizes
bounded local source/configuration repairs and focused verification. No commit,
publication, downloads, central Toolbox maintenance or automatic complete rerun.
Existing dirty and untracked work is preserved.

This is a full-route, high-profile correction under scripts-toolbox-native
REQ-01/02 and T030: changing a security baseline is a material evidence/gate
decision. Its broad AC-01/02/03 remain undecided; the following bounded manual
criteria do not replace or bypass them.

## Requirements and manual criteria

- BS-01: Account for all phases of the retained run, compare result codes and native assessments, identify warnings/skips and distinguish recorded metrics from pass/fail gates.
- BS-02: Review each of the eight Bandit occurrences against actual source and trust boundaries; retain executable Python tests in scope and all rules/severities. Only demonstrated benign occurrences may enter the source-bound baseline.
- BS-03: Correct the three Ruff and three ShellCheck findings from the same run, preserving diagnostics, exit states and existing functional assertions.
- BS-04: Verify current Bandit/Ruff/ShellCheck operation, source coverage and positive/negative controls; changed reviewed source/policy must fail, and new dangerous code must still be detected. Run affected regression suites and report any operational blocker without claiming complete/product acceptance.

## Decisions, risks and sequence

D-01 / R-01: Retain scripts/tests and tools/governance/tests. These execute local
processes and validate security/governance behavior; blanket test exclusion would
conceal defects. Generated/build/cache trees and historical validation artifacts
remain outside current-source scans. History is a separate Gitleaks secret scan,
not a Python vulnerability audit of historical snapshots.

D-02 / R-02: Use the existing native Bandit baseline plus exact source and policy
hash validation. Native baseline comparison alone is not an exact-line security
boundary. Review matching semantics and exercise source mutation rejection and
new findings. Do not use nosec, severity thresholds or global rule skips.

D-03 / R-03: Fix Ruff imports and make ShellCheck's suspected masked command
status explicit. A jq literal receives only an explained local annotation where
shell expansion would be incorrect. Preserve original results and evidence; do
not refresh old hashes into a new assertion of execution.

D-04 / R-04: Execute only focused native checks on stabilized inputs and inspect
actual raw reports, diagnostics and inventory. Original complete-run results
remain historical, including genuine warnings and opted-out tests. No claim of
absence of every possible defect or broad product acceptance.

1. T030a: coordinator inventories the original 28-phase run and source selection; independent reviewer traces all eight occurrences.
2. T030b: implementer applies bounded Ruff/ShellCheck repairs and reviewed baseline entries with preconditions and preimages.
3. T030c: coordinator executes focused regressions and native checks/controls, reconciles affected evidence and documentation.
4. T030d: independent review and validation assess stable changes against BS-01..04; coordinator records verdicts and limitations.

## Selected methods and ownership

Primary: `sdd/chain/application-security.md`, bridge_version 1, actual entry
`.codex/skills/application-security/SKILL.md` (no skill version declared).
Consulted and used for source-to-process boundary analysis, bounded false-positive
dispositions and legitimate/denied scanner controls.

Supporting: `sdd/chain/workspace-integrity-engineering.md`, bridge_version 1
(coordinator consulted the actual bridge during closure); actual entry
`.codex/skills/workspace-integrity-engineering/SKILL.md` (no version declared),
consulted by implementer for preimages, content preconditions and
disjoint writing in the existing multiauthor checkout. No other skill is claimed
as used. Input hashes in the final evidence identify the entries actually read.

Coordinator owns this report/plan, shared documentation and affected evidence.
Implementer owns scripts/tests/test_governance_diagnostics.py,
tools/governance/scripts/log_repair_revision.py, scripts/lib/progress.sh,
scripts/config/native/bandit/bandit-baseline.json and only reviews.static in
scripts/config/automation.json. Independent reviewer owns review.json and never
implements the judged change. Independent validator owns validation artifacts.
No agent reverts another's work. Original reports are retained byte-for-byte as
`.bin`; identities of all 365 retained original log files are recorded separately.

Observed capabilities: profile-based creation, fresh independent contexts,
messages and four total active slots. Root + coordinator + two specialists use
the full budget; review and validation are sequential if required. Interruption
is not assumed to free a slot. Independent acceptance is required, not simulated.

## Documentation disposition to complete

Review scripts/README.md, README.md, sdd/project.md, scripts-toolbox-native,
terminal-progress, history-scanner-correction and configuration-cohesion evidence.
Update dependent observations or mark them undecided, preserving predecessors.
Public commands and product architecture are unchanged. The maintained README
already requires source-bound exceptions and scanning tests; avoid editing pinned
documents solely to duplicate this bounded report.
