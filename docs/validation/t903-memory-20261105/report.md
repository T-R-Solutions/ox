# T903 memory correction and current-input acceptance

T903 COMPLETE; current F0 APPROVED. Historical F0 approval remains tied to its original inputs. This successor accepts only the final sources identified in product-inputs.json, environment.json, per-run binary identities and instrumentation/. No persistence, commit, staging, publication, dependency upgrade, global installation or remote agent occurred.

## Authority and protocol

Full route reuses product-f0-gate, product-local-task-ui and product-verification-engine. Read AGENTS/project/constitution/architecture/workflow/evidence, F0 boundary, robustness and T903 reports/artifacts, graphical resumption contract/matrix/successors, affected specs/plans/tasks/convergence/trace/evidence and actual callers. preimage comparison confirms all77 inherited product inputs byte-identical at resumption. Preserve all existing dirty work; own production change is Engine representation/capture and regression tests. Existing newline-preserving desktop correction is retained unchanged. plan.md was recorded before new trials; feature plans link it and record actual skill selection (performance primary, Rust/Iced supporting, unversioned entries/bridge1). No delegation.

64MiB applies: the adopted decision-proposal.md defines GUI RSS during bounded task/history interaction and excludes the separately adopted large-history corpus. That exception is the fixed renderer-free two15MiB corpus, not any GUI that happens to retain32 observations. Thus the earlier90.63–133.69MiB observations reject the existing GUI budget; no missing maintainer decision or256MiB transfer is needed. Neither corpus, limit, profile nor renderer was relaxed.

Before trials: GUI maximum response120ms; client draw through present-call return125ms; sampled RSS64MiB; three10s idle windows<=5% one core. Per-cell3 warmups+20 measured responses, all raw draws reviewed including startup/history;20ms sampling plus lifetime HWM. Twelve cells: X11/native Wayland ×100/150/200% ×640x480/900x700 logical. CPU tick100Hz, asynchronous compositor capture and20ms polling limit resolution. Captured pixels are not physical scanout. Backend3+20 uses50/50ms execution/verification,100ms cancel-to-observed direct exit and32MiB direct-harness RSS. Large renderer-free corpus: two15MiB inputs,128MiB logical retained budget/reservation, refusal before effects,256MiB RSS over3 runs.

## Diagnosis and correction

Equivalent200%900x700 native32-observation reproduction: baseline133.875MiB RSS,61,218,816 logical bytes and67,125,248 bytes of actual Vec capacity. Whole-snapshot Arc sharing reduced unique capacity to1,048,832 bytes, same logical payload and32 observations, but RSS85.918MiB still REJECTED. Retaining UI layout experimentally gave85.480MiB; rejected as insufficient benefit and removed. Source/result of that discarded candidate remain stable-layout-desktop.rs.bin and stable-native-2-900/.

Disposable C preload allocation probe is diagnostic tooling only, never an Ox dependency or product unsafe code. Raw allocation/free addresses, maps, symbol-resolved live-analysis.json and smaps are retained under allocation*-native-2-900/. >=256byte tracker observed12,297,157 live bytes at32: about3.43MiB ShapeGlyph/LayoutGlyph,1MiB capture capacity,2.40MiB renderer mask,2.80MiB decoration pixmaps plus other caches/spans. >=16KiB probe is separately retained. Small allocations, mmap/shared surfaces and allocator reserve are outside those totals. Profile probes alter timing and are excluded from acceptance. smaps separates shared surfaces (~25MiB in native200%) from anonymous pages: candidate46,232KiB versus final-stream15,008KiB. Numerous ~1.5MiB anonymous mapped regions explain why live payload and RSS differ; exact allocator-internal classification is not claimed.

