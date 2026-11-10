# ADR — Shell automation with shared modules

Authorized by the maintainer's explicit 2026-11-06 refactoring request.

D-01: Operational scripts under scripts/ use Bash .sh. Python there is only for
tests. Existing Python governance authorities outside scripts/ remain independent
tools invoked by the shell coordinator. jq handles JSON; no embedded Python,
renamed Python implementation or alternate implementation outside scripts/.

D-02: One automate.sh entry and one check registry replace repeated wrappers.
lib/ owns shared execution, paths/snapshots, command definitions and reports;
checks/ prepares/runs scanners; security/analyzers/ and reports/ expose standalone
consumers of the same libraries. Retain local rules and attribution.
This supersedes only the Python coordinator and wrapper layout decisions in the
two earlier scripts ADRs. Their offline controls and capability requirements remain.

D-03: Preserve bytes, raw outputs, exits and prior observations. Exact registered
authority successors normalize to authenticated preimages; unknown changes still
fail preservation. Root .local/ is generated runtime data, excluded from source
document/link checks, while actual source documents remain checked.

D-04: Subprocess regression tests, Bash syntax, real installed ShellCheck and
Gitleaks, and available governance/Rust checks establish bounded acceptance.
Missing scanners/datasets/license policy are explicit blockers for those audits;
test doubles establish adapter contracts only. No installations, downloads,
product edits, global approval, commit or publication.

Rejected: retaining Python behind .sh wrappers, duplicating report parsers,
generic arbitrary-command configuration, or removing unavailable scanners.
Revisit when the shell/JSON dependencies or scanner CLI/schema contracts change.
