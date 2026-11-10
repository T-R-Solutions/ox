# Native Toolbox migration evidence — 2026-11-08

Implementation is delivered; operational acceptance is UNVERIFIED.

Observed inputs: hashes in inputs.json; code and tests in scripts/, affected
README/project state and native successor ADR. Extensive pre-existing working
changes were preserved. Recovery preimage: .local/build/toolbox-migration/before.
No commits, downloads, host changes, Ec changes or central writes were performed.

| Criterion / method | Result | Limit |
| --- | --- | --- |
| AC-01, consumer unittest suite | native wrapper, aliases, arrays, spaces/special/empty args, findings and measurement contracts tested | fake central boundary; no scanner qualification |
| AC-02, consumer suite + governance tests | rejects bad/missing diagnostic, cleanup failure, timeout/cancel outcome, invalid reports, incomplete inventory, source/mode changes and source additions; command metadata omits synthetic credential | raw streams can contain secrets; no real Gitleaks redaction proof |
| Local process lifecycle test | real SIGTERM forwarded, cleanup awaited, parallel process unaffected | Docker lifecycle remains unverified |
| Real native opt-in suite | preflight FAILED: central list returned {} | zero scanner operations; no image/base used |
| Docker version | sandbox permission denied; escalated read-only retry returned client/server 29.7.2-ce | no permissions changed; no image activation |
| Real cargo-machete test | clean/finding/invalid manifest cases executed by installed binary | outside central catalog; not a Rust gate |
| SDD structure | standard structure-only check passed | no acceptance inferred |
| check-ox | FAILED: prior input hashes and removed lock/config references no longer describe current inputs | old evidence was not rehashed or promoted |

Exact commands and stderr/results are retained beside this report: tests.stderr,
governance.stderr, automation.stderr, real.stderr, check-ox.stderr, sdd.stdout.
Preliminary failed governance assertions were corrected for the new exec contract
and distinct Ox exit classification; final results are in governance.stderr.

Mappings and responsibility matrix: scripts/README.md and lib/registry.sh.
Central scanners: gitleaks/history → gitleaks dir/git, osv → osv-scanner scan
source, sbom → syft scan, malware → yara-x (yr scan); ruff, bandit, shellcheck,
opengrep, trivy and grype retain their catalog names. Sources /project:ro and
results /out:rw; no implicit extra mounts/network/env. ShellCheck inventories
all scripts .sh, including prepare-datasets.sh and the new wrapper.

Removed active configurations: scripts/config/toolbox.json and
toolbox.images.lock.json. Native Ox configs/rules and historical files remain.
OX_TOOLBOX_BIN/OX_SCANNER_BACKEND now fail with migration instructions.
Gitleaks native finding code 10 is retained in tool_exit_code; Ox exit_code is 1.
The former adapter finding code 42 is no longer expected. stdout/stderr are raw
native streams; backend_record.json is the separate public diagnostic.

External resumption requirements:
1. Operator prepares/qualifies/activates central revisions. No installation or
   activation was attempted; active image identities and used base IDs are empty.
2. Platform exposes supported verified DB timestamps/age checks: OSV 24h and
   Trivy 120h currently fail closed. Grype retains native age 120h. No age limit
   or DB snapshot was changed to obtain success.
3. Qualify commands/parsers against actual active versions. YARA-X 1.0.0 source
   lookup was unavailable; other retained interfaces still need Docker probes.
4. Run real clean/findings/invalid-config, suppression/ignore/inventory, DB
   expiry, synthetic secret redaction, mounts, source integrity, concurrent scans,
   timeout and cancellation/cleanup. Contract mocks are insufficient.
5. RustSec review expired 2026-11-07. Real advisory maintenance and a provenance
   review/probe are required before audit, never editing expiry/hash only.
   cargo-audit/deny/machete/geiger/llvm-cov remain separate local utilities,
   outside the catalog; centralization needs new operator-owned modules.
6. Historical evidence in scripts-toolchain-config and related script features
   remains stale for changed inputs; this successor does not approve it. Global
   check-ox remains red until its acceptance history is reconciled explicitly.

Recovery: use the saved Ox preimage only after comparing current edits, retain
raw reports and diagnostics, and never delete shared images/bases/generations or
.local/security-tools by name/age. Central recovery belongs to the operator with
an identified prior revision and retained image. No automatic legacy fallback.
