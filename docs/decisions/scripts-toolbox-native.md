# Native executor ownership successor — 2026-11-08

Current OSV policy: [single acquisition clock](osv-acquisition-validity.md)
(2026-11-16) supersedes the historical OSV 24h clauses below. Trivy/Grype are
unchanged; historical permissions/observations below do not grant new effects.

The user explicitly authorizes Ox implementation and tests, with no central or
Ec changes, host maintenance, commits or implicit downloads. Full workflow:
`sdd/features/scripts-toolbox-native/`.

This supersedes docs/decisions/scanner-toolbox-ownership.md only concerning
consumer-pinned DB snapshots/image locks, adapters and native-first dispatch.
Central catalog scanners use scripts/toolbox.sh exec. Product policy stays in
Ox, including 24h OSV / 120h Trivy/Grype. Missing public age metadata fails closed.
Cargo utilities outside the catalog stay explicitly local; expired RustSec is
not renewed by editing review dates. No central modules are simulated.

Wrapper discovery is TOOLBOX_BIN (explicit invalid values fail) then PATH.
Removed OX_TOOLBOX_BIN/OX_SCANNER_BACKEND are rejected. Reports are written to
explicit /out and native streams stay separate from diagnostic metadata.
Gitleaks findings retain native code 10 and map to Ox classification 1.

Recovery, exact mappings, operational prerequisites and limitations are in
scripts/README.md and docs/validation/scripts-toolbox-native/report.md. No runtime
fallback or deletion of security tools/data/generations is authorized by recovery.

## Consumer guide successor — 2026-11-09

The maintainer requests Ox alignment with the current dev_audit consumer guide.
The actual README is shared-toolbox/README.md; consumer-integration.md and
application.md consolidate the former native-execution/operations guides.
Only the implicit shared-label choice from the 08/11 SELinux correction is
superseded: scripts/toolbox.sh now preserves the caller's unset/empty/shared/private
selection. Relabel must be explicit because it affects host xattrs even for ro
mounts. Existing Bash/empty-override guards and native exec controls remain.
No legacy locks, platform maintenance, scanner expansion, downloads or host
changes are part of this adaptation. Record: scripts-toolbox-native D-25/T025
and docs/validation/toolbox-consumer-alignment-20261109/report.md. Revisit when
the public discovery/mount contract changes; previous test evidence stays historical.

## Operational repair successor — 2026-11-09

The maintainer requests restoring working Ox verification with Ec read-only as
reference. Local invocation explicitly selects shared SELinux mounts and the
dedicated locked Cargo cache. Portable wrapper behavior remains caller-controlled.
Reviewed static false positives are bounded by native occurrence/path and exact
source/policy SHA-256. No global rule/severity reduction or vulnerability acceptance.
Changed/missing review inputs block; new unknown findings still fail. Unsafe
rule fixtures are non-executable data, tested separately through real detection.
Details and limitations: docs/validation/ox-operational-repair-20261109/.

Governance-only copies omit dependency-hygiene because its acceptance needs the
Cargo workspace, which that package deliberately excludes. It remains at the
same path and is checked in the full checkout. The local stable Cargo cache is
.cache/ox/cargo-home; preparation is explicit and checks remain offline.

## Runner defaults clarification — audit correction 2026-11-17

The 13 November default-parity successor in scripts-centralization introduced
runner-level environment/discovery defaults, including shared SELinux labels and
the sibling Toolbox layout. The earlier no-implicit-relabel clause above remains
the public wrapper contract when called directly. It does not describe plan/run,
which applies automation.json before invoking that wrapper. AGENTS.md still
requires explicit maintainer Toolbox selection for complete runs in this checkout.
This clarification records existing scoped authorization; it grants no new relabel,
central maintenance or full execution permission.
