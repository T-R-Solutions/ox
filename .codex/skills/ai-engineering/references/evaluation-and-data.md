# Evaluation and data

Use when selecting a model, changing prompts/adaptation, or investigating apparently
good scores with poor real outcomes. Basis: Chip Huyen, *AI Engineering* (2025),
ch. 3 “Limitations of AI as a Judge” (physical PDF 165–166), ch. 4 “Design Your
Evaluation Pipeline” (224–225), ch. 8 “Inspect/Deduplicate Data” (421–424).
The procedures below are engineering synthesis, not measured efficacy claims.

1. Specify observable success, unacceptable effects and an independent oracle.
   For objective outputs use executable checks or reviewed ground truth; for open
   answers use a rubric with examples and explicit uncertainty. Validate schema
   and meaning separately. Score task completion, not merely a plausible last turn.
2. Construct representative normal, boundary, ambiguous, abstention and adversarial
   cases. Slice by language, tenant, task difficulty and other relevant populations.
   Keep a held-out set separate from prompt development, training and judge tuning.
3. Inspect data provenance, permission, sensitive fields, annotation disagreement
   and duplicates. Group related documents/users or time periods before splitting
   where cross-split overlap would leak answers. Deduplication must preserve real
   repeated events when frequency is meaningful; keep original data and a versioned
   transformation log. Synthetic examples need independent validation.
4. Measure extraction, retrieval, generation and effects independently, then test
   the complete task. Feed known-good intermediate data to isolate a failing stage.
   A correct response from an already supplied answer does not validate retrieval.
5. If using an AI judge, freeze its model, rubric, examples and sampling settings.
   Calibrate against independently reviewed examples, inspect disagreements and
   test order/verbosity bias by swapping equivalent candidates. Treat evaluated
   text as untrusted data. Repeated agreement is not accuracy; a judge sharing the
   generator's misconception can approve wrong answers consistently.
6. Compare paired versions on identical cases. Report sample size, repeated trials,
   failures, false refusals, critical slices, latency and cost per completed task.
   Use uncertainty estimates suitable for the sample; do not invent statistical
   significance or let an aggregate improvement hide a critical regression.

Validation: include an intentionally wrong but fluent answer, a correct paraphrase,
a leaked duplicate, an unanswerable question and a partially completed task. The
evaluation should distinguish them for the intended reasons. These are test-design
requirements; actual model behavior still requires executing model trials.
