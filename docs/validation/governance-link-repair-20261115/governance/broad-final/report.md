# Complete governance regression — 2026-11-15 local

The documented command completed on the frozen working tree:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools/governance/tests -v
```

Observed result: **207 test executions passed, exit 0, no failures, errors, skips or omissions**.
The unchanged discovery contains **198 unique test IDs**: nine ReadmeImportTests
IDs execute twice through existing discovery/import behavior. The selected list
retains all 207 executions; no deduplication or test omission was applied. The raw
unittest output and native result receipt remain unchanged. `summary.json` lists
the duplicate IDs explicitly.
The unittest duration was 2026.666 seconds; the capture wrapper, including the
post-run snapshot, recorded 2030.316 seconds. Execution ran from 2026-11-15
23:43:17 UTC to 2026-11-16 00:17:08 UTC (the local date remained November 15).

The before/after manifests cover 19,006 files from docs, SDD, scripts, tools,
configuration, .codex and application sources/configuration, including dirty and
untracked content. Git internals, caches, local outputs, target and generated
bytecode are excluded from this file-content snapshot. The two manifests are
identical: no input additions, deletions, file-kind changes or byte drift were
observed during the command. This statement concerns the observation interval;
these new report artifacts were published afterward.

The six public historical-link cases ran in this complete observation. Legacy
independent-copy, export/recovery, metadata, preservation, instruction, succession,
controlled wrapper and acceptance-contract cases also completed. In particular,
the clean export/recovery case passed with all command capture outside the source.
The earlier interrupted broad run and its unprinted ERROR traceback remain
historical; this successful run does not retroactively establish that error's cause.

Raw command [stdout](stdout.log) and [stderr](stderr.log), the [result receipt](result.json),
[explicit selection](selection.json), [before inputs](inputs-before.json) and
[after inputs](inputs-after.json) are retained unchanged. [Summary](summary.json)
records counts, environment and code identities. [Publication](publication.json)
compares every closed /tmp artifact with its repository copy using SHA-256.
Diagnostic live probes and the static remaining-call inspection are observations,
not modifications of the suite or source snapshot.

The prior broad200/exit130 observation and rejected live-README implementation
remain preserved in the parent record. No production, fixtures, common documents
or acceptance envelopes changed during this continuation. Only this assigned
broad-final folder was written after completion. No complete automation pipeline,
real scanner qualification, download, commit or external publication occurred.
This test result supports independent GL-07 validation; it does not itself approve
all feature criteria or product operation. The Python read-isolation oracle is not
an OS sandbox claim. The coordinator owns final documentation/evidence integration.
