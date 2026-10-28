# Release identity and state compatibility

Read for packaging, promotion or deployment. Obtain actual consumer contracts and
release requirements before choosing a rollout strategy.

Identify immutable artifact digest, source/input manifest, verified provenance and
applicable SBOM. Build once for a defined platform/variant and promote those bytes;
rebuilding per environment creates another artifact requiring verification. Bind
external configuration and feature flags by version with their own validation and
secret references. Include migrations and asset compatibility without embedding secrets.
[Release engineering, hermetic builds and deployment](https://sre.google/sre-book/release-engineering/)
illustrates this discipline in Google's environment; its tooling/staffing is optional.

Declare public contracts and versioning policy. If SemVer is chosen, incompatible
public API changes require a major version and published contents remain immutable.
A version label cannot demonstrate actual compatibility with strict consumers or
old persisted data. Verify those pairs and communicate migration/deprecation.
[SemVer 2.0.0 §§1–9](https://semver.org/spec/v2.0.0.html).

Enumerate reachable old/new application, configuration, schema, jobs and client pairs.
Expand compatible state before deploying code that needs it; gate new writes until
required readers can interpret them. Backfill/reconcile before switching authority,
then contract after rollback and consumer windows close. A pipeline should check the
actual migration result and application readiness; process startup is insufficient.

Choose rolling, canary, replacement or a maintenance window from risk, capacity and
observability. Define cohort, comparison/control, observation window, representative
work, failure/latency/correctness signals and stop/continue actions in advance. Use
project thresholds; no universal rollout percentage. Treat absent/low-volume telemetry
as inconclusive and shared dependencies as possible contamination. Progressive exposure
limits impact but exposes real users. [Canarying, population/metrics/isolation](https://sre.google/workbook/canarying-releases/).

Rehearse failed readiness, interrupted promotion and incompatible state. Retained code
is not sufficient rollback evidence: new enum values, deleted columns and rotated
credentials may prevent return. Choose rollback only when its state contracts hold;
otherwise stop exposure and use a tested roll-forward, transformation or restore path.
Restore may discard later valid writes and needs external reconciliation. Record the
last reversible point and operator/runbook ownership. Remove temporary flags and
compatibility shims after explicit completion evidence, rather than leaving two
unowned release paths indefinitely.
