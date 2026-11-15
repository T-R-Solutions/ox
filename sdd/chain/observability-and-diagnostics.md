---
skill: observability-and-diagnostics
skill_path: .codex/skills/observability-and-diagnostics/SKILL.md
bridge_version: 1
---

# Instrumentation and evidence-led diagnosis

## Select and do not select

Select only when the feature has a concrete instrumentation or evidence-led diagnosis question and this skill
is available at the configured path. Do not select for a mechanical/cosmetic change
without that risk, or merely because another selected bridge mentions this one.
Read the skill's actual activation boundaries; choose one primary skill and auxiliaries
only for unresolved questions. No recursive activation or dependency installation.

## Inputs and contributions

Supply requirement/criterion, decision, risk and task IDs, authorized scope, operational question, symptom/window/cohort, topology, telemetry versions and access constraints.
Keep unknowns explicit and preserve the destination project's authorities.

| Artifact | Contribution |
| --- | --- |
| Constitution | Reconcile existing principles, security/data and operational constraints; introduce no product policy or fixed target. |
| Spec | Identify observable outcomes and diagnostic questions; no invented SLOs. |
| Plan / ADR | Connect requirement → decision/risk IDs to question/signal mapping, hypotheses, discriminating observations and telemetry costs/risks. |
| Tasks | Name bounded work, actual inputs/tools, stop conditions and expected evidence: instrumentation/probe changes, propagation, export-failure and alert/runbook checks. |
| Evidence / convergence | Return criterion/task IDs, environment, observation and limitations: sanitized observations, loss/sampling limits, rejected hypotheses and supported conclusions. |

## Conditional handoff

Consult performance-engineering for unresolved quantitative cost attribution or reliability-engineering for recovery policy only when available and needed. Supply IDs, observations, constraints
and existing permission scope. Absence is an explicit gap, not a completed consultation.
The bridge maps contributions; the skill owns its technical procedure.

## Completion and authority

Shared routing, authorization, outcome states and documentation closure follow
[workflow](../workflow.md) and [evidence](../evidence.md). This bridge maps a
selected method to artifacts; it neither activates skills nor changes permissions.
For reuse elsewhere, keep these shared contracts and adapt skill_path to that project.
