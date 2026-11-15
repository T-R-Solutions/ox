# Current and planned surface contracts

Product requirements originate in architecture and product feature contracts; prototype IDs are presentation detail, not new backend authorization. Each `Surface::dependency()` names the integration prerequisite.

| Capability | Requirement source | Flow | Screen/component | Backend state | Visual delivery |
|---|---|---|---|---|---|
| S01 Central de projetos | `sdd/features/product-local-task-ui/spec.md` | select → execute → verify → inspect | `Surface::Start` / desktop/views.rs | local Controller integrated | native controls/evidence |
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
| S13 Preferências | `docs/architecture/context.md` | navigate → inspect contract → return | `Surface::Settings` / desktop/views.rs | session presentation | native preferences |
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
