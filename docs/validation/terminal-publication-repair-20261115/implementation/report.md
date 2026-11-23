# Implementation observation — 2026-11-15

Ownership: `scripts/lib/progress.sh`, newly assigned
`scripts/tests/test_terminal_publication.py`, and this implementation directory.
The original `scripts/tests/test_terminal_progress.py` remains byte-identical.
No configuration, baseline, gate or unrelated source was edited.

## Failure and intervention

The emergency log `/tmp/ox-publication-dhE1Bz7i.log` contains an `rm` failure:
`Directory not empty` for `/tmp/ox-run-bOeh24Oi`. Inspection shows that
`run_complete` calls retention and then removes its owned run. The finalization
watcher formerly called `progress_line` while those operations were underway;
that function atomically rewrote `progress-observed.json` inside the run.
The new test observes inode and nanosecond timestamp changes in that run during
a 2.2-second publication delay. It fails against the preserved implementation
and passes after the change. This establishes the competing writer; the original
incident's exact process interleaving was not traced.

`progress_line` now accepts an optional recording flag, defaulting to `true`.
Only the finalization watcher selects `false`, avoiding both reads of the observed
file and its writes. The synchronous initial finalization line still reconciles
the greatest observed percentage and records the finalization snapshot before
the publisher starts. The watcher continues terminal refreshes and redirected
heartbeats, using its inherited counters. Preparation and check watchers preserve
their existing recording behavior. No retry, extra writer or retention change
was introduced.

The seven historical SC2250/SC2312 findings were addressed by bracing the five
variable references and evaluating phase name/action substitutions separately,
with explicit failure propagation. Native ShellCheck is coordinated separately.

## Observations

Environment: GNU Bash 5.3.20(1)-release, Python 3.13.16, Linux checkout.
Commands were run from `/home/rodrigo/Projetos/ox` with bytecode disabled.

| Command | Result | Artifact |
| --- | --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s scripts/tests -p test_terminal_publication.py -v` against preimage | exit 1, expected assertion failure on changed inode/timestamp manifest | `before-test.log` |
| Same command after repair | exit 0, 1 test | `after-publication-test.log` |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s scripts/tests -p 'test_terminal_*.py' -v` | exit 0, 28 tests in 33.433s | `terminal-suites.log` |
| `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=scripts/tests python3 -m unittest test_process_lifecycle test_local_lifecycle test_capture_status -v` | exit 0, 13 tests in 1.837s | `lifecycle-suites.log` |
| `bash -n scripts/lib/progress.sh` | exit 0 | `bash-syntax.log` |

The added test reuses the existing runner fixture and subprocess boundary. It
compares the entire temporary run's identities/timestamps before and after the
publication delay, requires elapsed-time refreshes, checks removal and retained
results/snapshot, and observes another 1.1 seconds after cleanup to expose late
reads/writes. Existing terminal tests exercise publication failure, emergency-log
failure, SIGTERM during publication, cancellation during execution, pipe EOF,
monotonic progress, raw-byte preservation, findings and operational exit codes.
Retention tests exercise two-date removal, concurrent publication and raw bytes.

## Inputs and limits

Preserved production preimage: SHA-256
`736b9d58d534707483ab3890410a8262e1dd044e4851a6305f1938df88e85116`.
The oracle is identical for the before/after invocation and the combined suite;
its SHA-256 is `79aa40faedda0de16d7cfa51295b5eed0707b104530e8ceff6320238b70a89a9`.
`inputs.sha256` records the observed final source/helper/configuration bytes and
preserved preimages. `artifacts.sha256` identifies the execution logs.

These are disposable fixtures and local regression observations. They do not
qualify a complete scanner run or product acceptance. ShellCheck/Ruff/Bandit are
absent from the local PATH; the coordinator owns the authorized native targeted
ShellCheck observation. No download, full pipeline, commit or publication was
performed by this implementer. Independent review/validation remain coordinator
steps; this report is not an approval.

Documentation disposition: reviewed `scripts/README.md` progress/retention contract,
the shell-refactor/task-closure ADRs and SDD workflow/evidence. Document ownership
remains with the coordinator, who will record the finalization concurrency repair
in the existing feature and validation successor. Public CLI, output states,
heartbeat cadence, log paths and retention policy remain unchanged.
