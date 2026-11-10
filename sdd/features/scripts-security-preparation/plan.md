# Plan

D-01 / R-01: Immutable generation directories and a locked atomic manifest replacement avoid partial publication and lost updates. Imported provenance is an explicit reviewer assertion, never inferred from hashes. Scanner probes reject incompatible data. No implicit download in checks. T001.
D-02 / R-02: First-party rules, bounded syntactic coverage and regression examples; review signals are not vulnerability proofs. Compiler unsafe prohibition stays authoritative. T002.
D-03 / R-03: Canonical CLI path and installation layout checks preserve existing backend boundary. T003.
Primary skill: application-security, .codex/skills/application-security/SKILL.md (no version field; bridge sdd/chain/application-security.md version 1). Consulted and used for provenance/integrity distinction, publication failures and false positive/denial cases. No delegation.

## Ownership successor — 2026-11-07

Local database preparation is reduced to RustSec. Trivy/OSV/Grype preparation and
execution belong to dev_audit; their consumer selection/policy is governed by
scripts-toolchain-config D-09. Prior local preparation evidence is historical.
No external writes or database acquisition are authorized in this change.
