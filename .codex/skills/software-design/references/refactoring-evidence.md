# Refactoring Evidence

Use this checklist for a change whose behavior is not obvious. Scale it to risk; do not create a new process or test framework merely to complete the list.

## Establish the contract before the edit

Inspect requirements, callers, existing tests, and implementation. Record the observable values and effects that matter. Include error types or categories, ordering, mutation, transaction boundaries, cancellation, ownership, and compatibility where relevant. Unknown behavior is an uncertainty to investigate, not permission to redefine it. Search can miss generated or external consumers; record that limit. Hyrum's Law is a warning about real dependencies, not a requirement to retain every accidental behavior forever.

A characterization test records existing behavior; it does not prove that behavior is desired. If it exposes a bug, separate the corrective contract change from the mechanical refactor and obtain the required product decision when the intended behavior is unclear.

## Select independent checks

Use existing meaningful checks first. Add checks for changed risks when necessary: boundary values, negative cases, state transitions, repeated calls, and real collaborator behavior. A test that merely repeats the new implementation is a weak oracle. Compare independently stated requirements or known results.

For nondeterministic behavior, control time, randomness, scheduling, and external state where possible without removing the behavior under investigation. Keep a separate check for actual integration when a fake substitutes an external boundary.

## Inspect semantic changes hidden by syntax

| Change | Possible contract difference | Useful verification |
|---|---|---|
| Return value becomes callback | Timing, reentrancy, exception propagation | Caller outcomes and callback ordering |
| Several reads become one cached read | Freshness, authorization context, memory use | Changes between reads and invalidation |
| Error becomes default value | Missing data versus failed access | Permission, corruption, timeout cases |
| Independent operations are combined | Transaction scope and partial completion | Failure between effects |
| Shared helper replaces duplicate code | Different domain meaning or release policy | Each consumer's accepted behavior |
| Parallel work replaces sequential work | Ordering, contention, cancellation | Observable ordering and failure outcomes |

These are illustrative review prompts, not executed examples or universal test requirements.

## Report evidence at its actual strength

State the exact checks run and their result. Distinguish inspection, compilation, test execution, benchmark measurement, and production observation. If a dependency or runtime is unavailable, explain the affected claim and the remaining validation. Do not describe passing tests as proof of complete correctness.

Source basis: Ousterhout, *A Philosophy of Software Design*, chapters 9–10, 16, 19–20 (physical PDF pages 81–110, 158–164, 176–189); Farley, *Modern Software Engineering*, chapters 7–8 and 14 (physical PDF pages 110–133, 214–233). Also informed by *Software Engineering at Google*, chapter 1 (physical pages 36–39), chapter 9 (193–211), chapter 15 (339–350), and chapters 21–23 (461–478, 481–485, 491–520). The table is engineering synthesis of contract risks, not a verbatim author checklist.
