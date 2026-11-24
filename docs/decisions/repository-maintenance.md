# ADR — Repository maintenance and local artifact lifecycle

Adopted under the maintainer's 2026-11-09 explicit sequential maintenance request.
Feature: `repository-maintenance` (processo; sem spec viva, recuperável pelo histórico do Git).

D-01: Delete only demonstrated obsolete/disposable material. Preserve historical
hash-bound duplicates, portable skill resources and inconclusive local data.
D-02: The workflow owns per-task documentation closure; shared skill integration,
bridge index and templates link to it. No duplicated policy in 31 individual skills.
D-03: A shared shell resolver owns local paths. Keep checks/security/cargo-home
compatible; group loose historical records under records/legacy with a reversible
manifest. Preserve legacy paths with unresolved consumers and embedded references.
D-04: Retention follows lifecycle rather than guessed age/quota: an owned complete
run is explicitly released only after a complete retained byte-identical copy exists.
Explicit apply revalidates the copy and lease, journals, renames to trash and deletes.
Interrupted partial deletion resumes against retained bytes. Latest and previous
cleanup receipts bound audit growth; permanent evidence is outside cleanup.
D-05: Authenticate exact authority successors against preserved preimages. Reexamine
only dependent documentary observations, preserving operational product evidence.

Rejected: deleting 44+ GB because it is old/large; moving all legacy directories
without analyzing embedded paths; keeping per-producer path definitions; weakening
acceptance to ignore documentary changes. Consequence: substantial legacy data stays
pinned; this is documented preservation, not automatic reclaimable space.

Review when producers, retained-copy guarantees, filesystem concurrency assumptions,
Cargo environment or evidence consumers change. No product features, commits,
publication, global installs or central repository changes are authorized here.

## Superseding local retention decision — 2026-11-11

Explicit maintainer request replaces the retained-copy prerequisite, pinned legacy
artifacts and old local layout. Only logs remain in `.local/logs/YYYY-MM-DD/`;
keep two dates, removing the oldest before a third. Delete backups rather than
moving them to recovery/trash. Operational Cargo/RustSec/tool inputs move without
copying to `.cache/ox/`; original supplied design references move to `.inputs/design/`.
The shell-only production contract stays intact. Temporary scanner snapshots are
execution inputs and are removed on completion, including publication failure;
uncatchable termination remains a documented limitation. Existing source changes
are preserved. Historical validation reports remain historical and are not rebound
to changed inputs by merely updating hashes.
