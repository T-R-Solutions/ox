# Design and authority

Full workflow: contract/security/operational migration authorized by the user's
2026-11-08 request, limited to Ox, no commit or central maintenance.

D-01: Replace the existing backend in place with native exec. Keep registry,
files, process and report modules; reject a second executor or private imports.
D-02: Reject obsolete environment controls rather than ambiguous dual discovery.
D-03: Fail closed where central DB timestamps cannot enforce 24h/120h; Grype
uses its native 120h policy. Never pin consumer snapshots or change validity.
R-01: Mock transport cannot qualify actual scanner versions or Docker cleanup.
R-02: Central registry is empty; RustSec review expired; external maintenance
requires independently authorized operator work. No downloads in this task.

Selected primary skill: software-design, .codex/skills/software-design/SKILL.md;
no declared version; observed SHA256 4e214fd5dbf141ee437814a5c817b6924a05e8ad75cf6bc208281155204f6143. Contribution: responsibilities,
contract seam and proportionate removal of obsolete config/lock. No supporting
skill or sub-agent used. Compare leaving native-first dispatch (violates authority)
with adapting the existing modules (chosen); no new platform library.

## SELinux access correction — 2026-11-08

D-04 / R-03 / T004: Native exec sources are disposable snapshots. Opt in to
shared SELinux labels in the Ox exec wrapper, retaining explicit empty/private
overrides. The platform gains shared z alongside existing private Z; shared
labels permit concurrent readers without private MCS relabel collisions. This
changes SELinux xattrs only on mounted paths, preserving UID/GID, read-only
mounts, capability dropping and enforcing mode. No chmod, privileged mode,
global policy weakening, tool installation or DB renewal.
Primary skill application-security, .codex/skills/application-security/SKILL.md
(no version field), contribution: mount ownership, explicit trust boundary and
positive/negative access validation; no delegation. Official contract consulted:
https://docs.docker.com/engine/storage/bind-mounts/#configure-the-selinux-label .
AC-03 stays UNVERIFIED: selected real file probes do not qualify all scanners,
DB ages or central production activation. Preserve old observations verbatim.

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

## Consumer documentation alignment — 2026-11-09

User authorization: read dev_audit documentation and align only Ox scripts/guides.
The requested workspace-root README is absent; shared-toolbox/README.md and its
consumer-integration/application guides are the observed primary sources.
D-25 / REQ-01/02 / T025: keep native exec and discovery; remove implicit shared
SELinux selection to match the operator's explicit mount choice. Preserve native
argv/exits and Ox guards for Bash 4.4+ and empty explicit TOOLBOX_BIN. Document
tools/ as platform-owned modules/volumes and consumer configs/results as Ox-owned.
Rejected: copying legacy JSON/locks, direct scanner/volume execution, or expanding
the Iced product with Playwright/CodeQL solely because those tools are available.
R-25: enforcing hosts need an explicit reviewed shared/private selection or valid
existing contexts; old deployments relying on the automatic default must configure
their environment before scans. No automatic chmod/relabel, downloads, central
maintenance or real scanner execution in this adaptation.
Primary skill selected/read/applied: software-evolution,
.codex/skills/software-evolution/SKILL.md; bridge sdd/chain/software-evolution.md
version 1; no declared skill version; SHA256
b6649a9db5f2653cccca8b9e53c0489face98a398f2cca8ca7473087ff8b124c.
Reference read: references/transition-decisions.md. Contribution: characterize
the old/new environment behavior, choose a bounded transition, retain stronger
existing discovery guards and define recovery/qualification limits. No delegation.
Preimages, primary-source hashes, affected observations and manual results are in
docs/validation/toolbox-consumer-alignment-20261109/.

## Mandatory consumer rules successor — 2026-11-09

D-26 / REQ-01/02 / T026: adopt the exact provided consumer guide, including
central OSV auto-renewal at 12h acquisition age; retain Ox 24h upstream data-age
checks and offline scanner argv. Remove obsolete local central-scanner commands
from check_command, host exports not forwarded by exec, and unreachable local
report branches. Plans choose transport first, so unavailable local tools yield
no runnable fallback argv. Native argv is defined once in native_command.
Preserve native configs: all are referenced by current commands or preparation;
empty trivyignore intentionally forbids vulnerability exclusions. Rejection of
old OX_* selectors is a diagnostic guard, not a second configuration authority.
Alternative: leave duplicate commands, risking host-path/local dispatch drift;
rejected. No schema-1 compatibility files/callers currently exist in scripts/.
R-26: a future OSV invocation may acquire centrally even with a network-none
scanner. Document this before execution; tests in this task use fake transport,
no real Docker/scanner or maintenance operations. Current configuration conformity
is distinct from AC-03 operational qualification.
Primary skill selected/read/applied: software-design;
.codex/skills/software-design/SKILL.md; no declared version; bridge
sdd/chain/software-design.md version 1. Contribution: separate central native
argv from local commands, remove dead configuration and verify public caller
behavior. Observed hashes and preimages are in
 docs/validation/toolbox-consumer-rules-20261109/. No delegation.

## Operational repair — 2026-11-09

