# Local persistence experiment authorization — 2026-11-05

Authority: explicit maintainer request in this session, “registre minha decisão ...
prepare a T009 para revisão antes dos ensaios”. This records adoption and conditional
authorization, never operational acceptance. Supersedes pending D2/D3/D4/D4-deps
statements in the proposal and prior preparation packets; their original bytes
were preserved by the 2026-11-05 preflight and are now recoverable only from Git history.

| Decision | Effective disposition | Consequence / review trigger |
| --- | --- | --- |
| D1 | Already adopted post-F0, before F3/MVP | Do not reopen; no F0 acceptance transfers to storage. |
| D2 | Adopt the common contract in `ea3cf0f:sdd/features/product-local-persistence/experiment-protocol.md` | Stable identities, full provenance, immutable observations, integral references; durable intent before effects; atomic complete observation and references; supervisor-observed confirmation; confirmed transactions survive owned-process death in tested envelope. Unconfirmed outcome is uncertain and reconciled by operation_id without automatic effect repetition. Same ID/payload idempotent; conflicting payload rejected. Preserve five states and revalidate after load. One cooperating writer owns the store lease; contenders refuse before effects. Recoverable migration with pre-backup, incompatible versions rejected without writes, consistent restore. Detect corruption, preserve original bytes and recover only validated data or explicit error. Excludes OS crash, power loss, hostile writers and remote sync. |
| D3 | Conditionally authorize disposable paired SQLite/versioned-snapshot E01..E08, same experimental Iced worker/error shell on X11 and native Wayland separately | Independent expected manifests and external effect/ack counters; journal documentary only. Freeze and pre-execution review mandatory. Current step prepares review only: no candidate encoders or trials. Does not choose D5 or grant D6. |
| D4 | Adopt Linux x86_64, Rust 1.99.1, local XFS; owned .local/build/persistence-experiment-<run>/; M0/M1/M32/ML with ML 120 MiB raw content | Reobserve environment/mount/free space immediately before trials. Three warmups, twenty measured no-fault repetitions, ten per fault/cut/corpus, paired alternating order; retain all raw samples/failures. Store admission 1 GiB, total run cap 4 GiB, peak candidate RSS 512 MiB, writer fail-fast/no retry, recovery/restore/error watchdog 5 s. Visual response <=120 ms is experimental hypothesis requiring new evidence. No eviction. These differ from current logical 128 MiB admission. |
| D4 faults | SIGKILL only owned experiment processes; truncate/corrupt only owned copies; real permission denial as unprivileged process | Real ENOSPC needs separate bounded disposable-filesystem authorization. No host filling, mounting, OS crash or power cut. Injected faults always labelled simulated. |
| D4-deps | Authorize isolated resolution and review of proposed rusqlite =0.41.1 with bundled and backup, conditional on technical assessment | Exact isolated Cargo.toml/Cargo.lock, libsqlite3-sys, SQLite version/source ID/checksum, flags, licenses, effective-version primary docs; DELETE/FULL/foreign_keys ON, explicit transactions and store writer lease with effective-value readback. Freeze snapshot v1 layout/locking/validation/flush/sync/same-FS publication/directory sync/recovery. No application/ manifest, lock or dependency changes. Version is not prevalidated. |
| D5 / D6 | Pending separate decisions | D5 requires comparable critical evidence with correctness elimination before costs. D6 requires separate integration authorization and product evidence. |

Network acquisition was separately and explicitly authorized in this session by
“Autorizar aquisição isolada”, limited to Cargo/crates.io acquisition for this package
and transitives. This is not a standing network grant. Resolution is not validation.

Alternatives: amend the common envelope, defer the comparison, or later select neither
candidate. Maintainer chose the bounded common comparison; no weighted scores or
winner. Lost confirmed history, partial/corrupt acceptance, false approval, duplicate
effects, writer violations or unsafe migration/restore eliminate before performance.
Missing critical evidence prevents D5. Changed inputs require affected-case reobservation
and explicit comparability. AC-01..07 remain UNVERIFIED.
