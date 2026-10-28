---
name: application-security
description: Implement or assess application security boundaries and controls, investigate vulnerabilities, or model concrete threats. Use for security decisions involving identity, permissions, untrusted data, secrets, dependencies, or configuration; their mere presence in ordinary code does not require a specialized review.
---

# Application Security

Turn relevant threats into proportionate controls and evidence. Basic secure coding remains required even when this skill is not selected.

## Scope and evidence

Start from the existing requirements, contracts, code, deployment configuration, dependency versions and acceptance criteria. Identify the affected assets, actors, entry points, trust boundaries, data destinations and business impact. Treat missing facts as uncertainties; do not invent security requirements or exposure.

Use this skill when implementing or reviewing a security boundary, changing a sensitive workflow, investigating a possible weakness, or assessing threats. An isolated spelling or layout change normally needs no specialized assessment. Preserve safe existing behavior in any task.

This skill owns threat/control reasoning and security verification. Use domain-modeling only when business invariants are unclear; api-testing for broader protocol/compatibility verification; reliability-engineering for overload and recovery mechanisms; software-architecture for material structural alternatives. These are conditional handoffs, not mandatory imports.

## Workflow

1. **Bound the task.** State affected flows and the expected policy. Distinguish authentication, authorization and data validation. For an investigation, separate an observed defect from a plausible hypothesis. Confirm authorization and scope before intrusive testing, external scanning, or destructive failure injection.
2. **Trace the boundary.** Follow untrusted inputs to interpreters, privileged operations, persistence, outbound requests and output. Include alternate routes, background jobs, admin paths, tenant boundaries and downstream services where applicable. A diagram is useful only when it clarifies a real ambiguity.
3. **Model plausible abuse.** Describe actor capability, precondition, action, asset and impact. Consider bypass, replay, concurrent requests, missing/expired credentials, excessive work and sensitive-data exposure. Prioritize by consequence and exposure, with explicit uncertainty; a CWE ID or scanner severity alone is insufficient.
4. **Select controls.** Reuse maintained project mechanisms. For each important recommendation record action, applicable context, exact source/control ID, rationale, exceptions, cost and verification. Consult only relevant sections of [control decisions](references/controls.md). Verify concrete runtime and framework behavior in current official documentation before using configuration or API examples.
5. **Implement proportionately.** Keep problem specification, technical choice, code changes and validation evidence separate. Preserve contracts or identify deliberate restrictions and migration impact. Do not introduce an identity platform, policy engine or service boundary without a demonstrated need.
6. **Verify both permission and denial.** Test legitimate behavior plus the identified abuse paths with controlled data. Confirm the absence of prohibited reads, writes and side effects, not just an error status. Inspect resulting logs and error output for secret leakage. Select code review, automated checks and integration tests according to the threat; each has coverage limits.
7. **Close the evidence loop.** Report findings with location, preconditions, impact, supporting evidence, remediation and a repeatable check. Separate fixed/verified, unverified, accepted risk and out-of-scope surfaces. Risk acceptance belongs to an authorized owner; never silently accept it for the user.

For delegated OAuth authority, outbound URL fetching or deployment artifact trust,
read [delegation and artifacts](references/delegation-and-artifacts.md). It supplies
boundary-specific negative checks beyond the general control review.

For attenuated credential reissuance, proof of possession or replay state that
must survive restart/offline use, additionally read
[bound credentials and replay](references/bound-credentials-and-replay.md).
Apply the actual destination protocol; this does not select an identity stack.

## Essential constraints

- Enforce security decisions at a trusted boundary. Hidden buttons, opaque IDs, CORS and client validation are not substitutes for authorization.
- Use safe interpreter APIs and bounded inputs. One generic sanitization step cannot protect every output context.
- Protect secrets through their lifecycle; do not disclose them in commands, artifacts, logs or diagnostics.
- Fail securely for the affected operation. A catch-all handler is not permission to continue with invalid state or to grant access when a dependency fails.
- Choose maintained cryptography and identity implementations; do not improvise algorithms or infer safety from a language, container, cloud provider or familiar pattern.
- Do not claim complete security, ASVS compliance or scanner coverage without the corresponding scoped evidence.

## Completion and reporting

Provide the implemented change or actionable finding first, then policy/threat rationale, tests actually run, versions relevant to the result and remaining limitations. Include an illustrative example only if it clarifies the decision; label unexecuted pseudocode. For a small change, a short paragraph and focused test evidence suffice.

Research provenance is available in source coverage (historical library source: `system/research/operations-official-sources.md`; not required at runtime) and local reading ledger (historical library source: `system/research/operations-reading-progress.md`; not required at runtime). These support maintenance and audits; do not load them during routine tasks.

## Additional investigation references

Consult only when relevant: [access-control-matrix](references/imported/api-testing/access-control-matrix.md); [evaluation-and-trust](references/imported/prompt/evaluation-and-trust.md); [resource-lifecycle](references/imported/reliability-engineering/resource-lifecycle.md).

Other named skills are optional specialist suggestions. Use them only when available and needed for a specific unresolved question; their absence does not prevent using this skill. Report any expertise or verification gap without claiming a handoff occurred.

## Adjacent responsibilities

Software-delivery may own build/promotion mechanics; keep signer/builder authority and threat verification here. Artifact identity and reproducibility are distinct claims.
These are optional available capabilities, not dependencies of this folder.
