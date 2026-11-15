# Plan

Full route: policy decisions and dependency resolution authorized by the current maintainer request.
D-01/R-01: Record the local Toolbox executable in AGENTS; do not change portable discovery or implicitly run scans.
D-02/R-02: Allow eight reviewed SPDX identifiers including GPL-3.0-only for first-party crates; retain notice/AND obligations and no general public distribution claim. Source manifests/notices are compared to the prior archive-backed inventory.
D-03/R-03: Exact RustSec/OSV IDs only, approved temporarily on 2026-11-09 pending maintainer review. Do not disable the unmaintained category or ignore whole packages.
D-04/R-04: Resolve in a disposable workspace before changing the product lock. Keep Iced and graphical/platform contracts; obtain explicit disposition for constraints that cannot unify. Do not use skip as if it removed dependencies.
Primary: software-delivery, .codex/skills/software-delivery/SKILL.md; bridge sdd/chain/software-delivery.md version 1; no declared skill version. Contribution: controlled inputs, resolution, license identities and reversible promotion. Read references/build-inputs-and-trust.md.
Supporting rust skill read for Cargo/compatibility decisions; no Rust source changes yet. No delegation.
Evidence and preimages: docs/validation/dependency-hygiene-20261109/. No commit/publication or central maintenance as part of this slice. Earlier failed verification is preserved.
software-delivery content SHA256: cfa0249938fb4dd95fe8dc9b93ffd5dfd71ca137014327090aaeb8e196dc7480
rust content SHA256: da7b9ada8326b2d2cb4288ac6f67864c7b9defb833641470904c6fe9221d8891

Maintainer disposition: preserve Iced 0.14; exact nine-version duplicate exceptions
are adopted for the retained graph, with per-chain reasons and review on stack
updates. No skip-tree or global duplicate allow, and no claim that waived packages
were removed. Native Deny exits zero under this explicit policy.

## Complete-run remediation — 2026-11-13

Maintainer selected all cargo-deny findings. Preserve GPL-3.0-only and Iced 0.14. Review cached package license files and exact declaration/resolved edges; unify only compatible ranges in an isolated/offline lock candidate. Explicitly allow BSL-1.0 after comparison with Boost text/GNU compatibility classification. Exact older-version dispositions retain deny-by-default for unknown generations; no skip-tree. Current report records native checks and distribution limitations. Supporting application-security entry .codex/skills/application-security/SKILL.md (bridge sdd/chain/application-security.md version 1) was actually consulted for dependency control and evidence; primary software-delivery and Rust contributions are recorded in scripts-centralization's remediation plan.
