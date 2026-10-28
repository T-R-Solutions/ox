# Adaptation and operation

Use for model choice, finetuning decisions or inference cost/latency changes. Basis:
Huyen, *AI Engineering*, ch. 7 (physical PDF 335–341), ch. 9 “Inference Performance
Metrics” (436–437), ch. 10 caching and feedback limits (484, 514). Author heuristics
are qualified below; no historical provider pricing or model ranking is adopted.

## Choose from a diagnosed failure

For a self-operated model's memory or execution bottleneck, use
[model resource diagnosis](model-resource-diagnosis.md) for the actual tensor/cache
inventory and capacity-versus-bandwidth hypotheses, without prescribing an engine.

Try an adequate prompt/context baseline first. Missing changing knowledge suggests
retrieval; persistent formatting/style/task behavior may justify finetuning only
with suitable examples, data rights and evaluation. This is a hypothesis to compare,
not a partition of all possible failures. Finetuning can regress other capabilities;
retrieval can return irrelevant facts. They can be combined.

For a finetuning experiment, freeze the base version, dataset/splits, training recipe
and evaluation. Estimate training and serving resource costs using the actual
precision, optimizer, sequence lengths and batching; parameter count alone omits
activations and other memory. Run a bounded trial before a large job. Compare to
the base model and simpler alternatives on held-out tasks and unaffected capabilities.
Keep checkpoint provenance and a way to return to the prior model. Do not launch
paid training or upload private data without applicable authorization.

## Measure what users receive

Measure request arrival to first **visible** output and to completed usable result;
record queueing, retrieval, hidden intermediate steps, tool execution and generation
separately. State input/output lengths, cache state, concurrency, errors and token
accounting. Faster first output is not faster completion. For N visible tokens,
there are N−1 inter-token intervals after the first; do not blindly multiply an
interval average by N or mix server timing with user-observed timing.

Compare batching, caching, routing, smaller models or quantization only after
locating cost. Batching may raise waiting time; quantization/routing require quality
regression tests. Response cache keys must cover tenant/access scope, relevant
context version, model and configuration. Define freshness/invalidation and test
revocation; semantic similarity is not sufficient permission to reuse an answer.

## Close the feedback loop

Version the complete serving configuration. Monitor completion, failure classes,
critical quality slices, latency and cost with redacted telemetry. Keep feedback
collection optional where the product permits; lack of complaints is not success.
Ratings and user edits have selection/leniency bias and can be poisoned. Review
them before adding training/evaluation examples; keep a separate stable regression
set. A canary or model fallback must preserve data and tool permissions.

Validation: compare the same workload with warm/cold caches, authorized/denied
users, short/long outputs, failed/unfinished tasks and the previous model. Report
measured gains only for the executed environment; no universal token-speed target.
