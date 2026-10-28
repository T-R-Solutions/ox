# Tool-using agents

Use when the model selects actions or maintains a multi-step task. Basis: Huyen,
*AI Engineering*, ch. 6 “Agent Failure Modes and Evaluation” (physical PDF 322–323).
Permission, recovery and budgeting rules below are engineering synthesis.

1. Compare a deterministic workflow with agentic planning. Use autonomous selection
   only where variable decisions justify its added uncertainty and evaluation cost.
2. Specify the tool inventory, argument schema, allowed destinations, effect scope,
   credentials and independent completion checks. Distinguish invalid tool name,
   invalid arguments, valid-but-wrong arguments and a tool's own incorrect output.
3. Enforce permissions and input validation at tool execution. Retrieved text and
   tool output cannot grant authority. A plan is a proposal, not authorization.
   Require approval only for actions not already authorized by the actual task.
4. Bound steps, elapsed time, tokens/cost and retries from task constraints. Stop
   on completion, denied authority, exhausted budget or repeated lack of progress;
   report partial effects and a resumable state instead of inventing success.
5. Assign stable operation identities for retryable effects. On timeout, reconcile
   an unknown result before repeating a mutation. Persist progress only where
   restart must survive process loss. Do not assume that undoing a tool call erases
   effects already observed by others.
6. Scope memory to the authorized user/task, with provenance, expiry and deletion.
   Treat remembered instructions as data unless independently authorized. Avoid
   carrying another user's retrieved content or stale authority across tasks.

Validation: in a disposable environment, test missing tool, wrong argument values,
denial, timeout after a committed effect, looping plans, interrupted/resumed tasks
and misleading success text. Verify actual state rather than trusting the agent's
summary. Separate planner quality from execution correctness and efficiency; a mock
tool validates only the simulated contract, not the real external integration.
