# F0 quality refinement proposal

Status: PROPOSED milestone requirements. Documentary refinement is authorized by
the maintainer's “ok, efetue os ajustes recomendados”. This refines the
[F0 gate](../foundation-current-20261101/f0.md); D1–D5 still require adoption.
No operational results or milestone acceptance are recorded by this document.
Q01–Q13 are UNVERIFIED as expanded operational clauses. Existing observations may
support parts of them only after criterion-level review; no approval transfers here.

Frontend, backend, security, performance, testing and integrity all require evidence.
Compilation or one isolated test cannot establish completion. POL-04's priority for
reliability and preservation remains. Apply these clauses to the existing Linux
x86_64 foundation and bounded host/runtime/verifier/task-UI slices.

## Proposed verifiable clauses

| ID / F0 mapping | Required observation and oracle | Inputs / remaining work |
|---|---|---|
| Q01 / P01, P06 | Exact validated toolchain, versioned lockfile, reproducible build procedure; check/fmt/clippy/tests without unexplained warnings or skips; candidate updates evaluated separately. | Adopt the [version policy](../../decisions/version-update-policy.md); identify source, tools, features, native dependencies and environment. Reproducibility does not imply byte-identical binaries. |
| Q02 / P01, P03, P05 | Unit tests cover rules/states/boundaries; integration tests exercise real communication. Explicit critical success, rejection, error, cancellation and recovery scenarios, with contract-based explanations for inapplicable paths. | Inventory actual assertions/fixtures, not test counts; identify missing scenarios even if aggregate tests pass. |
| Q03 / P01, P05 | Measure total foundation coverage and changed-code coverage separately; initial >=80% changed executable-line target with the calibration and exception rules below. Critical behavior remains mandatory. | Tool, baseline, numerator, denominator and component gaps; no percentage measured by this refinement. |
| Q04 / P01, P05 | Regression test fails on the reproduced defect and passes on the correction for the intended behavioral reason; retain test and both observations. | Defective/corrected snapshots, oracle and environment. If automation is infeasible: repeatable alternative, rationale, evidence, owner and automation revisit trigger. |
| Q05 / P01 | Existing UI uses shared colors, typography, spacing, components and visual states. Real input covers keyboard/focus, processing, actionable errors, cancellation and explicit verification; success follows the independent verdict. | Minimal design system applied to existing screens; frontend/backend state mapping, screenshots, interaction traces and observed backend/process exit. |
| Q06 / P01 | Contrast, named scale/window-size cases and absence of clipped essential content; reference-image comparison plus inspection of intended differences; separate X11 and native Wayland interaction. | Theme/fonts/renderer/compositor/scale/window/capture/comparison tolerance. Screenshots cannot replace interaction; reference updates cannot erase regressions. |
| Q07 / P01, P03 | Responsive UI, appropriate async I/O/waits, bounded workers/concurrency; cancellation stops actual work and releases owned resources; late results cannot affect a newer attempt. | Barrier/event-based race scenarios, bounded timeouts, resource limits and injected failures; actual exit/reap/socket checks. No mandatory general runtime or universal async conversion. |
| Q08 / P01 | Measure interaction latency, frame time, memory and CPU, establish baseline, then adopt numeric limits before F0 closure and verify them. | Hardware/OS/display/tools, build profile, workload, warm-up/repeats, units/distributions and noise treatment. Baseline alone cannot approve responsiveness. |
| Q09 / P02 | Initial threat model maps assets, trust boundaries, permitted actors/effects and threats to controls and adversarial scenarios. Independent observation proves each claimed prohibited effect did not occur. | Permission/integrity tests and residual risks. Host API denial is not OS confinement; isolation claims require OS enforcement and denied-effect tests. |
| Q10 / P02, P06 | Review direct/transitive dependencies, advisories, licenses and native/unsafe boundaries; record dispositions and unresolved items. | Resolved inventory/lockfile/features/target, tool/advisory database versions/dates, licenses and exception owners/triggers. Clean scanner output does not prove security or rights. |
| Q11 / P03, P07 | Versioned contracts demonstrate compatible communication, predictable malformed/incompatible/unauthorized failures, cancellation, bounded concurrency, shutdown and cleanup. | Current fixtures and anticipated extension seams; version negotiation, ownership, migration/revisit triggers. No guarantee of zero redesign or complete public SDK. |
| Q12 / P04 | Proposed durable-storage deferral retains independent pre-MVP acceptance. Current core/UI must not advertise volatile session history as restart-safe acceptance or durable recovery. | Review current source/user-visible claims; future product-local-persistence evidence. Deferral does not waive present honesty or automatically make the entire row NOT APPLICABLE. |
| Q13 / P05, P06 | Independent adequate oracles and current code/oracle/contract/environment bindings for every clause. Missing/stale/contradictory/skipped evidence cannot approve; failures and legitimate successors are preserved. | Requirement → decision/risk → task → change → observation → verdict; negative evidence/input controls. Structural checks do not accept product behavior. |

