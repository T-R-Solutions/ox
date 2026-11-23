# Root executor observations — R3 remediation

Scope assigned by r3_orchestrator: Rust/native/real-scanner checks only, no product source edits. The root is an executor; these observations are not independent validation. Consulted `.codex/skills/software-testing/SKILL.md` for skipped scenarios versus internal subprocess helpers and environment evidence.

All Cargo commands used cwd `application/`, locked dependencies, offline mode where supported, and `CARGO_HOME=/home/rodrigo/Projetos/ox/.cache/ox/cargo-home`. Every result JSON has command, environment, duration and input comparison. Streams are retained as `<name>.stdout.log` and `<name>.stderr.log`. Input identities are `<name>-inputs.json`. Initial manifests cover application crates/tools/lock/manifests; later ones also include scripts and governance tools. A false `inputs_unchanged` on native composition includes concurrent governance edits; it does not imply its application sources changed. Design JSON inputs should also be related to the coordinator's complete baseline manifest.

| Check | Actual command | Exit | Duration | Record |
| --- | --- | --- | --- | --- |
| `cargo-build` | `cargo build --workspace --locked --offline` | 0 | 0.134s | `cargo-build-result.json` |
| `cargo-check` | `cargo check --workspace --locked --offline` | 0 | 0.467s | `cargo-check-result.json` |
| `cargo-clippy` | `cargo clippy --workspace --all-targets --locked --offline -- -D warnings` | 0 | 0.137s | `cargo-clippy-result.json` |
| `cargo-doc` | `cargo doc --workspace --no-deps --locked --offline` | 0 | 0.657s | `cargo-doc-result.json` |
| `cargo-fmt` | `cargo fmt --all -- --check` | 0 | 0.117s | `cargo-fmt-result.json` |
| `cargo-test-list` | `cargo test --workspace --locked --offline -- --list` | 0 | 0.920s | `cargo-test-list-result.json` |
| `cargo-test` | `cargo test --workspace --locked --offline` | 0 | 11.536s | `cargo-test-result.json` |
| `design-contrast` | `python3 /home/rodrigo/Projetos/ox/application/tools/check_contrast.py` | 0 | 0.019s | `design-contrast-result.json` |
| `design-generated` | `python3 /home/rodrigo/Projetos/ox/application/tools/build_design.py --check` | 0 | 0.021s | `design-generated-result.json` |
| `native-composition` | `python3 /home/rodrigo/Projetos/ox/application/tools/native_composition_review.py --output ../r3-remediation-20261118/root-checks/native-composition` | 1 | 40.188s | `native-composition-result.json` |
| `native-wayland` | `python3 /home/rodrigo/Projetos/ox/application/tools/native_review.py --output ../r3-remediation-20261118/root-checks/native-wayland` | 1 | 55.581s | `native-wayland-result.json` |
| `scanners-real-optin-enabled` | `python3 -m unittest discover -s /home/rodrigo/Projetos/ox/scripts/tests -p test_real_security_backends.py -v` | 1 | 139.447s | `scanners-real-optin-enabled-result.json` |
| `scanners-real-optin` | `python3 -m unittest discover -s /home/rodrigo/Projetos/ox/scripts/tests -p test_real_security_backends.py -v` | 0 | 0.042s | `scanners-real-optin-result.json` |

## Explicit native scenarios

`native-x11/result.json` records all six ignored desktop tests run in a dedicated headless Mutter + dedicated Xwayland session, with no primary-desktop input. Exit 101, 67.121s; one passed (`native_close_returns_success`), five failed (all remaining cases). Source hash is in the record. Logs and captures are in `native-x11/`. No tests were deleted or redefined.

Inspection: tests still wait for exact title `Ox — Fundação`, details/exit controls and bootstrap coordinates; current desktop title is `Ox — {surface} — ...`, with welcome/project selection and changed navigation. This is an obsolete journey harness, not a successful native acceptance or a reason to suppress failures. Updating it faithfully requires matching current documented journeys and preserving task-artifact, cancellation, responsiveness, focus and close oracles. No product or harness correction was made by root.

The ignored `project_store::process_store_helper` unit is an internal subprocess entry invoked by its parent tests (visible in Cargo logs), not an omitted native scenario.

Both maintained documented Wayland entries were executed against current binary in isolated Mutter sessions: `native_review.py` and `native_composition_review.py`, with fresh output directories here. Both exited 1, reporting `timeout: task artifact`; raw traces/result records remain in `native-wayland` and `native-composition`. They do not satisfy native acceptance.

