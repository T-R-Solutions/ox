# Mandatory Toolbox consumer rules — 2026-11-09

The maintainer requires Ox scripts to follow the exact provided consumer guide
and remove conflicting, deprecated and obsolete configuration. This extends
scripts-toolbox-native (REQ-01/02, D-26/R-26, T026); the latest instruction
supersedes earlier no-acquisition promises only for the documented central OSV
renewal. Existing unrelated working changes were present before this task and
were preserved. No Git staging, commits, central edits or product edits occurred.

## Observed contract and changes

The source is `/home/rodrigo/Projetos/dev_audit/shared-toolbox/docs/consumer-integration.md`.
Its exact observed bytes are preserved in consumer-integration.md.bin; its hash is
in configuration-review.json. The source was compared again after implementation
and had not changed. Before files are preserved in before/, with hashes in
before.json. changes.diff describes this task relative to those actual working
bytes, including previously untracked scripts; Git HEAD is not its baseline.

- Central scanners retain exec arrays with native tokens after `--`, active
  central selection, `/project` ro, `/out` explicit, timeout and diagnostics.
  check_command now contains only local governance/Cargo operations. Duplicate
  scanner argv with host paths was deleted; backend planning selects the
  transport first. Missing local tools no longer leave misleading runnable argv.
- Deleted host-only scanner exports not forwarded to containers. Native YAML,
  TOML and CLI flags remain the effective scanner configuration. Deleted
  unreachable Gitleaks/Opengrep handling after the central transport exits.
- Corrected scripts/README.md and the opt-in test description: central OSV may
  acquire/validate missing data or data acquired over 12h ago before exec/run.
  Failed required acquisition blocks analysis. Scanner `--offline`/network none
  does not prevent central acquisition. The 24h Ox upstream data-age gate is
  retained, separate from acquisition time; Trivy/Grype retain 120h.
- Inspected every native config: 11 files, all referenced by current commands.
  Retained effective rules and the empty trivyignore (no vulnerability exclusions).
  No toolbox.json, toolbox.images.lock.json or integration.json exists under
  scripts; there are no legacy consumers requiring these files.
- Wrapper discovery remains TOOLBOX_BIN/PATH, including stronger existing Ox
  rejection of an empty explicit override. Native argv/exit forwarding, SELinux
  caller selection and failure checks remain. Rejection of obsolete OX_* selectors
  is a diagnostic guard; these variables do not configure any active backend.

## Method and result

Command, from Ox root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s scripts/tests -v
```

Exit 0; 30 tests in 64.283s, 29 passed and 1 explicitly gated real-Docker test
skipped. Raw output: tests.log. Includes Bash syntax for all shell entries,
public plans/aliases, native/finding exit interpretation, missing/configured
executors, spaces/metacharacters/empty argv, malformed diagnostics/reports,
cleanup failures, source/inventory/mode mutation, local Cargo fixtures,
database age rejection and SELinux environment forwarding. Added a public-plan
regression for central exec selection and missing local tool empty argv.
Static configuration inventory and absence of legacy files are recorded in
configuration-review.json. Observed inputs and artifact hashes are in inputs.json.

| Criterion | Method / inputs | Result and state | Limit |
| --- | --- | --- | --- |
| T026 configuration conformity, REQ-01/02 | Exact guide; current scripts; config-reference inspection; public CLI suite | APPROVED within this bounded task: 29 passed, no obsolete local scanner dispatch | Simulated transport does not validate central images or native config parsing |
| Feature AC-01/02 | Current consumer contract suite | INCONCLUSIVE at full feature scope | No full feature acceptance/freshness execution; historical evidence is not renewed |
| Feature AC-03 | Real test is opt-in and was skipped | UNVERIFIED | No Docker scans, central OSV download, native version qualification or resource cleanup observed |

No full verification was run; the exact TOOLBOX_BIN rule for a future authorized
full run remains in AGENTS.md. No native policy was removed merely because it is
stricter than the integration guide. No legacy evidence or reports were deleted.

Recovery: compare the current file hash with inputs.json before using a before/
preimage; preserve unexpected later changes and restore only the affected file.
The OSV behavior belongs to the central manager: returning documentation to a
no-acquisition promise would misrepresent the required contract.
