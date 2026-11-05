# F0 acceptance after graphical resumption

F0 is APPROVED within the explicitly adopted local Linux x86_64 foundation
boundary, subject to the accompanying current integrity checks. This successor
replaces the provisional closure withdrawn by history-counterevidence.json.
It preserves that counterevidence and all failed runs; it does not reinterpret
a passing toggle-only sample as a passing full journey.

| Blocker | Correction and verifiable evidence |
| --- | --- |
| Native Wayland journey correlation | primary-native-1 independently ties the identified human interaction to request/result bytes, APPROVED/REJECTED history, keyboard events, child disappearance and exit 0. Six optimized-native cells repeat actual native protocol interaction with session/build/workspace, captures, exact good/bad artifacts, cancellation and natural exit. optimized-original-flow corroborates the current product binary without diagnostic UI changes. |
| Shift+Tab / graphical instability | Preserve failed XTEST modifier assertion and first-key readiness probe. Correct harness device readiness, private-bus VFS dependency, display readiness and compositor keyboard delivery. Actual held-Shift/focus/activation assertions pass. Current matrix: six native journeys and 42 X11 tests, plus current original-binary held cancellation/close. Earlier three native held and three coverage-instrumented held repetitions remain supporting historical observations. |
| Performance contract / support matrix | Maintainer explicitly adopted decision-proposal.md. Full-history draw then exposed a real product-build performance failure, up to 429.99 ms. Optimize only locked tiny-skia in the dev profile; first-party code remains unoptimized. Revalidate all 12 cells, including every raw full-history client draw and full-flow resource samples. |

| Metric | Maximum across current 12 cells | Adopted limit |
| --- | ---: | ---: |
| Input to observed changed GUI pixels | 59.217 ms | 120 ms |
| Client draw through presentation-call return, full recorded corpus | 74.055 ms | 125 ms |
| GUI lifetime high-water RSS | 56.102 MiB | 64 MiB |
| Idle CPU, maximum of 36 windows | 0.000% of one core | 5% |

Acceptance uses the maximum of twenty response samples after three warmups per
cell and three idle windows of at least ten seconds. The client-frame review is
more conservative: every recorded draw, including startup and full history, is
checked. RSS uses 20 ms process sampling and kernel lifetime high-water values
through the task/history/cancellation corpus. CPU ticks are 100 Hz; zero measured
delta is below observation resolution, not zero work. optimized-checks.json lists
all cell values, counts, functional checks and raw run paths. The original backend
and separately bounded large-history budgets/corpus are unchanged. The backend
example was rerun with the current build: execute16.043ms, verify3.412ms, direct-child
cancel0.094ms, verification cancel2.354ms and direct-harness RSS8.364MiB, within
50/50/100/100ms and32MiB. See optimized-backend-checks.json. Non-rendering
large-history source/dependency inputs are unchanged; its renderer-free dependency
graph does not include tiny-skia, so its original three-run corpus remains pertinent.

Adopted support: X11 and native Wayland separately, scales 100/150/200%, logical
640x480 and 900x700, on the identified host. Native matrix uses isolated headless
Mutter/PipeWire capture; X11 uses rootful Xwayland in that compositor and client
framebuffer capture. Actual display configurations, process identifiers, events,
source/test snapshots and diagnostic binary identities are retained. Primary
Wayland interaction is a separate earlier-profile observation; it does not prove
primary-desktop performance for the optimized build. No physical frame exposure,
unobserved compositor/GPU combination or general accessibility conformance is claimed.

The product delta is only application/Cargo.toml's package-specific dev override
for existing tiny-skia 0.11.4. First-party Rust sources, dependency versions and
lockfile are unchanged from the initial accepted-input comparison. Failed line/
word subdivision candidates remained disposable. Governance changes add exactly
one operational-evidence export exclusion and its regression assertion. No commit,
publication, global installation, transmission, storage implementation or roadmap
expansion occurred.

All 20 rows of matrix.json are APPROVED; explicitly excluded future capabilities
remain NOT APPLICABLE with their adopted reasons. P01/P05 inherit the new GUI/build
validation; Q05/Q06/Q07 use current rendered/input/cancel observations; Q08 uses
full-corpus maxima; Q13 and product-f0-gate AC-05 require current evidence bindings,
negative controls and acceptance checks. Other clauses retain unchanged semantic
inputs and independently recorded security/coverage/domain evidence; no new
coverage percentage is invented for an unchanged first-party line set.

Ordinary current checks: offline workspace build/check/test, fmt and clippy, plus
reconstruction of the exact diagnostic build. Explicit GUI tests supply the
coverage omitted by ordinary ignored desktop tests. The full 46-test governance
suite already passed after the helper/test change; final schema/freshness,
acceptance negative controls and export regression validate current documents.
See optimized-product-checks.json and closure-checks.json for actual command exits.

No remaining blocker in the adopted F0 corpus. Broader platform, physical-scanout,
assistive-technology and persistence decisions remain separate future work, owned
by the maintainer; they are not silently promoted to tested support. Persistence
is still required before F3/MVP and its implementation remains unauthorized.
