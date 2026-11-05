# Authoring plan for code-knowledge-graph-engineering

Full route because of the capability contract, boundaries and evaluation criteria. Authority: this feature's spec and the consumer's constitution for authorized effects.

## Preserved technical alternatives

The choices below are alternative methods to teach/evaluate, not approved Ox technical decisions.


| ID | Decision or risk | Proposed verification |

|---|---|---|

| D-01 | Typed node/edge model with stable IDs and a per-snapshot source of truth. | Alternative review + observed contract |

| D-02 | Separate index, algorithms and rendering; structural and network modes are views of the same graph. | Rejected scenarios and comparison of options |

| R-01 | False relationships that lead agents to incorrect changes. | Relevant adversarial test |

| R-02 | Combinatorial explosion when querying/drawing large graphs. | Controlled falsification of the result |



D-03 [REQ-04]: create an entry, three specialized references and dedicated cases instead of duplicating a general skill; maintenance cost is justified by the specialized capability and local spec scenarios; the comparison is historical origin only. R-03 [REQ-04]: ambiguous selection or superficial text; check with positive, negative and failure cases. Reevaluate after observed use or source changes.

## Method selection and dependencies

Primary authoring method actually consulted: the environment's skill-creator (version not declared; consultation copy at docs/validation/adoption-baseline/skill-creator.md). No local bridge exists for this method. This new skill did not exist at initial selection and is not claimed to have been consulted during its own authoring.

The bridge sdd/chain/code-knowledge-graph-engineering.md, bridge_version 1, and entry .codex/skills/code-knowledge-graph-engineering/SKILL.md are available for consumers and later evaluation; existence does not prove consultation. Proposed conditional supporting skill: `code-context-engineering` — Can the edge's origin be verified in the indexed code snapshot? No automatic consultation.

Authoring dependencies: protocol → runtime → verification; workspace/Iced complete the foundation; context precedes graph; output and usage depend on event vocabulary. These are not installation dependencies.

## Proposed technical activities to teach and resume

> - [ ] P001 [applicable REQ, AC, D, R]: Define the schema and evidence classes per relationship type.
> - [ ] P002 [applicable REQ, AC, D, R]: Create the graph and query algorithms with limits and cancellation.
> - [ ] P003 [applicable REQ, AC, D, R]: Test incremental invalidation and distinguish inferences.
> - [ ] P004 [applicable REQ, AC, D, R]: Validate navigation in a large corpus and rendering cost.

P001..P004 preserve the intent of proposed tasks; they do not claim product implementation. Local authoring execution is in tasks.md. Real tests depend on a consumer and authorized scope.

## Subsequent consultation during evaluation

On 2026-10-26 an internal subagent consulted `.codex/skills/code-knowledge-graph-engineering/SKILL.md` version 1.0.0 and technical references to answer an adversarial scenario. Available bridge: bridge_version 1; direct evaluation without claiming bridge consultation. Primary: this now-existing skill; supporting skills were unnecessary. The description catalog was used for selection before reading. Questions, raw response, consulted paths and limitations are in `docs/validation/agent-evals/`; the executor's judgment is separate in review.md. This is neither consultation during authoring nor product integration.
