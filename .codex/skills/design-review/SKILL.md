---
name: design-review
description: Review user journeys, interface behavior, hierarchy and usability; explain design trade-offs and respond to stakeholder feedback using evidence. Use for UX critiques, design decision presentations and review follow-up. Do not use for backend code design, generic meeting advice, unsupported aesthetic judgments or routine implementation of an already agreed component contract.
---

# Design Review

Evaluate whether people can understand and complete the intended task, including recovery. Explain choices so others can assess them. Separate observed defects, evidence-based risks, aesthetic preferences and hypotheses needing user research. Stakeholder support and demonstrated usability are different outcomes.

## Scope and evidence

Collect the user task, audience, constraints, acceptance criteria, relevant flow states and existing conventions. For interface evaluation, inspect the actual interface when available, capture screenshots and reproduce behavior. For supplied mockups, state which interactions are unknown. For a decision explanation or feedback response, use the supplied artifacts, observations, decision status and stated concerns; do not pretend to have inspected a product or run a study.

This skill owns interface evaluation, design rationale and review follow-up. It does not require a full redesign or a meeting. Reusable component/token contracts belong to design-system; backend structural decisions belong to software-architecture; specialized threats belong to application-security. Basic correctness, security and accessibility apply without loading other skills. Load another skill only for a concrete task boundary.

## Workflow

1. **Frame the task and decision.** State the user goal, completion condition, material risks and constraints. Distinguish the product outcome from the immediate review decision. Use existing requirements and decision authority; a small critique needs no full specification process.
2. **Collect relevant evidence.** For an interface critique, trace entry, choices, submission, pending, empty, error, recovery and completion states as applicable. Record screen/state, action and result. Assess hierarchy, labels, feedback, navigation, consequences and consistency. Check keyboard/focus and relevant accessibility criteria when the interface permits; screenshots cannot establish them. For communication-only work, identify what the supplied evidence supports and what remains unknown.
3. **Clarify and classify.** Connect each observation to task impact. Distinguish reproducible failure, plausible risk, preference and research hypothesis. When feedback proposes a control or layout, clarify the underlying need before accepting or rejecting the solution. Confirm material paraphrases; do not infer hidden motives or strengthen someone else's claim.
4. **Compare proportionate alternatives.** Explain the problem, observed or expected user effect, viable options and reasons for the recommendation. Compare real costs, constraints and contrary evidence; a targeted repair may suffice. Use [review method](references/review-method.md) for interface findings. Load [decision communication](references/decision-communication.md) when preparing a rationale, answering objections or recording a review decision.
5. **Resolve the actual decision.** Acknowledge concerns honestly; state disagreement and uncertainty plainly. Revise when new evidence warrants it. Record the chosen option or unresolved question, actual decision status, rationale, material dissent and agreed next step where useful. Continue already authorized reversible work; seek a decision only when a material unresolved choice requires it. Do not interpret silence as new permission.
6. **Validate at the correct level.** Check that the explanation accurately represents evidence and commitments. Separately, replay affected tasks/recovery paths and inspect adjacent states when a product change is available. Test behavioral hypotheses with appropriate research when feasible. Report absent validation; a persuasive explanation is not proof of improved UX.

## Constraints

- Do not invent user reactions, research, metrics, consensus or predictable gains; a familiar pattern or book example is not proof for this audience.
- Do not hide payment, privacy, consent or destructive-action consequences to simplify a flow or win agreement.
- Do not suppress material objections by influence, use sham alternatives, exaggerate losses or deliberately degrade a design to provoke a decision.
- A modal, menu or infinite list is not inherently defective; evaluate purpose and alternatives. Visual uniformity and novelty are not goals by themselves.
- Do not claim accessibility, security or performance from appearance or a single score. Do not dismiss a critical defect as outside the meeting agenda.
- Do not contact stakeholders, publish recordings or assign commitments without corresponding authorization. Drafting a review does not authorize sending it.

## Report

Lead with the consequential finding or decision. Give the artifact/state, evidence, task impact, recommendation, rationale, exceptions/costs and validation method as relevant. For decision communication, add the decision needed or recorded, unresolved concerns and next evidence step. Distinguish inspected, proposed, authorized, implemented and validated. Keep the output proportional; do not manufacture findings, meetings or documents to fill a template.

Other named skills are optional specialist suggestions. Use them only when available and needed for a specific unresolved question; their absence does not prevent using this skill. Report any expertise or verification gap without claiming a handoff occurred.
