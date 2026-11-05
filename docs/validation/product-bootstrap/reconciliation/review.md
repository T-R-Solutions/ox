# Product-bootstrap acceptance reexamination — 2026-10-29

Method: compare all 13 Portuguese REQ/AC pairs in the retained pre-translation
specification with the current English specification, inspect the 16 crate contracts,
compare historical input digests, rerun Cargo 1.99.1 commands, and execute the X11
integration harness. This review does not transfer approvals by updating hashes.
The pre-translation evidence envelope remains in english-documentation/previous.
The immediately preceding English UNVERIFIED envelope is preserved separately.

All 13 acceptance statements retain the same actors, behavior and limits. No AC was
added, removed or weakened by translation. The later explicit reconciliation request
changes the toolchain policy from floating stable to pinned 1.99.1; that is a real
configuration change, not translation. The declared floor stays 1.99. Compiler
1.99.0 has not been tested and is not claimed as a demonstrated technical minimum.
Historical-input-comparison.json covers 59 application inputs: 58 identical,
rust-toolchain.toml changed. Thus old behavioral evidence remains historical and
fresh Cargo/GUI execution is used for this acceptance.

Environment: Linux x86_64, Rust/Cargo 1.99.1, X11 through the available XWayland
session, tiny-skia. Exact compiler identity, display and Python version are in
environment.json. Logs retain failed observations as well as successful ones.

| AC / requirement | Semantic comparison and historical observation | Current method and relevant observed inputs | Decision and limit |
| --- | --- | --- | --- |
| AC-01 / REQ-01 | Workspace virtual, 16 crates and one lockfile unchanged; E-STRUCTURE-LAYOUT / E-CHECK-LAYOUT | Locked cargo check, metadata and adapted structural oracle; all manifests, lockfile, pinned toolchain and source roots | APPROVED: 16 members compile, one lockfile; warm local build, no clean-room build claim |
| AC-02 / REQ-02 | Window opens, details interaction, button/native closing unchanged; old E-GUI-LAYOUT passed | New desktop.log and collapsed.png; unchanged desktop.rs and harness, pinned toolchain, environment | INCONCLUSIVE: native close passed; window rendered, but toggle timed out after 15s despite pointer position (80,130). Button exit was not reached. No current approval based on old pixels or pure state tests |
| AC-03 / REQ-03 | Binary delegates to library unchanged; E-REVIEW-LAYOUT / E-TEST-LAYOUT | Read main.rs -> ox_app::run -> startup -> ox_ui::run; regular startup test executed | APPROVED for delegation and propagated initialization failure, not graphical interaction |
| AC-04 / REQ-04 | All first-party roots prohibit unsafe; dependencies separate, unchanged; E-STRUCTURE-LAYOUT / E-DEPS-LAYOUT | Structural oracle reads every library/binary root; Cargo enforces inherited forbid; compare dependency manifests and lockfile | APPROVED for scoped prohibition/review. 154 historical dependency manifest digests match; reuse manifest-level unsafe/FFI inventory only, not a full security audit |
| AC-05 / REQ-05 | External modules without mod.rs unchanged; E-STRUCTURE-LAYOUT | Structural oracle scans crate sources, and compiler resolves modules | APPROVED: no mod.rs, external modules present |
| AC-06 / REQ-06 | Unit and external test discovery/execution unchanged; E-TEST-LAYOUT / E-DISCOVERY-LAYOUT / E-GUI-LAYOUT | New test.log, discovery.log and desktop.log; unchanged Rust test sources and pinned toolchain | INCONCLUSIVE for full previous acceptance scope: 9 tests discovered, 7 regular passed, 2 graphical explicitly executed, one failed. Discovery and regular tests individually pass |
| AC-07 / REQ-07 | Acyclic graph and UI/domain separation unchanged; E-STRUCTURE-LAYOUT / E-CHECK-LAYOUT / E-REVIEW-LAYOUT | Cargo metadata + graph traversal in structural oracle; dependency edges from current manifests | APPROVED: app -> ui, ui -> iced; domain crates do not depend on composition/UI |
| AC-08 / REQ-08 | Distinct identities, UUID v7 only for global persistent entities unchanged; E-REVIEW-LAYOUT / E-TEST-LAYOUT | Read WorkspaceRoot(PathBuf), NodeKey(String), plugin name/version; execute root_contract and inspect manifests | APPROVED: distinct types; no global persistent entity/UUID consumer. This is not a test of future UUID generation |
| AC-09 / REQ-09 | Evidence binds actual inputs/results unchanged; E-SDD-LAYOUT / E-REVIEW-LAYOUT | Retained historical envelope, current per-criterion decision and schema-2 bindings; run SDD freshness checker | APPROVED for provenance/checkable local hashes, not independent authentication of observations; graphical gap is explicit |
| AC-10 / REQ-10 | Governance checkers operational unchanged; E-GOV-LAYOUT | Run check-ox, verify-maintenance, complete test groups and SDD with current profile/scripts/fixtures | APPROVED when linked logs pass; these observations prove no Rust runtime behavior |
| AC-11 / REQ-11 | Versioned plugin contract; IPC/sandbox unavailable unchanged; E-REVIEW-LAYOUT / E-TEST-LAYOUT | Read ProtocolVersion/PluginDescriptor/HostError, execute compatibility test | APPROVED: equal major and sufficient minor, negative incompatibility exercised; no host/transport/sandbox claim |
| AC-12 / REQ-12 | Product excluded from governance distribution unchanged; E-GOV-LAYOUT / E-REVIEW-LAYOUT | Allowlist/package regression tests and independently extracted governance package | APPROVED for actual exclusion and governance-only receipt; no application distribution tested |
| AC-13 / REQ-13 | 16 useful contracts, future capabilities unavailable unchanged; E-REVIEW-LAYOUT / E-CHECK-LAYOUT / E-GUI-LAYOUT | Read all 16 modules; locked compilation; static desktop view and current collapsed window | APPROVED for bounded contracts/unavailability, not interaction: no process adapter, persistence, plugin host, index or graph engine is exposed as working |

Contract inspection: core availability is distinct from authorization; agent exposes
session/capability/error types only; policy defaults to ApprovalRequired; task rejects
invalid transitions without losing state; workspace wraps absolute lexical paths,
not confinement. Storage reports unavailable; context uses nonzero limit and snapshot;
graph distinguishes verified/inferred; output retains raw bytes/termination/losses;
verification retains all five states; observability distinguishes unknown and measured;
SDD and skills model portable references without executing them. UI is the sole shell.

Dependency reuse justification: dependency-comparison.json compares every one of the
154 manifests in the historical review; Cargo.lock and dependency declarations are
unchanged. Reuse is limited to the previous manifest/unsafe-token/native-file inventory.
Full offline metadata across every platform encountered uncached android-activity;
Linux-filtered offline metadata succeeded. No new cross-platform support is inferred.

Graphical investigation: the captured 640x360 window shows the correct toggle button
covering (80,130), so stale coordinates alone do not explain the timeout. The harness
confirmed the pointer position, but did not observe the expanded title. No first-party
source or harness changed; this does not establish a regression introduced by pinning.
No isolated X server tools (Xvfb/xvfb-run/openbox/kwin_x11) were available. Next step:
repeat with controlled focus/input on a dedicated X11 session and capture event delivery;
then require toggle roundtrip and both closing paths. Preserve this failed run. Do not
repeat identical attempts or replace the oracle with state-only tests.

Future graphical work: native Wayland on the currently supported Linux x86_64 target;
Windows/macOS only after explicit support decisions and available test environments.
No platform expansion, accessibility, load, sandbox or commercial distribution acceptance.
