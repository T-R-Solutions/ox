# Make a benchmark comparison support the decision

Use when a benchmark decision depends on variation or statistical inference.
This extends [changes and comparisons](changes-and-comparisons.md); it does not
require hypothesis testing for every measurement or cover research of human work.

## Specify the estimand and design before the result

Define metric, units, population/workload, desired direction, practical effect
margin and tolerated regressions. Distinguish superiority, equivalence within a
meaningful margin, non-inferiority and descriptive exploration. If the owner has
not established a decision margin, do not invent one or certify equivalence.

Record experimental unit, run order, warmup, cache state, pairing/assignment,
hardware/runtime/configuration, observation window and stopping rule. Samples
within one process/run may be correlated; thousands of requests are not thousands
of independent machine-level replications. Match pairing and resampling/analysis
units to the design. Include errors, timeouts and incomplete work, not only survivors.

Choose a summary and uncertainty method whose assumptions fit the observations.
A mean, median, tail quantile and throughput measure answer different questions.
Check stationarity, dependence and relevant distribution assumptions; consult a
method-specific primary source before applying its formula or software defaults.
Do not assume normal observations or a fixed repetition count universally.

## Interpret uncertainty without changing the question

Report effect size and uncertainty on the chosen scale, with raw measurements and
all planned comparisons. A p-value is not the probability a hypothesis is true.
Without the specified hypothesis, test and decision threshold, the p-value alone
does not even determine a reject/non-reject decision; do not assume alpha = 0.05.
Not rejecting a difference is not a demonstration of equivalence. To support
equivalence/non-inferiority, use the prespecified margin and an appropriate design
and method; an interval spanning both useful benefit and meaningful harm is
inconclusive. A detectable tiny change can still be practically irrelevant.

Declare confidence/significance choices, exclusions, multiple-comparison handling
and stopping before selecting the winner. Do not remove slow runs because they
disagree with the hypothesis or repeatedly rerun until a preferred result passes.
Investigate genuine environment defects and retain the original result and reason
for exclusion; distinguish planned confirmation from exploratory follow-up.

For confidence intervals, state the method and covered parameter. The
[NIST confidence-limits discussion](https://www.itl.nist.gov/div898/handbook/eda/section3/eda352.htm)
explains repeated-sampling interpretation; its one-sample mean example is not a
universal test for correlated latency or tail metrics. Do not reinterpret an
observed frequentist interval as a posterior probability of the parameter.

## Challenge and report the conclusion

Check a useful effect, a smaller-than-useful detectable effect, a broad interval
including harm, correlated repetitions, selective stopping and mismatched workloads.
Different workloads with equal scores do not establish a comparable intervention.
Keep correctness and neighboring resource/quality regressions in the decision.

Deliver the practical decision, estimate/uncertainty, design, exclusions, raw data
and limits. If evidence cannot resolve the decision, specify the additional
independent observation needed rather than claiming improvement or equivalence.
Basis: *Java Performance*, physical 47–49 (qualified), and *Systems Performance*,
benchmark design and measurement chapters; no fixed alpha or statistical package.
