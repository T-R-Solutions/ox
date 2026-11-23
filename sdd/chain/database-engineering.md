---
skill: database-engineering
skill_path: .codex/skills/database-engineering/SKILL.md
bridge_version: 1
---

# Application persistence, access and integrity

## Select and do not select

Select when the feature has a concrete persistence modeling, transaction, query/access
or migration question and this skill is available at the configured path. Assess
concurrency only when relevant to the invariant or workload. Do not select for a
mechanical/cosmetic change without a persistence question, or merely because another selected bridge mentions this one.
Read the skill's actual activation boundaries; choose one primary skill and auxiliaries
only for unresolved questions. No recursive activation or dependency installation.

## Inputs and contributions

Supply requirement/criterion, decision, risk and task IDs, authorized scope, schema, emitted SQL, invariants, writers, workload and recovery constraints.
Keep unknowns explicit and preserve the destination project's authorities.

| Artifact | Contribution |
| --- | --- |
| Constitution | Reconcile existing principles, security/data and operational constraints; introduce no product policy or fixed target. |
| Spec | Identify persistence invariants, data semantics and, where relevant, rejected concurrent outcomes. |
| Plan / ADR | Connect requirement → decision/risk IDs to schema/transaction/access alternatives, enforcement boundaries and migration risks. |
| Tasks | Name bounded work, actual inputs/tools, stop conditions and expected evidence: schema/query changes, concurrency schedules, backfill and reconciliation. |
| Evidence / convergence | Return criterion/task IDs, environment, observation and limitations: committed data, invariant checks, query measurements and recovery limits. |

## Conditional handoff

Consult an installed engine-specific capability for an unresolved PostgreSQL mechanism only when available and needed; this profile does not install a postgresql skill. Supply IDs, observations, constraints
and existing permission scope. Absence is an explicit gap, not a completed consultation.
The bridge maps contributions; the skill owns its technical procedure.

## Completion and authority

Shared routing, authorization, outcome states and documentation closure follow
[workflow](../workflow.md) and [evidence](../evidence.md). This bridge maps a
selected method to artifacts; it neither activates skills nor changes permissions.
For reuse elsewhere, keep these shared contracts and adapt skill_path to that project.
