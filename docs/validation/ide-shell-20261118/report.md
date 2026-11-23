# IDE shell — implementation report (2026-11-18)

Feature: [product-ide-shell](../../../sdd/features/product-ide-shell/spec.md).
Contract: [ide-shell.md](../../design/ide-shell.md). All observations below were
made by the implementing agent; no independent review or validation was run.

## Baseline (before edits)

| Check | Result | Log |
| --- | --- | --- |
| check-ox | exit 0 | [baseline-check-ox.log](baseline-check-ox.log) |
| SDD validate | exit 0 | [baseline-sdd-validate.log](baseline-sdd-validate.log) |
| Governance suite (`unittest discover -s tools/governance/tests`) | exit 1: 251 tests, 5 failures, 129 errors (already red; ran concurrently with cargo) | [baseline-governance-suite.log](baseline-governance-suite.log) |
| `cargo test -p ox-ui` | exit 0 (56 + 4 + 1) | [baseline-cargo-test.log](baseline-cargo-test.log) |

Input hashes before editing: [baseline-inputs.sha256](baseline-inputs.sha256);
tree state: [baseline-git-status.txt](baseline-git-status.txt).

## Changes

- Dark theme roles (tokens.json → tokens.rs): graphite work area, navy chrome,
  saturated primary with white text. Light/HC unchanged.
- New `desktop/chrome.rs` (48-unit bar, menus, status bar, window title) and
  `desktop/dock.rs` (document tabs, bottom tool dock).
- `desktop.rs`: state/messages for menu, tabs, dock and recents filter; sidebar
  limited to 19 document destinations; Ctrl+J; modal menu traversal.
- `views.rs`: info bar, flat sections, breadcrumb, scoped badge, reading width,
  S01 tiles/filter/empty state, editor tool strip removed (moved to the dock).
- `design.rs`: Menu/Tab roles, selected navigation without perimeter, thin
  scrollbar, info bar and note styles; `splitter.rs` neutral at rest;
  `icons.rs` Info/Plugin/Chevron/Dock/Status added, five unused kinds removed.

Defects found during verification and fixed: the initial document was dropped
from the tab list when navigating away; closing the active tab re-registered
it; tab markers stretched each tab to a full row (seen in the first capture);
the fixed 240-unit dock left little document space on short windows (seen at
1024×700; replaced by a 30 % portion).

## Final focused checks

| Check | Result | Log |
| --- | --- | --- |
| `build_design.py --check` | exit 0 | [build-design-check.log](build-design-check.log) |
| `check_contrast.py` | 114 pairs, 0 failures | [contrast.json](contrast.json) |
| `cargo fmt --check` | exit 0 | [cargo-fmt.log](cargo-fmt.log) |
| `cargo clippy --workspace --all-targets -- -D warnings` | exit 0 | [clippy-default.log](clippy-default.log) |
| `cargo test --workspace` | exit 0; 102 passed, 0 failed | [cargo-test.log](cargo-test.log) |
| clippy with automation flags (pedantic/nursery/cargo) | exit 101; findings only in unchanged code + 2 duplicate dependency versions | [clippy-pedantic.log](clippy-pedantic.log) |

Tests updated for the deliberate contract change (4): sidebar completeness,
sidebar group contiguity, focus targets that left the sidebar, and the menu
trigger replacing the removed density control. Tests added (7): reachability of
every destination, modal menus, document tabs, tool dock and Ctrl+J, title and
badge scope, recents filter ids, measured reading width.

## Native captures

Isolated headless Mutter + PipeWire, scale 1, keyboard-only journey driven by
[capture.py](capture.py) (reusing the existing session harness). Each run holds 13
captures: S01 Light/Dark, S12 Light/Dark, S05 Light/Dark/HC/HC Compact/Light
Compact, S05 with dock, W00 Light/Dark and the open Exibir menu.

- First run [native-1600x1000](native-1600x1000/) (tabs wrapped one per row: defect).
- Second run after the tab fix: [1024×700](native-r2-1024x700/),
  [1600×1000](native-r2-1600x1000/), [2560×1080](native-r2-2560x1080/)
  (dock too tall at 1024×700: defect).
- Final run: [1024×700](native-r3-1024x700/), [1600×1000](native-r3-1600x1000/),
  [2560×1080](native-r3-2560x1080/).

Inspected: bar fits at all three widths (go-to collapses to an icon below 1180);
menus anchor under their triggers; tabs in one row with top marker; dock 30 %;
info bar single; S01 tiles and "Em breve" visible; Dark graphite with navy chrome.
At 1024×700 the window was not maximized by the compositor (about 916×626).

## Limitations

- Visual judgment above is the agent's; maintainer acceptance (AC-07) pending.
- HC disabled buttons look close to enabled ones (existing `text_muted`).
- No assistive-technology bridge (Iced 0.14 without AccessKit).
- Pinned documents not updated; superseded statements are listed in ide-shell.md.
- `application/tools/native_review*.py` and `#[ignore]` X11 tests in ox-app keep
  their earlier, already stale expectations.

## Governance and complete verification

Recorded in the section appended below after execution.

### Executed (2026-11-18)

| Check | Result | Note |
| --- | --- | --- |
| check-ox (local, after docs) | exit 0 | — |
| SDD validate, with and without `--check-convergence` | PASS | — |
| Governance suite (local) | exit 1: 251 tests, 3 failures, 162 errors | [final-governance-suite.log](final-governance-suite.log); 169 `OSError [Errno 122] Disk quota exceeded` while tests copy the repository into `/tmp`. `/tmp` holds ~22 GB of earlier copies (`ox-audit-final-copy-20261117`, `ox-historical-public-*`, `ox-r3-baseline-holder-20261118`, `ox-test-rsomktf7`), which were not deleted without authorization. Baseline was already red (5 failures, 129 errors). |
| Complete Toolbox run (`automate.sh run --scope complete`, explicit TOOLBOX_BIN) | exit 2 | [complete-verification.log](complete-verification.log), [complete-results.json](complete-results.json) |

Complete-run phases: passed — sdd-structure, ox, scripts-syntax, shellcheck,
ruff, rust-fmt, rust-check, rust-build, rust-test, machete, gitleaks, history,
opengrep, trivy, grype, bandit, malware; recorded — coverage, sbom. Not passed:

- governance-tests: failed (suite already red at baseline; local rerun shows
  `/tmp` quota exhaustion; the published log is truncated after 107 lines).
- scripts-tests: 139 tests, 1 failure + 1 error, both in
  `test_terminal_progress` signal-cancellation timing tests; no script or test
  file was changed by this task.
- rust-clippy (pedantic flags): exit 101, the same pre-existing sites listed in
  [clippy-pedantic.log](clippy-pedantic.log); none in new code.
- deny: 1 finding, duplicate `miniz_oxide` lock entries (Cargo.lock was already
  modified before this task and was not edited here).
- audit and osv: 1 finding each; the published assessments do not name the
  advisory and the raw report directory was removed by the runner.
- geiger: error, incomplete member reports (tool exit 101).

None of these phases has an input changed by this task except rust-clippy,
whose findings are in unchanged code. They remain open and are not approved.
