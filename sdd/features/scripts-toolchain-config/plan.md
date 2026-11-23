# Plan

D-01 / R-01: Keep Bash orchestration and installed cargo-* binaries. Resolve native scanners first; only a missing native binary can select a supported shared-toolbox adapter. A failed scan never triggers a fallback. OX_TOOLBOX_BIN relocates the shared CLI; no downloaded executable or arbitrary flags. REQ-01/T001.
D-02 / R-02: Keep native configs in scripts/config, already included in independent governance copies. toolbox.json selects exact catalog versions; generated runtime config targets the identified snapshot and copies the reviewed immutable image lock. Missing image locks block before invoking a runner. REQ-02/T002.
D-03 / R-03: Preserve raw streams, configuration/source identities and toolkit summary; independently parse native reports. Check summary identity, statuses, source integrity and exit agreement. All vulnerability severities count; no baseline, inline suppression or license allowlist imported. REQ-03/T003.
D-04 / R-04: New feature records bounded adapter acceptance separately from actual scanner coverage. Shared toolbox remains external and unmodified; candidate builds and research-blocked adapters remain prerequisites. Playwright is inapplicable to native Iced, with no browser/API surface. REQ-04/T004.

Primary skill: software-delivery, .codex/skills/software-delivery/SKILL.md; bridge sdd/chain/software-delivery.md, bridge_version 1. Used for native/container input identity, offline separation of preparation and checks (T001/T002).
Supporting skill: application-security, .codex/skills/application-security/SKILL.md; bridge sdd/chain/application-security.md, bridge_version 1. Used for configuration suppression, untrusted reports/paths and denial tests (T002/T003). Skill files have no version field; SHA256 identities are recorded in the evidence inputs. No delegation.

Threat boundary: trusted installed executables and local shared-toolbox code consume identified source copies and reviewed datasets. Malformed results, configuration overrides, source/report substitution or missing adapters must not yield approval. Docker daemon/code remain trusted; offline flags do not isolate native processes. Toolbox volumes are outside this checkout and require effective write permissions when run.

## Scanner remediation successor — 2026-11-06

D-05 / R-05: The explicit maintainer request expands this feature to real scanner
compatibility and coordinates scripts-security-preparation (datasets),
scripts-security-quality (findings), scripts-shell-refactor (shell contracts) and
scripts-task-closure (succession). No duplicated requirements or policy approvals.
Shared-toolbox modifications require environment approval outside the writable roots.
Primary software-delivery (path/bridge above, version unspecified) addresses artifact
preparation. Supporting tool-output-engineering,
.codex/skills/tool-output-engineering/SKILL.md, bridge_version 1, addresses strict
versioned parsers, raw retention and incompatible exits. Both consulted directly.

Checkpoints: T005 wrappers/parsers and isolated Docker; T006 succession and adversarial
copies; T007 occurrence-level Python triage; T008 dependency/license review and real
remaining adapters; T009 final documentation and integrated full execution. Dependencies
follow that order, with independent investigations allowed. License authorization is
not inferred from technical compatibility. Earlier observed hashes remain historical.

Supporting Rust skill consulted for T008: .codex/skills/rust/SKILL.md, no version
field, sdd/chain/rust.md bridge_version 1. Contribution: isolate the Deny workspace
bug before changing manifests; preserve edition 2024, MSRV 1.99, toolchain 1.99.1,
lockfile and selected graphical dependencies. A two-crate real reproducer shows
unversioned inherited path -> wildcard plus internal diagnostic; exact =0.1.0
requirement -> exit 0. Apply matching requirements to existing local paths only.

## Resumption — 2026-11-07

D-06 / R-06: Retain the stricter scanner verdicts while performing contextual,
occurrence-level triage. Detection fixtures remain scanned; inspection of trusted
argv and adversarial temporary paths is not a global suppression. License grants,
transitive-version exceptions and product upgrades still need owner decisions.
Application-security (path and version above) was consulted for source-to-interpreter
tracing, distinguishing executable fixtures from production and preserving denial.

D-07 / R-07: Explicitly prepare complementary tools privately in `.local`, using
exact official release assets and published SHA256 identities. No scanner installs
or refreshes during checks. Environment approval separately covers Docker volume
writes, local extraction and LLVM toolchain component preparation. Keep upstream
metadata and preparation receipts, distinguishing integrity from authentication.
The existing local Trivy image has only its observed digest/provenance, not a new
signature/authenticity claim. Source snapshots remain exclusive and recoverable.

D-08 / R-08: Reconcile Cargo-bound obsolete observations without renewed hashes;
keep affected product acceptance inconclusive. Scanner integration acceptance is
independent of product GUI acceptance and license/risk decisions. New tests exercise
Grype clean/vulnerable/broken-config cases; OSV reviewed import and denied datasets
are reexecuted using a private executable extracted from the already locked image.

Supporting performance-engineering consulted for the observed report-validation
bottleneck: `.codex/skills/performance-engineering/SKILL.md`, no version field,
`sdd/chain/performance-engineering.md` bridge_version 1. Contribution: isolate the
169 KB Geiger report's 45-second lexical guard, compare stage timings and discard
the duplicate-key-map hypothesis. Keep the duplicate-key algorithm; validate ASCII
JSON syntax bytes under LC_ALL=C and bound keyword tokens instead of constructing
an entire unquoted line. Independent stdlib JSON tests cover decoded duplicate
keys, UTF-8 strings, nonfinite literals and a larger one-line report. Local timings
are observations, not a new product performance contract. No delegation.

