# Welcome project-store implementation record

Owner: /root/welcome_store. Exclusive repository write set: application/crates/ox-ui/src/desktop/project_store.rs.
Precondition observed before first write: path absent (`test ! -e ...` exit 0); no preimage bytes existed. Workspace contains extensive unrelated dirty/untracked files; none assigned to this implementer.
Authorities reviewed: AGENTS.md, docs/development/codex-agents.md, sdd/workflow.md, sdd/project.md, docs/constitution.md, docs/architecture/context.md, docs/decisions/visual-workbench.md and product-visual-workbench spec/plan/tasks.
Actual skills consulted: rust (edition 2024 / MSRV 1.99 / pinned toolchain 1.99.1, safe ownership and sync IO), workspace-integrity-engineering (exclusive write ownership, create_new publication and preservation), database-engineering (bounded version schema, lock-before-fresh-read invariant, explicit corrupt recovery). Supporting references: rust concurrency-and-safety/service-engineering, workspace file-operations, database model-and-transactions. No semantic versions declared in entries.
Documentation responsibility: coordinator owns shared docs; backend report supplies observed behavior, focused evidence and limits for T018. No common docs edited by backend.

Implementation/tests pending at initial report creation. No commit, dependency installation, full scanners, publication, or real HOME storage writes authorized/performed.

## Final implementation observations

- Added only `application/crates/ox-ui/src/desktop/project_store.rs`; unchanged fixed API shared with coordinator/UI/root. No module declarations/manifests/shared docs changed by backend.
- Snapshot schema: `OXRECENT` magic (8 bytes), little-endian u32 version 1, u32 count, then u32 byte-length + UTF-8 path per row. Maximum 20 distinct absolute lexically normalized canonical paths, maximum 16384 bytes per path, maximum snapshot 327776 bytes. MRU is successful publication order; paths missing later remain visible/removable. File existence/type and canonical identity are validated on record; load deliberately does not require projects to remain available.
- Location reads XDG_STATE_HOME when nonempty, otherwise HOME/.local/state; root must be absolute. Filename ox/recent-projects.v1. Tests use pure configuration helper and isolated /tmp files, never write actual HOME state.
- Each operation obtains a nonblocking std OS exclusive lock on a stable `.lock` sidecar, reads current disk snapshot under lock, then publishes a unique create_new staging file via write_all + file.sync_all + same-directory rename + directory.sync_all. Sidecar is never deleted/replaced. Guard explicitly unlocks before closing to prevent a concurrently forked unrelated subprocess retaining the inherited open-file-description lock until exec.
- Observed snapshot/lock/parent symlink or special-file state is refused. Standard library checks are cooperative-process protection, not adversarial TOCTOU confinement. Project path aliases canonicalize/deduplicate; symlink collisions at project creation are rejected by exclusive create_dir.
- Corruption refuses ordinary reads/mutations and asks for explicit reset. Reset within supported size preserves exact original bytes into an exclusive retained corrupt-backup file, syncs it and its directory before replacement. Partial backup failures preserve original and retain partial artifact with diagnosis. Valid reset need not create a backup. Repeated corruption reset retains each earlier backup. Unsupported version numbers, including truncated future-version payload, refuse every mutation/reset.
- Oversized corrupt file reset is refused with manual-recovery instruction; the original is byte-for-byte unchanged and no backup copy is made. Backup streaming also takes at most snapshot cap+1 bytes if an uncooperative writer grows the original. This is an explicit size-safety boundary agreed with coordinator; not automatic migration or destructive recovery.
- Sync failure after rename reports publication may already be applied. Abandoned staging files are retained across restart and never automatically promoted; per-process unique staging reservation attempts are bounded to32, no lock retry loop.
- `create_project` validates a nonempty single component (rejects dot/dotdot, slash, backslash, NUL), canonicalizes existing parent and creates exactly one empty directory with create_dir. Existing files/directories/symlinks survive rejected/raced collisions. No scaffolding/Git/commands/tasks/agents/removal are invoked.

## Commands and results actually observed

