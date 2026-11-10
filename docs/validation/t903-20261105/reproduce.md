# T903 local reproduction

Read report.md and the adopted boundary before replaying. No primary desktop input,
remote agents, product persistence, global installation or dependency update.
Installed Mutter/Xwayland, GI/GStreamer/PipeWire/Pillow, libX11 and pinned offline
Rust cache are prerequisites. Compositor sockets/input need effective graphical
permissions; the initial sandbox denial is preserved in probe-native/result.json.
Never reuse an existing output directory.

Historical first trial: product-inputs.json, instrumentation snapshots and
before-diagnostic-desktop.rs.bin identify the original rendering and current
robustness Engine. `history-native-2-900` is the counterexample (32 real Verify
observations); original binary copy is /tmp/ox-t903-before-history-fix. The committed
historical f0-resumption corpus was not overwritten. Newline-column candidate and
current product bytes are separate; current-product-inputs.json freezes the latter.

`run-current.py` records build, graphical matrix, 32-entry journeys, FIFO, held
verification, original binary corroboration and ordinary checks. It has fixed
observed output names and must not be blindly replayed into them. Copy/adapt with
fresh names after verifying source hashes. Helpers and instrumentation are local
source artifacts, not evidence of successful execution by their mere existence.
Each runner may return process exit0 while result.json contains an error; inspect
both. `check-current.py` rejects missing/failed inherited-corpus observations.

Disposable diagnostic root /tmp/ox-t903-app copies application manifests/toolchain/
crates; differences are the local iced_winit timer patch, corresponding local lock
entry, message logs, workspace default and size selectors, and the retained X11
instrumented test observer. Engine/Runtime/controller/fixture sources stay identical
to the observed product. Do not use historical prepare-optimized.py: it deliberately
rejects new source hashes. Reconstruct from current-product-inputs plus explicitly
retained instrumentation deltas, not by overwriting a mismatching scratch tree.

Native runs remove DISPLAY and log actual xdg/wl protocol. X11 standard tests remove
WAYLAND_DISPLAY, find the X window by PID and assert geometry/focus. Extra FIFO/
history runs use their own Xwayland, remove WAYLAND_DISPLAY and focus its Ox window
through focus-x11.py; stdout identifies the actual X window. ctypes is observer-only,
not first-party Rust unsafe. Capture uses isolated compositor pixels for these
additional runs, unlike standard X11 get_image. Neither method proves scanout.

The 32-entry loop is distinct from the two-entry historical journey and from the
renderer-free two-15-MiB-input memory stress. It must observe maximum run32, retain
20 measured scroll responses after3 warmups and all frame timings; body logs and
bottom screenshots expose retained text. A response sample and a client frame time
have different boundaries. Native captures arrive asynchronously; 20ms wait polling,
compositor/capture scheduling and 100Hz CPU ticks limit interpretation.

Cancellation is cooperative. The held fixture substitutes only the owned oracle,
records its direct-child PID and live worker TID, then observes both disappear;
close observes application exit and child absence. No descendant containment,
blocked regular-file interruption, power-loss or universal close deadline claim.
FIFO paths and damaged artifacts belong only to fresh fixtures. Preserve failures;
fix observer preconditions before attributing a timeout to the product.
