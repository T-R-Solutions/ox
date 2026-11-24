---
name: prompt
description: Create, rewrite, or refine prompts from user input, translating intent into technical requirements, guardrails and measurable acceptance criteria, with clarifying questions when needed. Use when the user asks to write, build, improve, or refine a prompt, or when a consumer project's workflow requires converting a work request into an operational prompt before execution; do not execute the task described in it unless explicitly requested or required by that workflow.
---

# Prompt

Turn the user's information into a ready-to-use prompt that preserves their intent and provides enough detail to guide a strong response. Use the user's language unless they request otherwise.

## Mandatory independent technical assessment

Always assess the request's premises, feasibility, internal consistency, and success criteria before drafting. Never agree with the prompt author automatically or treat their confidence, preferences, or desired conclusion as evidence. Agree only when reasoning and evidence support agreement; do not disagree merely to appear critical.

Apply impartial evaluation: use the same standards for supporting and opposing claims, consider credible counterevidence, disclose assumptions and uncertainty, and separate facts, interpretations, and preferences. Weight conclusions by evidence quality rather than giving all positions equal weight. Do not claim that complete freedom from bias can be guaranteed.

When a premise is false, unsupported, or inconsistent, explain the issue briefly and propose a correction or ask a focused question. Preserve the user's objective without converting questionable claims into facts or optimizing the prompt to validate a predetermined answer. Treat subjective preferences as preferences, not scientific conclusions.

## Evidence for external claims

When the prompt introduces or assesses factual, empirical, API or tool-behavior claims,
read [evidence policy](references/evidence-policy.md) and include proportionate evidence
requirements in the generated prompt. Never invent references, quotations or findings.
Do not impose research on purely creative, formatting or rewriting tasks.

## Apply the consumer project's rules

When the prompt will be executed inside a project, read that project's governing
documents (for example its constitution, workflow or contribution rules) before
drafting. Carry into the prompt the principles, restrictions, non-negotiable
requirements, required prompt structure, closure steps and permission limits that
apply to the request. Cite the document that each imported rule comes from. Do not
invent project rules, and do not copy one project's policy into an unrelated prompt.
If the project prescribes a structure, section names or a forbidden-terms list,
use them exactly.

## Extract and clarify

Identify the objective, audience, inputs, expected outcome, constraints, and success criteria from the request and available context. Reuse information already provided without asking for it again. Distinguish explicit requirements, preferences, and assumptions.

When a gap or contradiction would materially change the result, ask a few focused questions, preferably one to three per round. Prioritize scope, content, constraints, and output format; offer options when useful. Avoid turning every request into a questionnaire.

While awaiting answers, organize the known requirements. Do not present a prompt as final if it depends on an essential answer. For minor gaps, proceed with a brief, labeled assumption. If the user requests no questions, use explicit assumptions or placeholders without inventing facts.

A prompt may be delivered as **provisional** while questions are open: mark each
criterion whose metric, method or expected result depends on an answer as pending
and link it to its question (for example `PENDING: Q-1`, or the consumer project's
marker). Number the questions. When an answer arrives, rewrite the pending criterion
in full form and remove the marker. A provisional prompt states which work is blocked
by which question; work that does not depend on open questions may proceed.

## Make requirements verifiable

Translate intentions into observable instructions: what to produce, which inputs to use, what limits apply, and how to evaluate the result. Use technical terminology only when it improves precision in the task's domain.

- Preserve user-specified values, technologies, deadlines, audiences, and formats.
- For quantitative goals, specify the metric, unit, threshold, and measurement conditions when enough information is available.
- Do not invent numbers, benchmarks, sources, tools, or requirements to create an appearance of precision. Ask about essential targets; label suggestions as proposals.
- For subjective qualities, use observable criteria, examples, or a short rubric. Do not force numerical measures onto creative tasks.
- Do not leave unmeasurable qualifiers in requirements or criteria. Replace each with its observable form: "fast" → operation, scenario, metric, unit and threshold; "error-free" or "robust" → the named tests or checks and the failure cases covered; "beautiful" or "clean" → the named design rule or reference and how adherence is checked; "complete" or "everything" → an enumerated list; "simple" or "intuitive" → steps, shortcuts or states that are defined. If the observable form is unknown and essential, ask.
- Write each acceptance criterion as one line with three parts: the observable condition, the method that checks it (command, test or inspection) and the expected result. A criterion without a method or an expected result is incomplete.
- Resolve incompatible requirements with the user before silently choosing one.

