# Scanner remediation resumption — 2026-11-07

The scanner integration and explicit preparation work is implemented. Its
acceptance concerns execution, denial, configuration and honest evidence, not a
clean security verdict or permission to ship third-party code. The original
requirements were retained. Owner decisions on licenses, duplicate versions and
product upgrades were not inferred from the request to complete this task.

## Changes and recovery

- Machete/Deny contracts and the exclusive SELinux-labelled toolbox snapshots from
  the predecessor remain in use. The already prepared Grype image/database are
  now selected explicitly; no fabricated lock or database identity was added.
- ShellCheck source directives resolve dataset-preparation modules. Ambiguous
  boolean chains became explicit conditions. The backend module identifies its
  caller-owned variables and outputs; no security rule/baseline was disabled.
- Grype 0.119.0's actual database status uses `valid: true` and `schemaVersion`.
  Preparation now validates those fields, the build date and scanner parsing.
- Geiger attempts all 16 members even when one report is incomplete. Per-member
  raw exits, omissions and diagnostics remain visible. Incomplete results still
  return error; no generated Rust or non-Rust input was silently waived.
- The lexical JSON guard was the measured bottleneck: 45.48 seconds for the real
  169,366-byte report. Stage measurements isolated it from duplicate-key checking.
  The final byte-oriented, bounded-token guard took 0.864, 0.869 and 0.919 seconds
  over the same process boundary and report. Duplicate-key checking was retained.
  This is a local measurement, not a new product performance guarantee.
- Stale Cargo-bound observations in five product features were moved unchanged
  to historical evidence. No product source or dependency version changed in
  this resumption, and no graphical acceptance was renewed by changing hashes.

`before-first-edit/` recovers the affected preimages from the first identified
source snapshot. `before/` and `reconciliation.json` retain the affected evidence
preimages and their changed-input map. Earlier reports and observations remain.

## Executed verification

| Method | Observed result | Exact retained record / limit |
| --- | --- | --- |
| `bash scripts/automate.sh --scope full` with the verified toolbox | All 123 governance/script cases passed (4 opt-in skips); Rust fmt/check/build/test/clippy passed | `runs/full-observed/`; this run preceded the final shell-only refinements. Its initial `ox` failure was stale Cargo evidence, subsequently reconciled and rechecked. |
| All script tests with `OX_REAL_SECURITY_ADAPTERS=1`, `OX_REAL_OPTIONAL_DATASETS=1`, `OX_REAL_OSV=1` | 26 cases passed, no skips | `logs/tests-real-final.log`; real Docker adapters, native OSV, native Trivy/Grype and controlled boundary cases. |
| Current governance fast group | 105 cases passed, 6 opt-in skips | `logs/governance-fast-final.log`; the six real cases passed separately above. No sum of these counts is presented as unique coverage. |
| Opengrep real rule tests in the locked image, network none | 9/9 rules passed, expected positive lines equal actual lines; no missing/error cases | `rule-probe/stdout.json`; Rust/Python examples remain scanner inputs. |
| Real default security and quality/complementary scans | Results below | `runs/security-final/`, `runs/quality-final/`; stdout/stderr, tool/runner exits, config/source identities are preserved. |
| Coverage | LCOV generated; tests completed | `runs/coverage-observed/coverage/coverage.lcov`; no invented coverage threshold or GUI acceptance. |
| Historical Gitleaks, complete local Git history and all refs | 11 commits scanned; 824 raw findings retained | `runs/history-observed/`; no fetch, rewrite or credential transmission. |

Raw run records contain actual commands, source manifests, tool paths/versions,
image/library identities, dataset identities and exits. `observations.json` indexes
them. `collected-sha256.json` identifies the collection-time artifacts; it is not
a claim of authenticity or a manifest of later review additions. Source snapshots,
build directories and full databases remain in the original private run paths;
they were not duplicated into the portable evidence corpus.

## Final scan dispositions

