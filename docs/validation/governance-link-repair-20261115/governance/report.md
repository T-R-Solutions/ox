# Governance implementation observations — 2026-11-15

Scope: T002/T003, GL-01/02/03, delegated by the coordinator after T001. Local
implementation/tests/documentary reporting only; no complete automation, downloads,
central maintenance, commits or publication. This implementer's report does not
replace independent review or criterion acceptance.

## Changes and boundaries

`historical_link_revision.py` authenticates the required additional origins registry
with the transferred `efc3c228...` pin, exact schema/inventory and the preserved older
registry binding. Five sources map to the reviewed two original locations. Required
files, lexical paths, symlinks, duplicate JSON properties, duplicate/conflicting
sources and unknown inventory fail closed. Unlisted Markdown keeps its own location.
No missing-registry legacy mode, target search or directory exclusion exists.

`log_repair_revision.py` combines the authenticated sixteen older origins with the
five new ones. New records have empty excluded-target sets. The twelve historical
missing-target pairs are unchanged and still require the exact declared-copy receipt.
The old metadata/source checks remain in place, with explicit schema/type guards.

The separately pinned `successors.json` (`904ff632...`) normalizes exactly the four
configuration-cohesion documents and scripts README before the older predecessor
chain. It checks the previous registry, origins identity and retained `.bin` preimages.
All five live documents must have their exact reviewed hashes; unknown live bytes,
missing files, symlinks and predecessor downgrade fail. Unknown argument bytes only
pass through when the live files remain exact. `sdd/project.md` and the pinned public checker
are unchanged. Registries and historical sources were never written by this agent.

Partial fixtures obtain new succession inputs explicitly through `fixture_paths`.
Two additional fixtures (`test_defaults_succession.py` and
`test_configuration_succession.py`) received separately delegated ownership for this
adaptation. `test_instruction_copy.py` distinguishes the required decision reference
from hash-authenticated inputs: its bytes are not declared pinned by this registry,
but its absence is rejected. Original pinned inputs retain their tamper tests.

## Methods and inputs

Primary skill actually read/applied:
`.codex/skills/autonomous-verification-engineering/SKILL.md`, through bridge
`sdd/chain/autonomous-verification-engineering.md`, bridge version 1; the skill has
no declared semantic version. Contribution: separate execution from acceptance,
independent expected pairs/counts, schema challenges independent of the outer pin,
public mutation rejection and retained failed observations.

The new test's expected five pairs and counts 1/10/1/1/9 are literal independent
oracles, rather than imported registry constants. All 22 decoded local destinations
exist at their reviewed original locations. Tests patch only a temporary in-memory
pin to reach schema guards; public subprocesses use production pins unchanged.
Public consumers use `isolated-run.py`, whose Python audit oracle rejects reads of
the original checkout's parent. A deliberate original-source read is rejected. This
is a read-observation oracle for these stdlib tools, not OS sandbox evidence.

Each command receipt records cwd, relevant environment, exit and raw stdout/stderr;
input manifests identify production, oracle, registry, source, preimage and contract
bytes. `focused-01-inputs.json` was captured during the initial run after code had
stabilized, with no own code edits between launch and capture. Subsequent manifests
were captured before their commands. Initial ownership preconditions are in
`implementation-inputs-before.json` and `additional-fixture-inputs-before.json`.

## Observations and retained history

| Observation | Result | Retained record |
| --- | --- | --- |
| Previous origin/successor and twelve-exception tests | 12/12 pass | `focused-01-1.*` |
| New helper/schema/scope/path/succession tests | 14/14 pass | `focused-02-1.*` |
| Defaults, configuration and instruction succession fixtures | 15/15 pass | `focused-02-2.*` |
| Instruction-copy receipts/live-source constraints | 6/6 pass | `focused-01-3.*` |
| Initial new nineteen-case suite | 18 pass, one shared-document baseline fails | `focused-01-2.*` |
| Public checkout checker | exit 0, no product acceptance | `public-checkout-01.*` |
| Immutable paths compared to transferred baseline | eight SHA-256 equalities pass | `immutable-comparison-01.json` |
| Final current guards, predecessors, receipts and shared fixtures | 52/52 pass | `current-guard-focused-01.*` |
| Final public baseline/required-registry/tamper and unknown README append | 2/2 pass | `current-guard-public/public-current-guard-01.*` |
| Final frozen-source export and recovery replay | 1/1 pass | `current-guard-public/clean-export-replay-01.*` |

