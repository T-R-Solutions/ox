# Instruction implementation — 2026-11-14

Implementation report for A02/T007, A07/T014, A09/T015 and assigned A08/T013
alignment. The maintainer approved the complete correction plan; this report is
an implementer observation, not independent acceptance. Parent AC-01/03/05/10/11/12
and preservation/integration AC-14/15 remain subject to the coordinator's evidence
and independent review. No criteria, other agents' records or historical reports
were edited by this writer.

## Scope, ownership and preconditions

Read AGENTS, project, constitution, architecture, workflow/evidence, common agent
procedure, approved correction spec/plan/tasks, task-closure preference successor,
governance layout and adopted instruction reconciliation ADR. Read actual scripts
README/catalog, task-closure tests and affected preservation consumers. Inventoried
all 31 bridges/skills with exact identities and section maps; inventory is not a
claim of independently exercising all technical methods.

The nine originally assigned paths matched the coordinator's preserved preimages
before writing. The additional autonomous-verification bridge was manifested and
transferred by the coordinator before editing its one state-description phrase.
The ten edited inputs, actual identity/measurements, all 31 selection/contribution
maps and methods consulted are in [deduplication.json](deduplication.json).
New test: `tools/governance/tests/test_instruction_routes.py`.
Only this report and the deduplication record are this writer's validation outputs.

The first bounded edit attempt failed with read-only filesystem on `.codex/config.toml`
before writing any target. Reexecution of `/tmp/ox-instruction-edit.py` requested
and received explicit protected-command approval, then applied the nine manifested
paths after all hash preconditions matched. No sandbox workaround was used.

## Decisions and preserved obligations

Commit skill owns Sim/Não/no-answer/failure; AGENTS owns the complete local recipe;
scripts README/implementation own CLI semantics. The affirmative instruction now
reads those maintained sources instead of carrying legacy `full`. The actual
resolved recipe is `run --scope complete` with the selected Toolbox, shared label
and Cargo cache. The negative route and the complete-run failure paragraph retain
exact prior bytes. Applicable explicit user choice takes precedence without
another question; no answer remains no consent.

Root config identifies a controller, while `ec_triador` restricts the delegated
specialist to read-only/no tests/no children. Config, replication guide and dated
scope successor align with the adopted proportional execution contract. All 13
profile names, model/effort pairs and concurrency fields remain unchanged.
Validator profiles retain criterion/oracle/input/failure duties and reference the
common route contract rather than copying its table; explicitly selected whole
features retain every applicable gate, without global sibling approval.

Prompt/distributed-systems bridges had both Completion and authority and an
appended Shared routing policy after their conditional selection paragraph.
One authority section now carries resolvable workflow/evidence references, outcome,
artifact ownership and no-permission/no-activation duties. Selection, contributions,
technical task boundaries and optional handoffs retain exact text. The extra bridge
clarifies pending as domain lifecycle vocabulary, separate from SDD UNVERIFIED.
Thirty skill bodies are byte-identical; commit-governance only changes routing
and applicable-user-choice handling. Shared standalone safety and optional-specialist
paragraphs remain. No mandatory common skill or recursive activation was added.

## Executed checks and observations

| Method / command from root | Observation | Limit |
| --- | --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools/governance/tests -p test_instruction_routes.py -v` | 5 passed, no failures/errors/skips | Static contracts plus real plan-only CLI; does not establish agent obedience |
| AGENTS Toolbox/Cargo environment + `bash scripts/automate.sh plan --scope complete` | Exit 0; 26 unique checks, exact union of current catalog surfaces | Plan only; no Cargo/scanner execution or preparation |
| Same environment + `bash scripts/automate.sh --scope full --plan` through focused test | Exit 0; 16 legacy checks equal catalog full selection and strict subset of complete | Comparison demonstrates why substituting full loses selection; count is observed, not frozen oracle |
| `python3` + stdlib `tomllib` over config and 13 profiles; `ast.parse` new test | Exit 0; every file parsed; expected matrix/common-procedure references retained | Parsing does not prove client loading or effective model |
| `PYTHONDONTWRITEBYTECODE=1 python3 /home/rodrigo/.codex/skills/.system/skill-creator/scripts/quick_validate.py .codex/skills/commit-governance` | Exit 0: Skill is valid | Naming/frontmatter/scaffold validation only |
| Isolated temporary SKILL copy with preserved original recipe; run affirmative-route test only | One expected assertion failure, zero errors, before subprocess execution | Original defect detected by static source-routing oracle; no commit simulation |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools/governance/tests -p test_task_closure.py -v` during integration | 7 executed; 6 passed, 1 error: Missing instruction succession registry | Coordinator-owned T017 had linked predecessor but registry was not yet created; reexecute after stable integration |

