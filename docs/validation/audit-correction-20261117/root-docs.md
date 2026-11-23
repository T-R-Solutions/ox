# Root documentary contribution — 2026-11-17

Owner: root, under high-profile audit coordination. Scope: D-02, D-12 (sharing/index),
C-10/F2-15, D-17 and D-18; read-only supplementary F1/F2 assessment.
Primary skill actually consulted and applied: `.codex/skills/technical-documentation/SKILL.md`,
SHA-256 f128a9f1c328151c05f6f4364b2de4553dd1eefd24f7028a1057daa17c408483; bridge `sdd/chain/technical-documentation.md` v1.
Contribution: align trust-boundary explanation and navigation with inspected code,
retain historical identity and distinguish source inspection from operational proof.
No external sources or new security decisions. Text/table corrections add no visuals.

## Implemented corrections and focused verification

- D-02: replace absent-host/runtime/product assertions with nine implemented or
  pending trust boundaries, naming source paths and data/control/limitations.
  This describes existing controls and does not declare them secure or accepted.
- D-12: link sharing instructions to governance.md; separate Git log omission from
  export inclusion; index now describes actual two-date operational retention.
  README root retention prose is assigned to the visual/documentation worker.
- C-10/F2-15: index all 43 direct feature directories, distinguish twelve skill-*
  features from nine specializations and label F0 observations historical.
- D-17: index bootstrap v2.0 as executed historical instructions; preserve prompt bytes.
- D-18: explain files.json as provenance/succession ledger; preserve all ledger bytes.

Observed checks: focused Python local-link existence check over the five changed
Markdown documents PASS (exit 0); actual direct spec-bearing feature directory set
versus indexed names PASS, 43/43; git diff --check over owned paths PASS (exit 0).
These checks do not validate anchors, exported-copy portability, rendering or security.
Source inspection covered host handshake/grant/socket setup, Runtime spawn,
Controller workspace/attempt/oracle wiring, Zenity supervisor and RecentStore paths.
No Cargo or native interaction run for this prose contribution.

Documentation disposition: reviewed/updated all five owned paths above. Reviewed
constitution, architecture context, evidence/workflow, local-artifacts, sharing,
feature specs and source files below. No Rust behavior or security policy changed;
no historical observation hashes renewed. Independent review remains coordinator-owned.

## Additional F1/F2 assessment

| Finding | Source-grounded disposition |
| --- | --- |
| F1-02/F2-03 | Scope families outside AC JSON are real, but manual acceptance is explicitly allowed by evidence.md Markdown-only. Manual observation cannot promote broad ACs. Ambiguous current-versus-historical wording needs correction; mandatory conversion of every manual criterion to AC is an optional redesign. |
| F1-04/F1-19 | PE-03/WC-05 and older visual plans conflict with later sidebar/fallback composition. Assigned visual worker for in-place succession; no new GUI acceptance inferred. |
| F1-05 | Repeated input manifests are real historical duplication; centralizing them would change evidence schema/readers and preservation. Retain history; optional migration with independent compatibility tests, not deletion in this audit. |
| F1-06 | Several ACs closely repeat REQs, but plan/test oracles exist (e.g. bootstrap traceability). Repetition alone does not make an AC invalid. New acceptance requires concrete scenario/oracle; no blanket rewrite or approval from prose. |
| F1-07/F2-18 | Traceability contains spec-as-oracle and source-as-oracle entries (f0-gate, local-persistence, workbench). Structural validator does not prove oracle independence. Documentary planning criteria can use a spec inspection; runtime criteria need actual independent execution before acceptance. Current undecided states do not become APPROVED. |
| F1-09/F2-07 | Workbench traceability still lists T001–T003 despite later tasks; toolbox/toolchain retain predecessor decision mappings. Real maintenance debt; needs per-criterion successor mapping rather than assigning every task indiscriminately. |
| F1-10 | Bootstrap REQ-11/AC-11 still say IPC unavailable; later plugin-host code exists and bootstrap plan/task T011 record succession. Correct narrowly; whole AC cannot be marked NOT APPLICABLE because versioned-contract and absent-sandbox obligations remain. |
| F1-11 | Foundation AC-01/02 have literal old application/skill counts. AC-03 already has explicit 2026-11-01 applicability note and ADR technical-acceptance. Historical acceptance is not current; changing all predecessor gates to today's product scope needs an explicit successor, not silently weakening assertions. |
| F1-12/F2-05 | Dated historical notes do not become current JSON acceptance. Clarify heading/scope where misleading; retain original observations. |
| F1-13 | Environment-provided skill-creator is actually available outside the catalog; outside location alone is not a policy violation. Historical plans cannot acquire a fabricated old hash; record available identity and unverified original version. |
| F1-14 | Product-local-persistence scope is task/attempt/check/history. MRU is an explicitly authorized narrow exception in architecture/context.md and workbench WC. Missing cross-reference is real; moving project_store into ox-storage would be an optional architectural change. |
| F1-15 | skill-native-visual-method/tasks.md names nonexistent T004/T005. Correct phantom IDs without inferring closure of T003. |
| F1-16 | Missing checkbox formatting is present, but bootstrap has explicit current-note succession. T903 statements of partial execution are immediately succeeded by t903-memory closure notes in f0-gate/local-task-ui/verification-engine; do not reopen those tasks merely from intermediate text. |
| F1-17 | D-ROBUST/T901–903 duplicated across integrated consumers. Duplication by itself does not justify deleting independent obligations; library-versus-UI scope needs clarification at new acceptance. |
| F1-18 | Generic criterion text/limitations are weak metadata; stale active evidence is corrected by governance worker. No auto-promotion based on new descriptions. |
| F1-20 | VS baseline native convergence remains unverified; documentary ACs do not prove implementation. New native acceptance work requires the actual paired observation, not invented build/theme data. |
| F1-21 | Absence of exact feature-name grep in project.md does not establish absent authorization. Existing feature scope and request history must be examined; audit request itself authorizes corrections, not revival of prior product scope. |
| F1-22 | Spacing typos are locally repairable; visual worker owns affected visual docs. |
| F2-08 | Overlapping scanner ownership successors are real. Consolidation into one feature is optional; preserve all gates and histories. |
| F2-09 | D-30/R-30 reused for Gitleaks and Bandit is real. T014 successor paragraph explicitly labels succession of the existing task; numeric gaps are not defects. |
| F2-10 | scripts-security-preparation original native/OX_TOOLBOX_BIN clause is historical; ownership successor covers Trivy/OSV/Grype, while AC-02 Opengrep reason incorrectly points at those ACs. Do not claim those scanner observations approve Opengrep. |
| F2-11/F2-12/F2-14 | Cache path/check table/default-versus-wrapper docs require updates; coordinator owns. Shared defaults are already authorized in scripts-centralization Default parity successor, so lack of authorization allegation is not sustained. |
| F2-13 | Legacy versus run subcommand complete selections differ; document actual CLI distinction rather than change selection policy. |
| F2-16 | scripts-centralization AC-06/07 have empty evidence_ids/reasons and INCONCLUSIVE. Prior task observations can be historical; they cannot establish current broad approval. |
| F2-17 | Format/disposition gaps real in some older tasks. Do not fabricate retrospective reviewed paths or independent proof for historical completion. Current closure disposition is recorded here. |
| F2-19 | technical-acceptance ADR expressly supersedes foundation AC-03, not the three other compound gates; existing 2026-11-01 notes explicitly preserve them INCONCLUSIVE pending succession confirmation. Their remaining preservation obligations cannot be waived by this audit. |
| F2-20 | Geiger 16-member observation exists in geiger-selection-20261115/report.md; supersede old incomplete note but preserve historical identity and broad feature's unverified state. External-owner reason is old context, not fresh operational evidence. |
| F2-21 | Missing /tmp recovery cannot be reconstructed truthfully from a nonexistent path. Retain historic reference with limitation; no speculative replacement of original bytes. Environment skill paths are not mandatory portable dependencies just because historical plans cite them. |
| F2-22 | Empty reasons for undecided states are not a schema violation, but insufficient explanations; arbitrary REQ/AC duplication alone not proof of incorrect behavior. Malformed table and misleading current prose are documentary repairs. |
| F2-23 | RustSec expiry is a bounded current data constraint, not a program defect. Do not extend timestamp or pretend upstream review occurred; acquisition/review must be real and separately authorized. |

