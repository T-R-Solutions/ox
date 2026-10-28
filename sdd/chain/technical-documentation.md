---
skill: technical-documentation
skill_path: .codex/skills/technical-documentation/SKILL.md
bridge_version: 1
---
# SDD bridge: technical-documentation

Copy this optional bridge into the destination sdd/chain directory and configure
the project-relative path of the copied SKILL.md. The skill owns the technical
method; this bridge maps its work to existing SDD artifacts.

## Selection

Use when a tutorial, how-to, API reference or technical explanation is the main
feature deliverable. Do not select solely for inline comments, an ADR's architectural
decision or binary document formatting. Record the selected bridge and reason in
the feature plan; catalog presence does not activate it.

## Inputs and contributions

| Artifact | Required input / contribution |
| --- | --- |
| Constitution | Read repository documentation conventions, source authority, preservation and publication permissions; add no publishing policy automatically. |
| Spec | State audience/task, prerequisites, supported version/environment and observable documentation acceptance. Distinguish the documented contract from implementation behavior needing a decision. |
| Plan / ADR | Link requirement/decision/risk IDs to document type, canonical sources/revisions, examples, verification boundary and maintenance location. Do not invent a separate documentation system. |
| Tasks | Name actual documents, affected references and executable or illustrative examples. Verify authorized reader paths, arguments, outputs and effects with the available environment. |
| Evidence / convergence | Return criterion IDs, document locations, consulted versions, checks and actual command outcomes. Distinguish proofreading, compilation, execution, external lookup and reader validation. Missing prerequisites remain visible gaps. |

## Conditional handoff

Consult the affected language/domain skill only for an unresolved contract or
version question and only when available. Supply relevant sources, criterion/task
IDs, the precise uncertainty, needed evidence and existing authority. No recursive
skill chain or mandatory installation is introduced.

## Completion and authority

Use the destination SDD's outcome vocabulary. Each applicable criterion needs
evidence or explicit pending/inconclusive status; a successful link/HEAD request
cannot substitute for a documented download/execution claim. Spec owns behavior,
plan/ADRs own decisions and tasks own work. This bridge does not authorize publication,
deployment, external messaging or production mutation beyond the user's task.
