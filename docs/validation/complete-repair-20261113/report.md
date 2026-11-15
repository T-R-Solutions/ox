# Complete-run remediation — 2026-11-13

The maintainer selected correction of all local failures, linter findings and cargo-deny findings after the partial diagnostic. Full route extends scripts-centralization and dependency-hygiene. Preserve unrelated changes and historical evidence. No commits, publication, central source edits or global installation.

Criteria: plans work without installed tools; linters retain their configured rule sets and report no unexplained findings; dependency policy is based on actual license/graph review; RustSec is acquired/reviewed rather than date-edited; Geiger measures every member or explicitly retains an unresolved tool limitation. Functional regression and documentation review accompany changes.

Initial observation: the cited temporary run has completed. Published results contain 26 checks: 15 passed, 2 recorded, 5 findings, 2 failed, 1 blocked and 1 error. Bandit finds one redundant exception handler; YARA-X matches its own EICAR rule string. Coverage/SBOM are recorded measurements, not product acceptance. Six graphical tests remain skipped.

## Implemented changes

- Legacy planning no longer invokes installed_cargo/metadata. Canonical plans retain canonical argv; legacy adapters keep their availability projection.
- ShellCheck: braced variables and explicit defaults; checked line/NUL producers; explicit status/side-effect propagation in snapshot predicates; source-local documented status and module-interface dispositions. No optional checks disabled in shellcheckrc.
- Rust: must_use/const/Eq and supported suggestions, concrete Errors documentation, bounded pixel conversions and explicit InvalidState on absent plugin children. Source-local expect reasons preserve cohesive widget composition and worker ownership contracts. Native Clippy groups remain enabled.
- Ruff: import/UTC/iteration/list fixes and bounded expected exception handling. Authenticated immutable SDD validator and succession runner retain source-bound I001/UP017 style dispositions. Bandit retains one reviewed validator B110 handler: trace_errors reports the rejected path separately. Source/policy digests are enforced before scanning. Unknown drift is not accepted.
- Deny: BSL-1.0 was reviewed against cached package notices and the [Boost text](https://github.com/boostorg/boost/blob/master/LICENSE_1_0.txt); [GNU compatibility classification](https://www.gnu.org/licenses/license-list.html#boost) supports the scoped policy disposition. No distribution approval. Isolated/offline resolution removed windows-sys 0.59.0; incompatible generations retain exact version dispositions. Clippy's family allowances are complemented by Deny's exact-version gate.
- RustSec: official commit 4ef2df8e806a65e2f1ecc14f56f51249062b23d6 (2026-11-13), git fsck, actual import/probe and five-day validity through 2026-11-18. Existing two advisory IDs are unchanged; native audit reports 1509 advisories, zero vulnerabilities and no additional warnings.
- Geiger: isolated 0.14.0+ox.1 patch rejects missing active/root development edges while skipping unbuilt transitive development declarations from mixed-kind resolved nodes. Existing engine, metrics and strict omission checks remain. Eleven graph regressions and an actual ox-ui scan (150 packages, zero missing metrics/files) passed. Explicit local-cache preparation did not modify global tools or Ec sources; CARGO_HOME/bin precedes PATH for an explicitly selected Cargo home.
- YARA: regex preserves EICAR detection without matching its own rule source; positive fixture matched and rule-source negative did not.
- Historical recovery: preserve authenticated originals of three import-edited runners; maintenance verifier compares retained bytes with the original expected digest. Existing historical manifests and hashes are unchanged. Unknown mutations still fail the preservation gates.

## Evidence and documentation disposition

Initial results and per-input observations are retained here. Changed bound observations from four features were preserved under prior/ and made INCONCLUSIVE where operational reacceptance was not performed; no historical hash renewal. Root README, AGENTS, constitution, architecture, wrapper discovery, surface contracts, local-artifact retention, scripts/README and the dependency policy were reviewed. Only scripts usage and dependency policy need updates: there is no new product capability or visual contract. scripts-centralization and dependency-hygiene plan/tasks are updated; native graphical acceptance remains outside these source/linter observations.

T005 (scripts-centralization) and T006 (dependency-hygiene): APPROVED in the bounded corrective scope. All 16 Geiger member assessments are recorded with native/classified exit zero; the final adapter also verified input and binary identities and published its assessment. The later edits to the exception analyzer and CLI test do not execute in Geiger; geiger-catalog-reexamination.json records the exact source-review-only catalog change, with all execution/selection settings unchanged.

| Criterion | Method and observed inputs | Result and limit |
| --- | --- | --- |
| Plans without Rust/Cargo | Public canonical/legacy plans, missing-manifest/toolchain root; defaults and legacy CLI tests | APPROVED: planning succeeds without Cargo; malformed Cargo input is rejected by execution |
| Linter findings | Native Ruff/ShellCheck/Bandit current policies, full-workspace Clippy all targets/features | APPROVED: zero unexplained findings; bounded preservation/module/duplicate dispositions are recorded in static-review.json and source |
| Dependency policy | Inventory of 279 current packages, archive/manifest/lock comparisons; isolated lock candidate; real Deny | APPROVED: no manifest/archive mismatch, no Deny error/warning; remaining incompatible API generations are retained explicitly, not eliminated |
| RustSec | Official clone/review/import; actual audit of current lock; adopted-maintenance and unknown-vulnerability fixtures against a copied DB | APPROVED: current audit zero vulnerabilities/warnings; adopted two IDs accepted, RUSTSEC-2020-0071 rejected with native exit 1; database validity ends 18/11 |
| Geiger | 0.14.0+ox.1, eleven graph regressions, stable adapter run 9O65HZUQ | APPROVED for complete member/build-input measurement: 16/16 recorded, no missing package metrics/used files accepted; measurement is not product/security acceptance |
| Regressions | Rust workspace tests; scripts tests; governance all plus four targeted reevaluations | 43 Rust executions passed, six graphical tests ignored. 58 script cases: 57 passed/one opt-in skip. The 186-case combined governance run had three failures/one error/one skip; all four failing cases passed after correction in a 59.149s focused run. No later single full-suite exit-zero observation is claimed. |
| Historical recovery | Independent export plus current/original/metadata integrity retests | APPROVED: originals remain recoverable by exact prior digests; unknown mutations remain rejected |

The final review found clipboard-win's archive declares BSL-1.0 but includes no standalone license file; that is a distribution-notice gap, not hidden by the build policy. current-license-inventory.json records actual source/archive identities. The source-bound review and native policy probes apply to the inputs recorded here. The previous operational/graphical observations in other features are preserved without reapproval.

## Limits

No new complete-scope scan, graphical interaction/acceptance, global installation, central source maintenance, commit or publication. Existing parser diagnostics for the intentionally invalid pin-project UI fixture remain visible; a successful used-build-input inventory does not establish that every package fixture parses or that third-party unsafe is absent. Dependency notices for public distribution remain pending. The first all-member attempt overlapped source/documentation work and is not used as a clean-current-run claim; the final attempt uses stable sources.

