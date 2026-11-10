# Plan

D-01 / R-01: Supersede the blanket deletion rationale. Security and quality have
current consumers: secret exposure in source/history, dependency vulnerabilities,
Rust/Python defects, unsafe inventory, unnecessary dependencies, licensing and
coverage evidence. Keep JVM/frontend/Tauri/Graphify/product-specific release
operations excluded. Reuse original report algorithms and preserve their MIT
notice; do not restore foreign persistence, severity budgets or blanket exceptions.

D-02 / R-02: Fixed named checks, private per-run logs, no shell command overrides,
no installation or data refresh. Sources are scanned from a manifest-bound copy
when scanner ignore/cache behavior could hide generated paths or mutate sources.
Missing tools or reviewed datasets block the requested check. Strict reports and
nonzero raw exits prevent success by parser omission. Geiger/coverage/SBOM are
measurements, not product/security acceptance. Extra tools are selected according
to the changed surface; full adds baseline security and quality. Optional scans
remain available even when prerequisites are absent. Review all inherited files,
including generic analyzers and report helpers, before excluding anything.

D-03 / R-03: Add exact-content successor normalization before the previous closure
revision. Preserve preimages, authenticate the successor registry, test unknown
mutations and detached copies. Explicitly extend the existing scripts copy boundary
to maintained scripts and their local rules/modules, excluding runtime data and
erase.md. Do not change profile/catalog or generate a distribution package.

D-04 / R-04: Preparation uses official current documentation. No tools are installed
in this environment. Tests with controlled executables validate orchestration;
they do not substitute for real scanners. AC-04 remains UNVERIFIED for absent
tools/data, without mislabeling the implemented adapters as a security audit.

Primary skill: application-security; path .codex/skills/application-security/SKILL.md;
bridge sdd/chain/application-security.md, bridge_version 1; content SHA256 0d992c0538df30bd5e0c6be689990184ec51671225809eac0f01759cc08257c4.
Used for trust boundaries (source/report/data/tool), explicit denial on incomplete
scans, suppression and unavailable prerequisites, and evidence limits (T002/T004).
No additional skill or delegation selected. Earlier consulted design/integrity
methods remain in the predecessor plan, not a claim of new consultations here.

## Shell successor — 2026-11-06

Operational Python and repeated wrappers are superseded by scripts-shell-refactor.
The observations above are historical. Current inputs and adapter acceptance are
recorded in that feature; previous affected observations are retained verbatim
in evidence.json and are not renewed by changing hashes. Missing real scanners
remain UNVERIFIED. Active entry: bash scripts/automate.sh.
