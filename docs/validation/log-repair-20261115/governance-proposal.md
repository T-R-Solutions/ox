# Proposal requiring independent review

The exact sdd/project.md intermediate 82c57cdebb84cd3a620e02de99cc91485076c8d389b9644016dc09ebb13bcfa1
from the 14 November registry is unavailable. Search all validation files below
200KB plus candidate snapshot truncations found no match. Do not claim exact
reconstruction or historical replay of this intermediate; that remains UNVERIFIED.
The earlier authenticated a0d9bbfbde1db828db87a08475dadb37ebc28683ef4e6c0f3b8d810c187472d2
preimage exists unchanged. governance-project-proposal.diff shows the complete
new terminal vs that preimage. All changes to project context/current/history
require real review. The old pinned registry and its hashes remain immutable.

Proposed new independent exact-content terminal-to-original transition for project,
with explicit chain_base=original. Other new transitions use chain_base=terminal
and exact 14 November terminal preimages. New registry bytes pinned in code;
preimage/current path, bytes and no-symlink checks; reject unknown mutation,
recalculated metadata, missing or changed original, terminal downgrade.
Instruction errors validates exactly the registered new project terminal, then
permits its normalized original a0d9 through preservation. All other instructions
continue expecting their previous terminal. No wildcard/path approval. Missing
new registry never accepts changed bytes. Existing exact-original recovery tests
remain; any test requiring82c57 replay stays blocked and must not be relaxed.

This authenticates only a newly reviewed present state with available original.
It is not evidence that the missing intermediate was inspected or executed.
