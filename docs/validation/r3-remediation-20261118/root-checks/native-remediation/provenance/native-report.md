# Native journey remediation — observations awaiting final checkout acceptance

Root owns only desktop.rs and the two maintained Python observation scripts. No product UI source was changed by root. Independent reviewer accepted desktop07 and Python03 static changes; Python04 review is pending. Existing original failed executions remain under root-checks; all candidate attempts below remain in this proposal directory until durable consolidation.

Six X11 scenario identities and their artifact, stale-input, wrong-result, cancellation, PID-liveness, native-close, keyboard-focus, scrolling, responsiveness and idle-CPU oracles were retained. The driver now follows current welcome/project/manual-recovery and IDE journeys. Each scenario uses private workspace/state and a controlled optional chooser exit-2 provider. This does not test an actual portal/dialog, cancellation exit1, real-user MRU or the whole project lifecycle.

| Observation | Actual result | Meaning |
| --- | --- | --- |
| X11 attempt01/source02 | 1 passed, 5 failed, exit101 | Old journey assumptions still unresolved |
| X11 attempt02/source03 | 1 passed, 5 failed, exit101 | Unresolved focus/render sequencing |
| X11 attempt03/source04 | 1 passed, 5 failed, exit101 | Diagnostic render work; response timer still included driver delay |
| X11 attempt04/source05 | 4 passed, 2 failed, exit101 | Incorrect single-tab control count caught by result42 and live-PID oracles |
| X11 attempt05/source07 | 6 passed, 0 failed/ignored, 57.668s, exit0 | All six candidate scenarios actually executed on recorded copied product/helper binaries |
| Wayland native_review attempt01/Python03 | exit0/natural_exit0; artifact42 preserved | INCONCLUSIVE: screenshots show Not verified; no acceptance claim |
| Wayland native_review attempt02/Python04 | exit0/natural_exit0 | Focused Verify control and Criterion approved badge visually observed |
| Wayland composition attempt02/Python03 | exit0/natural_exit0 | Criterion approved badge visually observed |
| Wayland composition attempt03/Python04 | exit0/natural_exit0 | Selected embedded workbench.rs, actual Tests dock, and Criterion approved badge visually observed |

Native07 SHA256 b49f9b621c99948d79c9b77cb5e5bdf6b26fb9a7dc944067950cda2af50c6f9f was integrated with an exact original-content precondition; rust-integration.json records both identities. No concurrent source edit was overwritten. Python04 forces a different public document transition S03→S04 before each task action, records the focused control, and binds the observing source, arguments and session mechanism to result.json. This removes ambiguity in repeated navigation; a more precise product-internal cause is not claimed.

Visual response samples exclude pointer positioning, focus preparation, settling and compilation. The native XTEST press/release and actual pixel-change wait are inside the measurement. Attempt05 retains 3 warmups/20 samples, nearest-rank p95 56.575587ms, max57.268379ms, bounded to this Xwayland setup. Concurrent governance load existed. This is not compositor-independent or assistive-technology performance acceptance. The original diagnostic-only product copy was never integrated or used as final acceptance evidence.

All successes are observations of captured inputs. Final Cargo compilation, the actual maintained commands against integrated paths, final scanner/full runs and independent validation remain required. Screenshot names are labels, not semantic proof; the native_review03 false-positive label above was explicitly rejected after viewing its contents.
