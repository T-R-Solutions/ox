# Prompt execution contract — 2026-11-19

The maintainer explicitly requests automatic use of the prompt skill for every
request, a five-part operational prompt saved before execution, cumulative
analysis/planning, and a final report of work and unfinished items. This decision
adopts that request in the Ox caller, with the original request retaining authority.

## Decision and boundaries

Add one explicit normative section to AGENTS.md and one to sdd/workflow.md.
The workflow owns detailed procedure, local append-only artifacts, revisions,
five stages and outcome reporting. AGENTS points to it. Keep the generic prompt
skill, catalog, profile and bridge intact: creating a prompt artifact is now
explicitly requested by the Ox entry contract. Other skill use remains selective.
The host read-only boundary on .codex is respected.

An instruction-only adoption is sufficient for this governance request; a CLI
interceptor or Rust runtime change is outside scope. Instructions and structural
checks cannot guarantee that every client/model will comply. Prompt-only requests
authorize prompt delivery, and later user restrictions supersede standing defaults.
Read-only questions have proportional inspection methods and the standing records;
an explicit prohibition on writes blocks persistence rather than being bypassed.
Internal delegation does not recursively create another user task.

The existing document_ledger.validate_authority seam now requires exactly these
two additional sections, binding each normalized body to its reviewed section
digest. Existing protected sections, historical terminal authentication and
unknown-section rejection remain unchanged. No historical registry, terminal,
evidence or old result hash is renewed. A missing or altered new contract rejects;
restoring the previous complete authority also rejects. The ledger source itself
continues under its current code-review contract, without a new successor module.

## Alternatives and consequences

Changing the reusable skill would impose Ox policy on other consumers and require
writes outside the host boundary. Editing existing protected preambles would
broaden historical succession unnecessarily. Allowing arbitrary new sections
would weaken the existing negative oracle. Explicitly bound additive sections
provide the bounded adoption requested here.

The .ai files remain local and ignored, created on demand; they are histories,
not authority, acceptance or scheduler state. The existing root activity log,
documentation requirements, five evidence states and independent gates remain.
docs/development/codex-agents.md already requires AGENTS/workflow and needs no
duplicate policy. The catalog/profile/bridge still select prompt creation, which
the new caller requests on every entry.

Review trigger: changed prompt divisions, log paths, authority boundaries or stage
semantics require an explicit contract revision and new independent review.
Recovery restores only this task's delta using its observed preimages, preserving
unrelated work and recording any correction append-only.
