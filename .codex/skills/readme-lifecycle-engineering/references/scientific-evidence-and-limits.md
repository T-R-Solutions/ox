# Academic evidence on README content, structure, and staleness

> Research checked 2026-11-03. Papers support general engineering heuristics for their studied
> populations, **not** guaranteed effects or target product performance. A paper accepted by a
> journal and a university guide are different evidence categories. Counts and correlations
> must not be generalized to every language, project type, hosting platform or future cohort.

| Study, publication and verification | Observed scope / result | Engineering implication | Important limitation |
|---|---|---|---|
| **Prana, Treude, Thung, Atapattu & Lo**, *Categorizing the Content of GitHub README Files*, **Empirical Software Engineering** (2018), DOI [10.1007/s10664-018-9660-3](https://doi.org/10.1007/s10664-018-9660-3); [Singapore Management University](https://ink.library.smu.edu.sg/sis_research/4360/), [ICSE 2019 journal-first](https://2019.icse-conferences.org/details/icse-2019-Journal-First-Paper/39/Categorizing-the-Content-of-GitHub-README-Files). | Manual coding of 4,226 sections from 393 sampled GitHub repositories; common WHAT/HOW content; observed omissions in purpose/status. | Explicitly surface **why** and **current status**, not just installation snippets. | Classifier F1 0.746 and a 20-professional perception check do not establish universal documentation quality or usability. |
| **Liu, Noei & Lyons**, *How ReadMe Files are Structured in Open Source Java Projects*, **Information and Software Technology** 148 (2022), article 106924, DOI [10.1016/j.infsof.2022.106924](https://doi.org/10.1016/j.infsof.2022.106924); [University of Toronto author preprint](https://enoei.github.io/papers/liu2022readme.pdf), [replication archive](https://zenodo.org/records/6099362). | Examined 14,901 Java projects; README structural choices correlate with repository stars, and many did not match recommended sections. | Make installation/usage/license and navigation easy to find; review missing essentials. | Correlation with stars is **not causal**; Java/GitHub sample cannot set a universal file count or section order. |
| **Wang et al.**, *Study the correlation between the readme file of GitHub projects and their popularity*, **Journal of Systems and Software** (2023/2024), [publisher abstract](https://www.sciencedirect.com/science/article/pii/S0164121223002017). | Found positive associations between README maintenance/organization indicators and popularity in its studied GitHub sample; discusses reference updates and content evolution. | Prefer regular review of links and updated instructions over static templates left stale. | Reported relationships are observational, affected by project popularity and other confounders; no universal update frequency proven. |
| **Tan, Wagner & Treude**, *Detecting outdated code element references in software repository documentation*, **Empirical Software Engineering** 29, article 5 (2024; published online 2023), DOI [10.1007/s10664-023-10397-6](https://doi.org/10.1007/s10664-023-10397-6); [Monash University record](https://research.monash.edu/en/publications/detecting-outdated-code-element-references-in-software-repository/). | Analysed documentation of >3,000 GitHub projects; reports 28.9% of sampled popular projects with at least one stale reference at observation and 82.3% with one at some point in history. | Add source-change triggers and automated/local checks of references; treat drift as a lifecycle concern. | Specific detector recognizes deleted code references; does **not** detect every semantic stale statement. Percentages apply to the studied sample. |
| **Benjamin D. Lee**, *Ten simple rules for documenting scientific software*, **PLOS Computational Biology** 14(12), e1006561 (2018), DOI [10.1371/journal.pcbi.1006561](https://doi.org/10.1371/journal.pcbi.1006561); [full text](https://journals.plos.org/ploscompbiol/article?id=10.1371%2Fjournal.pcbi.1006561), Harvard affiliation. | A peer-reviewed **guidance/editorial**, recommends basic README with installation, configuration, docs, license, tests, acknowledgements. | Provide a self-sufficient first entry and route to deeper references. | Normative advice rather than experiment measuring the benefit of any specific README architecture. |

## University guidance (not primary empirical studies)

- **Harvard Kempner Institute**, [Documentation and Readability](https://handbook.eng.kempnerinstitute.harvard.edu/s2_swe_for_research/documentation_and_readibility.html): README as the front door, short setup and minimal use, links for depth; documentation type depends on reader task.
- **Cornell University Data Services**, [Writing READMEs for Research Code & Software](https://data.research.cornell.edu/data-management/sharing/writing-readmes-for-research-code-software/): metadata for reuse and preservation, versions, status, contents, license, archiving; higher self-containment can help archival contexts.
- **Johns Hopkins University Open Source Programs Office**, [Public Code Repository Best Practices](https://ospo.library.jhu.edu/learn-grow/public-code-repository-best-practices/): project purpose, setup, help, contributions and review during milestones/releases.
- **University of Birmingham / The Carpentries lesson**, [Building Better Research Software: Software documentation](https://bham-carpentries.github.io/better-research-software/07-software-documentation.html): README as entry or linked routes, separate metadata files and the minimum documentation appropriate to project complexity.

## What the evidence does and does not decide

**Supported pattern:** essential entry information, task-oriented navigation and change-coupled
review reduce avoidable discoverability and drift risks. **Engineering judgment:** where to
split README, number of files, tests to automate, owners and frequency. **Not supported:**
README over N lines is always bad, exact template guarantees adoption, an arbitrary number
of README files improves performance, or source publication certifies the target project's README.

See [sources-and-decisions.md](sources-and-decisions.md) for official engineering documents,
source authority and conflicts.
