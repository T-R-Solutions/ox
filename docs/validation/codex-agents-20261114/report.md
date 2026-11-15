# Codex agent installation — 2026-11-14

Scope and criteria: [local project record](../../../sdd/codex-agents.md).
The source Ec checkout was read only. Thirteen profiles and the root configuration
were adapted, with Ox verification instructions in both validators and the common
guide. Model/effort defaults follow the requested matrix. No application code,
global config, existing skills, hooks or distribution allowlist were changed.

## Verification

Environment: Linux checkout, Python 3 with tomllib, `codex-cli 0.169.0`.
Input identities are recorded in `inputs.json`: exact installed/configuration
and documentation bytes, plus read-only Ec source identities. Existing AGENTS.md
and sdd/project.md hashes were checked unchanged from the start of this task.
The previously modified docs/README.md received only one additional navigation row.

| Criterion | Method and observation | State and limit |
| --- | --- | --- |
| C1 | Python tomllib parsed root config and all 13 profiles; names and every model/effort pair compared with the requested matrix; installed bytes compared with the prepared manifest | APPROVED for configuration; no efficacy claim |
| C2 | Independent read-only reviewer using explicit Sol 6.1/high parameters inspected all 16 candidate config/guide files and relevant Ox authorities; no material findings | APPROVED for instruction contract; model obedience and full team lifecycle not measured |
| C3 | Both validator profiles inspected against sdd/evidence.md and the actual --features directory semantics; runtime model and concurrency defaults read through the local client's config/read API | APPROVED for local adaptation/configuration; no product or automated feature acceptance |
| C4 | Usage and replication guides, navigation, local SDD scope and documentation disposition reviewed; structural/link checks recorded below | APPROVED for documented installation and its limits |

`codex --strict-config app-server --print-startup-config` returned exit 0.
The sandboxed invocation warned that PATH aliases could not be created on the
read-only filesystem; it still completed config validation. A separate stdio
app-server config/read probe initially failed on read-only local client state.
After the environment's specific approval, that probe succeeded and shut down:
the active project layer was `/home/rodrigo/Projetos/ox/.codex`, with no disabled
reason, root model `gpt-6.1-sol`, effort `medium`, agents enabled, three subagent
threads, and subagent defaults `gpt-6.1-sol` / `high`. Only these selected fields
and layer names were observed; no global configuration was changed or model
inference requested by the probe.

The independent reviewer was created with explicit model/effort and a fresh
context. This demonstrates that bounded review invocation, not native discovery
of every custom profile. All 13 custom-profile invocations, automatic triage,
handoff and slot recycling in a complete new-session team remain UNVERIFIED.
No full automation/scanner run, cost/latency benchmark or product acceptance was
performed. Existing conversations keep their current model/configuration.

Both `python3 sdd/tools/validate.py --root . --structure-only` and
`python3 tools/governance/scripts/check-ox.py` returned exit 0 before installation.
The first post-install check rejected two Markdown links escaping the portable
SDD folder in the new local record. Those references were changed to explicit
repository paths, matching the existing SDD convention; no checker was weakened.
Final reruns on the corrected inputs both returned exit 0. The SDD checker
reported portable files, configured bridges and requested evidence checks;
check-ox reported profile/catalog/bridges/SDD/links and content inspection passing.
Additional focused checks verified every recorded input hash, new local links,
new-file whitespace and `git diff --check -- docs/README.md` (exit 0).
These are configuration/documentation checks, not semantic product acceptance.

Disposition: C1–C4 APPROVED within the bounded installation scope. A new session
is required to use the new root defaults; end-to-end execution of the configured
team remains a separate, unverified operational observation. No earlier evidence
was relabeled or rehashed to claim reexecution.

## Documentation disposition

Reviewed AGENTS.md, sdd/project.md, sdd/workflow.md, sdd/evidence.md,
docs/constitution.md, docs/architecture/context.md, README.md,
docs/development/governance.md, docs/development/local-artifacts.md and the
scripts-task-closure ADR, including its preference successor. These authorities
need no changes: this installation follows their existing contracts and leaves
product acceptance and verification authorization unchanged.

Added docs/development/codex-agents.md and codex-agents-replication.md; updated
docs/README.md navigation. Scope is recorded in sdd/codex-agents.md. The current
governance package excludes the project config/profiles; this checkout-local
limitation is explicit in both guides. No packaging change is claimed.
