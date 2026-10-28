# User outcomes, telemetry and actionable alerts

Use for instrumentation, SLI/SLO definition or noisy/missing alerts. Basis:
Majors, Fong-Jones and Miranda, *Observability Engineering*, chs. 12–13 (physical
PDF 152–153, 157, 159–160, 164–165). The book's preference for events does not
make aggregate metrics useless; measurement fitness depends on the question.

## Define the population before the target

Record the user operation, eligible population, good/bad criteria, observation
point, window, exclusions and owner of the target. Distinguish request-based
success from time-based availability; their percentages are not interchangeable
when traffic changes. For request-based SLO S and N eligible events, the allowed
bad count is (1−S)N. Define retries, timeouts and unfinished work so disappearing
requests do not improve the score. Zero traffic or missing telemetry is not success.

Use the agreed target, never a book's example percentage. For error ratio e,
burn rate e/(1−S) compares consumption to the allowed fraction when 0<S<1.
Choose alert windows/thresholds from tolerated budget consumption and response
time; use multiple windows when they improve detection/reset trade-offs. Test low
traffic, spikes, sustained failure, no data and recovery. See
[Google SRE, Alerting on SLOs](https://sre.google/workbook/alerting-on-slos/),
“Multiwindow, Multi-Burn-Rate Alerts” and low-traffic guidance (2026-10-19).

## Connect an alert to a diagnosis

Provide affected cohort/operation, time window, recent change context and actionable
runbook. Page when urgency and available action justify interruption; route slower
issues to the existing work process. Retain capacity, security or telemetry-health
signals when they detect important risks before user failures. Demonstrate replacement
coverage and recovery before retiring an existing alert; do not delete by category.

Instrument representative request lifecycles with safe structured fields and
correlation across boundaries. Put high-cardinality detail where the backend can
support it; do not blindly turn user/request IDs into metric labels. Verify context
propagation, asynchronous links, duration units, redaction and retention.

Choose sampling by diagnostic need and cost. Head sampling cannot select by a
later error; tail sampling needs state and may lose late spans or overload its
collector. Neither restores spans discarded upstream. Do not use biased trace
samples as exact SLO denominators. Track export loss, queue age and collector health.
[OpenTelemetry sampling](https://opentelemetry.io/docs/concepts/sampling/)
documents head/tail trade-offs; verify the installed SDK/collector configuration.

Validation: run a known bounded success/error workload and reconcile independent
counts with telemetry and alert decisions. Check redaction, context across one
dependency, loss reporting, alert reset and useful runbook steps. A dashboard or
configured rule alone does not establish detection or response.
