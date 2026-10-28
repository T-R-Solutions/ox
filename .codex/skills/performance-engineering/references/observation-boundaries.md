# Instrumentation validity and eBPF boundaries

Use when a profile or event stream is being interpreted as proof. Sources: Rice, Learning eBPF ch. 6 pp. 120–122, ch. 9 pp. 171–173 (B07); Majors/Fong-Jones/Miranda, Observability Engineering ch. 5 pp. 57–59, ch. 17 pp. 213–215 (B01). [Coverage](portable-sources.md).

1. State the question, event population, attachment boundary and expected observation from a known controlled operation. Inspect installed kernel, tool, attachment support and allowed privileges before considering any probe. A successful verifier result is not proof of low overhead or policy correctness.
2. Use structured request/lifecycle events with correlation, operation, result, duration unit and relevant resource state. Keep secrets out; bound volume and field cardinality for the selected backend. Do not impose the book's event width as a requirement.
3. Record sampling probability/weight and decision point. Consistent trace decisions preserve related spans; missing sampled events cannot establish absence of a failure. Do not treat sampled counts as exact totals.
4. Track dropped events, map/buffer capacity, absent symbols and observer overhead. Reconcile known generated operations with observations, and compare a run without collection where safe. Distinguish attempts, completions and successful bytes.
5. A security diagnosis needs expected policy and error-path context as well as an event. An unusual syscall can be legitimate recovery. Escalate only with a concrete policy/impact hypothesis.
6. Preserve prior tracing configuration and remove attachments/resources at completion. Historical verifier limits and helper APIs are not current guarantees. If tools/privileges are absent, use application counters or OS observations and label the reduced scope.

Validation: a bounded known workload, retained raw telemetry, loss accounting and cleanup evidence. No privileged eBPF program was loaded here. The pilot's logs do not validate eBPF or distributed tracing.
