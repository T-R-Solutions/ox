# Contextual control decisions

Read only the section matching the changed surface. These are engineering decisions grounded in Janca's *Alice & Bob Learn Application Security* (Wiley, copyright 2021), with current official cross-checks. Book locations use physical PDF pages in `docs/system/Learn Application Security.pdf`; main printed page = physical − 28. No book code is a verified implementation here.

ASVS links below refer to release 5.0.0. Selecting a few controls does not establish an ASVS level or certification. Exact requirements and applicability must be reviewed if compliance is requested.

## Threats and proportionality

**Action/context:** For a new privileged flow or material boundary change, write a compact actor → input → boundary → asset model and a few plausible abuse cases. Start with existing requirements and implementation evidence. Record mitigation, removal or an authorized acceptance decision for relevant risks.

**Why/cost:** This finds missing controls that code scanners cannot infer from syntax. It costs analysis time and can become speculative if the system model is inaccurate. For a small local fix, one abuse case and its regression check can suffice; organization-wide workshops are not mandatory.

**Validate:** Confirm the model against actual entry points and ownership; turn selected mitigations into observable acceptance criteria. Revisit after a boundary or trust assumption changes. Book pp 93-110,179-194; [OWASP Threat Modeling, system modeling through review](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html).

## Identity and permissions

**Action/context:** State who may perform which operation on which object and fields, including tenant/state constraints. Enforce that policy using the project's trusted service boundary on every applicable path. Preserve explicitly public operations. A role check alone may leave same-role cross-user access open; adopt attribute or relationship rules when policy needs them, without mandating a new policy engine.

**Why/cost:** Authentication establishes identity; authorization establishes permitted effects. Centralized enforcement can reduce omissions but must fit jobs, caches and service calls. Caching permission decisions creates revocation/staleness costs.

**Validate:** Exercise allowed access, anonymous access, insufficient privilege, another user's object, another tenant, prohibited fields and revoked access. Inspect side effects and returned data. Book pp 57-65,117-132; [ASVS v5.0.0-8.2.1–8.2.3,8.3.1,8.4.1](https://raw.githubusercontent.com/OWASP/ASVS/v5.0.0/5.0/en/0x17-V8-Authorization.md); [OWASP Authorization](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html).

Illustrative, unexecuted policy example: before, `authenticated → load invoice(id) → return all fields`; after, `verified identity → fetch within permitted tenant/object scope → enforce readable fields → return selected fields`. This intentionally restricts unauthorized behavior. A denial response must not reveal invoice contents or mutate it; an allowed user must retain access. Atomic checks or database constraints may be needed if policy-relevant state can change concurrently.

**Authentication/session action:** Use the established identity provider/framework and assess login, recovery, enrollment, logout and alternate paths together. Choose assurance and session lifetime from risk. Verify session renewal, invalidation and replay behavior; a valid signature alone is insufficient. Self-contained tokens need trusted keys, correct issuer/context, audience, type and validity checks. OAuth authorization is not by itself user authentication; OIDC adds identity semantics.

**Exceptions/costs:** Revocation may need state, short lifetimes or coordinated checks; stronger authentication can affect recovery and usability. Never invent fixed token character counts. Check exact framework defaults.

