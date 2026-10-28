---
name: engineering-productivity
description: Evaluate engineering tools, workflows, and process changes through actionable questions, appropriate evidence, and explicit decision criteria. Use for developer experience and team workflow decisions; skip runtime profiling, product analytics, individual rankings, and routine code edits.
---

# Engineering Productivity

Help a project decide whether to change a tool or way of working. Start with the
decision, its owner and feasible alternatives. More activity is not necessarily
more useful work; reduced machine time is not necessarily reduced human waiting.

## Frame the decision

Inspect the project's actual workflow, constraints, existing evidence and data
permissions. Identify the affected population, task and time horizon. Describe
what action would change for each plausible result, including keeping the current
approach. If the result cannot affect a decision, explain why further measurement
is unnecessary rather than inventing a study.

This skill studies engineering work. Runtime latency/capacity investigation and
interface usability have different units and methods; consult a specialist only
for a concrete unresolved question, when available. No other skill is required.

## Develop a proportionate evidence plan

1. Connect **goal → observable signal → measure**. Explain why the measure can
   represent the goal, what it omits and what could improve it without helping
   developers. Record practical effects worth acting on before selecting a winner.
2. Select a method for the uncertainty: interviews/observation to discover causes,
   surveys for reported experience, operational records for observed workflow, or
   a controlled comparison where feasible. Existing authorized aggregate evidence
   may suffice. Do not prescribe an experiment for every decision.
3. Identify selection, nonresponse, survivorship, recall, novelty and measurement
   biases relevant to that method. Define the population and denominator; voluntary
   adopters do not automatically represent all users. Separate elapsed, active,
   blocked and overlapping time; a shorter build may run entirely in the background.
4. For a comparison, describe assignment, baseline, observation window, confounders,
   independent units and possible spillover/learning effects. Randomization or a
   defensible alternative needs its actual assumptions. Association alone does not
   establish the tool caused the result. Do not treat repeated observations of one
   team as independent teams or choose stopping/exclusions after seeing a winner.
5. Minimize collection to what the decision needs. Use authorized sources and
   aggregation appropriate to the population; small groups can remain identifiable.
   Do not collect employee telemetry, conduct outreach or publish results merely
   because an evidence plan exists. Preserve applicable consent/access/retention rules.
6. Compare evidence with implementation, migration, training and maintenance costs.
   Examine contrary observations and affected subgroups without inventing causal
   certainty. A useful outcome can be a bounded pilot, retaining the current tool,
   or identifying the smallest missing observation.

## Deliver a decision that can be revisited

Provide the question and options, goal/signal/measure mapping, evidence and method,
uncertainty, recommended action, responsible role and a concrete follow-up trigger.
Keep a small decision small; do not manufacture dashboards or a universal KPI set.
State which collection or comparison was actually executed and what remains proposed.

Reject commits, lines of code, tickets or hours as standalone individual productivity
rankings. They omit task difficulty, collaboration and outcomes and invite gaming.
Do not replace them with another unvalidated individual score. Team throughput,
survey sentiment, build speed and defect counts also need context and trade-offs.
Do not claim a numerical improvement or causal effect without supporting evidence.

Basis: *Software Engineering at Google*, first edition, chapter 7 (physical
151–166), with chapter 3 (94) and chapter 23 (525–530). This is a portable decision
workflow, not Google's staffing model, a performance-management system or a mandate
to collect data. Adapt it to the destination project.

## Adjacent responsibilities

Software-delivery owns implementation of build/pipeline/release mechanics. Use this skill for evidence about developer workflows, not automatically for every pipeline edit.
These are optional available capabilities, not dependencies of this folder.
