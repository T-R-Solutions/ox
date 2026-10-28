# Fitness functions tied to decisions

Use when a lasting architectural decision needs drift detection. Source: Ford/Parsons/Kua/Sadalage, Building Evolutionary Architectures, 2nd ed., ch. 2 pp. 26–28 and ch. 4 pp. 79–81 (B06 in [reading scope](portable-sources.md)).

For each relevant decision, record: requirement ID → architectural characteristic → observable outcome → method and environment → cadence → owner → failure response → revisit trigger. Use the ADR as authority for the decision, and spec for its acceptance budget. Do not restate policy in every template.

Choose an objective outcome rather than a favored implementation. A dependency rule can inspect actual imports; a recovery promise needs fault/recovery execution. Combine dimensions without hiding trade-offs: passing latency cannot compensate for denied authorization being bypassed.

Test the fitness function itself with a known violating case. A written checklist is a review aid; only a configured executed check supplies automated enforcement. Keep false positives, operating cost and legitimate exceptions visible; no arbitrary universal coupling score.

Example: a project can validate evidence links/hashes and independently test denied effects and cleanup. They do not establish architectural quality for deployed systems. CI configuration is a local-check recipe; branch protection requires separate configuration and evidence.

Compatibility checks must preserve intentional tolerance without accepting ambiguous
or unauthorized input. Ford et al., ch. 7 “Postel's Law” (physical PDF 170), motivates
loose coupling; it does not justify weakening validation or allowing extra fields to
escalate privilege. Define accepted unknown fields and round-trip behavior from the
contract, then exercise old/new consumers plus malformed and security-relevant input.

## When comparing a migration candidate in parallel

Name the authoritative execution and the result returned to the consumer. Map
reads, writes, events and external calls on both paths. Isolate, suppress or replay
candidate effects under an explicit contract; equal responses do not justify
duplicate mutations. A shadow read may still incur load or access sensitive data.

Pair observations by logical operation and relevant data revision/snapshot.
Account for time, randomness and deliberate contract changes before classifying a
difference. Use an independent oracle for desired correctness; agreement with the
old implementation alone proves neither correctness nor universal equivalence.
Set additional load/cost bounds and stop conditions from the authorized experiment,
then verify cleanup while retaining the evidence needed to interpret the result.

Check a correct response with an unauthorized duplicate effect, an incorrect
response, an intentional difference, mismatched snapshots and budget exhaustion.
Confirm only the authoritative result reaches the user and stopping the candidate
ends its owned work. This does not mandate production traffic, a library or a
fixed sampling rate. Basis: Ford et al., physical PDF 98–100 and 237; corroborated
by Adkins et al., physical 211–214 and 468. The procedure is engineering synthesis.
