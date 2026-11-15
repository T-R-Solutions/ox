# Current acceptance projection

Current automated states from [evidence.json](evidence.json). This projection
is not a new observation or product acceptance.

<!-- sdd:current-status -->
| Criterion | Status |
| --- | --- |
| AC-01 | INCONCLUSIVE |
| AC-02 | INCONCLUSIVE |
| AC-03 | INCONCLUSIVE |
| AC-04 | INCONCLUSIVE |
| AC-05 | INCONCLUSIVE |
<!-- /sdd:current-status -->

## Historical convergence — before 2026-11-14 correction

The following conclusions apply only to their original observed inputs. Current
states are above; prior bytes remain in the bounded correction preimages.

# Convergence: product-verification-engine

All declared criteria APPROVED for the bounded local slice.

# Verification Engine acceptance review

AC-01/02: approval_requires_observation_not_completion_claims starts without evidence, adds an agent/task completion note and remains NotVerified; a real local-oracle exit 0 with stable content creates approval tied to run id, command and immutable input bytes.
AC-03/04: failure_history_survives_repair_and_content_invalidation_is_selective injects candidate defect, observes exit17/rejection, repairs bytes and requires a new run; old failing bytes/result remain accessible. Unrelated criterion acceptance survives. Changed oracle or description invalidates the result.
AC-03: contradictory_current_pass_does_not_erase_observed_failure deliberately varies undeclared fixture state; observed failure then pass share declared inputs, and rejection remains. This also illustrates why caller dependency completeness matters.
AC-05: incomplete_and_not_applicable_are_not_approval produces timeout/Inconclusive and requires a nonempty NotApplicable reason. Existing Verdict retains all five SDD meanings, NotVerified corresponds to UNVERIFIED.
Four tests pass, including real fixture processes; workspace check/fmt/Clippy pass. Initial fixture compile error was corrected and retained in test-initial-compile-failure.log.



Limitations:
- In-memory local exit-code oracle only; no persistence, artifact authentication, arbitrary oracle suitability proof or real-agent integration.
- Exact byte snapshots are bounded, not cryptographic hashes; dependency completeness is caller responsibility. Environment/dynamic libraries and transient concurrent changes between snapshots are not fully bound.
- Direct-child deadlines only; no process-tree or OS sandbox. Output is unavailable for this exit-only oracle.
- Caller explicitly supplies executable and inputs; accepting evidence grants no execution, publication or deployment permissions.

## F0 operational successor — 2026-11-03

Current evidence is E-F0-EXECUTION-CURRENT in evidence.json and the
operational report at `docs/validation/f0-execution-20261102/report.md`.
Historical results above retain their original scope and inputs. F0 remains OPEN;
GUI/native/performance limitations are explicit in the current matrix.

Final review: E-F0-FINAL-REVIEW. F0 stays OPEN; current per-criterion states are
in evidence.json and docs/validation/f0-execution-20261102/matrix.json. Product
operational records are excluded from the governance-only export.


## Robustness successor — 2026-11-05

See docs/validation/robustness-20261105/report.md and current evidence.json.
The archived predecessor retains historical acceptance on its exact inputs.
New Engine input handling and child cleanup have focused process/API evidence;
actual GUI response/close/rendered-state and F0 performance on this build remain
UNVERIFIED. T903 records the exact missing observation. No storage, real-agent or
plugin-desktop implementation is added; historical F0 closure is not erased.

Current AC-01..05 APPROVED for the bounded Engine library, using final focused
tests and source review; cleanup fault errors are simulated, cancellation/timeout
and reap are observed with real processes. This does not accept GUI or F0.


## T903 current-input successor — 2026-11-05

See docs/validation/t903-20261105/report.md. Historical acceptance and failures are preserved. Current real X11/native Wayland journeys, FIFO, stale history, cooperative cancel/close and worker/direct-child exit are supported. A new32-observation draw violation was reproduced and repaired by newline-preserving Iced column composition; all12 corrected cells pass draw/response. Extra full-count GUI RSS reaches133.69MiB: its applicability against64MiB versus the separately adopted fixed large-history corpus is INCONCLUSIVE. T903 stays open pending that oracle; current F0 is not closed. No threshold, product scope or persistence permission changed.


## T903 memory closure successor

Current acceptance and exact observed inputs: docs/validation/t903-memory-20261105/report.md and matrix.json. This supersedes the earlier RSS applicability gap:64MiB applies to full-count GUI,256MiB remains fixed renderer-free. Current Engine/callers preserve API/content equality, immutable history, five states, selective invalidation and logical pre-effect admission. Current independent GUI/function/resource/coverage observations and governance/binding checks support APPROVED in the adopted boundary. Historical F0 remains attached to its original bytes; no automatic transfer or persistence claim.
