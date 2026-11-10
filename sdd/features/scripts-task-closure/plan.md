# Plan

D-01 / R-01: Replace the imported multi-stack configurable executor with one fixed Python stdlib entry. Its arbitrary task overrides, fictional pins, scanner policies and project discovery add contracts without current consumers. Reusing it intact or keeping wrappers would preserve misleading commands. Existing tools/governance and sdd/tools remain the authorities. No imported implementation is retained; original license stays in recovery, no copied component is relicensed.

D-02 / R-02: Back up all 92 imported files and intended existing write paths to /tmp/ox-scripts-integration/recovery before changes. Compare bytes immediately before each removal/replacement. This is a cooperative local workspace procedure, not protection against a malicious racing writer. Recovery is outside the active tree/distribution. Restore selected files only after comparing newer work.

D-03 / R-03: Governance runs structural SDD, existing Ox checks and fast tests; full adds all governance tests and Rust. Rust runs fmt/check/build/test/clippy offline and locked as applicable. Building helpers before tests preserves documented process fixtures. No GUI interaction is automatic. Default scope is mandatory, no inferred Git selection, no custom command configuration.

D-04 / R-04: Add bounded content-authenticated succession for changed authority files, preserving exact predecessors and historical evidence. Do not refresh historical evidence. D-05: an independent-copy regression requires explicitly adding the two resulting script files to ROOT_FILES; directory allowlist, recovery exclusion, catalog/profile and package generation remain unchanged. Existing intentionally UNVERIFIED features do not require global approval. Current raw evidence may expose affected stale observations; report those independently.

Primary: software-design, .codex/skills/software-design/SKILL.md, bridge sdd/chain/software-design.md version 1; content SHA256: 4e214fd5dbf141ee437814a5c817b6924a05e8ad75cf6bc208281155204f6143. Used to compare responsibilities and eliminate unused configurable adapters (D-01/T002).
Supporting: workspace-integrity-engineering, .codex/skills/workspace-integrity-engineering/SKILL.md, bridge sdd/chain/workspace-integrity-engineering.md version 1; content SHA256: 3156e92baceb75376182423952607da665ff2c8db0d8cdc4296b44431b5c915a. Used for backup, write preconditions and explicit recovery limits (D-02/T001). No other skill consulted or activated. Skills themselves remain reusable and unchanged; the local interchange guide owns the closure mapping.

## Shell successor — 2026-11-06

Operational Python and repeated wrappers are superseded by scripts-shell-refactor.
The observations above are historical. Current inputs and adapter acceptance are
recorded in that feature; previous affected observations are retained verbatim
in evidence.json and are not renewed by changing hashes. Missing real scanners
remain UNVERIFIED. Active entry: bash scripts/automate.sh.

## Preference successor — 2026-11-06

D-06 / R-06 / REQ-04: remove the automatic closure blocks from AGENTS, workflow, evidence,
root README and the skills interchange guide; remove obsolete command examples
from project context. Keep acceptance semantics and historical/scanner references.
The commit skill owns the optional execution gate; neither hooks nor product code
change. Preserve pre-edit bytes under .local/commit-choice-before and inspect the
bounded diff against those bytes, rather than the already dirty Git baseline.

Primary: skill-creator, /home/rodrigo/.codex/skills/.system/skill-creator/SKILL.md
(environment skill, no SDD bridge); contribution: narrow update to the existing
skill, explicit answer handling and failure boundaries. Supporting: commit-governance,
.codex/skills/commit-governance/SKILL.md (existing conditional skill, no bridge);
contribution: integrate the gate before staging and preserve authorized scope.
Versions are the pre-edit SHA-256 identities in commit-choice-inputs.json. No other
technical skill was used. Validation: skill validator, structural SDD check, bounded
manual scenario review and diff review. The automation itself is not invoked by
this documentation request.
