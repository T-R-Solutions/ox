---
name: plugin-protocol-engineering
description: Design and verify versioned host-plugin protocols, capability negotiation and lifecycle failure boundaries. Use for plugin hosts or compatibility changes; skip clients of an unchanged SDK.
---

# plugin-protocol-engineering

## Responsibility and selection

Design and verify versioned protocols for plugins isolated from the host, including capability negotiation, permissions, lifecycle, failures, ABI and compatibility.

Select: New protocol/plugin host, capability manifest, IPC, vN/vN+1 compatibility, safe installation/uninstallation.

Do not select: Do not select for a lint plugin that only uses an established SDK; use Rust and API Testing in that case. Do not turn this skill into an automatic recommendation for Wasm, gRPC or Dylib.

## Inputs and gaps

extensibility policies, threat model, operations/capabilities, version matrix, OS, available resources.

Inspect actual contracts and resources before execution. A missing version requires consulting the corresponding documentation; a missing permission prevents the dependent effect. Record the gap, its impact and how to resolve it while continuing independent work. Examples in this package are evaluation contracts, not APIs or policies imposed on all consumers.

## Operating procedure

1. Inventory each operation as a tuple: caller identity, requested capability, granted scope, input limit, effect, idempotency rule and revocation point. Separate host-mediated effects from direct process access; an allowlist in a manifest cannot constrain the latter.

2. Write a negotiation transcript before implementation. Define transport framing, maximum frame size, protocol version ranges, unknown fields, request correlation and error ownership. Compute effective capabilities as the supported/requested/granted intersection; never grant a capability merely because both binaries implement it.

3. Compare out-of-process RPC, in-process ABI and a restricted runtime against the actual trust model. Record which failure each option contains, platform mechanisms required and what remains trusted. Do not default to Wasm, gRPC or dynamic libraries.

4. Define lifecycle transitions from discovery through negotiation, ready, draining and stopped/failed. Admission closes before shutdown; in-flight requests either finish or expire under a documented policy. Reconnect creates a new instance generation, so old replies cannot satisfy new requests.

5. Build a compatibility matrix by host version, plugin version and capability subset. Exercise successful negotiation, denied capability, malformed frame, oversized payload, crash mid-effect and timeout. Inspect persistent state and protected-file effects, not just the error response.

6. Deliver a protocol contract, denied-effect matrix, lifecycle transcript and platform-specific residual risks. Treat a successful mock as protocol evidence only; isolate and test a real untrusted plugin before claiming sandbox enforcement.

## Deliverables and acceptance

message contract, host states, permission model, resource limits, compatibility matrix, failure and migration tests.

Bind each conclusion to observed inputs, method, result and limitations. Run the normal, boundary and failure cases from the [evaluations](references/evaluation-cases.md) in the authorized environment; distinguish review, simulation and integration results. Written cases remain unexecuted until run. Skill text neither proves effectiveness nor grants authority.

## Boundaries and handoff

`application-security` — Does the chosen isolation actually prevent unauthorized effects from a compromised plugin?

Hand off only the distinct unresolved technical question, including scope, criterion IDs, facts, gaps and required evidence. Confirm availability before consultation. A mention does not install, delegate, execute or recursively load other skills. The consumer's contract owns behavior; the skill provides the method.

## Specialized references

- [protocol-negotiation](references/protocol-negotiation.md): consult for Negotiation and message identity.
- [permissions-and-isolation](references/permissions-and-isolation.md): consult for Mediated permissions and containment.
- [versioning-and-faults](references/versioning-and-faults.md): consult for Compatibility and failure windows.

Official sources accessed on 2026-10-26 are cited alongside claims. A consulted version is not a version adopted by the consumer. Operational summaries and example schemas are methodological decisions of this skill, without a promise of implementation or future compatibility.

## Adjacent responsibilities

The specialized capability above does not replace the general methods below. Consult them only when the corresponding question remains unresolved; no handoff is mandatory.

| Capability | Adjacent technical authority |
|---|---|
| `api-testing` | verification of protocols, effects, permissions and consumer compatibility |
| `application-security` | trust boundaries, secrets, authorization and threats |
| `reliability-engineering` | failures, cancellation, limits, degradation, recovery |
| `software-architecture` | boundaries, integration, quality attributes, ADRs |
| `software-evolution` | compatibility, migrations, coexistence and older versions |
| `distributed-systems` | guarantees across failure domains and versions, messaging/consistency |
| `rust` | ownership, crates, concurrency, compatibility, Rust validation |
| `software-delivery` | supply chain, builds, signatures, release and rollback |
| `software-design` | interfaces, cohesion, coupling, local refactoring |
