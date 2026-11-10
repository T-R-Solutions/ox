# Operational qualification preflight — 2026-11-08

Maintainer requested operational unblock. Clarification pending: whether this
extends the prior Ox-only scope to central modifications/activation and explicit
official acquisition. No production Toolbox, host permissions or databases changed.
No download, installation, commit or publication performed.

Method: Docker version outside sandbox (exit 0); docker image ls (exit 0);
public central list (exit 0, empty). Nine prepared image records were copied and
registered through the public CLI into an isolated installation under
.local/build/operational-qualification/toolbox. All nine register calls exited 0
and verified image/version. The isolated registrations were activated for probes;
these are not production activations and do not approve the Ox consumer.

Images: Ruff, Bandit, Gitleaks, ShellCheck, Opengrep, Syft, Trivy, Grype,
OSV-Scanner. registration.json binds source image records and revision IDs.
Scripts qualify.py and probe.py remain in the local build directory.

Observed probes: nine command executions completed; all diagnostics reported
native outcome and cleanup removed. Several intended clean/findings cases failed
because source files were unreadable with permission denied. Ruff findings exit 1
was actually an E902 read error, not successful detection. Bandit clean exit 0
and Syft inventory exit 0 are insufficient: the findings fixture returned no
findings, and Syft reported an empty artifact list. Therefore raw exit matches in
isolated-probes.json are diagnostics only, never acceptance. No scanner is
qualified by these probes. Exact streams and executor JSON are preserved in each
probe directory. The cause of bind-mount read denial needs discriminating checks;
SELinux, filesystem access and container mount policy have not been distinguished.
Do not change host permissions or weaken isolation speculatively.

Current Ox AC-05/06/07 and native AC-03 remain UNVERIFIED. RustSec validity remains
2026-11-07. OSV/Trivy public diagnostic lacks an age field; no consumer exception
was introduced. YARA-X has no prepared local image found in the inventory.

Resume after explicit scope confirmation: diagnose read access in disposable
fixtures; implement any necessary public platform contract changes with tests,
qualify images/metadata and fresh bases in isolation, then promote only qualified
central revisions and exercise actual Ox commands including error, source
integrity, age denial, concurrency and cancellation. Preserve current history;
create new successor observations for actual bytes rather than changing dates.
Recovery requires no production rollback: isolated files and run records can be
retained. No container leftovers were reported by the nine probe diagnostics.
