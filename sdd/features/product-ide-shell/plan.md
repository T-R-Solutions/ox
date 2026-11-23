# Plan

Full route: the visual contract, navigation contract and tests change.

D-01 / R-01 (REQ-01): Change only Dark role values in docs/design/tokens.json and
regenerate tokens.rs. Keep navy shell roles as identity; graphite ladder
editor < base/workbench < explorer < recessed. Risk: focus/disabled contrast;
oracle: check_contrast.py and design.rs role tests extended to Menu/Tab.
D-02 / R-02 (REQ-02): New module desktop/chrome.rs owns the bar, menus, status
bar and window title. Menus are an overlay `stack` with a transparent
`mouse_area` backdrop that captures the dismissing press (Iced 0.14 stack and
mouse_area sources inspected). Fixed-width triggers give deterministic anchors
instead of measuring layout. Menu items wrap existing messages (no new effect).
D-03 / R-03 (REQ-03): New module desktop/dock.rs owns document tabs (presentation
state `tabs`) and the bottom dock (`dock_open`, `dock_tool`). Navigate to a tool
surface opens the dock without changing `surface`. The document being left is
registered as a tab; closing the active tab sets the neighbor before navigating
so the closed tab is not re-registered (defect found and fixed by tests).
D-04 / R-04 (REQ-04): views.rs gains info_bar, flat section/note styles,
breadcrumb and reading_width; capability labels drop "· não integrado".
D-05 / R-05 (REQ-05): S01 action tiles, filter id 284 with tracked input, stable
ids derived from the unfiltered index.
D-06 / R-06 (REQ-06): Update four tests whose old contract changed (sidebar
completeness, sidebar-only focus targets, menu trigger focus) and add seven.

Rejected: a new governance successor layer to edit DESIGN.md (maintainer chose a
new document); a single overflow menu (maintainer chose real menus); fixed dock
height (unusable on short windows; replaced by 30 % portion after capture).

Skills consulted (actual entries read 2026-11-18):
- Primary: `.codex/skills/iced-engineering/SKILL.md`, sha256
  3818039d9490dcfc58cedd43bde642a47e352242ef3608971c47fd7544e8d7aa — procedure
  steps 2, 5 and 6: Message/state transitions independent of widgets, verifying
  the selected Iced version's layout/event contracts for the custom overlay,
  and recording missing assistive-technology support as unverified.
- Supporting: `.codex/skills/design-review/SKILL.md`, sha256
  048fe288565eb434f3f8f866c08c11ceed6aacc4a908a2661bfa205b0fcd37e4 — compare the
  same task/state across sizes and themes; report visual inspection separately
  from keyboard/accessibility observations; do not claim improved UX from looks.
- `design-system/SKILL.md` was indicated by AGENTS but not consulted beyond
  the existing token architecture in DESIGN.md §5; no claim of its use.

Verification: build_design --check, check_contrast, cargo fmt/clippy/test,
isolated headless Mutter captures (capture.py, same harness as earlier native
reports) at 1024×700, 1600×1000 and 2560×1080 in Light/Dark/HC and both
densities, check-ox, SDD validate, governance suite and the complete Toolbox run.
