# Shell automation refactor

Authorized by the maintainer on 2026-11-06. Only scripts automation, its callers,
tests and affected governance records are in scope. Preserve unrelated changes.
Existing Python governance authorities outside scripts remain independent consumers.

- REQ-01: All operational code under scripts is shell (.sh); Python there only tests shell behavior. Remove repeated wrappers and centralize command definitions by responsibility.
- REQ-02: Preserve explicit scopes, offline checks, raw byte streams/exits, strict reports, private logs, snapshot identities, path boundaries and prerequisite failures. Never install tools or download databases during checks.
- REQ-03: Migrate active callers and document actual dependencies and commands; preserve predecessor observations and reexamine affected evidence.
- REQ-04: Validate shell automation using subprocess tests, syntax and available real checks; disclose unavailable scanners independently of adapter correctness.

- AC-01 → REQ-01: Recursive inventory finds no operational Python in scripts and no duplicated command wrappers; shared shell modules have distinct responsibilities.
- AC-02 → REQ-02: Behavioral tests exercise scopes, alternate cwd/spaces, offline arguments, raw streams/exits, incomplete and duplicate reports, data expiry/identity, snapshots, missing prerequisites and all retained adapters.
- AC-03 → REQ-03: Active commands resolve, preservation checks and independent-copy governance tests pass, with prior evidence preserved and affected criteria reevaluated.
- AC-04 → REQ-04: Syntax and regression suites pass; real closure results and omitted/blocked checks have exact inputs and limitations. Missing scanners do not imply a clean security audit.
