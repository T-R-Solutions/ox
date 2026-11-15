# Ec Cargo parity and portable configuration evidence — 2026-11-13

Authorized by the maintainer after read-only Ec comparison and the failed
`ox-run-toqdfXzz` complete run. Full-route extension: scripts-centralization T006,
AC-06/AC-07, D-07/D-08. Ec input identities are in ec-inputs.json.

## Implementation and scope

Follow Ec PATH-first Cargo-plugin discovery with a separate OX_CARGO_BIN fallback.
Reject an explicitly empty override. Adapter fixtures own their Cargo home and
plugin directory. Like Ec, Geiger uses all features and a configured 16 MiB thread
stack limited to its child process. Ox retains its installed pinned toolchain,
locked/offline commands, native binary identities, strict JSON omission checks
and traversal of every member. No Ec services, web/browser runners or product
license/advisory decisions are imported.

The previous cache-first capture test was updated to check Cargo-home fallback
with a controlled PATH. The new discovery test also checks PATH priority over an
available Cargo-home binary, explicit plugin-directory fallback and empty-override
rejection. A plugin already in PATH wins intentionally; selecting the prepared
Ox Geiger requires putting .cache/ox/cargo-home/bin first in PATH. No installed
binary is changed. Four modified test sources were reviewed against their previous
static exception bindings: static-source-review.json records the changes. No new
exception, severity reduction or Bandit baseline occurrence was introduced.

Keep scripts-centralization in governance exports. Each prior composite observation
bound 81 excluded inputs: 63 application files, 13 bytecode files, four
dependency-hygiene contracts and one cache registry. Prior evidence documents for
scripts-centralization and dependency-hygiene are retained byte-for-byte under
prior/, identified by prior-inputs.json. Changed composite observations become
INCONCLUSIVE; they are not hash-renewed. New portable script/configuration
observations support only AC-06/AC-07. The full-checkout product/dependency records
are not reapproved and no feature is hidden from the validator.

## Verification

Exact commands and results: checks.json. Source/configuration identities observed
after the test suite: tested-inputs.json. A later scripts/README.md clarification
is a documentary reexamination recorded in checks.json; code/configuration bytes
remain unchanged. Environment/tool identities: environment.json. Native assessment
inputs and exits: native-results.json and the three tool assessment JSONs. The
native observations are supplemental and keep their actual full-checkout inputs;
they are not converted into product acceptance or portable native reexecution.

| Criterion | Method and observed inputs | Result and limit |
| --- | --- | --- |
| AC-06 | Controlled Cargo discovery cases and complete scripts suite, with prepared CARGO_HOME inherited by the runner but private fixture tool/cache settings | APPROVED: 59 tests, one opt-in skip, exit 0; Geiger fixture asserts 16 MiB stack and all-features arguments. No fresh real Geiger measurement. |
| AC-07 | Seven focused governance checks including all five prior independent-copy failures; exported-feature input inspection; independent validator and changed/missing binding probes | APPROVED: all seven tests and both rejection probes passed; feature remains included, without application/cache/bytecode input bindings. |
| Supplemental linters | Final stable native ShellCheck, Ruff and Bandit through explicit maintainer Toolbox/shared selection | All native/classified exits 0, zero findings. No new full-scope or graphical acceptance. |

Initial failures remain observable: scripts-tests.before-contract-update.* retains
the intentionally superseded cache-first expectation; sandbox/ contains the denied
Toolbox operational-record attempts. native-before-final/ retains a Ruff run with
native zero findings but classified error because the source inventory changed
while the legacy test was being corrected. The final stable replay passed all
three linters. No failed observation is relabeled as successful.

Final current-evidence, independent-copy, freshness and root-governance results are
recorded in final-validation.json and its named logs. These checks validate the
final documentation/evidence state; they do not renew earlier operational results.

## Documentation disposition

Updated scripts/README.md and this feature's spec, plan, tasks, traceability and
current evidence. Updated dependency-hygiene current evidence only to invalidate
the affected composite bindings while retaining its exact predecessor. Reviewed
Ec scripts/README.md, docs/decisions/scripts-toolbox-native.md, docs/constitution.md,
docs/architecture/context.md, sdd/project.md, sdd/workflow.md and sdd/evidence.md.
Product architecture, Toolbox discovery/mount ownership, dependency versions,
licenses and GUI contracts are unchanged, so their authorities need no behavioral
revision. No Ec/shared-toolbox source edits, downloads, global installs, commits or
publication. Actual native tool execution was approved to write its normal Toolbox
operational records outside the filesystem sandbox.