1. `rustc --version`: rustc 1.99.1 (58cf8f9c3 2026-10-13), matching pinned application toolchain; edition2024 and declared MSRV1.99 inspected.
2. `rustc --edition 2024 --test /tmp/welcome-store-harness.rs -o /tmp/welcome-store-tests && /tmp/welcome-store-tests`: initial execution15 passed,2 failed,1 helper ignored. Failures were transient locks on separate fixture histories during concurrent subprocess fork. `--test-threads=1` passed17/0/1, isolating the concurrency hypothesis. Explicit OS unlock guard added; subsequent parallel run passed17/0/1.
3. Final strict standalone command: `rustc --edition 2024 --forbid unsafe_code --deny warnings --test /tmp/welcome-store-harness.rs -o /tmp/welcome-store-tests && /tmp/welcome-store-tests > /tmp/welcome-store-tests.log`: exit0,17 passed,0 failed,1 intentionally ignored subprocess helper. The helper is actually launched by parent cases for real process lock refusal, process write and exits before/after rename. Log retained in /tmp/welcome-store-tests.log.
4. `rustfmt --edition 2024 --check application/crates/ox-ui/src/desktop/project_store.rs`: exit0.
5. Integrated attempt: `CARGO_HOME="$PWD/.cache/ox/cargo-home" cargo test --manifest-path application/Cargo.toml --offline --locked -p ox-ui project_store --lib`: exit101 at current UI changes in desktop.rs; six E0433 errors for iced::advanced gated by disabled advanced feature. No backend compile error reported. Dependency issue transmitted to UI and root; backend does not own manifests. A fresh integrated run remains for integration owner after that fix.

Test oracles: restart/order/dedup/missing removal preserving sentinel; metadata cap without deleting projects; canonical alias and non-UTF8 rejection; invalid record no mutation; exact corrupt backups and repeated recovery; refusal/preservation for unsupported versions; every truncation of representative snapshot, max count/path lengths, UTF8, duplicates, NUL, unnormalized paths and trailing bytes; oversized refusal preserving all bytes; stale instances fresh-read and two synchronized racing writers retain all acknowledged writes; parent lock excludes same-process and real child-process operations; released lock permits child recording; abrupt child exits in manually arranged primitive publication windows; symlink/socket refusals for snapshot/lock and symlink state parent; empty project, sentinel/file/symlink/dangling collision, invalid/traversal names, absent parent no creation, simultaneous creators exactly one winner.

## Limits and remaining work

Evidence is focused Linux local-filesystem execution, not power loss/OS crash/NFS/multiplatform or hostile concurrent replacement proof. Process-exit tests manually arrange the same staging/sync/rename primitives and call process::exit; they are not injected failures inside the production publish function. Ordinary IO failure injection for disk-full or directory-sync failure was not run. Same-process writers and a real cross-process held-lock/writer were executed; no broad scheduling/model-checking claim. Explicit reset backup retention and crash-abandoned stages can accumulate across user resets/crashes; there is no destructive cleanup policy in this slice. UI threading/journeys/native captures and independent backend review/validation belong to other owners. No acceptance declared by implementer.

Documentation disposition supplied to coordinator: review/update plan D10/WC03, spec reset-size limit, surface/application usage recovery microcopy and T018 evidence with these exact limits. No update to general persistence technology D5/D6 is implied; metadata is a bounded convenience snapshot only.

Actual consulted skill entry SHA256 identities:
- rust: da7b9ada8326b2d2cb4288ac6f67864c7b9defb833641470904c6fe9221d8891
- workspace-integrity-engineering: 42c9ece69f065461c34c4ddeecd6f69a4da758fbd43c4157504c1d423ab88196
- database-engineering: 9fcee66df99fda30e51a004dd16143e2ac1fde12a4398cb8da88ec4ca72ab686
f54c0414d81c41301b89c81124660ca36276b5fe0fc86fb4830d5955b80ac6cf  application/crates/ox-ui/src/desktop/project_store.rs
249cf1f47c1f45a49d9f9ea11f0062c509d01251152245d112bc0553dd52fb82  /tmp/welcome-store-tests.log
