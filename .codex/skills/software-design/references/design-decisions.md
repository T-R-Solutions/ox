# Code Design Decisions

Use the relevant decision only. Page references below are one-based physical PDF pages in the repository, not printed page numbers. The books offer author recommendations; the operational choices below are context-dependent synthesis. Full research records belong in `system/research/` and are not required task context.

## Choose a boundary around knowledge

**Action and context:** When changes repeatedly cross several helpers, identify the decision or invariant that those helpers share. Put ownership of that knowledge behind a coherent interface. When a module mixes independently changing concerns, separate those concerns without forcing consumers to assemble low-level machinery.

**Evidence:** Ousterhout, *A Philosophy of Software Design*, second edition, chapters 4–5 and 9, physical pages 34–53 and 81–100; Farley, *Modern Software Engineering*, chapters 9–11, physical pages 134–179; Winters, Manshreck, and Wright, *Software Engineering at Google*, chapter 1, physical pages 31–40 and 46–50, on lifetime, scale, consumers, and total change cost.

**Reason:** Hidden implementation knowledge limits change propagation; cohesive responsibility reduces what a reader must coordinate. Interface depth is a useful question about value versus cognitive burden, not a size metric.

**Exceptions and costs:** A tiny function can express an important concept. A large module can conceal unrelated responsibilities. Splitting may add wiring, data transfer, or inconsistent ownership; joining can increase privileges or change frequency. Preserve necessary security and transactional boundaries even when combining code would be shorter.

**Validate:** Walk a real caller and a plausible change through the proposed interface. Verify contracts and invariants at their owning boundary. Compare what the reader must know before and after, without inventing a numeric complexity score.

## Reuse knowledge without speculative generality

**Action and context:** Consolidate a repeated rule when it has the same meaning, owner, and change policy. Use a modestly general interface for actual consumers. Keep similar-looking implementations separate when their semantics differ.

**Evidence:** Ousterhout chapters 6–8, physical pages 54–80; Farley chapters 12–13, physical pages 180–213.

**Reason:** Repeated knowledge can drift, but premature generalization forces unrelated callers to coordinate. KISS, YAGNI, and DRY are decision prompts, not exemptions from requirements.

**Exceptions and costs:** An established protocol or published API may require capabilities that the current caller does not use. A shared library can be appropriate across independently deployed services, with version and compatibility costs. A wrapper around every dependency adds work without necessarily hiding useful knowledge.

**Validate:** Identify the invariant and consumers explicitly. Exercise distinct consumer cases and compatibility obligations. Remove speculative flags only after checking they are not required contracts.

**Illustrative example, not executable:** Two displays both format an amount today. If one represents a legally fixed invoice and the other an estimated quote with different rounding, extracting one rounding policy would couple different business rules. Share only the representation mechanics whose meaning actually agrees.

## Preserve useful failure information

**Action and context:** Simplify errors only when the desired operation's semantics make the distinction irrelevant. Document whether an operation means “remove an existing item” or “ensure the item is absent.” Propagate or translate errors that affect authorization, data integrity, cancellation, or partial completion.

**Evidence:** Ousterhout chapter 10, physical pages 101–110; Farley chapter 12, physical pages 180–199. This synthesis limits the authors' error-hiding and retry examples by the consumer's real guarantees.

**Reason:** Eliminating an unnecessary exceptional state can simplify callers. Hiding a consequential failure creates false success and prevents recovery.

**Exceptions and costs:** A bounded retry can make transient failures transparent if the operation is safe to repeat and fits its deadline. Indefinite retry cannot establish eventual success. A boolean persistence result does not make a later in-memory mutation atomic with storage.

**Validate:** Check missing-item, permission-denied, timeout, cancellation, partial-write, and repeat-call behavior where applicable. Confirm the same externally visible outcome for a refactor; explicitly revise the contract and callers for a semantic change. Use reliability or distributed-systems expertise only if the concrete failure crosses those boundaries.

## Compose dependencies to clarify responsibility

**Action and context:** Pass a collaborator, value, or function explicitly when it makes ownership and testing clearer. Hide implementation details behind a stable operation only when consumers gain a meaningful abstraction.

**Evidence:** Farley chapters 10–11, physical pages 150–179; Ousterhout chapters 7–8, physical pages 64–80.

