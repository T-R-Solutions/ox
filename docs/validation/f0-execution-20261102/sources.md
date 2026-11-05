# Direct source review — 2026-11-02

External sources inform methods; repository authorities and the maintainer adopt
Ox requirements. No source establishes an 80% coverage guarantee, universal latency
budget, sandbox, Rust soundness or acceptance of this implementation.

Institution eligibility: [QS 2025 official subject page](https://www.topuniversities.com/university-subject-rankings/computer-science-information-systems/2025)
and its [QS regional page](https://www.qs-topuniversities.cn/en/university-rankings/university-subject-rankings/2025/computer-science-and-information-systems)
identify the edition. Their retrieved dynamic table omitted rows; the consulted
[reproduced QS table](https://www.ieeuc.com.tw/upload/web/2025QS/2025_QS_Computer_Science___Information_Systems%E6%8E%92%E5%90%8D.pdf)
shows MIT 1, Stanford 2, CMU 3 and Washington 19. This is a disclosed secondary
transcription for rank membership, not evidence of technical quality.

| Directly consulted source | Kind, result/method and limitation | Ox-specific use |
|---|---|---|
| Kazman, Klein, Clements, [ATAM: Method for Architecture Evaluation](https://sei.cmu.edu/library/atam-method-for-architecture-evaluation/), CMU/SEI-2000-TR-004, August 2000 | Method for architectural risks and quality-attribute tradeoffs; report record/abstract consulted. Not a causal efficacy claim for this project. | Scenario/environment/response/oracle/owner rows, explicit competing boundary choices. This is a proportional adaptation, not a completed formal ATAM engagement. |
| Just, Jalali, Inozemtseva, Ernst, Holmes, Fraser, [Are mutants a valid substitute for real faults in software testing?](https://homes.cs.washington.edu/~mernst/pubs/mutation-effectiveness-fse2014-abstract.html), FSE 2014, pp. 654–665 | Empirical: 357 real faults, five applications, statistically significant correlation between mutant and real-fault detection after considering coverage. Author-hosted abstract consulted; PDF timed out. Correlation and sampled programs do not establish equivalence for Rust/Iced. | Three targeted artificial defects challenge selected critical oracles; no mutation-score target or whole-program inference. |
| John Ousterhout, [Always Measure One Level Deeper](https://www.cl.cam.ac.uk/teaching/2425/P56/files/ousterhout2018always.pdf), CACM 61(7), July 2018, DOI 10.1145/3213770; Stanford author, university-hosted full article | Measurement recommendations with examples, not an Ox benchmark. Investigate underlying mechanism and measurement artifacts. | Separate worker polling, capture, process exit and input-to-pixel boundaries; timer samples cannot claim compositor frame presentation. |
| Chen, Ziegler, Chajed, Chlipala, Kaashoek, Zeldovich, [Using Crash Hoare Logic for Certifying the FSCQ File System](https://pdos.csail.mit.edu/6.828/2018/readings/fscq-sosp15.pdf), MIT CSAIL, SOSP 2015, DOI 10.1145/2815400.2815402 | Formal specification/proof plus prototype experiments. Crash conditions and recovery are part of the model; proof assumptions and implementation boundary matter. Not proof of arbitrary filesystem/hardware or Ox. | Retain future common recovery/corruption/acknowledgement contract; no storage technology selected, implementation or power-loss guarantee. |
| Google, [Code Coverage Best Practices](https://testing.googleblog.com/2020/08/code-coverage-best-practices.html?hl=no), August 2020 | Documented industrial recommendations: coverage exposes untested code but does not demonstrate test quality. | Separate total/changed denominators and challenge behavior; 80% remains the inherited engineering proposal. |
| Petrović, Ivanković, Fraser, Just, [Practical Mutation Testing at Scale: A view from Google](https://research.google/pubs/practical-mutation-testing-at-scale-a-view-from-google/), IEEE TSE, 2021 record | Industrial empirical evaluation: incremental mutation and relevance filtering at Google; platform/organization-specific. Publication page and abstract consulted. | Bounded, purposeful mutation in disposable copies; not adoption of Google's infrastructure or effectiveness estimates. |
| Google SRE, [Release Engineering](https://sre.google/sre-book/release-engineering/) | Documented industrial process for identifiable/reproducible release inputs; not binary identity guaranteed by Cargo.lock. | Exact toolchain/lockfile/source/config baseline and independent candidate promotion; no release/publication performed. |
| Microsoft Research, [CHESS](https://www.microsoft.com/en-us/research/project/chess-find-and-reproduce-heisenbugs-in-concurrent-programs/), established 2008 | Tool/method: explore and reproduce differing thread schedules. Not used here and not evidence that one readiness barrier exhausts schedules. | Process readiness markers fix the tested cancel-after-start ordering; residual schedules explicit. |
| Microsoft, [SDL practices](https://www.microsoft.com/en-us/securityengineering/sdl/practices) | Documented industrial security design/threat-review practices; no compliance certification. | Map assets, actors, permitted effects, controls, negative observations and residual risk. |
| Newcombe, Rath, Zhang, Munteanu, Brooker, Deardeuff, [How Amazon Web Services Uses Formal Methods](https://www.amazon.science/publications/how-amazon-web-services-uses-formal-methods), CACM, 2015 | Industrial experience with formal specification/model checking for critical designs since 2011. Not a proof of Rust code or a requirement to add TLA+ here. | Distinguish modeled transitions from actual subprocess evidence; avoid transferring distributed-system guarantees. |

Version-specific official contracts consulted: [Rust Child, page identifying 1.99.1](https://doc.rust-lang.org/std/process/struct.Child.html)
(no automatic child cleanup; wait observes termination), [Rust coverage](https://doc.rust-lang.org/rustc/instrument-coverage.html)
(profiles written on termination), [Cargo version requirements](https://doc.rust-lang.org/cargo/reference/specifying-dependencies.html),
[Iced 0.14 focus operation](https://docs.rs/iced/0.14.0/iced/widget/operation/fn.focus_next.html),
[iced_widget 0.14.2 Button](https://docs.rs/iced_widget/0.14.2/iced_widget/button/struct.Button.html)
and the corresponding installed source. Button keyboard behavior was established
from installed source plus real failure/repaired interaction, not documentation absence.

[WCAG 2.2](https://www.w3.org/TR/WCAG22/) supplies selected checks: normal text 4.5:1,
non-text indicators 3:1, keyboard operation and visible focus. Desktop scope is an
explicit adaptation; no full WCAG or assistive-technology conformance is claimed.

RustSec: revision `263a4d951a0867d4bddc29dddd6d59427c78f9a7`, downloaded public
archive; exact archive digest, candidate records and numeric-range review are local
artifacts. [Maintainer issue for ttf-parser](https://github.com/harfbuzz/ttf-parser/issues/217)
was consulted directly. Local matching is not cargo-audit or an exhaustive security audit.

Additional timing-boundary inspection (2026-11-03): official iced_winit 0.14.1
registry source src/lib.rs was read directly around interface.draw and
current_compositor.present, with original digest in frame-instrumentation.json.
The docs.rs source URL was unavailable through the web reader. A local isolated
copy adds monotonic timers without changing the product manifest/lockfile; the
measured interval is client draw-through-present-return, excluding earlier layout,
compositor scheduling and physical presentation. The official
[Wayland frame request specification](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_surface-request-frame)
was consulted directly: a scheduling callback is not a physical presentation
timestamp. Existing callback samples are retained but are not accepted as frame time.
