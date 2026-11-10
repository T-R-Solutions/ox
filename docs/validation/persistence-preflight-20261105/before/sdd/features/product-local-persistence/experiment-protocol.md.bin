# Paired persistence experiment — decision-ready proposal, 2026-11-05

Status: PREPARED, NOT AUTHORIZED OR EXECUTED. This supplements the ADR's E01..E08;
no additional acceptance criteria, candidate implementation or winner is introduced.
The adopted F0-D1..D5 already place persistence after F0 and before F3/MVP. D1's
milestone question is resolved; D2/D3/D4 below remain open. AC-01..07 remain UNVERIFIED.

## Common logical contract (D2)

Use store_id/task_id/attempt_id/operation_id/observation_id, independent of paths,
PID or session clock. IDs are opaque strings; fixtures use explicit stable labels.
An operation stores payload_version and complete canonical logical payload; identical
ID/payload returns its existing result, different payload is a conflict without writes.
Checks retain ID, description, criterion version, absolute executable identity and
bytes, arguments in order, directory, expected exit, declared input path/bytes and
before/after identities. Record run, result (exit/code, cancellation, timeout or unknown),
source/method, observed time with clock provenance, schema, tool/build identities,
completeness and explicit missing/unknown tags. Timestamp is not identity or ordering.
Observations are immutable; revisions append observations with references, never
rewrite failing bytes. All references must resolve within the committed logical cut.
NOT APPLICABLE requires its rationale; persisted approval is historical only until
current input/oracle/argument/criterion revalidation. Five states remain distinct.

Commit durable intent before admitting an external effect. Intent, effect and
confirmed observation are three separate facts. Observer acknowledgement is a
sequence in a supervisor-owned log written outside the candidate process. A timeout,
closed pipe or missing reply means uncertain outcome, not failed commit. Query operation
ID before safe retries; interrupted intent never triggers automatic effect replay.
Complete observations and all references publish atomically. Acknowledged valid
transactions survive process death; unacknowledged transactions may be absent or
fully committed. No partial visibility, invented approval or silent volatile fallback.
Corrupt stores are not repaired in place: retain original bytes and explicit error;
recover only a validated complete generation/transaction or require recovery.

Initial policy proposed: one cooperating process owns the entire store writer lease,
not merely one SQL transaction at a time. Contender refuses before effects. Lock
release/reacquisition after process death is tested. No stale-lock deletion by age.
Migration: pre-backup, source version guard, publish complete target only after
validation, interrupted recovery or original restoration; future versions refuse
without changing bytes. Backup: pin one logical cut including referenced evidence,
copy to fresh destination, manifest/hash check and independent restore process.
No deletion, compaction or retention eviction is implicit in this experiment.

## Serializer-independent manifest and corpus (D4 proposal)

Before candidate code, author a UTF-8 logical entity table, external raw payload files,
and expected verdict/dependency table; freeze SHA-256 of each. Candidate encoders
must not generate expected values. Byte comparison uses raw evidence; table comparison
sorts entities by IDs and references, preserving ordered arguments, byte strings,
unknown/absent distinctions and rationales. Compare against both encoders and an
independent reviewer/validator. Hashes detect tested modifications, not authenticity.

Base fixture M1: store S1, task T1, attempts A1..A5, operations I1..I5 (intent) and
O1..O5 (observations), observations V1..V5. Checks C1..C5 share independent oracle
fixture identity but separate input labels P1..P5; args are [P_i], expected exit 0.
Each observation has before=after 16 bytes, byte j = (i+j) modulo 251, j=0..15.
V1 exit0 => APPROVED; V2 exit17 => REJECTED; V3 timeout => INCONCLUSIVE;
V4 missing post-input => UNVERIFIED when current evidence is absent;
V5 is a justified NOT APPLICABLE claim with rationale "fixture platform excluded",
not a fabricated execution. Unknown exit is tagged unknown, never zero. Intent
payload contains task/attempt/command; observation payload references the intent,
check, evidence and result. Include task T2/A6/I6 with durable intent but no confirmed
effect: restart reports interrupted/unknown and the effect counter stays unchanged.
The exact timestamps are fixture strings, not sampled clocks. Expected historical
states and current revalidated states are separate columns. Removing P1 makes only
C1 UNVERIFIED; changing C2 arguments affects only C2; restoring bytes does not erase V2.

Corpora: M0 empty; M1 above; M32 extends the same five-state pattern to 32 observations,
4 KiB per before/after evidence payload, stable IDs; ML contains two complete
observations with two 15 MiB inputs in each before and after (120 MiB raw retained
content plus oracle/provenance). Actual admitted size includes executable bytes;
reject over 128 MiB before effect, preserving old history. These sizes derive from
existing F0 bounds; they propose an experimental workload, not a durable lifetime
quota. Include exact-boundary and one-byte-over-limit payload admission in E07.
Generate expected bytes from the stated arithmetic, independent of candidate code;
freeze the actual complete entity/verdict tables before implementing either encoder.

