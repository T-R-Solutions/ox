# Specification: terminal progress

## Context and authorization

The maintainer's 2026-11-15 request authorizes implementation and focused tests of
the human terminal output of `./scripts/automate.sh run --scope complete`.
Commits, publication, downloads and a real complete pipeline are not authorized.
Controlled temporary fixture runs do not approve scanners or the product.

The actor is an operator following the real selected plan. Preserve selection,
order, argv/environment, qualified Geiger identity, raw stream capture and existing
redaction, aggregate exit precedence, report schemas, gates and log retention.
This feature owns the presentation successor, not historical scanner acceptance.

## Requirements and acceptance

- REQ-01: Number phases from the actual selection plus preparation and finalization; show Portuguese phase name, total progress, phase progress or unavailable, activity and elapsed duration.
- REQ-02: Use equal completed-phase units and observable subunits only. Integer percentages cannot regress. Unknown progress stays unavailable. Publication must succeed before total 100%; cancellation cannot look like normal completion.
- REQ-03: Close phases with permanent state, duration, executed summary, warnings/skips/limits and a diagnostic locator. Recorded inventory/measurement is not approval. Distinguish operational errors, findings and blocked prerequisites.
- REQ-04: Enumerate problems with supported location, causal certainty, code/signal and source; group repetitions with counts. Never print secrets or execute/interpret tool text as instructions. Missing cause/location remains explicit.
- REQ-05: TTY may update one line; redirected output has no control sequences. Honor NO_COLOR. Human stderr is separate from machine plan/JSON; retain original raw streams under their existing access/redaction contracts.
- REQ-06: Preserve process supervision, cancellation cleanup, exit precedence, scanner gates and publication/retention. Test failure transitions without executing real scanners.

- AC-01 → REQ-01: Controlled plans with different selected counts produce their actual N plus preparation/finalization and consistent phase identification.
- AC-02 → REQ-02: Fixtures demonstrate monotonic integer total progress, real member subunits, unavailable opaque progress, and no premature total 100% on publication failure or cancellation.
- AC-03 → REQ-03: Fixtures distinguish passed, finding, operational error, blocked, skip, cancellation and recorded outcomes, with permanent truthful summaries and limits.
- AC-04 → REQ-04: Adversarial and structured fixtures produce numbered source-backed diagnostics, known/unknown causes and locations, counts, and no secret/control-text disclosure.
- AC-05 → REQ-05: TTY, redirected and NO_COLOR fixtures preserve readable output; plan JSON and raw stdout/stderr bytes remain unchanged.
- AC-06 → REQ-06: Focused regression fixtures retain codes, signal forwarding/reaping, fail-closed reports and publication failure behavior; independent review and validation support the bounded change.

## Limits

Only measured events can yield internal progress. No estimate by time, bytes, lines
or history is permitted. Tool reports are untrusted data. Raw diagnostics are not
replaced by summaries. Raw publication failure diagnostics may need an emergency
temporary log because the existing publisher removes the run even on failure.
Platform/scanner operation and full product acceptance remain outside this feature.
