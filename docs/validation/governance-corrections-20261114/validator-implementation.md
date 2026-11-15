# Validator implementation observations — 2026-11-14

Scope: A01/A04/A06 (T008–T010), under the approved correction plan and the
coordinator's exclusive path assignment. This report records implementation and
focused tests, not independent review/validation or acceptance of product behavior.
No subdelegation, scanners, downloads, commits, publication or product edits occurred.

## Preconditions and paths

Read AGENTS.md, docs/development/codex-agents.md, project/constitution/architecture,
workflow/evidence, relevant layout/reconciliation ADRs and the complete correction
spec/plan/tasks. Existing dirty/untracked work was preserved. The existing files
matched the coordinator's immutable preimages before writing:

| Path | Initial SHA-256 |
| --- | --- |
| `sdd/tools/validate.py` | `6df3b403dc50d4d6aebcbd803a65af175ec4baf6f9c18afb21e183b0db2f3aa5` |
| `tools/governance/scripts/check-ox.py` | `82f52262550e9483f6402a32c0a1131f24f86694c3471e5c652573c7454b7c92` |

`tools/governance/tests/test_instruction_validator.py` did not exist. This new test
module, the validator, the single check-ox call change and this assigned report are
the only paths written by this implementer. No ownership conflicts were observed.
check-ox was enabled only after the coordinator confirmed migration of 39 projections.
A direct byte comparison confirmed that its entire delta from the assigned preimage
is `V.audit(root)` → `V.audit(root, check_convergence=True)`.

Consulted software-design and software-testing entries and their version-1 bridges,
as selected by the approved plan: preserve public positional interfaces, isolate the
new decisions, derive positive/negative partitions and prove original-defect
sensitivity. Also read software-testing/references/case-design.md. These are method
consultations, not a claim of separate specialist execution or independent review.

## Contracts implemented

`--check-convergence` is opt-in. For each selected automated feature, it requires
exactly one pair of own-line markers, exact headers, one row per normative spec AC
and current normalized JSON agreement. The grammar is:

```markdown
<!-- sdd:current-status -->
| Criterion | Status |
| --- | --- |
| AC-01 | UNVERIFIED |
<!-- /sdd:current-status -->
```

Rows use exact English state tokens without backticks; legacy evidence statuses
are normalized without rewriting JSON. Row order is unrestricted. Historical prose
outside the block is not interpreted. Missing/duplicate blocks or rows, unknown ACs,
malformed headers/rows, invalid tokens and mismatches fail. Supporting non-normative
JSON criteria retain the existing evidence schema behavior. Checking never repairs
Markdown or JSON. Structure-only plus convergence/freshness/approval is rejected.

`--link-scope project|portable` defaults to project for CLI/project audit. Project
mode accepts real sibling authorities inside the root; portable mode contains model
links within the model. `markdown_errors(folder, boundary=None)` retains its former
folder default. Links are percent-decoded before inspection; file and intermediate
symlinks are rejected before resolution, including `alias/../target`. `local_file`
uses the same protection for evidence/traceability inputs. Standalone skills retain
their own folder boundary and reject explicit project/feature mode flags. External
URLs are not fetched; fragment handling is unchanged. This remains offline path
inspection, not an OS isolation or race-free file-opening primitive.

Repeatable `--feature NAME` selects direct children under the unchanged `--features`
container. Names are sorted/deduplicated and reported before validation. Omission
retains all-feature behavior. Unknown/empty/escaping names, symlinks and invalid
containers fail; passing a feature as its own container yields corrective guidance.
Schema, traceability, bindings, approval and convergence checks cover the complete
selected features. Shared model/bridge/link checks still apply. No criterion filter
or acceptance bypass was added. Explicit empty containers and irrelevant skill/model
combinations are also rejected.

Existing positional API arguments keep their meanings. Optional parameters append:

```python
audit(..., link_scope="project", feature_names=None, check_convergence=False)
feature_errors(..., feature_names=None, check_convergence=False)
markdown_errors(folder, boundary=None)
```

## Executed checks

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools/governance/tests -p test_instruction_validator.py -v
```

Final result: exit 0; 23 tests, 1.126 seconds, no failures/errors/skips. Cases cover
all five states and legacy normalization; malformed/missing/duplicate projections;
historical approved prose beside current UNVERIFIED; unchanged file bytes;
old-checker regression; manual/structure use; sibling/portable boundaries; encoded,
missing, escaping and symlinked paths; standalone skills; selected approved/fresh
features beside unfinished/malformed siblings; stale/schema-1/artifact/binding/JSON
failures; missing traceability; custom/multiple/duplicate names; invalid/empty names
and containers; shared links/bridges; positional compatibility and mode exclusions.

The regression executes the authenticated-before preimage validator in a disposable
fixture with current JSON UNVERIFIED and projection APPROVED: old audit returns
no errors; current opt-in check reports a status mismatch and CLI exit 1. Neither
checker writes the fixture. This demonstrates detection of that specific defect.

Also executed eight existing tests using `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest`
with these fully qualified suffixes under
`tools.governance.tests.test_governance.GovernanceTests`, followed by `-v`:

- `test_declared_criteria_ignore_examples`
- `test_duplicate_criterion_rejected`
- `test_duplicate_json_rejected`
- `test_path_escape_and_symlink`
- `test_bridge_identity_and_unconfigured`
- `test_missing_artifact_not_approved`
- `test_english_and_legacy_states_enforce_the_same_evidence_gates`
- `test_freshness_selective_invalidation`

Result: exit 0; eight tests, 0.003 seconds, no failures/errors/skips.

Intermediate live-checkout integration observations, before the final empty-container
and skill/model exclusion refinement:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 sdd/tools/validate.py --root . --check-convergence
PYTHONDONTWRITEBYTECODE=1 python3 sdd/tools/validate.py --root . --structure-only
```

Both exited 1 while other assigned writers were active. Structure identified missing
`instruction-implementation.md`, `deduplication.json` and
`test_instruction_succession.py`. Evidence mode additionally identified stale inputs:
product-local-persistence `E-T011-R3-LOCAL-SOURCE-REVIEW` → converge.md;
scripts-centralization `E-EC-PARITY-REVIEW` → sdd/evidence.md and sdd/tools/validate.py.
No projection mismatch was reported. These observations were sent to the coordinator;
they are integration dependencies, not converted into approvals or repaired by
changing another agent's evidence. A stable-input integration run remains necessary.

## Handoff identities and documentation disposition

Final handed-off implementation bytes, observed with `sha256sum`:

| Path | SHA-256 |
| --- | --- |
| `sdd/tools/validate.py` | `3b1e99d6152dbf7e6ac27dba534798baa66b57a63ba6f943c40de151f243922c` |
| `tools/governance/tests/test_instruction_validator.py` | `1fc1335d366c1e262e816640e398f3d8297ca098b5ba1e8bb47b1ae8366af4e7` |
| `tools/governance/scripts/check-ox.py` | `801a56833923a1588b1d0ba2b1e65e81e88602fa43cf26b6c7316fe52578e097` |

Reviewed the coordinator's current sdd/evidence.md and sdd/README.md; their block,
selection and boundary descriptions match these implemented contracts. CLI help
documents the new options in the assigned validator. Common instructions,
projection migration, evidence disposition, README and succession remain assigned
to the coordinator. This implementer changed no criterion, receipt or another
agent's evidence. Remaining work: stabilize integration inputs; run affected
consumers; obtain independent review/validation; evaluate every applicable parent
criterion without requesting unrelated global approval.