## Observed source identities

These hashes identify bytes inspected, not a new acceptance envelope. Later edits
invalidate only dependent observations; coordinator must account for any changes.

```json
{
  "application/crates/ox-plugin/src/host.rs": "d9090041b0d0012788fb95d1fb94848e51ab792715304e73300ce70ade5cf54b",
  "application/crates/ox-agent/src/runtime.rs": "aa276e43e5137220fa00ea34fd7d85ea505a8ead3d90c3a16a736f000cf0023c",
  "application/crates/ox-ui/src/desktop.rs": "7c753eff19719b6ed7ccbcaedb591e796b231a2c752e9e9744061fe7cd6fb1f9",
  "application/crates/ox-ui/src/local_task.rs": "88553bcfba911ee664ff8ff59de492197ebae1b199367be08bfd239759052098",
  "application/crates/ox-ui/src/desktop/folder_picker.rs": "ab8625cfd36b99b624b676c19f822c37e8cd61286105f1dadbe0a12f7032b6fb",
  "application/crates/ox-ui/src/desktop/project_store.rs": "09c3e15655b2c50697daea20f6ac560181ec1a612f87cc58b680c07576ece0ce",
  "application/crates/ox-verification/src/engine.rs": "6a214c1925034db9497f6b3ccc47cf2573503219d28604e524ce1686db0b6c1e"
}
```

## Transferred narrow feature corrections

Coordinator transferred exclusive ownership of product-bootstrap/spec.md and
scripts-toolbox-native/{plan,tasks}.md. F1-10: clarify IPC-only succession while
retaining versioned-contract/sandbox requirements and undecided acceptance.
F2-09: distinguish Bandit D-32/R-32 from Gitleaks D-30/R-30. F2-20: replace stale
T029 pending prose with the dated 16-member Geiger observation and current-input
limitations; broad AC-03/complete remain open. No runtime behavior changed.
Pre-edit bytes retained under /tmp/ox-audit-root-before; no historical hash renewal.

## D-16/V-14 supplemental factual inventory

Coordinator transferred NOTICE, docs/licensing/review.md and font-provenance.json.
Added docs/design/dependency-fonts.json rather than misattributing dependency fonts
to IBM. Inspected local Lucide ISC/MIT, Plex OFL, scripts/security MIT/NOTICE,
lockfile iced_graphics 0.14.0 checksum and cached include_bytes/TTF name records.
NOTICE now identifies later skill imports and these materials; original dates and
unresolved rights remain explicit. Iced-Icons font-specific permission is unverified.
No legal conclusion, download, asset copying, dependency change or distribution.
Documentation disposition: all four paths updated; sources listed above reviewed.
