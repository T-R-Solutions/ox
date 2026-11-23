# Toolbox database ownership — 2026-11-07

Current OSV policy: [single acquisition clock](osv-acquisition-validity.md)
(2026-11-16) supersedes the historical OSV 24h clauses below. Trivy/Grype are
unchanged; historical permissions/observations below do not grant new effects.

Maintainer explicitly assigns preparation/versioning and execution of Trivy, OSV
and Grype to Docker (dev_audit), owned by another agent. Ox owns scan targets,
native configurations, selected snapshot identity and maximum age. This supersedes
native-first dispatch only for those scanners and local preparation of their data.
RustSec/cargo-audit stays local; Syft requires no vulnerability database.

D-09 chooses explicit immutable snapshot IDs in Ox over automatic current/latest
selection. The checked external image lock is imported read-only into the Ox lock.
Trivy 0.76.2 is now a supported toolbox adapter. Ox retains 24h OSV and 120h Grype
policies; Trivy uses 120h, matching its previous maximum reviewed lifetime.
Missing/expired data blocks; checks never acquire data or fall back to native.
Native code 0 with findings is valid for Trivy/Grype only when the parsed report
and toolbox findings status agree. Database id/tool/version must match selection.

Local copies are disposable generated data. Cleanup removes OSV/Trivy/Grype
directories from Ox generations and per-check dataset copies, removes their
active registry entries and preserves RustSec, preparation receipts and raw scan
reports. Historical evidence remains historical; cleanup does not renew acceptance.

Scope excludes Docker runs, builds, updates and external writes. Consumer tests
and read-only toolbox validation can pass independently of real Docker acceptance;
current end-to-end integration remains UNVERIFIED until jointly executed.
