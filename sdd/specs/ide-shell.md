# Spec — ide-shell

Spec viva da capacidade `ide-shell`. Migrada em 2026-11-23 da feature `product-ide-shell` do modelo
anterior (título original: "Product IDE shell"). Texto original preservado; ACs marcados
`(herdado)` mantêm o estado registrado até 2026-11-23, mas a evidência bruta foi removida e
não sustenta nova aprovação. A task que tocar a capacidade reescreve o AC na forma
`| método: … | esperado: …` e o reavalia. As limitações técnicas foram mantidas; as notas de
controle de evidência do modelo anterior, não.

## O quê e por quê

Authorized 2026-11-18 by the maintainer: implement the visual analysis proposals
(task log entry 2026-11-18T06:59:21-03:00) using VISUAL STUDIO 2026 ENTERPRISE
as a reference model only, keeping an Ox identity. Decisions taken by the
maintainer: own command menus (Arquivo, Exibir, Ferramentas); keep the 128×40
signature in a 48-unit bar; rename "Abrir pastas…" to "Abrir pasta…"; run the
complete Toolbox verification; record the contract in a new
`docs/design/ide-shell.md` and this feature without editing hash-pinned documents
or governance code.

Actors: desktop user (pointer and keyboard); maintainer (visual acceptance).
Invariants: navigation, menus, tabs and the dock never start, cancel or approve
domain work; demonstrations stay labelled; unknown is not success; IBM Plex,
OX signature artwork and semantic roles are preserved; Light and High Contrast
token values are unchanged.

Out of scope: editing DESIGN.md, docs/design/surfaces.md, docs/design/components.md,
(registro do modelo anterior, removido em 2026-11-23) and product-visual-workbench records (exact-byte pins);
pinned tabs, resizable dock, collapsible groups, AccessKit, persistence of shell
state, and the stale `#[ignore]` X11 tests/native review scripts of earlier tasks.

## Requisitos

- REQ-01: Dark theme uses a neutral graphite work area under the OX navy chrome with coherent depth, generated native roles and passing contrast pairs.
- REQ-02: Workbench chrome is a 48-unit command bar with own menus, a go-to field, project selector, tool-dock toggle and settings; theme/density/details/Sair leave the icon strip; window title and status bar carry only place, project and operation state.
- REQ-03: Destinations open as document tabs; tool windows (Problemas, Testes, Rastro, Terminal) open in a bottom dock; the sidebar lists only document destinations; every destination remains reachable.
- REQ-04: Pages present one availability banner, flat sections, a breadcrumb, scoped evidence badge and bounded reading width.
- REQ-05: Project entry (S01) keeps the maintainer's fixed sidebar with descriptive action tiles, visible clone unavailability, a flat Plugins entry, a recents filter with stable ids and an explicit empty state.
- REQ-06: Existing automated checks remain green and the complete verification result is recorded with any failures.
- REQ-07: The maintainer judges whether the result follows the reference while keeping Ox identity.

## Critérios de aceitação

- AC-01 → REQ-01: tokens.json and tokens.rs agree (build_design --check exit 0); check_contrast reports 0 failures; design.rs focus/contrast tests pass for Menu and Tab roles in every theme. (herdado)
- AC-02 → REQ-02: menu traversal is modal; Escape and outside click close and return focus to the trigger without executing an item; items dispatch existing messages; title omits theme/density; captures show the bar at 1024, 1600 and 2560 widths. (herdado)
- AC-03 → REQ-03: tabs open/activate/close, the last tab is not closable, at most 8; dock navigation keeps the document and execution state; Ctrl+J toggles; every Surface is reachable through sidebar, menus or palette. (herdado)
- AC-04 → REQ-04: the dependency notice appears once; the badge shows only on task surfaces; the measured page content is ≤ 1200 units at 2560 while the editor uses the full width. (herdado)
- AC-05 → REQ-05: filtered recents keep MRU order and ids; filter is in traversal only with recents; captures show tiles, "Em breve" tag and empty state. (herdado)
- AC-06 → REQ-06: cargo fmt, default clippy and workspace tests pass; the complete Toolbox run is executed and its result recorded; pre-existing failures are distinguished from new ones. (herdado)
- AC-07 → REQ-07: maintainer visual acceptance of the captures or the running app. (herdado)

## Estado atual

| AC | Estado | Decidido por (task) | Data |
|---|---|---|---|
| AC-01 | INCONCLUSIVE | modelo anterior (herdado) | ≤ 2026-11-23 |
| AC-02 | APPROVED | modelo anterior (herdado) | ≤ 2026-11-23 |
| AC-03 | INCONCLUSIVE | modelo anterior (herdado) | ≤ 2026-11-23 |
| AC-04 | INCONCLUSIVE | modelo anterior (herdado) | ≤ 2026-11-23 |
| AC-05 | INCONCLUSIVE | modelo anterior (herdado) | ≤ 2026-11-23 |
| AC-06 | INCONCLUSIVE | modelo anterior (herdado) | ≤ 2026-11-23 |
| AC-07 | APPROVED | modelo anterior (herdado) | ≤ 2026-11-23 |

## Limites e questões abertas

- No AccessKit bridge; screen-reader behavior unverified.
- Single compositor, scale 1.
- Pedantic clippy failures pre-exist in unchanged code.
- 2026-11-19 UI02: four stale source-bound observations moved intact to history. Maintainer V2 and E-TOKENS remain unchanged and fresh. Only AC02/AC07 retain supported current decisions; other criteria remain unapproved. Hashbrown and task blockers are not waived.
