# Selection, non-overlap and evidence routing

## Choose `readme-lifecycle-engineering` when

- A project/package README needs authoring, audit, revision, restructuring or continuous upkeep.
- The question is whether one README suffices or when/how to move details to `docs/`.
- A repository README diverged from release/status, install commands or linked docs.
- A monorepo needs a clear hierarchy of root/package READMEs without duplication.

## Do not choose it solely when

- Writing a standalone API reference or tutorial: `technical-documentation` generally owns it.
- Making an architectural design decision: `software-architecture` owns the choice, not README.
- Implementing a markdown rendering engine or doc site: use the relevant web/docs skill.
- Deciding legal license or publication rights: follow authorized owners, not README skill.
- Updating comments or ADRs with no reader entry impact: keep existing domain workflow.

## Conditional handoff

Consult an available specialist only for a **specific unresolved question**, such as:
verified supported Rust command, CLI versioning, security warning, CI status, actual consumer YAML
schema or release compatibility. Pass the question, required evidence, context, input revision,
permission scope and project-specific criteria. Do not auto-load a catalog or imply another
skill has been used merely because a bridge mentions it.

## Main oracles

1. **Documented route vs real code:** can the described action be performed on this revision?
2. **Canonical claim vs duplicate:** is the authoritative explanation unique and up to date?
3. **Reader task vs discoverability:** can an unfamiliar reader find the route from the entry?
4. **Status vs release:** is every usability claim supported by version/feature evidence?
5. **Changes vs docs:** did behavior modifications invalidate a previously documented path?
6. **Failure/recovery:** if a setup step fails, does the user have a bounded next action?

For every selected oracle, distinguish *not applicable*, *not checked*, *inconclusive* and
*observed result* according to the actual consumer workflow. The skill is a procedure; it
cannot certify repository quality just by being present.
