# Evidence audit correction — 2026-11-17

Scope: independently inspect and correct C-02, C-03, F1-01, F1-18, F2-04;
add bounded trace repairs F1-08/F2-06 assigned by the coordinator. No new product
acceptance, relaxed gate, reexecuted historical test or refreshed old digest.

## Method and observed inputs

Read the project authorities, evidence contract and actual validator; compare all
43 current envelopes and the reported observations with their source criteria.
Recovery includes all 43 pre-edit envelopes/convergences, evidence.md and both
changed traceability files in `/tmp/ox-audit-governance-20261117-before/`.
Its original 87-file digest inventory is `manifest.json`; the subsequently assigned
two traceability preimages are retained separately under their original paths.
This is local recovery, not a portable artifact or a permanent retention promise.

Selected skill: autonomous-verification-engineering,
`.codex/skills/autonomous-verification-engineering/SKILL.md`, bridge
`sdd/chain/autonomous-verification-engineering.md` version 1. Contribution:
separate observed evidence from authorization and current verdicts; preserve
immutable observations and test false acceptance/selective invalidation.
Consulted entry SHA-256: 5ddf5e56747ec5aa418e1a97ad8f08d61cdb7e26c3a5be4c68cb4bfe1bf38958.

## Disposition

| Finding | Result and correction |
| --- | --- |
| C-02 | The mandatory tasks binding and documentation closure order can coexist: finalize task/documentation disposition, then capture the final review. The claimed inevitable contradiction is not established. Clarified this order in evidence.md; no minimum input or checker change. A later task correction still requires affected reevaluation. |
| C-03 | Confirmed undocumented history usage. Current checker matches evidence.md's explicit rule that all current schema-2 observations are checked regardless of criterion status. Documented `historical_evidence` as an Ox extension ignored by the portable checker, current-only references and the limits of history validation. No new schema guarantee is claimed. |
| F1-01 | Confirmed 18 stale bindings across the three windows-design-baseline observations; three APPROVED verdicts changed to UNVERIFIED and references cleared. All original observations moved intact to history. No rehash or cosmetic weakening of input lists. |
| F1-18 | Confirmed 27 stale bindings in visual-skill-refinement's three current observations; moved them intact to history and cleared current references, retaining UNVERIFIED. Replaced generic REQ identifiers in these two features' criterion text with their actual spec declarations. Broader environment/skills.json conventions and workbench family design remain outside this bounded correction. |
| F2-04 | Confirmed unrelated retention links across 26 features: removed 147 criterion references to E-T011-R2-SOURCE-RETENTION and preserved those observations in history. The 148th reference belongs to product-local-persistence T009-PREFLIGHT and remains relevant/current. Also removed eight references to product E-TECH-RUN-AC-* observations from three skill-authoring features; retained the original objects historically. Existing undecided states remain unchanged. |
| F1-08 | Confirmed swapped tasks in technical-acceptance: AC-03 export now maps to T004/D-04/R-04; AC-04 migration now maps to T003/D-03/R-03. Mapping follows the actual spec, plan and tasks. |
| F2-06 | Confirmed scripts-task-closure AC-02/AC-03 pointed to unrelated predecessor decisions. Corrected to D-03/R-03 and D-04/R-04 respectively. The AC-04 legacy declaration remains accepted by the existing grammar; no contract rewrite. |

28 evidence envelopes changed. Forty current observation objects were retained
unchanged in history. Exactly three criterion states changed (the windows feature
APPROVED → UNVERIFIED); no criterion was promoted or removed. Historical and current
observation objects from every preimage were compared for exact JSON equality,
including all original methods/results/artifact/input hashes: PASS.

## Executed verification

