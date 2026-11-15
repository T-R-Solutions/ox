# Plan: native visual workbench

## Authority and route

Full route. User explicitly authorizes visual product changes, useful skill adaptation,
SDD/AGENTS integration and proportionate checks. Linux x86_64 remains the target;
Rust 1.99.1, edition 2024/MSRV 1.99, Iced 0.14.0 and existing lockfile are preserved.
Preimages, initial dirty status and reference identities are under
`docs/validation/visual-workbench-20261111/`. Unrelated repository maintenance remains intact.

## Decisions and risks

- D-01 / R-01 (REQ-01): Use v4's broader state/component/coverage contracts and v3's English/token detail to author DESIGN.md in English. External self-declared authority cannot supersede Ox policy. Preserve sources rather than importing the prototype directory as product architecture.
- D-02 / R-02 (REQ-02): Use typed native theme/density/component roles, neutral reading surfaces and Signature Blue shell. IBM Plex remains the documented font family; unavailable distributable native fonts use explicit fallback. Proposed typography/chromatic alternatives remain proposals.
- D-03 / R-03 (REQ-03): Retain worker/generation/cancellation ownership and raw evidence text. New presentation state never grants backend acceptance. Native status labels may localize known vocabulary while raw diagnostics remain available.
- D-04 / R-04 (REQ-04): Use source-backed native destinations for all planned capability families. Display backend availability and integration prerequisites; do not add fake execution, prices or graph relations.
- D-05 / R-05 (REQ-05): Dynamic focus order includes visible controls only; narrow layout collapses secondary navigation and retains access to it. Test real key activation and domain state boundaries separately.
- D-06 / R-06 (REQ-06): New observations bind new bytes; historical F0 images/metrics remain historical. Do not claim the old performance corpus on new layouts.

## Selected methods

Primary: `.codex/skills/design-system/SKILL.md`, bridge `sdd/chain/design-system.md` v1: shared roles, variants and state contracts.
Supporting: design-review (reference diagnosis), iced-engineering (native layout/focus/message integration), rust (ownership/validation), skill-creator (separate skill-method adaptation), workspace-integrity-engineering (dirty-file preconditions and preimages). Entries have no declared semantic version; hashes are recorded in the observation manifest.
No recursive activation or delegation. The skill-library work has independent acceptance in `sdd/features/skill-native-visual-method/`.

## Implementation

T001 inventory/design → T002 native roles/navigation → T003 functional and planned views → T004 native/Rust verification → T005 evidence/docs.
Sources stay in ox-ui; desktop integration tests in ox-app. No new runtime or storage dependency.

Actual method identities and applied contributions: docs/validation/visual-workbench-20261111/methods.json. Native geometry/state/paired-capture method was used for the role generator, controls review and native_review.py. Tests do not establish full acceptance.

## Reference integration successor

User requests analysis, planning and implementation of useful supplied material.
Continue full route, REQ-01/02/04/05/06. Prioritize real desktop composition over
additional destinations: embedded file browser and tabs, primary code canvas,
context inspector, tool strip, relationship map and agent role table. Demonstration
selection is presentation-only, explicitly labelled, and performs no filesystem IO.
Use existing Iced widgets and roles; no new dependencies, runtime or engine.
Acceptance: selections change displayed embedded content; wide panes stack at narrow
width; active controls enter traversal; every source member has identity and a
disposition category, without claiming automatic classification is semantic review.
R13 B remains proposed, fonts remain Plex, duplicate skills are not reinstalled.
Primary design-system and supporting iced-engineering/rust use paths/bridges already
recorded above; actual identities recorded in the successor manifest.

## Start-screen implementation plan — 2026-11-14

Full-route continuation of REQ-02–06. D-07 / R-07: distinguish path draft, validated
session and actual operation; keep Controller effects and Select→Tasks transition.
Choose R4's entry + context-inspector composition with a compact directory form;
reject a marketing hero and a fictitious recent-project list. R11/R12 selection
inspection contributes actual session context only. Native roles retain Plex,
neutral canvas, Signature Blue chrome, Light default and explicit Dark/HC.
At narrow widths stack contextual content and keep all active controls reachable.

Primary selected/consulted method: `.codex/skills/iced-engineering/SKILL.md`,
`sdd/chain/iced-engineering.md` bridge_version 1; contributes Message/focus/layout
contracts and `references/native-visual-contract.md` capture/inspection workflow.
Supporting selected/consulted method: `.codex/skills/design-review/SKILL.md`,
`sdd/chain/design-review.md` bridge_version 1; contributes R4/R12 hierarchy comparison
and honest empty/resume decisions. Neither entry declares a semantic version;
actual content hashes are recorded in this observation's methods.json.

Ownership: ec_implementador owns desktop.rs and desktop/views.rs plus focused inline
tests; coordinator owns project/feature/design documentation and evidence report;
root owns isolated native-session harness and native-* outputs; ec_revisor and
ec_validador_alta inspect independently of implementation. Preserve others' edits.
Preflight observed profile-based spawn, fresh review context, messages/list/interrupt;
limit four total agents, two specialist slots. No close tool; successful later spawn
must establish released capacity. No specialist may subdelegate.

T009 source analysis/plan → T010 native implementation → T011 focused Rust + native
journeys and independent review → T012 documentation, input-bound evidence and
independent validation. SC-01 hierarchy/truth, SC-02 actions/focus/state boundaries,
SC-03 native responsive/themes, SC-04 regression/documentation are bounded
observations, not substitutes for the feature's broader AC gates.

## Folder-picker plan — 2026-11-14

Full route: asynchronous external-dialog ownership and late replies introduce material
concurrency/compatibility risk. D-08/R-08: keep one worker-owned dialog, request identity,
explicit cancellation/reaping, and existing Controller validation. Preserve preimages.
Compare installed Zenity 4.2.2 (LGPL-2.1-or-later per local RPM) with a portal crate
(new unavailable cached dependencies) and a bespoke Iced file browser (larger filesystem
UI scope). Provisional choice: supervised installed Zenity through Rust std, no shell;
manual input and recoverable error when the external helper is absent. Confirm CLI
contract, exact path encoding and lifecycle before acceptance. No Cargo dependency
or platform expansion is implied.

Primary consulted method .codex/skills/iced-engineering/SKILL.md, bridge
sdd/chain/iced-engineering.md v1, plus message-update-state: async request and focus.
Supporting .codex/skills/rust/SKILL.md, sdd/chain/rust.md v1 plus concurrency-and-safety:
worker ownership, process cleanup and exact bytes. Entries declare no semantic version;
content hashes recorded in methods.json.

Ownership: implementer desktop.rs/views.rs/new folder-picker module and tests;
coordinator project/feature/design/usage documentation and report; root native harness
and native-* captures; independent ec_revisor and ec_validador_alta read/evaluate.
Observed profile-based spawn, fresh contexts, messages and four-agent capacity;
no close tool. Review and implementation use the two specialist slots, validation
follows a completed slot. All writers preserve unrelated edits.

T013 compare/plan → T014 implement/tests → T015 native/review → T016 documentation
and independent acceptance. FP criteria are scoped manual decisions, not wholesale
feature approval.
