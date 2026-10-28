# Delegation, outbound requests and artifact trust

Use the section matching the boundary. These procedures do not authorize external
scans or deployment-policy changes beyond the user's task.

## Delegated authority

Basis: Neil Madden, *API Security in Action*, §7.1.2 (physical PDF 245).
Map actor, client, issuer, audience, delegated scope, resource ownership and tenant.
Access must satisfy both delegated scope and resource policy; scope cannot grant
permissions the principal lacks. Separate user delegation from a service's own
identity. Do not forward a token to an unrelated service.

Use maintained OAuth/OIDC implementations and verify the chosen flow.
[RFC 9700](https://www.rfc-editor.org/rfc/rfc9700.html), §§2.1–2.4 and 4.14
(2026-10-19), requires PKCE for public authorization-code clients and recommends
it for confidential clients. Bind transaction and issuer, validate redirects and
audience, and follow refresh-token replay protection. Do not introduce the password
grant or use an ID token as an arbitrary API credential.

Validate allowed delegation and denied wrong-resource/tenant/scope/audience, code
replay, wrong transaction binding and revocation. Assert no prohibited effects.
Document concurrent-refresh and unavailable-policy behavior; signature verification
alone does not settle authority. Revocation adds state/coordination costs.

## Outbound URL fetching

Basis: Madden §10.2.8 (physical PDF 388), qualified by
[OWASP SSRF prevention](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html)
(2026-10-19). Prefer explicit allowed services where the product permits. Parse URLs;
restrict schemes, destinations and ports. Disable redirects or revalidate every hop.
Account for all address families and DNS changing between validation and connection.
Enforce destination policy at connection/egress as well as input validation, using
the selected client's supported mechanism. TLS and inbound Host checks alone do
not define outbound policy. Do not forward credentials across destinations; bound
response bytes and duration.

Validate in an isolated fixture: allowed fetch, private/loopback address, changed
DNS answer, redirect to prohibited destination, oversized/slow response and cleanup.
Distinguish preflight rejection from evidence of no forbidden connection.

## Verify the deployed artifact

Basis: Adkins et al., *Building Secure and Reliable Systems*, ch. 14 “Verify
Artifacts, Not Just People” and “Binary Provenance” (physical PDF 345, 350–351).
Trace source revision, dependencies, build configuration, builder identity, output
digest, test results and deployed bytes. Protect provenance against tampering;
check it against the actual artifact and allowed builder/source policy. A digest
establishes matching bytes; a signature adds a trust claim whose signer and authority
still need validation. Neither proves software safety.

For a relevant supply-chain threat, enforce verification at deployment and inspect
bypass paths. Use existing infrastructure; do not mandate a new signing service
or Google's stack. Keep legitimate emergency access limited and auditable without
inventing approval requirements for unrelated work.

Validation: accept a permitted artifact; reject substituted bytes, untrusted builder,
mismatched source/test evidence and replay forbidden by actual policy. Exercise
authorized recovery without silently bypassing verification. Static review cannot
prove enforcement of a live deployment gate or builder isolation.
