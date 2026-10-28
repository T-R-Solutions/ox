# Diagnose collection against application service

Use when GC is a plausible cause of an observed latency, throughput or memory
problem. Supplement [memory and work](memory-and-work.md); do not choose a collector
or enlarge the heap merely because collection appears in a profile.

## Establish the timeline and usable memory

Record runtime/collector/version, workload and phase, process/container limits,
heap and native budget, allocation rate, live/retained population, promotion,
collector CPU, pauses and cycle boundaries. Identify missing observations and the
application objective. Distinguish collector events from application allocation,
blocking, runnable delay and other stop-the-world work using that runtime's semantics.

Place arrivals, completed work, queueing and collection on a common elapsed-time
basis. A concurrent cycle can last much longer than its stop-the-world phases.
Measure progress in windows relevant to the workload, not only maximum pause or
whole-run averages. Equal maximum pauses can hide very different pause clustering
and useful-service gaps. Startup and steady-state populations need not behave alike.

Inventory usable reserve as well as aggregate free bytes. Some collectors need
space to move survivors or satisfy large contiguous allocations; capacity reserved
for another purpose may be unavailable. Check collector-specific meaning before
calling this fragmentation, an evacuation failure or a leak. High RSS alone does
not distinguish live application data, retained allocator pages and collector reserve.

## Test a discriminating hypothesis

| Observation | Investigate before changing configuration |
| --- | --- |
| Small pauses but poor service during a long concurrent cycle | Collector/application CPU competition, allocation work, mutator assists and available headroom under the actual collector |
| Similar maximum pause but worse tail latency | Pause clustering, queue growth and the service window containing them |
| Allocation failure with aggregate free bytes | Usable reserve, region/contiguity requirements, size classes and remaining process/native budget |
| Rising occupancy after comparable quiescence | Live owners/retaining paths versus temporary, floating or legitimately cached data |

Choose a bounded trace or controlled change that separates alternatives. Preserve
workload, correctness, equivalent warmup/cache state, resource limits and units.
Record observation overhead and compare application completions, tails and total
CPU/memory cost. More reserve, less allocation or a different workload shape can
be preferable to collector tuning, depending on evidence.

Use the selected runtime's current event and configuration documentation before
prescribing commands. [Oracle's G1 description](https://docs.oracle.com/en/java/javase/25/gctuning/garbage-first-g1-garbage-collector1.html)
is one collector-specific example, not authority for BEAM, another collector or all
JDK versions. No pause target is a hard deadline guarantee by itself.

Deliver a supported/rejected hypothesis, the observations distinguishing it,
measured comparison or smallest missing collection, and remaining uncertainties.
Basis: *The Garbage Collection Handbook*, chapters 1, 4, 7, 10, 11 and 19;
*Java Performance* and *Systems Performance* provide workload/measurement context.
