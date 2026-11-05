# One README or several? Documentation topology and information architecture

## Rule of decision

There is **no scientifically established optimum number of READMEs or line limit** for all
projects. Use a single root README until independent audiences, code ownership, release
cycles or tasks make it difficult to find a complete starting path. Split by reader task
and canonical ownership, **not** automatically by file length or every new feature.

## Placement and destination

| Content | Prefer | Why / caveat |
|---|---|---|
| Project identity, current status, quick start, navigation | Root `README.md` | Single first landing page; stable entry |
| Independent package/library/agent with its own installation | Package-level `README.md` | Local contract and next steps; avoid cloning the root |
| Task tutorial for novices | `docs/tutorials/` or equivalent | Learning path independent from reference |
| A task procedure (deploy, restore, rotate key) | `docs/how-to/`, ops/runbooks | Specific outcome, prerequisites and recovery |
| Protocol, schema, CLI/API and supported options | `docs/reference/` | Lookup accuracy and versioned detail |
| Architecture rationale, concepts and trade-offs | `docs/explanation/`, ADR | Explanations distinct from facts and operational steps |
| Contribution process | `CONTRIBUTING.md`, if adopted | Avoid duplicating instructions across packages |
| Support/release notes | Actual support policy, `CHANGELOG.md` or release notes | One maintained source per version/status |
| Security disclosure | `SECURITY.md`, if adopted | Never publish a non-existent contact route |
| License | Actual `LICENSE` | README only points to real legal text |

The names above illustrate *content ownership*, not required directory structure or
runtime configuration. A smaller repository may keep short task instructions inline.

## Diátaxis as an organizing lens, not a mandate

- **Tutorial**: teach a first experience and build confidence.
- **How-to**: achieve a specific task; assumes some background.
- **Reference**: describe precise interfaces, schemas and behavior.
- **Explanation**: explain causes, concepts and design decisions.

A README can briefly introduce each and link out. Do not force all four to have separate
folders before material exists; do not mix extensive API tables into first-run instructions.

## Migration procedure when splitting

1. Audit links into/out of the README, including deep heading anchors and external users.
2. Identify which single file will own each moved topic; preserve non-duplicated statements.
3. Move complete self-contained material to a stable destination and leave a brief context
   sentence with a **relative link** where a user would expect it.
4. Update links in docs, package READMEs, contribution instructions and SDD references.
5. Check GitHub rendering, anchors, relative paths and other supported renderers.
6. Review whether bookmarks to headings may have broken; use compatibility notes or redirects
   where the platform supports them. Avoid promising automatic redirects in raw Git.
7. Keep history in version control; archive past release instructions only when the consumer
   needs them and label versions explicitly.

## Cases and trade-offs

**One package:** root README plus links; no artificial docs tree. **Multi-component application:**
root README introduces product scope and its deployables; server/agent READMEs only if
independent build/install/troubleshooting genuinely justifies them. **Extensive manuals:**
`docs/` navigation with root links; package READMEs remain short and local. **Archived research
software:** Cornell notes that a more self-contained README can make sense when preservation
is more important than live links. **GitHub vs Google placement:** GitHub recognizes READMEs in
root, `.github` and `docs`, with precedence rules; Google's styleguide advocates package-level
root READMEs outside docs. These are different platform/style **conventions**, not contradictory
laws; choose the repository's actual host and maintain one intended landing page.

The four documentation kinds come from the Diátaxis framework. No fixed filename taxonomy is
implied by scientific evidence. See [sources](sources-and-decisions.md).
