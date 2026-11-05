# Controlled foundation threat/control review

Owner: maintainer for scope/exceptions; executor for observations. Target: Linux
x86_64, trusted local fixtures, local filesystem, no remote providers/credentials,
no product sandbox or descendant containment. Existing APIs are not a public SDK.

| Asset / actor and threat | Permitted effect / control | Independent observation | Residual risk / revisit |
|---|---|---|---|
| Workspace files; user or fixture accidentally overwrites prior content | Controller canonicalizes existing directory, exclusive new attempt directory and create_new request; task owns only its attempt output | local_task real_result_identity_history_invalidation_and_preservation checks sentinel bytes; inaccessible workspace rejection precedes attempt increment | Not protection from noncooperating same-user writers, symlink replacement after validation or arbitrary executable code; re-evaluate with real agents |
| Host grant; peer advertises unsupported capability or caller denies | Both advertisement and caller grant required before CALL | incompatible_and_unauthorized fixture exits 21 on any CALL; successful shutdown proves denied call absent. Grant-bypass mutant rejected | Direct tools of hostile plugin bypass host API; no OS confinement claim |
| Protocol state; malformed/oversized/mismatched data | ASCII frame <=1024 bytes, version 1.0, matching request ID/token; terminal Failed on admitted-call error | host malformed/oversized/mismatch, incompatible, timeout/crash cases; cancel test observes /proc PID absence then socket directory removal | Host calls serialize through &mut self; shared reference isn't a multi-tenant scheduler. Startup/shutdown each have phase budgets, not global API wall time |
| Owned processes/resources; user cancels running work | Runtime kill followed by poll/wait; verifier cancel flag propagated from UI; host exchange checks token, reaps before return | readiness-marker cancellation regressions fail against old behavior; new tests assert terminal Cancelled and PID absent | Direct children only; blocking filesystem capture and OS reap do not have a hard total deadline; forced app kill is not graceful cleanup |
| Acceptance; stale/duplicate events or claims masquerade as evidence | Attempt/generation and sequence checks; independent literal/identity oracles; immutable before/after snapshots | runtime ordering, UI stale/duplicate test; verifier contradictory/current/changed-input tests; stale-input and late-ui mutants rejected | Declared inputs only; no inference that all external dependencies were declared; no continuous watcher |
| Volatile evidence and resource exhaustion | <=128 MiB retained before+after payload, conservative pre-launch reservation, no eviction; <=32 observations; <=8 declared paths; <=16 MiB/file and <=32 MiB/capture; missing/oversize/history overflow cannot launch/approve | verifier-limits tests: 33rd run refused and marker absent; new Engine has no approval; nine-input/oversize capture refused | The pre-fix stress run measured 1,997,060 KiB RSS. The adopted content-budget fix measured 164,576 / 164,640 / 160,792 KiB across three runs, below the adopted 256 MiB RSS corpus limit. Payload budget is not a universal heap cap; transient capture and OS allocation remain separate. See history-summary.json |
| Dependencies/native system; unsafe implementation or unmaintained code | Own crates forbid unsafe; exact lockfile/target; no arbitrary dependency promotion | target metadata 170 package records (16 first-party), 21 RustSec package-name candidates, numeric version review; 20 patched/unaffected, one owner exception | 102 package versions have lexical unsafe occurrences; not reachability/soundness proof. 23 build-script/native-boundary entries; dynamic system libraries not pinned by lockfile |

Dependency evidence: cargo-metadata.json, dependency-inventory.json,
dependency-boundaries.json, license-files.json, rustsec-candidates.json and
rustsec-review.json. Public RustSec archive identity is retained; no source upload.
Metadata was filtered to actual target after an all-platform offline query required
uncached Android sources. Platform expansion is explicitly outside adopted F0.

License review: every target package has a declared expression; own GPL-3.0-only
is governed by root LICENSE/NOTICE. Ten Iced subcrates do not bundle a license file
in their cached crate directory; their declared MIT license and Iced repository
lineage need packaging confirmation before distribution. No public redistribution
clearance is claimed. Other package expressions include MIT, Apache-2.0, BSD, ISC,
Zlib, Unicode-3.0 and LLVM exceptions; exact per-package declarations/files are
recorded. The original copied-governance-material rights blocker remains outside
this local F0 delivery and blocks publication. SPDX inventory is not a legal opinion.

The maintainer expressly accepted the temporary F0-only ttf-parser 0.25.1
unmaintained notice (RUSTSEC-2026-0192): review at next monthly cycle and before
public distribution/untrusted fonts. This is not dismissal of a demonstrated exploit.
No version or native dependency changed in this task.