Final Engine uses private Arc<Vec<Content>> and exact path/byte equality to share immutable whole captures; public Content.bytes Vec and inputs()->&[Content] remain compatible. Every run/Check/result/before/after identity remains distinct. Capture first reads every current ordinary file in8192byte chunks against a retained snapshot; only complete equal content reuses ownership. A mismatch performs ordinary bounded fresh capture; changed length/chunk-edge/suffix are tested. No metadata/hash/pointer freshness shortcut. Known capture comes from the same Engine, preserving per-file/count/capture bounds. Admission still sums logical before+after bytes for every observation and reserves maximum post-capture before launching; physical dedup never expands that budget. Missing/special/FIFO remain non-approval. Original file-open/reap safeguards are unchanged.

Final stream reproduction55.141MiB, then twelve accepted history cells corroborate the result; final native200%900 is55.484MiB. Transient capture elimination, rather than ownership sharing alone, accounts for the additional measured improvement. New tests exercise immutable clone access,32-count admission, changed lengths/chunk boundaries and recovery; existing128MiB fail-before-effect, selective invalidation, contradictions/five states, FIFO and owned-process cleanup regressions pass.

## Final twelve-cell full-count comparison

Before values come from unchanged-input predecessor current-history-checks.json (77/77 preimages matched), not new executions on modified sources. After values are all observed maxima; no favorable repetition selection. Full-flow small-corpus matrix is separately accepted-flow-checks.json: max RSS52.121MiB, client draw69.267ms, response59.887ms. Old159.935ms draw failure and prior corrected74.384ms corpus remain historical.

| Backend-scale-width (height700/480) | Before RSS MiB | After HWM MiB | All-draw max ms | Response max ms | Idle max % one core |
| --- | ---: | ---: | ---: | ---: | ---: |
| native-1-900 | 95.34 | 34.67 | 63.824 | 7.803 | 0.000 |
| x11-1-900 | 91.77 | 31.92 | 64.528 | 58.794 | 0.000 |
| native-1-640 | 92.10 | 32.31 | 70.154 | 7.981 | 0.000 |
| x11-1-640 | 90.63 | 30.82 | 63.715 | 37.794 | 0.000 |
| native-1.5-900 | 124.32 | 45.77 | 74.346 | 14.326 | 0.000 |
| x11-1.5-900 | 114.18 | 35.90 | 66.231 | 66.535 | 0.000 |
| native-1.5-640 | 116.53 | 38.58 | 66.592 | 13.966 | 0.000 |
| x11-1.5-640 | 110.96 | 32.55 | 67.652 | 40.402 | 0.000 |
| native-2-900 | 133.69 | 55.48 | 68.392 | 19.970 | 0.000 |
| x11-2-900 | 119.34 | 41.11 | 69.845 | 68.027 | 0.000 |
| native-2-640 | 121.85 | 43.35 | 73.638 | 20.492 | 0.000 |
| x11-2-640 | 113.79 | 35.29 | 65.122 | 42.936 | 0.000 |

All12 final history cells retain32 observations and scroll to run32. Current sampled RSS and lifetime peak are separately available in result.json; tables conservatively use HWM. Large corpus three peaks[34.09765625, 33.12109375, 32.91015625]MiB, all<=256; still exactly2 observations and prelaunch refusal without eviction. Backend maxima execute/verify/runtime cancel/verification cancel[16.531497, 2.938875, 0.08254, 2.066793]ms; direct-harness RSS5.457MiB. Earlier batch backend/large commands did not explicitly rebuild examples, so their logs are retained but excluded; accepted-postflight build-examples and backend-accepted/large-accepted logs identify current executable inputs. The initial report parser incorrectly excluded three rows again, although the harness already suppresses warmups; its assertion failed and no report/binding was accepted. Corrected parsing retains all20 emitted rows(0..19) and verifies23 actual iteration directories; raw samples are unchanged.

## Functional observation and failures

Six native full journeys and42 explicit X11 graphical cases correlate real keyboard/pointer actions, focus/Shift+Tab, good/bad task artifact bytes, APPROVED/REJECTED/UNVERIFIED/INCONCLUSIVE rendered state, stale invalidation, history, responsive cancellation and natural exit. NotApplicable remains an explicit Engine API disposition, not a fabricated GUI-generated state. accepted-fifo-native/x11: own result replaced with actual FIFO without writer, Refresh yields UNVERIFIED, Verify explicit regular-file error, restored original fixture exposes retained history; sentinel/identity/logs/captures retained. accepted-held and accepted-held-x11 record live worker TIDs and owned oracle /proc state, responsive display, cancel, worker/direct-child disappearance, second held oracle and close. accepted-close-native/x11 record actual running task/worker, responsive rendered details, close and application/direct-child absence. accepted-original corroborates current uninstrumented product on native Wayland.

