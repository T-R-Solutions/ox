# History false positives and terminal clarification — 2026-11-15

Authorized by the maintainer's correction request after diagnosing a finding on
line 76 of welcome-projects-20261114/native-input-enter-fixed-pointer/result.json.
Full route, high-profile coordination and independent review/validation apply.
Scope and criteria: sdd/features/history-scanner-correction. Existing edits were
preserved. No complete pipeline, downloads, central changes or repository commits.

## Change and decision

The original report contains 147 `generic-api-key` occurrences. The implementer's
occurrence-review.json records the exact Git blob, line, source path, source
commit and independently computed content digest for every added fingerprint.
135 match source bytes in the artifact's commit; 12 match source bytes identified
in a separate, later committed snapshot. This proves the digest classification,
not freshness of the earlier validation artifact. These are file-content SHA-256
values, not credentials.
The authenticated ignore list grows from 1,606 to 1,753 exact fingerprints.
No path/rule exclusion or detection threshold changes. Future commits have
different fingerprints and do not inherit these exceptions.

Both fixed terminal sentences now read: “A aceitação funcional do produto é
avaliada separadamente.” This states the verification boundary without implying
failure. States, codes, diagnostic provenance and report formats are unchanged.

## Verification and independent disposition

Observed focused commands, executed from the Ox root on the current production
inputs identified by implementation-inputs.json:

| Command | Exit / result | Artifact |
| --- | --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s scripts/tests -p test_terminal_progress.py -v` | 0; 21 passed, 23.246 s | coordinator/terminal-tests.txt |
| `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=scripts/tests python3 -m unittest -v test_process_lifecycle test_capture_status test_backends test_geiger_selection test_defaults test_automation test_native_reports` | 0; 49 passed, 122.011 s | coordinator/regressions.txt |
| `PYTHONDONTWRITEBYTECODE=1 python3 sdd/tools/validate.py --root . --structure-only` | 0 | coordinator/structure.txt |

Independent source review (review.md) found no defects, reproduced all147 digest
provenances and confirmed exact diffs. The independent validator reproduced the
147 cases and approved AC-03 and terminal-progress AC-01–06. It caught missing
explicit log/oracle bindings in the first terminal envelope; those were corrected
and the validator independently observed the selected approved/fresh/convergence
gate exit0. Receipts: validation-partial.md and validation-terminal-final.md.

## Native execution limitation and resumption

The focused command used explicit TOOLBOX_BIN at the maintainer's installed
dev_audit/shared-toolbox/bin/toolbox, TOOLBOX_SELINUX_LABEL=shared and
`bash scripts/checks/run.sh --check history`. It returned adapter exit2, native
tool exit null, finding_count null: infrastructure error before native execution.
Toolbox could not write its operational receipt in
`/home/rodrigo/Projetos/dev_audit/shared-toolbox/tools/gitleaks/volume/central/executions`
under the workspace sandbox. Preserved observations are
coordinator/history-assessment.json and coordinator/history-stderr.log.

A separately generated synthetic secret was confined to a disposable /tmp Git
repository; no secret was added to the Ox checkout. That first probe hit the same
host restriction before Gitleaks produced a report. Its stderr is retained under
probes/history-new-doc-secret/; coordinator/probe-script.py.bin preserves the
planned controls, which are **not** claimed executed. A request to rerun with
escalated permissions waited446.9 seconds and returned `aborted by user`. No
escalated rerun, bypass, native success or new finding count is claimed. The
implementer reported its session ended and no executor remained active.

History AC-01 and AC-02 remain UNVERIFIED because their required native evidence
is unavailable. Static review proves the bounded correction, not its operational
acceptance. Resume only with renewed host permission/capability for Toolbox's
required operational write; verify input drift, run the focused history scan and
isolated secret/exact-fingerprint/altered-fingerprint controls, then submit the
results to independent validation. The existing authentication-rejection fixture
passed among the49 regressions. No full pipeline is required by this correction.

## Documentation disposition

Reviewed scripts/README.md and updated the exact exception count, history meaning
and terminal message explanation. README.md delegates commands to scripts/README
and needs no change. sdd/project.md and architecture/context.md describe product
authorization/architecture and remain unchanged: this request is recorded in the
correction feature and changes no product behavior. Terminal-progress evidence is
reevaluated for the changed presentation/configuration inputs; the previous
envelope/convergence remain in coordinator/. Scripts-toolbox-native already has
UNVERIFIED broader criteria; this focused correction does not renew them.
Historical evidence JSON, native screenshots and original reports are preserved.
