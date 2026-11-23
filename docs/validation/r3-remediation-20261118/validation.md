# Independent validation — preliminary, 2026-11-18

This is an independent criterion review, not implementation acceptance. Sources
were inspected during ongoing coordinated work. No implementation, requirement,
gate input or evidence envelope was modified by this validator. The coordinator
consolidates this delegated activity in the append-only root task log at closure.

## Observed inputs and method

Read AGENTS.md, docs/development/codex-agents.md, sdd/workflow.md,
sdd/evidence.md, docs/constitution.md, docs/architecture/context.md,
sdd/project.md, the R3 spec/plan/tasks and R3-4 disposition, claude_analysis.md
Part 3, docs/decisions/governance-authority-contracts.md, document_ledger.py,
package-ox.py, ledger tests and current feature traceability/evidence envelopes.
Compared baseline-inputs.json with current governance tests by SHA-256.

Observed identities at this review (not replacements for historical bindings):

| Path | SHA-256 |
| --- | --- |
| sdd/workflow.md | `3c2de7e71414e6e90972c4098a038d4f98bc1aa20b276eab4dc5eb3b8670913b` |
| sdd/project.md | `7fc42e1b97526855dd1a77748a0b1c48f9d4c52ae8b9b30482c9649be3abdd6d` |
| tools/governance/scripts/document_ledger.py | `be36873fcebaaaf4c3ecdeaf9b3c98bf96aa96ba2fa0db4f01d39f20869994e2` |
| docs/decisions/governance-authority-contracts.md | `70e66e254f67a11328857f693703326b635aba1857fdc3db16ca7aa36f71af99` |

Baseline comparison found changed test_document_ledger.py plus seven fixtures:
test_governance.py, test_instruction_copy.py, test_instruction_governance.py,
test_instruction_routes.py, test_maintenance_succession.py,
test_reconciliation.py and test_task_closure.py.

## Criterion verdicts

| Criterion | State | Observation and limit | Resumption condition |
| --- | --- | --- | --- |
| AC-01 | INCONCLUSIVE | governance-baseline.log was still partial, with failures; no completed final full governance execution was available at inspection. Focused success cannot establish this criterion. | Finish baseline accounting and run the complete suite on stabilized final inputs; inspect every failure/skip and record exit. |
| AC-02 | INCONCLUSIVE | package-ox.py includes extraction inventory comparison and isolated commands, including the complete governance suite. Reading this code does not prove extraction. | Provide both named regression outcomes and independently extracted package execution, complete manifest identity and isolation evidence. |
| AC-03 | INCONCLUSIVE | Ledger separates protected sections from project context; tests cover append, current-summary edits, history corruption, downgrade, symlinks and unknown buffers. No final coordinated operational observation has yet been reviewed. | Stabilize ledger/authorities/tests, complete independent review and collect positive and negative observations through real consumers. |
| AC-04 | REJECTED | Selected feature acceptance returned exit 1; native and enabled real-scanner result files also report exit 1. | Resolve failures and execute the complete requested matrix, opt-ins, natives, package and all applicable feature gates on stable inputs. |

R3-4: manual comparison found each of the 31 listed items represented in
r3-4-disposition.md with a reason or resumption condition. This establishes
disposition coverage only, not repair or acceptance of those items. In particular,
deferral of visual changes does not waive mandatory native observations.

## Explicit feature gate observation

Executed from the Ox root, exit **1**:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 sdd/tools/validate.py --root . --features sdd/features --feature configuration-cohesion --feature repository-maintenance --feature product-foundation --feature governance-externalization --feature governance-layout --feature governance-reconciliation --feature scripts-task-closure --feature scripts-security-quality --feature scripts-centralization --require-approved --require-fresh --check-convergence
```

The checker explicitly selected those nine complete features and rejected their
57 normative ACs as UNVERIFIED or INCONCLUSIVE. No global approval of unrelated
features was requested. Selection is a directly affected preliminary set, not a
claim that later source changes cannot add consumers.

Direct dependencies: configuration-cohesion AC-13 uses project.md; AC-05/06/08/
10/11 use changed instruction fixtures. repository-maintenance AC-02 uses
workflow.md. product-foundation AC-01 uses project.md and test_governance.py.
governance-externalization/layout use test_governance.py;
governance-reconciliation uses test_reconciliation.py;
scripts-task-closure/security-quality use test_task_closure.py;
scripts-centralization AC-07 uses test_governance.py. Selecting a feature retains
all its ACs, not just those named here.

No current observation input found in the inspected envelopes binds project.md,
workflow.md or document_ledger.py. Relevant prior observations are historical;
their retired status does not create a fresh approval. Historical bindings also
mention these authorities in product-visual-workbench, scripts-toolbox-native,
scripts-toolchain-config, windows-design-baseline, terminal-progress and
history-scanner-correction. Those mentions alone are not a reason to require
global acceptance: determine semantic impact and current supported scope.

The package commands call the validator without approval/freshness flags.
Successful packaging would therefore not replace the selected acceptance gate.

## Operational evidence inspected

root-checks result JSON files report Cargo build/check/test/fmt/clippy/doc exit 0,
with inputs_unchanged=true. These are supporting observations, not sufficient
acceptance of native behavior or governance. Final review must compare their
captured inputs with the final tree and inspect ignored test disposition.

native-wayland-result.json reports exit 1 and its stderr ends with
`RuntimeError: timeout: task artifact`. native-composition-result.json also
reports exit 1 with the same final timeout and inputs_unchanged=false.
scanners-real-optin-enabled-result.json reports exit 1, inputs_unchanged=false;
stderr reports 11 failures, including read-only central Toolbox execution
metadata writes. The earlier opt-in-disabled result exit 0 cannot satisfy the
enabled test requirement. These failures are not evidence of a specific product
defect without diagnosis, but they contradict the required error-free matrix.

No heavy suite, scanner, native execution or whole-tree copy was started by this
validator. The sources remain mutable and final package/full-run results were
not available. Failed probes of two unverified candidate documentation paths
found no files; no conclusions rely on those nonexistent paths.

## Return to coordinator

Acceptance is withheld. Preserve the observations and criteria, diagnose failed
checks, stabilize inputs, complete the requested execution matrix, and submit
raw logs/results plus exact selected feature gates for independent final review.
Do not refresh historical hashes or replace a mandatory failure with a skip.
This report is the documentation disposition for the delegated preliminary
review; common task documentation and the final append-only activity entry remain
the coordinator's responsibility.
