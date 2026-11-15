# Welcome UI implementation — T019

Owner: /root/welcome_ui. Written paths: application/crates/ox-ui/src/desktop.rs, desktop/views.rs, workbench.rs; additional exclusive assignment application/Cargo.toml by /root/welcome_coord (only Iced advanced feature). No project_store.rs edits. Shared documentation belongs to coordinator; native harness/captures belong to root. Other dirty/untracked edits preserved. Preimages and initial SHA256: /tmp/welcome-ui-preimages/inputs.json and sibling .bin files. Backend final SHA f54c0414d81c41301b89c81124660ca36276b5fe0fc86fb4830d5955b80ac6cf remains identical to backend report after formatting checks.

## Authorities and actual methods

Read AGENTS.md, docs/development/codex-agents.md, sdd/workflow.md, project.md, constitution, architecture context, visual-workbench ADR, DESIGN.md, surfaces.md, current feature spec/plan/tasks and preceding start-screen/folder-picker reports. Inspected actual supplied IntelliJ screenshot /tmp/pasted-image-.png. Adopted neutral entry hierarchy and grouped actions only; no copied assets/palette or invented project content.

Primary actually consulted: .codex/skills/iced-engineering/SKILL.md; bridge sdd/chain/iced-engineering.md version1; references/native-visual-contract.md and message-update-state.md. Contribution: explicit messages/worker ownership, stale replies, actual-layout focus scrolling and native capture handoff. Support actually consulted: .codex/skills/rust/SKILL.md; bridge sdd/chain/rust.md version1 and references/concurrency-and-safety.md. Contribution: owned channel results, cancellation atomics, worker isolation and focused offline/locked Rust checks. No entry declares semantic version; final hashes in /tmp/welcome-ui-inputs-final.json. No subdelegation.

Observed consumer: Rust edition2024, declared MSRV1.99, pinned1.99.1; Iced0.14.0 and cached iced_widget0.14.2. Existing std workers/oneshot retained; no new dependency/version or lockfile edit. Feature advanced enables the public widget Operation API, avoiding estimated row heights. A first compile caught private imports and then Id::new(String); corrected to advanced public API and Id::from(String) before passing checks.

## Behavior and decisions

- Dedicated S01/S02 neutral shell, discreet Ox+Configurações header, no rail/technical toolbar/footer. Content max1000px, intro/actions plus dominant recent list; stack at <=1024px. Plex/fonts/theme/density roles reused. Headings24/22 logicalpx.
- S01 Open folder + New project, optional current-session resume, secondary manual-path disclosure with persistent field label, actual wrapping name/path and remove per row. No fictional dates/status/projects. MRU is entirely backend-returned data.
- Initial history load runs from Iced initializer via dedicated worker. history_busy blocks open/create/remove/reset/load overlaps; busy blocks domain operations and subsequent history mutations. Replies carry serial; old/duplicate results ignored. Store IO never occurs in view.
- Open/create worker validates actual canonical UTF8 path through Controller before record. MRU failure is separate history_error and visible on destination Tasks as well as welcome. Successful project selection still opens; no task is executed. Store results never fabricate verification evidence.
- New project requires name and existing absolute parent in UI, previews full destination, states empty-directory consequence, and writes only after Criar e abrir. Parent picker changes only parent; never creates/opens. Cancel/Escape before confirmation creates nothing. Backend owns name/exclusive-create validation. A directory created before later failure/cancellation is retained with path/instruction, no rollback. Relative parent is a recoverable UI preflight error to keep complete preview possible without view IO.
- Reset is explicit and conditional: empty list; bounded known corrupted bytes are backed up; valid snapshot need not have backup; oversized/future format refused with original retained. Removal touches metadata only.
- Picker request/generation guards preserved; parent/open mode recorded at request. Navigation/close cancel picker. Project worker has own cancel flag; navigation/close prevents late automatic project navigation. Committed filesystem/history effects are not undone. Close waits for owned worker replies.
- Actual-layout RevealControl queries focused wrapper bounds and main viewport/translation, then scrolls the exact control into view. This supports variable-height paths/errors without hardcoded row estimates. Text fields retain native focus; buttons have explicit themed focus.

## Harness IDs and keyboard order

Welcome:272 Settings →273 Open folder →274 New project →[270 resume] →275 manual disclosure →[2 workspace input →3 Open path] →[280 retry →281 request reset →282 confirm reset →283 cancel reset] → recent rows [400+2*i open,401+2*i remove], i0..19. Controls absent/disabled during loading/busy are omitted; resume of an already-running task stays reachable. Header remains fixed; focused body wrapper IDs welcome-control-{id}; scrollable main.

Creation:272 Settings →290 project-name input →291 project-parent input →292 parent picker →293 Criar e abrir →294 Cancelar. Entry focuses name290. Input Enter does not confirm creation. Escape returns welcome before confirmation. Picker cancel returns273 on S01 or291 on S02; chosen parent focuses293. Command palette Ctrl+K and existing workbench keyboard remain available; settings uses existing preferences and navigation/command return.

## Focused verification

All commands from Ox root, offline/locked, CARGO_HOME="$PWD/.cache/ox/cargo-home". Final raw output /tmp/welcome-ui-cargo-test-final.log, /tmp/welcome-ui-clippy-final.log, /tmp/welcome-ui-build-final.log. Exact current input identities /tmp/welcome-ui-inputs-final.json.

1. cargo test --manifest-path application/Cargo.toml --offline --locked -p ox-ui: exit0.40 unit tests passed,0 failed,1 intentionally ignored subprocess helper; backend parent tests invoke helper as real child. Four local-task integrations passed (including real artifact/freshness/FIFO/cancellation/timeout) and one shell contract passed. No ignored integration cases.
2. cargo clippy --manifest-path application/Cargo.toml --offline --locked -p ox-ui --all-targets -- -D warnings: exit0.
3. cargo build --manifest-path application/Cargo.toml --offline --locked -p ox-app: exit0; current application/target/debug/ox ready for root native harness.
4. rustfmt --edition2024 --config skip_children=true --check [three owned Rust sources]: exit0. git diff --check on owned tracked paths: exit0. Untracked views/workbench are covered by formatting/compilation; tracked-only Git output is not full coverage.

New UI state tests cover: startup history serialization and stale/duplicate reply refusal; successful open with failed history still selecting Tasks; navigation while open suppresses late automatic navigation; no implicit creation on field edits/cancel/parent picker; creation failure reports retained destination; long-list tab order (20 rows); exact geometry reveal including translation; current-session/runtime preservation; inherited picker cancellation/duplicates/stale/errors and confirmation without task execution. Synthetic ProjectDone/HistoryDone messages test UI transitions, not the real store effect; backend filesystem tests and root native journey are separate oracles.

## Documentation disposition and remaining work

Reviewed DESIGN.md, surface contracts, feature spec/plan/tasks, architecture and existing start/folder reports. Shared docs require coordinator updates for real persisted MRU, creation effects, absolute parent preview, advanced feature, new tab order/cancel focus, conditional reset and task-only persistence wording. Sent concrete changes/commands to coordinator; this implementer edits no common docs/evidence/criteria. Status/footer/details now say task history remains session-only rather than denying all persistence. workbench.rs reflects real bounded S02/backend availability.

Native rendering/keyboard/picker/restart/create/removal/long-list/themes/narrow-size observations, independent source review and acceptance remain with root/coordinator and new independent contexts. No graphical acceptance, AT/X11/fractional-DPI/performance, crash/power-loss or full-product claim follows from state tests. No commit/publication/download/install/full scanners performed. Production writes stop after this report; available for bounded follow-up corrections.

