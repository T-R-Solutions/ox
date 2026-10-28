# Service engineering

Use this reference for services, external I/O, persistence, or background workflows. ZTP's frameworks, providers, containers and deployment topology are teaching choices, not mandatory architecture. Page numbers below are printed pages; [sources](sources.md#zero-to-production) records complete chapter coverage.

## Define and test the boundary

Specify accepted/rejected input, status/body/headers, persistence effects, permissions, resource limits and failure behavior before implementing an endpoint. Deserialize transport data, then validate domain invariants through constructors that cannot be bypassed by derived deserialization or mutation. Stored records can become invalid under newer rules: explicitly choose rejection, quarantine/skipping with reporting, migration, or processing under a historical schema. Do not `unwrap` merely because an earlier application version validated the row.

Test the actual protocol where routing, serialization, middleware, configuration or storage integration is at risk. Assert the exact required status and meaningful body/payload values; a generic successful response or mere field presence can miss the defect. Test forbidden effects as well as successful ones. Bind a listener to port zero and retain it for the server, avoiding a close-and-rebind race. Isolate database state per test and clean up resources deliberately. Rolling back a test connection does not roll back requests served through other pool connections.

Stub external providers at their protocol boundary to exercise timeout, malformed response and failure paths without real messages. Set and verify mock expectations within the relevant scenario; use reusable clients and production startup paths where possible. Test HTTP-client redirect and cookie settings explicitly, because automatic redirects can conceal the initial status and a new cookie store can lose the session.

Sources: ZTP ch. 3, 6–7, 9 and 10, especially pp. 260–268, 362–385, 460–478. For generated input, retain deterministic boundary cases and reproducible failing samples; generation is not exhaustive proof.

## Configuration, diagnostics, and execution

Load configuration in a documented precedence order, validate required values at startup, and expose errors with useful context. Keep real credentials out of committed examples, command traces, logs, images and generated fixtures. A redacting wrapper only protects formatting paths that actually use it; explicit secret exposure bypasses it.

Reuse connection pools and HTTP clients according to their ownership contracts. A cloneable pooled handle may already share its internals; adding an `Arc` is not automatically necessary. Set end-to-end request budgets and resource bounds appropriate to the operation; distinguish transport success from an acceptable HTTP/application response. Do not impose short-request timeouts on intentionally long-lived streams.

Use structured operation context and log primary errors where handled. Preserve causes internally while constructing explicit safe public responses. Never assume that a framework's generic internal-error wrapper redacts `Display`; inspect the pinned implementation and test the response body. Review automatic argument instrumentation for secrets and personal data. Use future-aware tracing across awaits and explicitly propagate context into blocking workers. Bound expensive CPU work; preserve both join errors and operation errors.

For database query macros or generated metadata, follow the pinned tool's offline/schema workflow and check it against the intended migrations/features. Compile-time query checks do not establish runtime connectivity. Separate liveness from readiness where deployment behavior requires it. Build/runtime architectures and native dependencies must be compatible; a container does not establish that automatically. Do not copy historical vendor plans, prices, TLS modes, or runtime images as present-day requirements.

Sources: ZTP ch. 4–5 and 8; pp. 230–242, 375–383 and 415–426. These are operational criteria, not an instruction to deploy or contact external services.

## Authentication and security-sensitive changes

Preserve the project's reviewed authentication, authorization and secret-management mechanisms. Distinguish identity from permission for the specific action/resource. Test unauthenticated, unauthorized, expired/revoked and permitted cases for affected routes, including middleware scope/order. A typed user ID does not by itself establish authorization.

ZTP deliberately progresses from insecure password handling to a password-hashing library, salts, PHC-formatted hashes, session renewal and logout. Never adopt the intermediate plaintext/fast-hash comparisons, public seed credentials, or simplified HMAC pseudocode. Do not select current cryptographic parameters from this historical snapshot. Use the project's approved policy and supported library, enforce its input/work limits, and test credential migration, old/new password behavior and failure paths. Offloading expensive hashing does not remove the need for a concurrency budget.

