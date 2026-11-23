# Feature templates

For the full workflow, copy spec.md, plan.md, tasks.md and converge.md into the
chosen feature directory. On the local route in [workflow.md](../workflow.md),
reuse the existing record without creating an artificial feature. When an existing
feature is affected, update its documents and evidence. Keep tasks.md in Brazilian
Portuguese (pt-BR); all other template prose is in English.
Checklists and ADRs are optional. Templates are guides to fill in, not evidence
or already-approved criteria. Preserve existing contracts and remove only irrelevant
sections, with justification when omission affects interpretation.

Traceability may remain in Markdown tables. For automated evidence validation,
add traceability.json and evidence.json according to `sdd/evidence.md`;
using the workflow does not depend on that automation format.

## Copy and adapt as one operation

After copying the selected templates, adapt their authority links before use.
For `sdd/features/<name>/`, replace `../evidence.md` with `../../evidence.md` and
`../workflow.md#documentation-before-task-closure` with
`../../workflow.md#documentation-before-task-closure` in spec/tasks and optional
checklist. These source links remain valid while the files are templates.
For a custom destination, compute each authority path relative to that directory
(for example with `os.path.relpath`), retaining its fragment. Inspect all resulting
local links including any newly supplied content. Do not copy authorities into a
feature to satisfy links. Copying and link validation do not fill placeholders or
create observations; spec/plan/tasks and optional automation still need real inputs.

## Optional current-state projection

Manual consumers use the convergence table directly. For an Ox automated feature,
add the delimited current-status table specified in [evidence](../evidence.md)
and populate it from the actual evidence.json states before `--check-convergence`.
The plain converge template intentionally does not imply automated enrollment.
JSON examples and required schema-2 bindings live in evidence.md; copying a Markdown
template alone does not produce a checker-ready feature.
