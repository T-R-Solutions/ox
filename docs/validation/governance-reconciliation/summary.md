# Local governance and acceptance reconciliation — 2026-10-29

Confirmed: 30 installed skills against the former 29-entry profile; obsolete
ITAPIRACÓ operational reference; seven historical recovery mismatches; all 13
translated product criteria UNVERIFIED; floating stable toolchain; nested Git
paths eligible under distribution roots. The existing skill-ui-metadata-001
revision was already correct and remains byte-for-byte unchanged.

Implemented: 30-entry profile (17 general, 4 conditional, 9 specializations),
commit-governance bridge version 1, Ox operational wording, explicit eight-path
succession revision and authenticated predecessor recovery. Original hashes,
archives and preexisting changes remain preserved. local-changes.json identifies
all 27 modified preexisting files and retained predecessors. No file deleted.
No application source/harness was changed; toolchain fixed to Rust 1.99.1 while
declared floor 1.99 remains explicitly unproven on 1.99.0.

Validation: check-ox, verify-maintenance and SDD freshness pass. Recovery observes
485 governed historical files and 439/439 layout inputs. Negative tests cover
unauthorized skills, inconsistent bridges, corruption/deletion/current drift,
predecessor failures and recursive Git metadata. 17 fast tests pass in 0.122 s;
17 integration tests pass in 111.818 s. All 34 also pass in the independently
extracted package. Equivalent 15-test median wall time: before 0.159526 s, after
0.160117 s (three alternating sequential runs). The improvement is a fast feedback
group, not reduced coverage or an alleged whole-suite speedup. See timing-review.md.

Product-bootstrap: semantic equivalence confirmed for all 13 translated REQ/AC
pairs. 11 APPROVED; AC-02 and AC-06 INCONCLUSIVE. Exact-toolchain cargo check,
7 regular tests, discovery of 9 tests, fmt and clippy -D warnings passed. The real
X11 native close passed, but toggle timed out; button exit was not reached. Current
window capture confirms coordinates intersect the button, leaving event delivery/
focus unresolved. Historical GUI approval was not reused. Review matrix, raw failure,
environment, application digests and dependency-manifest comparison are under
product-bootstrap/reconciliation. Next step: controlled dedicated X11 input/focus
observation. Native Wayland future on supported Linux; Windows/macOS only after
support decisions and environments. F0, sandbox, IPC and engines remain incomplete.

Sharing: preexisting ox.zip has 96,391,274 bytes and 1,541 Git entries totaling
82,581,520 logical bytes (82,509,509 compressed). Workspace .git has 178,446,123
logical bytes, so the 83 MB estimate describes the old archive's Git payload,
not the current Git directory. No supported script generates ox.zip; it is preserved.
Official generators now exclude exact .git components, including nested directories
and worktree files, preserve .gitignore, and reject included archives containing Git
metadata. Recursive archive budget and corruption detection remain active.

Final package: dist/20261029T134536.318394Z/ox-governance.zip, 13093375 bytes,
908 entries, SHA-256 137890350a435bafcb7e582fe8bcaff316a7159787d6780c41063b97b4cbeefa.
Zero Git/product entries; required recovery, license and validation files retained.
All five commands in the independent extraction passed; source unchanged during
build. The first build failed only its source-stability check while new observation
files were being written; that receipt is retained. The final ZIP is a verified
snapshot; post-build receipts/evidence are recorded separately, not silently inserted.

Main decisions: docs/decisions/governance-reconciliation.md; profile, files.json,
AGENTS, toolchain, distribution/recovery helpers, run-tests and affected SDD features.
No commit, publication, support expansion or historical deletion was performed.
