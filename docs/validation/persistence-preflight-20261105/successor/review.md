# T009 corrective successor review — 2026-11-05

Criterion: preparation is complete enough for pre-execution review, with independent
expectations, bound inputs, explicit gaps and no product acceptance. Result:
INCONCLUSIVE pending the dispositions below. This review supersedes the outstanding
items in the parent review only where explicitly examined. No encoders, builds,
trials, product modifications, network acquisition or real ENOSPC occurred here.
D1/D2/D4 remain adopted, D3 conditional, D5/D6 pending; AC-01..07 UNVERIFIED.

## Corpus and independence

Method: read the actual M0/M1/M32/ML, operation payloads, raw payload identities,
revalidation and expected cases, migration fixtures and current Engine capture/admission
code. Run the original verify.py unchanged and the supplementary audit.py. Independent
here means authored before either candidate, with no encoder/decoder used to derive
expectations. It does not imply a second human review or an executed reference engine.

The corpus bytes and earlier checks are unchanged. M1 means five state records (four
observations, one disposition); M32 means 26 observations and six dispositions.
The earlier protocol's V1..V5/O1..O5 observation shorthand is superseded by the explicit
kind fields: O5 persists an applicability disposition, never execution. T2 unfinished
intent has unknown effect/absent observation. Extra payloads for absent after captures
and dispositions are fixture resources, not retained execution evidence. No claim that
M32 saturates the Engine's 32 executed-observation capacity is made. Changing that
corpus requires explicit preserved successor/comparability review before either trial.

All C* share oracle.bin. An oracle mutation invalidates every C* including applicability
context; input, arguments, criterion and missing evidence mutations affect the designated
check. The new audit derives that set from executable_payload_id rather than trusting
affected_checks, then checks the whole expected map including unaffected controls.
The original four negative controls plus five supplemental ones cover dangling and
duplicate IDs, payload conflicts, empty rationale, oracle reference, provenance,
invalid state, fabricated disposition execution and duplicate acknowledgements.
These checks complement inspection; no finite suite proves all malformed data rejected.

The copied oracle binary is historical fixture data: exit17/timeout/missing-capture
rows are synthetic history, not outcomes produced by /usr/bin/true. The future effect
harness must implement controlled actual outcomes independently of this history;
never execute true and relabel its exit. The 54 E01..E08 variants define allowed cuts,
counters and errors, with 3 warmups/20 measured/10 fault repetitions and alternating
pair order. Candidate physical barrier maps and supervisor/effect binaries do not
exist; verify coverage of every applicable case/corpus before running, record explicit
inapplicability (e.g. no populated-history mutation in M0), never silently skip a cell.
Migration v0 is a header-only fixture conversion, v2 an unsupported sentinel. This
checks guards/equivalence, not complex schema migration or a historical Ox format.

## Admission distinct from experiment quotas

Source Engine sums logical before+after snapshots per observation, even shared Arc
bytes, plus the new before and maximum 32 MiB after reservation before effects.
Dispositions do not count as executions. ML raw input occurrences total 125829120;
logical retained with repeated oracle captures is 125985856. M32 logical retained is
1990880; M1 is 274400. Each observed prefix fits 128 MiB, files fit 16 MiB and captures
fit 32 MiB. These are manifest arithmetic, not observed Engine roundtrips.

The boundary vectors in admission.json are exact arithmetic; they are not materialized
bounded file fixtures or executed admission tests. A concrete future recipe for a
32 MiB capture with the current 39184-byte oracle is input lengths 16777216 and
16738032, plus oracle 39184. Retained 67108864 can be two logical 32 MiB snapshots;
retained +1 requires a separately constructed historical prefix. Freeze those histories
and verify refusal before effect with a counter before treating boundary/+1 as run
coverage. Deduplication never reduces logical charge. Physical store 1 GiB, run 4 GiB,
RSS 512 MiB and no eviction are separately adopted experimental limits, not substitutes
for this admission rule. No payload/corpus was changed to manufacture boundary coverage.

## Dependency, license and configuration review

Method: compare exact isolated Cargo.toml/lock and local Cargo metadata resolve nodes,
read versioned rusqlite/libsqlite3-sys source and bundled amalgamation. Retain resolved
features and registry checksums; snapshot local license texts by bytes. No remote
reference was newly consulted; earlier web observations remain historical.

