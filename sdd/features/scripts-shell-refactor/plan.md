# Plan

D-01 / R-01: Replace Python orchestration with Bash .sh modules and jq for JSON,
GNU coreutils/find for byte-safe files and hashing. Bash is the existing shell
contract; POSIX-only sh would complicate argv arrays and error propagation.
Keep only one public automation entry, standalone analyzer/report entries and
one scanner runner; remove redundant aliases. No eval or arbitrary commands.
D-02 / R-02: Keep scanner flags and strict classification. Fail closed on malformed,
duplicate or incomplete reports and unreviewed data. Centralize process capture,
source selection and identities. Rust metadata comes from installed Cargo only;
no regex-based general TOML parser or Python embedded in shell.
D-03 / R-03: Preserve initial bytes in docs/validation/scripts-shell-refactor/before;
exact-content succession maps only reviewed authority changes to prior bytes.
Existing Python tools/governance and sdd/tools are outside the conversion scope.
The existing governance transient filter must exclude root .local runtime output:
scanner snapshots deliberately omit historical documents, so their Markdown links
are not standalone repository links. Keep validation of all real source documents.
D-04 / R-04: Test shell through subprocesses using Python unittest; test doubles
exercise adapters, real closure runs establish available checks. No scanner
installation, network refresh, product edits, GUI acceptance, commit or publication.

Primary skill: software-design, .codex/skills/software-design/SKILL.md;
bridge sdd/chain/software-design.md, bridge_version 1, content SHA256
4e214fd5dbf141ee437814a5c817b6924a05e8ad75cf6bc208281155204f6143.
Consulted and used to separate registry/process/files/report responsibilities,
compare wrappers against one entry, and preserve observable failures (T001/T002).
No supporting skill or delegation used.
