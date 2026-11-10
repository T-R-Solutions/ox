# Shell automation refactor validation

The maintainer requested shell-only operational scripts, logical folders, removal
of duplication and repeated validation. The active entry is
`bash scripts/automate.sh`; existing Python governance authorities outside scripts/
remain consumers. All operational Python under scripts/ was retired with exact
preimages. Python there now only executes shell tests.

Observed environment: Linux x86_64, GNU Bash 5.3.20, jq 1.8.2, Python 3.13.16,
Rust toolchain 1.99.1. Existing local ShellCheck 0.11.0 and Gitleaks 8.30.1 were
used without installation. The selection/command registry is shared; source
snapshots, subprocess byte capture and report schemas each have one implementation.

| Method / command | Observed result | Artifact / limit |
| --- | --- | --- |
| `python3 tools/governance/scripts/run-tests.py --group fast` | 89 passed, zero failures/errors | fast.log; includes ten new shell acceptance tests and the adapted closure/scanner tests |
| `TMPDIR=/home/rodrigo/.cache/ox-shell-validation PYTHONDONTWRITEBYTECODE=1 python3 tools/governance/scripts/run-tests.py --group integration` | 20 passed, zero failures/errors | integration.log; independent copies, corruption/deletion and preservation; temporary directories cleaned by tests |
| `bash -n` for each of ten .sh files | Passed through test_shell_layout_and_syntax | fast.log; no Python embedded in production shell |
| `PATH=/tmp/shellcheck-v0.11.0:/tmp/automation-integration/gitleaks:$PATH bash scripts/automate.sh --scope full --check shellcheck --check gitleaks` | Both passed, zero findings | scanners.log and both assessment/process JSON files; named selection explicitly records omissions |
| `bash scripts/automate.sh --scope full` | Rust fmt/check/build/test/clippy all passed | full.log and native-results.json; initial governance failures superseded by stable regression runs; unavailable scanners remain blocked |
| Full security and quality baseline | Seven tools missing: osv-scanner, opengrep, cargo-audit, bandit, cargo-machete, ruff, cargo-deny | full.log; corresponding audits UNVERIFIED; databases and license policy must also be reviewed before applicable real runs |

All sixteen adapters executed successfully with controlled tools, including
virtual-workspace Geiger enumeration, coverage and SBOM measurement states,
offline datasets and tool identities. Additional cases reject duplicate and
incomplete JSON, SAST omissions/suppressions, altered inputs, path/symlink escapes,
expired exceptions/data and missing prerequisites; raw binary stdout/stderr and
nonzero exits are retained. Tree hashes match the historical format for hidden,
Unicode and newline-containing file names.

Initial failures are retained: a raw parser count prevented assessment creation;
newline file names affected hashes; ShellCheck needed SCRIPTDIR source resolution;
generated .local snapshots were being checked as repository Markdown. Each has
corrected code and regression coverage. One shell execution observed a concurrently
edited input and one export detected changed source bytes; final checks used stable
script bytes. Both sandboxed and unsandboxed /tmp copies hit disk quota; disk-backed
copies passed without deleting existing files. Rust sockets passed outside the
sandbox after authorization. No product source changes were made for these fixes.

`initial-inputs.json`, `migration.json`, `retired.json`, `revision.json` and before/
identify original bytes, exact authority succession and every retired path.
Only scripts-security-quality active observations bound to changed files were
invalidated; original evidence is retained verbatim. scripts-task-closure already
had historical/inconclusive observations; its active implementation pointer was
migrated. New feature bindings are in evidence.json; they do not renew predecessor
approval. Output snapshots show the inputs actually scanned, not future source
versions. Later SDD acceptance records are documentary updates, not a new audit.

GUI/X11/Wayland: NOT APPLICABLE to the shell refactor; six Rust GUI cases remain
ignored under their separate explicit protocols. Optional history, coverage,
Geiger, Trivy, SBOM, Grype and YARA are not real audit claims here. Unavailable
mandatory scanners prevent claiming complete security/quality validation or 100%
completion; resume with those prerequisites using scripts/README.md.
