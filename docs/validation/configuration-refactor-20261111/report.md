# Configuration cohesion review — 2026-11-11

The maintainer authorized local review/refactoring of skills, SDD and AGENTS.
No application code, profile membership, permission, commit or publication change.

## Coverage and decisions

Static inventory covers 225 current files: 31 skill entries, their resources/UI
metadata, 31 bridges, templates, AGENTS, workflow/evidence and profile. Selection
boundaries and resource purposes were examined across the catalog; deeper textual
comparison targets the nine repeated specialization entrypoints and bridge boilerplate.
This is not a claim to have rerun every specialized method or verified every external
source. Full semantic efficacy for all resources requires representative consumers.

- 26 bridges now reference shared routing/evidence rules; all contribution-table
  lines remain byte-equivalent. Five bridges without the repeated blocks stay intact.
- Nine specialized entries retain their numbered technical procedures, metadata,
  reference targets and optional handoff questions. Repeated generic prose is shorter;
  missing versions still require documentation, missing permissions still block effects,
  and examples remain fixtures rather than product policy. Evaluation cases are selected
  for actual scope, without imposing every fixture on every consumer task.
- AGENTS remains the operational entry, retaining explicit Toolbox selection verbatim,
  authority/permission boundaries, visual-contract links and documentation before closure.
- The stale blanket claim that specialization scenarios can never have verified integration
  was replaced by the actual criterion-specific technical-acceptance authority.
- Profile membership and UI invocation metadata stay unchanged: no new capability,
  circular dependency or recursive activation was introduced. Reusable techniques for
  non-current backends are not obsolete merely because the MVP does not use them.
- Shared workflow/evidence/templates remain the authorities. No generic rules file was
  added to standalone skills: that would add a dependency and extra context loading.
- bridge_version remains 1, the validator's format version. Content SHA-256 identifies
  this editorial revision. Initial use of 2 was rejected and corrected, not waived.

## Measurements and preservation

The 36 compacted files remove 15893 bytes and 2492 whitespace-separated words.
These are input-text measurements, not tokenizer counts, billing savings or improved
model behavior. Additional audit/evidence files are not automatically loaded.
changes.json gives per-file sizes; inventory.json gives observed hashes; preservation.json
records all 36 comparisons. Preimages under before/ preserve existing local work.
Succession accepts only the exact new content and authenticates predecessors; unknown
changes remain unknown. Existing historical registries are unchanged.

## Verification and limits

Focused structural, succession and metadata checks are recorded in checks.log and
converge.md. Negative cases cover unknown mutation, modified registry/preimage,
symlink and downgrade. The check of retained technical paragraphs is an independent
byte comparison, not a behavioral skill evaluation. No native UI, full Toolbox run,
remote model evaluation or assistive-technology test is necessary to validate this
textual/configuration change, and none is claimed.

Changed inputs invalidate dependent observations. before-evidence/ keeps their exact
prior documents; unaffected evidence records remain active. New inspections do not
renew old execution claims. Technical criteria without sufficient current evidence
remain UNVERIFIED; product criteria remain non-decided where affected. Reexecute
specific consumer/oracle scenarios on the current skill bytes to decide those criteria.
No application result is approved by this refactor.

## Documentation disposition

Updated AGENTS, project state, bridge guidance, skill integration guide and
configuration-cohesion spec/plan/tasks/traceability/convergence. Workflow's existing
closure rule remains the single normative rule. Catalog/profile need no membership
change; their identities and paths are checked. Historical evidence and preexisting
visual implementation are preserved. General skill methods, resource provenance,
commit-specific user choices and technical safety constraints were retained.
