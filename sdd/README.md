# SDD: local use and clean adoption

Version 1.3.0 lineage, with the local contracts below. Markdown use needs neither
Python, GitHub Spec Kit, a fixed skill catalog nor special agent commands.

## Use this checkout

Read [project context](project.md), [workflow](workflow.md) and the
[constitution pointer](constitution.md). Existing Ox features and evidence are
project records, not blank templates. Follow [template instantiation](templates/README.md)
when the full route calls for a feature; local changes reuse the existing record.
[Evidence](evidence.md) owns outcomes, bindings and acceptance. Installed
[bridges](chain/README.md) are selected conditionally, never activated by presence.

## Adopt a clean model in another project

From the source checkout, use only this allowlist:

- `sdd/workflow.md` and `sdd/evidence.md`.
- `sdd/templates/README.md`, `spec.md`, `plan.md`, `tasks.md`, `converge.md`;
  optionally `checklist.md` and `adr.md` when needed.
- Optionally `sdd/tools/validate.py` (Python 3.11+ stdlib, no installation).

Create destination `sdd/`, `sdd/templates/`, empty `sdd/chain/` and, for the checker,
`sdd/tools/`. Copy only those files to the same relative locations. If the target
already exists, inspect and merge deliberately; preserve its decisions and evidence.
Create destination-owned `sdd/README.md` with its actual usage/commands and
`sdd/project.md` with phase, scope, paths and limitations. Create
`sdd/constitution.md` pointing to the destination authority (for example
`[Constitution](../docs/constitution.md)`), and create `sdd/chain/README.md` stating
that no bridges are selected yet. Reuse an existing constitution; never copy the
Ox policies as the destination's adopted decisions.

Do not copy `features/`, `project.md`, `codex-agents.md`, the Ox README/context,
acceptance/evidence records, this correction supplement, `.codex/config.toml`,
agent profiles or the full bridge catalog. Ox governance export is a different,
versioned distribution contract. `sdd/model/` describes historical source-library
layout; it is not a command or directory required in this checkout.

Skills are separate: if needed, copy a complete selected skill directory including
its internal resources to an authorized destination. Copy only its corresponding
bridge into `sdd/chain/` and set `skill_path` from the destination project root to
the real `SKILL.md`. Check the declared name and path. Missing selected skills are
a configuration gap diagnosed by the checker; presence does not install a skill
or execute a specialist. No skills or bridges are needed for the base workflow.

Give Codex the destination context and authorized goal in chat, for example:
“Read sdd/README.md and sdd/project.md; follow the workflow for this goal within
this authorized scope.” That sentence is not a terminal command. Updates compare
versions and retain destination changes; skills' technical resources evolve separately.

## Instantiate a feature

Use the complete copy-and-adapt procedure in [templates/README.md](templates/README.md).
At `sdd/features/<name>/`, template links to `../evidence.md` and
`../workflow.md#documentation-before-task-closure` become `../../evidence.md` and
`../../workflow.md#documentation-before-task-closure`. At custom locations compute
relative paths from the actual destination. Preserve fragments and inspect every
local link; copied placeholders are not completed contracts or evidence.

## Optional checker

Run from the destination project root after creating its context and authorities:

```bash
python3 sdd/tools/validate.py --root . --structure-only
python3 sdd/tools/validate.py --root . --link-scope project
python3 sdd/tools/validate.py --root . --features sdd/features --feature configuration-cohesion --require-approved --require-fresh --check-convergence
python3 sdd/tools/validate.py --skill path/to/skill
```

The selected-feature example names an Ox feature; substitute an actual destination
name after creating it. `--features` names a container of direct feature directories;
repeat `--feature NAME` for several complete features. Without selection all direct
features apply. Empty/unknown names, separators, escaping paths, symlinks and a
feature mistakenly used as the container fail. Shared model/bridge/link checks
still apply. Selection does not omit any criterion within the selected feature.

The CLI now defaults to `--link-scope project`: real sibling authorities inside the
root are valid. `--link-scope portable` checks that all model links stay in the
model directory, preserving the former implicit CLI boundary. A sibling `docs/`
constitution therefore requires project scope; a portable package must contain
all referenced authorities. Standalone `--skill` and `markdown_errors(folder)`
retain their folder boundary. Both scopes reject symlinks, missing and escaping
targets; external URLs are not fetched. No flag changes permissions.

A model without features can pass structure, not acceptance. `--structure-only`
is incompatible with approval, freshness and convergence checking. Full automated
feature checking uses traceability/evidence JSON per evidence.md. Convergence
checking is opt-in for portable consumers and explicitly enabled by Ox; it checks
the current projection against evidence, without writing or accepting historical
prose. Manual consumers need none of these JSON/CLI conventions. The checker
cannot establish truthful execution, oracle adequacy or agent effectiveness.

## Ox governance-copy consumer boundary

This is separate from the clean adoption allowlist above. Existing governance
export/copy writers generate `.ox-governance-copy.json` and bind its bytes in their
manifest. The receipt declares a consumer mode, not trusted origin or permission.
Absent/malformed/symlinked receipts never relax local checking; a receipt conflicts
with .git, application or installed agent config/profiles. The existing product
exclusion list remains unchanged and mandatory governance paths still must exist.
Agent profiles in that copy are observed evidence snapshots, not installed agents.
In the full checkout, run `python3 tools/governance/scripts/check-ox.py` before
selected-feature acceptance: it requires exact live config/profile equality with
those snapshots, rejecting missing, changed and symlinked sources. The standard
SDD checker verifies the evidence bindings; it does not replace this Ox consumer
check or prove a live agent loaded configuration.
