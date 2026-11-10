# T011 pre-execution successor review

This review ends at preparation. Full route and scope were recorded before code in
sdd/project.md and the existing feature spec/plan. Entry-state.json and before/
preserve preexisting changes. No product source/manifest/lock was changed here.
Original review, successor review, logs, corpus and registry bytes remain preserved.
D1/D2/D4 retain their adopted dispositions; D3/D4-deps remain conditional; D5/D6
pending; product AC-01..07 UNVERIFIED. T009 and T011 remain open. F0 acceptance
remains within its original product-input envelope, without replaying GUI results.

| Criterion | Method / observed inputs | Result | Limit |
| --- | --- | --- | --- |
| Exact authority succession | Inspect skill_revision, readme_revision, governance_support and check-ox consumers; project-succession.json binds integration → entry → current, both preimages and succession-review.md | APPROVED for the registered transition; focused tests log; 56 final fast tests pass | Both transition digests and review digest are pinned in code; rewriting the registry digest for arbitrary current content is rejected. Content identity, not source authenticity or maintainer approval |
| Original and unknown-byte protection | Original integration registry retained; existing README preservation/visual chain retained; current/readme/project mutations, downgrade, malformed/duplicate records, wrong scope/digests, missing/corrupt preimage, direct/parent symlink and outside directory tests | APPROVED by diagnostic assertions in test_project_revision.py and existing regression cases | Finite adversarial suite; no general successor registration API |
| Neutral corpus / expected outcomes | verify.py and supplemental audit.py; M0/M1/M32/ML, payload identities, full shared-oracle invalidation maps, nine combined controls; inspect protocol, configuration.md, admission.json and case tables | APPROVED for preparation consistency only, logs/checks identify inputs | Synthetic exit17/timeout rows are history fixtures, not actual true outcomes; dispositions have no execution. M32 has 26 executions plus six dispositions. Admission boundaries are arithmetic, not admission trials |
| Linux dependency origin and applicability | Linux-filtered locked offline metadata; traverse normal/build edges from isolated root, propagate build role, no dev traversal; compare unfiltered metadata; verify registry archive digests | APPROVED for 159 applicable archives; 113 exclusions individually identified in linux-licenses.json | Cargo resolution is not actual native linking; system libraries/toolchain and embedded assets still require build attribution |
| Text/license completeness | Read source archives and recursively retain license/NOTICE/COPYING/copyright text, including third-party DRUID; compare declarations with licensing ADR | INCONCLUSIVE / BLOCKED: main MIT texts absent for ten applicable Iced subcrates listed in license-summary.json | No text invented or copied from another crate as proof. Local versioned archives lack these texts; no additional network acquisition authorized or attempted. Need verifiable upstream version/revision texts and attribution review. No legal clearance |
| Compatibility / notices | Per-component expressions, origins, versions, checksum, texts and obligation notes in linux-licenses.json; own material GPL-3.0-only | INCONCLUSIVE: alternative license branches and full attribution/compatibility review pending | Permissive expressions alone do not establish completeness; fonts/native components keep their terms. SQLite public-domain source header retained in parent native-source dossier, not inferred from wrapper MIT |
| Configuration / publication contract | Inspect configuration.md and source build overrides, compare correction in predecessor successor/review.md | APPROVED as obligations for future code | Effective PRAGMAs, lock behavior, sync calls/order and native flags are UNVERIFIED. Cross-directory generation rename requires sync of staging source and destination parents before acknowledgement; this corrective obligation succeeds abbreviated configuration prose |
| Global freshness | check-ox.py, global.log and checks-initial.json | REJECTED: affected evidence bindings still reference prior project/feature and governance bytes | The original integration-current failure is resolved. Historical evidence is preserved; no old hashes/results renewed. Exact stale records are listed in log; this review cannot promote their acceptance |
| Content freeze | freeze.json enumerates reviewed inputs, archive/text bytes and local resources; verify-freeze.py verifies all entries | Identified package with material blockers | No maintainer approval; no candidate/trial readiness claim; Git-only checkout is incomplete |

## License blockers and authorized recovery

Ten applicable main-text gaps: iced_core/debug/futures/graphics/program/renderer/
runtime 0.14.0, iced_tiny_skia 0.14.1, iced_widget 0.14.2 and iced_winit 0.14.1.
iced_core's DRUID_LICENSE is a separate third-party license, not its main MIT grant.
The sources' inherited workspace declarations and root iced LICENSE do not alone
establish the effective upstream subcrate notices. Obtain version-linked primary
repository/license evidence with a specifically bounded acquisition authorization,
or supplied verifiable source, then preserve this freeze and issue a reviewed successor.
No request here presumes continued network permission from the earlier Cargo fetch.
The 113 exclusions follow the exact Cargo graph, not platform names or a license gap.
Build dependencies remain included, even if not linked into the candidate binary.

## Reproduction boundary

Retain the complete files named by freeze.json, especially .local/build/persistence-
experiment-preflight-20261105/raw, dependencies, dependency-source and reviewed-crates.
Raw payloads and registry archives are required resources. Metadata records original
Cargo cache paths; offline re-resolution needs those packages made available to Cargo
from the retained checksum-verified archives/configuration. This is not a vendor-ready
Cargo installation or a Git-only self-contained runnable package. The freeze verifier
checks local file contents without compiling, executing fixtures or resolving network.
Any changed entry requires preserved successor, impact review and new identity.

## Concrete next authorization request (not granted)

After resolving the material preparation blockers and issuing a reviewed successor,
request: “Authorize implementing only the disposable SQLite and snapshot-v1 candidates,
independent effect/ack supervisor and shared experimental Iced worker/error shell,
using the exact freeze.json identity recorded in freeze.sha256 (or its explicitly
reviewed successor), under the adopted D2/D4 contract, solely in owned
.local/build/persistence-experiment-<run>/. No product integration or trials yet.”
The current package is reviewable but is not recommended for unconditional approval.
Maintainer approval is PENDING; no response is inferred from this document.

Before any separately authorized trials, observe environment, mount/free space,
toolchain, Cargo configuration and overrides, compiler/linker/flags and executable
identities; native SQLite version/source ID/compile options and effective PRAGMAs;
actual two-process lease; snapshot write/flush/sync/publication and both rename-parent
sync calls/error order; every fault barrier and external effect/ack counter. Defaults
are insufficient. Freeze those implementations and independent executables as new
inputs before execution. Real ENOSPC still needs explicit authorization for a bounded
disposable filesystem. D5 selection and D6 product integration remain separate.
