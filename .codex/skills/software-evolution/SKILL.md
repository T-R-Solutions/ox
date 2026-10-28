---
name: software-evolution
description: Change existing systems through characterized behavior, compatibility, mixed-version transitions, and incremental modernization. Use for consequential replacement, data/contract migration, or coexistence; skip cosmetic changes and local behavior-preserving refactors without a transition problem.
---

# Software Evolution

Own the transition between functioning versions, including temporary states and
retirement. Discover current code, implicit consumers, contracts, persisted formats,
jobs, dependencies, incidents, deployment order, supported versions and recovery
requirements. Modernization does not imply microservices or cloud.

## Procedure

1. Characterize actual behavior at the affected boundary before changing it. Capture
   representative normal, irregular historical, failure and side-effect cases.
   Distinguish required compatibility from accidental behavior and explicitly approved
   fixes; do not preserve an unsafe behavior silently or change it without disclosure.
2. Read [transition decisions](references/transition-decisions.md). Compare retaining,
   local refactoring, incremental replacement and rewrite using concrete constraints,
   evidence, ownership, migration cost and verification burden.
3. Enumerate API/event/format/data/dependency contracts and reachable old/new version
   pairs, including delayed messages and offline clients. Select an implementation
   seam and order that keeps required operations valid throughout the transition.
4. If state moves, read [state migration](references/state-migration.md). Establish
   authority, resumable movement, concurrency protection and reconciliation before
   making new state authoritative. Define the last safe return point.
5. Implement an observable slice, test coexistence and interrupted recovery, then
   expand only with criterion-based evidence. Shadow execution must not duplicate
   production effects. Do not confuse equal response shapes with equivalent behavior.
6. Cut over with explicit signals and stop/return/roll-forward conditions. Remove
   obsolete routes, temporary abstractions, flags and storage only after consumer,
   data and recovery evidence supports removal; assign ownership and revisit trigger.

## Result and boundaries

Deliver the implemented slice, compatibility matrix, transition/recovery state,
checks actually run and criteria for retirement or the exact remaining dependency.
A green final-state suite cannot prove safe intermediate states. Keep local changes
proportional. Architecture selects structural boundaries; design owns local interfaces;
database/delivery specialists may resolve concrete product or rollout questions when
available. No other skill or SDD is needed to perform this workflow.