For each corpus run E01..E08 in numeric order on fresh copies. Three warmups and
20 measured repetitions for non-fault costs; ten repetitions per fault/cut/corpus,
balanced SQLite/snapshot then snapshot/SQLite alternation by repetition parity.
No random faults: deterministic sequence, seed 20261105 only if fixture expansion
requires a PRNG (algorithm must then be frozen before runs). Do not drop outliers.
Cold-cache cost is not claimed: new process per recovery, OS cache not flushed.

## Environment and proposed configurations (D4)

Target the current Linux x86_64 host, Rust 1.99.1, edition 2024, local XFS observed
by findmnt on the workspace mount. Record kernel, CPU, RAM, mount flags, available
space, toolchain/lock, executable hashes and no competing benchmark jobs before runs.
Use an owned `.local/build/persistence-experiment-<run>/` under this mount, not /tmp
unless its filesystem is independently recorded and explicitly selected. No live
product store; export evidence to a separate new directory before cleanup.

Propose SQLite via exact rusqlite 0.41.1, bundled native SQLite, backup feature,
no extension loading; pin resolved libsqlite3-sys, amalgamation source ID/checksum,
build flags, licenses and lockfile in the isolated experiment before execution.
The published driver lists libsqlite3-sys ^0.39.0; this is not an exact native-engine
selection. D4-deps is a mandatory pre-run freeze review: no engine guarantee or
run until exact resolved native version/source ID and its release-specific primary
docs are recorded. Alternative: system SQLite with exact package/source identity;
recommend bundled for reproducibility, conditional on dependency review. No package
is cached here and no download/build of either candidate was performed.
Propose rollback journal DELETE, synchronous FULL, foreign_keys ON, explicit
transactions and application writer lease; read back effective settings. Do not
use WAL as an incidental optimization. SQLite backup API plus evidence manifest;
integrity and foreign-key checks plus application payload hashes/reference checks.

Snapshot candidate: versioned immutable generations, complete entity manifest and
payload lengths/hashes, std safe file lock (or separately reviewed lock dependency),
write/flush/sync temporary generation, validate, publish generation selector by
same-filesystem rename, sync containing directory, retain previous generation.
Define selector recovery without silently dropping an acknowledged generation;
ambiguous/corrupt selector requires explicit recovery. Pin format v1 and every file
in its publication protocol before runs. These are design obligations, not observed
guarantees. Journal remains documentary unless a demonstrated gap and later grant
add it. Both candidates use the same payload verification and process-effect harness.

Proposed experiment-only limits for approval/amendment: 1 GiB store admission quota,
4 GiB total run workspace cap, 512 MiB candidate peak RSS, writer fail-fast without
retry, 5 s recovery/restore/error reporting watchdog. Justification: room above the
120 MiB corpus for current/previous generations plus copies, and bounded runs while
collecting baseline costs. Reaching the run cap stops new runs and exports evidence;
never delete damaged bytes to fit. These values are not adopted product requirements.
Propose using the existing <=120 ms UI response contract as an experiment hypothesis,
measured separately, without transferring the F0 small-workload result to storage.
If limits are changed after baseline, preserve baseline and rerun both affected sets.

## Cuts, faults and independent observations

Use pipe/file readiness barriers with supervisor acknowledgements, never sleep-based
kill guesses. E02: B0 before intent; B1 after durable intent acknowledgement; B2 after
external effect counter is written/observed; B3 before observation transaction commit;
B4 commit returned internally but no reply sent; B5 supervisor observed reply. Pause
at each hook then SIGKILL only the owned candidate, wait/reap, reopen in new process.
Record all barrier/effect/ack sequences and expected allowable complete manifests.
B1 intent persists, no automatic effect; B2 unfinished effect remains uncertain;
B3/B4 observation may be absent or whole; B5 acknowledged observation must exist.
Both candidates map physical hooks to these cuts; document uninstrumented internal
windows. Additional internal write cuts in E03 complement these logical cuts.

E03: truncate header/manifest/payload and alter one evidence byte on owned copies;
kill around physical publication/write hooks. Preserve damaged bytes + hashes before
recovery. E05 barriers before migration backup, during target writes, before publication,
after publication before reply. E06 pin backup cut, pause after first copy chunk and
let writer advance, then restore independently; a completed cut must match exactly.
E08 synchronize two writer requests; losing process launches no effect. Duplicate
same payload returns same identity/result; conflicting payload leaves bytes unchanged.

Permitted proposed faults: SIGKILL of experiment-owned processes, corruption/truncation
of owned copies, real permission-denied using a nonprivileged process, actual ENOSPC
only in a separately authorized bounded disposable filesystem. No host disk filling,
mount operations, OS crash, power cut or live-store modifications. Until disposable
filesystem permission exists, ENOSPC via injected write failure is explicitly simulated;
real ENOSPC stays UNVERIFIED and limits selection confidence. Injected driver/API
errors are distinguished from real storage/process observations in every result.
A watchdog detects nonresponse and records UNVERIFIED/REJECTED as appropriate; it
does not prove universal interruption of blocking filesystem calls.

