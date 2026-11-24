# Spec — visual-workbench

Spec viva da capacidade `visual-workbench`. Migrada em 2026-11-23 da feature `product-visual-workbench` do modelo
anterior (título original: "Specification: native visual workbench"). Texto original preservado; ACs marcados
`(herdado)` mantêm o estado registrado até 2026-11-23, mas a evidência bruta foi removida e
não sustenta nova aprovação. A task que tocar a capacidade reescreve o AC na forma
`| método: … | esperado: …` e o reavalia. As limitações técnicas foram mantidas; as notas de
controle de evidência do modelo anterior, não.

## O quê e por quê

Authorized by the maintainer's visual development request of 2026-11-11.
Full route: shared presentation contracts, interaction and planned surfaces change.
The existing local Controller/Runtime/Engine remain the functional authority.

No new backend engines, remote providers, persistence, sandbox, commit or publication.
Planned surfaces are native presentation/integration contracts, not delivered engines.

### Start-screen successor — 2026-11-14

The current request selects S01 as a bounded continuation of REQ-02–06. Present an
existing-directory entry point, an honest empty session, and a resume action for
the currently validated directory. R4 entry hierarchy is the primary composition
reference; R11/R12 refine contextual selection. Do not fabricate recent projects,
backend readiness or persisted history. A typed draft is not a validated workspace.
Navigation must remain free of task effects; directory validation keeps its existing
transition to Tasks. The scoped SC-01–04 observations in the successor report support
this delivery without replacing or reducing AC-01–06 above.

### Folder chooser successor — 2026-11-14

The requested S01 action “Escolher pasta…” opens a nonblocking directory dialog.
Confirmation carries the exact selected path into existing validation and opens Tasks
only on success, without execution. Cancellation preserves draft/selection/result.
Failure leaves manual entry available and restores meaningful visible focus.
Only one dialog is owned; stale replies after edits/navigation/close cannot change
current state. Owned dialog cleanup is observed; non-UTF8 paths must not be silently
converted to another path. The 640×480 expanded-details case remains accessible.

Scoped criteria FP-01 integration/paths, FP-02 cancellation/lifecycle, FP-03 native
keyboard/adaptive behavior and FP-04 regression/review/documentation are evaluated
in the successor report without replacing the broader AC-01–06 gates.

### Project welcome successor — 2026-11-14

Explicit user authorization adds only recent-project persistence and empty-directory
creation to REQ-02–06. Earlier prohibitions remain for general persistence/engines.

- WC-01: S01 shows concise Ox introduction, Open folder, New project, Settings and
  honest recent projects. Dedicated neutral entry omits extensive workbench chrome;
  IBM Plex/themes/tokens remain. Narrow window and keyboard retain every action.
- WC-02: Actual successful opens alone enter persistent MRU history, capped at 20,
  deduplicated by canonical absolute UTF-8 path. Last successful open moves to front;
  failed/missing paths do not reorder. Removal changes only history, never project
  files. Restart reloads metadata without opening or executing automatically.
- WC-03: Versioned, bounded history snapshot; cooperating writers serialize each
  read-modify-publish operation under a stable file lock and reread current data.
  Atomic publication and explicit IO errors; corrupt bytes preserved, reset explicit;
  unknown versions refuse writes. Unavailable storage does not prevent opening a
  project but reports that history was not saved. No fake history or evidence data.
- WC-04: New project asks for a single-component name and existing parent directory,
  displays complete destination and consequence (create empty folder and open).
  Explicit Create and open exclusively creates one directory; collisions (including
  symlinks/files) fail without mutation. Cancel before confirmation makes no changes.
  Failure after creation preserves directory and reports it; no destructive rollback.
- WC-05: Open folder reuses supervised picker/validation, cancellation and stale-reply
  guards; manual entry is a secondary disclosed alternative. Recent reopen validates
  again and offers repair/open-other/remove on unavailable paths. Settings uses
  current preferences. No open/create/navigation starts tasks, agents or commands.
- WC-06: Paired real captures, Rust state/filesystem/concurrency tests, actual GUI
  journeys incl restart/unavailable/removal/create/collision/chooser/settings/keyboard,
  themes and 640×480, independent review and validation, source-bound documentation.
  Preserve existing execution/verification flow; distinguish simulated/state/GUI evidence.

The user identified JetBrains IntelliJ IDEA and supplied /tmp/pasted-image-.png
(SHA-256 64a5901d7c862240c763e0010e2b69aee8125dd7cdc8bd7bb4c7926f510ab663).
Its neutral project entry, concise introduction and action grouping inform organization;
version and interactions are not established by the screenshot. .inputs/design
remains organizational inspiration. No pixel-level reproduction is claimed.
These scoped criteria do not replace the broader AC-01–06 gates.

### Welcome identity/layout successor — 2026-11-16

