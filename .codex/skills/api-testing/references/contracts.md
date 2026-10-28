# Contracts and Compatibility

These are engineering recommendations with explicit contexts, not universal architectural rules. Book page references are physical PDF pages, 1-based.

## Establish an independent oracle

**Action and context:** Before adding API assertions, compare the published contract, caller expectations, and observed implementation. Record disagreements and clarify the material ambiguity; do not silently promote current behavior to the specification.

**Evidence:** Winteringham, *Testing Web APIs*, chapter 4, PDF 105–145; Aniche, *Effective Software Testing*, chapters 2 and 4, PDF 58–90 and 125–144.

**Rationale:** A test generated from the same mistaken model as production can confirm a shared defect. Contract review exposes missing type, state, and error decisions early.

**Exceptions and trade-offs:** A legacy characterization test can intentionally preserve observed behavior while requirements are recovered. Label it accordingly. Independent request construction adds maintenance but reduces shared serialization mistakes; reuse production DTOs only with that trade-off understood.

**Validation:** Trace representative requests and malformed variants to an accepted requirement. Check responses and effects with an oracle that does not recompute the production algorithm.

## Validate schemas in their declared dialect

**Action and context:** With a machine-readable schema, validate the document and selected requests/responses using compatible tooling already present in the project. Include required/optional fields, omission versus null, numeric bounds, strings, arrays, and unknown properties according to the actual contract.

**Evidence:** Winteringham chapter 4 PDF 128–137; [OpenAPI 3.1.1 Schema Object, section 4.8.24](https://spec.openapis.org/oas/v3.1.1.html#schema-object), consulted 2026-10-17.

**Rationale:** OpenAPI 3.1 uses JSON Schema 2020-12 semantics; some constraints such as `format` are annotations unless tooling enforces them. A validator's green result must be interpreted through its configuration.

**Exceptions and trade-offs:** Other protocols may use different schemas. Do not migrate a specification version just to adopt this skill. Schema tooling adds compatibility/maintenance costs and cannot establish business invariants or authorization by itself.

**Validation:** Include one deliberately invalid sample for each important enforced constraint and demonstrate rejection. Test semantics omitted by the schema separately. The book's OpenAPI 3.0 listing contains duplicated keys and inconsistent fields; do not copy it as a valid template.

## Coordinate consumer and provider evidence

**Action and context:** For independently evolving participants, encode actual consumer interactions, verify the provider against deterministic states, and associate results with the versions that may run together. Review compatibility before deployment.

**Evidence:** Winteringham chapter 9 PDF 291–315; [Pact: When to use Pact](https://docs.pact.io/getting_started/what_is_pact_good_for), all substantive sections consulted 2026-10-17, page updated 2022-04-13.

**Rationale:** Consumer assertions and provider verification expose divergent expectations without requiring every environment to be live simultaneously. They do not prove downstream side effects, network configuration, or full business workflows.

**Exceptions and trade-offs:** Pact is a candidate when both sides cooperate and provider state is controllable. Unknown public consumers or an uncooperative external provider weaken this approach. Broker operations, fixtures, matching rules, version selectors, and communication have costs. Contract sharing must not expose secrets or private payloads.

**Validation:** Introduce a controlled incompatible response or request and verify the relevant check fails. Confirm required interactions are exercised by real consumer code. Retain targeted integration checks for risks outside contract verification. A pending verification failure must not be mistaken for compatibility evidence.

## Evolve deliberately

**Action and context:** When an API changes, identify old/new consumer and provider combinations, including staggered deployments. Test meaningful differences in field presence, nullability, enum values, semantics, error handling, and ordering.

**Evidence:** Synthesis of Winteringham chapter 4 PDF 114–115 and chapter 9 PDF 309–315 with Aniche chapter 4's contract discussion.

**Rationale:** A syntactically additive change can still break strict consumers or alter meaning. Replacing old expectations without examining use hides regressions.

**Exceptions and trade-offs:** A private in-process API deployed atomically may need fewer compatibility combinations. Maintaining legacy support costs complexity; an intentional break can be valid with an explicit migration agreement.

**Validation:** Run representative supported consumer behavior against the changed provider; show planned breaks and their migration path separately from regressions. Do not invent a universal semantic-versioning guarantee.
