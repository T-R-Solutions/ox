# Boundary Scenarios and Oracles

Use only rows relevant to the operation and its risk. Source locators refer to physical PDF pages, 1-based. Examples are conceptual and not executable programs.

## Match the test to the failure

| Risk | Action and evidence to collect | Important limit |
| --- | --- | --- |
| Incorrect input handling | Exercise normal, boundary, malformed, missing, null, empty, oversized, and wrong-type values that the contract distinguishes; check errors and unchanged protected state. | Do not assume every absent/null distinction matters or enumerate every Cartesian combination. |
| Authorization bypass | Compare permitted caller, wrong role, another owner, and another tenant; check reads, writes, and indirect effects. | A valid credential proves identity, not permission. |
| Partial failure | Interrupt a dependency before and after the local effect; inspect persisted state, emitted work, and retry outcome. | A 5xx response does not prove nothing committed. |
| Asynchronous completion | Observe acceptance and the contracted terminal outcome separately, bounded by a deadline. | A receipt or HTTP 202 alone is not completion. |
| Duplicate/concurrent work | Reissue the relevant operation and interleave competing requests against a stated invariant. | Idempotency scope, keys, expiry, and atomicity need explicit contracts. |
| Consumer drift | Compare real consumer expectations with provider verification for supported versions. | Contract agreement does not exercise live routing or prove every consumer works. |
| Flaky setup | Confirm readiness, isolate data and ports, control time/randomness where useful, and classify failures. | Removing a real dependency can conceal a genuine integration defect. |

**Evidence:** Winteringham chapters 3–6 PDF 78–231, chapter 8 PDF 272–290, chapter 9 PDF 291–315; Aniche chapters 2,6,9 PDF 58–90,169–199,243–285.

**Rationale:** Boundary checks are valuable when they expose serialization, identity, state, or dependency behavior that a pure function test cannot observe.

**Exceptions and trade-offs:** Real dependencies improve fidelity but cost runtime, control, and diagnostic precision. Simulations are useful for rare faults; verify their assumptions separately. Keep complex logic cases close to the logic when the API boundary adds no relevant evidence.

**Validation:** Each selected case has a clear oracle and observable consequence. Confirm fixture isolation and cleanup, and exercise a plausible faulty outcome to show assertion sensitivity.

## Apply HTTP semantics only to HTTP

For HTTP, verify methods, representation metadata, and response semantics against the actual contract and [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html), especially sections 9.2,13.1.1,15.3.2–15.3.3. A method's idempotency concerns intended effects, not identical response bytes. A 202 response is acceptance before completion. Conditional updates need tests for stale validators where supported.

**Action/context:** For a retryable update, lose a response after the effect, repeat the request, and verify the promised final state. For asynchronous deletion, wait for the documented completion signal before asserting absence.

**Rationale:** Transport feedback and business outcomes differ. **Exceptions/cost:** These checks require controlled failure injection and state observation; skip unsupported semantics rather than retrofit the API. **Validation:** Assert the stated guarantee and its bounds, not a guessed rule about every HTTP service.

## Explore uncertainty with a charter

**Action/context:** When behavior or risks are poorly understood, define a small target, question, time budget, and observation method. Record version/environment, actions, outcomes, oracle, and new questions. Debrief findings and extract worthwhile regressions.

**Evidence:** Winteringham chapter 5 PDF 146–191.

**Rationale:** Adaptive exploration can discover assumptions absent from existing automated assertions. A heuristic suggests an investigation; it is not evidence of a defect.

**Exceptions and trade-offs:** An established deterministic regression may only need a focused automated check. Exploration requires attention and records, and repeated sessions may differ. Findings based on familiarity remain hypotheses until reconciled with stakeholder requirements and protocol behavior.

**Validation:** Provide reproducible evidence for confirmed defects and label open questions, blocked areas, and unexecuted charters. Do not replace a required acceptance check with an unexplained exploration claim.

## Worked scenario: ambiguous booking failure

Before: send a booking, receive a 500 response, assert failure, retry automatically.

After: define whether booking persistence and notification must succeed atomically. In an isolated fixture, make notification fail after persistence. Observe booking identity/state, response, and permitted retry behavior. If the contract permits a committed booking with failed notification, assert the documented recovery/status outcome. If atomic failure is promised, assert no booking remains. A retry must not create an unintended second booking.

This is a synthesis from Winteringham chapter 5 PDF 164–177, not copied runnable code. Changing the atomicity promise is a contract change, not a test-only fix.

## Verify adapters and committed effects separately

**Action/context:** When an API persists state or emits events, include the actual serialization and persistence boundary relevant to the claim. Observe committed state through a fresh context; verify emitted message content independently of the production serializer. Exercise the promised behavior when commit or publication fails.

**Evidence/rationale:** Khorikov, *Unit Testing* (2020), chapters 9-10 PDF 238-278, distinguishes a mock of a domain helper from a recording double at the outbound boundary and shows ORM-context false confidence. Mohan, *Full Stack Testing* (2022), chapter 5 PDF 141-174, adds caches, batch restarts and message processing. A successful controller return or recorded call leaves database, transport and consumer effects unproven.

**Exceptions/trade-offs:** Do not require a live external provider for every local case. Use controlled provider states or simulation for fault exploration, retain targeted real-adapter evidence and disclose missing guarantees. A focused repository test may expose a query defect more cheaply than a full HTTP journey. Owned database schemas still need compatibility checks during staggered deployments.

**Validation:** Remove persistence or corrupt a message in an isolated copy and confirm detection. Check duplicate processing and retry scope against the actual contract, including TTL or idempotency-key behavior when specified. Never infer exactly-once delivery from a mock receiving one call. The source CRM publishes before committing; its example is not evidence of atomic external publication.
