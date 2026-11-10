# Retention proposal, no deletion performed

retention-inventory.json records allocated sizes for Ox checks, validation, build
artifacts and shared toolbox run/data volumes. Docker daemon layers are not measured.
Large validation archives and per-run source/database copies are not automatically
redundant: they may be exact observed inputs. Keep raw logs, command/exits, accepted
artifacts, manifests, predecessors, image locks and referenced dataset receipts.

Proposal for owner review: index references from active and historical evidence
before selecting any run for retirement. Unreferenced generated build/cache data
can be proposed separately from evidence. Archive completed referenced runs with
original paths plus a verified manifest and tested recovery, and only then consider
cold storage. Deduplicate bytes in a future content-addressed archive with an
explicit relocation successor; do not replace required files with unchecked links
or silently rehash past observations. Toolbox data is managed by its owner; any
prune starts as an identified per-project dry-run and requires its own permission.
The earlier selective migrated-database cleanup is recorded independently and was
not repeated by this recovery. No retention period or destruction is adopted here.