User requests working Ox checks with Ec read-only as a reference. Retain portable
wrapper discovery and caller-controlled SELinux selection; select shared explicitly
in local full verification. Repair native-report null handling, obsolete test
callers, exact-content documentary succession and portable SDD prose references.
Prepare a dedicated Cargo home from reviewed archives and locked official fetch;
no dependency version changes. Preserve previous evidence and mark stale
observations historical; never renew approval by replacing hashes.
Primary skill: software-design, .codex/skills/software-design/SKILL.md (unversioned),
for minimal boundary/caller corrections. Supporting observability-and-diagnostics
(unversioned, same catalog) for real scanner diagnosis; workspace-integrity-engineering
(unversioned) for preimages/content preconditions. Actual entries read.
Validate focused contracts/negative controls, real scanners, then the full public
command; standalone mocks or partial runs cannot release the pending commits.

D-27: Review scanner false positives by exact occurrences and source identities,
without lowering severity or globally skipping rules. The native Bandit baseline
and Ruff per-path dispositions are guarded by static-review.json content hashes;
missing/mutated policy or source fails before scanner execution. Unsafe rule data
remain .txt and are separately scanned in disposable .py/.rs copies to prove
positive detection. R-27: stale or broadened dispositions could hide regressions;
mutation and new-finding controls are required. Application-security skill
(.codex/skills/application-security/SKILL.md, unversioned) consulted for the
false-positive boundary review. This is not acceptance of a vulnerability.

D-28/R-28: dependency-hygiene binds application/Cargo.lock and is product-dependent;
exclude it only from governance-only exports alongside other product-dependent
features. Keep it at its existing path and in all complete-checkout validation.
The independent-copy tests assert the export boundary. Partial succession fixtures
include the repair registry/preimages before resolving the full chain.
Bridges actually consulted: sdd/chain/software-design.md, application-security.md,
observability-and-diagnostics.md and workspace-integrity-engineering.md, all v1;
entry paths and distinct contributions are recorded above.

## Complete-run repair — 2026-11-11

D-29/R-29: inspect every published file of run ox-run-eujcD5Sa, distinguish
configuration/preparation failures from regressions, and repair callers without
weakening report completeness, source identity or freshness gates. Reconcile
exact documentary successors; preserve prior observations before reexamination.
Governance exports continue to exclude criteria needing absent product sources.
Primary skill selected, read and used: software-delivery,
.codex/skills/software-delivery/SKILL.md (unversioned), bridge
sdd/chain/software-delivery.md v1. Contribution: diagnose tool/cache inputs,
repair execution contracts and validate failed stages against their real inputs.
No delegation. Details, criteria and final limitations belong to the repair report.

Supporting skill selected/read/applied: application-security,
.codex/skills/application-security/SKILL.md (unversioned), bridge
sdd/chain/application-security.md v1; contribution: review every historical
Gitleaks occurrence and bound dispositions to immutable commit fingerprints,
with tamper and positive-detection controls. D-30/R-30: no directory/rule/commit
allowlist, no current-tree suppression; unknown or altered fingerprints fail
review. The native 8.24.3 implementation confirms exact commit fingerprint matching.
Trivy keeps the central Checks Bundle/cache mounts; YARA's indicator uses an
equivalent regex spelling to avoid matching its own rule file. Geiger omissions
remain errors and require separate tool-level remediation, never silent removal.

Static successor: Bandit --quiet keeps JSON free of progress output without
changing severity or exit policy. Six reviewed subprocess import/call occurrences
in native review helpers and lifecycle tests use explicit argv; the Bash test
uses /bin/bash and a fixed program with positional paths. Exact-source guarded
native baseline/per-file S603 dispositions apply, not global exclusions. Python
style corrections preserve AST except an unused import and strict zip of fixed
three-channel tuples. Native UI execution is not renewed by this comparison.

## Bounded complete-run correction — 2026-11-15

D-32 / R-32 / REQ-01,REQ-02: the maintainer authorizes diagnosis and repair of
the retained ox-run-OQzMt04y failures, including selection and concealed failures.
Retain active tests and all Bandit rules; bind only reviewed benign records to
exact source/policy hashes. Native baseline matching alone is not line-exact.
The full-route plan, selected skills, ownership and manual BS-01..04 criteria
are in docs/validation/bandit-repair-20261115/plan.md. This bounded correction
does not promote the broad feature ACs or authorize a complete rerun.

## Single OSV acquisition clock successor — 2026-11-16

D-31/R-31: the explicit request supersedes all earlier OSV 24h clauses in this
plan. Implement one central 12h clock since successful download, independent of
scan time or upstream publication age; preserve Trivy/Grype and advisory policies.
Full route, ownership, selected software-delivery entry/bridge and manual criteria
are in docs/validation/osv-acquisition-20261116/plan.md. The actual skill was read
and applied, not merely indicated. Independent review/validation are required;
central changes are prepared locally and need effective write permission to apply.
No real downloads, complete run, commits or publication in this successor.

## Audit identifier clarification — 2026-11-17

The Bandit correction uses D-32/R-32; D-30/R-30 above continues to identify the
Gitleaks fingerprint review. This disambiguates existing decisions without
changing scanner policy, criterion scope or historical observation identities.
