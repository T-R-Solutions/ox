# Persistence decision packet after T903 — prepared, not adopted

D1 (post-F0, before F3/MVP) is already adopted. This packet grants no experiment,
dependency download, technology selection or integration. The controlling proposal
is [experiment-protocol.md](../../../sdd/features/product-local-persistence/experiment-protocol.md),
with [AC-01..07](../../../sdd/features/product-local-persistence/spec.md) and
[E01..E08](../../decisions/local-persistence-proposal.md). Both candidates remain UNVERIFIED.

| Decision to record | Concrete proposed disposition | Pending dependency / permission |
| --- | --- | --- |
| D2 | Adopt common immutable identities/provenance, intent before effect, atomic complete observations, independent acknowledgement, uncertain outcome reconciled by operation ID, five-state revalidation after load, no replay, one cooperating writer, migration backup and consistent restore. Acknowledged transactions survive process death; corruption preserves original bytes and reports recovery-required. | Maintainer adoption of process-interruption envelope; OS crash/power loss, hostile writers and remote sync excluded. No storage guarantees are inferred from F0. |
| D3 | Authorize only disposable paired SQLite/snapshot E01..E08, including the same experimental Iced worker/error shell on X11 and native Wayland, independent expected manifests and effect/ack counters. Journal stays documentary. | Explicit experiment grant, current UI/Engine interface dependencies and recorded T903 limitations; D5 selection after results, D6 separate product integration. |
| D4 | Current Linux x86_64/Rust1.99.1/XFS; owned `.local/build/persistence-experiment-<run>/`; M0/M1/M32/ML (120 MiB raw history); 3 warmups+20 timings, 10 repeats per fault/cut/corpus, parity-balanced order. 1 GiB admission quota, 4 GiB run cap, 512 MiB peak RSS, fail-fast writer, 5 s recovery/restore/error watchdog; <=120 ms visible response as experimental hypothesis. No eviction. | Adopt/amend these proposed parameters before runs. Reobserve mount/free space and freeze complete hand-authored entity/verdict tables before encoders. SIGKILL/corruption only owned processes/copies; real permission-denied in nonprivileged process. Real ENOSPC needs separate bounded disposable filesystem permission; no host filling/mount/power-cut grant. Injection remains labelled simulated. |
| D4-deps | Isolated exact rusqlite0.41.1 proposed, bundled SQLite/backup, DELETE journal, FULL sync, foreign_keys ON, explicit transactions and app writer lease; snapshots format v1 with immutable generations, payload/reference validation, flush/sync, same-FS selector publication and directory sync. | Mandatory pre-run review of resolved libsqlite3-sys exact version, SQLite source ID/checksum/build flags/licenses, isolated Cargo.lock and applicable release docs. Existing ^0.39.0 is not a freeze. Network/dependency acquisition not authorized here. Review snapshot locking dependencies if needed; no product Cargo changes. |

Correctness gates eliminate lost acknowledgements, partial/corrupt acceptance,
false approval, duplicate effects, broken migration/restore and writer violations
before speed. Missing critical evidence prevents D5. If both pass, compare retained
raw timings/RSS/bytes and actual maintenance mechanisms; do not invent scores.
Prototype success alone cannot approve integrated AC-01..07.

Next concrete decision: maintainer records D2, D3, D4 and the conditional D4-deps
freeze/review scope. Then T009 authors and freezes independent manifests and isolated
source/lock/configuration for pre-run review. No D1 question is reopened. D5 and D6
are not part of that decision. No experiment was run by this T903 request.
