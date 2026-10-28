# Verdicts and authorization

A verdict answers whether evidence supports a criterion for a particular input state. It does not authorize execution, publication or access. Keep at least these distinctions: observed support; observed contradiction; no verification; observations insufficient/conflicting; explicitly out of scope with reason.

Example: a test executable is absent. The execution record says unavailable and the criterion is unverified. Exit code zero from a wrapper that skipped tests cannot override this. If a real test failed because the claimed behavior is violated, report rejected; if the environment prevented reaching the assertion, report the environment gap without claiming behavior passed.

Aggregate only the mandatory criteria for the declared scope. One approved build criterion cannot approve recovery, accessibility or sandboxing. An agent's done message is an input to investigation, not a verdict. A deployment gate must separately inspect current authorization even if every acceptance criterion passed.
