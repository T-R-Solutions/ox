# Detailed decisions, edge cases and reusable workflow

Load this file only when the brief `SKILL.md` does not resolve the reader, document ownership
or verification problem. This is a procedure, not a mandatory artifact template.

## End-to-end audit sequence

1. Discover real Git root, branch/commit, products and maintained entry points. Build a list of
   files and authoritative product/build sources; identify dirty or independent changes.
2. Extract reader tasks and permissions from real use cases or documented policy, not guesses.
3. Read each existing README and its immediate links. Mark factual statements as observed,
   contracted, proposed, deprecated or unknown; note the supporting source/revision.
4. Locate contradictions, duplicate instructions, dead links, stale command names, missing
   prerequisites, version conflicts and unannounced dependencies.
5. Choose root/package/docs separation based on independent entry points and task needs.
   Split if readers routinely must scroll past unrelated material, if ownership diverges,
   or if canonical references have different release cadence; these are qualitative signals.
6. Draft root reader journey and minimal task examples; link to complete explanations. For
   decisions and SDD, link instead of pasting text and inducing a second authority.
7. Verify Markdown, relative paths and fragments; execute actual safe commands where authorized;
   record environment, revision, exact inputs and outputs.
8. Present a change map by file, reader task, source of truth and remaining gap. If a command
   cannot run, document the blocking prerequisite, not a fabricated pass.
9. Identify update triggers (CLI change, new package, release, deprecation, schema changes,
   documentation split) so the README grows with the product.

## Edge cases

**Private project:** contributor and support paths may be internal; do not publish private URLs
without authorization. **Incomplete project:** status is explicitly experimental/in progress;
no fake setup. **Multi-version product:** root points to current version, with explicit archived
references; avoid assuming `main` is a released version. **Monorepo:** root gives system map,
package READMEs only where separate start paths exist. **Research archive:** prefer extra
self-contained metadata if links may rot. **Generated docs:** their source generator, not the
output, may be canonical; README links to generated output/version only when real.
**README named elsewhere:** account for GitHub's README precedence, Google package convention
and current host; do not create ambiguous competing front pages. **Screenshots/badges:** avoid
outdated or misleading display; accessibility/alt text matters where imagery is present.

## Anti-patterns to reject

- One file with every configuration option and runbook repeated elsewhere.
- Several READMEs that contain diverging or duplicated install commands.
- 'Just run ...' without working directory, prerequisites or expected outcome.
- `curl | sh` as an unqualified installation recommendation, or production changes in demo steps.
- Roadmap wording written as a supported-feature claim.
- Security/license/release badges implying approval without actual evidence.
- Test outputs, uptime percentages or support contacts invented for the README.
- A passing broken-link checker used to claim functional correctness.
- Documentation moved to `docs/` without updating backlinks, anchors or navigation.

## Reference routing

- First page and task path: [scope and content](readme-scope-and-content.md).
- Structure and Diátaxis: [topology](documentation-topology-and-diataxis.md).
- Staleness: [maintenance](maintenance-and-change-triggers.md).
- Evidence and check selection: [verification](verification-and-acceptance.md).
- Consumer authority and scope: [consumer boundaries](consumer-boundaries.md).
- Academic strength/limits: [scientific evidence](scientific-evidence-and-limits.md).
- Exact URLs and conflicts: [source ledger](sources-and-decisions.md).
- Distinct skills and oracles: [routing](routing-and-oracles.md).