The maintainer requests S01 layout integration of the supplied definitive identity.
WC-01 retains the existing project-entry/actions/real-history contract and now uses
the Catalisador/Valência signature and tagged cotton mascot. Wide identity column,
narrow stacked strip, readable controls, themes and wrapping paths follow DESIGN.
WC-02–05 effects and persistence/confirmation contracts are unchanged. Focused
local observations are recorded in welcome-identity-20261116; they do not replace
WC-06's full independent review/validation matrix or reapprove historical criteria.

### Enterprise desktop successor — 2026-11-16

The maintainer explicitly supersedes the centered 1080-unit welcome card and
240-unit mascot column. S01 adopts window-filling desktop composition: context
chrome, docked project/actions navigation, real recents and a neutral primary
canvas. S02, workbench and preferences share the visual component language.
This changes WC-01's composition clause only; no task effects or persistence
semantics change. The extensive workbench destination list remains unnecessary
on S01. Definitive identity stays intact and subordinate to operations.

Scoped manual criteria EV-01–04 supplement existing gates without replacing them:

- EV-01: Actual native wide and narrow captures show a window-filling project
  shell, readable actions/recents, bounded identity, and reachable overflow.
- EV-02: Shared chrome/navigation/section styling reaches workbench and settings;
  source/captures preserve IBM Plex, semantic palettes and truthful unavailable data.
- EV-03: Focused Rust regressions and native keyboard open/navigation/theme flows
  preserve existing effect boundaries; opening does not execute a task.
- EV-04: Independent review and validation inspect current source, observed inputs,
  documentation and limitations. Broad historical AC/WC acceptance is not renewed
  without its complete scenario matrix.

### Desktop navigation successor — 2026-11-17

User rejects remaining web-like chrome, repeated sidebar icons and mascot.
Preserve DESIGN palette/IBM Plex and signature, existing domain effects and IDs.
Scoped manual criteria DN-01–05 supplement previous criteria without replacing
broad AC/WC matrices or inheriting prior binary acceptance.

- DN-01: Settings at upper right is icon-only with real hover tooltip and a
  visible keyboard focus border; its text appears only on hover as requested.
  Other icon commands/rail provide focus labels. Compact toolbar targets preserve
  readable content at wide and640×480, including Dark/HC. No mascot is rendered.
- DN-02: Each of27 destinations has its own semantic icon; grouping appears once
  per category with stable destination IDs and visual/keyboard order aligned.
- DN-03: A real horizontal divider changes sidebar width by pointer drag within
  safe bounds. Release/outside/focus-loss stops drag; window resize clamps width.
  Narrow windows preserve a usable primary area. Keyboard provides equivalent resize.
- DN-04: Collapse preserves a usable labelled-on-hover/focus icon rail; expand
  restores last width, selected destination and reachable focus. Navigation has
  no domain effects or implicit project/task execution.
- DN-05: Rust tests, real native pointer/keyboard observations, source-bound
  independent review/validation and updated documentation substantiate the slice.

### Project-entry presentation correction — 2026-11-17

User supersedes S01's left-side recents and manual-path menu action. Scoped local
criteria PE-01: every settings entry uses a cog. PE-02: actions follow Novo projeto
→ Abrir pastas… → Clonar repositório, without a manual-path menu action; Clone is
disabled and explicitly unavailable until backend implementation. PE-03: actual
recents and session resumption occupy the primary area beside the actions. The
fixed-sidebar successor supersedes stacking below 900 units: sidebar width is
210 logical units below 900 and 280 otherwise. PE-04: keyboard traversal matches actionable order; chooser-failure
recovery and existing project effects remain unchanged. Broad AC/WC and historical
DN acceptance are not renewed by this bounded local observation.

### Visual baseline successor — 2026-11-17

Future visual changes must follow DESIGN revision 5.0: VISUAL STUDIO 2026 ENTERPRISE
is the primary visual base, with Windows/Fluent guidance adapted to Ox. Documentary
integration is accepted separately in windows-design-baseline. Existing native AC/WC,
DN and PE observations are not reexecuted or renewed by this requirement.

### Fixed-sidebar/settings local successor — 2026-11-17

SS-01: S01 sidebar fills available content height, independently of recent-list
length, with Plugins fixed at the bottom, including narrow windows.
SS-02: Settings/Appearance omit general navigation and unrelated commands.
SS-03: Voltar/Salvar stay at bottom right outside scrolling content. Save retains
preview values for the session and returns to origin; Back/Escape restore the
previous theme/density and return. No plugin backend or durable settings scope.

## Requisitos

- REQ-01: Maintain one English design reference reconciled from supplied v3/v4 sources, preserving institutional Light colors and proposal provenance.
- REQ-02: Provide a native task-first workbench with navigation, shared components, three explicit themes and two densities; settings are session-only.
- REQ-03: Preserve real workspace selection, controlled execution, cancellation, independent verification, freshness and supervised close.
- REQ-04: Provide navigable native compositions for current and documented future capabilities; unavailable backends and demonstration data are explicit.
- REQ-05: Preserve keyboard access, visible focus, readable localized content and adaptive layout without hiding critical actions.
- REQ-06: Record source-bound visual, functional and contrast evidence; distinguish implementation from acceptance and retain previous observations.