For example, "I want a comprehensive report" can become "cover the supplied topics A, B, and C, cite sources, and identify missing data." However, "the page must be fast" requires clarifying the operation and scenario before setting a latency threshold.

## Define guardrails

Every prompt states what must **not** be done, as explicit negative instructions:
out-of-scope changes, behavior and files that must be preserved, actions that need
separate authorization (for example commits, publication, downloads, destructive
operations) and shortcuts that are forbidden (for example weakening a criterion to
make a check pass). Take guardrails from the user's request and the consumer
project's rules; do not invent restrictions that change the user's objective.
Keep guardrails in their own division or section, separate from requirements.

## Build the prompt

Include objective, context and inputs, requirements, guardrails, output format, acceptance criteria, and an explicit task completion criterion. When the consumer project prescribes divisions, use them in its order. A paragraph may suffice for simple tasks; use short sections when complexity warrants them.

Choose length according to the decisions the task requires, without an arbitrary minimum or maximum. Remove repetition, vague adjectives, decorative personas, and generic instructions that do not change the result. Preserve details that affect execution or evaluation. Do not promise perfect results or request disclosure of private internal reasoning; request justifications, evidence, or checks when useful.

Make the prompt self-contained: include essential context and identify required files or materials. Use placeholders such as `[target audience]` only for genuinely missing information. When incorporating reference material, distinguish it from task instructions.

## Mandatory task completion criterion

Every generated or refined prompt must explicitly state when the described task
may be declared finished, in the user's language. Use a labeled sentence for a
simple task or a dedicated section for a complex one. Name the required
deliverables, observable acceptance conditions, and checks or evidence needed to
support completion. Avoid vague instructions such as "finish everything".

Incorporate the consumer project's applicable closure requirements, including
documentation updates, required review/validation and activity records, without
inventing new gates or permissions. When a project requires an append-only task
log, explicitly include its path and the requirement to append the completed
task's work without deleting or overwriting existing information. Obtain those
requirements from the supplied context or project authorities; do not impose a
particular project's policy on unrelated prompts.

Require the final response to report the delivered result, checks actually
performed and remaining limitations. If a mandatory condition is unmet or cannot
be verified, report the task as incomplete or blocked, with the missing condition
and resumption step, rather than claiming completion. Keep the distinction between
delivering the prompt and executing the task it describes.

## Review and deliver

Check that the prompt preserves intent, supports evaluation, avoids invented requirements, and includes only relevant detail. Ensure each acceptance criterion corresponds to a real need.

Verify that questionable premises have been addressed, conclusions are not predetermined, and applicable evidence restrictions are included in the final prompt.

Before delivery, verify that the prompt itself contains an explicit, verifiable
task completion criterion and the applicable closure requirements; commentary
outside the ready-to-copy prompt does not satisfy this requirement. Also verify
that guardrails are present, that every criterion has a method and an expected
result or is explicitly pending on a numbered question, and that no unmeasurable
qualifier remains outside a pending criterion.

Deliver one ready-to-copy version in a code block. Outside it, include only relevant assumptions or unresolved points. When the consumer project's workflow names a destination for the prompt (for example a section of a task record), write it there in the prescribed format instead of repeating it in chat. When refining, incorporate the user's answers and provide the complete updated version. Writing a prompt does not authorize executing the task it describes.

## Additional investigation references

For prompts consuming external documents or directing tools, read
[evaluation and trust](references/evaluation-and-trust.md). Implementing an AI
application, retrieval pipeline or agent is a distinct task; `ai-engineering` is an
optional specialist when available. Prompt drafting alone does not authorize it.

Other named skills are optional specialist suggestions. Use them only when available and needed for a specific unresolved question; their absence does not prevent using this skill. Report any expertise or verification gap without claiming a handoff occurred.
