# Reader-facing verification and acceptance evidence

## Evidence levels (do not conflate them)

| Level | Example | What it does **not** establish |
|---|---|---|
| Structural inspection | Files exist, headings and links parse | That linked behavior works |
| Render and navigation review | README renders, user finds a task | That installation succeeds |
| Contract cross-check | Command matches `--help`, schema matches source | That runtime effect occurred |
| Authorized execution | Command run, exit status/output/side effects observed | All environments or users succeed |
| Reader usability study | Actual readers complete task | Broader population without sampling |
| Deployed/released observation | Tagged artifact and published docs verified | Future releases keep same behavior |

### Focused acceptance cases

- **AC-01 entry:** A newcomer can identify purpose, target users and honest support status without following an unrelated link. Oracle: compare first page against approved product contract.
- **AC-02 first-run:** The exact path from fresh checkout to safe observable result is complete (prerequisites, CWD, commands, inputs, output, recovery). Oracle: fresh authorized environment; otherwise UNVERIFIED.
- **AC-03 structure:** Every task moved out of root remains discoverable via a clear relative link and has one canonical maintained location. Oracle: link graph and manual navigation.
- **AC-04 factual status:** No planned, deprecated or disabled capability is described as released or generally usable. Oracle: versioned implementation/release evidence and decisions.
- **AC-05 link integrity:** Internal links and headings resolve in the supported renderer. Oracle: inspected target paths and rendered anchor behavior; external URL reachability is a separate check.
- **AC-06 safe examples:** No live tokens or passwords, no production-destructive one-liners without scope and explicit authorization. Oracle: security review and source scan.
- **AC-07 change traceability:** An affected behavior change updates README text or links with the same change, or has an explicit justified exemption. Oracle: diff + source contract + review record.
- **AC-08 split migration:** Existing entry paths and cross-references remain usable or include deliberate migration guidance. Oracle: navigation and link check on changed revision.
- **AC-09 boundaries:** If root describes independent packages, each has either a complete local entry or a clearly linked canonical set of instructions. Oracle: representative first-run per package.
- **AC-10 no manufactured proof:** Test results, performance, screenshots, badges and versions are real or visibly marked illustrative/unverified. Oracle: evidence provenance.

These are suggested evaluation oracles, not automatically authorized SDD acceptance criteria.
Adopt IDs and status vocabulary from the consuming project rather than creating duplicate gates.

## Practical checks without assuming a tool exists

1. Read README source and render under the actual hosting platform, if accessible.
2. Verify all **relative** Markdown links from the file's location; check case sensitivity.
3. Check headings/fragment links in the renderer. A path existing is insufficient for an anchor.
4. Inspect the target version of each command, API example, binary and documentation link.
5. Execute one safe first-run in a clean authorized environment, logging CWD, environment,
   revision, command, exit code, stdout/stderr and expected effect. Avoid unauthorized installs.
6. Test one misconfiguration/failure and recovery path where important.
7. Make a short reader review from the perspective of user, operator and contributor, not just
   project maintainer; this is still a *review*, not a usability study.
8. State precisely which checks ran and which were skipped; do not infer success from plans.

Optional linters and local link checkers can help **if already available**. No special tool,
fixed command, GitHub action or dependency is required by this skill. Benchmark claims demand
actual representative measures and workload context.

## Output evidence record (minimum)

Document modified paths and stable link targets; selected source revision; readers/tasks
covered; commands and results actually observed; any pending manual checks; owner and next
review trigger. Preserve prior notes when other authorities require historical traceability.
