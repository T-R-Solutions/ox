# Pending skill criteria — execution review, 2026-11-01

All 28 previously pending observations now support APPROVED within their explicitly bounded consumer scopes. The nine skill features total **36/36 technical criteria and 54/54 criteria APPROVED**. The existing 26 approved requirement objects are unchanged. No original technical scenario, skill source or evaluation oracle document was relaxed. Prior envelopes/convergence bytes are preserved in previous/; failed executions are retained.

This is library-consumer acceptance, not completion or adoption of production Ox engines. All application files identified in the preceding technical-acceptance consumer snapshot remain byte-identical. Existing unrelated workspace changes were preserved. No commit or external publication occurred. AC-05/06 still refer to authoring and reexamined historical agent responses; no new agent trial was run.

| Skill | Newly executed criteria | Result and evidence |
| --- | --- | --- |
| Plugin protocol | AC-02, AC-04 | Frozen host rejection with persistent-state comparison and actual namespace read denial; replay/operations.log and replay/isolation.json |
| Agent runtime | AC-03 | Cancellation during both output streams, bounded retention, reaped child and joined readers; replay/operations.log |
| Autonomous verification | AC-04 | Actual loopback receiver rejects approved artifact without grant; permitted positive control writes; replay/operations.log |
| Workspace integrity | AC-01..04 | Traversal/symlink rejection, competing processes, crash/recovery and watcher/read reconciliation; replay/operations.log |
| Iced | AC-01..04 | Real heartbeat/interaction, retained content/focus, two actual window sizes, hidden relayout counters; gui-02/tests.log and reviewed PNG/PPM captures |
| Code context | AC-01..04 | Unicode byte ranges, actual rename/edit, ambiguity and missing-provider degradation; replay/models.log |
| Code knowledge graph | AC-01..04 | Validated source provenance, inference rejection, stale-edge removal and bounded cyclic/dense traversal; replay/models.log |
| Tool output | AC-01..04 | Actual command failure/location after long successful prefix, adversarial fallback, retained raw output and estimate/billing separation; replay/models.log |
| Usage accounting | AC-01..04 | Unknown price, idempotent replay, cache-subset totals and explicit timezone boundary; replay/models.log |

## Execution and corrections

The replay script rebuilt five binaries with Rust 1.99.1 and warnings denied: 16 model tests and seven process/filesystem tests passed. The isolated read oracle observed a readable baseline, a readable permitted mount, and two denied protected-path routes. replay/receipt.json captures exact commands, source identities and executable hashes. The graphical oracle passed its complete real-interaction flow after compiling against identified Iced 0.14/x11rb dependencies. Environment, exact GUI build commands, dependency snapshots and cached rlib identities are in environment.json.

The first graphical execution exposed a clipped Quit label at 240x180 and failed to exit. The actual correction uses four 52-pixel actions with a readable 14-pixel label, fitting the documented minimum width. gui-01 preserves failed source/oracle/log/pixels. gui-02 shows full labels at 240x180 and 1600x1000; actual Slow/Pane/Graph input works at both sizes and Quit exits from the minimum. The hidden relayout counter remained stable during controlled waits, while visible work increased it. This evidence does not claim universal responsiveness, accessibility or native Wayland behavior.

Other retained development failures identify a missing initial test executable/private-field compilation issue, process sandbox socket denial, reused PID-only temporary-directory names, and a missing output fixture mode. The accepted runner uses time+PID+counter directories and a separate concrete output fixture; it fails on any nonzero build/test command. Accepted results come from replay/, not those failed logs. Initial restricted-environment failures were followed by explicitly authorized local socket/namespace executions.

All 42 existing governance tests passed before final envelope reconciliation (governance-before.log, governance-timings.json). Their implementation bytes are unchanged. After the new 54-criterion envelopes, a separately copied package with source-tree access denied passed six methods: fresh SDD, SDD structure, check-ox, maintenance recovery, eight adversarial technical-gate tests and explicit 54-criterion acceptance. See export-before-finalization/receipt.json and its six logs. The final export is repeated after this review/envelope update; its receipt is intentionally generated after the copied package and is not claimed inside itself. Native/Rust tests ran on the local system, not inside the independent Python export check.

## Semantic review and limits

AC-01 of skill-consumer-validation: all 16 mapped cases exercise actual implementations with explicit expected fixture values and negative controls; scope is the synthetic grammar/provider contract described in tools/governance/consumers/README.md.
AC-02: actual OS processes/files/namespace boundaries execute the eight mapped original criteria; the publication receiver checks its own grant. Controlled failures do not prove arbitrary malicious-process containment, hostile concurrent filesystem-race safety, power-loss durability or production authentication.
AC-03: real XTEST interaction and focus queries, observed worker/heartbeat state and source-bound pixel review support the four scenarios at the two documented sizes. A concrete failed minimum-size layout was corrected and rerun. Graph work is a controlled layout routine, not a production graph renderer.
AC-04: compare retained predecessor hashes, the unchanged 26 approved requirement objects, original contracts and all 28 new reviews. Freshness/technical gates and independent export pass with concrete source/oracle roles. The former technical-acceptance 8/3/25 split remains a historical checkpoint, explicitly superseded by these new observations rather than silently rewritten.

Final skill consultation metadata adds the Iced review selection only; contract scenarios, implementation and oracle bytes are unchanged. The completed executions were reexamined against that documentation change; no rerun is attributed to it. Hashes detect changed inputs but cannot authenticate logs or establish general skill effectiveness. All larger product integrations and the unrelated historical UNVERIFIED features retain their own independent status.

The exhaustive per-criterion mapping, methods, observed results and boundaries are in matrix.json and the 28 individual *-AC-*.md reviews. Reproduction instructions and exclusions are in tools/governance/consumers/README.md.

Final input stabilization: rustfmt joined two lines in model_tests.rs without changing behavior. The exact previous source, reviews and envelopes are preserved in before-format/. All 16 model tests, seven process/filesystem tests, isolation controls and the complete graphical flow were rerun successfully with the stabilized file set: replay-final/ and gui-final/. This is a new observed execution, not a hash-only renewal. No original skill criterion or product source changed.

Final accepted observations are replay-final/ and gui-final/. Earlier replay/ and gui-02/ remain valid historical observations of the same scenarios. A new complete export follows this stabilization, recorded in verified-export/.
