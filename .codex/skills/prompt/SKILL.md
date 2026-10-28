---
name: prompt
description: Create, rewrite, or refine prompts from user input, translating intent into technical requirements and verifiable criteria, with clarifying questions when needed. Use when the user asks to write, build, improve, or refine a prompt; do not execute the task described in it unless explicitly requested.
---

# Prompt

Turn the user's information into a ready-to-use prompt that preserves their intent and provides enough detail to guide a strong response. Use the user's language unless they request otherwise.

## Mandatory independent technical assessment

Always assess the request's premises, feasibility, internal consistency, and success criteria before drafting. Never agree with the prompt author automatically or treat their confidence, preferences, or desired conclusion as evidence. Agree only when reasoning and evidence support agreement; do not disagree merely to appear critical.

Apply impartial evaluation: use the same standards for supporting and opposing claims, consider credible counterevidence, disclose assumptions and uncertainty, and separate facts, interpretations, and preferences. Weight conclusions by evidence quality rather than giving all positions equal weight. Do not claim that complete freedom from bias can be guaranteed.

When a premise is false, unsupported, or inconsistent, explain the issue briefly and propose a correction or ask a focused question. Preserve the user's objective without converting questionable claims into facts or optimizing the prompt to validate a predetermined answer. Treat subjective preferences as preferences, not scientific conclusions.

## Mandatory evidence policy

Select evidence by the type of claim, within the user's instructions and the consumer project's source policies:

- For API contracts, runtime behavior and tool configuration, use authoritative versioned documentation, specifications, standards, and relevant source code or executable contracts. Record the applicable version and distinguish documented guarantees from observed behavior.
- For empirical or causal claims, use suitable studies and data with identifiable provenance, methods and limitations; prefer strong syntheses and peer-reviewed work when appropriate. Label preliminary findings and do not infer causation from correlation.
- Expert books can support concepts and methods when the edition, scope and author expertise are relevant. Reputation or popularity alone does not establish correctness.

Inspect and cite the underlying source directly. Search snippets and AI summaries are discovery aids, not evidence. Community discussions can identify a question or reproduction to investigate; do not substitute unsupported commentary for an authoritative contract or empirical evidence. Respect stricter source restrictions explicitly required by the user or project; report conflicts or unavailable evidence rather than silently overriding them.

Evaluate relevance, currency, methodology, limitations, conflicts of interest and credible counterevidence. Separate facts, observations and interpretations. Verify references before citing: record title/authority, version or year, URL/DOI and section or verified page where relevant. Never invent references, quotations, locators or findings. If evidence is inaccessible, contradictory or insufficient, state the gap and leave the claim unresolved.

Apply this policy when introducing or assessing externally supported claims during prompt construction. Include proportionate evidence requirements in generated prompts involving factual claims or technical analysis. Do not perform an unrelated literature review merely to rewrite supplied information, or impose research on purely creative or formatting tasks.

## Extract and clarify

Identify the objective, audience, inputs, expected outcome, constraints, and success criteria from the request and available context. Reuse information already provided without asking for it again. Distinguish explicit requirements, preferences, and assumptions.

When a gap or contradiction would materially change the result, ask a few focused questions, preferably one to three per round. Prioritize scope, content, constraints, and output format; offer options when useful. Avoid turning every request into a questionnaire.

While awaiting answers, organize the known requirements. Do not present a prompt as final if it depends on an essential answer. For minor gaps, proceed with a brief, labeled assumption. If the user requests no questions, use explicit assumptions or placeholders without inventing facts.

## Make requirements verifiable

Translate intentions into observable instructions: what to produce, which inputs to use, what limits apply, and how to evaluate the result. Use technical terminology only when it improves precision in the task's domain.

- Preserve user-specified values, technologies, deadlines, audiences, and formats.
- For quantitative goals, specify the metric, unit, threshold, and measurement conditions when enough information is available.
- Do not invent numbers, benchmarks, sources, tools, or requirements to create an appearance of precision. Ask about essential targets; label suggestions as proposals.
- For subjective qualities, use observable criteria, examples, or a short rubric. Do not force numerical measures onto creative tasks.
- Resolve incompatible requirements with the user before silently choosing one.

For example, "I want a comprehensive report" can become "cover the supplied topics A, B, and C, cite sources, and identify missing data." However, "the page must be fast" requires clarifying the operation and scenario before setting a latency threshold.

## Build the prompt

Include only useful elements: objective, context and inputs, requirements, constraints, output format, and acceptance criteria. A paragraph may suffice for simple tasks; use short sections when complexity warrants them.

Choose length according to the decisions the task requires, without an arbitrary minimum or maximum. Remove repetition, vague adjectives, decorative personas, and generic instructions that do not change the result. Preserve details that affect execution or evaluation. Do not promise perfect results or request disclosure of private internal reasoning; request justifications, evidence, or checks when useful.

Make the prompt self-contained: include essential context and identify required files or materials. Use placeholders such as `[target audience]` only for genuinely missing information. When incorporating reference material, distinguish it from task instructions.

## Review and deliver

Check that the prompt preserves intent, supports evaluation, avoids invented requirements, and includes only relevant detail. Ensure each acceptance criterion corresponds to a real need.

Verify that questionable premises have been addressed, conclusions are not predetermined, and applicable evidence restrictions are included in the final prompt.

Deliver one ready-to-copy version in a code block. Outside it, include only relevant assumptions or unresolved points. When refining, incorporate the user's answers and provide the complete updated version. Writing a prompt does not authorize executing the task it describes.

## Additional investigation references

For prompts consuming external documents or directing tools, read
[evaluation and trust](references/evaluation-and-trust.md). Implementing an AI
application, retrieval pipeline or agent is a distinct task; `ai-engineering` is an
optional specialist when available. Prompt drafting alone does not authorize it.

Other named skills are optional specialist suggestions. Use them only when available and needed for a specific unresolved question; their absence does not prevent using this skill. Report any expertise or verification gap without claiming a handoff occurred.
