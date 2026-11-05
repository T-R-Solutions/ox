# Plan

Full route: the preservation comparison contract changes for explicitly authorized
UI metadata files. Preserve unrelated working changes observed before editing.

D-01: Append a bounded revision to files.json and validate its current hashes;
retain original copy hashes and recovery archives. See the metadata inventory ADR.
Replacing historical hashes or exempting all metadata would weaken provenance.

R-01: A broad exception could conceal later modifications. Restrict paths to the
30 original inspected metadata paths and bind predecessor hashes to copy-001.
Keep all other resource and profile checks active. Mutation tests cover rejection.

Primary skill: software-design, `.codex/skills/software-design/SKILL.md`, version
not declared; consulted and used for the smallest shared revision reader and its
callers. No supporting skill or agent delegation. No commits requested.

T001 records revision and decision; T002 updates comparison consumers; T003
collects focused tests, current hash inspection and global diagnostics. Earlier
inspection results remain historical, with new evidence recorded separately.
