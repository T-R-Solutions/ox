# Explicit Geiger selection implementation — 2026-11-15

Owner: ec_implementador under ec_orquestrador_alta. Scope is persistent local
selection of the already installed corrected Geiger, preserving unrelated edits
and original logs. before/ holds exact session preimages; implementation.patch
compares those bytes, rather than attributing the entire dirty Git diff to this task.

Consulted primary: .codex/skills/software-delivery/SKILL.md and its
references/build-inputs-and-trust.md; sdd/chain/software-delivery.md bridge version1.
Contribution: identify explicit tool inputs and artifact digest, reject substituted
or missing cache artifacts, distinguish selected executable from PATH discovery.
No claim of independent reproducible tool build or universal scanner completeness.

## Implementation

- checks.geiger.executable selects the root-relative local ox.1 binary and its
  previously observed SHA256. Catalog schema admits this exact path/hash object
  only for native checks, rejects malformed values, absolute/traversing/control
  character paths, and unknown object keys.
- check_properties projects the executable fields; native selection checks path
  containment without symlinks, regular executable file and exact digest. Explicit
  failure blocks without PATH fallback. Checks without this object keep PATH-first
  Cargo discovery and existing OX_CARGO_BIN validation.
- Modern pure plans show the declared executable without accessing or executing
  it. Legacy discovery still reports an unavailable native check as before.
- Review P2 exposed a possible binary change between selection and the runner's
  captured tool identity. run.sh now requires that captured digest to equal the
  configured pin before version invocation. Existing end-of-check tool identity
  checks remain. A deterministic fixture replaces the binary after selection's
  hash; the actual adapter rejects it before any tool execution.
- Existing controlled Geiger adapter fixtures declare their own path/hash pair.
  Report completeness, locked/offline/all-features arguments and eager iteration
  through all members are unchanged.

## Focused observations before final freeze

`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s scripts/tests -p test_geiger_selection.py -v`:
9 tests passed, exit0,1.818s. Includes explicit priority over PATH, other-plugin
PATH priority, missing/drifted/nonexecutable/directory/symlink inputs, malformed
catalog and path cases, pure plan without binary, and selection-to-capture drift.

`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s scripts/tests -p test_automation.py -v`:
10 tests passed, exit0,14.552s. Existing controlled scanner identity and incomplete
first-member/remaining-member behavior were exercised; no real scanner homologation.

`bash scripts/check.sh`: exit0. Targeted `git diff --check`: exit0.
Actual select_backend with unmodified caller PATH resolved the local configured
Geiger, without invoking it. The coordinator owns real current-input scanner replay.

The first test_backends run exposed static-review drift for the modified fixture
file before a new review/pin. That failed observation is not accepted; final source
review and affected focused rerun are pending at this point in the chronology.

Documentation disposition: scripts/README.md now describes the explicit selected
Geiger, precedence, absent/drift blocking and pure-plan behavior. Its historical
manual PATH recipe is explicitly superseded. No product behavior, serialization,
dependency version, tool installation or global executable was modified. SDD
scope/evidence and final independent review/validation belong to the coordinator.

## Independent fixture review successor

The independent reviewer examined the seven added fixture catalog lines in
scripts/tests/test_automation.py: the private fake tool path and S.digest are
registered explicitly; no subprocess, shell, network, suppression or production
command changed. Only that source pin in reviews.static.sources was updated after
this review. Its old bytes and digest remain in before/scripts/config/automation.json.bin.
This is a new source-review observation, not renewal of the historical scanner result.

## Final implementation checks

After the independent fixture review and that single source-pin successor,
`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s scripts/tests -v`
completed with exit0:68tests in133.033s, one opt-in real-tool skip. Raw streams are
script-tests.stdout.log and script-tests.stderr.log. This includes all12backends
cases (the former static-drift failures now pass),9new selection cases, catalog,
pure planning, adapter identity, omission and process/retention fixtures. Production
logs were not rotated: any lifecycle execution belongs to disposable test roots.
The earlier backends-only run had14failed subcases in12tests/81.468s from the old
static source pin; that tool transcript and diagnosis remain historical.

Final syntax and targeted diff-whitespace checks passed. implementation-inputs.json
identifies the seven changed code/configuration/test/document files. Sources are
frozen; no implementation process remains. Real Geiger replay, independent review
and final validation are coordinated separately and must not be inferred from
these fixture tests.

## Fixture-path Bandit successor

The subsequent real Bandit scan reported B108 on the literal /tmp/plugin in the
invalid-path vector. No file was created there. The rejected absolute-path case
now uses str(self.root / "plugin"), the same per-test TemporaryDirectory fixture.
The absolute-path rejection scenario is preserved without an unmanaged temporary
path literal; no baseline or scanner rule changed. before-bandit/ preserves the
exact prior test bytes, implementation-inputs-before-bandit.json and
implementation-before-bandit.patch preserve the earlier observed sources/delta.

Only the test changed. Nine selection cases passed again with exit0 (raw logs:
selection-after-bandit.stdout.log and selection-after-bandit.stderr.log). The
manifest/patch now describe this newly observed test version. Production scanner
selection and catalog hashes did not change; earlier real execution is not
represented as reexecution against this new test input. Final scanner rerun is
assigned to the coordinator. No implementation process remains active.
