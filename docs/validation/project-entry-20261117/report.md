# Project-entry presentation correction — 2026-11-17

Local route, authorized by the supplied screenshot and explicit user feedback.
Root owns desktop.rs, desktop/views.rs, desktop/icons.rs and the affected docs.
Known consumers and recoverable presentation changes introduce no material domain,
authorization, persistence, concurrency or compatibility change. Existing working
changes were preserved. No delegation or independent-validation claim.

## Criteria and observations

- PE-01: Source inspection and native wide/small captures show a cog at Settings.
  The shared renderer covers header, toolbar, Settings destination and agent settings.
  No font-dependent settings glyph remains. Destination variants are source-inspected;
  not every destination was separately captured.
- PE-02: Wide/small initial captures show Novo projeto → Abrir pastas… → Clonar
  repositório, without the manual-path menu action. Clone has no activation message
  and an unavailable hover tooltip. It is an entry only, not Git functionality.
- PE-03: Captures with an actual disposable directory and isolated recent metadata
  show its row in the primary area; 640×480 stacks actions before projects and wraps
  the long path. Source inspection places current-session resumption there too.
  Empty-history rendering is in desktop-navigation-20261117/entry-refinement-wide.
- PE-04: Existing widget-click, input-focus, error/cancel/stale-reply, history and
  task-boundary tests pass. The keyboard-order regression now checks New then Open,
  skips disabled Clone and preserves the automatic chooser-failure input. Native
  capture-only replay also traversed Settings and navigated workbench/home. No new
  full open/create/resume native journey or assistive-technology claim is made.

During implementation, the existing input-event regression detected a zero-height
fallback field caused by a Fill-height child in unbounded scrolling content. Using
intrinsic child height corrected it; the actual click regression passed afterward.
The obsolete unused File icon was removed after compiler diagnosis.

## Verification and inputs

Linux x86_64, Iced 0.14, tiny-skia. Offline locked Cargo with
CARGO_HOME=/home/rodrigo/Projetos/ox/.cache/ox/cargo-home. Commands from repository root:

```bash
cargo fmt --manifest-path application/Cargo.toml --all -- --check
cargo test --manifest-path application/Cargo.toml --offline --locked -p ox-ui
cargo clippy --manifest-path application/Cargo.toml --offline --locked -p ox-ui --all-targets -- -D warnings
cargo build --manifest-path application/Cargo.toml --offline --locked -p ox-app --bin ox
python3 docs/validation/project-entry-20261117/native-entry.py --name wide --capture-only
python3 docs/validation/project-entry-20261117/native-entry.py --name small --monitor 640x480 --capture-only
```

Final Rust result: 46 unit tests, four integration tests and one shell contract pass;
one subprocess helper is intentionally ignored as a direct test. Formatting, Clippy
and build exit zero. Logs: rust-test.log and clippy.log. Native results are in
wide/result.json and small/result.json, with screenshots/events and exact source
hashes. Both observe stable source/binary inputs and natural process exit zero.
Root inspected initial images at 1366×768 and 640×480. Input/binary snapshot:
inputs.json. Native fixture directories and state are isolated under each run;
maintainer history/projects are not used. Captures are observations of real native
widgets, not implementation declarations. Capture-only does not execute drag or
full theme oracles; those historical results are not renewed.

## Documentation disposition and limits

Reviewed and updated DESIGN.md, docs/design/components.md and surfaces.md,
application/README.md, sdd/project.md and product-visual-workbench
spec/plan/tasks/converge for icon semantics, action order, unavailable Clone,
main-area projects, narrow stacking and chooser-failure recovery. Reviewed
constitution, architecture/context.md, product-bootstrap ADR and
reference-coverage.md: no architecture, effect, dependency, artwork or source
provenance change; their existing boundary/provenance remains valid. Consulted
iced-engineering/SKILL.md and references/native-visual-contract.md; applied shared
native drawing, widget/state order and source-bound layout observation.

Broad evidence.json ACs remain INCONCLUSIVE and WCs UNVERIFIED. DN/EV approvals
remain historical for their original inputs; this local slice does not renew the
full matrix or independent approval. No clone operation, dependency acquisition,
full scanner, commit or publication. These focused observations support PE-01–04
within the limits above; they are a manual local assessment, not an automated
product approval gate.
