# Instruction history within the shared succession protocol

Status: accepted design; implementation review and execution are separate gates.

The R3 vendor repair adds AC-05 to dependency-hygiene and its current convergence
projection. The complete historical instruction consumer rejected that new row:
its immutable 14 November registry fixes the earlier whole convergence document.
The old terminal remains an observation of history, not a perpetual prohibition
on reviewed criterion evolution. The before bytes retained by R3 exactly match
that authenticated historical terminal.

Decision: extend the same schema-2 active registry and document_ledger protocol
with the typed instruction-governance-20261114 historical anchor. It authenticates
only instruction_revision.records: registry and decision bytes under the existing
historical contract. No path exception, fallback, new successor module, or routine
Python hash update is introduced. Initial before bytes must match the historical
terminal sha256, never its previous_sha256. Later versions use the existing
contiguous chain, before/after, decision and independent-review bindings.

Both instruction consumers normalize the active live terminal before historical
comparison; supplied unknown buffers remain distinct. Metadata authentication is
kept separate from predecessor traversal to avoid recursion. The observation
readset includes the instruction registry and decision. Historical preimages are
carried in fixtures and remain authenticated by the original consumers when used;
the metadata-only anchor does not claim to validate their contents itself.
Active projection also rejects the older endpoints already identified by each
typed historical registry, including its pre-terminal predecessor. This applies
even to non-strict projection; an unknown supplied buffer is not a live downgrade.

Alternative: allow convergence sections by validating projection semantics against
spec/evidence. That would require a new projection grammar, normative section
boundary and larger readset, while broadening live-document mutability. It is not
the smaller repair here. Existing authorities still use section contracts and
cannot switch to whole-document active succession. Re-pinning the historical
terminal, removing AC-05 or accepting missing metadata would recreate or conceal
the defect and was rejected.

The declared-review/VCS trust limits of the existing active registry are unchanged.
This protocol does not authenticate human permission or defend against coherent
rewriting of the entire checker/registry. Future instruction-governed document
updates require reviewed data transitions, not changes to Python per path.
Acceptance requires real consumers/copies, baseline/authorization/log-append
scenarios, unknown inputs, downgrade/corruption/path negatives and the full suite.
Earlier ADRs and historical observations remain byte-for-byte preserved.
