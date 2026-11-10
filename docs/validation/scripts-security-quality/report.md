# Security and quality reintegration — observed results

The correction retains stack-relevant security/quality checks even when tools or
configuration are absent. Missing prerequisites now block a named check instead
of serving as grounds to delete it. Scope is governance/developer tooling only.

AC-01 APPROVED: all 92 original files were re-read and compared with their recovery
SHA256 values. inventory.json records every successor disposition. The maintained
scripts tree has 38 files: native adapters, compatible wrappers, local rules,
strict report/exception validation and truthful summaries. Fifteen named external
tools support sixteen checks (Gitleaks current/history share a tool). Baseline
security: Gitleaks, OSV, Opengrep, RustSec and Bandit. Quality: Machete, Ruff and
cargo-deny; complementary history/coverage/Geiger/Trivy/Syft/Grype/YARA/ShellCheck.
MIT attribution is retained for reused report/exception code and local indicators.
Foreign-stack/configuration rules and the unofficial Rust Qodana image remain
excluded for actual incompatibility/effects, not merely missing configuration.

AC-02 APPROVED: 16 controlled-executable/behavioral tests passed. They cover
real wrappers from another cwd with spaces, findings exit 10, missing tools/data,
expired/mutated/escaping datasets, partial/suppressed/empty SAST, zero-exit omitted
sources, missing JSON reports, raw binary stdout and exit 23, duplicate JSON,
expired exceptions, source snapshot integrity, measurement semantics, missing
license policy, Geiger's 16 concrete manifests, predecessor downgrade rejection,
and absence of inherited Grype severity thresholds. These validate adapters and
failure behavior, not scanner efficacy on real product inputs.

AC-03 APPROVED within tooling scope: 79 fast tests passed. The broader integration
execution completed 19 cases successfully, then the daemon restart interrupted
the final case before a suite summary. The remaining test was rerun alone:
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tools/governance/tests python3 -m unittest
test_ui_metadata_inventory.MetadataInventoryTests.test_unrelated_preservation_still_enforced -v
It passed. No aggregate exit 0 is invented for the interrupted process. Broad
checks are retained as supplemental observations of copy/recovery contracts;
scanner parser refinements and the added downgrade guard were reexamined through
focused tests and an independent copy of final scripts, with 42 exact source/copy
hash matches. That copy ran the original validator, check-ox, and the actual
Gitleaks wrapper plan under isolated-run without source-tree fallback; all exited
0. See detached-checks.json, its per-command raw logs and resumed-integration.txt.

Operational documentation now includes security/quality/full selection and named
complementary checks. The maintained scripts subtree explicitly joins the copy
boundary because modules/rules/wrappers are real consumers. Runtime data and
erase.md remain excluded. Catalog, versioned profile and reusable skill bodies
are unchanged; method interchange stays in the local development guide. No
solution is installed, globally or locally; no image is pulled or hook installed.

AC-04 UNVERIFIED: real CLI attempts for all 16 names returned blocked/3 because
required binaries are missing. scanner-attempts.json and each assessment preserve
the exact reason, actual adapter hash and tool_exit_code=null. This is evidence
of a missing prerequisite, not a successful scan or proof that code is secure.
Datasets and cargo-deny policy also require preparation/review. Temporary erase.md
records candidate versions, official sources, setup/verification, licensing,
network/privilege and container constraints; it is neither configuration nor
permanent documentation. SOURCES.md and scripts/README.md retain durable guidance.

No Rust source/manifest/dependency changed: the 76 identified native inputs match
the preceding supplementary observation. No native test was repeated solely for
these tooling changes, and no product/GUI approval is transferred. Graphical
acceptance is NOT APPLICABLE here; X11/native Wayland remain separate methods.

Recovery: /tmp/ox-scripts-integration/recovery contains all original imported
bytes. /tmp/ox-security-reintegration/before captures the state before this
correction. docs/validation/scripts-security-quality/before and preimages.json
identify relevant authority/evidence predecessors. Only the three criteria of
scripts-task-closure were invalidated by actual changed inputs in this correction;
older unrelated/operational observations remain untouched. No historical hash was
renewed to reuse an old conclusion. Restore selectively after comparing new work.

Limits: commands use upstream offline controls, not an OS network sandbox. Data
fingerprints and valid_until identify reviewed bytes/dates; they do not authenticate
origin, completeness or licensing. Source snapshots explicitly exclude generated
and historical paths as documented. Unknown/partial reports, source/data/tool
mutations and unavailable prerequisites prevent the corresponding completion
claim. Measurements (coverage/unsafe inventory/SBOM), scanners and builds do not
automatically approve the product. Actual scanner compatibility, rule parsing and
coverage/helper execution remain pending until AC-04 can be observed.
