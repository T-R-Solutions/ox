# Prompt-driven task workflow — 2026-11-19

Authorized scope: implement the maintainer's mandatory per-request prompt artifact,
analysis/plan history and post-validation completion report in Ox governance.
The original request remains the authority boundary. Product behavior, profile
installation, commits, publication and full scanner execution are outside scope.

- AC-01: Every user request is transformed through the prompt skill into five named sections and appended before task execution.
- AC-02: Analysis, planning, execution, tests and validation are required proportionately; analysis and plans append without destroying history.
- AC-03: After validation, completion records state work done, unfinished work and reasons in .ai/task_completed.md, preserving task_finalizada.md.
- AC-04: Ordinary requests, read-only questions, prompt-only requests, corrections, resumption and unavailable writes preserve scope, permissions and history.
- AC-05: Independent review and validation assess the installed instructions; check-ox and the complete governance suite execute with honest results.

Acceptance is manual under sdd/evidence.md. Structural checks do not demonstrate
universal future agent obedience. Local .ai records are ignored, created on demand;
versioned instructions are sufficient to establish the workflow in another checkout.