Declared: rusqlite =0.41.1 default-features=false with bundled/backup; Iced =0.14.0
with explicit tiny-skia/X11/Wayland/font/thread-pool features. Resolved: rusqlite
backup,bundled,modern_sqlite; libsqlite3-sys 0.39.1 has bundled,bundled_bindings,cc,
default,min_sqlite_version_3_45_3,pkg-config,vcpkg. Thus disabling driver defaults does
not disable all transitive defaults. Full resolve is in resolved-features.json; the
272 registry entries include non-Linux target packages, not 272 observed linked libs.
SQLite 3.54.1/source ID and source flags are source declarations only. Native build,
compiler/linker commands, generated bindings, loaded version/source ID/compile options
and effective PRAGMAs are UNVERIFIED. No technology choice follows resolution.

libsqlite3-sys build.rs permits environment overrides (LIBSQLITE3_SYS_USE_PKG_CONFIG,
LIBSQLITE3_FLAGS, SQLITE_MAX_VARIABLE_NUMBER/EXPR_DEPTH/COLUMN, compiler CC/CFLAGS,
target-specific equivalents and bundling controls). Before a build, record Cargo
configuration, target, allowed environment, compiler/linker and command identities;
reject unreviewed overrides. Observe actual emitted native flags and loaded library;
source defaults cannot establish these values. Bundled native extension capability
exists; driver load_extension feature is absent. Runtime must leave loading disabled;
record enforcement/readback or an independently bounded negative query. FFI/native
code is a separate dependency risk under POL-01, not first-party Rust unsafe.

421 local license/notice texts from registry sources are retained as byte files;
licenses.json enumerates each exact expression/checksum/text identity and all missing
texts. Missing texts (including Iced subcrates and non-host platform crates) remain
UNVERIFIED for origin/notice completeness; a declaration alone is not legal clearance.
No network recovery is attempted. Before freezing a runnable package, resolve notices
for the actual target closure or explicitly exclude non-target components with target
metadata evidence. Before distribution, complete origin/compatibility/notice review
under the existing license ADR; no publication is authorized by this inventory.
MIT driver/native wrapper texts and SQLite's public-domain header are retained in the
parent source package. Font/native/platform components keep their separate notices.

The parent configuration.md is a design: safe writer lease, DELETE/FULL/FK ON/busy=0,
explicit transactions, no extension API, backup pinned cut, snapshot flush/sync/rename
and directory sync order. Backup convenience retry and default busy timeout cannot
replace fail-fast. Snapshot directory publication must observe sync of both source
staging and destination parents for cross-directory rename before acknowledging;
verify call/error order and all kill windows. No tested Rust lock/sync implementation
exists. Future backup/restore must validate full payloads and current inputs; PRAGMAs
and hashes alone cannot approve current state. Real ENOSPC remains separately gated.

## Documentary reconciliation and residual global failure

The global log identifies stale shared documents and changed persistence preparation
inputs. Preserve prior envelopes and redirect historical references only when an exact
preimage with the original digest exists. A new evidence record observes this delta;
it does not renew hashes in old observations or replay F0/T903 measurements. Compare
every other bound input unchanged before retaining its original scope. impact.json
records each replacement. Application edits present at entry remain untouched.

One independent failure cannot be corrected by documentary evidence: skill_revision.py
requires sdd/project.md to equal the exact README-integration registered bytes and
has no successor mechanism for that path. The authorized appended scope changes it.
Do not reset the project authority, change the historical registry, or loosen that
validator to obtain green. Keep the global gate failing on this identity condition;
a separately scoped exact successor mechanism with adversarial tests is needed.

## T009 completion criteria

T009 remains open. Resolve the registry successor failure within authorized governance
scope; disposition missing source/license notices for the runnable target; obtain
explicit review of this content-identified package and its corpus limitations. Freeze
any accepted successor before encoders. Build/runtime values, actual two-process lease,
snapshot calls, fault barriers, external counters, environment/free space and UI shell
require subsequent authorized implementation/observation, not documentary approval.
Execute critical comparison cases only after their prerequisites/permissions are met;
real ENOSPC needs its specific disposable-filesystem grant. No documentary/structural
pass closes T009, AC-01..07, D5 or D6. See checks.json for actual checks and failures.
