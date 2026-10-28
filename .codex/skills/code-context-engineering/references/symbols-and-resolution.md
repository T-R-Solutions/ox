# Identity and resolution strength

Separate syntax facts, semantic resolution and inferred similarity. A function-call token plus a matching name elsewhere is a candidate relation; overloads, imports, macros and dynamic dispatch can prevent unique resolution. Report candidate sets and the missing semantic context.

Consult the [LSP 3.17 specification](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/) for capability negotiation, document synchronization and position encoding before implementing an adapter. Record server version, document version and configuration with the result. Do not assume byte offsets equal protocol character positions; include non-ASCII fixtures.

Before returning a range, read the actual bytes and compare the expected hash. If it differs, refresh or label the result stale. A useful test uses two modules defining the same name plus a multibyte character before the call: the oracle checks both identity uncertainty and range conversion. LSP unavailability should retain path/text search with reduced guarantees.
