# Negotiation and message identity

Choose framing independently from message semantics: JSON-RPC does not select a transport. Requests carry IDs; notifications do not receive responses. Version the host protocol independently from plugin package versions. [JSON-RPC 2.0](https://www.jsonrpc.org/specification) defines this envelope, not permissions or a plugin ABI.

Design record (not a wire standard): instance_generation, request_id, protocol_version, requested_capabilities, granted_capabilities, deadline. Require a complete negotiation before admitting effects. If the peer claims unsupported optional features, disable them explicitly; if a mandatory feature is absent, reject startup without partial activation.

Example oracle: host supports read/search, plugin asks read/write, grant is read on root A. The only effective grant is read on A. A later write request is denied even if its JSON is valid. An old-generation reply after restart must be recorded as stale, not applied to a reused request ID. Specify duplicate-ID handling and size limits before choosing serialization libraries.
