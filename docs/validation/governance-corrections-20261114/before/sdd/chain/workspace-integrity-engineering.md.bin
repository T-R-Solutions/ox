---
skill: workspace-integrity-engineering
skill_path: .codex/skills/workspace-integrity-engineering/SKILL.md
bridge_version: 1
---

# SDD bridge: workspace-integrity-engineering

## Selection

Use for: Concurrent editing, watchers, write atomicity, Git/worktrees, rollback, paths and symbolic links.

Do not select for: Do not activate to add a SQLite column or review UI formatting; use database-engineering/design-system. Do not reimplement Git merely for convenience.

## Inputs and contributions

Known inputs: workspace tree, exclusion policy, authorized roots, edit plan, Git state, OS events. Do not infer missing capabilities or permissions.

| Artifact | Required input / contribution |
|---|---|
| Constitution | Reconcile existing authorization, data residency, safety and project constraints; add no product policy automatically. |
| Spec | Define scoped, observable behavior and rejected cases. All file changes respect the authorized root and observed version. |
| Plan / ADR | Compare alternatives, contract versions and failure modes; link REQ, AC, D and R IDs; preserve authority boundaries. Write through staging+rename when platform semantics allow; document fallback. |
| Tasks | Name actual files, fixtures, tools, real permissions, failure injections and completion checks. Implement tests in temporary directories and with concurrency. |
| Evidence / convergence | Identify observed implementation/oracle/configuration versions and hashes, test results, unsatisfied criteria and explicit limits. validated file transactions, loss prevention, change trails, snapshot and recovery strategy |

## Conditional handoff

Optional specialist: `application-security`. Specific unresolved question: “Are there alternative paths/symlinks that escape the root granted to the agent?” Consult only if actually present and needed. Supply relevant IDs, known facts, unknowns, permission scope, versions and required evidence. Do not install or load a whole dependency chain. Continue independent work and mark blocked criteria unverified.

## Completion and authority

Shared routing, authorization, outcome states and documentation closure follow
[workflow](../workflow.md) and [evidence](../evidence.md). This bridge maps a
selected method to artifacts; it neither activates skills nor changes permissions.
For reuse elsewhere, keep these shared contracts and adapt skill_path to that project.
