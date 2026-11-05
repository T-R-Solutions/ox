# Application documentation review — 2026-11-04

## Goal and route

Maintainer request: analyze the application and update README/supporting documents
with identity, functionality, implementations and contracts. Local documentary
route under sdd/workflow.md: describe existing behavior without changing product
code, dependencies, permissions, acceptance budgets or technology decisions.

Primary method: `.codex/skills/readme-lifecycle-engineering/SKILL.md` (no declared
version), for entry-point audit, first use and documentation splitting. Supporting:
`.codex/skills/technical-documentation/SKILL.md` (no declared version), for API and
behavior reference. Both actual entries were read. No full-route plan or delegation
was needed. Existing dirty/untracked work was inspected and preserved.

## Inputs and changes

Git base: 68f8d072aa5656eb70c705e4bec5071a3afcff81, plus the local dirty tree.
`inputs-before.json` records SHA-256 identities of the observed Rust sources,
manifests, lockfile, toolchain, authorities, skill entries and pre-edit documents.
Pre-edit README, architecture context and convergence bytes are retained under
`before/` with `.bin` suffixes. The context map was restored to its exact pre-edit
bytes after detecting shared operational-evidence dependencies: it is unchanged
by this review. `inputs-after.json` identifies the final documents and unchanged
product inputs. Git alone does not identify this analysis snapshot.

Deliverables:

- Root README: product purpose, current functionality, first execution, verification,
  state, boundaries, documentation navigation and governance entry point.
- `docs/architecture/application.md`: execution flow, worker/UI integration,
  responsibilities of all 16 crates, implemented slices and future capabilities.
- `docs/architecture/contracts.md`: Controller, producer/oracle file format, runtime,
  strict plugin wire protocol, verification limits/precedence and domain types.
- `docs/development/governance.md`: operational/governance material relocated from
  the old README, preserving commands, packaging, license and recovery routes.
- `readme-skill-integration` convergence/evidence: explicitly records that the old
  navigation observation is historical and AC-04 is UNVERIFIED for the new README.
  Its observed README bytes are preserved, with the same hash and no new runtime claim.

## Criterion, method, result and limits

| Criterion | Method / observed inputs | Result | State and limitation |
| --- | --- | --- | --- |
| Identity/functionality distinguish delivery from direction | Read all 16 crates' library roots and domain modules, five executable implementation modules, controlled producer/oracle, manifests, tests and current authorities/F0 successor report | Documents distinguish functioning local flow, standalone host, contract-only modules and planned engines; stale open-F0 sentence removed from README | APPROVED for source-grounded description; no new F0 or real-agent acceptance |
| Contracts describe actual inputs, states, effects and failure paths | Source inspection of Controller, Runtime/Machine, Host, Engine and domain models against linked test cases | Includes exact request/result identity, strict wire 1.0 vs generic version compatibility, manual stale evaluation, rejection/incomplete precedence and content budgets | APPROVED for documentary inspection; no public API guarantee, hostile-process confinement or persistent storage claim |
| First build and ordinary local product tests remain executable | `cargo build --workspace --offline`; `cargo test --workspace --offline`, from application/, Rust/Cargo 1.99.1 | Both exit 0; 29 tests pass, six graphical tests ignored; process/socket tests and controlled result verification execute | APPROVED for observed build/test envelope; dependencies already cached; no installation or new GUI journey |
| Documentation links and process structure | `python3 sdd/tools/validate.py --root . --structure-only`, local link inspection and final check-ox log | Structural validator exits 0; final check log records current link result | Structural/documentary evidence only, not criterion acceptance for the application |
| Full governed current README identity | `python3 tools/governance/scripts/check-ox.py`; compare immutable `readme-skill-integration-001` registration against new README bytes | Current-byte preservation guard rejects README.md because it requires the preceding bounded revision | UNVERIFIED for governed successor acceptance. No guard weakened, historical revision overwritten, digest renewed or failed check claimed as passing |

## Governance limitation and resumption

The skill integration's preservation consumer freezes the root README as an exact
registered current file. This review changes its contents under the maintainer's
new documentation request, so check-ox reports `README integration current
changed/missing: README.md`. Resolving that requires a separately registered
preservation successor and corresponding consumer/evidence review; it is not a
broken application build or an unresolved Markdown link. The current integration
AC-04 is explicitly UNVERIFIED instead of retaining approval for changed inputs.
The original integration evidence and README bytes remain preserved.

This change does not modify preservation code, the profile or revision contracts
as part of a documentation request. Existing product sources and dependencies are
byte-identical to the analyzed inputs, so operational F0 observations were not
rerun or relabeled. No global freshness/approval, new graphical acceptance, reader
study, external-source verification, release, export or publication is claimed.

Maintenance trigger: changes to capabilities, modules, API signatures, states,
limits, auxiliary binary layout, toolchain, dependencies or accepted scope require
review of the corresponding README and reference sections. Owner: maintainer and
contributor making the change. The recorded governance limitation remains an
explicit acceptance gap, not an instruction to bypass the guard.
