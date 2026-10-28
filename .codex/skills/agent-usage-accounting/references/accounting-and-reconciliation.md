# Replay, corrections and totals

Example contract: input_total=100, cached_input=30 (a subset), output=20. Total tokens are 120, not 150. A different provider may report exclusive categories; require its actual contract before applying either formula.

For cumulative streaming usage 10 then 15, use the latest valid cumulative value for that request, not 25. For delta events 10 then 15 with distinct IDs, sum 25. A repeated event ID with identical payload contributes nothing new; the same ID with changed payload is a conflict or explicit correction according to the source contract. A new billed retry has a new request identity and should not be suppressed as a transport replay.

Retain append-only observations and explicit adjustments. Reconcile provider totals against ingested request totals by interval, scope and completeness; show gaps instead of filling missing usage with zeros. Test out-of-order delivery and partially closed sessions.
