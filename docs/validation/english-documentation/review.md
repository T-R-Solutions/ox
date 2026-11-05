# English documentation revision — 2026-10-28

The maintainer requested English skills, AGENTS.md and SDD, with tasks remaining
in Brazilian Portuguese. This revision follows the local documentation route:
existing policies, IDs, scopes and technical scenarios retain their meaning.
All 16 tasks.md files, including the template, retain their observed bytes.
Other maintained prose in the requested areas is English. Proper names, historical
filenames/URLs and Unicode Rust test data retain their identities.

The initial worktree already contained changes to commit-governance/SKILL.md and
its agents/openai.yaml. Those changes were preserved. Only five lines of Portuguese
invocation examples in that skill were translated; its YAML was unchanged from
the observed starting state. The existing profile has 29 entries while the actual
library has 30 skills, including commit-governance. This request does not revise
the profile or its authorization history.

Current evidence uses APPROVED, REJECTED, UNVERIFIED, INCONCLUSIVE and NOT APPLICABLE.
The validator normalizes the five legacy Portuguese tokens without rewriting
historical evidence. Both spellings enforce evidence, reason and input-binding
gates; spelling does not promote a state. The SDD's original validator remains
available in the historical baselines and this revision's predecessor snapshot.

Preservation comparisons recognize only the exact translated bytes registered in
translations.json and authenticate their predecessor snapshots by SHA-256.
Unregistered mutations are still compared as current content and rejected by the
existing preservation gates. Previous observations and baseline hashes were not
renewed. Two preservation tests now compare the authenticated predecessor with
the old authoring contract rather than requiring translated prose to equal its
Portuguese source. New tests check both status vocabularies and predecessor tampering.

Changing product-bootstrap/spec.md and plan.md affects every observation in its
evidence envelope. The original envelope and contract bytes are preserved under
`docs/validation/product-bootstrap/english-documentation/previous/` (outside the
governance export). Current product-bootstrap criteria are UNVERIFIED pending
fresh review/execution. The English convergence record clearly labels previous
acceptance as historical. Application sources and tests were not changed or rerun.
Other feature criteria were already UNVERIFIED; translation did not promote them.

| Criterion | Method and observed inputs | Result | State / limitation |
|---|---|---|---|
| Requested prose is English; task files stay pt-BR | Reviewed translated prose and bibliographic metadata; language-check.py.txt compares the initial hashes, ordered REQ/AC IDs and a Portuguese vocabulary scan; observed-inputs.json identifies current bytes | 16 unchanged task files; 16 specs retain ordered REQ/AC IDs; no remaining prose matches; active evidence statuses are English | APPROVED for this language revision; vocabulary scanning alone is not semantic proof |
| Skill metadata and structure remain valid | Environment skill-creator/scripts/quick_validate.py on every actual skill directory | 30 checked, zero failures (skills-check.log) | APPROVED for metadata/structure; does not measure skill effectiveness |
| Portable SDD and content bindings remain coherent | `PYTHONDONTWRITEBYTECODE=1 python3 sdd/tools/validate.py --root . --require-fresh` | Exit 0 (sdd-check.log) | APPROVED for the validator's scope; unverified product criteria are not accepted |
| Status compatibility and preservation guards retain their guarantees | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools/governance/tests -v` | 25 tests: 21 passed, 4 failed (tests-final.log); both newly added tests passed | INCONCLUSIVE for the complete suite; existing blockers below remain |
| Distinguish existing failures from translation regressions | Reconstructed pre-translation inputs from observed copies and clean original governance scripts; reran the original 23 tests with temporary fixtures outside the reconstructed source's parent | 19 passed, the same 4 tests failed (tests-before.log); individual checker results also match (baseline-check.log) | APPROVED for identifying these existing failures; not a claim of a clean repository |

The four failing tests are test_clean_export_and_recovery,
test_independent_copy_and_corrupt_resource, test_normative_hash_requires_review
and test_product_feature_isolated_from_skill_acceptance. The first reports
preexisting AGENTS.md recovery differences (438/439 layout inputs recoverable);
the remaining three encounter the preexisting extra commit-governance skill
outside the versioned profile. check-ox.py still returns exit 1 for that inventory
mismatch. verify-maintenance.py still returns exit 1 for AGENTS.md. Both diagnostics
were reproduced using the pre-translation state. They were not suppressed, added
to an allowlist or converted to successful acceptance.

Inputs and predecessor identities are in before.json, translations.json and
observed-inputs.json. Logs retain the actual failures. baseline-check.py.txt and
language-check.py.txt record the temporary session methods; their /tmp paths are
historical, not supported project commands or validation dependencies. The temporary
baseline copy used the original scripts from Git HEAD because they were clean at
session start. This was not a historical rerun on a deployed application.

Primary method consulted: `.codex/skills/technical-documentation/SKILL.md`, version
not declared; contribution: preserve authoritative contracts, reader-visible
commands and historical observation identity. Supporting method consulted:
`/home/rodrigo/.codex/skills/.system/skill-creator/SKILL.md`, version not declared;
contribution: preserve skill metadata/resources and use its structural validator.
No bridge consultation, delegated evaluation or installation is claimed.

Review was performed by the executor, not an independent human. No product
execution, effectiveness evaluation, release, publication or commit was performed.
Reevaluate this record only if its observed inputs change. Resolve the profile
and historical recovery discrepancies separately before claiming a fully passing
governance suite.
