# Usage event identity

Suggested design fields: provider/account scope, request_id, attempt_id, event_id, sequence, occurred_at, observed_at, metric_kind, token_category, value, unit, precision, source_locator and contract_version. Record whether a value is a delta or cumulative snapshot. Null/unavailable is distinct from zero measured usage.

The consulted [OpenTelemetry GenAI attributes](https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai/) distinguish input/output and cache token attributes. Verify each adapter's meaning before mapping fields; convention stability and provider support can vary. This is an interoperability reference, not a billing contract.

Do not use prompt contents as a deduplication key or store secrets for correlation. A provider request ID may be unique only within an account. Preserve conflicting payloads with a reconciliation status so an ingestion bug cannot silently rewrite measured history.
