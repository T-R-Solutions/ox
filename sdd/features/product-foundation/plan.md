# Plan — foundation transition

Full route: changes the operational contract and package distribution/acceptance.
Actual baseline without Git: docs/validation/implementation-transition/before.tar.gz
and before.json. Recover into an empty directory, compare bytes and preserve any
unexpected version before applying a selective restore.

| ID | Decision / risk | Relationship |
|---|---|---|
| D-01 | Phase in project, policy in constitution, entry point in AGENTS; only GOV-06/07 change | REQ-01, REQ-02 |
| D-02 | Skills/bridges/model preserved; project usage guide; independent product criteria | REQ-02, REQ-03 |
| D-03 | Unchanged allowlist; explicit name and metadata in ZIP and receipts | REQ-04 |
| D-04 | Archive previous bytes and replace only affected evidence/convergence envelopes after new observations | REQ-05 |
| D-05 | Accept internal links to existing directories; preserve the entry document | REQ-05 |
| R-01 | Interpreting phase as unrestricted permission or forcing every correction through the full workflow | REQ-01, REQ-02 |
| R-02 | Confusing available, used and approved skills with product implementation | REQ-02, REQ-03 |
| R-03 | Distributing a governance ZIP as a Rust release or using conflicting metadata | REQ-04 |
| R-04 | Freezing stale evidence or renewing an old result's hash | REQ-05 |
| R-05 | Oracle rejects legitimate history or accepts normative mutations | REQ-05 |

| Capability | Bridge / version | Consulted entry | Role, question and deliverable |
|---|---|---|---|
| software-evolution | sdd/chain/software-evolution.md / 1 | .codex/skills/software-evolution/SKILL.md | Primary: migrate contracts preserving consumers and history; sequence, compatibility and recovery |
| skill-creator | No bridge; environment; version not declared | /home/rodrigo/.codex/skills/.system/skill-creator/SKILL.md | Supporting: integrate skills with SDD without copying process/policies; responsibility analysis and local guide |

Both were selected, identified and consulted. Use: the decisions above were applied
in this change. The autonomous-verification-engineering entry was inspected as a
sample library contract without selecting/activating its method. Do not load the
whole library, install skills or delegate merely by reference.

Alternatives: rewriting 29 skills would couple reusable capabilities to Ox;
duplicating SDD in AGENTS would create competing authorities; keeping active
evidence immutable would break freshness. Plan v1.0 is adjusted on these points,
with old approvals retained in the baseline and explicit review in the current state.

Compatibility: SDD 1.3.0 model, 29 bridge paths, Python commands and profile remain.
The ZIP name intentionally changes; consumers must read the new receipt. No
process, database or deployed application needs migration. Do not infer authorization
to start another product feature from this transition.

Baseline run in docs/validation/runs/20261026T212731.499388Z: SDD and 13 tests passed;
check-ox rejected the existing docs/decisions/ link in the entry plan. D-05 fixes
the false rejection without removing the user's document.

Oracles: mutations to current authorities, package scope, skill states and history,
with restoration; independent-copy test; ZIP qualification with manifest and read
audit. Hashes identify content; they do not prove review. The executor's semantic
review is separate from execution and is not independent human review. Reevaluate
when phase, policy, profile or product pipeline changes.

## Current acceptance review — 2026-11-01
Local route for inspection and evidence reconciliation; no contract changes. Aggregate execution is distinct from criterion-specific acceptance. Persistence design is a separate unadopted proposal in docs/decisions/local-persistence-proposal.md.

## F0 gate preparation — 2026-11-01

Full-route documentary successor: sdd/features/product-f0-gate. Its plan records method selection and requirements for the gate proposal, not adoption of F0 scope. Legacy ACs and the 25-criterion baseline are not reexecuted wholesale. Persistence design belongs to the proposed product-local-persistence feature; implementation remains unauthorized.
