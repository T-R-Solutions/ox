---
name: api-testing
description: Design, implement, or diagnose tests of API contracts, authorization, consumer/provider compatibility, and boundary effects. Use when those boundary guarantees need verification; ordinary calculations behind an API and unrelated API implementation do not alone require this skill.
---

# API Testing

Validate the behavior promised to API consumers with reproducible evidence. Start from existing requirements and contracts; distinguish intended behavior, observed behavior, and an unresolved expectation. This skill covers boundary validation, not a mandatory HTTP architecture or testing framework.

## Establish the boundary

1. Read applicable repository instructions and discover existing test commands, clients, schema versions, fixtures, deployment modes, and consumer versions. Do not assume a server, dependency, or credential exists.
2. Identify protocol, operation, caller identity, resource ownership, request/response or event schemas, side effects, state transitions, and downstream dependencies. Trace one relevant flow through code or authorized local observation. Record assumptions when evidence is missing.
3. Rank concrete failures by impact and plausible exposure: malformed data, unauthorized access, duplicate work, stale state, incompatible consumers, dependency failure, or missing completion. Select the smallest scope that exercises the risk.

A calculation merely reached through an API usually needs focused function tests plus a few boundary checks. A serialization, authorization, transport, or consumer compatibility defect needs API evidence. Use `software-testing` only when broader case design or suite quality needs additional work; do not automatically load it.

## Design and execute checks

1. Specify input, caller, precondition, action, expected response, expected effects, and cleanup for each selected case. Include normal, invalid, boundary, absent/null/empty, and state-dependent cases where the contract distinguishes them.
2. Separate contract checks, real integration checks, and end-to-end journeys. State which dependencies are real, simulated, or unavailable. A schema match does not prove the business result; a mock does not prove provider behavior.
3. Check authentication and authorization independently: absent/invalid/expired credentials as applicable; wrong role, another owner's resource, and cross-tenant access. Assert both rejection and absence of unauthorized effects or disclosure. Baseline security is required without loading a specialist skill.
4. Validate successful and failed responses against the targeted protocol and application contract. Check payload meaning, headers/metadata, error usefulness, pagination/filter/order behavior, resource limits, and backward compatibility only where applicable. Do not impose HTTP status codes on non-HTTP protocols.
5. Verify observable effects: persisted state, emitted messages, externally visible outcomes, and failure atomicity. For asynchronous operations, distinguish acceptance from completion and use bounded condition-based observation with a defined deadline.
6. Exercise selected dependency faults in an isolated authorized environment. Record partial success, retry behavior, duplicate effects, cancellation, and cleanup. Do not automatically retry a failing assertion into a pass.
7. Keep independent fixtures, bounded startup/request waits, and safe synthetic data. Verify the target before mutation. Never direct fuzzing, load, destructive cleanup, or security attacks at external systems without corresponding authorization.
8. Run discovered commands, confirm tests were actually discovered, and inspect failures. Prove important assertions can reject a controlled wrong outcome when practical. Report skipped or blocked checks separately from passes.

## Essential decisions

- Preserve an existing contract unless a change is intentional; assess consumers and rollout order before updating expected values to make tests green.
- Consumer-driven contracts are useful when consumer requirements and provider verification can be coordinated. Public or uncontrolled providers may need another approach. Validate real client behavior, provider state, and applicable version pairs.
- Use request/fixture helpers when repeated mechanics obscure intent. Keep scenario data and assertions visible. Avoid a new framework or production architecture solely to fit a book's examples.
- Explore unknown behavior with a focused charter and recorded observations; convert stable valuable findings into regression checks. Treat an unfamiliar result as a hypothesis until its oracle is justified.

## Completion evidence

Report the boundary and versions tested, cases and risks covered, commands/results, real versus simulated dependencies, contract changes, residual uncertainty, and blocked checks. For a reproduced failure, include the minimal sanitized request and state needed to reproduce it. A successful focused check needs only its contract, observed result and material limits; do not manufacture a failure report. Do not claim complete compatibility, security, performance, or end-to-end correctness from a passing contract suite.

## Load only relevant detail

- [Contracts and compatibility](references/contracts.md): schema validation, consumer/provider verification, and evolution.
- [Boundary scenarios and oracles](references/boundary-scenarios.md): authorization, failure effects, exploration, and HTTP-specific checks.

Research history is separate: testing research progress (historical library source: `system/research/testing-progress.json`; not required at runtime). Ordinary API tasks do not require loading that ledger.

## Additional investigation references

Consult only when relevant: [access-control-matrix](references/access-control-matrix.md).

Other named skills are optional specialist suggestions. Use them only when available and needed for a specific unresolved question; their absence does not prevent using this skill. Report any expertise or verification gap without claiming a handoff occurred.

## Adjacent responsibilities

Software-evolution may own a broader mixed-version transition; keep consumer/provider boundary verification here. An ordinary API check does not require that workflow.
These are optional available capabilities, not dependencies of this folder.
