# Ec script defaults alignment — 2026-11-13

The maintainer requested identical standard configuration after the earlier migration
preserved Ox's old CLI, and explicitly confirmed including analyzer rules. This
successor covers the public interface and applicable defaults of implemented Ox
analyzers. Ec was read-only; existing unrelated work was preserved. No commit,
publication, tool installation or database refresh was performed.

## Observed reference and disposition

`reference.json` identifies the inspected Ec commands, catalog, environment,
native policies and rule files. The earlier complete file inventory remains in
`../scripts-centralization-20261113/ec-inputs.json`.

| Surface | Current behavior |
| --- | --- |
| Public CLI | `./scripts/automate.sh plan|run`; no arguments/unknown operations fail; `--scope complete` rejects filters |
| Default selection | docs/scripts/application/security; Grype, Bandit, Syft and YARA-X are complete-only; explicit checks can select them |
| Filtering | Repeated surfaces/checks, inferred surface, mandatory docs, coverage requires explicit surface; aliases cover Ec names |
| Planning | JSON commands without Cargo/tool execution, preparation or local-state writes; absent native tools still have a canonical command |
| Legacy consumers | Flag-only scopes/`--plan` retain their previous selection/filter behavior; native policy defaults intentionally change |
| Runtime environment | Locale/no-color/offline defaults; explicit overrides first, then PATH and declarative relative Toolbox discovery; shared label in canonical runner only; reuse prepared Ox Cargo cache |
| Results | Canonical aggregation: error 2, blocked 3, findings 1, success 0; legacy return behavior preserved |
| Inputs | Ec generated-file/cache exclusion patterns; Ox source roots, first-party `.codex` skills and historical-validation exclusion remain product-specific |
| Ruff/ShellCheck | Ec lint groups and all optional shell checks; no copied Ec per-file suppressions |
| Clippy/Deny | Ec Clippy all/pedantic/nursery/cargo groups, all features, keep-going; Deny checks all features; Ox duplicate/license/advisory decisions retained |
| Bandit | Typed empty exception checks enabled; existing Ox reviewed baseline and explicit INI retained |
| Syft/Grype | Ec inventory/archive/development-dependency defaults; no suppression of unpatched findings; Ox 120-hour Grype limit retained |
| Trivy | vuln/misconfig/secret, development dependencies and non-failures; count failures across all scanners; redact secret values and source snippets before retention, recording raw hash/size and loss |
| Opengrep/YARA-X | Ec Rust indicators/EICAR added to Ox rules; Ec per-tool timeouts and Opengrep scanning options adopted |

Project-specific license/advisory decisions, exact historical fingerprints, pinned
Rust toolchain and offline/locked Cargo remain Ox contracts. PostgreSQL, HTTP,
frontend and browser services do not apply to this desktop. Ec's additional external
rule catalogs and CodeQL execution engine are separate capabilities not implemented
by this configuration successor. No claim of identical total scanner coverage.

## Verification and limits

Native policy probes used temporary fixtures through the selected public Toolbox
with explicit shared SELinux label. Initial sandbox runs could not write central
execution receipts; authorized retries succeeded. Ruff/ShellCheck/Bandit/Opengrep
reported expected planted findings and zero findings in their negative files.
Syft inventoried the fixture package; Grype reported zero known vulnerabilities in
that fixture. Trivy loaded the broader policy and produced configuration findings;
this native probe did not establish positive vulnerability/secret effectiveness.
YARA-X detected EICAR; its initial file target with `--recursive` was corrected to
a directory. Clippy passed a dependency-free temporary workspace with the configured
groups. `native/summary.json`, native diagnostics and input identities record the
observations. Configuration acceptance does not mean a clean full Ox scan.

Regression logs and the final validation summary are retained in `checks/`.
Public-CLI tests cover selection, filters, missing arguments, side-effect-free
planning, environment discovery/overrides, source exclusions, result precedence,
missing toolchain classification, Trivy counts, suppressed/malformed reports and
redaction. Existing scanner/process/retention suites remain applicable. The real
security full-suite test is opt-in and was not enabled. No full Cargo/GUI/complete
application run was performed; broadened rules may expose existing findings.

## Documentation closure and documentary reexamination

Reviewed and updated `AGENTS.md`, root/application/scripts READMEs,
`docs/development/governance.md`, `sdd/project.md` and scripts-centralization's
spec/plan/tasks/traceability/evidence. Constitution, architecture, local-artifact
retention and Toolbox wrapper were reviewed: product boundaries, two-date retention
and direct-wrapper override/PATH behavior are unchanged. The new runner's environment
and CLI are explicitly documented. Prior examples in historical validation reports
retain their observed syntax.

The exact AGENTS change replaces the recommended full invocation with canonical
`run --scope complete`; the explicit Toolbox, shared-label and Cargo selections
remain. Project state only appends the authorized alignment scope. No skill method,
bridge contribution, original configuration-size measurement or product implementation
is changed by these two documentary edits. `succession.json` binds the five active
guide/authority changes to preserved preimages; unknown mutations and downgrades
remain rejected. Dependent documentary observations are reexamined as inspections,
without renewing historical operational acceptance. Previous evidence is under
`prior/`; changed executable configuration observations are replaced by current
regression/native observations, not by refreshing old hashes.
