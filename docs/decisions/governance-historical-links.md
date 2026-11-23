# ADR — Bounded historical Markdown origins and diagnostic projection

Adopted 2026-11-15 by the maintainer's explicit instruction to implement the
[reviewed plan](../validation/governance-link-repair-plan-20261115/plan.md).
Local implementation, focused tests, documentation and independent review/validation
are authorized. No complete pipeline, downloads, central maintenance, commits or
publication are authorized.

D-01: retain the previous origin registry and all snapshots byte-for-byte. Add one
authenticated, versioned registry containing exactly five reviewed source/origin
pairs, bound to the previous registry digest. Missing or changed required registry,
changed source, conflicting inventory, unsafe path or symlink fails closed.
Unknown Markdown retains ordinary link validation. No validation-directory exclusion,
basename inference, target search or implicit legacy mode is introduced.

D-02: current checkout and declared governance copies require the new registry and
five snapshots. The existing distribution includes those sources and their origins;
no source allowlist or missing-target exception expands. Resolving from an original
location proves link validity in the current consumer, not historical target bytes.
Provenance review and presence observations are recorded in the implementation report.

D-03: terminal diagnostics for the Ox checker select recognized failures from both
streams, preserve source identity and expose bounded, sanitized metadata only.
Unknown, malformed, empty and truncated output remains explicit; it cannot change
exit codes or become success. Original streams and result metadata remain authoritative.
Published references must resolve to retained files; retention remains two dates.

D-04: documentary successors are exact-content records with preserved preimages;
they do not refresh historical observations. Changed-input evidence is reevaluated
with independent review/validation. Existing complete feature criteria remain gates.
New captures must retain their origin and identity before being accepted; a displaced
Markdown snapshot is not an ordinary live document merely because it is readable.

Rejected: editing/moving/deleting snapshots, broad exclusions, self-authenticating
metadata, silent optional registries, unrestricted raw terminal output and historical
hash renewal. Revisit on a new capture inventory, distribution boundary, checker
format or retention contract; this decision grants no automatic future exceptions.
