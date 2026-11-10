# ADR proposal — OPEN-05 durable local task history

Status: **PROPOSED, not adopted**. Decision owner: maintainer. Preparation authorized on 2026-11-01; storage implementation, dependency selection and F0 inclusion require explicit authorization. This revision replaces the earlier proposal, preserved byte-for-byte under docs/validation/f0-reconciliation-20261101/before/. No storage engine or version is adopted.

## Observed need and authority

POL-02 requires local Ox-controlled persistence at MVP; POL-04/05/06 require preservation, current evidence and explicit acceptance. None explicitly requires storage at F0. See the [F0 decision docket](../validation/foundation-current-20261101/f0.md).

Observed by source inspection, not a new restart experiment: `application/crates/ox-ui/src/local_task.rs` constructs a new clock-based session and `Engine::default()` in `Controller::new`; request/result directories alone do not reconstruct checks/history. `application/crates/ox-verification/src/engine.rs` holds observations/claims in Vecs, with before/after bytes, Check arguments and result. `ox-storage/src/lib.rs` explicitly declares no persistence implementation; `local.rs` provides location/error types only. Source identities are recorded in the reconciliation input manifest. An APPROVED label alone is insufficient durable evidence. Existing code limits (32 observations, 8 declared inputs, 16 MiB/file and 32 MiB/capture) are observed API bounds, not an adopted lifetime retention policy.

## Common proposed requirements for every alternative

- Stable store/task/attempt/operation/observation identities, schema/payload versions, immutable observations and referential completeness. Preserve criterion, oracle identity/arguments/expected result, before/after input identity and result. Preserve all five acceptance states and unknown/missing distinctions. A loaded verdict must be reevaluated against current inputs; completion text cannot approve.
- Commit one observation plus all its references atomically. The process effect is outside that transaction: durably record intent before launch, then reconcile by attempt/operation identity. A recovered unfinished attempt is interrupted/unknown, never automatically rerun or declared successful. A reused operation ID with identical payload is idempotent; conflicting payload is rejected.
- Initially one cooperating writer per store. A second app fails clearly and boundedly; it must not run tasks while unable to record intent. Unknown commit outcome is resolved by durable ID before retry. No blind replay of external effects.
- Versioned migrations with pre-migration backup and recoverable transaction/new-store replacement. Reject future/unsupported schemas without writes. Preserve original corrupt/interrupted bytes. Code rollback does not reverse data migration.
- Consistent backup includes the history and referenced evidence/oracle identities, a manifest and independent restore. Missing binaries or changed workspace inputs produce stale/unverified observations, never current approval. Backups need not redistribute executable binaries; restoration must mark unavailable oracles.
- Visible bounded storage errors; no UI-thread blocking I/O, unbounded retry, silent fallback to volatile acceptance or automatic retention deletion. Initial proposal is no automatic deletion and explicit local export; quotas/location still require decision.

These are proposed feature requirements, not newly imposed product policy.

## Like-for-like alternatives

The following engineering assessment is a design comparison, not measured engine behavior. All alternatives must pass exactly product-local-persistence AC-01..07 and the same fault schedules; none is exempt from backup/migration/concurrency work.

| Dimension / shared obligation | Versioned snapshot + replacement | Append journal + checkpoints | Embedded transactional database (SQLite candidate) |
|---|---|---|---|
| Integrity: whole observation/references visible together | Single generation manifest; validate payload/checksum then publish replacement; references must belong to one generation | Frame length/version/checksum and transaction commit marker; only committed groups replay | Transaction plus unique IDs/references; schema constraints and driver mapping still must be verified |
| Recovery: acknowledged history, no invented success | Retain prior generation; reconcile temp/current generations and intent after each interruption | Reject/quarantine torn tail; replay only committed prefix; checkpoint and log handoff must survive interruption | Engine recovery depends on selected mode/configuration/FS; application still reconciles process effects and provenance |
| Migration: preserve original and reject future format | Read old, write/validate new generation before switching | Version event decoding and checkpoints; replay semantics across versions increase obligations | Transactional migration where supported, version guard and pre-backup; driver/DDL semantics need real tests |
| Backup: consistent history + referenced evidence | Copy a pinned immutable generation and its evidence manifest, then restore independently | Pin checkpoint plus necessary log range and evidence; compaction cannot remove backup inputs | Use engine-consistent backup mechanism plus external evidence manifest; copying one live file is not a complete protocol |
| Concurrency: one writer, duplicate operation safety | Application must implement/test interprocess lock and generation CAS; check-then-write alone is insufficient | Single append coordinator plus lock/sequence and duplicate index rebuilt on replay | Engine write coordination plus application writer policy and unique operation IDs; busy/errors remain explicit |
| Maintenance: bounded cost and review surface | Small dependency surface; custom serialization, locking, publication ordering and complete rewrites | Custom replay/tail/compaction/checkpoint protocol; most application-owned mechanisms | Dependency/driver/native build and upgrades; less custom transaction/recovery code is a hypothesis to validate |
| Workload/cost uncertainty | Full-history rewrite growth not measured | Replay/compaction cost not measured | Query/index/storage costs not measured; no benchmark win claimed |

