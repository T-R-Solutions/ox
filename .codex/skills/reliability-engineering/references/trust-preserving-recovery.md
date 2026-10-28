# Recover service without restoring revoked trust

Use for recovery after relevant compromise, security-version rollback or key/trust
rotation. Ordinary functional rollback still uses
[deployment and recovery](deployment-and-recovery.md). Do not impose a security
incident workflow on an unrelated local change.

## Determine the trusted starting point

Map artifacts, source/build provenance, signing roots, credentials, authorization
state, backups and persistent metadata. Record what is known compromised, unknown
or still trusted, the required recovery outcome and the owner's authority. Do not
assume every key must rotate or that a signed artifact is currently acceptable.

Order recovery around trustworthy prerequisites: verification and emergency access
must not depend solely on a component already considered compromised. Use existing
approved recovery mechanisms and authenticated sources. Distinguish evidence of
matching bytes, permitted signer/build provenance and permitted security version.

## Keep security state through transitions

1. Separate functional rollback compatibility from a security floor or revocation
   rule. Identify the authority for that rule, its scope and how it is protected.
   A previous signed but vulnerable image can be a prohibited recovery candidate.
2. Bind artifact, version and security metadata under the updater's actual trust
   contract. Check copied/mismatched metadata, interrupted activation, restart and
   restore of old snapshots. State how a crash between security-state persistence
   and activation avoids silently reopening forbidden versions.
3. For relevant credential rotation, establish new trust and verify that the old
   authority stops working on every declared consumer. Include caches, replicas,
   disconnected clients and delayed messages. Describe allowed offline behavior
   or a visible unavailable state; unknown revocation is not permission to fail open.
4. Restore backups with authenticity, version and semantic checks. Reconcile
   authorization changes, deletion obligations and old secrets so restoration does
   not silently resurrect prohibited data or access. A recent timestamp is not proof.
5. Exercise authorized emergency recovery without bypassing the same essential
   trust boundary. Record bounded exceptions, expiry/removal conditions and the
   evidence needed before reintegrating the recovered component.

## Validate the actual guarantee

In a disposable environment, test a legitimate restoration, a forbidden old signed
image, substituted metadata, an interrupted transition, rejected old credentials,
tampered backup and permitted emergency access. Observe both service recovery and
absence of prohibited effects. Rejecting everything is not successful recovery.
Use the destination platform's storage/updater/identity semantics; a model of these
transitions does not prove hardware, PKI or a deployed cluster works.

Deliver the dependency order, trusted inputs, decisions, recovery evidence, residual
uncertainty and a way to stop/recover the experiment. Basic reachability alone is
not evidence that trust was restored.

Basis: *Building Secure and Reliable Systems*, physical 39–40, 214–251 and 453–478.
[NIST SP 800-193's abstract](https://csrc.nist.gov/pubs/sp/800/193/final) supplies
the firmware-specific protect/detect/recover context; this reference does not claim
NIST conformance or transfer hardware mechanisms to every application.
