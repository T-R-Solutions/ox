# Independent governance — revision 1

Actor: maintainer and authorized agents. Authorization: request to apply
Ox_Correcoes_Governanca_Independente_v1.1.md. Scope: governance, library,
checkers and local distribution. Do not implement or publish the product.

- REQ-01: Neither require nor distribute the three external studies, including for recovery.
- REQ-02: Keep local authorities, the versioned catalog and SDD 1.3.0 contracts intact.
- REQ-03: Preserve old observations without reusing approval of stale inputs.
- REQ-04: Deliver a new package with inspection and execution in an independent extraction.
- AC-01 → REQ-01: An independent copy runs the Ox and SDD checkers without studies or the source library.
- AC-02 → REQ-01: Recursive inspection rejects study names and full contents in files and archives, including renamed ones.
- AC-03 → REQ-02: Coverage points to existing local authority IDs; links and catalog/profile agree.
- AC-04 → REQ-02: Tests reject skill, bridge, authority, evidence and link corruption; restoration recovers success.
- AC-05 → REQ-03: Previous observations are preserved with original hashes; affected evidence is replaced with new observations or an undecided state.
- AC-06 → REQ-03: The nine skills' 36 technical scenarios remain UNVERIFIED.
- AC-07 → REQ-04: The new ZIP contains a verifiable inventory and passes recursive inspection and the five official commands in a clean extraction.

Reject: reintroduction of originals; approval by file count alone;
promotion of technical proposals; retrospective evidence alteration; global
approval of skills as implementation. Product license/platform remain
open in docs/decisions/open-questions.md.

## Current applicability note — 2026-11-01

The literal requirement to keep all 36 skill scenarios UNVERIFIED records the preparatory baseline, not their current observed state. docs/decisions/technical-acceptance.md explicitly supersedes product-foundation AC-03 and the transition decision; skill-consumer-validation records the successor executions. Its named supersession does not expressly enumerate governance-externalization AC-06, governance-layout AC-04 or maintenance-001 AC-04. Those compound legacy gates remain INCONCLUSIVE pending maintainer confirmation of succession scope and any remaining preservation/qualification evidence. No original scenario, historical result or other clause is waived. Current consumer acceptance never transfers to the product. See docs/validation/f0-reconciliation-20261101/legacy-succession.md.