Snapshot and journal columns specify required mechanisms, not guarantees of an implemented library. No filesystem rename or process-kill experiment alone establishes power-loss durability.

## Technical source ledger and limits

Local contracts/code above are the authoritative observed implementation, bound by content in the reconciliation manifest. External primary documentation was consulted on 2026-11-01, without installing or executing an engine:

- [SQLite transaction documentation](https://www.sqlite.org/lang_transaction.html): multiple readers, one simultaneous write transaction; contention may return SQLITE_BUSY. This supports evaluating a single-writer design, not automatic application-wide writer exclusion.
- [SQLite atomic commit](https://www.sqlite.org/atomiccommit.html): describes rollback-mode protocol and its storage/locking assumptions; it is not a WAL guarantee or evidence about this host's hardware.
- [SQLite backup API](https://www.sqlite.org/backup.html): provides a consistent database-copy mechanism; external evidence files require their own coordinated manifest. No backup/restore was executed here.
- [Versioned release record 3.51.0](https://sqlite.org/releaselog/3_51_0.html), dated 2025-11-04, identifies a historical SQLite release only. It is neither a selected version nor a claim of the latest/safest release. The general documentation pages are unversioned; exact applicability must be checked against the pinned engine/driver/source ID before adoption. No SQLite-specific guarantee is accepted from this review.

A Rust driver, native dependency/FFI and license/build review are unresolved. POL-01 prohibits first-party unsafe, not all transitive native code; that distinction does not preapprove any driver. Network filesystems, hostile noncooperating writers, encryption, secret storage and power-loss tolerance are outside the proposed first tested envelope unless explicitly added.

## Recommendation and consequences

No technology is recommended before comparative results. Evaluate **SQLite and
versioned snapshots as equal candidates** for the same accepted contract. The
previous leading-candidate preference and direct-selection shortcut are superseded
by the current request; their bytes survive in decision-preparation/before/.
A custom append journal remains a design alternative, not a third implementation
in this experiment. It becomes relevant only if the results show a concrete unmet
need; adding it requires an explicit scope decision. Internal SQLite journals or
snapshot recovery metadata do not constitute adoption of a separate event store.

Sequence: adopt the contract and tested failure envelope; authorize the disposable
paired experiment; fix versions/configuration and expected results before candidate
runs; compare observed results; record a technology decision; separately authorize
integration. No direct adoption or implementation path bypasses the comparison.

Proposed envelope: Linux x86_64, one named local filesystem, one cooperating writer,
existing controlled task flow, acknowledged history surviving process interruption.
OS crash and power loss are unclaimed. A local app-data directory outside source
files, no automatic deletion and export to a fresh destination remain proposals.
Directory, workload, quota, writer wait, recovery deadline and UI responsiveness
threshold must be explicitly set before runs. Earlier numeric suggestions were
unmeasured; this revision does not carry them forward as defaults or requirements.
Record the chosen values and rationale once, then use them for both candidates.

Consequences: durable IDs replace session-clock-only identity; Engine needs versioned import/export/revalidation rather than persistence of displayed verdicts. Iced must expose recovery/storage errors, interrupted attempts and stale evidence without blocking. Backup/migration increase feature scope but cannot be omitted just to fit a candidate. No generalized repository store, search, graph or remote sync is included.

## Decision requested and resumption

D1 separate post-F0/pre-MVP delivery is already adopted by the F0 boundary ADR. Maintainer must record: (D2) common
requirements and process-interruption envelope, excluding OS/power-loss claims;
(D3) authorization for the paired disposable experiment only; (D4) directory,
retention/quota, workload, deadlines, dependency and permitted fault mechanisms.
D5 is reserved for the technology decision **after** results; D6 is a separate
product integration authorization. None is recorded as adopted by this proposal.

The [feature specification](../../sdd/features/product-local-persistence/spec.md)
retains seven operational criteria, all UNVERIFIED. A successful prototype alone
does not accept the production UI integration, backup path or feature. Record the
maintainer's actual decision scope/source before executing dependent work.

## Paired experimental protocol — proposed, not executed

Before either candidate is implemented, freeze a technology-neutral expected
manifest: store/task/attempt/operation IDs; operation payload and schema versions;
criterion and oracle identity/arguments; input identities and immutable evidence;
observation/outcome and acceptance state; reference relationships and acknowledgement
sequence. Use explicit absent/unknown values. A current verdict is derived by
revalidation after load, not trusted from a saved display label.

The logical transaction is intent or a complete observation plus its references.
The effect is separate. The harness records whether acknowledgement was observed
outside the killed process. With a valid store, acknowledged transactions must
survive process death. Unacknowledged transactions may be absent or wholly committed;
resolve by ID, never infer absence from timeout or automatically repeat an effect.
Deliberate corruption may make history unrecoverable: detecting it, preserving bytes
and reporting recovery-required is valid; silently accepting damaged history is not.

| Case / AC | Shared input and fault | Independent expected result |
|---|---|---|
| E01 / 01 | Empty and populated histories; all five states, multiple attempts, missing/unknown fields; close then reopen in a second process | Exact logical entities, identities and references match a hand-authored manifest; invalid/dangling records rejected atomically |
| E02 / 02,07 | Kill before/after durable intent, after controlled effect, before commit, after commit before reply, after observed reply | Acknowledged history retained; no partial transaction; uncertain operation reconciled by durable ID; unfinished attempts interrupted/unknown; independent effect counter never increases on restart |
| E03 / 02 | Truncated payload/metadata, modified evidence bytes, interrupted generation publication or transaction write in owned copies | Damage visible, original damaged bytes preserved; valid complete generation/transaction only or explicit recovery-required; no invented approval |
| E04 / 03 | Reopen then change separately input, oracle, arguments or criterion; omit evidence; include unaffected observation | Only dependent acceptance stale; missing evidence cannot approve; expected dependency/verdict table independent of storage decoder |
| E05 / 04 | Old/current/future schemas; kill at migration boundaries; attempt downgrade | Equivalent logical entities after successful migration; no partial visibility; original backup recoverable; future/unsupported versions rejected without writes |
| E06 / 05 | Backup while writer operates; restore in new directory/process; missing/tampered manifest/evidence | One consistent manifest cut, exact entities/provenance; missing/changed external inputs stale; invalid backup refused without overwriting original |
| E07 / 06 | Permission denied, disk full, unavailable/corrupt store, lock contention, recovery deadline exceeded | Visible bounded error; no effect without intent admission and no volatile approval fallback; instrumented UI/worker boundary remains responsive under agreed limit |
| E08 / 07 | Two actual processes race for writer ownership; retry same ID/payload and conflicting payload; lose commit reply | One writer admitted; loser bounded and launches no effect; one result per ID/payload, conflict rejected; external counter proves no duplicated effect |

For each E02 commit schedule, start from the same acknowledged prefix and use
barriers, not timing guesses. Map logical cuts to candidate-specific internal hooks;
record uncovered windows explicitly. E03 corrupts corresponding logical structures,
not arbitrarily identical byte offsets in unrelated file formats. Run both candidates
from fresh owned copies of the same corpus. Record initial and final store hashes,
external acknowledgement/effect logs, exact fault point, expected and observed
entities, exit/error, and retained damaged bytes. Expected histories must not be
generated by either implementation's serializer or recovery code.

Freeze the shared seed/corpus, operation order, repetitions, run-order balancing,
hardware/OS/filesystem/mount, toolchain, workload sizes and fault permissions before
running. Record SQLite source ID, Rust driver, build flags, transaction/journal/sync
configuration and every file it needs; record snapshot format, writer lock,
publication/flush ordering and recovery rules. Match the logical durability contract,
not option names. Any changed shared requirement/corpus reruns affected cases for
both; a candidate-only change reruns its affected cases and labels comparability.
No fabricated commands: the harness and executable replay commands do not exist yet.

Measure elapsed write/recovery/restore time, written bytes, peak memory and error/UI
response under the same workload, retaining raw samples and measurement method.
These are proposed measurement dimensions, not adopted SLOs or benchmark outcomes.
Review maintenance by listing custom recovery/locking/migration mechanisms, dependency
and build obligations, required integration changes and diagnosed failures. Distinguish
observed effort from estimated future work; do not invent weighted scores.

The isolated experiment should exercise the same worker/error contract for E07.
If actual Iced observation is outside the experiment grant, record E07 as UNVERIFIED
at product level, with that integration risk explicit in the decision. Do not turn
a fake UI heartbeat or harness result into product AC-06 acceptance.

## Decision rule and result form

Correctness precedes speed: reject a candidate for lost acknowledged history within
the tested process-failure model, accepted partial/corrupt records, false approval,
duplicate effects, broken restore/migration or violated writer policy. Preserve the
failure; a repaired version needs new affected observations. Missing critical
integrity/recovery evidence prevents selection. If both fail, repair and rerun or
revisit the contract explicitly; do not weaken it to select a winner.

If only one meets the common gates, it is eligible after dependency/integration risk
review. If both meet them, compare measured workload costs and documented maintenance
burden against the agreed priorities; an unresolved trade-off leaves the decision
open. Noncritical integration limitations must be explicit prerequisites for D6 and
product acceptance. Product AC-01..07 require the integrated implementation's evidence.

For each candidate and E01..E08 record: version/configuration/corpus identity,
criterion, method/command, expected/observed result, five-state verdict, raw artifact,
input hashes and limits. Current results: SQLite UNVERIFIED; snapshots UNVERIFIED;
no engine, driver or version chosen. Prototype permission, selection and product
integration remain separate decisions.


## Current preparation successor — 2026-11-05

The milestone proposal above is superseded only by the already adopted
F0-D1..D5 boundary: independent post-F0/pre-MVP storage. The
[decision-ready paired protocol](../../sdd/features/product-local-persistence/experiment-protocol.md)
provides concrete D2/D3/D4/D4-deps proposals, common logical manifest, corpus,
repetitions/order, XFS target, barriers, metrics and elimination rules. No candidate
was implemented/executed. D5 and D6 remain separate later decisions. Earlier
unversioned sources are design references, not evidence of an evaluated build.