**Validate:** Expired, forged, wrong-audience and wrong-purpose credentials fail; recovery cannot bypass required factors; logout/revocation behavior matches the documented contract. Book pp 57-65,117-125; [ASVS V6](https://raw.githubusercontent.com/OWASP/ASVS/v5.0.0/5.0/en/0x15-V6-Authentication.md), [V7](https://raw.githubusercontent.com/OWASP/ASVS/v5.0.0/5.0/en/0x16-V7-Session-Management.md), [V9](https://raw.githubusercontent.com/OWASP/ASVS/v5.0.0/5.0/en/0x18-V9-Self-contained-Tokens.md), [V10](https://raw.githubusercontent.com/OWASP/ASVS/v5.0.0/5.0/en/0x19-V10-OAuth-and-OIDC.md).

**Password storage action:** If passwords are stored, use a maintained adaptive salted password-hashing implementation and verify current algorithm/parameter guidance. Stolen salted hashes still permit offline guessing. Benchmark legitimate authentication and resource exhaustion; plan versioned hash upgrades and recovery. Higher cost improves guessing resistance but consumes CPU/memory and can amplify denial of service. Federated authentication may remove local password storage; legacy migration may require staged replacement. Book pp 51,77 require correction; [OWASP Password Storage, algorithms and upgrading legacy hashes](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html).

## Inputs, interpreters and business effects

**Action/context:** Validate type, range, size, structure and domain consistency at the authoritative boundary. At each interpreter, use appropriate safe APIs: query parameters, safe template rendering, structured process arguments and restricted parsers. Validate dynamic identifiers against allowed choices. Stored procedures and ORMs can still contain unsafe dynamic queries. Avoid unsafe object reconstruction and uncontrolled dynamic execution from untrusted input.

**Why/exceptions/cost:** Validation establishes acceptable business data; encoding/parameterization protects interpreter structure. Rich text may need a maintained sanitizer, with intentional removal of unsupported markup. Overly broad filters can reject legitimate names or languages. Arbitrary user-supplied URLs need destination and redirect controls, not a string prefix check.

**Validate:** Normal and boundary values, malformed structures, duplicate/extra fields, oversized inputs, encoding differences and relevant injection paths. Test uploads/downloads for authorization, path confinement, content/type mismatch and decompression/resource limits. Book pp 79-91,111-116,133-146; [ASVS V1 sections 1.1–1.5](https://raw.githubusercontent.com/OWASP/ASVS/v5.0.0/5.0/en/0x10-V1-Encoding-and-Sanitization.md), [V2 sections 2.1–2.4](https://raw.githubusercontent.com/OWASP/ASVS/v5.0.0/5.0/en/0x11-V2-Validation-and-Business-Logic.md), [V5](https://raw.githubusercontent.com/OWASP/ASVS/v5.0.0/5.0/en/0x14-V5-File-Handling.md).

**Business concurrency action:** Protect scarce resources and policy state changes with actual atomicity at the responsible store/boundary. Define retry/replay semantics and outcome reconciliation. A local lock cannot enforce a cross-process invariant; a failed network response does not prove no side effect occurred. Stronger coordination can cost throughput and availability. Test concurrent and repeated operations against the invariant. Book pp 141-146; [ASVS v5.0.0-15.4.1–15.4.4](https://raw.githubusercontent.com/OWASP/ASVS/v5.0.0/5.0/en/0x24-V15-Secure-Coding-and-Architecture.md).

## Browser and API boundaries

**Action/context:** For browser applications, configure cookie scope/security attributes, CSRF defenses, contextual output handling, CSP and other headers for the actual flows. For APIs, inspect trusted proxy handling, framing, protocol-specific limits and error/data contracts. Do not impose browser controls on non-browser protocols.

**Why/exceptions/cost:** Browser restrictions reduce specific attack paths; they do not replace server authorization. Strict cross-origin policies can break legitimate embedded resources or login flows. HSTS needs reliable HTTPS and subdomain readiness; its max-age is not certificate lifetime. Avoid copying the book's deprecated X-XSS-Protection, Feature-Policy or Expect-CT examples.

**Validate:** Use an actual supported browser for cookie/origin/focus-sensitive flows and protocol tests for server behavior; check redirects, state-changing requests, intended cross-origin resources, sensitive caching and denial paths. Header presence alone is not proof. Book pp 66-78,133-146; [ASVS V3](https://raw.githubusercontent.com/OWASP/ASVS/v5.0.0/5.0/en/0x12-V3-Web-Frontend-Security.md), [V4](https://raw.githubusercontent.com/OWASP/ASVS/v5.0.0/5.0/en/0x13-V4-API-and-Web-Service.md), [OWASP HTTP Headers](https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html).

## Secrets, data, dependencies and configuration

**Action/context:** Classify affected data and minimize collection/return/retention. Keep backend secrets out of source, artifacts, URLs and diagnostics. Use existing secret distribution with least-privilege access, revocation and rotation. Use maintained cryptography and authenticated transport with verified peer identity; distinguish encryption, integrity and encoding.

**Why/exceptions/cost:** Protection must survive storage, transit, backups, caches and logs; moving secrets to a vault adds an availability dependency. Retention and recovery must respect actual requirements. Crypto migration needs compatibility and key lifecycle planning; neither a checksum nor Base64 provides authenticity/confidentiality.

**Validate:** Inspect actual deployed configuration and secret exposure; test invalid certificates, denied secret access, rotation, protected-data deletion/retention and recovery where authorized. Book pp 49-91,129-132,195-220; [ASVS V11](https://raw.githubusercontent.com/OWASP/ASVS/v5.0.0/5.0/en/0x20-V11-Cryptography.md), [V12](https://raw.githubusercontent.com/OWASP/ASVS/v5.0.0/5.0/en/0x21-V12-Secure-Communication.md), [V13](https://raw.githubusercontent.com/OWASP/ASVS/v5.0.0/5.0/en/0x22-V13-Configuration.md), [V14](https://raw.githubusercontent.com/OWASP/ASVS/v5.0.0/5.0/en/0x23-V14-Data-Protection.md).

**Dependency action:** Identify actual direct/transitive components and their origins, versions, exposure and update path. Triage advisories using reachable behavior and deployment impact; record an owner and mitigation/remediation timeframe. Scanner findings alone neither prove exploitation nor justify ignoring an issue. Updates can change behavior, so run relevant regression checks. Book pp 89-91,147-178; ASVS V15 above.

## Evidence, errors and observability

**Action/context:** For each relevant threat, combine control-focused review and repeatable negative checks. Log enough structured context to reconstruct security decisions while protecting identifiers, credentials and sensitive data. Separate expected domain denials from unexpected failures; fail the operation securely when its policy cannot be established.

**Why/exceptions/cost:** Logs aid investigation but can leak data or exhaust storage. Tool false positives and blind spots require triage. A fatal corrupted process may need safe restart rather than continued execution; recovery must not grant unauthorized access.

**Validate/report:** Exercise unavailable policy/identity dependencies, malformed requests and logging failures; verify no secret output and no prohibited side effect. Report evidence and scope, including untested routes. CWE can classify the demonstrated root cause; a CVE/CWE identifier is not a severity score. Book pp 129-132,147-194; [ASVS V16](https://raw.githubusercontent.com/OWASP/ASVS/v5.0.0/5.0/en/0x25-V16-Security-Logging-and-Error-Handling.md), [assessment guidance](https://raw.githubusercontent.com/OWASP/ASVS/v5.0.0/5.0/en/0x04-Assessment_and_Certification.md), [CWE-862 mapping and detection limits](https://cwe.mitre.org/data/definitions/862.html).
