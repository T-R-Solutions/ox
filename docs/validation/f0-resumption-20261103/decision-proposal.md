# Proposed GUI acceptance contract

Status: PROPOSED, awaiting explicit maintainer adoption. This proposal does not
change the already adopted backend/history budgets or accept F0.

Scope: existing controlled local task UI, Linux x86_64, identified Ryzen 9 7900X /
openSUSE host, pinned Rust/Iced/lockfile, dev build and tiny-skia renderer. Record
actual compositor, GPU, scale, dimensions and instrumented/uninstrumented build
identity for every run. New hardware/workload/backend requires reassessment.

| Metric | Proposed limit | Statistic and observation |
| --- | --- | --- |
| Input to observed changed GUI pixels | <=120 ms | Maximum of 20 samples after 3 warmups per matrix cell; disclose capture/poll resolution |
| GUI RSS | <=64 MiB | Maximum sampled process RSS during the bounded GUI corpus, with sampling period stated; excludes the separately adopted large-history corpus |
| Client draw through presentation-call return | <=125 ms | Maximum observed duration, 20 samples after 3 warmups per cell, identified two-point instrumentation; excludes earlier layout and physical scanout |
| Idle CPU | <=5% of one core | Process CPU-time delta / 10 s wall-time, three idle windows per cell; report resolution and all samples |

Support matrix: X11 and native Wayland separately; each at 100%, 150%, 200%,
with logical content sizes 640x480 and 900x700 (12 backend/scale/size cells).
Record physical dimensions too. The acceptance corpus includes keyboard focus,
Tab/Shift+Tab, Enter/Space, scrolling, good/bad task verification, responsive
cancellation, retained volatile history and owned-process exit. Correlate each
journey with its workspace, artifacts and build. A nested compositor must be
identified as such; it cannot silently establish primary-session support.

Prior observations cover X11 visual/resize cases at all three scales, but do not
establish all per-cell performance measurements, native Wayland journeys or
Shift+Tab. The prior frame run at scale 1 timed out at final keyboard exit.
Physical presentation, assistive technology and full WCAG conformance are not
claimed. Missing or failed observations remain undecided/failed as appropriate.

Alternatives: adopt this bounded contract; revise metric/statistic/support cells
explicitly before acceptance. A revision must preserve unmet requirements and
explain its rationale rather than turn a failed observation into a pass.
