# Reconcile after lost events

Model the watcher as an invalidation hint stream, not an authoritative transaction log. Events can coalesce, overflow or arrive after the underlying file has changed again. On a hint, read the current identity/content under the project's limits; publish an updated snapshot only after the read is validated.

After overflow or restart, mark the affected scope uncertain and perform a bounded rescan. Deleted files need tombstones so old symbols and graph edges do not remain visible. Renames may be represented as delete/create when identity cannot be proven; do not invent a stable identity from matching basenames.

Recovery matrix: staged-only → retain or discard under ownership policy; committed bytes/no completion record → reconcile from hash; unexpected bytes → conflict; unavailable mount → defer, not delete. Test an edit with deliberately suppressed watcher delivery and verify that reconciliation still invalidates stale consumers.
