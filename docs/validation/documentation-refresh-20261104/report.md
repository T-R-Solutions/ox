# Documentation refresh — 2026-11-04

## Goal, route and methods

Maintainer request: redo READMEs and related documentation. Local route under
sdd/workflow.md: restructure existing source-grounded explanations without changing
product code, scope, dependencies, policy or release decisions. Existing dirty and
untracked work was inspected. No delegation, commit, publication or installation.

Primary method: `.codex/skills/readme-lifecycle-engineering/SKILL.md`, no declared
version, for entry paths, layout, first run and maintenance. Supporting method:
`.codex/skills/technical-documentation/SKILL.md`, no declared version, for source-grounded
instructions and reference navigation. Both entries were read. Tables express the
capability, action and document mappings; no new graphical behavior diagram or
rendered-media claim is introduced.

## Changes and observed inputs

Root README now introduces purpose, delivery status, minimal first run and routes
readers. `application/README.md` owns detailed build, controlled-task usage,
troubleshooting, tests and Rust reference generation. `docs/README.md` indexes
architecture, development, decisions and current evidence. The feature index now
includes the implemented local slices and the final F0 successor; architecture and
governance guides point to the new entry paths. English SDD conventions remain.
Historical execution reports are unchanged.

`inputs-before.json` identifies inspected sources, manifests, lockfile, toolchain,
authorities, methods and pre-edit documents by SHA-256. `before/` retains immediate
predecessors. `inputs-after.json` records final document and source identities.
The working tree includes earlier unrelated changes; Git HEAD alone is insufficient
to reproduce these observations. Source inspection covered manifests, desktop
auxiliary discovery, Controller, producer/oracle and linked contracts/F0 reports.

## Criteria, methods, results and limitations

| Criterion | Method / observed inputs | Observation | State and limit |
| --- | --- | --- | --- |
| Readers find a complete first run and current scope | Editorial comparison of the README, new guides, Cargo manifests, desktop/fixture sources and accepted local F0 report | Prerequisites, working directory, auxiliary layout, expected verdicts, disk effects, restart limits and failure paths are explicit | APPROVED for documentary inspection; no new GUI journey or reader study |
| Build and ordinary tests match instructions | In application/: `cargo build --workspace --locked --offline`; `cargo test --workspace --locked --offline` | Both exit 0; 29 tests pass, six desktop tests ignored | APPROVED for cached local Linux environment; not clean-machine installation or graphical acceptance |
| Additional developer commands are executable | Exact commands and raw outputs in commands.json / command-*.log | Check, fmt, clippy and Rust documentation generation exit 0 | APPROVED for observed toolchain/cache; no dependency update or general platform support |
| Navigation and SDD portability | Focused local target/fragment inspection, structural validator and whitespace check, captured in final-checks.json and links.json | See exact final observations in those artifacts | Static checks only; no remote links, rendered host inspection or usability claim |
| Feature index preserves F0 meaning | Compare product-f0-gate spec and final raster successor, unchanged persistence proposal and local source hashes | Lists current slices, adopted-corpus acceptance and pending persistence authorization separately; skill/product acceptance stays independent | APPROVED for documentary index inspection; does not reaccept operational criteria |
| Preservation chain is honest | Compare baseline-checks.txt and final check-ox result | The preexisting exact-byte README integration guard still rejects README.md | UNVERIFIED for global governed README successor acceptance; no guard weakened |

Build/test observations above were captured through command tool results; this
record retains their summary, not a complete raw test transcript. Other executed
commands have raw log files. The first SDD check after editing rejected cross-root
links inside the portable SDD index. They were replaced by explicit root-relative
path references. A subsequent intermediate check-ox found links to this not-yet-written
report and the index's historical F0 input; final checks follow their correction.

## Affected evidence and preservation

AC-04 in readme-skill-integration remains UNVERIFIED, as already recorded before
this request. The current root README still differs from the immutable integration
registration. Fixing that preservation consumer requires its own reviewed successor;
this documentation change does not rewrite that registration or historical hashes.

The feature index was an input of E-QUALITY-REFINEMENT in product-f0-gate. Its exact
old bytes are retained under before/sdd/features/README.md.bin; the old observation
now resolves to that same-hash historical preimage. E-DOCUMENTATION-REFRESH records
the changed index inspection for documentary AC-01..04. Earlier product measurements,
oracles, F0 acceptance budgets and persistence decisions are unchanged. This is an
explicit documentary successor, not renewal of operational evidence from a new digest.

Maintenance owner: contributor changing the affected source and Ox maintainer.
Review root/app guides when commands, binaries, UI actions, tests, support envelope
or status change; review the docs/feature indices when entries or successors change.
No full suite of governance export/recovery tests, fresh global acceptance, graphical
replay, external research, packaging or publication is claimed here.
