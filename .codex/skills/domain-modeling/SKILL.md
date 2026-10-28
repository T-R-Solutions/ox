---
name: domain-modeling
description: Model business rules, domain language, valid states, invariants, and transactional boundaries when implementing or changing behavior whose meaning or consistency is uncertain. Use for domain modeling and proportional DDD; do not activate for routine persistence mapping or purely mechanical code edits.
---

# Domain Modeling

Turn business requirements into a model whose behavior and consistency can be checked. Match modeling effort to uncertainty and consequence; simple rules can remain simple procedures.

## Scope and evidence

Collect the relevant requirements, acceptance examples, existing behavior, domain terminology, data ownership, and concurrent writers. Separate confirmed rules from assumptions. If domain experts are unavailable, use existing contracts and examples and label unresolved semantics; do not invent business policy.

This skill owns the meaning of rules and boundaries. Code organization belongs to software design; deployment and quality attributes belong to architecture; guarantees across independent failure domains belong to distributed systems. Use another skill only when a concrete unresolved question crosses that boundary. DDD does not require microservices, event sourcing, CQRS, or object-oriented programming.

## Workflow

1. **Describe the problem.** Identify actors, commands, decisions, outcomes, and business value. Distinguish business importance from implementation complexity. For a simple change, a short behavioral example is enough.
2. **Make language explicit.** Define ambiguous terms within their context. Capture behavior, exceptions, and invariants alongside nouns. Preserve the established domain language; do not impose an organization-wide canonical entity.
3. **Model valid transitions.** Record the starting state, actor/authority, inputs, rule, resulting state, and rejected transitions. Identify units, identity, time basis, precision, and absence semantics where relevant. Read [modeling decisions](references/modeling-decisions.md) for boundary and representation choices.
4. **Locate each invariant.** State which data must be consistent together, who may write it, and how persistence and concurrent execution enforce the rule. A database entity is not automatically an aggregate. Do not weaken a real invariant to satisfy a pattern.
5. **Choose the smallest useful implementation.** Use a procedure or existing persistence model for simple behavior. Introduce value types, controlled commands, or an aggregate boundary when they prevent demonstrated invalid states or duplication. Retain the language's idioms.
6. **Handle interactions deliberately.** Distinguish commands from committed facts, internal events from public contracts, and state ownership from read copies. For complex context integration, temporal models, or modernization, read [integration and evolution](references/integration-and-evolution.md).
7. **Validate behavior and boundaries.** Check examples with the authoritative requirements; exercise normal, boundary, invalid, and competing transitions. Verify transactional failure and retry behavior at the persistence boundary where applicable. Preserve existing behavior during refactoring or explicitly record changed contracts.

## Decisions and constraints

- Use a bounded context to separate meanings or models that genuinely differ; it is not an instruction to deploy another service.
- Keep consistency boundaries no larger than required, but large enough to enforce the actual invariant. Separate transaction requirements from eventual propagation preferences.
- State whether reads used for decisions are authoritative, stale, or unknown. A version check on one row does not establish a multi-record invariant by itself.
- Treat event sourcing as a storage/history decision with replay, evolution, retention, and recovery costs. A history requirement alone does not prove it is the best choice.
- Prefer explicit migration/import events over pretending unknown history was observed. Keep raw facts and derived interpretation distinguishable.
- Preserve basic correctness, security, and accessibility without requiring specialist skill activation.

## Completion and report

Present the implemented or proposed behavior, the important rules and examples, selected boundaries, alternatives rejected and why, and validation actually performed. Include unresolved policy questions and their impact. Show a context diagram or transition table only when it clarifies the decision.

For significant recommendations, state action, context, evidence, rationale, exception, cost, and validation. The linked references provide examples of that form. Do not claim domain validation merely because code compiles or tests reproduce the same assumptions.

Other named skills are optional specialist suggestions. Use them only when available and needed for a specific unresolved question; their absence does not prevent using this skill. Report any expertise or verification gap without claiming a handoff occurred.

## Adjacent responsibilities

Database-engineering can implement a confirmed invariant at the persistence boundary. Keep business meaning here; a routine mapping needs neither a new modeling exercise nor automatic specialist activation.
These are optional available capabilities, not dependencies of this folder.
