---
skill: plugin-protocol-engineering
skill_path: .codex/skills/plugin-protocol-engineering/SKILL.md
bridge_version: 1
---

# SDD bridge: plugin-protocol-engineering

Copy this file to the destination project's `sdd/chain/` and set `skill_path` to the actual project-relative path of the skill entry. This is an optional bridge and does not install or activate the skill.

## Selection

Use for: New protocol/plugin host, capability manifest, IPC, vN/vN+1 compatibility, safe installation/uninstallation.

Do not select for: Do not select for a lint plugin that only uses an established SDK; use Rust and API Testing in that case. Do not turn this skill into an automatic recommendation for Wasm, gRPC or Dylib.

Select only when the concrete feature has this specialized question. Read the actual skill; record its path/version and selection reason in the plan. A bridge reference does not recursively select other skills.

## Inputs and contributions

Known inputs: extensibility policies, threat model, operations/capabilities, version matrix, OS, available resources. Do not infer missing capabilities or permissions.

| Artifact | Required input / contribution |
|---|---|
| Constitution | Reconcile existing authorization, data residency, safety and project constraints; add no product policy automatically. |
| Spec | Define scoped, observable behavior and rejected cases. Negotiate version and capabilities without performing operations that are not yet authorized. |
| Plan / ADR | Compare alternatives, contract versions and failure modes; link REQ, AC, D and R IDs; preserve authority boundaries. External process + versioned contract versus a dynamic library loaded in the host; decide by failure model and ABI. |
| Tasks | Name actual files, fixtures, tools, real permissions, failure injections and completion checks. Implement a test harness for contracts, failures, limits and compatibility. |
| Evidence / convergence | Identify observed implementation/oracle/configuration versions and hashes, test results, unsatisfied criteria and explicit limits. message contract, host states, permission model, resource limits, compatibility matrix, failure and migration tests |

## Conditional handoff

Optional specialist: `application-security`. Specific unresolved question: “Does the chosen isolation actually prevent unauthorized effects from a compromised plugin?” Consult only if actually present and needed. Supply relevant IDs, known facts, unknowns, permission scope, versions and required evidence. Do not install or load a whole dependency chain. Continue independent work and mark blocked criteria unverified.

## Completion and authority

Use the destination SDD's states: APPROVED, REJECTED, UNVERIFIED, INCONCLUSIVE, NOT APPLICABLE (with justification). A mock or document is not execution evidence. Record freshness of inputs and source of each observation. Spec owns behavior; plan/ADRs own decisions; tasks own work; this bridge only connects the skill to those artifacts.
