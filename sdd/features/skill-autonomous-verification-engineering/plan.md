# Authoring plan for autonomous-verification-engineering

Full route because of the capability contract, boundaries and evaluation criteria. Authority: this feature's spec and the consumer's constitution for authorized effects.

## Preserved technical alternatives

The choices below are alternative methods to teach/evaluate, not approved Ox technical decisions.


| ID | Decision or risk | Proposed verification |

|---|---|---|

| D-01 | Separate states: pending, approved, rejected, inconclusive, justified not applicable. | Alternative review + observed contract |

| D-02 | Immutable evidence per observation and content binding, recording origin and hash. | Rejected scenarios and comparison of options |

| R-01 | False approval through self-verification or a test that accepts a defective implementation. | Relevant adversarial test |

| R-02 | Confusing “compiled,” “tests passed” and “meets all requirements.” | Controlled falsification of the result |



D-03 [REQ-04]: create an entry, three specialized references and dedicated cases instead of duplicating a general skill; maintenance cost is justified by the specialized capability and local spec scenarios; the comparison is historical origin only. R-03 [REQ-04]: ambiguous selection or superficial text; check with positive, negative and failure cases. Reevaluate after observed use or source changes.

## Method selection and dependencies

Primary authoring method actually consulted: the environment's skill-creator (version not declared; consultation copy at docs/validation/adoption-baseline/skill-creator.md). No local bridge exists for this method. This new skill did not exist at initial selection and is not claimed to have been consulted during its own authoring.

The bridge sdd/chain/autonomous-verification-engineering.md, bridge_version 1, and entry .codex/skills/autonomous-verification-engineering/SKILL.md are available for consumers and later evaluation; existence does not prove consultation. Proposed conditional supporting skill: `software-testing` — Does the chosen oracle actually fail when a representative defect is introduced? No automatic consultation.

Authoring dependencies: protocol → runtime → verification; workspace/Iced complete the foundation; context precedes graph; output and usage depend on event vocabulary. These are not installation dependencies.

## Proposed technical activities to teach and resume

> - [ ] P001 [applicable REQ, AC, D, R]: Define authorities, criteria, the verdict model and rejected states.
> - [ ] P002 [applicable REQ, AC, D, R]: Design bindings among requirements, checks, inputs and immutable evidence.
> - [ ] P003 [applicable REQ, AC, D, R]: Create fixtures with false tests, failures, skips and post-validation changes.
> - [ ] P004 [applicable REQ, AC, D, R]: Run adversarial verification and record coverage and authorization limits.

P001..P004 preserve the intent of proposed tasks; they do not claim product implementation. Local authoring execution is in tasks.md. Real tests depend on a consumer and authorized scope.

## Subsequent consultation during evaluation

On 2026-10-26 an internal subagent consulted `.codex/skills/autonomous-verification-engineering/SKILL.md` version 1.0.0 and technical references to answer an adversarial scenario. Available bridge: bridge_version 1; direct evaluation without claiming bridge consultation. Primary: this now-existing skill; supporting skills were unnecessary. The description catalog was used for selection before reading. Questions, raw response, consulted paths and limitations are in `docs/validation/agent-evals/`; the executor's judgment is separate in review.md. This is neither consultation during authoring nor product integration.
