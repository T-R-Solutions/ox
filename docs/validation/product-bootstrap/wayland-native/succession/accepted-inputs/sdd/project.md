# Ox project context

## Identity and phase

Project: Ox — an agent-first, local-first, extensible desktop application.
Current phase: `implementation-foundation`.
Application state: `bootstrap-implemented`.
Status: product implementation is authorized through bounded SDD features;
no product component is considered implemented or validated without concrete evidence.

Governance and library work was recorded as a preparatory stage with historical
observations preserved. The governance transition is handled by
`sdd/features/product-foundation/` and does not implement application code.
Future deliveries use independent `product-*` features with authorized scope.
Local corrections follow the proportionate route defined in the workflow. This
does not automatically authorize deployment, external access, spending, policy
changes or destructive actions.

## Authorities

- `docs/constitution.md`: permanent Ox policies.
- `AGENTS.md`: operational entry point and references.
- `sdd/constitution.md`: pointer to the constitution, not a second policy.
- `sdd/workflow.md`: route selection and development lifecycle.
- `sdd/evidence.md`: states, evidence and acceptance.
- `docs/architecture/context.md`: planned components and milestones.
- `docs/decisions/*.md`: current, historical and pending decisions.

## Features and methods

`adoption-governance` and `governance-externalization` are historical.
The nine `skill-*` features validate library authoring and selection, not the
operation of product modules.

Application features use the `product-*` prefix, remain directly under
`sdd/features/`, and have requirements, oracles, evidence and states independent
of skill SDDs. The local route follows `sdd/workflow.md`; do not open a full
feature merely for formality.

The 30 skills and 30 bridges remain available according to the versioned profile.
Select a primary capability only when relevant; supporting skills require distinct
technical questions. Availability, indication, selection, consultation and use are
not equivalent. `docs/development/sdd-skills.md` explains bridge interchange
without modifying skills' technical procedures.

## Stack and technical state

Adopted for first-party product code: Rust and Iced, prohibiting first-party
`unsafe` according to `POL-01`. Ox-controlled storage will be local in the MVP;
LSP and advanced capabilities will be integrated through plugins.

**Historical baseline in the base package of 2026-10-26:** no product Cargo.toml,
lockfile or crate was present. This statement describes the baseline; the current
state is described below.
Current state: workspace in `application/`, 16 crates and a minimal window.
Authorized scope: `product-bootstrap`, execution of prompt v2.0. Linux x86_64
was confirmed by the maintainer. The toolchain is now pinned to 1.99.1
under docs/decisions/governance-reconciliation.md. Iced 0.14.0, edition
2024 and Rust 1.99 floor according to `docs/decisions/product-bootstrap.md`.
Acceptance is in `sdd/features/product-bootstrap/`; this structure alone does
not complete F0.

Current governance tools: Python 3.11+ and stdlib. SDD 1.3.0 and its original
validator remain preserved in historical baselines; English documentation is a
language-only adaptation. These tools are not the application's Rust code.

Current organization: tools and tests in `tools/governance/`, evaluation data in
`tools/governance/tests/fixtures/`, profile and normative coverage in
`config/governance/`; `application/` contains the virtual Rust workspace,
separate from governance. Sources and tests belong in
`application/crates/<crate>/src/` and `application/crates/<crate>/tests/`;
the workspace root has no src/ or tests/.
The ADR `docs/decisions/governance-layout.md` supersedes only previous location
and allowlist decisions, preserving their records.

## Available commands — governance

From the Ox root, while these scripts exist:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 sdd/tools/validate.py --root .
PYTHONDONTWRITEBYTECODE=1 python3 sdd/tools/validate.py --root . --structure-only
PYTHONDONTWRITEBYTECODE=1 python3 tools/governance/scripts/check-ox.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools/governance/tests -v
PYTHONDONTWRITEBYTECODE=1 python3 tools/governance/scripts/run-checks.py
```

Product commands: `cd application`, `cargo check --workspace`,
`cargo test --workspace`, `cargo test --workspace -- --list`,
`cargo fmt --all -- --check`, `cargo clippy --workspace --all-targets -- -D warnings`
and `cargo run -p ox-app --bin ox`.
No Python command output validates the Rust/Iced application.

## Pending decisions and limits

Consult `docs/decisions/open-questions.md` before selecting platforms, versions,
runtime, IPC, database, sandbox, agents or distribution.
Feature authorization does not replace risk policy and effective permissions.
Do not request global --require-approved while technical criteria are intentionally
UNVERIFIED.

## Library history

The active catalog is in `.codex/skills/`. All 30 bridges use this location.
Historical records in `docs/validation/` preserve earlier paths, hashes and limits;
they are not sources for the application's current state. The three external
studies are not part of distribution or validation.

## Authorized reconciliation — 2026-10-29

The maintainer authorized local profile, recovery, acceptance, toolchain, test-group
and package corrections in governance-reconciliation and product-bootstrap. No
commit, publication or historical deletion is authorized. Decisions and limits are
in docs/decisions/governance-reconciliation.md. New commands, when present:
`python3 tools/governance/scripts/run-tests.py --group fast` (small fixtures),
`--group integration` (full-copy integrity), and `--group all` (complete suite).

## Authorized sequential deliveries — 2026-10-29

The maintainer authorizes local implementation, tests and full-route SDD updates
for native Wayland bootstrap acceptance, then minimal Plugin Host, Agent Runtime
and Verification Engine slices, each gated by acceptance of its predecessor.
Record each new feature scope before code. Native Wayland is now an explicit
validation target on Linux x86_64; existing X11 obligations remain. No commits,
publication, global installation, destructive operations, remote providers,
credentials or transmission are authorized. Context/graphs, marketplace, full
orchestration and platform expansion are excluded. F0 is not thereby complete.
