# Current and planned surface contracts

Product requirements originate in architecture and product feature contracts; prototype IDs are presentation detail, not new backend authorization. Each `Surface::dependency()` names the integration prerequisite.

## Current interaction rules — 2026-11-17 correction

S01 has a fixed 280-unit actions sidebar (210 below 900 logical units), with an
independent `welcome-sidebar` scroll region; recent projects scroll in `main`.
These dimensions supersede the historical stacking compositions below. A failed
folder chooser reveals and focuses the manual path field in the actions sidebar.
Cancel and stale replies preserve the prior project and verification state.
S02 chooser errors retain its existing parent-path input.

S13/S14 reveal focused theme/density controls in their own `main` scroll region;
Voltar/Salvar remain fixed. Navigation shortcuts apply to workbench surfaces and
respect captured text-input events. Pointer motion is subscribed only during an
active divider drag; release, cursor exit, window defocus and resize end the drag.
These are source/unit-test observations, not renewed native or assistive-technology
acceptance. Visual composition remains DESIGN revision 5.0, Visual Studio 2026
Enterprise; no artwork or visual baseline changes are introduced by this repair.

## Surface inventory

| Capability | Requirement source | Flow | Screen/component | Backend state | Visual delivery |
|---|---|---|---|---|---|
| S01 Boas-vindas | `product-visual-workbench` welcome successor | choose/create/reopen → validate/open project | `Surface::Start` / desktop/views.rs + project_store.rs | bounded project metadata and creation; no task execution on S01 | native project entry |
| S02 Novo projeto | `product-visual-workbench` welcome successor | name + parent → confirm → exclusive create → validate/open | `Surface::NewProject` / desktop/views.rs + project_store.rs | bounded local empty-directory creation | native form and explicit consequence |
| S03 Visão do projeto | `sdd/features/product-local-task-ui/spec.md` | select → execute → verify → inspect | `Surface::Project` / desktop/views.rs | local Controller integrated | native controls/evidence |
| S04 Tarefas | `sdd/features/product-local-task-ui/spec.md` | select → execute → verify → inspect | `Surface::Tasks` / desktop/views.rs | local Controller integrated | native controls/evidence |
| S05 Criar tarefa | `docs/architecture/context.md` | navigate → inspect contract → return | `Surface::NewTask` / desktop/views.rs | planned backend | native composition, unavailable action + dependency |
| S06 Atividade e evidências | `sdd/features/product-local-task-ui/spec.md` | select → execute → verify → inspect | `Surface::Activity` / desktop/views.rs | local Controller integrated | native controls/evidence |
| S07 Decisões e permissões | `docs/architecture/context.md` | navigate → inspect contract → return | `Surface::Decisions` / desktop/views.rs | planned backend | native composition, unavailable action + dependency |
| S08 Agentes | `docs/architecture/context.md` | navigate → inspect contract → return | `Surface::Agents` / desktop/views.rs | planned backend | native composition, unavailable action + dependency |
| S09 Configurar agente | `docs/architecture/context.md` | navigate → inspect contract → return | `Surface::AgentSettings` / desktop/views.rs | planned backend | native composition, unavailable action + dependency |
| S10 Modelos e provedores | `docs/architecture/context.md` | navigate → inspect contract → return | `Surface::Providers` / desktop/views.rs | planned backend | native composition, unavailable action + dependency |
| S11 Contexto e conhecimento | `docs/architecture/context.md` | navigate → inspect contract → return | `Surface::Context` / desktop/views.rs | planned backend | native composition, unavailable action + dependency |
| S12 Ferramentas e plugins | `docs/architecture/context.md` | navigate → inspect contract → return | `Surface::Tools` / desktop/views.rs | planned backend | native composition, unavailable action + dependency |
| S13 Configurações | `docs/architecture/context.md` | navigate → inspect contract → return | `Surface::Settings` / desktop/views.rs | session presentation | native preferences |
| S14 Aparência | `docs/architecture/context.md` | navigate → inspect contract → return | `Surface::Appearance` / desktop/views.rs | session presentation | native preferences |
| W00 Editor e arquivos | `docs/architecture/context.md` | navigate → inspect contract → return | `Surface::Editor` / desktop/views.rs | planned backend | native composition, unavailable action + dependency |
| A01 Arquitetura | `docs/architecture/context.md` | navigate → inspect contract → return | `Surface::Architecture` / desktop/views.rs | planned backend | native composition, unavailable action + dependency |
| A02 Orquestração | `docs/architecture/context.md` | navigate → inspect contract → return | `Surface::Orchestration` / desktop/views.rs | planned backend | native composition, unavailable action + dependency |
| A03 Observabilidade | `docs/architecture/context.md` | navigate → inspect contract → return | `Surface::Observability` / desktop/views.rs | planned backend | native composition, unavailable action + dependency |
| A04 Revisão de alterações | `docs/architecture/context.md` | navigate → inspect contract → return | `Surface::Review` / desktop/views.rs | planned backend | native composition, unavailable action + dependency |
| A05 Falhas e recuperação | `sdd/features/product-local-task-ui/spec.md` | select → execute → verify → inspect | `Surface::Recovery` / desktop/views.rs | local Controller integrated | native controls/evidence |
| A06 Modo de foco | `docs/architecture/context.md` | navigate → inspect contract → return | `Surface::Focus` / desktop/views.rs | planned backend | native composition, unavailable action + dependency |
| TW01 Problemas | `docs/architecture/context.md` | navigate → inspect contract → return | `Surface::Problems` / desktop/views.rs | planned backend | native composition, unavailable action + dependency |
| TW02 Testes | `sdd/features/product-local-task-ui/spec.md` | select → execute → verify → inspect | `Surface::Tests` / desktop/views.rs | local Controller integrated | native controls/evidence |
| TW03 Rastro de execução | `sdd/features/product-local-task-ui/spec.md` | select → execute → verify → inspect | `Surface::Trace` / desktop/views.rs | local Controller integrated | native controls/evidence |
| TW04 Terminal | `docs/architecture/context.md` | navigate → inspect contract → return | `Surface::Terminal` / desktop/views.rs | planned backend | native composition, unavailable action + dependency |
| SDD Desenvolvimento SDD | `docs/architecture/context.md` | navigate → inspect contract → return | `Surface::Sdd` / desktop/views.rs | planned backend | native composition, unavailable action + dependency |
| SKL Skills do projeto | `docs/architecture/context.md` | navigate → inspect contract → return | `Surface::Skills` / desktop/views.rs | planned backend | native composition, unavailable action + dependency |