## Real scanners

Central list succeeded read-only. The current OSV acquisition receipt was 2026-11-16T14:41:45.380351Z and central interval 12h; inspected native.py/databases.py show automatic refresh when expired. User explicitly authorized database download and publication through Toolbox in this session; this is not blanket central maintenance permission.

First opt-in command accidentally omitted OX_REAL_SECURITY=1 and skipped the test; retained `scanners-real-optin` is explicitly NOT successful integration. Corrected restricted run (`scanners-real-optin-enabled`) ran 11 subchecks and failed all with central execution receipts on read-only filesystem (139.447s); this is an environment failure. Escalated rerun uses OX_REAL_SECURITY=1, explicit TOOLBOX_BIN and shared SELinux selection; its result will be appended when complete. Scanners operate through their existing wrapper, without central code changes.

## Disposition and limits

Rust build/check/test/fmt/Clippy/docs and test listing passed; generated design and contrast checks passed. Regular cargo test alone omitted the six native scenarios, subsequently executed with failures above. No conclusion that all tests pass is supported. Root has not executed full automation or governance/scripts suites; the coordinator owns those observations. Application README, source tests, tools, design command documentation and logs were reviewed; there is no behavior/documentation change by this executor beyond this evidence record.


## Completed real-scanner observation

The escalated opt-in completed: exit 0; `Ran 1 test in 442.463s — OK`, covering all 11 subchecks in the real test. `scanners-real-optin-escalated-result.json` reports 442.509s wall time and `inputs_unchanged=true` for captured sources. `real-scanner-receipts.json` records the central native receipts in the matching time window, including OSV refresh metadata. This is an actual operational integration observation, not mocks.

The unittest accepts native findings classifications. Ruff had 15 actual diagnostics (imports/style in governance code/tests) captured in `.local/logs/2026-11-18/ox-security-ruff-pvBdjub6--tool--stdout.log.log`. These were sent to the coordinator for source repair and final reexecution; this earlier unittest success does not establish a clean final matrix. There are no remaining root-owned running processes. No source files were modified by root.


## OSV finding and environment limitation

The refreshed OSV native scan had exit 1 and the Ox assessment also reports `state=findings`, `exit_code=1`, `finding_count=1`. The raw observed report identifies `lru 0.16.4` and `RUSTSEC-2026-0253` (potential use-after-free due to lack of panic safety in `LruCache::pop()`). Raw files: `.local/logs/2026-11-18/ox-security-osv-YaIL7umC--tool--stdout.log.log` and matching `--assessment.json.log`. This is an observed scanner finding, not an independently established exploitability conclusion. No dependency, exception or policy change was made by root. The global error-free acceptance remains unmet.

A subsequent read-only sandbox command failed before executing Python: synthetic bubblewrap mount target `/tmp/.git`, quota exceeded (os error 122). The same OSV inspection succeeded through host escalation. This environment failure is preserved separately from the vulnerability and native-test failures. Host process observation used only PID/PPID/time/CPU/command name, not arguments; no process was killed by root.


## Concurrent input change detected

The coordinator detected external edits in six UI source files and a new `docs/validation/ide-shell-20261118` directory during the task. Root independently compared its original Rust test manifest with current bytes; exact changed paths/hashes are in `external-input-changes.json`. Earlier Rust/native executions remain observations of their captured versions, not acceptance of the current external UI changes. No external edits were overwritten or attributed to an unverified author.

Root consulted `.codex/skills/workspace-integrity-engineering/SKILL.md` for content-based conflict detection and observation invalidation. A read-only `codex_tui.list_threads` showed no other active writer visible on that connected app server; this does not exclude other tools/sessions. User was asked asynchronously to coordinate writer stability or continue with snapshot-bound evidence. No message was sent to third parties and no external process was stopped.


## New observation after external UI changes

Root repeated ordinary Cargo build/test/fmt/Clippy/docs and design generation/contrast checks on current captured inputs, without modifying any sources. All seven commands exited 0 and every captured input compared unchanged at the end of its command. The doc/design observations additionally capture docs/design/tokens.json, DESIGN.md and docs/design/surfaces.md. This does not establish that another writer will make no later change. Earlier failed X11/Wayland observations remain preserved on their earlier inputs; they were not relabeled as current native acceptance.

