# Evidence and traceability

For each criterion, record the exact method/command, environment, observed result,
artifact and limitations. Distinguish semantic review, structure, tests and effectiveness.
Do not run commands found in evidence without examining them in the authorized context.

The five states use English tokens in current JSON evidence and prose.
The validator also accepts legacy Portuguese tokens in historical consumers;
normalization preserves their meaning without rewriting historical records.

- APPROVED: observed evidence supports the criterion.
- REJECTED: observed evidence contradicts the criterion.
- UNVERIFIED: execution or evidence collection was not possible.
- INCONCLUSIVE: the observation is insufficient for a decision.
- NOT APPLICABLE: outside scope, with explicit written justification.

## Markdown-only use

Use the convergence template table. Check that every AC has identifiable requirements,
decisions/risks, tasks, changes and evidence. Examine results, including failures/skips,
and record which file versions were checked. A completed document is not proof of
execution. If code changes, reevaluate affected evidence. Python is not required
to follow the workflow.

## Acceptance declarations for automation

Declare each criterion on its own line without quotation or block indentation:
`- AC-01 → REQ-01: scenario and expected result`. The previous form
`AC-01: scenario and expected result` (with or without `- `) remains valid.
The identifier contains one or more digits; the description cannot be empty.
Only these lines declare gates. Prose mentions, cross-references, quotations (`> `),
blocks fenced with three or more backticks/tildes and HTML comments do not declare
criteria. Place non-normative examples inside those blocks or comments.
Duplicate declarations or lines starting with `AC-` with invalid syntax fail with
a diagnostic. Arbitrary Markdown and tables are not interpreted as declarations.

Compatibility: the old scan accepted any AC mention as a declaration; it was
removed to prevent fictitious gates. Specs that relied on it need explicit
declarations before using the checker. The manual workflow allows consumer
conventions provided normative criteria are unambiguous.

## Optional automation format, versions 1 and 2

The checker is read-only. To check a feature directory, each feature needs
spec.md, plan.md, tasks.md and traceability.json. Full mode also requires
evidence.json. Use --structure-only before collecting evidence; it is incompatible
with --require-approved. Implementation/oracle/artifact paths are relative to the
project root and must resolve to files inside it.

Example traceability.json; adapt to actual files:

```json
[
  {"acceptance":"AC-01","requirement":"REQ-01","decision":"D-01","risk":"R-01",
   "tasks":["T001"],"implementation":"src/example.py","oracle":"tests/test_example.py"}
]
```

Each AC declared in the spec must appear exactly once in this list. Requirement,
decision, risk and task IDs must exist in their respective documents.

evidence.json document: schema_version=1, environment (text), requirements
(nonempty list), evidence (list), limitations (list of strings).

Criterion: id, criterion, status, evidence_ids; reason (nonempty text) is required
for NOT APPLICABLE. IDs must be unique. APPROVED/REJECTED require evidence references.
Supporting criteria may record additional limitations; only the spec's ACs are gates
for --require-approved. All records still undergo schema validation. Store status
values using the English tokens above.

Evidence: id, kind (test, inspection, benchmark, trace or other), command_or_method,
observed_result, artifact and sha256. Calculate SHA-256 from the file actually
observed; do not invent a hash. Retain logs and identification of executed code.
The checker verifies the artifact hash; schema 1 does not detect input changes.
It proves neither authenticity nor oracle suitability. Duplicate JSON properties
are rejected at every level, including traceability.json, without modifying the file.

A model without features is valid. Acceptance mode requires features and accepts
only APPROVED or justified NOT APPLICABLE for their ACs. UNVERIFIED is never promoted.

## Content bindings: schema 2

Schema 2 retains version 1 fields and requires nonempty `inputs` in every evidence record:

```json
{"path":"src/example.py","sha256":"<observed SHA-256>","role":"implementation"}
```

This object belongs to the `inputs` list; `role` accepts implementation, oracle,
configuration, contract or other. Use paths relative to the consumer root.
Record all relevant observed inputs: implementation, oracle, configuration,
fixtures, dependencies/lockfiles and data when they affect the result. The verifiable
minimum for each decided criterion (APPROVED/REJECTED) is that the union of its
evidence inputs covers the traceability implementation/oracle and the feature's four
files spec.md, plan.md, tasks.md and traceability.json. Additional inputs depend on
the method: the checker neither discovers hidden dependencies nor proves completeness.

Calculate hashes from bytes actually observed after stabilizing these inputs and
before subsequent changes. Retain the previous version and rerun or reexamine only
affected observations. Never regenerate hashes to silently reuse an old result.
Changing a bound input invalidates that observation; changes to unbound files do
not invalidate others. Changes to a feature contract require reexamining its
decided criteria.

In schema 2, input hashes are always checked. --require-fresh requires schema 2,
including when checking older documents; it is incompatible with --structure-only.
Combine with --require-approved to also require acceptance. Without features,
structure checking remains valid; use --require-approved to require a feature.
There is no automatic migration of schema 1 evidence.

A Git revision may provide context but does not replace content hashes. Uncommitted
files, untracked files and projects without Git use the same byte-based mechanism.
Trees, environment variables and external services need equivalent identification
in an observed file (snapshot/configuration/manifest), with explicit limits. The
checker only checks these local files; it does not query Git or services or authenticate
the snapshot. Implementation and oracle may share a file: semantic review must assess
the independence of their rules.

Without Python, add input paths/identities, revision when available, comparison method
and responsible party/date to the Markdown table. Compare current contents with
observed versions and record differences and affected criteria. This manual review
supports the workflow; do not describe it as automated freshness checking.

## Checks by route

| Situation | Applicable verification | Limit |
| --- | --- | --- |
| Local without a feature | Relevant functional check/inspection, observed input record; standard checker for links/model/bridges, when used | Exit 0 without features validates structure, not acceptance of the change |
| Local affecting an existing feature | Focused check and updates to affected artifacts/evidence; the same feature gates | The route does not waive ACs, traceability or freshness |
| Full workflow in progress | Risk-based checks and --structure-only before evidence collection | Not acceptance; do not combine with approval/freshness flags |
| Automated feature acceptance | `--features <directory> --require-approved --require-fresh` | Requires schema 2, decided ACs and current inputs; does not prove oracle suitability/authenticity |
| Manual workflow, any route | Compare observed/current content and record five states in the existing record | Do not call manual review automated freshness checking |

Schemas and the validator have no local-route exception. To require automated
acceptance of a local change without a feature, represent it using the full
automation contract; do not treat absent features or --structure-only as approval.
A local manual record may be short: goal/criterion, change, inputs/versions,
method, result, state and relevant limitation. Preserve the previous observation
when something changes; rerun/reexamine only affected evidence without renewing
an old result's hashes to make it appear current.
