# ADR — Verification repair after the 2026-11-23 complete run

Adopted under the maintainer's 2026-11-23 request to fix the failures of the complete
verification (`./scripts/automate.sh run --scope complete`, exit 2). Task:
VERIFY-FIX-20261123 (registro removido em 2026-11-23 com o legado; recuperável pelo histórico do Git).

D-02 (Clippy): `hashbrown` joins the reviewed `allowed-duplicate-crates` list in
`scripts/config/native/clippy/clippy.toml`. Both generations come from the Iced
stack introduced in `5ab2f39`: `wgpu`, `wgpu-core` and `naga` require 0.16, while
`indexmap` 2.14.2 (through `toml_edit` and `proc-macro-crate`) requires 0.17. No
older `indexmap` exists in the offline cache. Every other lint stays enabled. The two
findings that the duplicate had hidden are fixed in code, not suppressed.

D-05 (Opengrep): Opengrep 1.33.1 cannot parse the valid half-open range pattern
`16..` in `application/vendor/png-0.18.1`. The validator correctly rejects the
partial report (POL-08). `application/vendor/` is excluded from Opengrep only, with
`--exclude /application/vendor` anchored at the snapshot root, and the Opengrep
assessment records the exclusion as a limit. Vendored crates stay in the common
snapshot and remain covered by cargo-deny, cargo-audit, OSV, Trivy, Grype, Geiger,
Gitleaks and YARA-X.

Consequence of D-05: the local Opengrep rules (`scripts/rules/opengrep/`) no longer
run on `application/vendor/`. A defect those rules would catch in vendored code is
left to the dependency scanners and to review when a crate is vendored or updated.

Rejected: downgrading `indexmap`, which needs a download and changes the lockfile
for no behavioral gain; `#[allow]` attributes; excluding `vendor/` from every
scanner; editing vendored third-party source.

Review when Iced/wgpu upgrade (the 0.16 pin may disappear, so remove the entry), when
Opengrep parses Rust half-open range patterns (remove the exclusion), or when a new
vendored crate is added.