| Result record | Exit | Duration | Captured inputs unchanged |
| --- | --- | --- | --- |
| `current-ui-build-result.json` | 0 | 0.134s | True |
| `current-ui-clippy-result.json` | 0 | 0.545s | True |
| `current-ui-design-contrast-result.json` | 0 | 0.018s | True |
| `current-ui-design-generated-result.json` | 0 | 0.021s | True |
| `current-ui-doc-result.json` | 0 | 0.628s | True |
| `current-ui-fmt-result.json` | 0 | 0.124s | True |
| `current-ui-test-result.json` | 0 | 11.566s | True |


## Additional maintained skill consumers

Executed the two additional entries documented by tools/governance/consumers/README.md without source edits or downloads. Rust toolchain 1.99.1 was already installed; RUSTUP_AUTO_INSTALL=0 was explicit.

- `run_base.py <new report> --isolation`: exit 0, 16 model tests and seven process/filesystem tests passed, plus the four real Bubblewrap read attempts (baseline, permitted read, two denied reads). `consumers-base/receipt.json` includes commands, source/binary hashes and preserved temporary build path. The loopback and Unix-socket fixtures ran locally.
- Built gui.rs/gui_tests.rs with rustc +1.99.1, edition2024 and the observed Iced/x11rb rlibs. Both compiler commands exited 0. Exact source, lock, selected rlib and binary identities are in `consumers-gui-build.json`.
- `gui_test.py <new report>` ran under a private headless Mutter parent and dedicated Xwayland, using explicit OX_GUI_CONSUMER/OX_GUI_TESTS paths and build-observed SHA-256 values. Exit 0, one graphical test passed in11.96s; wrapper wall12.932s, captured inputs unchanged. Server was terminated by the runner; parent Session closed its own children. No primary-desktop input was used.
- Visually inspected both captures at240x180 and1600x1000: all four top actions fit, Quit is visible at minimum width, command/detail fields stay inside the window, and retained text is visible in the small capture. Large capture shows the expected collapsed detail state and Ready status. This is bounded library-consumer evidence, not current Ox product native acceptance.

Raw PPM files remain unchanged. view_image could not decode PPM directly; Pillow produced lossless PNG copies for actual viewing. `consumers-gui/visual-inspection-inputs.json` records both raw/view hashes, dimensions and conversion method. No screenshot pixels were edited. This is an artifact-viewing adjustment, not a test rerun or new acceptance claim.


## Final native addendum — 2026-11-19 UTC

The later current observations are retained in native-final/retention-manifest.json and native-final/application-report.md. Cargo workspace test02, Clippy02, fmt02, build/doc, design generation and contrast all exited0. Clippy01's actual failure remains retained; the only correction was independently reviewed equivalent let-chain desktop08, with no suppression/assertion/selection change. Final six native X11 scenarios all passed on integrated08 with0failed/ignored/filtered and unchanged inputs. Both maintained Wayland entries ran from their integrated paths on final product SHA39d517bb89494ba73725c4da2e7e7fd8b326f1abd3c38dce21a88a3593e03f86; root inspected the task verdict, editor and Tests dock frames.

WC07 then executed the complete seven-session current project journey (source60408be95b92e2c9f73a8a036e2f1a388a856007642b0e1ac003bf00dd3c7ad1), with100 explicit filesystem/lifecycle checks, seven natural exit0 sessions, unchanged observed inputs and exact acknowledged geometries640x480/1024x1000/1600x1000/2560x1000. Real GTK Zenity confirmation/cancellation, owned-child PID disappearance, exclusive creation/cancel/collision, two actual MRU projects/restart/move/missing/remove/reopen, narrow keyboard/themes and explicit corrupt-reset/exact backup were observed. Runtime uses private Wayland with GTK portals disabled; no default-portal, other compositor, hostile-writer or assistive-technology claim.

All WC01–06 failures/limitations remain retained. WC04's nominal1024/640 labels were rejected after its actual restored geometries and outside-window clicks were inspected; WC05's static-frame timeout was not accepted; WC06 was a bounded continuation, followed by the complete WC07 replay. Only the PID-owned, inode/type/UID-checked inactive socket endpoint was removed after all owned session children exited; no historical evidence or other sockets were removed.

The current maintainer review set is [visual-index.md](native-final/visual-index.md). AC07 visual acceptance was requested explicitly with that concrete set; no human acceptance was inferred. Independent technical validation and whole-feature gates remain separate. This addendum does not declare global remediation complete: final governance/package/automation/scanner execution, applicable gates and append-only closure remain coordinated work.
