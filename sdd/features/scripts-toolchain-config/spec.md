# Scanner configuration and backend integration

- REQ-01: Use installed Cargo scanners and support the existing shared-toolbox contract for external tools, preserving native execution when available. No implicit preparation or downloads.
- REQ-02: Version explicit Ox scanner configurations and official references; include their bytes in evidence. Do not grant license exceptions or suppress findings to obtain success.
- REQ-03: Fail closed on missing tools/images/data, malformed or conflicting reports, changed inputs and incomplete analysis. Preserve raw tool and runner exits.
- REQ-04: Exercise backend dispatch and denial with regression tests, inspect real prerequisites, execute applicable closure and retain predecessor observations.

- AC-01 → REQ-01: Backend plans and controlled subprocesses demonstrate native Cargo and shared-toolbox execution with no prepare/install commands.
- AC-02 → REQ-02: Configuration review and parser checks identify explicit files for each applicable scanner, with official sources and hashes.
- AC-03 → REQ-03: Adversarial tests reject absent/altered locks, invalid reports, omissions, source mutations and conflicting outcomes without fallback after execution.
- AC-04 → REQ-04: Closure results, exact inputs, actual findings and prerequisites are recorded; no claim of clean enterprise security without real coverage.

## Toolbox ownership successor — 2026-11-07

- REQ-05: Supersede REQ-01 native preference for Trivy, OSV and Grype. Toolbox alone prepares snapshots and executes. Ox supplies source targets, native configuration, explicit snapshot SHA256 and positive age policy; never prepare/download during scans or fall back to native. Only Ox may be modified; dev_audit remains owned by another agent. RustSec remains local.
- REQ-06: Reject missing policy, incompatible native overrides and result database identities inconsistent with Ox selection. Remove redundant local OSV/Trivy/Grype databases after controlled verification, preserving historical raw reports and RustSec. Real Docker coverage requires separate observed execution.

- AC-05 → REQ-05: Controlled subprocess tests demonstrate toolbox-only dispatch even with installed native tools, selected targets/configuration/policies, and no local dataset or implicit preparation.
- AC-06 → REQ-06: Tests reject absent policies and substituted database identities; cleanup inventory records removed local bases and preserved RustSec.
- AC-07 → REQ-06: Real Docker execution validates current image locks, snapshots, clean/findings and invalid inputs for all three scanners.

## Native exec successor — 2026-11-08

Authority: docs/decisions/scripts-toolbox-native.md. This section supersedes the
consumer mechanism clauses above: central catalog scanners use toolbox exec,
without Ox locks, explicit snapshot selection, mandatory adapters or native
fallback. RustSec utilities outside that catalog remain local. REQ-05 still
requires source/configuration/policy ownership, no local scanner data acquisition
and no implicit preparation. REQ-06 still requires policy and report integrity,
fail-closed age enforcement and preservation of RustSec and historical records.
The AC-03 lock-denial wording above now means refusal of invalid exec prerequisites;
the AC-06 identity checks apply to verifiable native reports and public metadata,
without consumer-pinned snapshots. AC-07 requires real exec Docker coverage of
current central tools, clean/findings/error reports and lifecycle cleanup.
Old lock/snapshot references describe the predecessor contract only and are not
operational prerequisites. Missing age metadata or execution keeps acceptance
UNVERIFIED, never NOT APPLICABLE. Earlier specs remain in preserved evidence
preimages; no earlier observation is renewed by this successor.

Operational completion successor: the current criteria additionally require public
snapshot-bound origin/identity/data timestamps, unchanged age enforcement, explicit
RustSec update with integrity/offline consumption, qualified active central scanner
revisions, and a traceable real operational matrix. Include clean/known findings,
invalid options/execution failures; report absence/truncation/malformed/incompatible
schemas and empty coverage; missing/corrupt/stale/inconsistent data; prepare/publish/
select/update/recover; concurrent runs, real cancellation/resource cleanup and source
hash preservation. Define fixture oracles before execution. Internal simulated tests
cannot substitute for public Ox/Docker execution. All existing gates remain.

## Single OSV acquisition clock successor — 2026-11-16

Current authority: docs/decisions/osv-acquisition-validity.md. Supersede earlier
OSV 24h/upstream-age and no-central-acquisition clauses: Toolbox reuses a validated
base for <=12h since the last successful download, and acquires on absence,
unknown acquisition or >12h. Every successful download records acquisition,
including manual/idempotent updates; scans never reset it. Identity and acquisition
publish atomically; failed acquisition blocks the requested scan and preserves
previous state. Upstream dates are provenance only for OSV. Retain Trivy/Grype
120h, source/report integrity and advisory exceptions. Existing broad real-Docker
criteria remain unverified; bounded manual criteria OSV-01..05 and inputs are in
docs/validation/osv-acquisition-20261116/plan.md and report.md.