## Toolbox database ownership successor — 2026-11-07

D-09 / R-09 / REQ-05..06 / T011..T012: Make Trivy/OSV/Grype toolbox-only,
reject explicit native execution, preserve native Cargo audit/RustSec. Consumer
configuration pins observed external image/snapshot records; do not generate fake
IDs or call prepare/update-db. Targets/configs belong to Ox; OSV age remains 24h,
Grype 120h, and Trivy adopts the previous maximum five-day review lifetime (120h).
Trivy 0.76.2 and Grype report findings with native exit 0; independently count the
report and compare toolbox status. Verify returned database id/tool/version.

Primary skill: software-delivery, `.codex/skills/software-delivery/SKILL.md`, no
version field, bridge sdd/chain/software-delivery.md v1. Consulted for observed
image/snapshot provenance and separation of external preparation from consumer
execution. plugin-protocol-engineering was inspected but not selected: this is a
client of the existing CLI, not a new host/plugin protocol. No delegation.

Read-only contract sources: shared-toolbox docs/configuration.md, toolbox/config.py,
toolbox/databases.py, toolbox/runner.py and the three pinned adapters. Real records
come from examples/offline-security/toolbox.images.lock.json, copied only into Ox.
Docker execution writes external run volumes, so it is not part of this Ox-only
change. Mock tests establish consumer behavior, not scanner or Docker acceptance.
Remove only generated local database directories for the migrated scanners, under
the preparation lock; preserve registry RustSec, metadata and historical outputs.

## Post-restart ownership recovery — 2026-11-07

D-10 / R-10 / T013: Preserve the migration and external owner's boundary. Register
only the appended project section as a content-bound successor of the reviewed
scanner-remediation project bytes. Reconcile old native-OSV tests with REQ-05:
assert native refusal even when an executable exists; test genuinely missing
native tooling independently. Retain unknown-content, downgrade, preimage, registry
and symlink denial, plus the independent governance copy. No Docker execution.

Supporting skill consulted and used: .codex/skills/workspace-integrity-engineering/
SKILL.md (no version field), sdd/chain/workspace-integrity-engineering.md bridge v1.
Contribution: compare actual post-restart state, preserve each current write-set
preimage, check content preconditions immediately before writes, and leave the
other agent's dev_audit files untouched. No delegation. This recovery reexamines
only affected consumer/evidence inputs and does not grant missing policy approval.

## Native exec governance reconciliation

D-11 / R-11 / T014: use the existing historical_evidence separation; historical records cannot satisfy current references. Pin the two reviewed documentary successors and preserve preimages. Do not project scanner evidence through documentary succession. Primary skill software-design, .codex/skills/software-design/SKILL.md, no declared version; contribution: bounded succession seam and distinct current acceptance. No delegation.

## Operational completion authorization successor — 2026-11-08

The current explicit user request supersedes historical Ox-only/no-acquisition/
no-central-maintenance/no-database-update restrictions solely for completion of
scripts-toolbox-native AC-03 and scripts-toolchain-config AC-05/06/07. Authorized:
bounded Ox and Shared Toolbox corrections, official explicit acquisition/builds,
RustSec refresh, isolated real qualification, central activation and recovery.
Effective filesystem/network permissions still apply. No commits, pushes, global
installs, private code transmission, historical evidence deletion or global SELinux/
permission changes. OSV 24h and Trivy/Grype 120h remain mandatory. Scans stay offline.

D-20: Publish data timestamps derived from upstream generation metadata, bound to
verified snapshot contents and source identities through public exec diagnostics.
Never substitute preparation time. Reject missing, future, inconsistent or expired
metadata. Consumer retains maximum ages; central ownership and exec remain.
D-21: Prepare real updates explicitly and qualify isolated immutable image revisions
before activation. Retain prior pointers/revisions; verify public selection after
activation and recover on failed readiness. No production activation before proof.
R-20: Upstream unavailable/stale data can prevent completion; record exact failure
and request only the external intervention required, without weakening freshness.
R-21: Incomplete/empty reports and leaked resources cannot count as clean runs.
Primary software-delivery, .codex/skills/software-delivery/SKILL.md (no declared
version), consulted with references/build-inputs-and-trust.md and
references/release-and-state.md for immutable preparation/promotion/recovery.
No supporting skills or delegation used in this successor.

## Single OSV acquisition clock successor — 2026-11-16

D-31/R-31: the explicit request supersedes all earlier OSV 24h clauses in this
plan. Implement one central 12h clock since successful download, independent of
scan time or upstream publication age; preserve Trivy/Grype and advisory policies.
Full route, ownership, selected software-delivery entry/bridge and manual criteria
are in docs/validation/osv-acquisition-20261116/plan.md. The actual skill was read
and applied, not merely indicated. Independent review/validation are required;
central changes are prepared locally and need effective write permission to apply.
No real downloads, complete run, commits or publication in this successor.
