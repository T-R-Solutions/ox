# Single OSV acquisition clock — 2026-11-16

The maintainer explicitly requests one OSV temporal validity rule: reuse an existing
validated database when at most 12 hours have elapsed since its last successful
download; otherwise acquire and validate it before scanning. Analysis never resets
the acquisition clock. Every successful acquisition, including explicit update-db
and downloads with identical bytes, records a new timestamp.

This supersedes the OSV 24h upstream-date veto in
[scripts-toolbox-native](scripts-toolbox-native.md) and
[scanner-toolbox-ownership](scanner-toolbox-ownership.md), plus their feature plans.
It also supersedes file mtime as an acquisition oracle. A legacy auto-refresh
receipt bound to the same snapshot remains valid evidence of acquisition during
migration; it does not create a second clock.
Trivy/Grype retain 120h and their current semantics. Advisory exceptions, native
findings/report checks and provenance identity remain unchanged.

Toolbox owns the clock. It publishes acquired_at with the selected immutable
snapshot in current.json atomically after download and validation. A missing
trusted acquisition timestamp causes reacquisition. Reads do not write the pointer;
a failed acquisition preserves prior state and blocks that requested analysis.
Prior snapshots remain available to scanners already using them. Under the exclusive
data lock, a pointer without acquired_at may migrate an existing auto-refresh.json
receipt only when its snapshot identity matches: validate and copy the exact saved
acquired_at, never now or file mtime. Existing current.json acquisition takes
precedence. Migration preserves the <=12h reuse boundary and does not reset the
clock. Unknown/mismatched receipt requires acquisition; preserve legacy history.

Ox removes its OSV maximum_age_seconds and upstream age comparison. Public
upstream timestamps remain provenance, bound to the selected database; consistency
and identity checks still apply. They do not establish an additional OSV lifetime.
The threshold has one central configuration owner, data.osv_refresh_hours = 12.

Alternatives rejected: retain both clocks (contradicts the request and rejects
recently acquired legitimate upstream objects); set the Ox upstream limit to 12h
(still uses the wrong clock); overwrite a mounted snapshot (breaks in-flight
consistency); record scan time (postpones refresh indefinitely).

Review trigger: change of acquisition/publication paths, receipt schema, central
clock configuration or native metadata contract. Scope and evidence:
[OSV successor plan](../validation/osv-acquisition-20261116/plan.md). Real downloads,
Docker qualification and complete runs are not part of this bounded verification.
