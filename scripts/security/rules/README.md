# Ox rules, revision 2

First-party MIT rules (see ../LICENSE); no external rule pack incorporated.
From the Ox root, use the public executor:
`bash scripts/toolbox.sh exec --tool opengrep --project-root "$PWD" --timeout 120 -- test --config scripts/security/rules scripts/tests/rules`.
The active central version must support the chosen CLI. Each rule has positive ruleid and negative ok
annotations in the Python/Rust fixtures; annotations are not suppressions.

| Rule | Rationale and limitation |
| --- | --- |
| ox.python.dynamic-eval | Dynamic execution requires input review; does not establish attacker control or track wrappers. |
| ox.python.shell-true | Shell interpretation in subprocess/os requires provenance review; trusted literals also match. Arrays with shell=False do not match. |
| ox.python.unsafe-deserialization | Pickle/default YAML can execute code. SafeLoader/CSafeLoader positional/keyword arguments are exempt. Custom safe subclasses are not inferred. |
| ox.python.tls-verification-disabled | Requests/SSL bypass removes peer authentication; arbitrary client configuration is not covered. |
| ox.rust.unsafe-block | Explicit unsafe blocks violate POL-01; macros/generated code require compiler enforcement. |
| ox.rust.unsafe-function | Unsafe function declarations violate POL-01; coverage depends on parser syntax. |
| ox.rust.unsafe-impl | Unsafe trait implementations violate POL-01; not every unsafe construct is enumerated. |
| ox.rust.shell-interpreter | INFO review signal for literal sh/bash constructors, not proof of vulnerability. Dynamic/absolute paths are not covered. |
| ox.rust.tls-verification-disabled | Explicit builder bypass methods remove authentication; this is not type resolution. |

Compiler forbid(unsafe_code) remains the primary comprehensive control. Paths,
permissions, concurrent substitutions and trust propagation need specific tests.
Zero findings is not proof of security. The adapter uses 1.33.1's experimental
ignore-file bypass and independently checks all selected paths in the report.
Unavailable flags fail closed. Positive fixtures remain scanned and triaged,
without suppressions to obtain a clean result.
