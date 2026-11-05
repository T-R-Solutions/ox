# ADR — Skill UI metadata inventory revision

Adopted on 2026-10-29 under the maintainer's explicit request to register the
metadata changes and update their expected hashes.

Append `skill-ui-metadata-001` to `docs/structure/files.json` for exactly the
30 `agents/openai.yaml` files identified by the original UI inspection. Record
the SHA-256 of their current bytes and the original copy hash where one exists
(`prompt` and `rust`); use null for files absent from the original copy.

Historical revisions, archives and inspection results remain unchanged. The
current checker validates the new revision, its coverage, predecessor bindings
and current file hashes. Only these metadata paths use the new expected hashes;
all other preservation rules remain in force. Future changes require a new
reviewed revision, rather than silently refreshing this revision's hashes.

Replacing original copy hashes was rejected because it would misrepresent
provenance and conflict with recovery archives. Ignoring metadata files was
rejected because subsequent modifications must still be detected.

The 29-skill profile and the separate commit-governance inventory discrepancy
are outside this request. No profile, bridge, application or policy is changed.
Review when UI metadata changes again. Acceptance is recorded in
`sdd/features/skill-ui-metadata-inventory/`.
