# Raw, normalized and compact representations

Keep three separately identified artifacts. Raw is the captured byte stream with completion and retention metadata; normalized is a versioned interpretation; compact is a lossy view. Record transform version, raw hash, ranges consumed/omitted, parser warnings and truncation reason.

Exit code and signal come from process observation, not from phrases like all tests passed. If output says success but the process exits nonzero, preserve the contradiction. If storage fills before capture completes, expose incomplete_raw and the captured extent; a locator cannot promise bytes never retained.

For a privacy-sensitive log, preserve authorized evidence with restricted access and a retention policy. Redacted display is distinct from raw evidence. Escaping terminal control characters prevents display effects without treating log text as commands. A summary should never erase the only occurrence of a failure location without reporting the omission and retrieval route.
