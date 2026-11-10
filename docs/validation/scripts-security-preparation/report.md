# Security preparation acceptance — 2026-11-06

Default official OSV/RustSec acquisition and reviewed OSV import executed with
OSV 2.7.0 and cargo-audit 0.22.2. The actual offline scanner runs and negative
OSV tests ran under `bwrap --unshare-net --bind / / --dev /dev --proc /proc`.
This isolates networking, not file access. The sandbox initially denied namespace
creation; the authorized escalated execution succeeded. Native scans returned
findings, not infrastructure failures: RustSec reports unmaintained pin-utils
0.1.1 and ttf-parser 0.25.1. No product dependencies or risk exceptions changed.

`python3 -m unittest discover -s scripts/tests -v` exercises adapter contracts;
the real data test is separately enabled by OX_REAL_OSV=1 in the network namespace.
It accepts reviewed import and real scanning, rejects missing/expired/corrupted
data before scanner execution, rejects a corrupt ZIP even with a recalculated
review digest, and confirms byte-identical published registry after failed import.
Raw outcomes are in offline-tests.txt and regression.txt.

`opengrep test --config scripts/security/rules scripts/tests/rules` passes 9/9
rules. Final `checks/run.sh --check opengrep` ran without network and verified all
103 selected source paths. All 23 findings are intentional positive test fixtures;
triage.json identifies each rule/path/line. No other matches or parsing errors.
The snapshot includes Rust and Python tests: initial upstream default exclusions
were caught by the existing completeness check. The final adapter uses the native
1.33.1 experimental ignore bypass; unavailable flag/report contracts fail closed.
Compiler unsafe prohibition remains primary. These are bounded syntactic rules,
not proof of safe dataflow, paths, permissions or concurrency.

Backend regression includes another cwd, spaces, PATH discovery, explicit valid
and invalid paths, missing tools, native Cargo selection, locks, report tampering
and runtime failures without fallback. The installation contract is a layout check;
trust in installed code remains necessary. Existing image/version/hash/report
controls are preserved, not replaced by discovery.

Optional native Trivy/Grype preparation is implemented but real compatibility
acceptance is UNVERIFIED because those scanners and databases were not selected
for local acquisition. Their sources and CLI contracts were reviewed. The external
Grype toolbox adapter retains its existing independent database contract.

Observed scanner hashes, dataset/provenance metadata, raw reports, assessments,
fixtures, implementation and tests are bound by the feature evidence. Data remain
outside Git under specific ignore rules. Earlier toolchain observations retain
their original inputs and are superseded only where affected. No commit,
publication, product change or claim of complete security acceptance.
