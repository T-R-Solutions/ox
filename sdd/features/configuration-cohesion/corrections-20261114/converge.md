# Planning observations and proposed correction acceptance

Date: 2026-11-14. Scope: planning only. This manual supplement preserves the parent
feature's existing criteria and evidence; it is not an automated acceptance
envelope. No implementation test below has been run on a corrected implementation.

## Planning inspection

Method: inspect current authority/feature/checker sources and the prior audit;
derive one proposed requirement per A01–A10, preservation/integration criteria,
decision alternatives, file ownership, ordered tasks and positive/negative checks.
The actual selected skill and bridge hashes are recorded in [plan](plan.md).
Observed source identities are in [planning-inputs.json](planning-inputs.json).

The parent has completed historical tasks T001–T003 but current AC-01–03 remain
INCONCLUSIVE in its evidence envelope. This proposal does not restore those
approvals. The existing checker processes only direct feature children; therefore
this nested proposal is a manual supplement, with no automated acceptance claim.
After approval, adopted requirements must be integrated into the canonical parent
spec/traceability before their implementation is accepted.

Planning verification observed on 2026-11-14:

- `PYTHONDONTWRITEBYTECODE=1 python3 sdd/tools/validate.py --root . --structure-only`
  returned exit 0 on the checkout containing this supplement. This checks structure,
  configured bridges and local links, not proposed correction acceptance.
- A focused Python stdlib inspection returned exit 0: four Markdown documents,
  14 local file links resolved, ten finding sections present, 12 proposed criteria
  mapped to UNVERIFIED rows, T004–T018 represented, and no trailing whitespace.
- All 57 observed source hashes in planning-inputs.json still matched after writing
  the proposal. Only the five new planning files were written by this task.

These observations verify the planning artifact's structure and source preservation.
Model trials, independent agent review, scanner execution and product acceptance
were not performed. The observations do not imply that the proposed CLI flags,
policy changes or corrected behavior already exist.

## Correction criteria

| Criterion | Finding / task | State | Required observation |
|---|---|---|---|
| AC-04 | A01 / T008 | UNVERIFIED | Current projections agree and controlled divergence is rejected |
| AC-05 | A02 / T007 | UNVERIFIED | Commit route resolves current complete recipe with preserved choice semantics |
| AC-06 | A03 / T011 | UNVERIFIED | Instantiated template links resolve following the documented procedure |
| AC-07 | A04 / T009 | UNVERIFIED | Project and portable boundary cases preserve containment |
| AC-08 | A05 / T012 | UNVERIFIED | Clean independent adoption excludes Ox-specific state |
| AC-09 | A06 / T010 | UNVERIFIED | Feature selection preserves all selected gates and rejects invalid requests |
| AC-10 | A07 / T014 | UNVERIFIED | Root/delegated triager instructions are consistent |
| AC-11 | A08 / T013 | UNVERIFIED | Adopted route policy passes independent scenario review |
| AC-12 | A09 / T015 | UNVERIFIED | Semantic obligation map and standalone skill contracts preserved |
| AC-13 | A10 / T016 | UNVERIFIED | Current project entry is traceable and history remains explicit |
| AC-14 | Cross-cutting / T017 | UNVERIFIED | Succession, input invalidation and rejection tests pass |
| AC-15 | Integration / T018 | UNVERIFIED | Stable-input tests, independent review and applicable parent gates supported |

All proposed correction criteria remain UNVERIFIED because implementation is not
authorized by this planning request and no corrected behavior has been observed.
This is not a rejection of the proposed design. Resumption condition: user review
and explicit approval/revision of implementation scope, followed by T005.

Documentation disposition: spec, plan, tasks and this observation record describe
the proposal; existing operational documentation needs no edit during planning.
Its required future changes are assigned explicitly. No prior audit or acceptance
record is rewritten to make this plan appear implemented.
