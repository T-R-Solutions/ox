# Audit correction follow-up — 2026-11-17

The maintainer authorized correcting the follow-up findings. This report supersedes
the current blanket closure of audit-correction-20261117, preserving its original
bytes and observations under retained/. Earlier AC-01–04 approvals describe the
prior manual supplement and do not accept these new inputs.

## Corrections and limits

D-14 was a real missed defect: DESIGN.md explicitly sets product-interface pt-BR.
The local-task sentence had a translated fragment inside English text. The full
completion presentation and both outcomes are corrected; engine states remain
unchanged. This is a presentation repair, not universal translation of logs/metadata.

V-11 improved contrast but erased button roles under focus. Focus now preserves
role and interaction colors; the contrasting boundary carries focus. Disabled
appearance and selection remain distinct. Unit/native observations are separate.

The assessment now expands13generic skill rows and bare pointers into concrete
source-specific dispositions, with corrected original-versus-current wording.
assessment-index.json maps all151IDs to original source lines/headings and current
disposition. Row counts are inventory evidence, not semantic approval.

Root retained109 available source/preimage/baseline/copy artifacts with exact
hash/length/origin in retention-manifest.json. The original audit source and43
pre-edit envelopes/convergences can now be inspected without /tmp. Copy logs
remain historical; preserving them is not rerunning the isolated check.

Independent reviewers/validators use fresh contexts. Their messages are recorded
with agent identity, scope, methods and inputs; coordinator transcription is
explicit. A second review pass in the same independent context is legitimate;
unchanged inputs do not require repeated tests. No transcript proves OS isolation.

## Remaining governance design debt

The46-document pinned succession mechanism remains a maintenance constraint.
It authenticates exact historical/current terminals, not their semantic correctness.
Replacing it with arbitrary live-document acceptance would weaken adopted
historical-link ADR D-04 and older consumers. This task does not claim that redesign
solved. A future migration needs a separate authority decision, immutable historical
object identity, explicit current semantic checks and old/new consumer rejection tests.

One additional bounded successor for components.md was necessary because its
old focus description became false. It preserves the preimage and all previous
registries. Scope authorization is recorded here rather than editing more pinned
project/design files. This limits new changes but does not eliminate the debt.

## Verification and acceptance

- Rust ox-ui tests:52unit cases (51pass, one subprocess helper ignored at top level), five integration cases passed; explicit presentation-state assertion passed separately.
- Final clippy all-targets with warnings denied, fmt check and diff check: exit0.
- Independent reviewer:7focus,1presentation,7audit and6successor adversarial tests passed. Root additionally ran existing audit7/OSV6/Claude6 and new gate6 successfully.
- Native private Mutter session:3theme matrices rendered production button_style; actual application received five Tab events with captured focus. Forced fixture states and real application focus are distinct observations. Native result/source/binary hashes, retained replay helpers, events and captures are under native/. No AT or complete workbench acceptance.
- Freshness/convergence: exit0. Root check-ox: exit0. Whole selected product-workbench/scripts acceptance still rejects14INCONCLUSIVE criteria; these are not promoted by this bounded repair.
- Previous scripts AC08 is now INCONCLUSIVE because its bound claude_analysis_revision.py changed to integrate the new documentary successor. Original E03 remains intact in historical_evidence and prior-acceptance snapshots. No old hash was refreshed.

Final independent criterion verdicts are recorded in validation.md. No full scanner
run, publication or commit occurred. Three additional UI preimages are retained in
ui-before/ with origin/hash manifest, separately from the109historical artifacts.

## Documentation disposition

Reviewed/updated audit-correction assessment/report/visual/validation, components.md,
product-visual-workbench plan/tasks, scripts-centralization evidence/converge and
this supplement. Prior blanket approvals are historical, D14 andV11 corrected;
component contract matches code, targeted feature documentation records current
scope. Constitution, DESIGN and architecture authorities remain unchanged; their
pt-BR, Visual Studio2026Enterprise and Rust/Iced constraints apply. A native matrix
of shared component roles is not same-theme whole-IDE parity approval.

Final bounded verdict: AF-01–05 APPROVED by independent validation. Review found no open finding in its examined scope. Global product/scanner acceptance remains undecided as stated above.
