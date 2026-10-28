# Diagnose resources for a model you operate

Use when a self-operated serving or adaptation workload has a memory/cost/latency
question. Hosted API use or prompt drafting alone does not need this inventory.
Supplement [adaptation and operation](adaptation-and-operation.md) while preserving
the application's quality, data rights and tool-effect constraints.

## Identify the actual configuration

Record model/base revision, architecture, resident versus active parameters,
tokenizer, adapter/base compatibility, precision/quantization, engine/runtime,
hardware/sharding and workload. Include prompt/output lengths, batch, concurrent
sequences, cache type/prefix sharing and maximum observed phase. Do not replace
missing configuration with the book's model or a provider's historical ranking.

Inventory peak-resident components with units and lifetime: weights, adapters,
key/value cache, activations, gradients, optimizer/master states, temporary workspace,
communication buffers, allocator reserve and operational headroom. Mark estimated,
measured and omitted values. Some components are not present in inference; some
are sharded or replicated differently. Parameter count alone is not total memory.

For a simple dense decoder with uniform cache layout, estimate cache elements as
2 × layers × concurrent sequences × cached tokens × KV heads × head dimension;
multiply by bytes per stored element. This counts keys and values, not query heads.
Treat it as a stated layout model: GQA/MQA, variable lengths, sliding windows,
quantized/offloaded/paged caches and shared prefixes change actual residency.
Verify dimensions and allocation against the engine. The official
[Transformers cache guidance](https://huggingface.co/docs/transformers/main/en/kv_cache)
illustrates strategy trade-offs, not a mandatory implementation or a portable peak.

## Distinguish capacity, traffic and useful work

Estimate bytes and time separately. Seven billion resident parameters at two
bytes each are about 14 GB decimal of weights alone. If every emitted token really
required reading those weights once, 100 tokens/s would imply 1.4 TB/s decimal of
weight traffic, not 700 GB/s. That assumption can fail under batching, caching,
sharding or expert selection; it is not a prediction of hardware bandwidth.

For bandwidth/compute utilization or roofline claims, define numerator, denominator,
batching and measurement boundary. GPU busy time is not achieved FLOPS; parameter
traffic alone omits cache/activation/communication work. Locate capacity, compute,
memory traffic, queueing, communication or host stalls with actual engine counters.

## Compare a bounded intervention

Compare equivalent tasks under short/long inputs, warm/cold state, concurrency
and peak conditions relevant to the failure. Test authorized adapter selection and
base/tokenizer compatibility; sharing a base does not isolate tenant data or caches.
Recheck critical quality and output distributions for quantization, kernels or
speculative decoding rather than trusting throughput or a matching output format.
Use the selected method's acceptance/correction contract, not an invented shortcut.

Measure arrival to visible output and completed usable result, including queueing,
retrieval and tools. Faster decode can coexist with a worse journey. Deliver an
estimated-versus-observed inventory, diagnosis, comparison and residual limits;
do not claim a production gain from an isolated arithmetic model or microbenchmark.
No paid job, download or private-data upload is authorized by this procedure.

Basis: Huyen, *AI Engineering*, chapter 7 physical 342–370 and chapter 9 435–472.
Verify current model/engine contracts in the destination project; numerical
illustrations above state their assumptions rather than prescribing hardware.
