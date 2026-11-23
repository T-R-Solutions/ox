# Bounded audit succession — 2026-11-17

The maintainer requested analysis of the supplied audit and correction of grounded
findings. This material integrity/gate subtask follows the existing high-profile
coordination and independent review/validation route. It repairs the documented
108 displaced-snapshot link failures and five preexisting current-content failures,
then authenticates the exact documentary/skill corrections produced by this audit.
It does not renew historical evidence or accept current product behavior.

## Decisions and scope

D-S01 / R-S01: retain every historical registry and captured Markdown byte-for-byte.
Add a separately pinned 46-destination successor registry, a pinned 20-source origin
registry and one exact project intermediate bridge. Only the literal inventories
in `tools/governance/scripts/audit_revision.py` can match. Old registries continue
to authenticate independently. Unknown buffers never normalize; changed terminals,
missing/tampered registries or snapshots, symlinks and downgrades fail current checks.
No Markdown directory is excluded. New unknown Markdown uses ordinary validation.

D-S02 / R-S02: normalize the new audited terminal before the existing Windows,
visual-skill, OSV, historical-link and older preservation stages. Each new preimage
is retained as `.bin` and bound by SHA-256. The two already-drifted baseline paths
use recovered older terminals, authenticated by the existing pinned hashes, rather
than treating the audit's starting bytes as an approved predecessor.

D-S03 / R-S03: origin records identify each captured source and its original path.
They resolve relative links from the original location and retain the previous
origin-registry digest. Every one of the 20 sources is mandatory. Governance-copy
exceptions remain limited to individually pinned absent application/product targets,
using the existing declared-copy receipt and product boundary. Checkout consumers
require actual origin files; missing product paths do not infer copy mode. No
source allowlist or product capability is added to the governance distribution.
The retained workbench preimage duplicates already distributed historical prose;
its live product feature remains excluded from governance copies.

Rejected: replacing old hashes, moving/deleting Markdown snapshots, excluding
validation directories, permitting arbitrary successor paths, silently accepting
missing new registries, reclassifying unknown content as a historical version,
or claiming old observation hashes describe newly executed checks.

Owner: governance implementer owns audit_revision.py, bounded hooks in Windows/
OSV/log-repair revision modules, new adversarial test and the affected historical
origin-count assertion. Coordinator/reviewer/validator retain independent contexts.
No product source, evidence envelope or original registry is edited by this subtask.

## Recovery and authentication

The initial tree includes dirty/untracked work. Starting content identities are
in `/tmp/ox-audit-correction-base/hashes.json` and its full Git diff. Thirty tracked
preimages were reconstructed from HEAD plus that captured diff in a separate local
directory and checked against those initial content hashes. Additional preimages
came from the independent writers' before directories, including the approved
17-skill patch's `before` directory. New pinned snapshots live below
`docs/validation/audit-correction-20261117/before/`; no historical snapshot changed.

The baseline project had two missing documentary transitions:

1. The pinned Windows terminal `6e6c2738...` was recovered as an exact 38,271-byte
   prefix of the observed starting project file (38,889 bytes). Its existing
   reverse edit reconstructs the pinned Windows predecessor `97f5a391...`.
2. That predecessor already contained extra later authorizations beyond the pinned
   OSV terminal. The OSV terminal `7ecff339...` was recovered by combining the
   unchanged OSV predecessor snapshot with the OSV authorization block retained in
   the later project. Its SHA-256 exactly matches the immutable OSV registry.
   The new intermediate bridge maps only `97f5a391...` to those `7ecff339...` bytes,
   and only while the independently authenticated new live terminal is present.

The workbench convergence terminal `91981cc1...` was recovered as the exact first
4,108 bytes of the audit's starting convergence file. Later prose remains preserved
in original envelopes/snapshots and current feature documentation. None of these
recoveries changes the hashes or results of historical observations.

The origin sources are exactly the ten Markdown files each under
`desktop-navigation-20261117/before/` and `enterprise-visual-20261116/before/`.
New origin capture authenticates the currently reviewed snapshot bytes; it does
not prove a historical target's contents or the time of its original creation.

## Verification and limits

The initial six-test suite passed after final writer stabilization. It challenges all
registered reconstructions, independent pinned project/convergence hashes, unknown
buffers, live mutation, missing files, symlinks including an ancestor, preimage and
registry tampering, duplicate JSON keys, invalid scope/schema and the intermediate
bridge's live-terminal prerequisite. Existing Windows successor suite: five tests
passed. The affected historical-origin count test passed with 41 total origins;
its original 21 records and 12 excluded targets retain their previous assertions.

Early runs during writer activity failed on exactly the changed pinned paths;
a missing Windows-registry test fixture was corrected. These failed runs are not
reported as passing observations. The first historical suite run also found the
outdated aggregate count of 21; the corrected test preserves the old subset and
accounts for exactly 20 additions. Its long public-copy portion was interrupted
with exit 130 to avoid redundant full checker invocations. No complete historical
suite pass is claimed.

