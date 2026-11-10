# Scanner configuration outcome — 2026-11-06

Implemented native Cargo resolution plus a shared-toolbox backend for supported
external adapters, explicit Ox configurations, independent native-report checks,
configuration/source/toolkit identities and fail-closed prerequisites. The user’s
existing changes, product source, dependency declarations and historical observations
are preserved. No installation, image build/pull, database refresh, shared-toolbox
edit, commit, publication or graphical product acceptance occurred.

| Criterion | Method / observed result | State / limit |
| --- | --- | --- |
| AC-01 | Backend plans, 16 controlled subprocess tests (included in final 95 fast cases), real toolbox config validation | APPROVED for dispatch contracts; candidate images have not executed |
| AC-02 | Official references in scripts/security/SOURCES.md, explicit TOML/YAML/INI/rules, TOML parser tests, real cargo-audit 0.22.2 parser probe | APPROVED for configuration review; real parsing/execution of unavailable scanners remains unverified |
| AC-03 | Missing/changed locks, omitted/contradictory/malformed reports, timeout, source mutation and report symlink tests; manual suppression and succession denial review | APPROVED for exercised boundaries; installed tools/shared code/Docker daemon are trusted |
| AC-04 | Full closure attempt, final 95 fast cases, 20 integration cases from full attempt, actual native Rust retry, final bounded closure and explicit missing tools/data | INCONCLUSIVE: no complete security/quality audit; real scanner coverage is blocked |

## Actual execution and corrections

`bash scripts/automate.sh --scope full` executed all 115 Python cases. Twenty
integration cases passed. Four fast failures were exposed: three fixtures omitted
the new content-bound project successor and one still expected the former unconfigured
cargo-deny path. The fixture now copies the registered successor/preimages, and the
policy-absence test removes the current versioned file. The runner verifies that
required configuration exists before executing the scanner. The final
`python3 tools/governance/scripts/run-tests.py --group fast` passed all 95 cases,
including those failures and all 16 shell/backend tests. Full initial failures and
raw per-command stdout/stderr remain in full/ and full.log.

The full attempt passed Rust fmt, check, build and clippy. Rust tests were denied
Unix sockets by the managed sandbox (PermissionDenied). The separately authorized
`bash scripts/automate.sh --scope rust --check rust-test` outside that sandbox passed
all 39 cases. Product bytes are unchanged by this task; no X11/Wayland claim follows.

A real native cargo-audit configuration probe exposed required `output.quiet`,
which a generic TOML parser could not detect. After adding it, cargo-audit accepts
the final config and stops because the deliberately absent advisory database has
no crates directory. This is parser evidence, not a vulnerability scan. The initial
and final config/stderr/exit are retained in audit-config-initial/ and
audit-config-final/. Trivy config now uses the officially documented `scan.offline`
key and disables version checks; the existing CLI already enforced --offline-scan.
The pre-correction configs and runner are retained as .bin files. The full attempt
observed those earlier bytes: it is not relabeled as validation of the final native
configurations. Final fast/config/prerequisite checks cover affected successor inputs.

Final bounded closure selects SDD, check-ox, the eight baseline scanners and
ShellCheck. Governance tests are covered by the final 95-case run; unchanged Rust
fmt/check/build/clippy by the full attempt, and Rust tests by the successful native
retry. The 20 successful integration observations are retained; they were not
repeated merely for final configuration fields or fixture repair. Final detached
consumer and documentation/evidence checks reexamine the affected delivery surface.

## Real prerequisites

Only cargo-audit was found among the configured native scanners in this environment;
its reviewed RustSec dataset is absent. cargo-deny/Machete/Geiger/llvm-cov were not
found on PATH or in the global Cargo bin directory. Other native scanners are also
absent. Ruff/Gitleaks/ShellCheck can dispatch to the shared toolbox but no real
consumer image lock is prepared; platform.json still has base_digest=null. Grype
also requires a reviewed real snapshot and is explicitly unselected in toolbox.json
until that exists. No fictitious digest or license grant was created.

OSV/Opengrep/Bandit/Trivy/Syft/YARA-X have research-blocked shared integrations;
their native checks remain available and block when prerequisites are missing.
The optional history/coverage/Geiger/Trivy/SBOM/Grype/YARA/ShellCheck attempts are
preserved in optional/ and measurements/. History stays native because the shared
candidate does not expose the required all-refs contract. Playwright is inapplicable
to this Iced desktop; native graphical acceptance remains separate.

License allow=[] is a deliberate review gate, not an adopted third-party distribution
policy. Broad SAST and lint rules have not received real scanner efficacy validation.
Offline options do not isolate native processes. Controlled tools prove adapter
behavior only; successful schema validation does not build or run an image. External
code/database identities are environment snapshots, not authenticated provenance.

Preimages, before.json, original full source-input manifests, environment.json,
observations.json, raw logs and current evidence inputs identify observed bytes.
Only scripts-shell-refactor had active observations invalidated by changed inputs;
its original evidence remains archived, with affected criteria INCONCLUSIVE. No old
artifact/input hashes were renewed to imply a new scan or product approval.

The first final detached-copy check exposed an evidence-only coupling to absent
application/Cargo files. Application is intentionally excluded from governance
copies. Product observations now use the identified product-inputs.json snapshot
(all original full-attempt application inputs compared unchanged), with an explicit
no-live-product-freshness limit. No distribution boundary or product policy changed.
The failed detached observation is retained; the corrected copy is reexamined.
