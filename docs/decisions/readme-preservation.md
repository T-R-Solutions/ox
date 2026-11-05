# ADR — README preservation successor

Adopted for the maintainer's 2026-11-04 “corrija”, following the reported exact-byte
README integration failure after the authorized documentation rewrite.

D-01: retain readme-skill-integration-001 and its hashes unchanged. Register only
README.md in docs/validation/readme-preservation-20261104/revision.json. Exact
current content resolves to the original integration content saved under before/,
whose hash must also match that original registration. Existing intermediate
README versions remain in the preceding documentary review records.

D-02: skill_revision normalizes this successor before its existing original-current
comparison and predecessor lookup. Unknown mutations remain raw and fail. Reject
unexpected scope/version/decision, duplicate JSON properties, invalid hashes,
missing or escaping files, symlink path components and corrupt preimages. This is
content provenance, not permission or proof of documentary usability.

D-03: test positive and negative cases, the independent governance copy and recovery.
Preserve prior evidence inputs by exact bytes and append new observations for
changed contracts/consumers. Reexamine AC-04 instead of promoting the historical
navigation result. Product code, dependency lockfile and F0 runtime measurements
are unchanged; no new runtime or release acceptance follows.

Rejected: disabling the guard, replacing an old registered hash, allowing all
Markdown revisions, or treating current-source hashing alone as successful testing.
Review when README bytes, registry scope or predecessor/comparison behavior changes.

D-04: the independent governance copy exposed product hyperlinks introduced by
previous documentation edits, pointing outside the deliberately exported scope.
Register exact source-document hashes and exact existing product targets in
product-references.json. In a tree without application/, only these registered
references may name excluded product files. Full source trees still require local
targets. Unknown links, changed source bytes, escapes and governance-file deletions
remain failures. No product files are added to the governance package. This is an
explicit source-versus-governance reference contract, not a blanket broken-link waiver.
