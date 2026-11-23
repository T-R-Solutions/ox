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

## Welcome/projects plan — 2026-11-14

Full route/high risk: persistent metadata, concurrent writers and filesystem creation.
D-09/R-09 (WC-01/05): dedicate S01/S02 entry shell, neutral canvas/reading surfaces,
small Ox brand plus accessible Settings; bounded approximately 1000 px content,
concise welcome/actions and dominant recent list. No rail/technical toolbar/footer
on entry. Use shared roles/Plex; blue marks action/focus/selection. Manual path is
disclosed on request. Recent rows expose name/full wrapping path and removal.
At narrow width stack sections, scroll focused control into view. Baseline captures
are actual native files in visual-workbench-20261111/welcome-baseline-*; desktop
geometry differs from monitor size and must be reported accurately.

D-10/R-10 (WC-02/03): a bounded versioned local snapshot for at most 20 canonical
UTF-8 paths, ordered by successful-open commit order (no clock dependence).
Location: XDG_STATE_HOME/ox/recent-projects.v1, fallback HOME/.local/state/ox; require
absolute state root. This is metadata convenience, not authoritative task evidence.
Choose std-only format with explicit lengths/version/size bounds, avoiding a new
DB dependency or resolution of D5/D6 for general storage. One stable lock file,
nonblocking cooperative OS file lock per operation, fresh read under lock, unique
create_new staging, sync+same-directory rename+directory sync. Busy/error reports
recoverably; no unbounded retry. Corrupt known-format history is preserved and
requires explicit reset with retained backup; future versions are read-only errors.
Unknown/invalid original bytes never silently overwritten. No automatic eviction
of projects: 20 is metadata cap only. Cooperative Linux local-filesystem envelope;
no hostile writers, OS crash/power-loss or remote filesystem guarantee.

D-11/R-11 (WC-04): create a single empty child directory in an existing canonical
parent, rejecting empty/dot/traversal/separators; use exclusive create_dir so raced
collisions preserve the winner. No create_dir_all for project destination, no Git,
scaffolds, processes or deletion. Parent replacement by hostile same-user processes
is outside envelope and must not be called confinement. Existing content survives
every rejected case. After an uncertain error inspect/report; never repeat effects
automatically. Worker owns effect and result; no IO in view.

Methods actually consulted: primary iced-engineering (native state/tasks/layout);
supporting workspace-integrity-engineering (preimages, races and preservation),
database-engineering (bounded schema/lock/read-modify-publish/recovery), design-review
(actual baseline hierarchy and proposed journey). Paths .codex/skills/<name>/SKILL.md;
bridges sdd/chain/<name>.md version 1, identities in welcome-projects-20261114/methods.json.
No entry declares semantic version. No recursive skill activation.

Ownership: coordinator owns project/feature/design/usage/architecture documentation
and report; backend implementer owns desktop/project_store.rs only; UI implementer
owns desktop.rs, desktop/views.rs, workbench.rs and focused UI tests. Root owns
native harness/captures. Specialists preserve existing edits and do not subdelegate.
Backend publishes fixed API before UI integration. Revision and validation use new
independent contexts; four total slots, implementation slots reused after termination.

T017 contract/baseline → T018 backend + T019 UI (disjoint ownership) → T020 tests/GUI/
independent review → T021 documents/evidence/independent validation. Changes reopen
only affected observations; earlier SC/FP acceptance remains historical.

Reference update before implementation: user identified IntelliJ IDEA and supplied
/tmp/pasted-image-.png (identity in spec/report). Coordinator inspected it: adopt
neutral project entry and grouped start actions, exclude unsupported clone/remote
entries and onboarding promotion. Ox tokens/Plex remain authoritative. Root owns
docs/validation/welcome-projects-20261114/native-harness.py and native-* exclusively.

Bounded recovery clarification: reset backs up malformed compatible-format bytes
only within the snapshot byte admission limit. A valid list may be cleared by the
explicit reset action without a backup; UI must state this consequence accurately.
Oversized files remain untouched and require manual recovery; copying arbitrarily
large corrupt input is excluded. Unknown schema versions always refuse reset.

Backend applied rust support: .codex/skills/rust/SKILL.md, sdd/chain/rust.md v1;
consulted by backend implementer for safe std-only IO/ownership and Rust 1.99.1
checks. Entry hash and applied contributions are in backend-implementation.md.

Integration ownership extension: UI implementer additionally owns application/Cargo.toml
solely to enable the existing Iced advanced feature required by widget operations
that reveal focused welcome controls. No dependency version/lock change or download
is authorized. Coordinator assigned this after confirming advanced absent; root
notified to avoid a competing edit. Build/test offline and locked.
S02 requires an absolute parent in UI so complete destination can be shown without
filesystem IO in view; backend canonicalizes the supplied existing parent.

## Welcome identity/layout plan — 2026-11-16

Local-route presentation refactor under the current request, superseding the
earlier scope's text-only identity/download restriction solely for the required
embedded PNG rendering support. Root owns UI/assets/manifests and affected docs.
Use existing controls/messages/IDs rather than a new entry-state machine. Put
the signature/mascot in a 240-unit navy column with a flexible project-entry/list
area (1080 max); below 900 use a horizontal identity strip and stacked sections.
The same body scroll/reveal operation handles focus and lengthy recent lists.
PNG-only image decoding extends Iced 0.14.0's current software renderer; preserve
edition/MSRV/toolchain and existing package versions. Runtime reads no local asset
path. Source PNGs remain unchanged and provenance is recorded beside their copies.

Consulted methods: design-system (composition/reuse/accessibility), iced-engineering
(native adaptation/capture/keyboard), rust (manifest/features/checks), actual entries
and references recorded in the identity report. No bridge installation or delegation.
Risk/criteria, actual commands, source/copy identities and observation limitations
are in docs/validation/welcome-identity-20261116/report.md. Historical WC/AC gate
states are not renewed by a bounded visual observation.