## Critérios de aceitação

- AC-01 → REQ-01: Inspect consolidated DESIGN.md, reconciliation and source inventory; legacy values and unresolved proposal status remain traceable. (herdado)
- AC-02 → REQ-02: Exercise theme/density/navigation in native Iced and inspect representative rendered surfaces; no browser CSS runtime or remote service is introduced. (herdado)
- AC-03 → REQ-03: Execute correct/incorrect/missing/stale results and cancellation/close scenarios; actual artifact bytes and direct-child exit remain independent oracles. (herdado)
- AC-04 → REQ-04: Every documented capability has a source-backed destination and integration contract; planned screens never report fabricated backend success or metrics. (herdado)
- AC-05 → REQ-05: Exercise Tab/Shift+Tab, activation, escape and resizing; inspect focus and content at small/large sizes, themes and densities. Assistive-technology support requires separate observation. (herdado)
- AC-06 → REQ-06: Run relevant Rust and documentary checks and record exact inputs/results/limits; inherited F0 acceptance is not transferred to the redesigned GUI. (herdado)

## Estado atual

| AC | Estado | Decidido por (task) | Data |
|---|---|---|---|
| AC-01 | INCONCLUSIVE | modelo anterior (herdado) | ≤ 2026-11-23 |
| AC-02 | INCONCLUSIVE | modelo anterior (herdado) | ≤ 2026-11-23 |
| AC-03 | INCONCLUSIVE | modelo anterior (herdado) | ≤ 2026-11-23 |
| AC-04 | INCONCLUSIVE | modelo anterior (herdado) | ≤ 2026-11-23 |
| AC-05 | INCONCLUSIVE | modelo anterior (herdado) | ≤ 2026-11-23 |
| AC-06 | INCONCLUSIVE | modelo anterior (herdado) | ≤ 2026-11-23 |
| WC-01 | UNVERIFIED | modelo anterior (herdado) | ≤ 2026-11-23 |
| WC-02 | UNVERIFIED | modelo anterior (herdado) | ≤ 2026-11-23 |
| WC-03 | UNVERIFIED | modelo anterior (herdado) | ≤ 2026-11-23 |
| WC-04 | UNVERIFIED | modelo anterior (herdado) | ≤ 2026-11-23 |
| WC-05 | UNVERIFIED | modelo anterior (herdado) | ≤ 2026-11-23 |
| WC-06 | UNVERIFIED | modelo anterior (herdado) | ≤ 2026-11-23 |

## Limites e questões abertas

- No overall acceptance; historical evidence remains stale rather than silently renewed.
- X11, assistive technology, full graphical failure matrix and remaining future-widget depth need further work.
- 2026-11-14 S01 continuation has scoped SC-01–04 approval; wider feature AC coverage remains incomplete. Final Wayland captures at two sizes/scale1 and focused tests do not approve X11, assistive technology, fractional DPI or historical F0 performance.
- 2026-11-14 folder-picker continuation changes S01 inputs. Original S01 scoped observation preserved in historical_evidence and folder-picker before-docs; new dependent observation required.
- Folder-picker GTK native observations use test-only portal/a11y/settings overrides; no default portal, X11, AT, fractional DPI or startup performance acceptance.
- 2026-11-14 welcome/projects successor changes contracts and product sources; folder-picker observation retained unchanged in historical_evidence, no inherited acceptance. WC-01–06 await new source/test/native/independent observations.
- 2026-11-15 native-input-enter-review reproduced unintended creation from Enter after mouse input focus; WC-04/05 remain INCONCLUSIVE pending correction and replay. Raw counterevidence preserved.
- 2026-11-15 final scoped WC-01–06 APPROVED after independent source/native/document validation; original six ACs remain INCONCLUSIVE. Initial GUI Enter inference was corrected because first pointer click was lost; delivered-pointer final replay passed. Closure changes only verdict/document bindings, not historical execution identities.
- 2026-11-16 welcome identity/layout: S01 sources and PNG support changed. Focused local Rust/native observations (evidência removida em 2026-11-23; histórico Git) do not renew WC-01–06 or wider feature acceptance; historical evidence remains unchanged.
- 2026-11-16 enterprise desktop redesign changes presentation inputs; scoped EV-01–04 observations and independent verdicts are recorded (evidência removida em 2026-11-23; histórico Git) Historical AC/WC gates remain unchanged and are not reaccepted by this focused delivery.
- 2026-11-17 desktop navigation changes presentation/interaction inputs. Scoped DN-01–05 observation is (evidência removida em 2026-11-23; histórico Git); previous enterprise and broad AC/WC observations remain bound to their historical inputs.
