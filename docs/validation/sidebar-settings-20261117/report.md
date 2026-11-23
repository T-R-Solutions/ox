# Fixed sidebar and settings — 2026-11-17

Local route authorized by the maintainer's request: full-height welcome sidebar,
Plugins at its bottom, Settings without those navigation options, Save and Back
at bottom right. Root owns desktop.rs, desktop/views.rs and affected documentation;
existing edits preserved. Known consumers, recoverable session-only changes and
existing state/widget/native oracles justify local execution. No delegation or
independent-validation claim. No new persistence, plugin runtime integration,
download, complete scanner run, commit or publication.

## Criteria and manual assessment

- SS-01 APPROVED within observed sizes: final-wide/initial.png (1366×768) and
  final-small/initial.png (640×480) show the actions sidebar filling the content
  height, from below shared chrome to the status footer. Plugins is fixed at the
  bottom. Its pointer activation opens the existing Tools surface (plugins.png).
  Source inspection confirms separate scroll regions for actions and projects.
  Narrow windows retain a 210-unit sidebar rather than the previous stacked layout.
- SS-02 APPROVED within observed settings: settings.png in both final runs shows
  the dedicated settings surface without the workbench menu/chrome or project
  actions. Settings keyboard controls contain only theme, density, Back and Save.
- SS-03 APPROVED within observed session scope: settings.png and save-focused.png
  show fixed bottom-right actions, including at 640×480 with overflowing content.
  Native keyboard activation previews Dark, Escape returns to Light, Save returns
  to the welcome page in Dark, and reopening retains Dark (settings-reopened.png).
  The Rust regression separately verifies Back restores both theme/density,
  Save retains values, Escape restores the last saved state and no task starts.
  Source inspection confirms return to the originating surface. Settings values
  are deliberately session-only; these results do not imply restart persistence.

## Observed inputs and verification

Linux x86_64, Iced 0.14.0, tiny-skia, private Mutter Wayland, scale 1. Disposable
project and history fixtures belong exclusively to each native run. Exact native
source hashes and binary SHA256 are in final-wide/result.json and
final-small/result.json; both report stable sources/binary and natural exit 0.
Final binary: e1ee54f19ab1d9ea88a7f8db16c381fe8046b8fe8f73190f075e46b696051e46.

Commands, from the repository root with
CARGO_HOME="$PWD/.cache/ox/cargo-home" for Cargo:

```bash
cargo fmt --manifest-path application/Cargo.toml --all -- --check
cargo test --manifest-path application/Cargo.toml --offline --locked -p ox-ui
cargo clippy --manifest-path application/Cargo.toml --offline --locked -p ox-ui --all-targets -- -D warnings
cargo build --manifest-path application/Cargo.toml --offline --locked -p ox-app --bin ox
python3 docs/validation/sidebar-settings-20261117/native-layout.py --name final-wide --capture-only
python3 docs/validation/sidebar-settings-20261117/native-layout.py --name final-small --monitor 640x480 --capture-only
```

Final commands exit 0: 47 unit tests, four integration tests and one shell contract
pass; one subprocess helper intentionally ignored directly. Logs: rust-test.log,
clippy.log. Root inspected both final sizes, Settings and saved-state captures,
and wide plugin activation/reopened Settings. Formatter and build pass.
The first compile caught an Element width API misuse, corrected before tests.
An existing keyboard-tail assertion exposed Plugins ordering after recents;
Plugins was moved before the main-project controls to follow visual regions.
The initial sandbox native attempt failed on a socket collision (wide/result.json);
subsequent native execution used approved host access in a private compositor.
wide-native is preliminary, preceding the final keyboard-focus correction/build;
it is preserved and superseded by final-wide/final-small.

The helper's inherited pixel_sidebar_edges estimator is calibrated for the old
workbench rail, not this layout; its inferred values are not used as an acceptance
oracle. Actual screenshots, source composition, widget regressions and native
interactions above support this local assessment. No full theme/density/platform,
assistive-technology, huge recent-list or full project-create/open native matrix
was reexecuted. No broad acceptance is inferred from successful capture/process exit.

## Documentation disposition

Reviewed and updated DESIGN.md, docs/design/surfaces.md, application/README.md,
sdd/project.md and product-visual-workbench spec/plan/tasks/converge: docked sidebar,
narrow-width successor, isolated Settings, fixed actions and session preview semantics.
Reviewed constitution, architecture/context.md, windows-design-baseline ADR,
reference-coverage.md and components.md: no asset provenance, component token,
domain integration, persistence format or architecture change; existing contracts
remain applicable. Existing broad evidence.json AC/WC states are unchanged; earlier
PE/DN/EV input-bound observations are historical and not renewed by this local slice.

Consulted/applied iced-engineering/SKILL.md and native-visual-contract.md from the
live checkout on 2026-11-17: bounded Fill layout, state/message transitions,
visible keyboard targets and native source-bound observations. Visual source:
Visual Studio 2026 Enterprise, DESIGN revision 5.0 and Windows analysis dated
2026-11-17; adopted docked auxiliary panel/fixed actions, adapted to Iced widgets,
opaque theme roles and Linux window chrome; Windows materials/platform-specific
APIs remain deferred. SS-01–03 are a bounded manual assessment, not an automated
feature approval gate or independent validation.
