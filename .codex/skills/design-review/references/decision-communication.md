# Communicating and revising design decisions

Load this reference for an interface decision explanation, feedback response or review follow-up. It is not a mandatory meeting process. The cards are contextual engineering synthesis of Tom Greever's *Articulating Design Decisions*, read in the authorized Portuguese translation of the English second edition: local PDF (historical library source: `docs/system/Articulando-Decisoes-de-Design.pdf`; not required at runtime), Novatec 2021. Locations below are one-based physical PDF pages, not printed pages. Research coverage (historical library source: `system/research/greever-coverage.json`; not required at runtime) records all reading, visual inspection, conflicts and source defects; normal tasks need not load it.

The author focuses on gaining support and assumes a sound design in the preface (PDF 19). Recheck that assumption: a clear explanation can reveal that the proposed design is wrong. Neither the author's experience nor stakeholder agreement demonstrates usability, accessibility or business improvement.

## Prepare the decision, not a sales pitch

**Action/context:** Before explaining a consequential choice, identify the user task, current artifact/version, fidelity, relevant acceptance criteria, stated constraints and immediate decision. Distinguish a working prototype from an aspiration. Tailor the explanation to the audience's stated responsibilities and questions, without guessing motives. **Evidence:** chapters 1–3, PDF 35–46, 47–69 and 75–104; chapter 11, PDF 249–252. **Rationale:** shared context prevents a future vision from being mistaken for current capability and a preference discussion from replacing the task. **Exceptions/costs:** collect only missing facts that can change the decision; routine authorized work needs neither a stakeholder map nor a meeting. Preparation and prototypes consume time. **Validate:** another reader can identify what is changing, why, what remains unproven and which decision is actually needed.

