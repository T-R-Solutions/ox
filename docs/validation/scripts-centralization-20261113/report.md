# Ox script configuration refactoring — 2026-11-13

The explicit maintainer request is implemented as a full-route configuration migration using Ec as a read-only reference. Existing unrelated work was preserved; no commit or publication occurred.

## Reference disposition

The complete Ec scripts file inventory (including vendored rules and attribution) is in ec-inputs.json. automation.json, all native configurations, public entries and stack responsibilities were inspected. Inventory hashes identify bytes; they do not claim an independent audit of every third-party signature.

| Ec surface | Ox disposition |
| --- | --- |
| Declarative automation/catalog selection | config/automation.json owns scopes, optional checks, scanner metadata, policy locations, timeouts, database age, source selection and local paths |
| config/native per tool | Migrated every existing Ox native policy; migration.json records each old/new location |
| rules/opengrep, rules/yara-x | Moved Ox rules, preserving contents and attribution; Ec third-party catalogs are not copied as a configuration-only change |
| Stack execution/inputs/reports | Existing Ox shell modules retained as consumers; report/exit/snapshot contracts preserved |
| Toolbox discovery/environment | Explicit TOOLBOX_BIN then PATH and caller-controlled SELinux retained, as required by Ox authorities |
| Rust/Cargo | Existing virtual workspace and offline/locked commands retained; Ec license and advisory decisions do not replace Ox policies |
| Frontend, PostgreSQL, HTTP, browser journeys | Not applicable to the Rust/Iced desktop; no services or credentials imported |
| CodeQL, expanded third-party SAST/YARA and browser tool adapters | Ec-only capabilities not imported; this migration does not claim new scanner coverage |
| Local state/log retention | Ox existing private temporary snapshots and two-date log retention retained; path definitions centralized |
| Static exception decisions | Existing Ox baseline retained, registry embedded under reviews.static; no Ec suppressions copied |

The Bandit YAML and explicit INI serve different purposes and are not obsolete duplicates. Historical Gitleaks fingerprints remain separately bound to their original hash. The static-review migration log records mechanical path updates; the new catalog harness uses literal argv with no shell and receives the same source-bound Ruff subprocess exceptions as existing harnesses.

## Verification

Results and exact observed input identities are recorded alongside this report. Tests use controlled executors unless explicitly identified as native; they do not certify real scanners, vulnerability status or desktop acceptance. No full application verification was run. The complete real-security suite remains opt-in. Native Bandit found exactly three new occurrences (B404/B607/B603) in test_catalog.py. Reviewed import and literal Bash argv call in the temporary plan-only harness: no shell=True, no remote input or interpolated program. Their observed native records were added to the source-bound baseline; bandit-before-review.json preserves the raw observation. A fresh scan verifies the resulting baseline.

Historical evidence referencing moved inputs was preserved under prior/ and its dependent acceptance marked UNVERIFIED. Current regression observations do not renew prior operational acceptance.

## Documentation closure

Reviewed/updated scripts/README.md, scripts/rules/README.md, scripts/security/SOURCES.md, scripts/tests/rules/README.md, docs/development and docs/licensing active path references; feature contracts and evidence for scripts-centralization, scripts-toolbox-native, repository-maintenance, dependency-hygiene and scripts-security-preparation. sdd/project.md and architecture/constitution were reviewed; no product architecture or authorization-policy change is required. Historical validation prose keeps its original paths.

Observed commands: `python3 -m unittest discover -s scripts/tests -v` (43 tests, one opt-in skip); focused catalog and exception-mutation suite (5 tests); `bash scripts/automate.sh --scope quality --check shellcheck`, same scope with `--check ruff`, security scope with `--check bandit`, using explicit local Toolbox and shared label; `python3 tools/governance/scripts/check-ox.py`. Native runs use the unchanged consumer wrapper; raw logs are retained here. Initial failures and subsequent corrections are described above. Full Cargo/GUI/complete scanner acceptance remains outside these observations.
