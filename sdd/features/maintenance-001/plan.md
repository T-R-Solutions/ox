# Plan

Full route: preservation contract review, recovery and OPEN-07 decision.
D-01: exact authenticated baseline transformation; R-01: an overly permissive guard.
D-02: current allowlist and directory export; R-02: omitting evidence or depending on the source.
D-03: copies of changed files and observed hashes; R-03: deduplicated recovery loses a version.
D-04: rights analysis per component; R-04: assuming third-party licensing.
Detailed decisions in docs/decisions/maintenance-001.md; REQ-01..04 correspond to
D-01..04 according to traceability.

Primary: software-delivery, .codex/skills/software-delivery/SKILL.md, version not
declared, bridge sdd/chain/software-delivery.md version 1; consulted and used for
the export boundary, identity, independent copy and recovery.
Supporting: skill-creator at /home/rodrigo/.codex/skills/.system/skill-creator/SKILL.md,
without declared version or local bridge; consulted and used only for frontmatter
and content preservation. Consulted entry identities are recorded in
docs/validation/maintenance-001/skills-consulted.json. Validation of the delivery
does not depend on those external paths.

Do not delete or physically reorganize history with active bindings. Preserve
affected observations in previous; new reviews do not renew old results.
Specific gates for ZIP packaging and agent trials not executed in this task
remain explicitly pending if their inputs changed. The 36 technical scenarios
remain UNVERIFIED.

Subsequent decision: GPL-3.0-only for first-party material, according to ADR licensing.md.
T005 implements LICENSE/NOTICE and allowlist inclusion; Rodrigo Batista was
identified as first-party owner and third-party rights remain pending, without
public readiness. The actual ROOT_FILES change requires rerunning export and
preservation tests.

Local update license-holder-001: record the declared owner, reexamine affected
documentary inputs and preserve previous envelopes. No change to code, criteria
or license; technical scenarios and third-party rights remain pending.

## Current acceptance review — 2026-11-01
Local route for inspection and evidence reconciliation; no contract changes. Aggregate execution is distinct from criterion-specific acceptance. Persistence design is a separate unadopted proposal in docs/decisions/local-persistence-proposal.md.