The final root checker returned exit 0 on the stabilized registry and inputs;
the coordinator also reports a separately observed independent validator pass.
The first final isolated governance-copy check returned exit 1 solely for the two
existing DESIGN product references. Its old exception pinned raw DESIGN bytes
`864f769e...`, while even this audit's initial DESIGN was `fd7b5999...`.
The bounded helper successor in readme_revision.py retains exactly those two
targets and requires the explicit governance-copy receipt, pinned audit registry
and exact current DESIGN hash. It adds no target exemption. A seventh adversarial
test confirms the two intended references and rejects a new target, changed DESIGN
and absence of the receipt; all seven new tests now pass (exit 0, 4.97 seconds).

The complete copy was produced by the existing distribution function at
`/tmp/ox-audit-final-copy-20261117`. After the first failure only the corrected
readme_revision.py was copied over, verified byte-for-byte equal to the root source:
SHA-256 `257888da876617b8d84f04e1a6f29788948e9c41aaf79c955dbb710c8eff6b16`.
The final isolated checker returned exit 0:
`PASS: local profile, catalog, bridges, skill copies, SDD, normative IDs, links and archive/content inspection. No product acceptance.`
The isolated runner denies
access to the source checkout; the copy retains the existing explicit receipt and
excludes the application and live product records. No full scanner run,
download, commit, publication or central maintenance was performed.

Documentation disposition: this record explains the new exact-content successor,
origin and intermediate-bridge contracts. Existing history/ADRs remain immutable;
`succession.json`, `succession-origins.json`, `succession-project-bridge.json` and
all new `.bin` preimages describe only this bounded correction. Independent review
and validation remain necessary; successful structural checking is not acceptance
of the 46 destinations' product/skill semantics.

Commands actually executed for the final relevant observations:

| Command / method | Result |
| --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools/governance/tests -p test_audit_revision.py -v` | Seven tests PASS, exit 0. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools/governance/tests -p test_windows_design_revision.py -v` | Five tests PASS, exit 0. |
| `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tools/governance/tests python3 -m unittest test_historical_link_resolution.HistoricalLinkTests.test_all_five_reviewed_locations_and_unlisted_identity -v` | One test PASS, exit 0; original subset assertions preserved. |
| `PYTHONDONTWRITEBYTECODE=1 python3 tools/governance/scripts/check-ox.py` | Final root check PASS, exit 0. |
| `copy_distribution(root, destination)` followed from destination by `python3 tools/governance/scripts/isolated-run.py <source-root> tools/governance/scripts/check-ox.py` | First attempt exit 1 on exactly two DESIGN links; corrected helper copied with exact byte comparison; final isolated attempt PASS, exit 0. Original outputs retained in `/tmp/ox-audit-final-copy-check.txt` and `/tmp/ox-audit-final-copy-check-successor.txt`. |

Pinned new registry identities:

- succession.json: `fc5127b589f98df748aef6caa01fc392fae8649ccb8378b4a6216a6461085709`
- succession-origins.json: `6df31f101bcf69e4e42a909073d0d0e5ace852b1241f068c8c520e80e487e697`
- succession-project-bridge.json: `74e2ae057055b9c9196f74e657c317307f581ee9b32a8c22edd41309e4528f0e`

All local verification processes started by this implementer are finished; the
redundant historical public suite was explicitly interrupted as recorded above.

Final implementation/test input identities (dirty working bytes included):

- `tools/governance/scripts/audit_revision.py`: `330c9f17d54e47389cdcbf67a12f7c28f20b955405268bfe6e0f7f7a97767aef`
- `tools/governance/scripts/windows_design_revision.py`: `918f504571fa512d2a07d9bd7e1414605680defd1ba492b00a4b7c9f0fd73398`
- `tools/governance/scripts/osv_acquisition_revision.py`: `a5ed050dfb94f4a00c0b6e70961feaf996eba1fc8704f7d5815ba91a80b74020`
- `tools/governance/scripts/log_repair_revision.py`: `0f20858c3f279da81f7026b6b46e956b447e03b8bad9bfb297cc083673d3d38d`
- `tools/governance/scripts/readme_revision.py`: `257888da876617b8d84f04e1a6f29788948e9c41aaf79c955dbb710c8eff6b16`
- `tools/governance/tests/test_audit_revision.py`: `91990d3a5ccfc85c226692b3207d31d22bd68a763c1bbdae8d38faba600e23ec`
- `tools/governance/tests/test_historical_link_resolution.py`: `df449b9c54ff6ead2f2e2a3ad1fc076a077c404597ed57b3bac3db1f4db0cc65`