## Coverage protocol

Select and validate the measurement tool/version, compiler/instrumentation, targets,
features, included crates/tests and line mapping before measurement. Rust source
coverage is a candidate, not a tool installation made here. Verify capture of spawned
helpers and graphical processes or report missing coverage explicitly.

Freeze baseline and candidate manifests including dirty/untracked files; Git HEAD
alone is insufficient. Changed-code coverage is executed eligible added/modified
executable lines divided by all eligible added/modified executable lines. Report
both counts. Zero denominator means not applicable to this metric, not 100%.
Retain removed-line behavior in regression review. Exclude generated/vendor code,
test fixtures and nonexecutable lines only by documented rules; handwritten UI logic
is not automatically excluded.

Report total foundation coverage separately, with per-component gaps and critical
paths. A tiny diff cannot conceal existing untested critical behavior. This does not
invent an 80% total-code requirement or grandfather existing critical gaps.
The initial 80% changed-line target is an Ox engineering proposal. Calibrate after
the first reproducible measurement and before closure. Any adjustment needs an
explicit decision with evidence/consequences, not a silent reduction after failure.
Exceptions identify files/lines, reason, risk, alternative verification, owner and
expiry/revisit trigger. Show excluded lines separately to prevent metric inflation.
Critical scenarios remain mandatory regardless of percentage or exceptions.

## UI, performance and cancellation details

Enumerate keyboard focus/activation and invalid-input, running, cancelling, failed,
verified and stale states for the existing controlled task journey. Define a scale
and window-size support matrix. Select applicable WCAG 2.2 text/non-text contrast,
keyboard and visible-focus criteria, with exact thresholds/method and desktop
applicability before review. This is not full WCAG conformance or unobserved
assistive-technology support. Keep design-system scope to existing screens.

Agree workloads and measurement boundaries before collecting performance data;
then adopt budgets from the baseline and product needs before final acceptance.
Compare candidate/baseline under comparable inputs, recording uncertainty and
investigating material regressions. Unavailable/noisy observations remain UNVERIFIED
or INCONCLUSIVE. Do not import Zed's frame budget or invent Ox targets without data.

Async tasks alone do not prove responsiveness or external-process cancellation.
Observe actual termination under the declared direct-child boundary; descendants
and effects outside it need a separate contract before stronger guarantees.
Late events carry attempt identity; deterministic tests must show stale rejection.

## Inventory and execution order

1. Adopt/amend F0-D1–D5, risk dispositions and applicable Q01–Q13 clauses.
2. Classify each clause: implemented with sufficient evidence, implemented without
   sufficient evidence, absent, or justified outside scope. Record source/assertion/
   artifact/input references and SDD verdict separately; inventory labels do not
   replace the five states.
3. Measure total/changed coverage and UI/performance baselines; identify missing
   scenarios and decide methods, limits and exceptions.
4. Implement only authorized tests, instrumentation and bounded fixes for observed
   gaps, preserving defect reproductions and prior observations.
5. Execute applicable checks, including real GUI and negative cases. Reevaluate
   only affected inputs and expanded criteria.
6. Close F0 only with APPROVED or justified NOT APPLICABLE applicable clauses.
   Unadopted thresholds, missing evidence, failures and skips cannot approve.
   Persistence remains separately accepted before MVP under the proposed deferral.

This refinement does not perform steps 2–5 as product validation. Inventory must
identify actual gaps rather than assume all proposed tests are absent.

## Official sources consulted in this conversation

[Cargo CI](https://doc.rust-lang.org/cargo/guide/continuous-integration.html) and
[requirements](https://doc.rust-lang.org/cargo/reference/specifying-dependencies.html)
support dependency resolution/testing distinctions. The
[Zed checklist](https://zed.dev/docs/development/ui-checklist) supplies UI review
dimensions. [Iced 0.14 Task](https://docs.rs/iced/0.14.0/iced/struct.Task.html)
documents concurrent actions/futures/abortable tasks, not external-process termination
guarantees. [WCAG 2.2](https://www.w3.org/TR/WCAG22/) supplies identifiable accessibility
criteria. They do not mandate Ox's 80% target, tooling, envelope or verdicts.
