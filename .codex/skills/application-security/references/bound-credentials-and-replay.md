# Attenuated authority, proof of possession and replay state

Use when an operation reissues delegated authority, uses sender-constrained
credentials or must preserve anti-replay state across restart/offline operation.
This supplements [delegation and artifacts](delegation-and-artifacts.md), not a
requirement to add a new credential protocol.

## Establish the actual acceptance contract

Identify protocol/profile and version, issuer, authenticated actor/client, resource,
tenant, operation, audience, key purpose, validity, revocation and offline policy.
Locate every accepting route, including proxies and background paths. Consult the
profile's current normative checks and errata; terms such as PoP, nonce or signature
do not supply a complete protocol. Prefer maintained implementations.

For reissuance, check who may delegate and the authority the parent can confer.
Bind the child to the intended recipient/context; require permitted resource,
operation and time bounds within the parent's authority. Handle revocation and
unknown restrictions according to the selected profile without silently dropping
constraints. A capability supplied by another actor is not by itself authority to
mint a broader or longer-lived credential. Test legitimate restricted delegation.

For proof of possession, verify both the credential's key binding and the request's
proof using the selected scheme. Enforce the scheme on all relevant routes, including
proxy-originated traffic; an untrusted forwarding header cannot supply proof.
For OAuth DPoP, follow [RFC 9449 §§4.3, 7 and 11](https://www.rfc-editor.org/rfc/rfc9449.html)
for proof, token/key and request binding and replay constraints. DPoP is not client
authentication and does not sign arbitrary request bodies; do not transfer DPoP
rules mechanically to mTLS or another protocol.

## Preserve replay protection and permitted effects

Define the identity and scope of an operation, accepted duplicate behavior, replay
window, key/context lifetime, retention and recovery. Cryptographic freshness and
business idempotency are different guarantees. Decide how replay consumption and
the protected effect interact under concurrency and a crash between them; a memory
cache alone does not establish durability or cross-replica coordination.

If keys survive restart but counters/windows do not, use the protocol's supported
persistence, context renewal or recovery method before resuming acceptance.
[OSCORE RFC 8613 Appendix B.1](https://www.rfc-editor.org/rfc/rfc8613.html#appendix-B.1)
illustrates why sender sequence and recipient replay state need explicit recovery;
its storage procedure is not a universal counter recipe. Account for rollback,
replicas, offline acceptance, delayed messages and counter exhaustion. Expiring a
deduplication entry must not silently re-enable an effect still forbidden by policy.

Validate permitted operations as well as wrong actor/resource/key, expanded child
authority, stale/revoked context, forged proxy headers, repeated proofs and
concurrent duplicates. Exercise crash/restart and retention boundaries against
actual state and effects before claiming persistence. A toy verifier or a rejection
status alone cannot prove those properties. Report residual guarantees and cost.

Basis: Madden, *API Security in Action*, physical 329–351, 421–456 and 520–543.
The workflow is engineering synthesis; it does not authorize scans, choose an
offline policy or implement new cryptographic primitives.