Use a short written explanation when sufficient. If presenting visually, provide readable material, describe meaningful visuals and make relevant content available in an accessible format; screen sharing alone can exclude participants. Choose the medium with accessibility and privacy in mind. This qualification draws on [W3C WAI presentation guidance](https://www.w3.org/WAI/teach-advocate/accessible-presentations/), especially material preparation and delivery sections; it is informative guidance, not a conformance assessment. No fixed video length, camera requirement or learning-style diagnosis is prescribed.

## Find the need behind feedback

**Action/context:** When feedback names a solution, ask which task, constraint or observed problem it addresses. Paraphrase faithfully and confirm material ambiguity. Acknowledge the concern honestly before explaining agreement, disagreement or uncertainty. **Evidence:** chapter 4, PDF 105–129; chapter 5, PDF 130–152. **Rationale:** a request to reorder inputs may concern exported column order instead; those contracts might be independent. **Exceptions/costs:** a verified defect needs repair, not ceremonial clarification. A direct refusal can be appropriate for an unsafe or infeasible proposal. Clarification adds delay; continue independent work. **Validate:** the response addresses the actual concern, does not strengthen the speaker's claim and makes no unsupported commitment.

Illustrative, not executed: Before: “Yes, we will reorder the form.” After: “The concern is matching the downstream report's columns. I will check whether export order can change while preserving the validated input flow. If they are coupled, I will compare the affected paths before proposing a change.” This preserves the existing form contract provisionally; it does not claim that decoupling already exists.

The author's habitual positive opening becomes sincere acknowledgment here, not a requirement to say yes. Do not fabricate personal stories, diagnose personalities, conceal disagreement or use politeness as implied approval.

## Compare real alternatives with checkable evidence

**Action/context:** Explain the problem, the proposed intervention, observed or hypothesized user effect, business objective and relevant alternatives. When interaction sequence matters, use a bounded prototype; for layout differences, compare equivalent content, viewports and criteria. Keep source, method and contrary observations available. **Evidence:** chapters 1 and 6, PDF 35–46 and 153–171; chapter 7, PDF 172–191. **Rationale:** a selected mockup alone hides competing costs and uncertainty. **Exceptions/costs:** trivial fixes need no alternatives gallery; research or prototype cost should be justified by uncertainty and change impact. A known criterion failure may warrant direct repair. **Validate:** test the intended task and guardrails, not only the favored metric; distinguish a demonstration from user research and before/after correlation from causation.

Example, illustrative and not executed: collapsing filters exposes more results, but can reduce discoverability. Compare finding an item, changing filters, empty-result recovery and keyboard access; do not claim that more visible items prove a better experience. A rise in cart additions does not establish completed purchases or absence of accidental additions.

Attach scope to data: population, task, environment, collection period, measurement boundary and limitations when available. Label predictions as hypotheses. Book percentages and illustrative quotes are not project measurements. Missing data does not prove a preference wrong, but limits confidence. Verify present platform capabilities in official documentation before invoking a historical technical constraint.

## Seek an explicit decision without manufacturing agreement

**Action/context:** For a material unresolved choice, state the recommendation, trade-offs, uncertainty and decision needed from the authorized owner. Use open questions that permit disagreement. **Evidence:** chapter 8, PDF 192–204; chapter 6, PDF 165–171. **Rationale:** a decision must distinguish permission to proceed from a prediction that the design will work. **Exceptions/costs:** unanimous taste is unnecessary, and already authorized reversible work needs no additional approval. Deliberation has an opportunity cost; defer only when the expected evidence can change the choice. **Validate:** record actual decision status, authority, conditions and material dissent; identify what would reopen the decision. Silence, enthusiasm and rehearsal are not validation or new authorization.

The source's IDEAL worksheet organizes problem, solution, user impact, business purpose and agreement (PDF 204; [public worksheet](https://tomgreever.com/assets/download/IDEALResponseWorksheet.pdf)). Use it only as a memory aid. This skill replaces pressure to secure assent with an accurate decision or an explicit unresolved question. It rejects leading pressure described on PDF 194–195, staged coalitions, decoy alternatives, fabricated scarcity and inflated consequences. These are deliberate qualifications, not claims that the author prescribed this revised method.

## Preserve decisions and dissent in follow-up

**Action/context:** After a review that changes direction or creates work, keep a concise record linked to the artifact: decision/status, rationale and evidence, unresolved concerns, agreed owner/action and checkpoint when applicable. **Evidence:** chapter 4, PDF 117–124; chapter 9, PDF 205–216. **Rationale:** recording why makes later handoffs and revisions inspectable. **Exceptions/costs:** reuse the existing source of truth; avoid transcripts and unnecessary personal data. Do not invent owners or deadlines. A draft note is sufficient when sending or task assignment is not authorized. **Validate:** compare the record with what was actually decided, preserve relevant minority objections and provide a correction path.

Condense repetitive or irrelevant detail, not inconvenient evidence. Do not filter objections by hierarchy. Do not intentionally break CSS to prompt a reaction, or convert a no-response deadline into permission. When a choice is blocked, prepare a reversible proposal within existing authority and state the missing decision.

A compact record can be one paragraph:

```text
Artifact/version and task: ...
Evidence and constraints: ...
Recommendation and viable alternative: ...
Decision status and authority: proposed / explicitly decided / unresolved ...
Rationale, costs and material objections: ...
Agreed next action and validation, or owner/checkpoint still unknown: ...
```

This is an illustrative writing aid, not executable code or a required file format. Omit unnecessary fields; never fill unknowns with invented facts.

## Reopen a decision when the evidence changes

**Action/context:** When feedback or outcomes challenge the choice, investigate changed requirements, misunderstanding, unmet needs and actual task failures. Revise the design or explanation, acknowledge supported mistakes and show the consequences for scope and delivery. **Evidence:** chapter 10, PDF 217–236; chapter 11, PDF 237–255. **Rationale:** defending the original design can preserve a mistaken assumption; an objection may expose a problem beyond the disputed control. **Exceptions/costs:** disagreement alone does not prove error, and one metric does not isolate a cause. Bound investigation by risk and the information needed; avoid recurring review rituals without a purpose. **Validate:** revisit the affected end-to-end task, preserve still-valid contracts and check regressions; record causal uncertainty and follow-up evidence.

Separate three results: the explanation was understood; the owner made a decision; the changed product met its acceptance criteria. A successful result in one category does not establish the others. Human usability, accessibility and business effects still require appropriate evidence.
