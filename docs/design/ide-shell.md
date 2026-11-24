# Ox IDE shell — Visual Studio 2026 reference, Ox identity

Revision **ide-shell-1**, 2026-11-18. Spec:
[ide-shell](../../sdd/specs/ide-shell.md). Evidence: native captures by the implementing
agent at 1024×700, 1600×1000 and 2560×1080 (Mutter, scale 1); the acceptance state
is in the spec.

This document is the current native contract for the workbench shell, the
project entry (S01) and the Dark theme values. It complements
[DESIGN.md](../../DESIGN.md) revision 5.0, which keeps the reusable rules
(identity, semantic roles, truth states, accessibility). Where the two disagree
about the shell geometry or controls listed under "Superseded statements" below,
this document describes the implemented behavior. The pinned documents could not
be edited in this task because governance authenticates their exact bytes; see
the limitation at the end.

## Reference and identity

The maintainer asked for VISUAL STUDIO 2026 ENTERPRISE as a **model to analyze,
not to copy**: Ox must keep its own identity. Sources are the three public
VS 2026 images and release notes already recorded in
[the Windows design analysis](windows-apps-analysis.md#visual-studio-reference).
No Microsoft asset, mark, palette value or undocumented dimension was copied.

| VS 2026 trait | Ox decision | Status |
| --- | --- | --- |
| Merged title/menu bar with a central search | 48-unit command bar: panel toggle, OX signature 128×40, menus Arquivo · Exibir · Ferramentas, centered "Ir para uma tela… Ctrl+K", project selector, tool-dock toggle, settings cog | Adopted, adapted |
| Neutral gray shell | **Kept the OX navy brand chrome** (`shell_bg`) in every theme; only the work area is neutral | Deliberate deviation (identity) |
| Document well with tabs | Document tabs above the primary canvas, active marker on the top edge, close per tab, last tab not closable, at most 8 | Adopted |
| Bottom tool windows (Error List, Output, Terminal) | Bottom dock with Problemas · Testes · Rastro de execução · Terminal; Ctrl+J; 30 % of the work area | Adopted |
| Solution Explorer | "Explorador" sidebar with grouped destinations only (19), no tool windows or preferences | Adapted |
| Info bar | One page-level availability banner (icon, accent stripe, recessed surface) | Adapted |
| Status bar | Operation state on the left, real project name on the right; no theme, density or surface codes | Adapted |
| Start window tiles | S01 actions as tiles with icon, title and one-line consequence; recents filter | Adapted to the user-chosen fixed sidebar |
| Dark theme gray | Graphite work area with a slight cool tint, navy chrome, saturated blue primary with white text | Adapted |
| Pinned tabs, resizable dock, collapsible groups, preview tabs | Not implemented | Deferred |

## Geometry and composition

- Command bar 48 units (padding 4 + 40-unit signature). Menu triggers have a
  fixed 84-unit width so the dropdown anchors at a deterministic x
  (184 + index × 86); dropdown width 320 with an overlay shadow.
- Below 1180 units the go-to field collapses to the search icon; below 900 the
  project selector shows only its icon (full path in the tooltip).
- Sidebar: header "EXPLORADOR", sentence-case group labels, thin neutral
  scrollbar (6 units), divider neutral at rest and accent only while hovered or
  dragged. Width rules (200–420, rail 52, Ctrl+B) are unchanged.
- Primary canvas uses `surface_base`; pages keep a 1200-unit reading width and
  S05 forms 880; Editor, Focus and Architecture use the full width. S01 recents
  use 880.
- Sections are flat (heading, caption, separator); notes are recessed without a
  frame; cards and duplicated notices were removed.
- Bottom dock takes 30 % of the work area (`FillPortion` 3 : 7) and is hidden
  in Modo de foco.

## Controls, ids and keyboard

| Ids | Control |
| --- | --- |
| 212 | navigation toggle (first in traversal) |
| 600–602 | menus Arquivo, Exibir, Ferramentas |
| 610–613, 620–627, 630–635 | menu items |
| 213 | go to (command palette) |
| 603 | project selector → Central de projetos |
| 644 / 645 | toggle / hide the tool dock |
| 640–643 | dock tabs |
| 500 + 2·i / 501 + 2·i | select / close document tab of `Surface::ALL[i]` |
| 284 | S01 recents filter (text input `recent-filter`) |

Removed from the chrome: theme (210), density (211), details (0), Sair (1) and
the sidebar ±24 buttons (215/216). Their messages remain and are reached from
Exibir/Arquivo, Ctrl+B and Ctrl+Alt+←/→. Sair now requires opening Arquivo.

Menus are modal for traversal: ↑/↓ move, Enter runs the item, Escape or a click
outside closes and returns focus to the trigger. The transparent backdrop
consumes the dismissing click, so it never activates the control below.
Navigating to Problemas/Testes/Rastro/Terminal opens the dock on that tab and
keeps the current document; it never starts or cancels work.

## Content rules

- The task evidence badge appears only on Visão do projeto, Tarefas, Atividade
  e evidências, Falhas e recuperação and the Testes/Rastro dock header.
- A breadcrumb ("Capacidades › Ferramentas e plugins") replaces the uppercase
  group label above the title.
- Unavailable actions keep their plain verb ("Planejar tarefa") and show the
  reason beside them; the dependency is stated once in the info bar.
- Window title: "{place} — {project} — Ox" (validation label appended when set).

## Dark theme values

Changed roles only (Light and High Contrast unchanged): shell `#1A2B40`/`#111C2A`,
workbench and base `#1B1E23`, explorer `#202329`, editor `#16191E`, recessed
`#272B32`, selected `#22384F`, text `#E6E9EE`/`#BAC1CB`/`#A4ACB7`, borders
`#353A42`/`#4B525C`/`#808A97`, action `#2F6DB3`/`#255C9A` with white text, focus
and selection marker `#8EC2F5`, neutral category/unknown backgrounds. The source
is [tokens.json](tokens.json); `check_contrast.py` reports 0 failures across all
114 checked pairs.

## Superseded statements in pinned documents

The following statements remain in exact-byte-pinned documents and now describe
the previous shell. They are superseded for current behavior by this document:

- DESIGN.md "Desktop navigation successor": workbench top chrome is 56 units;
  sidebar shrink/grow buttons support Tab/Enter; 27 destinations in the
  navigation; "The chrome also includes Sair" (also components.md).
- DESIGN.md §7 "56-unit context chrome (52 in Compact)".
- components.md "Navigation — all 27 destinations", "Controls 215/216", the
  editor tool strip (DemoTool 260–262), and "toolbar theme/density shortcuts".
- surfaces.md "Project-entry correction": the action label "Abrir pastas…"
  (now "Abrir pasta…").
- DESIGN.md §4/§5 Dark candidate values implied by the earlier navy work area.

## Limitations

- The DESIGN.md, surfaces.md, components.md and product-visual-workbench
  convergence was not done: governance pins then required a new successor layer,
  which the maintainer declined (`ea3cf0f:tools/governance/scripts/document_ledger.py`;
  the pins were removed later).
- High Contrast disabled buttons remain visually close to enabled ones
  (existing `text_muted` value); the adjacent reason text states availability.
- Iced 0.14 has no AccessKit bridge here; menus, tabs and dock have
  application-managed focus only. Screen-reader behavior is not established.
- Captures come from an isolated headless Mutter session at scale 1; other
  compositors, scales and human preference were not observed.