Initial new preservation test reported two failures because its section extractor
included the old shared footer in Conditional project profile. The oracle was
corrected to compare the exact conditional-selection paragraph separately from
the deliberately moved shared authority text; no acceptance obligation was removed.
Final focused execution above passed all five tests.

## Static route scenario review

The following compares authored instructions with the adopted policy. These are
source-based reviews, not live team/model trials.

| Scenario | Required route observed in current instructions |
| --- | --- |
| Delegated triager | Read minimal inputs; no implementation, tests or children; return handoff |
| Root with orchestrator available | Controller triages; uses normal/high orchestration according to common route and risk |
| Root without delegation, read-only inventory | Direct source-grounded completion permitted under user/host restrictions |
| Typo/link repair or known local bug | Direct only if clear, authorized, reversible, consumers/oracle known and no material risk; existing feature gates remain |
| Schema migration, permission change or acceptance-checker change | Material risk; high orchestration plus independent review/validation |
| Required slot/context absent in material-risk work | Finish independent authorized analysis/planning; dependent execution blocked with exact resumption condition |
| Unknown scope/material uncertainty | High provisional classification; acquire indispensable facts; no small-diff exception |
| Orchestrator discovers higher risk | Stop new assignments, settle/interruption-check writers, hand continuity back to controller; no nested orchestrator or simulated in-place model switch |
| Self-review or explicit delegation restriction | No independence claim; user/host restriction prevails and dependent risky stage remains blocked |

## Measurements and documentation disposition

Values are UTF-8 bytes / whitespace-separated words, measured against preserved
preimages. Added policy clarification is intentional; no token-saving, speed, cost
or model-quality claim is made.

| Edited input | Before bytes / words | After bytes / words |
| --- | --- | --- |
| `.codex/config.toml` | 831 / 99 | 1211 / 143 |
| `.codex/agents/ec_triador.toml` | 1741 / 214 | 1868 / 232 |
| `.codex/agents/ec_validador.toml` | 1196 / 153 | 1064 / 136 |
| `.codex/agents/ec_validador_alta.toml` | 1231 / 149 | 1099 / 132 |
| `.codex/skills/commit-governance/SKILL.md` | 14218 / 2026 | 14815 / 2103 |
| `sdd/chain/prompt.md` | 2941 / 408 | 2752 / 381 |
| `sdd/chain/distributed-systems.md` | 2945 / 385 | 2756 / 358 |
| `sdd/chain/autonomous-verification-engineering.md` | 2520 / 318 | 2670 / 341 |
| `docs/development/codex-agents-replication.md` | 4258 / 548 | 5114 / 637 |
| `sdd/codex-agents.md` | 2343 / 280 | 3739 / 430 |

Reviewed and updated documentation: replication guide, dated installation scope
successor, commit skill and the three manifested bridges. Reviewed AGENTS and
scripts README as maintained command sources; no edit needed in those authorities
from this writer. Common agent procedure and parent spec/plan/tasks/evidence,
succession, README/project/templates belong to the coordinator or other assigned
writer; observations returned by message. Installation report at
`docs/validation/codex-agents-20261114/report.md` retains its original bytes.
The test module documents its static/non-model scope directly.

Remaining work: coordinator completes authenticated succession, reevaluates changed
bindings, reruns affected closure/integration checks with stable inputs and obtains
independent review/validation. No full verification, scanner execution, commit,
hook, publication, download or model-effectiveness experiment was performed here.

## Actual method consultation

- `.codex/skills/software-design/SKILL.md` — SHA-256 `4e214fd5dbf141ee437814a5c817b6924a05e8ad75cf6bc208281155204f6143`. Maintain responsibility boundaries and distinguish policy change from deduplication.
- `sdd/chain/software-design.md` — SHA-256 `e15827b753ed1faa8df77e1c1f07ce06e362535dd207f46758c7bcc8d0268794`. Map decisions to artifact ownership.
- `.codex/skills/software-testing/SKILL.md` — SHA-256 `2d2fbc0b44e19a2d4428eb98b8602fc7dc58884294a9f6902606423959f34aba`. Select source-based regressions and real plan-only boundary; preserve uncertainty.
- `sdd/chain/software-testing.md` — SHA-256 `df02545b33d6953e9e2578eea88ed216e9b204e7f480f8c1d407583ba2cbdef5`. Trace scenarios and documentation impact.
- `/home/rodrigo/.codex/skills/.system/skill-creator/SKILL.md` — SHA-256 `6656e54755638e8efcf275a472b9672eaa8a9a1b9e59dc210e275b03b59e1e66`. Narrow skill update preserving scope/metadata; quick_validate and standalone sufficiency.
