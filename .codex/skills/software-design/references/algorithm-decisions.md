# Algorithm and data-structure decisions

Use when implementing nontrivial search, ordering, graph traversal or optimization,
or when input growth makes a local design unsuitable. Basis: Cormen et al.,
*Introduction to Algorithms*, 4th ed., §§2.1, 14.3, 15.2, 22.3 (physical PDF
40–42, 404, 448, 642). Adapted decision rules, not copied implementations.

1. Specify the result and preconditions: input dimensions, ordering/equality,
   duplicates, mutation, numeric range, feasible versus optimal result and memory
   limits. Separate n items from n bits, vertices/edges or output size. Prefer a
   maintained library operation when its contract fits.
2. Select a representation from required operations. Hash lookup does not supply
   ordering; a heap supplies an extremum rather than a globally sorted sequence.
   Price construction, updates, queries and retained memory across the lifecycle.
   Verify library complexity contracts rather than assuming average-case costs.
3. For a custom algorithm, state an invariant, why initialization establishes it,
   why each step preserves it, and why termination yields the postcondition. Add a
   decreasing measure for termination when it is not obvious. Preserve associated
   records and required stability when sorting; sorted keys alone are insufficient.
4. For dynamic programming, define state, recurrence, base cases, dependency order
   and reconstruction of a solution. Establish optimal substructure and overlapping
   subproblems; include all state needed by future choices. Account for table size
   and recursion depth. Memoization is not free memory.
5. For a greedy choice, justify that some optimum contains the choice (for example
   through an exchange argument). Without that argument, call it a heuristic and
   check counterexamples. A locally attractive choice need not be globally optimal.
6. For paths, verify graph and weight assumptions before selecting an algorithm.
   Dijkstra's guarantee requires nonnegative weights. Account for unreachable
   vertices, cycles, overflow and updates. Do not select by algorithm name alone.
7. Distinguish worst-case, expected and amortized bounds. Identify whether an
   expectation is over input distribution or internal randomness for each fixed
   input, including relevant independence/adversary assumptions. State the
   operation sequence covered by an amortized bound; amortization need not assume
   randomness or an input distribution. Neither bound is a per-request deadline.
   Exponential search can fit bounded small inputs; label cutoffs and approximation/
   optimality limits instead of promising arbitrary scalability.

Validation: compare against independently enumerated small cases when feasible;
test empty/singleton, duplicates, ties, adverse order, disconnected graphs and
numeric limits as applicable. Check properties of the full result. Measure
representative sizes and operation counts separately from elapsed time. A finite
test does not prove the general bound; an asymptotic proof does not measure runtime.
Pseudocode may omit engineering error handling.
