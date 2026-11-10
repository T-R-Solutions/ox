# Inspection observations and limitations

Entry command: `python3 docs/validation/persistence-freeze-20261105-r2/verify-freeze.py`.
Observed output before any edits: PASS, 2275 reviewed files, manifest SHA-256
4ad4c04f01adf0f0a3b3ce492d6dc3bfe9d414b2d1b24842ad70f1dc3ef61c02;
predecessor identity, 1388 inherited links and archive/text links passed. Its
preparation verdict remained BLOCKED. This transcribes the tool observation;
final successor integrity is a separate captured run.

A subsequent local exploratory archive read returned KeyError for
sctk-adwaita-0.10.1/src/title/mod.rs (nonexistent), causing that combined shell
invocation to return 1 after successful entry verification. Corrective inspection
read the actual src/title.rs, ab_glyph_renderer.rs and all archive members, retained
under primary/. No missing file was fabricated. No network response, acquisition
failure or source substitution occurred.

All XML module mappings were checked against every invocation in the retained
src/lib.rs; the 30 XMLs are generator inputs, not generated Rust. The scanner search
covered every retained Rust member and found only parsing and field definitions for
copyright; no emission use. This is static inspection, not an executed expansion.

Freshness impact is restricted to one feature, three exact historical bindings.
plan.md adds D-10 selection/scope/findings without changing requirements, decisions
or parameters; tasks.md adds blocked status/resumption without checking T009/T011;
converge.md records current limitations. spec.md and traceability.json are unchanged.
No source or authority document was edited. The entry file inventory provides
content preconditions; final preservation comparison detects unexpected changes.
No governance implementation changed, so prior adversarial test results are retained
as historical, not rerun or asserted current. Current structural/governance/freshness
commands and actual exit codes are in checks.json. These cannot establish license
applicability, legal compatibility, storage behavior or readiness.
