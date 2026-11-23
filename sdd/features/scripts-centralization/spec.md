# Script configuration centralization

REQ-01: Adapt the complete Ec script configuration organization to Ox, preserving existing local work and Ox execution contracts.
REQ-02: One declarative catalog owns scopes, scanner metadata, policy paths and execution parameters; native policies and local rules have dedicated homes.
REQ-03: Reject malformed catalogs and retain fail-closed reports, explicit overrides and deterministic Toolbox discovery, offline Cargo and reviewed exceptions.

- AC-01 → REQ-01: Reference inventory and migration disposition cover the Ec configuration surfaces.
- AC-02 → REQ-02: Plans and checks consume the central catalog with no obsolete policy copies.
- AC-03 → REQ-03: Focused regression tests pass; operational limitations remain explicit.

Authorization: explicit maintainer request on 2026-11-13 for complete local Ox script configuration refactoring using read-only Ec as reference. No commits or publication.

## Default parity successor — 2026-11-13

The maintainer explicitly requests Ec default parity after observing that the
previous migration preserved the old command interface. REQ-01 now includes the
public plan/run interface, default/complete selection, mandatory governance,
surface/check filters and shared execution defaults. Project-specific components,
licenses and exception decisions remain Ox inputs. No Ec writes or publication.

- AC-04 → REQ-01: The public plan/run interface matches Ec selection semantics, rejects invalid combinations before execution, and retains legacy callers.

- AC-05 → REQ-02: Existing native analyzers adopt applicable Ec defaults, with positive/negative native policy probes and explicit product-specific differences.

The maintainer explicitly confirmed including analyzer rules. This covers default
policies of implemented analyzers, not implementation of Ec-only CodeQL, browser,
service or third-party-catalog execution engines. Ox-specific license/advisory and
source-bound review decisions remain intact. Findings newly exposed by broader
rules are not suppressed to make the configuration migration pass.

## Remediation scope — 2026-11-13

The maintainer explicitly selects correction of all local failures, linter findings
and cargo-deny findings from pHMB3WNy, including the final Bandit/YARA observations.
T005 preserves the configured analyzer groups and fail-closed contracts. Local
RustSec acquisition/review and isolated preparation of a corrected Geiger are
authorized remediation, without global installs, central source changes or publication.

## Cargo discovery and portable evidence successor — 2026-11-13

Authorization: the maintainer requests Ox refactoring to follow Ec after comparing
the failed toqdfXzz run. Ec remains a read-only reference. Scope: native Cargo
plugin discovery, controlled test environments, applicable Geiger execution
parameters and portable configuration evidence. Product sources, dependency
versions, Toolbox ownership, commits and publication are outside this change.

REQ-04: Like Ec, preserve PATH priority and append a separately selectable Cargo
plugin directory; a dependency cache must not override tools selected by tests.
Retain Ox's pinned, installed toolchain and locked/offline execution.
REQ-05: Keep scripts-centralization in governance exports with current evidence
whose inputs are present there. Preserve broader historical observations unchanged;
do not weaken input freshness or imply that configuration tests accept the product.

- AC-06 → REQ-04: PATH tools precede Cargo-home tools, explicit plugin-directory selection and empty-override rejection are tested, controlled adapters pass with an isolated Cargo home, and Geiger uses the Ec stack/all-features parameters.
- AC-07 → REQ-05: An independent governance copy retains this feature and validates its current evidence without application, cache or bytecode inputs; missing or mutated current bindings remain rejected.

## Explicit native executable successor — 2026-11-15

The maintainer requests correction of the recurring Geiger failure in
ox-run-Fwke2bPi. Authorized scope is local selection of the already-qualified
Geiger binary, focused checks, and documentation; no global installation,
download, log rotation, publication or complete scanner run.

REQ-04 and AC-06 now distinguish explicit selection from discovery: a native
check may declare a repository-relative executable and its exact SHA-256 in the
catalog. That explicit identity takes precedence over PATH and fails closed
when missing, nonexecutable, symlinked, escaping or changed. Checks without that
selection retain PATH-first discovery and the existing Cargo-directory contract.
Geiger declares the existing local ox.1 binary; it does not silently substitute
the global ec.2 when the qualified local installation is unavailable. No cache
or binary joins governance distribution. A clean consumer must provision its
explicitly selected tool separately; planning remains tool-free.

## Analysis corrections successor — 2026-11-17

Authorization: analyze claude_analisys.md and implement corrections. Preserve prior
scanner policies, raw-result integrity and legacy compatibility unless a confirmed
defect requires a documented bounded successor.

- AC-08: Confirmed runner/reporting/selection/test-oracle defects from the analysis are corrected and covered by focused behavioral checks; every report ID has an explicit disposition against current code and contracts, with independent review and validation and unexecuted operational checks identified.
