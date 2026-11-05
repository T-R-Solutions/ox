---
skill: autonomous-verification-engineering
skill_path: .codex/skills/autonomous-verification-engineering/SKILL.md
bridge_version: 1
---

# SDD bridge: autonomous-verification-engineering

Copy this file to the destination project's `sdd/chain/` and set `skill_path` to the actual project-relative path of the skill entry. This is an optional bridge and does not install or activate the skill.

## Selection

Use for: Systems that accept/reject agent deliverables; evidence, criteria, gates, autonomous execution and false acceptance risk.

Do not select for: Do not use solely to create unit tests or investigate flaky tests; software-testing owns those methods. Do not produce an uncalibrated “confidence score.”

Select only when the concrete feature has this specialized question. Read the actual skill; record its path/version and selection reason in the plan. A bridge reference does not recursively select other skills.

## Inputs and contributions

Known inputs: normative criteria, code snapshots, authorized tests/checkers, change risk, approval policy. Do not infer missing capabilities or permissions.

| Artifact | Required input / contribution |
|---|---|
| Constitution | Reconcile existing authorization, data residency, safety and project constraints; add no product policy automatically. |
| Spec | Define scoped, observable behavior and rejected cases. Every verdict is bound to an explicit criterion, method and input snapshot. |
| Plan / ADR | Compare alternatives, contract versions and failure modes; link REQ, AC, D and R IDs; preserve authority boundaries. Separate states: pending, approved, rejected, inconclusive, justified not applicable. |
| Tasks | Name actual files, fixtures, tools, real permissions, failure injections and completion checks. Create fixtures with false tests, failures, skips and post-validation changes. |
| Evidence / convergence | Identify observed implementation/oracle/configuration versions and hashes, test results, unsatisfied criteria and explicit limits. gate model, auditable states, requirement-evidence-snapshot bindings, implementation/oracle separation, replay procedures |

## Conditional handoff

Optional specialist: `software-testing`. Specific unresolved question: “Does the chosen oracle actually fail when a representative defect is introduced?” Consult only if actually present and needed. Supply relevant IDs, known facts, unknowns, permission scope, versions and required evidence. Do not install or load a whole dependency chain. Continue independent work and mark blocked criteria unverified.

## Completion and authority

Use the destination SDD's states: APPROVED, REJECTED, UNVERIFIED, INCONCLUSIVE, NOT APPLICABLE (with justification). A mock or document is not execution evidence. Record freshness of inputs and source of each observation. Spec owns behavior; plan/ADRs own decisions; tasks own work; this bridge only connects the skill to those artifacts.