Domain integration must supply stable identities, snapshots, operation lifecycle and explicit errors through messages. Navigation never initiates domain effects. Demonstrations (embedded source, diff and documentary graph) are labelled and never read as project data. New general tasks, providers, plugins, SDD parsing and graph queries remain unavailable; no successful execution is simulated.

Composition successor: W00/A06 now share selectable embedded files, tabs, code,
inspector and tool strip. A01 uses a directional dependency map; S08/S09/A02 share
a role table. These are functioning presentation controls, not document/graph/agent
backend integration. Source dispositions are in reference-coverage.md.

Start-screen successor (2026-11-14): S01 has a dedicated existing-directory form
and a session-context inspector. Validation uses the existing Controller and opens
S04 on success. Editing the path invalidates selection; rejected paths display
repairable inline feedback. A validated session offers task resumption; Activity
and Appearance remain reachable. There is no persisted recent-project list. The
inspector stacks below the form at narrow widths; no task is executed by navigation.
Scoped observations: [start-screen report](../validation/start-screen-20261114/report.md).

S01 folder-picker successor: “Escolher pasta…” shares the path-input row and keyboard
order input → chooser → validate. The optional installed Zenity GTK helper runs under
a supervised worker; confirm reuses Controller validation, cancel preserves state,
and late replies cannot apply after context invalidation. Manual entry remains usable
when the helper is unavailable. Native coverage is recorded in the folder-picker
report; support of other desktops or assistive technologies is not inferred.