**Reason:** Explicit dependencies improve control and make required knowledge visible. Composition is one technique, not a mandatory architecture or proof that inheritance is wrong.

**Exceptions and costs:** A large shared context object can reduce argument propagation while introducing hidden dependencies, mutable shared state, and unclear lifetimes. Too many public seams can increase cognitive load. Changing a returned value into a listener callback changes timing, failure, and possibly ownership contracts.

**Validate:** Check construction, lifecycle, state sharing, failure propagation, and callers. Tests with fakes establish behavior against those fakes; separately verify real boundary compatibility when needed.

## Explain decisions and preserve feedback

**Action and context:** Document the stable contract and non-obvious rationale near the code. Compare a small number of viable alternatives for consequential choices. Use fast, relevant feedback while preserving checks for risks that isolated tests cannot cover.

**Evidence:** Ousterhout chapters 11–19, physical pages 111–182; Farley chapters 4–8 and 14, physical pages 71–133 and 214–233; *Software Engineering at Google*, chapters 3, 8–10, 20 and 23, physical pages 77, 87, 92, 188–233, 445–456 and 509–520.

**Reason:** Writing a contract can reveal unclear responsibility. Controlled experiments reduce speculation. Feedback speed is valuable only if the oracle and environment answer the real question.

**Exceptions and costs:** Comments that repeat syntax create maintenance noise; exhaustive design documents burden trivial changes. Ousterhout's skepticism about TDD and Farley's advocacy do not establish a universal verdict. Choose a technique that exposes the relevant risk and allows meaningful design exploration.

**Validate:** Review comments against actual behavior, check the intended failure reason of regression tests, and record unavailable checks. Do not transfer source claims about fixed function sizes, delivery times, or percentage productivity gains into acceptance criteria.

## Make dependency and compatibility costs explicit

**Action and context:** Before changing a dependency or public interface, inspect actual consumers, installed/locked versions, exported types, transitive effects and update ownership. State the inputs, outputs, errors, side effects and resource obligations consumers can rely on. Price the design against its expected lifetime and plausible change, not only its initial implementation.

**Evidence:** *Software Engineering at Google*, chapter 1, physical pages 36–39 and 46–50; chapters 8 and 10, pages 172–174 and 219–223; chapter 21, pages 461–478 and 481–485.

**Reason:** Real consumers may rely on behavior outside a written contract. Version resolution and semantic version labels do not establish behavioral compatibility. A dependency or fork creates continuing maintenance and security obligations.

**Exceptions and costs:** Incidental behavior need not be preserved forever, especially when it violates a required safety or security property. Make the intentional transition explicit. Google's One-Version assumes coordinated control; it does not justify removing lockfiles or prohibiting necessary version skew. Searching one repository may miss generated, external or stale consumers.

**Validate:** Trace representative callers and negative paths, inspect the selected artifact/version and meaningful behavior changes, and run relevant integration/regression checks using existing tooling. Record consumers that cannot be inspected. A checksum verifies expected bytes, not their safety. Verify platform-specific APIs in current official documentation for the actual version.

## Design the migration as well as the destination

**Action and context:** When a replacement cannot ship as one coherent compatible change, identify consumers, ownership, supported intermediate states and completion criteria. Use a compatibility bridge or staged migration only when it preserves the required contract. Retire the old path after verified migration and the relevant recovery window.

**Evidence:** *Software Engineering at Google*, chapter 15, physical pages 339–350; chapter 22, pages 491–504.

**Reason:** Adding a replacement does not reduce maintenance while unsupported consumers remain. A logical refactor may require several independently valid repository states; a textual replacement is not a semantic proof.

**Exceptions and costs:** Age alone is not a reason to deprecate. Parallel paths and migration tooling cost attention and can drift. A small private rename normally needs no compatibility layer. State/schema changes may prevent rollback; actual authority for a breaking change comes from the task and repository.

**Validate:** Check old/new behavior, mixed consumers where applicable, transformed artifacts and remaining uses. Confirm that new uses of the obsolete path are prevented when required. Record unresolved consumers and recovery limitations.

**Illustrative example, not executed:** Introduce an alias for an operation, migrate callers in coherent groups, verify no required consumers remain, then remove the alias. If both names cannot coexist or semantics changed, choose and document a different transition rather than claiming a behavior-preserving rename.