Visual review: full-history native200%900 bottom exposes run32 and complete wrapped records. Initial X11 full-history200%900 compositor capture clipped the rootful surface: preserve original run, classify display observation incomplete, no product fault inferred. Correct observer uses compositor2400x1800 scale1 and client WINIT_X11_SCALE_FACTOR (same convention as explicit X11 matrix); accepted-history-x11-2-900 is the successor. All accepted X11 history cells used corrected geometry. Actual requested backend confirmed by native protocol or own X-window/focus; per-run environment records isolate sessions. This does not establish main-session support. Additional captures are reviewed with their actions/artifacts/processes; screenshots alone are not the oracle.

Initial workspace test in restricted sandbox failed five Plugin Host Unix-socket tests with PermissionDenied; unrestricted repeat passed. Six ordinary ignored graphical tests are enumerated and executed separately (plus metric seventh case per X11 cell), not counted as ordinary-suite execution. Coverage current lines1011/1083, changed92/97; summary retains component gaps, excluded fixture/test/dependency lines and killed-child counter limits. Line reachability is not independent semantic correctness. Check/fmt/clippy and source binding checks recorded with results, not just agent declarations.

The first complete final-* matrix is preserved under its exact pre-lint input. Clippy then rejected collapsible_if; its equivalent let-chain correction changed both ELF identities. Before-lint sources/binaries were archived and the entire affected corpus was repeated as accepted-* (including Rust checks, all twelve full-flow and twelve full-count cells, FIFO/worker/close, original binary, backend, large-history and coverage). The earlier visible-history replay overlapped a lint rebuild and supplies no final resource acceptance. No prior binary result was relabeled current.

## Acceptance and limitations

Criterion-level successor is matrix.json: original requirement/authority/expected result retained, affected inputs reobserved through current tests/GUI/performance/coverage and unaffected source/lock/risk decisions selectively compared. Documentary AC01..04 retains existing scenario/decision preparation with scoped successor inspection; no persistence selection or experiment inferred. Historical evidence inputs resolve only through identical-byte preimages without digest renewal. Freshness/negative controls and governance results are checks.json and acceptance.json; these do not prove GUI effectiveness independently of raw observations.

No indispensable blocker remains in the adopted boundary. Session isolation, absent physical scanout, direct-child rather than universal descendant containment, cooperative cancellation rather than universal filesystem interruption remain limits of claims. Fixed fixtures/local ordinary files/identified host are the envelope. No durability/restart-safe storage, other host/OS/renderer, arbitrary-I/O deadline, main-session performance or universal flake rate is claimed. No new requirement was invented from those limits.


## Recorded final gates

The complete governance run in review-governance.log passed62 tests in698.378seconds, including independent-copy/archive/recovery and stale/missing/corrupt-input controls; no skips were reported. Its immutable run is docs/validation/runs/20261105T195043.359408Z/results.json. Review-stage structure, freshness, check-ox, maintenance and whitespace also passed. Closing changes only task/convergence/evidence/document metadata; the final scoped round rechecks structure/current bindings, check-ox, maintenance, whitespace and each of the three feature gates with changed-input/missing-evidence negative controls. It does not relabel the earlier62-test run as an execution on modified document bytes. Product inputs remain the same77 observed files.

[Clause decisions](matrix.json), [twelve-cell full-count measurements](accepted-history-checks.json), [full functional matrix](accepted-flow-checks.json), [backend and fixed large corpus](backend-checks.json), [visual/process correlations](visual-process-review.json), [raw artifact identities](execution-artifacts.json), [current integrity checks](checks.json) and [feature gate controls](acceptance.json).
