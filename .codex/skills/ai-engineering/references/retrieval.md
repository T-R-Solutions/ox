# Retrieval and grounded answers

Use for answers depending on external/private/changing information. Basis: Huyen,
*AI Engineering*, ch. 6 “RAG Architecture” and retrieval evaluation (physical PDF
278–280, 289–290); ch. 7 “Finetuning and RAG” (340–341). Synthesis, not a mandate
for embeddings or a claim that retrieval eliminates hallucination.

1. Identify authoritative sources, freshness and deletion requirements, document
   identity/version, tenant and access policy. Verify extraction on representative
   content before indexing; record omitted tables/images and broken text.
2. Compare direct context, lexical retrieval, semantic retrieval or a hybrid using
   the actual query set. Exact identifiers often benefit from lexical matching;
   paraphrases may benefit from semantic matching. Measure rather than assume
   superiority. Include index build/update cost as well as query latency.
3. Choose chunks around answer-bearing units and retain source locations. Check
   boundary-spanning answers, duplicated chunks, metadata filtering and context
   limits. Tune chunking, top-k or reranking against retrieval evidence; more
   context can introduce irrelevant or conflicting material.
4. Enforce authorization before retrieved content reaches the model. Apply policy
   to retrieval, caches, conversation memory and returned citations. A filter in
   the prompt cannot repair cross-tenant retrieval. Version indexes with embedding
   model/preprocessing changes; rehearse reindex/cutover and deletion propagation.
5. Evaluate recall of required evidence at the chosen k and ranking when order
   matters. Then assess answer correctness, support for each material claim,
   citation accuracy, freshness and appropriate abstention. Good retrieval alone
   does not establish a faithful answer. Missing evidence is not proof of absence.
6. For conflicting or insufficient sources, expose the conflict or abstain according
   to the application contract. Do not synthesize invented facts to fill the gap.

Validation: test a known answer, exact identifier, paraphrase, missing document,
stale version, conflicting passage, revoked access and a malicious instruction
inside a retrieved document. Confirm prohibited content never enters the model
request or cache result. Use known relevant-document labels separately from answer
labels. Report coverage gaps and costs; do not prescribe a universal k or chunk size.
