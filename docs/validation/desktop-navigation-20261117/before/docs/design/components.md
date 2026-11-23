# Native component contracts

Consumers are `desktop/views.rs`; roles/styles in `design.rs`, generated palette in
`tokens.rs`. Geometry uses density gap/inset/control padding; body/code sizes stay
stable. These contracts describe implemented components, not future widgets.

| Component | Purpose / consumers | Variants and states | Keyboard / focus | Sizing and overflow |
|---|---|---|---|---|
| Control | commands on every surface | primary, secondary, danger, chrome, navigation; disabled/hover/pressed/focus | explicit visible-control traversal; Enter/Space; disabled omitted | density padding; toolbar wraps |
| Navigation | all 27 destinations | 3-unit selected side marker, hover, focused; native group icons | Tab and Ctrl+K; hidden items omitted; focus moves to visible toggle | 256 logical px when wide; collapses below 980; scroll |
| Workspace input | start/project/task | editable, disabled while busy, focused, validation text | persistent label; Enter validates; text editing preserves native behavior | fills available width; text scrolls |
| Section / notice | task, settings, planned views | surface/recessed, title, context, content | noninteractive text; no fabricated focus target | fills width; body vertically scrolls |
| Evidence badge | task/history/header | unverified, approved criterion, rejected, inconclusive; busy overrides historical verdict | text and symbol; no activation | wraps with header; historical raw data separate |
| Command palette | all destinations | query, empty, selection | Ctrl+K; arrows; Tab; Enter; Escape restores trigger | bounded 760 px; scrollable results |
| Theme/density selector | settings and toolbar | 3 themes; 2 densities; session-only | controls in traversal, explicit selection | wrap; never reduces body font |
| Code/diff preview | editor/focus/review | labelled embedded/synthetic data | read-only; no save/accept effect | monospace; WordOrGlyph wrapping for source |
| Planned capability | future screens | unavailable reason and disabled effect | navigation stays active; unavailable effect excluded | vertical scroll; no fake result or progress |

Native 16-unit line icons in `desktop/icons.rs` supplement localized command
labels (folder, add, panels, search, settings, file and activity). Evidence symbols
remain redundant with state text. No third-party icon library is redistributed;
this bounded vocabulary does not complete the supplied 122-icon library. Dedicated graph/editor interaction widgets and
full tree/table icon coverage remain future visual work; backend absence alone does
not prove their design complete. Font provenance and bundled OFL are recorded in
font-provenance.json. Screen-reader semantics have not been verified.

## Embedded workbench successor

`document_view` consumes three build-embedded documents. `DemoDocument` changes
selection and inspector; `DemoTool` changes the unavailable tool context. Values are
bounded to 0..3 and cannot affect Controller/generation/cancellation. Selection
persists only in presentation state. Tree and tabs have separate keyboard focus targets and share selection.
Tool focus scrolls the outer viewport to keep its controls visible. Active text and border supplement color. The code viewport
scrolls at 360 logical px; long lines wrap. At 1400+ window width the explorer and
inspector flank the primary canvas; otherwise the composition stacks.
`relationship_map` uses declared Cargo dependencies, with a stacked alternative below
1200. `agent_roles` provides a role/responsibility/instance table with no invented
agent activity. Existing theme roles and body sizes apply; no new asset dependency.

## Enterprise chrome successor — 2026-11-16

At 1100+ logical width a single context row combines navigation, identity,
project context and presentation commands. Below that width commands use a
second row to preserve their labels. Busy cancellation retains its own visible
control region. The status footer is a single compact row. S01/S02 context
separators have bounded height; unrestricted vertical rules must not expand
header rows. The recent/action sidebar is 368 units wide at900+ and otherwise
uses available width; its scroll owns focus reveal.

Preferences default to theme/density and a concise session-scope explanation.
The existing Details toggle reveals noninteractive typography/color/state examples;
control IDs and effect contracts stay the same. Task evidence badges and backend
implementation notices are absent from S13/S14.