The initial independent copy preceded the coordinator's shared-document corrections.
Its sole failure names both actual stale inputs: history-scanner-correction's
E-PUBLICATION-WORDING bound to `progress.sh`, and the malformed terminal-progress
prose starting `AC-01–06`. The other four public cases passed with their expected
diagnostics: changed/missing snapshot, unknown broken/encoded links, missing/symlinked
link target and deliberate isolation violation. This failure is retained; it is not
attributed to the origin repair or converted into a successful observation.

Only the affected public method is replayed from current shared documents:
`PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tools/governance/tests python3 -m unittest -v
test_historical_link_resolution.PublicHistoricalLinkTests.test_public_copy_requires_registry_and_rejects_recalculated_metadata`.
It checks a positive baseline, missing required registry, changed/recomputed metadata
under the real pin, then the restored positive baseline.

That single shared-document replay passed (one test, 70.646 seconds) in
`public-baseline-replay-01.*`, before the additional guard correction below.

Independent validation then demonstrated that an unregistered plain-text append to
the live scripts README still passed the public checker. The predecessor mapping
alone did not protect a path without a subsequent historical content comparison.
This was a real rejection of the initial implementation. The coordinator retains
the independent raw probe under `rejected-succession/` in the parent report folder.
Prior production/oracle bytes and SHA-256 identities are retained under
`before-current-guard/` and in `before-current-guard.json`.

The correction adds exact live-content checks for all five succession destinations,
and enumerates those destinations explicitly in partial fixtures. A new helper case
rejects unknown bytes, absence and symlink for each destination. The new public
README-append case first requires a positive copied-checker baseline, then requires
the specific `Historical-link current changed` diagnostic for the mutation. The two
critical public methods passed in 100.899 seconds; the separate frozen export and
recovery passed in 38.734 seconds. These final command logs were captured outside
the source tree in `/tmp/ox-governance-current-guard-6w80c1lc` and published only after
closure, with SHA-256 equality in `current-guard-public-publication.json`.

The earlier governance discovery found 205 cases, selected 200 and excluded five
then-existing public cases. The explicit selection is retained in
`governance-regression-01-selection.json`. It reached 32 completed test markers
before interruption: one marked ERROR for clean export; the final traceback was
not emitted before interruption. Source mutation by concurrent captured artifacts
is a plausible cause, not a confirmed diagnosis. The production export and its test
were not relaxed; the final frozen replay passes.

After the independent live-content defect was confirmed, `write_stdin` U+0003
terminated that prior-code regression with observed exit 130, before production
mutation (`governance-regression-01-interruption.json`). It is incomplete and does
not approve the final code. The coordinator explicitly disposed a further full
regression as disproportionate for the bounded five-terminal guard and fixture
enumeration change: the 52 current focused cases, two critical public methods and
frozen export replay are the final observations. Broad integration/GL-07 remains
INCONCLUSIVE; no complete-suite or whole-feature green result is claimed.

## Documentary disposition and limitations

Reviewed README, scripts README, governance/local-artifacts guides, project/workflow,
constitution/architecture, relevant governance and closure ADRs, the reviewed repair
plan and configuration-cohesion contracts. No new CLI, distribution allowlist,
receipt, retention or product behavior is introduced by this implementation. The
coordinator owns common-guide/feature updates and all evidence envelopes; this
agent only updates this implementation report and its observations.

Independent review/validation and selected whole-feature acceptance remain the
coordinator's responsibility. Existing configuration-cohesion criteria are not
silently refreshed or approved. These tests concern governance and controlled
copies, not scanners, product operation, performance or public distribution.
