# Log diagnosis and repair — 2026-11-15

Final independent validation approved C1–C6 for this bounded repair. This report preserves intermediate observations and does not accept the product or full scanner pipeline.

## Original observations

Run ox-run-52R94IoD has 26 result records, of which seven failed or blocked: Clippy, ox, governance-tests, OpenGrep, Geiger, Ruff and Bandit. Input inventory: 343 files / 10,742,542 bytes on 15 November; 41 files / 798,488 bytes on 14 November. Original-log-inputs.json binds all 384 files before repair.

The message removing 13 November conforms to docs/development/local-artifacts.md and scripts/lib/logs.sh: at most two calendar dates. That directory is absent; its content cannot be examined. No rotation/cleanup is authorized during this investigation.

| Check | Observed state | Wrapper exit | Tool exit |
| --- | --- | --- | --- |
| audit | passed | 0 | 0 |
| bandit | blocked | 3 | None |
| coverage | recorded | 0 | 0 |
| deny | passed | 0 | 0 |
| geiger | error | 2 | 101 |
| gitleaks | passed | 0 | 0 |
| governance-tests | failed | 1 | not recorded |
| grype | passed | 0 | 0 |
| history | passed | 0 | 0 |
| machete | passed | 0 | 0 |
| malware | passed | 0 | 0 |
| opengrep | findings | 1 | 1 |
| osv | passed | 0 | 0 |
| ox | failed | 1 | not recorded |
| ruff | blocked | 3 | None |
| rust-build | passed | 0 | not recorded |
| rust-check | passed | 0 | not recorded |
| rust-clippy | failed | 101 | not recorded |
| rust-fmt | passed | 0 | not recorded |
| rust-test | passed | 0 | not recorded |
| sbom | recorded | 0 | 0 |
| scripts-syntax | passed | 0 | not recorded |
| scripts-tests | passed | 0 | not recorded |
| sdd-structure | passed | 0 | not recorded |
| shellcheck | passed | 0 | 0 |
| trivy | passed | 0 | 0 |

## Confirmed diagnostic groups

- Rust Clippy: 26 diagnostics in ox-ui project store/desktop/views, including const/closure/style, fallible length conversions and concurrent test iteration. Existing warnings-as-errors remain authoritative.
- Governance: ox emitted 80 failures: five current documentary lineage mismatches and 75 relocated historical Markdown link failures. governance-tests observed 231 tests, 16 failures and one skip. Most fail from those same inputs; remaining export/copy observations need independent reproduction.
- OpenGrep: one python.dynamic-eval finding in test_instruction_validator.py, executing a historical validator snapshot to compare old and new gates. Execution is real even though the input is repository-controlled; correction must preserve the old-oracle comparison and authenticate its input.
- Ruff/Bandit: execution blocked before native scanner invocation because static source identities changed. Initial current inspection identifies package-ox.py and sdd/tools/validate.py; tool_exit_code is null, so no scanner findings can be inferred from these two records.
- Geiger: two of sixteen members (app/ui) failed dependency association for serde1.0.229 with the selected global cargo-geiger0.14.0+ec.2. Root found an already-installed local ox.1 version with matching earlier repair identity. Focused replay uses explicit local PATH without changing precedence rules or central tools.

## Execution and acceptance

Plan, owner boundaries, criteria C1–C6 and restrictions are in plan.md. Implementation and governance notes capture per-file decisions. Review/validation remain pending; no correction is yet declared accepted. Original reports and current results must remain distinct.

## Stabilized repair observations

- Clippy exact runner policy/all-features/all-targets: exit0; formatting exit0; ox-ui unit/integration checks exit0 (one opt-in ignored). Implementation.md records command and source identities. Eager array worker startup preserves barrier concurrency.
- OpenGrep historical-oracle loading now validates a fixed source digest and compiles those same captured bytes; independent review found and closed an initial cache/reread binding defect.
- Governance historical links use16 exact authenticated origins; ten explicit successor records preserve original evidence. New project transition independently reviews current terminal against available a0d9 original. The missing82c57 intermediate cannot be replayed and remains UNVERIFIED. Historical registry/pins are unchanged.
- New static review covers changed package/validator sources and five occurrence-specific subprocess fixture findings. Final-scanners/ records Ruff, Bandit and OpenGrep: each native exit0 and parser exit0 over current snapshot with64 Python targets; post-input-check reports no changed inputs. Earlier failing observations remain in scanner-observation/ and task messages; no global lint/security rule was disabled.
- Reviewer context independently ran37 focused tests and verified384 original logs unchanged. Independent final validation and slow regression results are pending.

Original result/process logs often state argv_recorded=false; their historical commands are reconstructed from the observed catalog/configuration, not claimed as complete captured argv. New focused runs retain exact argv separately. Pass/recorded results from the old run are historical observations only.

Current product-visual-workbench welcome and configuration-cohesion criteria are explicitly UNVERIFIED where these edits changed bound inputs; preserved earlier observations do not approve the changed product. This repair report concerns the stated focused failures, not full product or graphical acceptance.

## Post-freeze counterevidence

