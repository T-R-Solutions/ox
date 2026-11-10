# Pre-execution configuration contract v1

Design for review only. No encoder or backend is implemented. Exact dependencies
are Cargo.toml/Cargo.lock here and the identical isolated package under
.local/build/persistence-experiment-preflight-20261105/dependencies/.
Native source bytes/flags/licenses: native-source.json and resolved-dependencies.json.
Lock checksums identify every registry package; source copies remain in the isolated
build directory. No application/ manifests or sources were edited by this step.

Both candidates acquire a safe std::fs::File::try_lock exclusive lease on the same
store-root writer.lock inode, held open for the full writer lifetime, before any
intent/effect. Never unlink/replace the lease file, never remove a lock by age.
Readers/recovery writers respect the lease. Contender fails immediately without
retry or effect. A killed writer releases its OS lease; reacquisition and two-process
exclusion require E08 observation. This is a design obligation on the effective
Rust 1.99.1/Linux filesystem, not a tested guarantee. Backup reads pin a logical cut.

## SQLite

Fresh owned store.db, no attached databases; keep referenced payload bytes inside
transactional storage for the experiment. Atomic observation includes all payloads,
checks/provenance/references. Primary keys on stable entity/operation IDs, foreign
keys on references; store canonical payload bytes plus digest and compare full bytes
for ID reuse. A hash match alone cannot approve identity. No UPDATE of observations.
Store-level lease is independent of SQL transaction locking.

Before effects, set and read back outside any transaction:

```sql
PRAGMA journal_mode=DELETE;
PRAGMA synchronous=FULL;
PRAGMA foreign_keys=ON;
PRAGMA busy_timeout=0;
PRAGMA journal_mode;
PRAGMA synchronous;
PRAGMA foreign_keys;
PRAGMA busy_timeout;
SELECT sqlite_version(), sqlite_source_id();
PRAGMA compile_options;
```

Expected journal_mode=delete, synchronous=2, foreign_keys=1, busy_timeout=0;
version/source ID must equal native-source.json. Reject mismatch before effects.
No extension loading API/SQL enabled. Bundled compile flags do include extension
capability; absence of driver load_extension feature alone is not a native omission.
Explicit BEGIN IMMEDIATE/COMMIT for intent and, separately, complete observation.
No retry callback around effects; query uncertain operation ID after restart.
Validate integrity_check='ok', empty foreign_key_check and all application hashes,
lengths/references before exposing a loaded historical result. Revalidate current
inputs before current acceptance. PRAGMAs alone do not validate provenance.

Backup: dedicated read connection pins a read transaction/logical cut, incremental
backup into a fresh destination with deadline and no retry loop. External manifest
identifies cut/entities/source/config. Writer continuation, pin semantics, backup
completion and restoration are E06 obligations. Never copy only a live main file.
Migration version guard before mutation, verified pre-backup, explicit transaction;
future/unsupported/downgrade refuse before writes. Recovery preserves originals,
including journal/sidecars. Corrupt bytes are copied and hashed before attempts.

## Snapshot file format v1

UTF-8 JSON metadata: integers only for sizes/versions/sequence, no duplicate keys;
canonical bytes use sorted keys, compact separators, UTF-8 without ASCII escaping,
no final newline for digests. Payloads are raw files. All references are IDs/relative
paths with no absolute paths or traversal in store metadata. Logical source paths
are separate fields and do not authorize access. Unknown/absent use explicit tagged
objects. Every entity and operation is as specified by M*.json; record digests bind
full check/observation payload, not only labels. Validations reject duplicate IDs,
missing references, unknown states, malformed rationales and payload conflicts.

Layout:

- writer.lock: permanent lease inode.
- generations/<sequence>-<manifest-sha256>/manifest.json: format_version=1,
  store_id, sequence, parent manifest hash (null only at genesis), complete entity
  arrays, operation index and payload table {id, relative path, length, sha256}.
- generations/<id>/payloads/<sha256>.bin: complete immutable raw payloads.
- CURRENT: JSON {format_version:1, generation:<id>, manifest_sha256:<hex>}.
- PREVIOUS: same structure for last complete selected generation; recovery aid,
  never justification to silently lose a confirmed generation.
- staging/<owned-id>/: unpublished files; never trusted merely because present.

Under lease: write new generation on same filesystem; flush buffered writers,
sync_all every payload/manifest; independently validate complete generation;
sync_all generation directory; rename staging generation to final name; sync_all
generations directory. Persist PREVIOUS via temporary-file flush/sync, same-dir
rename and root-directory sync; write CURRENT.tmp, flush/sync, same-dir rename to
CURRENT, sync_all root directory. Only then send reply. Supervisor records observed
ack separately. Keep old generations and damaged bytes; never auto-delete to fit.
Each durable intent is its own complete generation; next observation generation
contains intent plus complete observation/reference cut. No effect before durable
intent acknowledgement.

Recovery under lease validates selector, version, whole manifest, all payloads and
references; only whole validated cuts are eligible. Valid CURRENT resumes with
uncertain operations queried by ID. Unpublished staging is recorded as incomplete,
never promoted solely by sequence/time. Missing/corrupt/ambiguous selector yields
explicit recovery-required and byte-preserved candidates. PREVIOUS may be restored
only with explicit recovery evidence that no confirmed cut is lost; otherwise error.
No repair in place. Unsupported version: inspect/reject without write.

Migration: backup pinned complete source, validate it independently, build new
schema generation and validate equivalence, publish with same ordering. Interrupted
publication recovers original or whole target, never partial. Backup copies a pinned
immutable generation to a fresh destination and validates full manifest before
restoring into another fresh directory. Changed/missing external inputs invalidate
current acceptance despite intact historical bytes.

No process-kill result proves OS-crash or power-loss durability. Quota accounting
includes staging, old generations, SQLite sidecars and backups. Run cap stops new
work without deletion; export evidence separately. Effective locking, sync ordering,
all publication cuts and backup behavior remain UNVERIFIED until authorized trials.
