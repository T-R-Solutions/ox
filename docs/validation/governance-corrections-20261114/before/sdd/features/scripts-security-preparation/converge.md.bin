# Convergence

| Criterion | State | Observation and limits |
| --- | --- | --- |
| AC-01 | APPROVED | OSV 2.7.0 and cargo-audit 0.22.2 execute inside a network namespace; real OSV import and missing/corrupt/expired denial tests pass; failed imports preserve published bytes. |
| AC-02 | APPROVED | Opengrep 1.33.1 passes nine rule tests; complete project path coverage and triage recorded. Fixtures are findings, not suppressed. |
| AC-03 | APPROVED | Seven backend test methods include relocation/spaces, PATH/explicit/absent tools, image locks and failed-result denial without fallback. Native preference retained. |
| AC-04 | UNVERIFIED | Optional paths implemented from official contracts; no installed native Trivy/Grype or acquired optional databases. Do not claim real compatibility acceptance. |

T001..T003 implemented; T004 records the bounded results and optional-tool gap.
No product changes, dependency updates, vulnerability exception, commit or publication.

## Documentary freshness review — 2026-11-06

The approval statements above retain their historical scope. Current states:

- AC-01: INCONCLUSIVE.
- AC-02: INCONCLUSIVE.
- AC-03: INCONCLUSIVE.
- AC-04: UNVERIFIED.

Observations whose bound inputs changed are preserved verbatim in
`historical_evidence`; their hashes were not renewed. See
`docs/validation/documentation-maintenance-20261106/report.md` for the changed-input
inventory and remaining succession failures. Technical re-execution is pending;
this documentary review does not reject the historical scanner results.

## Real preparation successor — 2026-11-07

Current AC-01..AC-04 are APPROVED within this feature's preparation/detection
contract. The final 26-case suite ran with every real opt-in enabled and no skips:
OSV import/expiry/corruption denial, backend relocation/result boundaries, real
scanner clean/findings/invalid-input cases, and native Trivy/Grype import plus
reviewed corrupt-database rejection preserving the published registry. The real
locked-image Opengrep rule suite passed 9/9; project path coverage and all 23
fixture findings are retained and triaged. Configured data acquisition was an
explicitly approved separate operation, never a scan side effect.

Trivy's real DB was downloaded and Grype's reviewed real snapshot imported.
Grype 0.119.0 reports `valid` and `schemaVersion`; its preparation probe now checks
the actual contract. Exact code/configuration/test/contract inputs and raw outcomes
are in the resumption evidence and report. This does not approve licenses,
redistribution, a complete security audit or product GUI behavior. Prior states
above remain historical and were not refreshed by substituting hashes.

## Toolbox ownership successor — 2026-11-07

The maintainer moved preparation/execution of Trivy, OSV and Grype to dev_audit.
Ox's preparation entry now handles RustSec only, rejecting the migrated selectors
before writes. Earlier local import/format probes remain historical observations,
not acceptance of the new toolbox contract. Current ownership acceptance belongs
to scripts-toolchain-config AC-05..07 and docs/validation/scanner-toolbox-ownership/.
