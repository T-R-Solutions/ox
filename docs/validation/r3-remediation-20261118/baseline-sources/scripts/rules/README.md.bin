# Ox rules, revision 2

Original Ox rules (`opengrep/ox.yml` and `yara-x/ox.yar`) follow the root
[GPL-3.0-only license](../../LICENSE), as recorded in [NOTICE](../security/NOTICE).
The MIT license in `security/LICENSE` covers the imported automation component;
it does not license these original rules. `opengrep/rust.yml` contains indicators
adapted from Ec; the root license does not replace applicable upstream terms.
No external rule catalog is incorporated.
From the Ox root, use the public executor:
`bash scripts/toolbox.sh exec --tool opengrep --project-root "$PWD" --timeout 120 -- test --config scripts/rules/opengrep scripts/tests/rules`.
The active central version must support the chosen CLI. The original ox.yml rules have positive ruleid and negative ok
annotations in the Python/Rust fixtures; annotations are not suppressions.
Additional Rust indicator annotations and hex-encoded YARA positive/negative cases
are described in [the fixture guide](../tests/rules/README.md). Materialize the
text fixtures with their scanner-recognized extensions in a disposable directory;
the command above is a CLI template, not evidence that the stored `.txt` corpus
was selected or executed. New cases have no native detection observation yet.

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
