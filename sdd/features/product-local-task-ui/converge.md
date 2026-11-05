# Convergence: product-local-task-ui

All criteria UNVERIFIED. Specification is provisional; no integration code or graphical acceptance yet. Governance reconciliation is in progress.

## Artifact protocol implementation

Governance AC-01..04 and metadata inventory AC-01..02 were reexamined with new
independent-export checks; current evidence is in governance-reconciliation/local-task-ui-03.
New local-task and task-oracle binaries implement request identity plus result=42.
Direct process scenarios good/bad/failure/missing/wrong-identity/preexisting-result
behaved as expected; preserved sentinel bytes. See artifact-01/results.json.
This is partial implementation: no Runtime/Engine/Iced wiring, cancellation, input
refresh or actual graphical acceptance yet. All UI criteria remain UNVERIFIED.
Next concrete implementation: worker-owned Runtime/Engine controller in ox-ui,
correlated messages and graceful window close, then real graphical acceptance.

## Implementation and current verification — 2026-10-30

Controller, dedicated workers and actual Iced controls are implemented. Real Runtime
and Engine process tests pass, including correct/incorrect results, missing evidence,
staleness/history, inaccessible paths, cancellation and timeout. A late duplicated
completion after editing a workspace path was found during review and corrected;
request generations advance on edits and completion requires an active operation.
All five Cargo commands passed with unchanged captured inputs in final-checks-02.
The socket-restricted sandbox failure remains preserved separately.

Final independent export: 957 files, exact manifest/input agreement, five checks and
34 tests passed; no Git metadata or new product records leaked into governance.
Evidence: docs/validation/product-local-task-ui/final-export.

Graphical acceptance remains open. Wayland surface/commit protocol and real window
interaction observed; maintainer confirmed workspace validation enabled all four
execution buttons, then reported a difference without its details. A 600s manual
session ended by supervisor SIGTERM, not graceful closure. A further session was
opened for photographs at the maintainer request (1800s observation window).
No approval is inferred from its existence or generated task artifacts.

X11: native close passed, pointer-driven tests failed location/exit assertions.
All attempts preserved in x11-01..04. The end-of-scenario pointer restoration
experiment did not solve placement and was preserved then reverted; existing
restoration behavior retained. New ignored local_task_rendered_flow adds real
keyboard/pointer and captured-frame scenarios, not internal state calls. Do not
claim XTEST repaired. Await the maintainer's photo/details, investigate the reported
difference, then validate native close during active work and finish graphics.

## Final acceptance — 2026-10-30

All 11 declared criteria APPROVED. Current evidence.json binds new observations and explicitly reviewed reuse. See docs/validation/product-local-task-ui/acceptance/review.md and graphical-review.json. All five Cargo checks pass; 23 regular tests and all three explicit X11 tests pass. Native Wayland confirmed by protocol trace, human interaction and process exits. Earlier failures remain preserved. The bounded local slice is accepted; full F0 and excluded roadmap work remain outside scope.

## F0 operational successor — 2026-11-03

Current evidence is E-F0-EXECUTION-CURRENT in evidence.json and the
operational report at `docs/validation/f0-execution-20261102/report.md`.
Historical results above retain their original scope and inputs. F0 remains OPEN;
GUI/native/performance limitations are explicit in the current matrix.

Final review: E-F0-FINAL-REVIEW. F0 stays OPEN; current per-criterion states are
in evidence.json and docs/validation/f0-execution-20261102/matrix.json. Product
operational records are excluded from the governance-only export.

## Graphical resumption successor

The former open graphical criteria are supported by the identified primary native
journey, six native support cells, 36 X11 tests, three native held-verification runs
and three covered X11 held-verification repeats. Twelve separately measured cells
meet the explicitly adopted GUI contract. See E-F0-RESUMPTION and
docs/validation/f0-resumption-20261103/report.md for inputs, methods, checks and
limits. Earlier open conclusions above remain historical. This accepts the bounded
F0 foundation; no subsequent feature or persistence implementation is authorized.

## Final raster-profile successor

E-F0-RASTER-CLOSURE supersedes the withdrawn provisional conclusion and the
full-history failure after a bounded package-only tiny-skia dev optimization.
Current 12-cell functional/performance evidence, original-product corroboration
and ordinary checks support the applicable criteria. F0 is accepted only in the
adopted local foundation corpus; no subsequent roadmap or persistence work is
authorized. Exact historical bytes and failure observations remain preserved.


## Robustness successor — 2026-11-05

See docs/validation/robustness-20261105/report.md and current evidence.json.
The archived predecessor retains historical acceptance on its exact inputs.
New Engine input handling and child cleanup have focused process/API evidence;
actual GUI response/close/rendered-state and F0 performance on this build remain
UNVERIFIED. T903 records the exact missing observation. No storage, real-agent or
plugin-desktop implementation is added; historical F0 closure is not erased.

Current successor: AC-01..04/06..09 APPROVED for tested bounded API/process
behavior; AC-05/10/11 UNVERIFIED pending actual graphical response/close/display
observation. No API test is promoted to GUI acceptance.
