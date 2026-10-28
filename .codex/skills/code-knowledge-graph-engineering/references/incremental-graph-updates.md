# Remove stale relationships deliberately

Maintain reverse dependencies from evidence locations/documents to edges. On a new snapshot, invalidate affected edges before publishing replacements. A deleted function must not remain as a current node merely because a cached layout refers to it.

Use a staged generation or transaction suitable for the selected store. Verify endpoint and evidence consistency before switching readers. If extraction fails midway, keep a coherent previous snapshot labeled stale or publish partial coverage explicitly; do not mix generations without a coverage contract.

Fixture: snapshot S0 contains A calls B. In S1, remove that call and introduce an unrelated C. Assert the A→B edge is absent from S1, present only in historical S0, and queries for C do not inherit B's evidence. Test duplicates, rename ambiguity and dangling endpoints. Store-specific transaction mechanics belong to a persistence specialist only if unresolved.
