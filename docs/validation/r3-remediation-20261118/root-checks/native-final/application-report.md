# Final application observations — root executor

These are execution observations, not independent validation or global task acceptance. All commands use the root Cargo cache and retained per-command source manifests. Streams stay outside the distribution until source/corpus coordination permits retention.

| Observation | Exit | Seconds | Input comparison |
| --- | --- | --- | --- |
| design-contrast | 0 | 0.019 | [] |
| design-generated | 0 | 0.024 | [] |
| native-composition | 0 | 32.386 | [] |
| native-wayland | 0 | 46.895 | ['application/crates/ox-app/tests/desktop.rs'] |
| rust-build | 0 | 9.432 | [] |
| rust-clippy-02 | 0 | 0.246 | [] |
| rust-clippy | 101 | 7.787 | [] |
| rust-doc | 0 | 2.938 | [] |
| rust-fmt-02 | 0 | 0.132 | [] |
| rust-fmt | 0 | 0.133 | [] |
| rust-test-02 | 0 | 11.607 | [] |
| rust-test | 0 | 14.583 | [] |

The initial final Clippy failed on one collapsible_if in the desktop test driver. The equivalent let-chain change was independently reviewed (desktop08 SHA96bc348f10bd2ac91cc28536e1278c5ba37c83bed796397682dc4820f211ccaf). No lint suppression, assertion or selection changed. Clippy02/fmt02/workspace-test02 then passed.

Both actual Cargo native executions ran all six explicit ignored desktop scenarios: source07 passed57.66s; final source08 passed58.099s with0failed/ignored/filtered. All application source identities were unchanged across final08, and actual product binary SHA39d517bb89494ba73725c4da2e7e7fd8b326f1abd3c38dce21a88a3593e03f86 was recorded with the helper binary identities. Reports/streams/captures are /tmp/ox-r3-native-final-20261118 and /tmp/ox-r3-native-final-02. Ordinary cargo test ignores these six; these separate actual runs satisfy their execution requirement. The ignored internal project_store subprocess helper is invoked by parent tests.

Both maintained Wayland commands were run from the actual integrated paths against the final product binary (no module ROOT/BASE override). Root visually inspected the approved task badge and scrolled verdict in /tmp/ox-r3-wayland-final-01, and approved badge, selected embedded workbench.rs and actual Tests dock in /tmp/ox-r3-composition-final-01. Their request/result42 and user-content sentinel are independent file oracles. Real portal/dialog and complete project lifecycle are not established by their controlled chooser-exit2 fixture.

The first Wayland final run overlaps the equivalent desktop test-source07→08 change. Its broad manifest flags only application/crates/ox-app/tests/desktop.rs; the actual observing Python, imported Session mechanism and product/helper binary bytes stayed the same. That test-source file is not a runtime input to the maintained Python entry. The composition observation subsequently has no manifest difference.

Additional WC replay attempts are separate. Keep WC01/02 timeout failures, WC03 helper socket lifecycle failure and WC04 width/menu counterevidence. Do not promote them merely from an observed/exit0 label. WC05 current geometry-aware replay is pending.

Full verification, integral governance final suite, real final opt-in scanners, independent package extraction/commands/export, whole-feature gates, human visual acceptance and append-only closure are not established by this application report.


## Final native addendum — 2026-11-19 UTC

The later current observations are retained in native-final/retention-manifest.json and native-final/application-report.md. Cargo workspace test02, Clippy02, fmt02, build/doc, design generation and contrast all exited0. Clippy01's actual failure remains retained; the only correction was independently reviewed equivalent let-chain desktop08, with no suppression/assertion/selection change. Final six native X11 scenarios all passed on integrated08 with0failed/ignored/filtered and unchanged inputs. Both maintained Wayland entries ran from their integrated paths on final product SHA39d517bb89494ba73725c4da2e7e7fd8b326f1abd3c38dce21a88a3593e03f86; root inspected the task verdict, editor and Tests dock frames.

WC07 then executed the complete seven-session current project journey (source60408be95b92e2c9f73a8a036e2f1a388a856007642b0e1ac003bf00dd3c7ad1), with100 explicit filesystem/lifecycle checks, seven natural exit0 sessions, unchanged observed inputs and exact acknowledged geometries640x480/1024x1000/1600x1000/2560x1000. Real GTK Zenity confirmation/cancellation, owned-child PID disappearance, exclusive creation/cancel/collision, two actual MRU projects/restart/move/missing/remove/reopen, narrow keyboard/themes and explicit corrupt-reset/exact backup were observed. Runtime uses private Wayland with GTK portals disabled; no default-portal, other compositor, hostile-writer or assistive-technology claim.

All WC01–06 failures/limitations remain retained. WC04's nominal1024/640 labels were rejected after its actual restored geometries and outside-window clicks were inspected; WC05's static-frame timeout was not accepted; WC06 was a bounded continuation, followed by the complete WC07 replay. Only the PID-owned, inode/type/UID-checked inactive socket endpoint was removed after all owned session children exited; no historical evidence or other sockets were removed.

The current maintainer review set is [visual-index.md](visual-index.md). AC07 visual acceptance was requested explicitly with that concrete set; no human acceptance was inferred. Independent technical validation and whole-feature gates remain separate. This addendum does not declare global remediation complete: final governance/package/automation/scanner execution, applicable gates and append-only closure remain coordinated work.
