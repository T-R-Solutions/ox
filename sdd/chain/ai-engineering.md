---
skill: ai-engineering
skill_path: .codex/skills/ai-engineering/SKILL.md
bridge_version: 1
---
# SDD bridge: ai-engineering

Copy this file into the destination sdd/chain directory. Set `skill_path` to the
project-relative path of the copied SKILL.md. This optional bridge maps the skill
to project artifacts; it does not install providers, tools or other skills.

## Selection

Use for implementation, evaluation or diagnosis of a foundation-model application,
including retrieval, tool-using agents, adaptation and inference trade-offs.
Do not select for prompt-only drafting, ordinary deterministic software or training
a foundation model from scratch. Read the selected skill for the technical method.
Record selection and its reason in the feature plan; catalog presence is not activation.

## Inputs and contributions

| Artifact | Required input / contribution |
| --- | --- |
| Constitution | Read existing project principles, data permissions and effect authority. Introduce no provider-specific policy or consent to upload data. |
| Spec | Identify the task, supported population, observable completion, unacceptable errors, no-answer behavior and relevant quality/cost/latency constraints. Each criterion needs a concrete scenario and an oracle; do not invent thresholds. |
| Plan / ADR | Identify the application baseline, model/configuration, corpus/index, tools and evaluator versions. Map the diagnosed failure to intervention alternatives and trade-offs; link requirement, decision and risk IDs. |
| Tasks | Name changed surfaces, authorized fixtures/data, actual tools, dependencies and completion checks. Separate deterministic integration checks from actual model trials and component results from final effects. |
| Evidence / convergence | Return criterion IDs, baseline/candidate results on comparable cases, observed variability/cost, denied effects, failures and remaining gaps. Identify model/prompt/data/tool/evaluator versions needed to interpret the evidence. |

Keep evaluation examples and sensitive inputs within the project's authorized
scope. The bridge grants no API spending, data transfer, deployment or tool-effect
permission. Discover actual capabilities and versions before execution; an
unavailable model leaves the corresponding quality criterion unverified.
A mock tool or generated success message cannot establish real task completion.

## Conditional handoff

Optional specialist: `application-security`.
Question: “Can retrieved content or model-selected arguments cause data disclosure
or an effect beyond the caller's authority?” Consult only if unresolved and that
skill is available. Supply affected requirement/task IDs, boundary, facts,
constraints, needed evidence and existing permission scope. Do not recursively
activate skills or claim work by an absent specialist; record a material gap and
continue independent work.

## Completion and authority

Use the destination SDD's outcome vocabulary. Return every applicable criterion
with evidence or an explicit pending/inconclusive status. Separate structural
checks, semantic review, deterministic execution, actual model trials and production
observations. The spec owns behavior, plan/ADRs own decisions and tasks own executable
work. The bridge cannot override those artifacts or expand authorization.
