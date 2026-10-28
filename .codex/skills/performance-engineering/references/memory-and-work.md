# Retention, allocation and adversarial work

Use when allocation pressure or input growth is the unresolved mechanism. Sources: GC Handbook ch. 1 §§1.3–1.6 pp. 5–13 (B02), Introduction to Algorithms 4th ed. §2.2 pp. 25–31 (B09); [reading record](portable-sources.md). Supplements existing measurement-and-diagnosis; does not prescribe a collector.

1. Record input dimensions, algorithmic operations, live/retained objects, allocation rate, heap occupancy, RSS and pause distribution separately. Reachable objects can be logically dead; retained cache data can be intentional. RSS alone cannot classify either.
2. Capture a retaining path or ownership lifecycle for suspected leaks. Compare after quiescence at equivalent workload and heap settings; distinguish allocator reserve, fragmentation, floating garbage and application retention.
3. Measure application progress and throughput alongside pauses. A smaller maximum pause may cost CPU or memory. Compare startup and steady state separately; record warmup, repetitions and distributions without imposing a universal threshold.
4. State the complexity model and relevant dimensions (bytes/bits/items/edges), then select normal and adverse inputs. Identify the source of an expected bound: a distribution over inputs, or internal random choices for each fixed input. For randomized algorithms, state relevant independence and adversary assumptions; a fixed seed alone does not establish the bound. An average-case claim for a deterministic algorithm needs an input model. Amortized analysis bounds total cost over an operation sequence and does not inherently require randomness or an input distribution. None of these bounds is a per-request deadline or a measured elapsed time.
5. Put an explicit work/admission bound at untrusted input boundaries if the spec requires it. Measure actual completion and recovery, not only request rejection. Algorithmic complexity is explanatory evidence, not measured elapsed time; caches and runtime costs still matter.

Precision revision, 2026-10-20: Cormen et al., fourth edition, chapter 5
(physical 156–158), chapter 7 (204–226) and chapter 16 (470–497), distinguish
expectation over random choices from input averages and amortized analysis.
The source IDs in the older reading record retain their original namespace.

Validation: independent result oracle plus operation counts or profiles on increasing sizes; retained-owner evidence after cleanup; raw measurements and units. Current JVM/BEAM collector flags require local version documentation or newly authorized official sources. No GC tuning or performance gain was measured in this delivery.

## Generational assumptions and benchmark artifacts

When GC is the suspected mechanism, distinguish allocation rate, survivor/promotion
volume, retained roots, collector work and user-visible pauses. Object lifetimes
measured in allocated bytes and elapsed time answer different questions; a global
allocation count mixes threads. Compare startup, steady state and workload phases.
Do not assume all applications satisfy the same survival distribution or transplant
a historical nursery size. A smaller nursery may collect faster yet promote more
data and increase later work. Source: Jones/Hosking/Moss, ch. 9 §§9.2–9.4, physical
PDF 144–145; qualitative interpretation, not a collector-specific tuning recipe.

For JVM microbenchmarks, verify that outputs are consumed and relevant work survives
optimization; separate warmup/JIT behavior from steady-state measurement. Prefer
existing benchmark tooling with demonstrated controls. A volatile write added to
prevent elimination can itself change measured cost. Compare with representative
application behavior before attributing a user-visible gain. Source: Scott Oaks,
*Java Performance*, ch. 2, physical PDF 31–32. This does not prescribe current JVM
flags, fixed object sizes, a specific JIT strategy or a universal warmup duration.

Validation: retained-owner evidence and collection/promotion observations alongside
throughput/latency; small and large inputs with independent result checks; document
compiler/runtime, collector, heap limits and the work actually timed.
