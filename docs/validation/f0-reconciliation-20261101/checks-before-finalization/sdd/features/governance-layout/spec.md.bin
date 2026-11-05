# Governance tool organization

Actor: Ox maintainer. Authorized request: move governance out of src/ and
update references and consumers. Scope: Python tools, configuration,
fixtures, documentation, traceability, package and affected evidence.
Does not implement the application or change skill or SDD core content.

- REQ-01: Reserve src/ for future application sources; tools in tools/governance/scripts/, tests in tools/governance/tests/ and evaluation data in the tool's tests/fixtures/.
- REQ-02: Separate current configuration (profile and normative coverage) into config/governance/ and update commands, imports and operational references.
- REQ-03: Distribute only governance, including its new paths and excluding application sources and unrelated tools/configuration.
- REQ-04: Preserve historical observations and replace affected active evidence only after new executions or inspections.
- AC-01 → REQ-01: src/ has no governance files; all 23 original files have identified destinations without loss; fixtures and profile retain their content and coverage changes only affected references.
- AC-02 → REQ-02: Documented commands run from the root and an independent copy; active references and traceability resolve to new locations; guards continue rejecting improper changes.
- AC-03 → REQ-03: The actual ZIP includes tools/governance/ and config/governance/, excludes src/, Cargo, crates and unrelated paths; the manifest matches and five commands pass in an independent extraction.
- AC-04 → REQ-04: Recoverable baseline, preserved prior history, new observations bound to current inputs and valid freshness; the skills' 36 technical scenarios remain UNVERIFIED.

Compatibility: Python commands intentionally change path; there are no
aliases in src/. Logs, archives and historical decisions retain their original paths.
The original validator remains in sdd/tools/validate.py. This does not select the future
crate structure, runtime, platform or product dependencies.

## Current applicability note — 2026-11-01

The literal requirement to keep all 36 skill scenarios UNVERIFIED records the preparatory baseline, not their current observed state. docs/decisions/technical-acceptance.md explicitly supersedes product-foundation AC-03 and the transition decision; skill-consumer-validation records the successor executions. Its named supersession does not expressly enumerate governance-externalization AC-06, governance-layout AC-04 or maintenance-001 AC-04. Those compound legacy gates remain INCONCLUSIVE pending maintainer confirmation of succession scope and any remaining preservation/qualification evidence. No original scenario, historical result or other clause is waived. Current consumer acceptance never transfers to the product. See docs/validation/f0-reconciliation-20261101/legacy-succession.md.