## Metrics, gates and decision packet

Use monotonic timing from admitted operation to durable reply; separately record
intent latency, observation write, recovery-to-query/revalidated display, backup and
independent restoration. Retain raw durations, median/p95/max, number of samples,
failures/timeouts; compare paired differences and ranges without significance claims.
Record process peak RSS (/proc sampling cadence and /usr/bin/time high-water mark),
logical bytes, allocated file blocks including sidecars/old generations/backups and
/proc I/O write_bytes deltas (cache/kernel limitations explicit). Do not confuse
logical payload bytes with physical device writes. Record harness overhead separately.

E07 uses the same disposable Iced worker/error shell for both candidates, real input
and rendered response observations on X11 and Wayland; measure event-to-visible
feedback, cancellation/close-to-worker completion, sampled RSS and admitted queue
size. A worker heartbeat alone cannot accept product AC-06. The shell is experimental,
so all integrated product UI criteria still require later D6 implementation evidence.
If the shell is not authorized, E07 graphical evidence stays UNVERIFIED and selection
must state the unresolved integration prerequisite; no fabricated UI score.

Eliminate on lost acknowledged valid history, partial records, false approval,
duplicate effects, violated writer policy, accepted future schema, destructive
corruption handling, failed consistent restore or unsafe migration. A missing
critical oracle prevents selection. Proposed numerical bounds become gates only
if adopted. If both pass correctness, compare cost at each corpus plus concrete
custom recovery/locking/migration code and dependency/build/maintenance obligations.
No weighted score or winner before results. If trade-offs remain, request D5 with
measured alternatives; if neither passes, repair/retest both affected inputs or
revisit contract explicitly. Product AC-01..07 cannot be approved by this packet.

## Maintainer decisions and exact next step

| Decision | Alternatives / recommendation | Evidence and uncertainty | Execution/acceptance impact |
|---|---|---|---|
| D1 milestone | Already adopted: separate post-F0/pre-MVP delivery | F0 boundary ADR and project successor | Do not ask again |
| D2 contract/failure envelope | Adopt common contract above (recommended), or amend specific invariants/envelope | Existing in-memory semantics and primary docs; no storage observation | Must precede experiment; process death only, OS/power excluded |
| D3 disposable experiment grant | Authorize paired candidates and disposable Iced shell (recommended), or authorize backend only/defer | Protocol prepared; no implementations | Backend-only leaves graphical E07 UNVERIFIED; grants neither D5 nor D6 |
| D4 operations | Adopt corpus/order/limits/location/fault permissions above, or amend named fields | XFS/toolchain observed; costs not measured | Freeze before runs; limits remain proposals until adopted |
| D4-deps | Authorize isolated dependency resolution/review for rusqlite 0.41.1 bundled (recommended), or exact system build | Published driver primary docs; native source not resolved | Exact native version/source/lock/license/config freeze must be reviewed before runs; no product lock change |
| D5 technology | SQLite/snapshots/neither, only after results | Both UNVERIFIED now | Separate decision after shared gates and risk review |
| D6 product integration | Later bounded ox-storage/Engine/controller/Iced delivery or defer | No implementation evidence now | Separate authorization and operational AC-01..07 acceptance |

Approval can name D2, D3, D4 and D4-deps with amendments. Next authorized action
would be creating the disposable harness, freezing hand-authored manifests and
resolving the isolated dependency lock/source ledger for the pre-run freeze review;
only after that review may candidates run. No routine approval between individual
tests is intended. Product technology/integration stay separate decisions.

## Primary technical sources and claim classification

Consulted 2026-11-05: [Rust Child 1.99.1](https://doc.rust-lang.org/stable/std/process/struct.Child.html)
(version shown in consulted page): no implicit child Drop/reap; wait may block.
[Linux open(2)](https://man7.org/linux/man-pages/man2/open.2.html) and
[Linux UAPI flags](https://raw.githubusercontent.com/torvalds/linux/master/include/uapi/asm-generic/fcntl.h)
explain nonblocking FIFO open; they do not bound ordinary-file I/O or establish atomic capture.
[SQLite transactions](https://www.sqlite.org/lang_transaction.html),
[atomic commit](https://www.sqlite.org/atomiccommit.html),
[backup API](https://www.sqlite.org/backup.html),
[PRAGMA](https://www.sqlite.org/pragma.html),
[rusqlite 0.41.1](https://docs.rs/crate/rusqlite/0.41.1) provide design references.
SQLite pages are unversioned: applicability must be checked against D4-deps source
before tests. No SQLite/driver guarantee has been accepted from this preparation.
Integrity PRAGMA alone is not complete application provenance/corruption detection.
Lower maintenance cost, adequate snapshot rewrite performance and durability on this
XFS are hypotheses. Only the observed findmnt/toolchain and robustness tests are
local observations. Process-kill survival is not OS-crash or power-loss tolerance.
