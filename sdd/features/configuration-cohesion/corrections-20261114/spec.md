# Proposed instruction-governance corrections

Status: DRAFT, planning authorized on 2026-11-14; implementation awaits maintainer
review. The request is to plan audit findings 1–10 and report before applying them.
This supplement belongs to configuration-cohesion. It neither replaces its current
spec/evidence nor changes current policies or authorizes the previously requested
implementation work. No correction is claimed implemented by these documents.

Source: `docs/validation/governance-audit-20261114/report.md`, findings A01–A10.
Execution design: [plan](plan.md); work breakdown: [tasks](tasks.md);
observations and pending acceptance: [convergence](converge.md).
Authority remains the [workflow](../../../workflow.md) and
[evidence contract](../../../evidence.md), plus the constitution and effective
session permissions. The parent feature's AC-01–03 retain their existing meaning
and current states. Numbers below are reserved proposals for extending that feature
after approval; nested Markdown is not an additional automated feature or an
automated acceptance record.

## Actors, scenarios and invariants

An assistant resumes work from current project state; a maintainer reads acceptance;
a contributor instantiates a feature; a consumer adopts a portable SDD; a reviewer
checks one feature; and a controller selects a permitted execution route.
Each must obtain an unambiguous contract without reconstructing contradictory
instructions or accidentally requesting acceptance of unrelated unfinished work.

Preserve the five evidence states, real observed inputs, historical observations,
31 skill identities and their unique procedures, 13 agent profiles/model matrix,
explicit commit/publication boundaries and unrelated working changes. Instructions
cannot override host permissions. Static checks cannot certify model behavior.
No product implementation, new roadmap phase, public release or dependency
installation is included. Local full automation remains separately authorized.

## Proposed requirements and acceptance

- REQ-04: Automated features expose one current status per normative criterion, derived from their evidence envelope; historical observations remain identifiable.
- AC-04 → REQ-04: All adopted current projections match their evidence criterion IDs and states; a changed state, missing/duplicate row or missing projection is rejected by the explicit projection check, and old observations remain recoverable.
- REQ-05: The commit skill obtains the current complete-verification command and local environment from their operational authority.
- AC-05 → REQ-05: The affirmative commit route resolves to `run --scope complete` with the AGENTS environment; plan-only inspection matches the current catalog. Negative/no-answer routes retain their effects and no commit is performed by the test.
- REQ-06: Following the template-instantiation instructions produces valid authority links in the destination.
- AC-06 → REQ-06: Copying and adapting the documented templates in an isolated normal and custom feature location preserves link fragments and resolves their targets; no authority copies or invented observations are created.
- REQ-07: Project-link validity and standalone package portability are explicit, distinct validation boundaries.
- AC-07 → REQ-07: A real sibling project authority is accepted in project mode and rejected when outside a portable package; missing targets, path escape and symlink traversal remain rejected, with standalone skills retaining their folder boundary.
- REQ-08: SDD adoption copies a declared reusable set and configures destination context deliberately.
- AC-08 → REQ-08: An isolated adoption following the guide contains no Ox features/evidence, local agent config or full skill catalog by default, and passes applicable structure/link checks without reaching the original checkout.
- REQ-09: A caller can explicitly validate one or several named features while retaining existing all-feature behavior and complete selected-feature gates.
- AC-09 → REQ-09: Selected approved/fresh features can pass beside valid unfinished siblings; selecting a stale/unverified feature fails. Unknown, empty, escaping and ambiguous selections fail without silently selecting all features or accepting zero matches.
- REQ-10: The root controller and a delegated triager have explicit, compatible responsibilities.
- AC-10 → REQ-10: Role/configuration review finds no instruction that forbids root handoff while requiring it; a delegated triager remains read-only and childless. Profile names/model matrix stay unchanged.
- REQ-11: Direct execution is permitted only for defined low-risk tasks; material risks preserve independent review/validation and capability limits.
- AC-11 → REQ-11: The route matrix distinguishes read-only work, bounded local repairs, feature-gated work, material-risk changes and capability absence. No rule relabels self-review as independent acceptance or permits an effect beyond authorization.
- REQ-12: Every common policy has one maintained owner, while portable skills retain sufficient standalone context and unique methods.
- AC-12 → REQ-12: Before/after semantic mapping preserves all 31 skill identities, selection boundaries, technical procedures and bridge contributions; duplicate project policy/command bodies are replaced by resolvable references without recursive activation.
- REQ-13: Project entry distinguishes current implementation, current acceptance, pending work and dated authorization history.
- AC-13 → REQ-13: A reader can locate current phase, implementation limits, acceptance source and pending work from the opening summary; historical scopes are explicitly dated, prior observations remain recoverable and no new permission or product acceptance is inferred.
- REQ-14: Corrections preserve authenticated history and invalidate only genuinely affected observations.
- AC-14 → REQ-14: A changed-input map and bounded succession checks reject unknown mutations, tampered predecessors, downgrade and symlink substitutions; no historical digest is renewed to represent new execution.
- REQ-15: Integration is accepted using the corrected current inputs and reviewable evidence, without global approval of unrelated pending features.
- AC-15 → REQ-15: Focused regressions, affected consumers, independent review/validation and the selected feature's complete applicable gates are satisfied, or each outstanding criterion retains its proper non-approved state with a resumption condition.

## Decision boundary

The plan recommends explicit decisions for status projections, validation scope,
feature selection and proportional agent execution. These recommendations are not
adopted by authoring this supplement. A maintainer response may approve the complete
proposal or modify individual decisions. Effective permissions still govern effects.
The present delivery ends at planning and checking these documents.
