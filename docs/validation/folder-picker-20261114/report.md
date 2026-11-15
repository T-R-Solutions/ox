# Folder picker — 2026-11-14

## Scope and criteria

Existing-directory chooser on S01; preserve manual entry and Controller semantics.

| Criterion | Method and expected result | Status |
| --- | --- | --- |
| FP-01 | Source/tests and real GTK confirmation: exact selected path enters validation, no task execution | APPROVED |
| FP-02 | State/process tests plus real child absence: cancel preserves state, one dialog, stale replies ignored; close supported by source/state test | APPROVED (bounded methods) |
| FP-03 | Real native dialog confirmation/cancellation and keyboard/focus/640×480 expanded details observed | APPROVED |
| FP-04 | Rust regression, real artifact verification, independent review/validation and documentation closure | APPROVED |

Current broad feature ACs remain INCONCLUSIVE; previous S01 observations are historical
for modified product inputs. No implicit X11/AT or complete-product acceptance.

## Decision and evidence

Initial analysis observation (implementation now complete): local CLI observed: Zenity 4.2.2, directory-only
selection flag; RPM license LGPL-2.1-or-later. Rust 1.99 / Iced 0.14 manifests inspected.
Sources: local zenity --version/--help-file-selection and rpm -qi zenity, installed
Iced/std sources. No backend effects from navigation or cancellation.

## Adopted integration and trade-offs

The adapter uses Rust std process/thread/channel support and the separately installed
Zenity 4.2.2 GTK helper, with `--file-selection --directory` and no shell evaluation.
Local `--help-file-selection`, `--version` and RPM package metadata establish the
CLI/version/license (LGPL-2.1-or-later). No helper binary is bundled, no new Cargo
dependency/FFI is introduced. GTK selects its display backend; native acceptance
remains bounded to the observed backend. A portal-crate integration would add
uncached dependencies and a different desktop-service lifecycle; a custom Iced
file browser would add directory-listing/navigation scope. The chosen optional
helper has an explicit installation/PATH prerequisite and manual-entry fallback.

Worker owns a single direct child, cancels/reaps it before response, concurrently
drains stdout with a 64 KiB retained bound and rejects overflow. Response parsing
removes exactly one protocol LF; spaces/newlines in names survive. Non-UTF8 is an
explicit unsupported text-input case, never lossy conversion. Request identity and
context generation plus cancellation state guard completion. This is supervision
of the trusted installed helper, not a generic untrusted-process-tree guarantee.

## Documentation disposition

Updated project scope, feature spec/plan/tasks/convergence, surface contract and
application README (usage, optional Zenity prerequisite and fallback). Reviewed
DESIGN, constitution, architecture and visual-workbench ADR: existing contracts
apply, so no policy or architecture change is required. Prior S01 evidence retained
in historical_evidence and before-docs rather than refreshed against new inputs.

## Counterevidence: dialog-specific CLI support

The first native-wide run could not observe a live helper. Root reproduced Zenity
directly in the isolated session: exit 255 and stderr `--ok-label is not supported
for this dialog`. General help visibility does not establish support for each dialog.
The adapter command is corrected to remove unsupported OK/cancel-label overrides;
the desktop helper owns its native labels. Probe stderr and first-run result are
preserved under native-zenity-probe/ and native-wide/. Native confirmation remains
unverified until replay against corrected bytes.

## Focused Rust observation

A final-source `cargo test --offline -p ox-ui` from application with the repository
Cargo cache returned exit 0: 17 unit tests, four local-task integrations and one
shell contract, zero failed/ignored. The coordinator retained the raw log and source
identities in rust-observation.json. This final observation follows the CLI correction;
previous implementer summaries remain identified as summaries. Checks cover exact
path decoding, helper absence/nonzero exit, state cancellation/duplicate/stale/close
responses, confirmation→validation, and existing artifact/freshness/cancellation
contracts. A simulated child cancellation test does not alone prove a real GTK
window or focus behavior. Native replay supplies that separate oracle.

The corrected native-wide-fixed observation started a real Zenity child but did not
show a mapped dialog; Escape did not terminate it within the harness wait. This
remains an unresolved observation while isolated desktop/portal readiness is diagnosed.
No native acceptance follows from process startup alone.

## Historical provisional independent assessment

Independent ec_revisor found no open source finding in the corrected adapter/Desktop
bytes. Independent ec_validador_alta confirmed FP-01 by source/tests and the raw
22-test pass, while FP-02 remains INCONCLUSIVE pending real child disappearance;
FP-03 UNVERIFIED and FP-04 INCONCLUSIVE pending native journey/documentary closure.
Both contexts completed their provisional review and remain available for follow-up.
This is not task completion.

## Historical resume boundary — superseded by successful replay

