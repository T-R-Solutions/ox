# Specification: native visual workbench

Authorized by the maintainer's visual development request of 2026-11-11.
Full route: shared presentation contracts, interaction and planned surfaces change.
The existing local Controller/Runtime/Engine remain the functional authority.

- REQ-01: Maintain one English design reference reconciled from supplied v3/v4 sources, preserving institutional Light colors and proposal provenance.
- REQ-02: Provide a native task-first workbench with navigation, shared components, three explicit themes and two densities; settings are session-only.
- REQ-03: Preserve real workspace selection, controlled execution, cancellation, independent verification, freshness and supervised close.
- REQ-04: Provide navigable native compositions for current and documented future capabilities; unavailable backends and demonstration data are explicit.
- REQ-05: Preserve keyboard access, visible focus, readable localized content and adaptive layout without hiding critical actions.
- REQ-06: Record source-bound visual, functional and contrast evidence; distinguish implementation from acceptance and retain previous observations.
- AC-01 → REQ-01: Inspect consolidated DESIGN.md, reconciliation and source inventory; legacy values and unresolved proposal status remain traceable.
- AC-02 → REQ-02: Exercise theme/density/navigation in native Iced and inspect representative rendered surfaces; no browser CSS runtime or remote service is introduced.
- AC-03 → REQ-03: Execute correct/incorrect/missing/stale results and cancellation/close scenarios; actual artifact bytes and direct-child exit remain independent oracles.
- AC-04 → REQ-04: Every documented capability has a source-backed destination and integration contract; planned screens never report fabricated backend success or metrics.
- AC-05 → REQ-05: Exercise Tab/Shift+Tab, activation, escape and resizing; inspect focus and content at small/large sizes, themes and densities. Assistive-technology support requires separate observation.
- AC-06 → REQ-06: Run relevant Rust and documentary checks and record exact inputs/results/limits; inherited F0 acceptance is not transferred to the redesigned GUI.

No new backend engines, remote providers, persistence, sandbox, commit or publication.
Planned surfaces are native presentation/integration contracts, not delivered engines.

## Start-screen successor — 2026-11-14

The current request selects S01 as a bounded continuation of REQ-02–06. Present an
existing-directory entry point, an honest empty session, and a resume action for
the currently validated directory. R4 entry hierarchy is the primary composition
reference; R11/R12 refine contextual selection. Do not fabricate recent projects,
backend readiness or persisted history. A typed draft is not a validated workspace.
Navigation must remain free of task effects; directory validation keeps its existing
transition to Tasks. The scoped SC-01–04 observations in the successor report support
this delivery without replacing or reducing AC-01–06 above.

## Folder chooser successor — 2026-11-14

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

## Project welcome successor — 2026-11-14

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

## Welcome identity/layout successor — 2026-11-16

The maintainer requests S01 layout integration of the supplied definitive identity.
WC-01 retains the existing project-entry/actions/real-history contract and now uses
the Catalisador/Valência signature and tagged cotton mascot. Wide identity column,
narrow stacked strip, readable controls, themes and wrapping paths follow DESIGN.
WC-02–05 effects and persistence/confirmation contracts are unchanged. Focused
local observations are recorded in welcome-identity-20261116; they do not replace
WC-06's full independent review/validation matrix or reapprove historical criteria.

## Enterprise desktop successor — 2026-11-16

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
