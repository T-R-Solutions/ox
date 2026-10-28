---
name: technical-documentation
description: Create or maintain technical tutorials, how-to guides, API references, and conceptual documentation as the main deliverable, grounded in a versioned implementation or contract. Skip routine inline comments, standalone ADR decisions, binary document layout, and prompt-only writing.
---

# Technical Documentation

Produce documentation that lets its intended reader complete the stated task or
understand the stated concept. Work in the user's requested format and destination,
preserving repository conventions, canonical sources and existing user changes.

## Establish the reader and source

Identify audience, task, prerequisites, target version/environment and document
type. A tutorial teaches a bounded path; a how-to solves a known task; a reference
states a contract; an explanation develops a concept. Combine forms only when it
helps this reader. A short correction does not need separate planning documents.

Inspect the relevant implementation, schemas, tests, configuration and maintained
documentation. Resolve conflicting sources explicitly; code behavior, intended
contract and observed execution may differ. Record the revision or version needed
to interpret claims. Do not infer supported behavior from a familiar API name.

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

## Completion and maintenance

Deliver the requested document, relevant verification evidence and remaining
reader-visible limitations. Report exact commands and environment for executed
examples; label proposed checks. Do not claim usability studies or successful
reader completion from proofreading alone.

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
