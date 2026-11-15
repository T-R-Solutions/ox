---
name: ai-engineering
description: Build, evaluate, and diagnose applications using foundation models, including retrieval, tool-using agents, model adaptation, and inference trade-offs. Use for implementation or evaluation of an AI application; skip prompt-only writing, ordinary deterministic software, and training a foundation model from scratch.
---

# AI Engineering

Make the application succeed at its actual task under explicit quality, authority,
latency and cost constraints. Model fluency, valid JSON and a high benchmark score
are different from a correct completed task.

## Establish the contract

Inspect the existing application, model/provider configuration, input sources,
tool permissions, data rights, evaluation examples and deployment constraints.
Record the task, supported population, unacceptable errors, observable completion,
and what the system must do when it cannot answer. Preserve the selected stack.
Do not invent a budget, success threshold, consent to upload data, or model version.

## Workflow

1. **Establish relevant evidence.** Reuse a valid baseline for the affected task.
   For a quality, architecture or cost intervention, compare the existing system with a simple deterministic or
   prompt-based solution when feasible. Define expected outcomes before examining
   generated answers. Use [evaluation and data](references/evaluation-and-data.md)
   for held-out cases, judging, data leakage and regression decisions.
2. **Locate the failure.** Preserve a sanitized failing example and intermediate
   evidence. Distinguish missing information, poor retrieval, generation error,
   misunderstood instruction, tool failure, denied authority and exhausted budget.
   A larger model is a hypothesis, not the default repair.
3. **Select the intervention.** Improve context or retrieval for missing/fresh facts;
   investigate adaptation for repeatable behavioral gaps with suitable training data.
   Read [adaptation and operation](references/adaptation-and-operation.md) only when
   adaptation or serving operation is the decision. Test this
   distinction: retrieval and finetuning can be combined and neither guarantees truth.
4. **Implement one measurable change.** For document answers, read
   [retrieval](references/retrieval.md); for tool execution, read
   [agent boundaries](references/agent-boundaries.md). Keep source text as data and
   enforce access and effect permissions outside model-generated instructions.
5. **Compare on the same task distribution.** Check component outputs and final
   effects separately. Include no-answer, conflicting information, unauthorized
   data, malformed output, dependency failure and repeated attempts where relevant.
   Record repeated-trial variability and missing observations, not just averages.
6. **Operate and revisit when affected.** Version model, prompts, corpus/index, tool schema and
   evaluator together. Define rollback or forward recovery, safe telemetry,
   quality/cost regression signals and a trigger to refresh the evaluation set.

## Output and limits

For a memory/capacity or inference-cost question about a model operated by the
project, read [model resource diagnosis](references/model-resource-diagnosis.md).
Prompt drafting and hosted API use alone do not require its tensor inventory.

Complete the requested implementation or diagnosis and the relevant checks before
returning. For a bounded deterministic repair, focused regression evidence can
suffice; do not require a new model comparison, serving plan or cost inventory unless
the affected claim needs it. Report the result, observed checks and material gaps;
include comparisons and measured costs only when applicable. Separate static review,
deterministic fixture execution, actual model trials and production observations.
An unavailable model API leaves model quality unverified; do not replace it with a
mock and report model success.

Verify current official documentation for the selected model, API, tokenizer,
context/output limits, structured-output support, retention policy and pricing
before relying on them. Historical book model rankings and numerical examples are
not defaults. No provider, orchestration framework or vector store is mandatory.
Prompt drafting can optionally use `prompt`; security/performance specialists are
optional for unresolved questions. This folder supplies the complete workflow.
