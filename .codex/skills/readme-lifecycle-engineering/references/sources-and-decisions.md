# Imported research record

This ledger is retained from the supplied package. Its Ec-specific norms and
research actions describe that source context, not Ox policy or new browsing in
this integration. Use [consumer boundaries](consumer-boundaries.md) for the actual
repository. External links and scientific claims were not independently reverified
here; structural/source review is not an effectiveness study.

# Primary source register, provenance, and design decisions

**Research date:** 2026-11-03. **Method:** inspected supplied Ec and Ox skill entry points and
bridges; read Ec normative documents; consulted provider documentation, university guides,
conference/journal records and abstracts/full text where accessible. This is a targeted,
multi-source literature review, not a systematic review with a pre-registered search protocol.
Publisher abstracts alone are explicitly identified. No tests against an Ec repository, real
reader study, or benchmark were performed in this skill authoring task.

## Consumer and local sources

| ID | Source inspected | Role and limitation |
|---|---|---|
| N01 | `EC-REGRAS-DE-DESIGN-E-PRODUTO.md` | Ec identity, stack, YAML sole canonical desired configuration, honesty about feature status, operational persistence separate from desired config. Protocol norm remains versioned HTTP until revised. |
| N02 | `EC-REGRAS-CRIACAO-DE-TELAS-E-IMAGENS.md` | Truthful states and UI representations when README points to screens/examples; no fabricated visuals. |
| E01 | `ec_skills.zip`, 40 `new_skills/skills/*/SKILL.md` and sample `sdd/chain/*.md` | Native Ec entry shape and optional SDD bridge with `UNCONFIGURED` path. |
| E02 | `ox_resume.zip`, `.codex/skills/technical-documentation/SKILL.md`, `agents/openai.yaml`, `sdd/chain/technical-documentation.md` | Different specialized documentation scope; optional metadata style; no assumed agent activation. |
| E03 | `resume.md`, Ox governance summary | Separates constitution, SDD, skill method and actual acceptance. Documentation does not install or authorize anything. |
| E04 | `reavaliacao-skills-ec-dois-monolitos-atualizada.md` | Planned skill matrix of 66 before this candidate; does not certify installation or adopted new skill. |

## Official provider/framework guidance

| ID | Source | Specific support, not universal mandate |
|---|---|---|
| O01 | [GitHub: About READMEs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes) | Purpose, why, quick start, help, maintainers; README discovery paths, relative links, linked docs and overview vs long manuals. |
| O02 | [GitHub: repository best practices](https://docs.github.com/en/repositories/creating-and-managing-repositories/best-practices-for-repositories) | README per repository as recommended entry point. |
| O03 | [Google Style Guide: READMEs](https://google.github.io/styleguide/docguide/READMEs.html) | Small, up-to-date package READMEs with purpose, status, contact, usage and docs links. |
| O04 | [GitLab: Documentation Style Guide](https://docs.gitlab.com/development/documentation/styleguide/) | Documentation as continuously maintained product source, concise/searchable writing. |
| O05 | [GitLab: Documentation Workflow](https://docs.gitlab.com/development/documentation/workflow/) | Develop docs with code/feature changes; review and cross-check before milestone. |
| O06 | [Diátaxis: framework](https://diataxis.fr/) | Separate tutorials, how-to, reference and explanation by reader intent, not automatically by file format. |
| O07 | [The Turing Way: Code documentation](https://book.the-turing-way.org/reproducible-research/code-documentation/) | Project-dependent documentation scope; a small project may only need README/basic comments. |
| O08 | [Cornell research code README guidance](https://data.research.cornell.edu/data-management/sharing/writing-readmes-for-research-code-software/) | Research reuse, self-containment trade-off for preservation contexts. |
| O09 | [Harvard Kempner Handbook](https://handbook.eng.kempnerinstitute.harvard.edu/s2_swe_for_research/documentation_and_readibility.html) | README front door, deeper docs elsewhere, simple runnable usage. |
| O10 | [Johns Hopkins OSPO best practices](https://ospo.library.jhu.edu/learn-grow/public-code-repository-best-practices/) | Sustainable project README, status, links, project milestones. |

## Scientific publications

See full bounded interpretations, DOIs and academic verification venues in
[scientific-evidence-and-limits.md](scientific-evidence-and-limits.md):
Prana et al. (2018); Liu, Noei & Lyons (2022); Wang et al. (2023/2024);
Tan, Wagner & Treude (2024); Lee (2018, guidance/editorial). The evidence is
observational or prescriptive as stated, not proof of a universal documentation template.

## Decisions and alternative considerations

1. **A distinct README skill is justified by lifecycle ownership.** Ox `technical-documentation`
   owns general tutorials, reference and explanations; this skill owns repository first entry,
   topology, the split decision, README drift and README-to-docs navigation. Select the smallest
   relevant scope; do not activate both automatically.
2. **One root README is the default, not the only allowed file.** The repository is the main
   entry; independent modules with independent users may have local READMEs. Avoid redundant
   installation instructions if a canonical guide already exists.
3. **No hard page-length/section-count limit.** Universally optimal thresholds were not
   established by the sources. Evaluate navigation friction and reader outcomes instead.
4. **Google's package-location convention vs GitHub lookup precedence.** Both are official
   but answer different questions; inspect the actual host and repository style.
5. **Keep references in canonical files.** A README links to authoritative documentation
   rather than copying API schemas, SDD artifacts or ADR conclusions.
6. **Ec remains YAML-only for declarative product config.** Markdown is documentation;
   `agents/openai.yaml` in this skill package is *skill UI metadata*, not Ec configuration.
   Server/agent states, logs, test results and tickets must not be described as YAML truth.
7. **State what has not shipped.** Ec gRPC/SQLite from earlier analysis are proposed until
   implementation/ADR evidence; README must distinguish planned from implemented status.
8. **Integrate with existing SDD without overriding it.** Use optional bridge only when
   selected; project has final say on spec/plan/evidence and acceptance statuses.

## Unverified / absent

No actual target Ec git tree or current release manifests were provided for a README rewrite.
Therefore exact installation commands, version support, README screenshots and real CI status
remain unknown. This package is a **method**, not a completed Ec README or deployed documentation.
