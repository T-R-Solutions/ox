---
name: technical-documentation
description: Create or maintain source-grounded technical tutorials, how-to guides, API references and explanations with Mermaid, professional visual systems, diagrams, charts and imagery verified for the delivery renderer. Skip routine inline comments, standalone ADR decisions, binary document layout and prompt-only writing.
---

# Technical Documentation

Produce documentation that lets its intended reader complete the stated task or
understand the stated concept. Work in the user's requested format and destination,
preserving repository conventions, canonical sources and existing user changes.
Deliver polished, coherent documentation whose visual quality can be inspected
and measured. Use Mermaid for relationships, processes, sequences and states;
use charts for real data and images for information the reader needs to see.
Visual sophistication comes from composition, hierarchy, semantic iconography
and production quality, not extra nodes, gradients, emoji or decorative badges.

## Establish the reader and source

Identify audience, task, prerequisites, target version/environment and document
type. A tutorial teaches a bounded path; a how-to solves a known task; a reference
states a contract; an explanation develops a concept. Combine forms only when it
helps this reader. A short correction does not need separate planning documents.

Inspect the relevant implementation, schemas, tests, configuration and maintained
documentation. Resolve conflicting sources explicitly; code behavior, intended
contract and observed execution may differ. Record the revision or version needed
to interpret claims. Do not infer supported behavior from a familiar API name.

## Plan the visual explanation

For a substantive new document or redesign, identify the reader's questions and
assign each useful visual a purpose, source and place in the narrative. Include
Mermaid when behavior or relationships benefit from a diagram; select sequence,
state, ER or architecture views by meaning rather than using flowcharts for
everything. Short corrections need no illustration quota or unrelated redesign.

Establish the delivery surface (repository Markdown, documentation site, PDF or
slides), actual renderer/version, content width, themes and export needs before
choosing syntax, layout and icon registration. A Mermaid fence alone does not
prove host support. Keep editable sources and provide an inspected export where
native rendering cannot deliver the requested visual quality.

Translate aesthetic requests using [visual-quality.md](references/visual-quality.md):
measurable layout, typography, contrast, icon consistency, responsive reading and
zero clipping/missing glyphs. Apply the host's design system first; its absence
calls for a small documented visual system, not arbitrary styling per figure.
That reference separates release blockers, configurable defaults and standards.

- For Mermaid, professional icon nodes, shared themes, compatible exports and
  render review, read [mermaid.md](references/mermaid.md).
- For licensed SVG icon families, screenshots, illustrations, data charts and
  asset provenance, read [media-and-data.md](references/media-and-data.md).
- For independent acceptance scenarios and review evidence, use
  [evaluation-cases.md](references/evaluation-cases.md).

Use a coherent vector icon family with a consistent grid, stroke and optical
weight for component/role illustrations; use verified product marks only for
actual products. Generic flowchart shapes still encode decisions and terminals,
but are not substitutes for a designed architecture illustration. Never trade
labels, legibility, accuracy or renderer compatibility for ornament. If the
required presentation cannot be rendered, report that gap rather than quietly
delivering a basic diagram as finished enterprise-quality output.

## Author and verify

1. Define what successful use looks like. Include prerequisites the reader must
   actually satisfy, including working directory, input/state, permissions and
   dependencies. Discover actual commands and entry points; do not invent a build.
2. Write the smallest complete route to that outcome. Distinguish commands from
   output, supply meaningful example values and explain placeholders that the
   reader must replace. Describe important errors, effects and recovery, not only
   a happy-path result. Never include real credentials or private production data.
3. Keep API names, argument types/defaults, returns, null/absence, failure behavior
   and side effects aligned with the selected implementation or contract. Explain
   deliberate compatibility differences and mark genuinely illustrative code.
4. Verify the documented path in an isolated authorized environment when available.
   Follow the reader's prerequisites and directory assumptions; check actual exit
   codes, outputs and resulting state. Compilation is not execution. An HTTP HEAD
   response does not prove a GET download or that an archive can be used. Validate
   the relevant operation, artifact and contents before claiming that result.
5. Check links, identifiers and versions against the claimed destination. A link
   that resolves to a generic landing page does not verify the named API. Separate
   local checks, external source consultation and unexecuted instructions. If a
   prerequisite is absent, state the specific unverified step without declaring
   the whole procedure tested or changing its contract to pass.
6. Review the document from the reader's starting point. Remove hidden setup,
   contradictions, obsolete routes and repetition. Check neighboring references
   when changing a canonical contract. Keep content ownership and maintenance
   proportional: record version, responsible location/role and a useful update
   trigger where the content can become stale; a small note needs no review board.
7. Render and inspect each changed visual in the delivery surface. Check the
   rubric at intended size, narrow width, supported light/dark backgrounds and
   zoom; correct clipped labels, missing icons, ambiguous arrows and tiny text.
   Verify figures against sources/data, include accessible titles/descriptions,
   captions and a text/table equivalent for essential meaning. Capture the
   renderer/version, output identity, test sizes, observed defects and remaining
   gaps. Parsing, rendering, visual inspection and reader effectiveness are
   different checks; never claim a later check from an earlier one.

## Completion and maintenance

Deliver the requested document, relevant verification evidence and remaining
reader-visible limitations. Report exact commands and environment for executed
examples; label proposed checks. Do not claim usability studies or successful
reader completion from proofreading alone.
For visual deliverables, return the editable source, rendered assets when needed,
provenance/license information, quality-gate results and maintenance location.
Do not fabricate chart data, alter evidence screenshots or use generated images
as proof of an actual interface. A numerical style score cannot excuse incorrect
content, unreadable labels or unsupported rendering.

Prefer one canonical maintained explanation with appropriate links over copied
instructions that drift. For obsolete material, retain historical identity when
required and clearly point to the applicable replacement. Do not rewrite old
execution records to resemble a fresh run. Follow repository preservation rules.

Documentation work does not authorize publishing, deployment, external messaging,
dependency installation or production mutation. Continue already authorized local
verification and edits; request a missing fact only when it changes the result.
Other skills or tools may help a specific unresolved domain or format question
when available; they are not mandatory dependencies of this workflow.

Basis: *Software Engineering at Google*, first edition, chapters 3 and 10
(physical 77–89 and 213–233). Documentation is the main deliverable here; ordinary
comments and a feature's own ADR remain with their existing engineering workflows.

## Adjacent responsibilities

A database, delivery, diagnostics or evolution specialist is optional only when a concrete technical uncertainty prevents correct documentation. Documentation as the main deliverable remains here; no automatic specialist chain.
These are optional available capabilities, not dependencies of this folder.