For sessions, identify token ownership, storage, expiry, renewal, revocation and cookie protection separately. Signing establishes integrity, not confidentiality or HTML safety. Encode untrusted content for the output context even after authentication or signature verification. Return an explicit public authentication failure while retaining restricted diagnostic context. Dummy hashing can reduce one enumeration signal; it is not proof of identical timing or a substitute for the project's abuse controls.

The corpus does not provide a complete CSRF design, modern password policy, key-rotation policy, or authorization model for arbitrary applications. This is a closed prerequisite: for a change affecting one of these controls, locate the existing policy and implementation, establish the contract from permitted evidence, then validate it. If it cannot be established, do not implement or approve that security-sensitive portion; use the [resolution procedure](validation-and-maintenance.md#resolve-missing-or-conflicting-evidence). Unrelated Rust work can continue. Do not label the tutorial or this skill a complete security standard.

Sources: ZTP ch. 10 in full, pp. 387–523; specific unresolved tutorial requirements and corrections appear in [source conflicts](source-conflicts.md#service-tutorial-completion-gates).

## Persistence, retries, and worker lifecycle

For a durable workflow, settle each row relevant to its acceptance criteria before claiming the workflow is complete:

| Decision | Required contract and validation |
| --- | --- |
| Validation and schema changes | Use parameterized queries and database constraints for their actual invariants. For rolling versions, plan expansion, backfill, transition and removal with compatibility/rollback behavior. Test old/new data and failure during migration; do not assume a full-table update has negligible locking cost. |
| Transaction boundary | Name the state changes covered by the transaction and observe commit failure. A dropped transaction may schedule rollback rather than finish it synchronously. No database rollback retracts an email or remote API effect. |
| Idempotency identity | Scope a key to principal and operation. Define payload equivalence and reject conflicting reuse before effects. Bound key size using explicit units and inclusive/exclusive limits. Test same key/same input, changed input, other principal and concurrent submissions. |
| Atomic claim and replay | Acquire durable ownership before irreversible work. Keep the local state transition and deduplication record atomic where required. Define isolation/conflict retries. Preserve required response semantics while limiting buffered size and protecting stored secrets; decide which headers may be replayed. |
| Unknown external outcome | Timeout/cancellation may follow remote success. Retry only under an actual idempotency contract or an explicit duplicate/compensation policy. Test failure before and after external success. Do not promise exactly-once delivery from local transactions or row locks. |
| Durable enqueue | Commit accepted work, its tasks and the response record together when atomic acceptance is required. Report accepted/enqueued versus delivered accurately. A durable row alone does not guarantee eventual successful delivery. |
| Retry and terminal failure | Classify outcomes, bound attempts/work, specify delay/backoff, and persist attempts when recovery requires it. Define terminal reporting/quarantine/discard policy. Do not delete transiently failed work while claiming it will be retried. |
| Retention | Define the deduplication window, retries after expiry, cleanup bounds and races with active work. An unimplemented expiry exercise does not establish bounded storage. |
| Capacity and shutdown | Bound workers, queues and connection use. Include connections held while awaiting additional pool acquisitions in the budget. Stop intake, account for outstanding work, terminate/drain and join tasks as required, and propagate a meaningful process status. |

Use controlled synchronization to test races; a delay that merely encourages overlap is insufficient evidence of the relevant interleaving. Directly draining a worker can test business behavior, but separately test supervision, failure, cancellation and shutdown when those change. Avoid adding an outbox or worker if synchronous handling already meets the stated guarantees.

Sources: ZTP ch. 7, pp. 269–321; ch. 11 in full, pp. 525–582. The table's completion gates are a synthesis of the demonstrated failures and explicitly omitted exercises, not a claim that the supplied application implements every gate.
