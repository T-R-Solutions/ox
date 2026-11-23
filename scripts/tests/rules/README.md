# Rule detection fixtures

ox.py.txt and ox.rs.txt deliberately contain insecure examples. They are data,
never imported or executed. Copy to disposable ox.py/ox.rs files and run Opengrep
with scripts/rules/opengrep/ox.yml to test detection. Ordinary code scans retain
all executable source and exclude these non-executable data by file type.

`rust-reference.rs.txt` adds positive and negative annotations for every rule and
pattern alternative in `scripts/rules/opengrep/rust.yml`. Materialize it as
`rust-reference.rs` in a disposable directory before using Opengrep's test mode.
These are syntax-level examples, without dependencies or executable database calls.

`expectations.json` describes the added Rust and YARA cases and their expected
matches. YARA fixtures in `yara/*.hex.txt` encode the input bytes as hexadecimal:
decode each file into a separate disposable target before scanning it with
`scripts/rules/yara-x/ox.yar`. Compare the complete matched-rule set with the JSON
expectation, including the empty set for each negative. Hex storage keeps the
deliberate positive signatures out of normal repository content scans; no scanner
suppression is added. Never run these decoded files as shell or PowerShell code.

The cases are prepared inputs and expectations, not recorded scanner observations.
No Opengrep/YARA execution is established by the presence or JSON validation of
these files. Real detection tests need the installed public executor, authorized
execution, isolated materialization and captured native reports. Ordinary unittest
discovery does not execute this corpus.
