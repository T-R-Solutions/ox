# ADR — Governance reconciliation and reproducible bootstrap

Adopted 2026-10-29 under the maintainer's explicit local correction request.
No commits, publication or deletion of historical records are authorized.

D-01: profile governance-reconciliation-001 adds commit-governance as the fourth
conditional capability: 17 general + 4 conditional + 9 specializations = 30.
Its existing Ox-specific procedure is retained; bridge version 1 identifies that
entry by path and content hash, not an invented semantic skill version. This
supersedes the 29-entry profile only; historical counts remain historical.

D-02: append a bounded succession revision to files.json, retaining exact predecessor
bytes and hashes. Recovery resolves historical versions independently of the active
version, but verifies both. skill-ui-metadata-001 remains authoritative for its 30
unchanged metadata files. Recover its original copied metadata from the authenticated
adoption archive. The old AGENTS bytes can be reconstructed by removing exactly the
later commit paragraph from the retained Portuguese version: the result must match
the existing maintenance/layout hash. Save those recovered bytes and derivation.
Never change an old digest to bless new content. Unknown mutations remain failures.

D-03: pin Rust 1.99.1 (the previously observed stable build), retaining rust-version
1.99 as the conservative declared floor, not a demonstrated technical minimum.
This explicitly supersedes only the floating/no-numbered-install choice in the
bootstrap ADR. Compile/test the exact toolchain; 1.99.0 needs separate MSRV execution.
Linux x86_64 remains the supported bootstrap target. Native Wayland coverage is
future work; Windows/macOS testing requires a future support decision and environments.

D-04: fast tests use small fixtures; integration tests retain full independent copies,
archive/recovery checks and adversarial mutations. The default complete suite runs
both; splitting feedback loops does not remove coverage. Compare measured wall times
on the same host and record failures as well as timings.

D-05: exclude path components equal to .git, including worktree files and nested
repositories, in all shared copy/archive selection. Preserve .gitignore. Inspect
only the declared distribution boundary before export; arbitrary root packages such
as the preexisting ox.zip are local outputs, not governance inputs. Recursive archive
inspection remains mandatory for every included archive; no expansion budget is raised.

Rejected: silently relaxing guards, refreshing historical hashes, deleting ox.zip,
classifying commit-governance as an originally copied resource, or treating Python
checks as application acceptance. Revisit on profile, recovery format, platform,
toolchain or distribution boundary changes. Evidence: governance-reconciliation SDD.