The root owns the remaining native harness/replay. Probe5 independently inspected
by the coordinator shows a real GTK chooser after a 40-second startup wait with
GDK_DEBUG=no-portals, GTK_A11Y=none, GSETTINGS_BACKEND=memory and GTK_USE_PORTAL=0
in the isolated test environment. The probe terminated the helper (exit -15); this
is not successful user cancellation or a completed Ox journey. Source code did not
adopt those environment overrides. Complete the real confirm/cancel/focus/PID/artifact
observations, then request independent reviewer/validator follow-up and bind final
report/docs/harness hashes in evidence.json. T015/T016 remain open until then.

## Native harness follow-up

Subsequent runs mapped the actual GTK chooser with test-only environment overrides
and a startup wait. They did not change product sources. A Unicode injection case
dropped an IM dead-key character; a later location-entry case accepted a suggested
`sentinel` file, which the directory-only chooser correctly rejected. These harness
inputs are not successful directory selection and do not establish a path-corruption
defect in the Rust adapter. Raw captures/results remain preserved. Parallel graphical
runs also produced ambiguous focus evidence; acceptance requires a sequential replay.
The initial post-cancel capture names did not match the new tab order: from input2,
one Tab selects chooser273, not validate3. The corrected harness must use two Tabs
for validate3 and one Shift+Tab for chooser273. Captions alone are not the oracle.

## Successful native wide replay

`native-wide-empty` completed the actual Ox/Zenity journey in an isolated Mutter
Wayland session, logical 1440×900/scale1: cancel an empty selection, confirm an
existing directory named `pasta com espaços`, cancel again while a valid session
exists, execute the controlled task and verify its actual artifact. Application exit
was 0 and no chooser child remained. Three helper PIDs are recorded; each helper
was observed absent before continuing. The final binary hash is
`fd12fc33c2d7aa5a14f7046feda154654b9c2f532f68efb3aa51a5c6c7f1ffc8`.

Confirmation opened Tasks with the exact selected directory and produced no attempt
before execution. A sentinel was created after selection but before task execution;
it remained unchanged. Result bytes contain the matching request identity and
`result=42`, and the screenshot shows the verification result. The command overlay
responded to keyboard input after the chooser closed, without a manual focus-gain
operation. Root/coordinator inspected the captures; the later independent final review below supersedes the pending follow-up.
The exact executed harness is preserved at native-wide-empty/harness.py.

Test environment overrides (only the harness): GDK_DEBUG=no-portals, GTK_A11Y=none,
GSETTINGS_BACKEND=memory, GTK_USE_PORTAL=0, plus a 30-second startup readiness wait.
These make the installed GTK chooser observable in this private desktop; they do
not establish normal portal routing, normal startup latency, X11, assistive support
or behavior on every desktop. Native helper labels follow the desktop locale.

## Successful native narrow replay

`native-narrow-verified` completed sequentially at logical 640×480/scale1 with details
expanded, actual GTK chooser mapped, Escape cancellation and child disappearance.
After automatic return to input2, two Tabs focus validation button3 visibly above
the footer; Shift+Tab focuses chooser273, also visible. The Ox command overlay
responded to Ctrl+K, and closing through the application returned exit 0. The
binary and source hashes equal the successful wide observation. Root/coordinator
inspected raw captures, including native helper controls within the small window.

Coverage limits: real cancellation and confirmation observe direct-child absence
while Ox is alive; the post-app-exit empty children list alone would not prove it.
Closing with an active chooser, stale replies, duplicate rejection and helper errors
are supported by source/state/process tests, not separate complete native journeys.
No X11, fractional-DPI, default portal, assistive-technology or performance acceptance
is claimed. Helper locale/theme remains desktop-owned. Earlier native directories
are diagnostic history and must not be used to replace the two successful corpora.

## Final independent review

The original independent ec_revisor context reexamined corrected sources and the
successful wide/narrow captures, matched source hashes and actual artifact bytes,
and found no open finding within the observed scope. ec_validador_alta independently
confirmed FP-01–03 from the bounded source/test/native methods and checked current
source/binary identities. FP-04 was subsequently approved after final documentary/evidence review.

## Closure

Independent ec_validador_alta approved FP-01–04 within the explicitly bounded methods.
It compared current source and binary identities, raw Rust output, actual GTK captures
and artifact bytes, and reviewed the affected documentation. Independent ec_revisor
found no remaining source/native finding. T013–T016 are complete for the requested
folder picker. Earlier pending statements in chronological sections are historical.

The selected feature passes `--require-fresh --check-convergence`. Adding
`--require-approved` returns exit 1 only for the six preexisting broad ACs marked
INCONCLUSIVE; this is recorded and does not approve the whole visual workbench.
Focused tracked-file `git diff --check` returned 0; untracked adapter/view files are
covered by compilation and actual review. No complete scanner run or publication
was performed. Operational coverage and environment limitations above still apply.
