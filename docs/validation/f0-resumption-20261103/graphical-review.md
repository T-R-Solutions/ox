# Graphical resumption review

Criterion: Q05/Q06/Q07 and the graphical portions of F0-P01, bootstrap AC-02,
local-task-ui AC-05/10/11. Methods: actual compositor input, protocol logs,
rendered captures, exact artifact bytes, controlled child readiness/absence and
natural application exit. Machine times in the raw records span 2026-11-03/04 UTC;
the directory name identifies the resumption, not a single observation timestamp.

The initial 220-input comparison found no changed inputs. At the initial observation stage, product source, manifests and lockfile were
unchanged. The later package-only Cargo profile successor below supersedes this
statement for the final build. The original binary
06a77993d29cef582d1f09dbca14c6546ee1390c088c65423004e98d597df52d executed
native-flow-1, native-probe-2 and three native-held runs. Matrix runs use an
identified copy adding update-message logging, initial window-size selection and
the existing two-point iced_winit client timer. No oracle is replaced with a
passing verdict. Held-oracle cases explicitly substitute the existing controlled
held fixture and expect cancellation/INCONCLUSIVE, never APPROVED.

Primary-session F0-RETOMADA-03, PID 2241725, used /tmp/oxf0resume3, with DISPLAY
unset and wayland-0. The maintainer reported completing the requested interaction.
Machine records independently correlate request identity and results 42/41 with
APPROVED/REJECTED, retained run history, Shift+Tab Focus(true), the hang child's
PID 2242487 and observed disappearance, followed by natural exit 0. The copied
binary's instrumentation/prefilled path are identified. The primary session has no
screenshot/performance claim. This resolves the earlier missing-workspace conflict
for the new run; it does not repair or reinterpret the old human report.

Isolated native Wayland: six support cells each completed good/bad verification,
visible focus and Shift+Tab, Enter/Space, history scrolling, responsive task
cancellation and natural exit 0. Original-binary native-flow-1 independently
completed the same journey. Three original-binary held-verification runs observed
responsive details toggling, INCONCLUSIVE after cancellation, actual oracle PID
absence and a second oracle's disappearance before close returned exit 0.

Visual review inspected original/native and scaled captures, including
native-flow-1 approved/rejected/retained-history/cancelled, native-probe-2
Tab-to-exit and Shift+Tab-to-details plus activation, native-support-1-640
approved-history, native-support-1.5-640 retained-history, native-support-2-900
reverse focus and native-support-2-640 cancellation; native-held-3 shows an
INCONCLUSIVE verdict and retained cancelled observation. Text wraps and scrolling
exposes content in short windows. X11 support captures at 640x480 show APPROVED
and at 200% show INCONCLUSIVE after held cancellation. Original PPM pixels are
retained; two PNGs are lossless format conversions for inspection.

## Discriminating failures and corrections

- The private compositor initially blocked on a 25-second GVFS activation timeout.
  The 55-second trace reached readiness; GIO_USE_VFS=local removed that private-bus
  dependency. A failed devkit/socket collision and Xwayland readiness-pipe failure
  remain recorded. The runner now uses its own display and retains the readiness
  pipe, with -noreset. These are test-environment corrections.
- Native first-input probe had wl_seat capabilities 0 until the first key created
  the virtual keyboard. Protocol logs show the first Tab release but no press.
  The corrected harness primes the device and waits for focus before navigation.
  The original failed sequence remains native-probe-1; native-probe-2 passes.
- X11 Shift failed the modifier-mask precondition using XTEST even inside the
  isolated compositor (x11-isolated-2), matching the previous failed precondition.
  The same held-Shift test passes with compositor-delivered input
  (x11-isolated-3), observes Focus(true), activates details and exits normally.
  The executable harness retains an explicit modifier-state assertion.
- All six existing X11 graphical scenarios then passed in each of the six cells:
  36 tests, no failures/ignored tests. The separate metric test was filtered out
  because its six-cell evidence was collected independently. Three additional
  held-verification runs under coverage instrumentation pass. Together with six
  successful instrumented frame/metric exits and three original-binary native
  held runs, these establish stable execution of the formerly inconclusive
  scenarios in the corrected controlled environment.

The new evidence supports the adopted corpus; it does not prove the cause of every
historical timeout or a zero flake rate on arbitrary desktops. In particular,
primary-session XTEST remains unsuitable for held-modifier acceptance. Original
failed logs are preserved, no timeout/criterion was relaxed, and no product fix
was invented to compensate for missing input. New platforms, compositors, workload
or physical-presentation requirements need new evidence.

## Full-history counterevidence and optimized-profile successor

Review of the full raw corpus found up to 429.99ms client drawing with history;
toggle-only passing metrics were insufficient. F0 was reopened before final
acceptance. Two disposable line/word splitting experiments failed and were not
applied. Keeping the original full-text interface and optimizing only tiny-skia
0.11.4 in the dev profile addressed the raster cost. No workload, budget, first-party
source, dependency version or lockfile was changed to make observations pass.

The optimized matrix preserves all six native journeys and 42 X11 tests, with
per-cell 20 measured responses after 3 warmups,3 ten-second idle windows and full-flow
RSS. check-optimized.py checks every logged client draw, including history and
startup, instead of selecting favorable toggle frames. The native repeat also
measures twenty responses after good/bad history exists. This finite replicated
corpus supports the bounded correction; it is not a universal flake-rate estimate.
Three X11 cells exposed mixed parent-resource/child-frame output. Dedicated
per-process stderr/resource files and whole-cell repeats replace those incomplete
measurements; strict frame-line parsing rejects corruption. Raw failures are in
optimized-instrumentation-final-review.json.
Original product-binary full-flow and held-verification repeats corroborate the
diagnostic builds without copied UI changes. Earlier primary-session observation
remains tied to its original profile, not claimed as an optimized-primary benchmark.

Visual inspection of optimized-native-1-640 retained-history shows the rejected
artifact and scrollable retained history; optimized-native-1-900 reverse-focus
capture shows the border restored to Details. optimized-native-2-900 cancellation capture visibly records observed exit and
missing result with no false approval. Additional scaled captures and X11
assertions retain layout, verdict, history, focus and cancellation checks. The
losslessly converted optimized-separated-x11-1.5-640 cancelled-verification
capture visibly shows INCONCLUSIVE after held cancellation. Full
raw snapshots and failed attempts remain available for independent inspection.