Welcome/projects successor (2026-11-14): S01 is a dedicated neutral project entry
with restrained Ox identity, Settings, Open folder/New project and real recent paths.
The extensive workbench navigation/toolbar/status is absent on S01/S02; manual input
is disclosed on request. S02 creates one empty child directory only after explicit
confirmation with name, existing parent and destination. Recent metadata persists
locally with MRU/canonical deduplication/cap 20 and removal without project deletion.
Unknown/corrupt storage and unavailable project paths have recoverable diagnostics;
reset is explicit and preserves bounded corrupted bytes. Opening/creating does not
execute tasks. Settings/theme remain session-only; general persistence is unchanged.
Current evidence: [welcome report](../validation/welcome-projects-20261114/report.md).
The earlier session-only S01/form composition above is historical.

Welcome identity/layout successor (2026-11-16): Historical S01 embedded the supplied definitive
signature (Catalisador/Valência) and tagged cotton mascot; the 17 November
successor retains only the signatures at runtime. A 240-unit navy identity
column accompanies the primary actions and recent list inside a 1080-unit maximum
reading surface. Below 900 logical units the identity stacks as a compact strip.
The body scrolls, long paths wrap and focused controls retain the existing reveal
operation. S01/S02 share the concise “Central de projetos” header and Settings.
The empty-list explanation is shown only after loading succeeds; unavailable
history retains its diagnosis/reset controls. Effects, history format and creation
confirmation are unchanged. [Scoped native observations](../validation/welcome-identity-20261116/report.md).

Enterprise desktop successor (2026-11-16): supersedes the preceding welcome
identity geometry. S01 fills the window with context chrome, docked actions/recents
and neutral primary canvas; compact identity is subordinate. The later fixed sidebar uses 280 units, or 210 below 900 logical units. S02 uses a docked scrollable form.
Shared workbench navigation, sections and preferences adopt flat separators and
consistent chrome. Effects/availability/history and confirmation remain governed
by existing contracts. Current observations: [enterprise report](../validation/enterprise-visual-20261116/report.md).

S13/S14 enterprise refinement: normal preferences contain session scope, theme
and density with preview/Save/Back. There are no Details specimens. No task-evidence
badge or backend-integration notice is shown in this presentation-only flow.

Desktop navigation successor (2026-11-17): S01/S02 use icon-only Settings and no
mascot. Workbench chrome is a compact icon strip with hover/focus labels; 27
destinations use 26 icon geometries (S09/S13 share the cog), grouped once. Sidebar divider permits horizontal
drag with safe bounds; rail 52 preserves navigation when collapsed and expansion
restores preferred width. Keyboard shrink/grow controls and Ctrl+B remain local
presentation interactions with no domain effects.

S01 project-entry correction (2026-11-17): docked actions are Novo projeto, Abrir
pastas… and disabled Clonar repositório (unavailable tooltip). The separate manual
path action is removed; a field is disclosed automatically on chooser failure.
Recents and current-project resumption move to the primary area beside the fixed actions sidebar, including narrow windows. All settings icons share the cog. Effects/history unchanged.
Scoped observations: [entry report](../validation/project-entry-20261117/report.md).

## Visual Studio 2026 Enterprise target — 2026-11-17

All listed surfaces follow DESIGN revision 5.0 for future visual changes.
S01/S02 adopt a professional project-entry hierarchy; W00/A06 use the central
artifact workspace with tabs and contextual panes; S03–S14/SDD/SKL use compact
navigation, forms and data-oriented views; A01–A05/TW retain specialized content
inside the same shell. The mandatory base is **VISUAL STUDIO 2026 ENTERPRISE**.
The [source analysis](windows-apps-analysis.md) covers supporting Windows guidance.
This is target direction only: existing implementation rows and backend availability
above are unchanged, and no new native parity observation is claimed.

S01 fixed sidebar successor (2026-11-17): docked full content-height sidebar,
Plugins at the bottom, independently scrolling actions/projects. At widths below
900 the sidebar uses 210 units instead of stacking. S13/S14 omit general navigation
and keep Voltar/Salvar fixed at bottom right. Save confirms session-only preview
and returns to the originating surface; Back/Escape discard it. Plugins opens the
existing Tools destination and retains its explicit integration limits.
