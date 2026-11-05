# Governance test timing review

Python 3.13.16, same Linux x86_64 host, perf_counter wall time, local files,
PYTHONDONTWRITEBYTECODE=1. Timings include setup/teardown, not only assertions.
Initial full baseline: 29 tests in 63.910 s, 3 failures and 1 error. It is not a
successful equal-coverage performance baseline: early assertion failures prevented
later checks from running. Per-test times and failures are retained in tests-before.log.
The two largest observations were specialized preservation (20.937 s) and metadata
corruption/deletion (13.001 s). Full-copy/archive checks dominate the suite.

After corrections: first complete run 33 tests in 114.280 s, passed. After adding
one recursive Git-archive regression, the same 34-test suite partitions into 17
fast tests (0.122 s) and 17 integration tests (111.818 s), no failures/skips.
Unittest discovery in an independently extracted package also ran all 34, passed
in 124.605 s. Isolation auditing adds overhead; do not compare that run as a speedup.

Equivalent comparison: three alternating sequential executions of exactly the same
15 original fast tests on retained before/current snapshots, same interpreter/host,
with no package/test job concurrently active. Median process wall time (including
imports): before 0.159526 s; after 0.160117 s. All six executions
passed. Exact commands, IDs, per-run times and logs are in common-valid-timings.json
and ox-common-valid-*.log. The baseline is nested under /tmp/ox-benchmark-before/repo
so the isolation fixture can use a sibling outside its parent, like the current root.
The first comparison attempt placed baseline directly under /tmp, and its isolation
oracle correctly rejected another /tmp fixture: 1 failure per baseline run. Those
failed timings/logs remain in common-timings.json and ox-common-*.log and are not used
as a successful comparison. Small differences are not claimed as optimization.

The improvement is a separately selectable ~0.12 s feedback group, not a faster
complete suite. The default run-tests command, unittest discovery and run-checks
retain every mandatory test. Integration checks are never silently skipped by the
complete command. New tests default to inclusion; groups form a disjoint partition.
