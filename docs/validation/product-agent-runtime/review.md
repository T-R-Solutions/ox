# Agent Runtime acceptance review

AC-01: real_success_and_failure_are_observed launches compiled local-agent; exits 0/17 independently yield Success/Failed, event sequences [1,2], and post-terminal cancel leaves outcome unchanged.
AC-02/04: cancellation_and_deadline_reap_before_recovery observes Cancelling before terminal Cancelled, sequences [1,2,3], a deadline produces TimedOut and a new attempt succeeds while old state remains intact. try_wait observes/reaps the child before dropping its handle.
AC-03: late_duplicate_and_out_of_order_events_leave_state_intact injects wrong generation, gaps, duplicate starts and late success after failure; reducer refuses each without altering state/history. Reducer is not a sender authentication mechanism.
AC-05: controlled_adapter_preserves_workspace compares a binary sentinel and directory entry count after process completion. No sandbox claim follows.
All four runtime tests pass; workspace check/fmt/Clippy pass. Output availability explicitly false; null streams prevent unread-output pipe deadlocks but do not preserve output.

