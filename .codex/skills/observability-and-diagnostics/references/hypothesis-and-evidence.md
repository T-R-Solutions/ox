# Hypotheses, timeline and diagnostic validation

Read for unexplained behavior or incident investigation. Separate immediate impact
reduction from proving cause; preserve incident evidence before resetting counters,
restarting processes or deploying a speculative fix.

1. Bound the symptom: affected operation/tenant/version, first/last observation,
   frequency, expected behavior and independent user-visible evidence. Establish
   whether clocks, units and collection windows align.
2. Map the path and recent changes: queue, connection pool, database, dependency,
   retries and background tasks. Distinguish execution time, waiting and overlapping
   work; summed span duration can exceed elapsed request duration.
3. Write competing hypotheses and predicted observations. For “database is slow,”
   discriminate query execution, lock wait, connection queue and client fetch using
   matching requests/windows. A high database CPU average alone is insufficient.
4. Rank by consequence, plausibility and information obtainable. Choose a bounded
   read-only observation or authorized experiment that can refute an explanation.
   Keep contrary evidence and unobserved boundaries explicit; do not select only
   a trace that fits the first story.
5. Reconcile metrics/logs/traces with independent counts and verify sampling, export
   loss and missing context before interpreting absence. If the same underlying
   counter feeds two dashboards, agreement is not independent corroboration.
6. Change one relevant mechanism when feasible, predict the result and verify the
   symptom/invariant under comparable conditions. A coincident improvement after a
   restart may be mitigation without establishing the original cause.
7. Record observation → hypothesis → discriminating check → result → supported claim,
   plus remaining alternatives and an exact next observation. Attach a sanitized
   reproducer/runbook and a regression/detection check when a defect is demonstrated.

Validate instrumentation with known outcomes and an independent oracle, not a mock
that emits the same assumed labels. Validate alerts for failure, no data, low traffic
and recovery; test a responder can reach evidence via the runbook. Attribute findings
to the tested environment and window. No universal SLO, alert threshold or backend
is justified by this method.

Research context: [Dapper](https://research.google/pubs/dapper-a-large-scale-distributed-systems-tracing-infrastructure/)
and [Pivot Tracing](https://cs.brown.edu/~jcmace/papers/mace15pivot.pdf) motivate
cross-boundary context and diagnostic cost accounting. Dapper's Google library
coverage/sampling and Pivot's Java/Hadoop instrumentation are specific systems;
neither supplies a transferable overhead budget or automatic causal diagnosis.
The procedure above is engineering synthesis, not a controlled efficacy result.
