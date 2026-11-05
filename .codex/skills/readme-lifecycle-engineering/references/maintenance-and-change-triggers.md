# Continuous README maintenance and drift control

## Documentation should evolve with the implementation

Documentation drift is frequently silent: code can change without a broken build warning.
Treat an affected README as part of the change's acceptance when the change affects a
reader-visible workflow, package setup or support boundary. Keep documentation review
proportional and update it alongside code in the same change where feasible.

## Change-to-document impact map

| Change | Review or update | Evidence needed |
|---|---|---|
| New or removed feature | Purpose/capabilities/status, product limitations, destinations | Actual feature gate/release state |
| CLI command or flags | Quick start, command example, CLI reference | `--help`/CLI behavior on selected version |
| Setup/install, toolchain, OS support | Prerequisites and supported environments | Real lockfiles/toolchain and setup execution |
| YAML schema or behavior | Example links, configuration guide; **preserve the consumer's canonical configuration** | Real schema, validation and projection checks |
| Server/agent protocol or database change | Architecture summary and operational guide | Adopted ADR/contract, not a proposal alone |
| API change | Usage links, examples, compat/deprecation | Versioned API and consumer checks |
| RBAC/auth/secret path | Access and security warnings | Approved permissions/secrets policy, no live keys |
| Release or deprecation | Current status, compatibility matrix, migration | Published version/release proof |
| Split/rename/move file | Relative links, anchors, nav index | Local link resolution and click-through |
| Known outage/incident | Troubleshooting or runbook when generalizable | Incident evidence, not speculation |

## Ownership and review loop

Before writing, identify the canonical source for each assertion: code/manifest, schema,
accepted spec, decision, operational evidence or released documentation. No document should
silently override a higher-authority contract. For each important README section, record an
owner/location and a review trigger (e.g., changes to `Cargo.lock` do not by themselves prove
a new README claim, but toolchain or documented build commands may need review).

Suggested proportional process:

1. During planning: mark reader-visible contracts and docs impacted, not every edited file.
2. During implementation: update the canonical content and README navigation together.
3. During review: check exact command/path/version, audience clarity and negative paths.
4. In CI if available: markdown rendering/lint, local links/anchors and selected safe snippets.
5. At release: compare README status and supported versions with actual release artifacts.
6. Periodic audit: inspect outdated paths, dependencies, screenshots, contact routes and support
   version only when change history or repo activity justifies it. Scheduling is project policy.

## When documentation is intentionally forward-looking

Put future capabilities in an explicitly labeled roadmap/design section or separate planning
record. Do **not** advertise them as working features or simulate verification. State the current
revision and the evidence status. An ADR that proposes gRPC or SQLite is not proof these are
shipped. Distinguish `planned`, `in progress`, `tested`, `released`, and `deprecated` according
to actual product conventions.

## Avoid harmful automation

- A doc generator or LLM can flag missing sections but cannot prove user success or actual
  implementation; require human review of semantic claims.
- CI link success checks only destinations, not conceptual correctness.
- A command that exits 0 may still not exercise the promised operation; inspect outputs/state.
- Never regenerate existing examples from incompatible schemas or invent version numbers.
- Never rehash historical test records to claim they were re-executed.
- Distinguish internal developer docs from safe public install instructions.

See empirical evidence on documentation staleness in [scientific-evidence-and-limits.md](scientific-evidence-and-limits.md)
and operational [verification](verification-and-acceptance.md).