After the first final-scanners observation, review strengthened historical-origin validation for missing files: rglob would not visit a deleted snapshot. The helper now authenticates all16 sources, including for unlisted callers. This changed two source inputs; the first final-scanners observation remains historical and cannot approve their new bytes. Final independent validation correctly detected this drift. A fresh scanner observation is required after stabilization.

The slow regression pass exposed directory-link and independent-copy failures. C3 remains open until causes are corrected and affected checks pass. These failures are retained rather than relabeled.

Geiger remediation is an explicit operational selection of the already-installed local ox.1 binary. The default runner still honors caller PATH, and the unchanged global ec.2 can reproduce the original failure. Use a shell with `.cache/ox/cargo-home/bin` prepended to PATH for the verified selection; this does not change the canonical complete-run command or authorize a complete run. The focused Geiger snapshot predates Rust lint corrections and is diagnostic evidence, not current product acceptance.

## Geiger focused result

All16 workspace members completed with native exit0 and unchanged strict parser exit0. geiger/summary.json records exact argv, plugin identity, snapshot input hashes and per-member outcomes; raw member reports/stderr/assessments are retained. Existing local cargo-geiger0.14.0+ox.1 SHA256499d092… was selected explicitly; the failing historical run selected global0.14.0+ec.2. No tool rebuild/download/central change occurred.

Diagnostic stderr contains a dependency test-fixture parse message; the existing strict parser still verified empty omission arrays and accepted all member reports. This is the parser's bounded measurement result, not a claim that every dependency fixture parses. Run reproducibility requires selecting the local plugin: from root, `export PATH="$PWD/.cache/ox/cargo-home/bin:$PATH"` before the documented check command. The default caller PATH contract remains unchanged.

## Final execution successor

The counterevidence above is resolved for the bounded repair. The writer stopped before the final run. Nine previously failing integration/regression consumers all passed (exit0,808.499s), including independent copy/corruption, directory-link containment, clean export/recovery, normative hash review, product/skill separation, portable evidence, Git boundaries and original metadata recovery. Raw output is governance-regressions-final.stderr.log; earlier five-failure execution is retained separately.

The true post-freeze scanner observation is frozen-scanners/: Ruff/Bandit/OpenGrep each native0/parser0,64Python targets and no findings. closure-input-check.json compares the complete observed input manifest to final bytes after regression execution; zero changed/missing. final-scanners/ is the earlier observation and remains historical. The twelve copy exclusions are only exact absence mappings under an explicit receipt, with original snapshot hashes and lexical symlink rejection. Target hashes record local15November observation, not historical target recovery or runtime validation of absent bytes.

Documentation disposition: project scope and current feature states, configuration-cohesion plan/tasks/evidence/converge, product-visual-workbench evidence/converge were updated by the governance writer. Existing README/scripts retention/PATH/commands, constitution, architecture and product serialization contracts were reviewed; public commands, retention, PATH precedence, product formats and permissions are unchanged, so no policy/README rewrite is required. Implementation/governance/review/validation notes preserve earlier observations and explain current results. No full pipeline or native graphical acceptance was performed.

Remaining limits: unavailable82c57 intermediate replay; explicit local Geiger plugin selection required (global ec.2 unchanged); Geiger uses its identified pre-Rust-repair snapshot; broad product and configuration feature acceptance remains UNVERIFIED/INCONCLUSIVE as recorded, requiring the respective current full feature evidence. Original13November logs are unavailable under preexisting retention. All384remaining originals were preserved unchanged.

Final independent validation returned C1–C6 APPROVED for the focused repair. See independent-validation.md for the final verdict, preserved provisional states, methods and limits.

## Files changed in this repair

Session-only before/after identities and snapshots are in changed-files.json. Existing unrelated Git changes are not attributed to this repair. New diagnostic records are under docs/validation/log-repair-20261115/.

- `application/crates/ox-ui/src/desktop.rs`
- `application/crates/ox-ui/src/desktop/project_store.rs`
- `application/crates/ox-ui/src/desktop/views.rs`
- `scripts/config/automation.json`
- `scripts/config/native/bandit/bandit-baseline.json`
- `sdd/features/configuration-cohesion/converge.md`
- `sdd/features/configuration-cohesion/evidence.json`
- `sdd/features/configuration-cohesion/plan.md`
- `sdd/features/configuration-cohesion/tasks.md`
- `sdd/features/product-visual-workbench/converge.md`
- `sdd/features/product-visual-workbench/evidence.json`
- `sdd/project.md`
- `tools/governance/scripts/check-ox.py`
- `tools/governance/scripts/export-clean.py`
- `tools/governance/scripts/instruction_revision.py`
- `tools/governance/scripts/log_repair_revision.py`
- `tools/governance/scripts/package-ox.py`
- `tools/governance/tests/test_governance.py`
- `tools/governance/tests/test_instruction_copy.py`
- `tools/governance/tests/test_instruction_governance.py`
- `tools/governance/tests/test_instruction_routes.py`
- `tools/governance/tests/test_instruction_succession.py`
- `tools/governance/tests/test_instruction_validator.py`
- `tools/governance/tests/test_log_repair_revision.py`
- `tools/governance/tests/test_native_exec_succession.py`
- `tools/governance/tests/test_readme_skill_integration.py`
- `tools/governance/tests/test_reconciliation.py`
