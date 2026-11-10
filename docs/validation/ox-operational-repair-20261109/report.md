# Ox operational repair — 2026-11-09

Result: **APPROVED for FULL-01**, complete public full-scope verification.
`run-1QqSPPDE` exited **0**; **16/16 checks passed**, without findings, failed,
blocked or error states. Full output is retained in the original run and the
selected streams beside this report. The prior `run-MFlZVl5M` failed only its
nine governance cases; its other 15 checks passed. That failure is preserved.

## Authorization and method

Maintainer requested restoring Ox without breaking Ec, following the pending
repository-wide commit request including visible untracked files and the existing
`sim` full-verification choice. Root is /home/rodrigo/Projetos/ox. Full workflow
extends scripts-toolbox-native T027 and D-27/D-28; project authorization and actual
skill/bridge contributions are recorded in plan.md. Ec and Shared Toolbox source
were read only. No global installation, dependency version change, SELinux policy
disable, image substitution, publication or destructive history rewrite occurred.

```bash
TOOLBOX_BIN=/home/rodrigo/Projetos/dev_audit/shared-toolbox/bin/toolbox \
TOOLBOX_SELINUX_LABEL=shared \
CARGO_HOME="$PWD/.local/cargo-home" \
  bash scripts/automate.sh --scope full
```

The escalated run permits normal central execution records and explicitly selected
shared relabel on dedicated mounts. It does not grant blanket host write access
inside scanners. The portable wrapper still preserves caller-controlled selection.
Cargo preparation was separate: reviewed archives/current cache copied to a
checkout-local cache, then locked Cargo fetch acquired missing packages. Checks
remain locked/offline; global Cargo state and lockfile were not modified by prep.

## Observations and corrections

| Surface | Correction / observed result |
| --- | --- |
| Scanner access | SELinux enforcing plus unset selection had denied configuration reads. Shared explicitly selected; all mandatory native scanners now executed and passed, with version/image/cleanup diagnostics. |
| Cargo | Dedicated persistent .local/cargo-home supplies exact locked sources. fmt/check/build/test/clippy and Deny pass offline. |
| Portable SDD | Six repository evidence links replaced by explicit prose paths; the standalone model boundary was preserved. |
| Documentary succession | Exact-content terminal registry/preimages authenticate current project and AGENTS bytes. Partial test fixtures now include the whole chain. Unknown bytes and downgrades remain rejected. |
| Stale evidence | Changed-input observations retained verbatim in historical_evidence plus before/ bytes, dependent decided states made INCONCLUSIVE; no old approval renewed by hash replacement. |
| Governance distribution | dependency-hygiene depends on Cargo.lock, so governance-only exports omit it alongside other product-dependent records. It stays at its existing path and in complete-checkout checks. Independent copy/corruption tests pass. |
| Obsolete test callers | Grype test uses native_command/check_properties; OSV expects the current metadata diagnostic. No runtime fallback restored. |
| Static checks | Unsafe rule fixtures remain .py.txt/.rs.txt data. Native Bandit occurrence baseline and exact-path Ruff false-positive dispositions are guarded by source/policy SHA-256. Changed/missing review inputs block; no global rule/severity suppression or vulnerability waiver. Details in static-review.md. |

Final governance/automation suite: **139 tests in 1176.800 seconds**, no failures
or errors, one explicit real-Docker unit opt-in skipped. This skip does not replace
the mandatory real native checks in the full run. Rust tests passed; six graphical
opt-outs retain their dedicated protocol and are not claimed executed here.
Gitleaks, OSV, Opengrep, Audit, Bandit, Machete, Ruff and Deny all passed.
Existing two-ID advisory dispositions and exact dependency/version policy remain.

Independent controls: 32 script cases passed (one opt-in skipped); four native
succession and fourteen project tests passed; independent-copy/corruption test
passed in 398.588 seconds. New source/policy mutations and missing review registry
blocked. Real Ruff detected one new F821 in an unreviewed disposable source; real
Opengrep detected the 23 deliberately unsafe examples copied to .py/.rs. Fixture
bytes and rules are unchanged by the later copy-boundary/test-fixture corrections.

## Inputs, preservation and limits

observed-inputs.json records 7,603 visible changed/untracked paths and SHA-256;
all were compared again after the successful run with **zero content drift**.
This report and copied execution artifacts were added after that comparison; they
are evidence, not executable inputs relabeled as tested. artifact-manifest.json
binds retained results and streams to original run paths, sizes and hashes.
acceptance.json records criterion/method/observed result/inputs/limits. Original
snapshots/native reports remain under .local/checks. before/ preserves edited
preimages, including the full earlier evidence documents. No product source was
changed by this repair and no previous graphical/storage acceptance was renewed.

Commit safety review found only the two documented synthetic AWS fixtures, no
private-key/GitHub-token pattern, and no escaping/absolute member paths in 159
archives. The one retained ELF oracle.bin is byte-identical to /usr/bin/true
(SHA-256 08f38829911197c3d3c42b8339276b986eea4b7f9d95a13496ba09ee8e26b71b);
it was not executed. These bounded inspections are not a universal secret audit
or third-party redistribution/license approval. Existing licensing gaps remain
explicit. Generated local cache/runtime data remain ignored.

The pending local commits may proceed under the successful full-gate choice.
Git history records their hashes and scopes; committing is not product acceptance.
