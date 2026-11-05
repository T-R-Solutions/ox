# Skill evaluations

Case contract; execution must be recorded separately. These are not completed tests.

## Preserved technical scenarios

- AC-01 → REQ-01: A compatible, authorized plugin negotiates only granted capabilities; oracle: client/provider fixture and message assertions.
- AC-02 → REQ-02: An incompatible or malformed plugin receives an explicit failure without persistent mutation; oracle: compatibility harness.
- AC-03 → REQ-03: A plugin exits during an operation and the host recovers/expires resources without blocking; oracle: crash and timeout test.
- AC-04 → REQ-03: An unauthorized plugin attempts to read a protected path and the host blocks the effect; oracle: sandbox integration on the target OS.

## Evaluation protocol

Give an agent a concrete request and minimal inputs in an authorized isolated directory. In the selection round, show only the catalog/descriptions, without the expected answer. In the behavior round, provide the selected skill and adversarial data. Preserve the prompt, raw response, known agent identity/configuration, input hashes, outcome review and limitations. Do not run services or tools requiring new permissions.

Positive selection: request the specialized deliverable described in this entry. Negative selection: use the explicit exclusion; the response should identify a more suitable capability without loading this skill. Failure: provide input that contradicts the technical scenario and require evidence before approval. Concrete prompts in the consumer package must include sufficient data and an independent oracle.

## Concrete prompts

### plugin-protocol-engineering-positive

Create a host/plugin protocol for an LSP provider with version and permission negotiation.

### plugin-protocol-engineering-negative

Add a lint rule using an established plugin SDK without changing the protocol or permissions.

### plugin-protocol-engineering-failure

The host offers read/search; the plugin requests read/write; the grant is read on root A. The plugin in a separate process claims it can read root B directly and crashes after writing but before responding. Propose a contract and checks; do not run processes.

Review oracle: positive selects this specialized capability; negative routes to api-testing (or a justified adjacent capability). In the failure case, check: effective read A only; process is not sandbox; reconcile uncertain effect before retry. Review this answer key after the response; do not provide it to the evaluator during selection.
