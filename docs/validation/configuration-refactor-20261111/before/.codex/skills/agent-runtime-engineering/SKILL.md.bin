---
name: agent-runtime-engineering
description: Engineer CLI agent supervision, session state, event ordering, cancellation and recovery. Use for process adapters and execution lifecycles; skip prompt writing and model-quality evaluation without process effects.
---

# agent-runtime-engineering

## Responsibility and selection

Manage CLI agent lifecycles and communication protocols, resources, sessions, events, cancellation, reconnection and results without confusing model statements with completed effects.

Select: ACP/CLI adapter, process supervisor, session/task state, parallel agents, cancellation and resumption.

Do not select: Do not select for standalone prompts, model comparison or response quality evaluation without effects; use ai-engineering.

## Inputs and gaps

supported protocols, executables/versioning, permission policy, resources, session semantics, events and limits.

Inspect actual contracts and resources before execution. A missing version requires consulting the corresponding documentation; a missing permission prevents the dependent effect. Record the gap, its impact and how to resolve it while continuing independent work. Examples in this package are evaluation contracts, not APIs or policies imposed on all consumers.

## Operating procedure

1. Inspect the actual executable, version, launch contract, transport and supported operations. Build an adapter capability table for cancel, resume, permission requests and usage reporting. Missing capabilities remain unavailable; do not emulate pause or resume by inventing protocol messages.

2. Separate session ID, task ID, execution attempt, process identity and event sequence. Define allowed transitions and guards. An adapter statement such as done is a reported event; process exit, file changes and acceptance evidence are distinct observations.

3. Supervise stdin/stdout/stderr concurrently with bounded queues and an overflow policy that preserves critical events. Decide where backpressure blocks, where raw bytes spill to disk, and how failure to persist them surfaces. Never parse human stderr as authoritative permissions.

4. Design cancellation as a request followed by an observed terminal outcome. Stop new work, cancel supported protocol operations, drain outputs, enforce a deadline, terminate the owned process tree through supported platform mechanisms, and reap processes. Record partial effects before permitting retries.

5. On reconnection, compare generation and last acknowledged event. Deduplicate recorded events, expose sequence gaps and reconcile artifacts before replaying side effects. A new process does not inherit old grants implicitly.

6. Exercise out-of-order events, death with unread streams, cancellation under sustained output and done without evidence. Deliver a transition table, adapter contract and execution trace with remaining cleanup/permission limitations.

## Deliverables and acceptance

state machine, testable adapters, ordered events, process controls, cancellation handling, policy integration.

Bind each conclusion to observed inputs, method, result and limitations. Run the normal, boundary and failure cases from the [evaluations](references/evaluation-cases.md) in the authorized environment; distinguish review, simulation and integration results. Written cases remain unexecuted until run. Skill text neither proves effectiveness nor grants authority.

## Boundaries and handoff

`reliability-engineering` — How can orphaned processes, duplicate effects and event loss be bounded during failures?

Hand off only the distinct unresolved technical question, including scope, criterion IDs, facts, gaps and required evidence. Confirm availability before consultation. A mention does not install, delegate, execute or recursively load other skills. The consumer's contract owns behavior; the skill provides the method.

## Specialized references

- [session-state-machine](references/session-state-machine.md): consult for Session and execution state.
- [process-supervision](references/process-supervision.md): consult for Supervision and resource ownership.
- [acp-and-cli-adapters](references/acp-and-cli-adapters.md): consult for ACP and CLI adapters.

Official sources accessed on 2026-10-26 are cited alongside claims. A consulted version is not a version adopted by the consumer. Operational summaries and example schemas are methodological decisions of this skill, without a promise of implementation or future compatibility.

## Adjacent responsibilities

The specialized capability above does not replace the general methods below. Consult them only when the corresponding question remains unresolved; no handoff is mandatory.

| Capability | Adjacent technical authority |
|---|---|
| `ai-engineering` | models, RAG, agents using tools, diagnostics and outcome evaluation |
| `api-testing` | verification of protocols, effects, permissions and consumer compatibility |
| `application-security` | trust boundaries, secrets, authorization and threats |
| `reliability-engineering` | failures, cancellation, limits, degradation, recovery |
| `distributed-systems` | guarantees across failure domains and versions, messaging/consistency |
| `observability-and-diagnostics` | instrumentation, logs, metrics, traces, causal investigation |
| `rust` | ownership, crates, concurrency, compatibility, Rust validation |
| `software-architecture` | boundaries, integration, quality attributes, ADRs |