| Command / method | Observed result and limit |
| --- | --- |
| `python3 sdd/tools/validate.py --root . --require-fresh --check-convergence` before correction | Exit 1; 45 stale bindings: visual-skill-refinement 27, windows-design-baseline 18. Full output retained in local recovery `validate.txt`. |
| Same full-corpus freshness/convergence command after evidence correction | Exit 0; current schema/bindings/projections pass. Does not approve the undecided criteria or validate historical artifacts. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools/governance/tests -p test_instruction_validator.py -v` | Exit 0, 24 tests PASS; includes history ignored, all selected acceptance gates, schema-1 freshness rejection, mismatched projection, shared checks and symlink/escape rejection. |
| Five selected `test_governance.GovernanceTests` cases | Four PASS: freshness_selective_invalidation, english_and_legacy_states_enforce_the_same_evidence_gates, missing_artifact_not_approved, missing_evidence_artifact. Fifth, product_feature_isolated_from_skill_acceptance, ERROR via check-ox CurrentContentError: scripts/README.md current bytes differ from the pinned predecessor. That file was outside this writer's assignment. Suite exit 1; no successful suite claim. |
| `python3 sdd/tools/validate.py --root . --feature windows-design-baseline --require-fresh --require-approved --check-convergence` | Expected exit 1, rejects AC-01/02/03 as UNVERIFIED. Demonstrates that retiring stale evidence does not grant acceptance. |
| Observation/state preservation inspection | PASS: every old current/historical object retained intact across 28 changed envelopes; only the three named state downgrades. |
| Final repeat after both trace repairs and report creation | Exit 1: concurrent product-local-persistence/spec.md line 53 begins `AC-01–07 of this feature`, rejected as a malformed declaration. This writer did not edit that spec; coordinator notified to repair the prose before final validation. The earlier successful result applies to the earlier observed inputs only. |

Commands used Python stdlib, local files and no scanner/network invocation.
Independent review and validation of this correction are the coordinator's next
steps. The test error above and broader audit issues remain explicit limits.

## Documentation disposition

Reviewed and updated `sdd/evidence.md` and the two visual feature convergence files;
updated 28 affected evidence envelopes and two traceability files. The current
projection agrees with the evidence owner; dated independent validation remains
historical. Spec/plan/tasks minimum bindings, checker implementation and acceptance
criteria were preserved. Product behavior and native verification are unaffected
by this evidence-only correction. No current product or skill acceptance is inferred.

Changed evidence envelopes:

- `sdd/features/adoption-governance/evidence.json`
- `sdd/features/skill-plugin-protocol-engineering/evidence.json`
- `sdd/features/skill-agent-runtime-engineering/evidence.json`
- `sdd/features/skill-autonomous-verification-engineering/evidence.json`
- `sdd/features/skill-workspace-integrity-engineering/evidence.json`
- `sdd/features/skill-iced-engineering/evidence.json`
- `sdd/features/skill-code-context-engineering/evidence.json`
- `sdd/features/skill-code-knowledge-graph-engineering/evidence.json`
- `sdd/features/skill-tool-output-engineering/evidence.json`
- `sdd/features/skill-agent-usage-accounting/evidence.json`
- `sdd/features/governance-externalization/evidence.json`
- `sdd/features/product-foundation/evidence.json`
- `sdd/features/governance-layout/evidence.json`
- `sdd/features/maintenance-001/evidence.json`
- `sdd/features/product-bootstrap/evidence.json`
- `sdd/features/skill-ui-metadata-inventory/evidence.json`
- `sdd/features/governance-reconciliation/evidence.json`
- `sdd/features/product-plugin-host/evidence.json`
- `sdd/features/product-agent-runtime/evidence.json`
- `sdd/features/product-verification-engine/evidence.json`
- `sdd/features/product-local-task-ui/evidence.json`
- `sdd/features/technical-acceptance/evidence.json`
- `sdd/features/skill-consumer-validation/evidence.json`
- `sdd/features/product-f0-gate/evidence.json`
- `sdd/features/readme-skill-integration/evidence.json`
- `sdd/features/technical-documentation-visuals/evidence.json`
- `sdd/features/visual-skill-refinement/evidence.json`
- `sdd/features/windows-design-baseline/evidence.json`
