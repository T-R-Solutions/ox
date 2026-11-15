# Local Codex agent configuration — 2026-11-14

The maintainer requests implementation of the agreed triage/orchestration matrix,
using the Ec project's `.codex/agents`, `.codex/config.toml` and two development
guides as read-only references. Authorized scope: project-local configuration,
thirteen development-agent profiles, Ox-specific instructions, usage documentation
and focused verification. No product runtime, global configuration, commit,
publication, hooks, skill catalog or distribution-boundary change.

Route: local adaptation of an existing configuration contract. The model matrix,
role boundaries and concurrency ceiling were explicitly selected by the request;
the Ox workflow and evidence policies remain authoritative. This is a project
artifact for this bounded installation, not a new product feature or acceptance
of the application. Previously bound authorities and product observations remain
unchanged; the local scope is recorded here rather than rewriting their history.

Acceptance criteria for the installation:

- C1: the root config and thirteen TOMLs parse and match the agreed model/effort
  matrix, shared profiles and three-subagent ceiling.
- C2: the common procedure defines risk-based triage, handoff, optional specialist
  selection, subtask escalation, independent review/validation and capability limits.
- C3: all profiles route to the Ox procedure; verification uses actual Ox contracts,
  preserving permissions and unrelated changes, with no Ec runtime dependency.
- C4: documentation provides discoverable usage, adaptation and honest validation
  results, including what requires a new session and what was not exercised.

Implementation: `.codex/config.toml`, `.codex/agents/` and the common procedure
at `docs/development/codex-agents.md`. Documentation disposition,
observed input identities, methods, results and limitations are recorded in the
installation report at `docs/validation/codex-agents-20261114/report.md`.

Method consulted: the environment's `openai-docs` skill at
`/home/rodrigo/.codex/skills/.system/openai-docs/SKILL.md`, its self-knowledge
reference, local CLI help and official subagent/configuration documentation.
Contribution: confirm custom-agent fields and concurrency semantics; this does
not install a skill, change the Ox skill profile or prove model execution.

## Approved instruction successor — 2026-11-14

The maintainer approved the configuration-cohesion correction plan, including
the proportional execution policy and root/delegated-triager distinction. The
installation record and C1–C4 observations above remain historical on their inputs;
their reports are not rewritten to claim operation of the corrected instructions.

The root controller performs triage. It may complete authorized read-only work and
clear reversible local repairs only under the workflow conditions and without
material risk. The delegated `ec_triador` stays read-only and childless. Material
risks require `ec_orquestrador_alta` and independent review/validation; absent
capability blocks the dependent stage, with no direct-execution fallback or claim
that self-review is independent. Express user/host restrictions still prevail.
Models, efforts, thirteen profiles and concurrency ceiling remain unchanged.

The [common procedure](../docs/development/codex-agents.md) owns route details;
the [adopted ADR](../docs/decisions/governance-instruction-reconciliation.md) records
the policy decision. The [correction report](../docs/validation/governance-corrections-20261114/instruction-implementation.md)
records source identities, focused checks, documentation disposition and limits.
No live model-effectiveness claim follows from static checks or plan-only execution.
