# Session and execution state

Use separate state machines for a conversational session and a concrete execution attempt. A session may survive several failed attempts; a completed process does not imply an accepted task. A useful attempt model is starting → running → cancelling → exited/failed, with an independent evidence verdict.

Each event needs session, attempt/generation, source, sequence or observation time, payload schema and raw locator. Reject a running event from an older generation after restart. Preserve an unexpected event for diagnosis while preventing it from reversing a terminal state. Define which events can legitimately arrive late and where gaps force reconciliation.

Counterexample: attempt A emits done, dies, then a delayed output arrives after attempt B starts. Applying it to B corrupts provenance. Route it to A, retain it, and leave task acceptance unchanged until its criterion-specific oracle runs. Runtime state should not be reconstructed from rendered chat text.
