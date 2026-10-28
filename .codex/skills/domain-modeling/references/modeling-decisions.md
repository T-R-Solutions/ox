# Modeling decisions

Read when deciding whether domain concepts or boundaries need richer modeling. Page references below are inclusive, one-based physical PDF pages in `docs/system/Domain-Driven_Design.pdf` (Learning Domain-Driven Design, first edition, October 2021), not printed pagination. These are contextual engineering recommendations derived from the indicated author guidance; they are not a language or framework specification.

## Start with meaning and purpose

**Action and context:** When requirements are ambiguous, write a few concrete scenarios using the domain's terms, including a rejected action and a boundary condition. Identify the person or contract that can confirm each rule.

**Evidence and rationale:** Chapters 2-3, pp56-108, show why terminology and purpose-specific models reduce misunderstanding. A glossary alone misses behavior and invariants.

**Exceptions and costs:** A short, obvious correction does not need a workshop, formal glossary, or new domain layer. Domain conversations take time; focus on uncertainty that changes implementation or acceptance.

**Validation:** Trace each modeled transition to a requirement or confirmed example. Mark hypotheses explicitly. Use tests as checks of agreed meaning, not substitutes for agreeing on meaning.

Example: “An approved expense may be reimbursed once” needs clarification about partial reimbursements, reversal, currency, and competing requests. A table named `expenses` answers none of those questions.

## Select boundaries from invariants

**Action and context:** For a mutable business operation, list the data needed to decide legality and the writes that must succeed together. Encapsulate those rules at a boundary that all writers respect, including imports, administrative tools, jobs, and direct persistence paths.

**Evidence and rationale:** Chapter 6, pp155-189, treats an aggregate as a consistency boundary; chapter 11, pp306-339, revisits boundaries as knowledge and requirements change.

**Exceptions and costs:** The book's one-aggregate-per-transaction rule is a modeling heuristic. A legitimate atomic multi-record transaction must not be replaced with eventual consistency just to satisfy that heuristic. Reconsider the model, transaction API, or documented exception. Large boundaries increase contention and loading costs; overly small boundaries move complexity into coordination.

**Validation:** Test a race that could break the invariant, a failure between writes, and a stale update. Check affected-row counts or equivalent concurrency outcomes. Verify that alternative write paths enforce the same rule.

Illustrative reservation example: if capacity is one and two callers both observe zero reservations, independently inserting two rows is invalid. An in-memory `available()` check is insufficient. Choose an atomic conditional allocation, database constraint, suitable locking/isolation, or another mechanism whose guarantee covers the actual invariant; verify the selected database/version separately.

## Introduce richer values only when they earn their cost

**Action and context:** Use a value representation for concepts whose equality is by value and whose units, normalization, or operations need protection. Preserve identity separately for entities whose attributes change over time.

**Evidence and rationale:** Chapter 6, pp160-168, demonstrates value equality, immutability, units, and domain behavior. The benefit is preventing invalid combinations and duplicated reasoning, not increasing class count.

**Exceptions and costs:** A one-use primitive with clear meaning may be enough. Value types add conversions, serialization decisions, and maintenance. Immutability alone does not guarantee thread safety of referenced mutable objects or external operations.

**Validation:** Check equality and hashing where applicable, invalid construction, boundary units/precision, serialization round trips, and unchanged original values after transformations. Use the project's language conventions rather than transplanting C# class scaffolding.

Illustrative before/after: replace separately maintained `amount` and `currency` arguments with a money value only when operations need consistent currency/rounding rules. Define those rules before creating the type; the wrapper itself does not solve decimal precision.

## Match implementation complexity to business logic

**Action and context:** Retain procedures or active-record-style code for straightforward workflows; add a richer domain model when intertwined transitions, invariants, and change patterns justify it.

**Evidence and rationale:** Chapters 5-6, pp136-189; chapter 10, pp288-305; Appendix A, pp497-525. The marketing hub case demonstrates that commercial importance can coexist with simple software logic.

**Exceptions and costs:** Do not classify every core business capability as algorithmically complex. A domain model has learning and indirection costs; simple scripts become risky when the same evolving rule is scattered across paths.

**Validation:** Compare the implementation against the same acceptance scenarios, inspect rule duplication, and verify that a local rule change has a comprehensible impact. No pattern count or test coverage percentage proves better modeling.

## Optional collaborative discovery

**Action and context:** Use EventStorming when knowledge is fragmented across stakeholders or a complex process contains unknown branches: walk through events, actors, commands, policies, decision data, failures, and candidate boundaries.

**Evidence and rationale:** Chapter 12, pp340-367, prioritizes shared knowledge over the diagram itself.

**Exceptions and costs:** Skip the ceremony for obvious processes. Adapt remote participation, timing, and materials to accessibility and availability. A workshop's event diagram does not mandate an event-sourced implementation.

**Validation:** Record unresolved contradictions, check negative paths, and have the relevant stakeholders review the resulting behavior. Candidate contexts and aggregates remain hypotheses until implementation and change scenarios support them.
