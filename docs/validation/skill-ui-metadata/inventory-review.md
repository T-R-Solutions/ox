# Metadata inventory update — 2026-10-29

Authorized goal: include UI metadata changes in the inventory with hashes matching
current files. Full route selected for the bounded preservation contract change;
see sdd/features/skill-ui-metadata-inventory/ and its input-bound evidence.

The new skill-ui-metadata-001 revision contains 30 records, including hashes of
the completed prompt/rust files. Original copy hashes, previous revisions and
archives are retained. Null predecessors mean absent from the original copy,
not necessarily absent from the working tree before this task.

Four focused tests and three existing preservation tests passed. Global check
still exits 1 for commit-governance outside the authorized profile; the UI
preservation diagnostics are resolved. The original inspection.json is historical
and was not rewritten. Pre-edit bytes of the manifest and already modified checker
are retained under inventory-before/. Unrelated working changes were preserved.

Final acceptance/freshness: running the retained
verify-inventory-feature.py.txt with Python returned PASS for this feature's
standard feature_errors gates with require_approved=True and require_fresh=True.
The CLI --features option expects a parent of feature directories, so pointing it
at this individual feature initially produced No feature directories found;
the retained runner selects this feature's diagnostics from the standard gates.
A final global check still reports only the profile discrepancy. git diff --check
passed. The entire governance test suite was not rerun; the seven tests above
cover the changed comparison and existing preservation contracts.
