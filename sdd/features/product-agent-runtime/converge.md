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

# Convergence: product-agent-runtime

All declared criteria APPROVED for the bounded local slice.

# Agent Runtime acceptance review

AC-01: real_success_and_failure_are_observed launches compiled local-agent; exits 0/17 independently yield Success/Failed, event sequences [1,2], and post-terminal cancel leaves outcome unchanged.
AC-02/04: cancellation_and_deadline_reap_before_recovery observes Cancelling before terminal Cancelled, sequences [1,2,3], a deadline produces TimedOut and a new attempt succeeds while old state remains intact. try_wait observes/reaps the child before dropping its handle.
AC-03: late_duplicate_and_out_of_order_events_leave_state_intact injects wrong generation, gaps, duplicate starts and late success after failure; reducer refuses each without altering state/history. Reducer is not a sender authentication mechanism.
AC-05: controlled_adapter_preserves_workspace compares a binary sentinel and directory entry count after process completion. No sandbox claim follows.
All four runtime tests pass; workspace check/fmt/Clippy pass. Output availability explicitly false; null streams prevent unread-output pipe deadlocks but do not preserve output.


Limitations:
- Controlled local no-output adapter only; no real agent, provider, credentials, network or code transmission.
- Caller must poll to enforce runtime deadline; process-tree containment and OS CPU/memory limits absent.
- Drop kills/reaps direct child only; no durable state, crash restart, pause, resume, usage or output capture.
- Workspace preservation demonstrated with controlled fixture; arbitrary executable retains OS permissions.
