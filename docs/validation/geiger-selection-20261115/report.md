# Persistent Geiger selection repair — 2026-11-15

Implementation and measured behavior completed; final independent closure verdict
is recorded in independent-validation.md.

Latest run ox-run-Fwke2bPi selected global cargo-geiger 0.14.0+ec.2,
SHA256 d47253c5cdeb6a2fbb4da048ae17b68d8235f4b93ff1b47f031129206b4084cc.
App/ui failed with serde@1.0.229 active-dependency association, native exit101;
the adapter correctly rejected incomplete reports with exit2. Other25 checks
returned zero. The local ox.1 SHA256499d0923d8fa12c7f2e61f53616f3698ac5561b1eac14886e955eb118b7427a0
exists and matches its qualification record in complete-repair-20261113.

Original locations (line1):
`.local/logs/2026-11-15/ox-run-Fwke2bPi--geiger--tool--0--stderr.log.log`
and `ox-run-Fwke2bPi--geiger--tool--1--stderr.log.log`: "Dependência ativa não
associada: registry+https://github.com/rust-lang/crates.io-index#serde@1.0.229".
This prevented complete app/ui metrics, rather than demonstrating an unsafe-code
finding in those applications. Original date2026-11-13 is absent; no recovery or
retention rotation was attempted, and its deletion notice alone proves no defect.

Source diagnosis: the old graph filter considers development dependencies of
non-root packages active before checking association with the target dependency
graph. Cargo does not activate those transitive development dependencies. The
existing local patch passes is_root_package and excludes non-root development
dependencies before association, while preserving rejection of missing active
normal/root development dependencies. The older plugin was selected again because
the runner appends Cargo-home/bin after caller PATH. The previous manual export
only changed that one invocation; it did not persist the selection.

The new explicit catalog selection binds a root-relative executable and SHA256;
all other discovery retains PATH precedence. Missing/unqualified installation
must block clearly. Sources/inputs/results and independent verdicts follow.

## Implementation and focused observations

Seven script surfaces are identified in implementation-inputs.json and
implementation.patch against session preimages. Backend/schema/catalog now
support explicit native executable identity; scripts/checks/run.sh binds its
captured identity to the pin before invocation and checks identity again at exit.
The production Geiger declaration points at the qualified local ox.1 binary.
The fixture declares its own controlled plugin identity; other Cargo plugins keep
PATH-first discovery. Missing installations fail clearly without acquisition.

68 script tests passed, exit0,133.033s, one opt-in real-security skip. Nine new
selection tests include invalid paths/types/transports, missing/drifted/symlinked
or nonexecutable tools, competing PATH plugin, tool-free plan and a deterministic
replacement between selector and runner identity reads. Earlier test failures
from the stale fixture review pin are preserved in implementation chronology;
the pin was updated only after the independent reviewer examined its seven-line
delta. No broader static exception was introduced.

The existing local Geiger source's graph tests were rerun offline:11passed,
exit0. Source diagnosis and prior binary qualification are separate from any
reproducible-build claim; no scanner executable was rebuilt or globally installed.
check-ox returned exit0 during focused review. The selected whole-feature
acceptance gate returned exit1 solely because all seven preexisting criteria
remain INCONCLUSIVE; this task does not claim broad feature acceptance.

Independent reviewer found and closed P2 (lost pin binding across two reads),
executed nine selection tests, and returned no open findings. An independent
validator confirmed those nine tests and the743original log hashes. Its subsequent
C1/C2/C3 approvals and final closure reexamination are recorded separately.

## Documentation disposition

scripts/README.md documents explicit selection, precedence, missing installation
and qualification requirements. scripts-centralization spec/plan/tasks register
authorized scope and the precise D-09 qualification of the historical PATH-first
contract. evidence.json retains INCONCLUSIVE states and historical observations.
AGENTS, constitution, architecture, README root, current project and native-tool
ownership ADR were reviewed; product APIs, global installations, retention,
Toolbox ownership and canonical complete-run command do not change. No edits to
those authorities are needed. Public wrapper portability remains unchanged.

## Real adapter outcome

The unchanged real adapter interface ran all16 workspace members with the then-current
sources and the caller PATH intact. invocation.json records that ordinary PATH
discovery still found global ec.2, while assessment.json identifies the declared
local ox.1 binary. Overall exit0, native0, state recorded,917.702s. Every member,
including app/ui, has exit0/tool_exit0 and complete reports accepted by the
unchanged strict parser. No manual export of a preferred tool directory was used.

The entry was `bash scripts/checks/run.sh --check geiger --output DIR` with
OX_ACTIVE_RUN identifying the owned temporary run and CARGO_HOME selecting the
normal local dependency cache. Explicit temporary output suppresses publication
and rotation; it does not replace the backend/parser. Native raw output, input
identities and per-member assessments are retained under native/.

The immediate post-run input comparison found zero changed/missing inputs. All743 original logs
remain byte-identical, with no additions or removals. No global executable,
application source, dependency lockfile, parser policy or tool installation was
changed. The complete pipeline was not rerun. Later fixture and documentation changes are explicitly reexamined below; the
original816input hashes and assessment are never renewed.

## Final scanners and bounded reexamination

The first static observation returned ShellCheck0/parser0 and Ruff0/parser0, but
Bandit1/parser1 for B108 at test_geiger_selection.py:100: the intentionally invalid
absolute path literal /tmp/plugin. No file was created there. The fixture now
derives its absolute path from its own TemporaryDirectory. This preserves the
rejection oracle without a fixed temporary pathname; no rule/baseline changed.
The failed observation remains in scanners-before-fixture-fix/.

After this one-test change, nine tests passed (exit0,1.784s), and the independent
reviewer repeated all nine (exit0,1.865s). New ShellCheck, Ruff and Bandit executions
and parsers all returned0 with no findings; post-scan input comparison has zero
changes at observation time. The subsequent task-status documentation change makes
the all-input scanner snapshot formally stale; independent manual reexamination
confirms its only drift is tasks.md, with no scanned code/configuration change.
Their exact argv, tool diagnostics, raw streams, exits and observed inputs
are under scanners-final/. The helper uses the configured Toolbox installation
and canonical all-source snapshot; it does not execute the complete pipeline.

The real Geiger observation and68-test suite precede this fixture-only change.
Their whole-input snapshots are formally stale for the final tree and remain
preserved as historical observations. New manual reexamination, not hash renewal,
confirms runtime inputs (Rust sources, backend, registry, runner, catalog, binary)
unchanged; the literal only feeds a negative schema fixture. The affected nine
tests and scanners were rerun. Task-status/documentary closure changes likewise
do not execute or configure the scanner. native-reexamination.json records exact
differences. C1/C3 rely on the identified real observation plus this scoped manual
reexamination; no current full-tree or complete-pipeline approval is claimed.

Changed production paths: scripts/lib/backends.sh, scripts/lib/registry.sh,
scripts/checks/run.sh and scripts/config/automation.json. Coverage/documentation:
scripts/tests/test_automation.py, scripts/tests/test_geiger_selection.py,
scripts/README.md, and scripts-centralization spec/plan/tasks/evidence. Exact
session deltas and preimages are preserved independently of the unrelated dirty
Git workspace. Documentation paths reviewed are listed above.

The selected executable lives in ignored local cache and is not supplied to other
checkouts by this repair. Missing or different binaries fail clearly; provisioning
a separately qualified local binary requires the applicable installation authority.
No remaining blocker is known for this checkout's scoped repair. Broad feature
acceptance remains INCONCLUSIVE, and no full pipeline/product or reproducible
binary-build approval is inferred.
