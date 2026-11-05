# README scope, reader journeys and essential content

## Purpose

A repository-level README is the **first useful explanation and map** for a new reader.
Its audience is not uniform: a prospective user wants purpose and capability; a first-time
operator wants a safe installation and first run; a contributor wants development context;
a maintainer wants supported versions and links to authoritative decisions.

## Inspect before writing

Record the repository root, top-level products, existing README locations, package boundaries,
branch/revision, release state, audience, permissions and exact source-of-truth files. Read the
existing setup/build/test instructions, lockfiles and build manifests; do not infer executable
commands from framework familiarity. Check whether the repository is public, private, research,
application, library or monorepo; avoid assuming a public contribution policy.

## Root README minimum, where applicable

| Reader question | Minimum useful answer | Evidence / typical source |
|---|---|---|
| What is this? | Name, one-paragraph purpose and target users | Product contract / scope |
| Why use it? | Main verified use cases and limitations | Implemented behavior / approved releases |
| What is its status? | Prototype, experimental, alpha, supported, deprecated or unknown | Version/roadmap decision; not guesswork |
| How to start? | Preconditions, platform, working directory, installation and one minimal execution | Existing build, tests and actual observed command |
| How do I verify? | Known safe checks, expected class of outcome, failure handling | Commands and checked outputs, not fake PASS |
| Where do I continue? | Task-oriented links: user guide, ops, contributor, API/reference | Real local destinations |
| How do I ask for help? | Actual issue/support route and its access limitations | Real project contact or support policy |
| May I reuse/contribute? | Link to existing license and contribution policy | Actual LICENSE / CONTRIBUTING, never invent |

Optional: architecture overview if crucial to correct onboarding; release/compatibility table;
security disclosure route; troubleshooting for one common failure; screenshot only if current,
accessible and genuinely informative. Status badges must reflect a real maintained signal;
empty or misleading badges are worse than none. If license is undefined, say 'licensing not yet
specified' rather than proposing legal permission.

## Minimal onboarding should be reproducible

- State *where* to execute, on which OS/runtime, from which revision, with which harmless inputs.
- Mark placeholders and outputs clearly. Do not imply a code block was run without observation.
- Distinguish installation (prerequisites), configuration (desired state), first run (effect),
  and cleanup (reversal). Secrets are references or user-provided local environment values,
  not copied real credentials.
- Check failure and permission paths, not only an optimistic success line.
- Keep the shortest complete working path near the top; link advanced variants elsewhere.

## Example outline (illustrative, not a claim about any implementation)

```text
README.md
  # Project name
  One-paragraph purpose and current support status
  ## Quick start (platform/prerequisites/commands/expected observation)
  ## What exists today vs planned
  ## Documentation (task-based links)
  ## Development / contribution
  ## Help, security and license
```

This is **not a universal template**. Remove irrelevant sections or fold them together;
keep information findable, not bureaucratically complete. A project without an executable
entry point must say so and offer the closest truthful validation route.

## Research support and boundaries

GitHub explicitly lists purpose, benefit, getting started, help and maintainers; Google
recommends package purpose, status, usage, contact and links. Harvard's Kempner guide advises
a brief front door and deeper documentation elsewhere. Empirical work by Prana et al. finds
purpose/status gaps in sampled READMEs, not a universal mandatory template. See
[sources](sources-and-decisions.md) and [scientific evidence](scientific-evidence-and-limits.md).
