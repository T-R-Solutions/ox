# Operational completion matrix — prepared before implementation

All rows initially UNVERIFIED. Required scanners: Gitleaks (dir and Git history),
OSV-Scanner, Opengrep, Bandit, Ruff, ShellCheck, Trivy, Grype, Syft, YARA-X;
local Cargo audit/deny/machete/coverage/geiger remain applicable native consumers.

| Surface | Fixture oracle / required observations | State |
| --- | --- | --- |
| Each scanner | Known clean nonempty input; known finding with expected rule/package; invalid flag and execution failure; native content/exits and Ox classification | UNVERIFIED |
| Reports | Absent/truncated/malformed/incompatible report; empty analysis denied; real reports retained | UNVERIFIED |
| Databases | Missing/corrupt/stale/inconsistent metadata rejected; official prepare/publication/selection/update/recovery | UNVERIFIED |
| Lifecycle | Concurrent known findings; actual cancellation; UUID container/process/cache cleanup; before/after source hashes | UNVERIFIED |
| Central readiness | Inventory images/versions/config/data; isolated qualification; recovery retained; public active catalog and Ox execution agree | UNVERIFIED |
| RustSec | Official immutable revision/date/license; integrity; offline audit/deny consumers | UNVERIFIED |

No activation is permitted solely by version/help probes. Preserve historical runs.
