# Evidence policy for prompts with external claims

Read from [SKILL.md](../SKILL.md) when the prompt introduces or assesses factual,
empirical, API or tool-behavior claims that need sources.

Select evidence by the type of claim, within the user's instructions and the consumer project's source policies:

- For API contracts, runtime behavior and tool configuration, use authoritative versioned documentation, specifications, standards, and relevant source code or executable contracts. Record the applicable version and distinguish documented guarantees from observed behavior.
- For empirical or causal claims, use suitable studies and data with identifiable provenance, methods and limitations; prefer strong syntheses and peer-reviewed work when appropriate. Label preliminary findings and do not infer causation from correlation.
- Expert books can support concepts and methods when the edition, scope and author expertise are relevant. Reputation or popularity alone does not establish correctness.

Inspect and cite the underlying source directly. Search snippets and AI summaries are discovery aids, not evidence. Community discussions can identify a question or reproduction to investigate; do not substitute unsupported commentary for an authoritative contract or empirical evidence. Respect stricter source restrictions explicitly required by the user or project; report conflicts or unavailable evidence rather than silently overriding them.

Evaluate relevance, currency, methodology, limitations, conflicts of interest and credible counterevidence. Separate facts, observations and interpretations. Verify references before citing: record title/authority, version or year, URL/DOI and section or verified page where relevant. Never invent references, quotations, locators or findings. If evidence is inaccessible, contradictory or insufficient, state the gap and leave the claim unresolved.

Apply this policy when introducing or assessing externally supported claims during prompt construction. Include proportionate evidence requirements in generated prompts involving factual claims or technical analysis. Do not perform an unrelated literature review merely to rewrite supplied information, or impose research on purely creative or formatting tasks.