| Check | Result | Disposition |
| --- | --- | --- |
| Gitleaks current sources | passed | No finding in the defined source snapshot; historical/generated surfaces have separate limits. |
| OSV / RustSec | findings | `pin-utils@0.1.1` and `ttf-parser@0.25.1` unmaintained advisories remain enabled. Native Linux inverse-tree inspection excludes pin-utils; the all-target chain retains it through wasmtimer/iced_futures. No transitive override or new risk acceptance. |
| Opengrep | 23 findings | Annotated Rust/Python detection fixtures, individually located and retained. |
| Bandit | 94 findings | Detection fixtures, explicit subprocess boundaries and adversarial path/cwd examples reviewed per occurrence. No global test exception. |
| Ruff | 98 findings | Fixtures and explicit subprocess/path boundaries reviewed per occurrence; the partial Bash executable path in the native OSV test was corrected. |
| Machete | passed | No unused dependency reported by the verified 0.9.2 text contract. |
| Deny | exit 6; 177 findings | 165 license-policy diagnostics and 12 duplicate families retained; no internal diagnostic. Owner approval remains pending. |
| ShellCheck | passed | Source resolution and explicit conditions checked using 0.11.0. |
| Trivy / Grype | passed | Real compatible databases, updates disabled; no matches reported for these source snapshots. This does not negate the advisories found by OSV/RustSec. |
| Syft | recorded | SBOM with 283 components; inventory is not a security/license verdict. |
| YARA-X | findings | The encoded-PowerShell indicator matches its own rule definition. The raw finding remains; this is not evidence of malware in product execution. |
| Geiger | error, tool exit 0 | All 16 members attempted: 14 complete inventories and 2 incomplete. Unscanned generated Rust, included assets/non-Rust files and a dependency parse diagnostic remain explicit. No complete unsafe-inventory claim. |

`current-code-triage.json` binds every Ruff/Bandit/Opengrep occurrence to its observed
source and context. Trusted executable/environment assumptions remain limitations.
`history-triage.json` inspects every finding against the corresponding Git blob:
all 824 values are 64-character hexadecimal document digests in evidence maps;
780 also equal the referenced Markdown blob's SHA256 at that commit, and 44 refer
to historical versions. Neither a suppression nor a history rewrite was applied.

## Preparation and owner review

Preparation was separately approved and executed: private copies of OSV/Gitleaks
and Grype from locked existing images; Syft 1.57.0, YARA-X 1.23.0 and
cargo-llvm-cov 0.9.1 from exact official release assets checked against their
published SHA256; Trivy 0.72.0 from the identified pre-existing local image;
LLVM toolchain component installation and `cargo fetch --locked` for the nine
missing packages. Product Cargo.lock bytes and dependency versions were retained.
`preparation/` holds release metadata and receipts. TLS and hashes establish the
stated transport/integrity checks, not a signature verification claim. The existing
Trivy image has observed provenance/digest only.

OSV reviewed imports and missing/expired/corrupt data were tested. Both optional
native databases accepted real imports and rejected reviewed-but-corrupt database
bytes without replacing the prior published registry. Trivy acquisition and Grype
reviewed import were separate from scans. Failed attempts and prior generations
were preserved. No check installs tools, refreshes a database or switches backend
after an executed failure.

`license-inventory.json` accounts for all 267 registry packages. Their archives
match Cargo.lock; manifests and located notice files were also compared against
those archives. The nine formerly unavailable packages are now available. Linux
metadata identifies 154 registry packages (plus the 16 Ox members).
`license-summary.json` records proposed SPDX choices, including both obligations
for AND expressions. Missing standalone notices still require source-header or
upstream review before redistribution; metadata alone is not a legal opinion.
No allowlist was changed. The 12 duplicate families span the font/Wayland stacks
and proc-macro generations; they remain reported rather than blanket-exempted.

The task's configuration/preparation/verification deliverable is distinct from
these owner-controlled product/distribution decisions. This report authorizes no
publication, commit, license grant, dependency upgrade or clean enterprise-security
claim. Product graphical acceptance and native OS sandbox guarantees are outside
this scanner integration.
