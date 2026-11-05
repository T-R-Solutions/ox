# Portable SDD

Version 1.3.0 (lowercase paths). A standalone specification-driven development
structure usable by Codex starting from this document. It does not depend on
GitHub Spec Kit, Python, a fixed skill catalog or special agent commands.

## Manual adoption

1. Copy this directory's contents to `sdd/` at the destination project root.
   If `sdd/` already exists, compare and merge files deliberately; do not
   overwrite decisions, evidence or instructions.
2. Fill in [project.md](project.md) with actual context, paths and commands.
   Reuse the existing constitution and documents when they are authoritative;
   do not create a competing policy.
3. Copy only complete directories of necessary skills to an authorized project
   location. A skill directory includes SKILL.md and its internal resources.
   For explicit use, give Codex the entry path; this structure neither installs
   skills nor assumes automatic agent discovery.
4. Copy corresponding bridges from the library's `sdd/chain/` catalog to the
   destination's `sdd/chain/`. In each bridge, set `skill_path` to the actual
   path from the project root to SKILL.md. Do not copy the entire catalog by default.
5. In Codex, request: “Read sdd/README.md and sdd/project.md. Use this workflow
   for [goal], in feature [path], within [authorized scope].” This is a chat
   instruction, not a terminal command or an installed skill.

The workflow remains usable without skills or bridges. A missing bridge means
only that integration with that specialty has not been configured.

## Change route

Use [workflow.md](workflow.md) to choose a bounded local change or the full workflow.
The local route uses inspection, implementation, a focused check and proportionate
records; material risks involving contracts, authorization, data, concurrency,
consumers or recovery expand the workflow. Update affected existing artifacts on
both routes. Neither route converts missing evidence into approval or waives project gates.

## Model entry points

- [Workflow](workflow.md): feature execution and resumption.
- [Initial constitution](constitution.md): principles to reconcile with the project.
- [Evidence contract](evidence.md): outcomes and traceability.
- [Installed bridges](chain/README.md): conditional selection without automatic activation.
- [Templates](templates/README.md): copy only relevant artifacts.

To add a skill later, copy its directory and bridge, adjust `skill_path` and
review selection in the affected feature's plan. Do not change the workflow core.
For updates, compare skill and bridge versions and preserve local adjustments;
technical references included in different skills may evolve independently.

## Optional verification

The workflow and evidence review work with Markdown. If Python 3.11+ is installed,
the included stdlib checker can check links, bridges and the optional JSON evidence
format without installing packages, running commands from reports or writing files:

```bash
python3 sdd/tools/validate.py --root .
python3 sdd/tools/validate.py --root . --features sdd/features --require-approved
python3 sdd/tools/validate.py --require-approved --require-fresh
python3 sdd/tools/validate.py --skill path/to/skill
```

The first command accepts a model without features. The second requires at least
one feature with reconciled criteria. If the project uses another directory, pass
`--features relative/path`. A feature in progress may use `--structure-only`;
for full automated review, provide the JSON files described in evidence.md.
Without Python, manually perform the same checks described there. This checker
does not demonstrate agent effectiveness, truthful test execution, tool compatibility
or merge protection.

In the source library, the model is in `sdd/model/`, separate from the bridge catalog.
To check it without copying, use `python3 sdd/model/tools/validate.py --root . --model sdd/model`.
At the destination, with model contents in `sdd/`, the commands above use defaults
without extra flags.
