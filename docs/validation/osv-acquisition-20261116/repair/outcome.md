# OSV closure correction outcome

The three delivery regressions are corrected: the convergence closure has an exact,
separately authenticated successor; legacy diagnostic-list consumers reject changed
current content without leaking the new exception; the ambiguous Ruff alias was
renamed. An additional focused rejection test exposed and closed an unpinned ADR
content gap. Historical registries, assertions and scanner rules were preserved.

## Observed verification

The frozen-input run `ox-run-aaTDOmV6` finished with aggregate exit 2. SDD structure,
Ox and governance-tests passed. Governance executed 327 tests in 2323.593s,
with no failures/errors and one preexisting opt-in native security integration skip.
Ruff and Bandit failed to write central Toolbox execution records (Errno 30,
read-only filesystem); neither had a confirmed native exit or diagnostic record.
This attempt is preserved as failed, not converted to a successful aggregate.

The root's legacy quality retry was rejected by its parser with exit 2 and
`Unknown check selection: bandit`, before native execution. It remains retained
in `parser-rejected-retry.log`. After explicit host approval, the coordinator
executed only the two affected checks through `scripts/checks/run.sh --check NAME`,
using the same explicit Toolbox/Cargo environment and effective backend adapter.
No source changed and governance was not repeated.

| Native retry | State | Native / adapter exit | Findings | Runtime |
| --- | --- | --- | --- | --- |
| Ruff `ox-security-ruff-Nkgj7xfz` | passed | 0 / 0 | 0 | 0.11.13; cleanup removed |
| Bandit `ox-security-bandit-Qb02Te9i` | passed | 0 / 0 | 0 | 1.9.4; cleanup removed |

Both receipts report `outcome: native`, runtime exit 0 and no OOM. Exact image
identities, raw receipts, source inventories and SHA256 are retained under
`native-retries/` and indexed in `final-results.json`. Each scanner inventory
matches all 12 intersecting frozen inputs; the separate final comparison matches
all 19 frozen source/configuration/document inputs. The other seven include
historical validation artifacts intentionally excluded from scanner inventories.
The selected checks passed in reconciled observations; no combined aggregate exit
zero or full product acceptance is claimed.

Focused verification also passed 31 tests and check-ox; the earlier expanded
failure that identified the ADR gap remains in `preliminary-expanded.log`.
The independent reviewer found no remaining source/contract issue on frozen
inputs. Independent final criterion validation is recorded below after inspection of
the native receipts and final input comparison.

## Documentation and limits

The frozen `report.md`, `plan.md`, feature tasks/convergence, original registries,
source and configuration remain unchanged after verification. This result-only
record and its receipt index complete the already documented closure disposition
without changing authenticated inputs. The prior OSV-05 closure claim remains
superseded for the changed governance/test inputs. The previous OSV acquisition
implementation and its separate evidence are not reapproved by these checks.

No central source change, database download, commit, publication or full scanner
run occurred in this repair. The native integration skip limits this governance
run; actual Ruff and Bandit execution is independently evidenced above. Broad
feature gates remain UNVERIFIED/INCONCLUSIVE. Root and coordinator each observed
zero drift among the 19 frozen inputs after the native retries.

## Independent acceptance

`validate_osv` (independent, read-only context) approved RC-01 through RC-04
for this correction. RC-01 includes its own six helper tests, exit 0. RC-02
combines consumer inspection with the focused and full governance observations.
RC-03 reconciles the preserved failed aggregate with successful native retries.
RC-04 confirms historical preservation and zero drift in all 19 frozen inputs;
the validator also compared all 838 inputs of each scanner against live files
and the recheck inventories, with no mismatch. Copied receipts match their hashes.

The independent source review (`review_osv`) found no remaining issues in the
frozen implementation. Neither reviewer nor validator implemented these changes.
The validator's explicit broad-feature checker returned exit 1 only for the ten
existing UNVERIFIED/INCONCLUSIVE gates; those gates remain unapproved.

Observed identities: frozen manifest
`7468547627ffbcf74c7651291917999878b5c8a8a6bdabaffede3b85038f2971`;
Ruff assessment `909768770e0bbe69a3078269fa78a549e9aad38a6b7c8debfc70937fde20a4bf`;
Bandit assessment `7bb7bfd15f367a4ceb9bf858ebe5a97ef7659a7496efbd6044f716f188bcd3c4`;
final-results `2b9e394ef1b85dabc992cbd4d7bfcdc2e33761a25493231cdb63c2cbbfd92cc9`.
Only this result record was completed after validation; protected inputs were
compared again without mutation. Future input changes require affected reobservation.
