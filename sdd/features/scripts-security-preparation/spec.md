# Explicit security preparation and detection

REQ-01: Prepare official or reviewed imported OSV/RustSec data by default and optional Trivy/Grype data; validate dates, format and scanner compatibility before atomic registry publication. Preserve prior generations on failure. Separate provenance/review from integrity.
REQ-02: Local Opengrep rules cover execution, deserialization, TLS and prohibited unsafe; positive and negative examples document limitations.
REQ-03: Discover native scanners first, then explicit OX_TOOLBOX_BIN or PATH toolbox, resolving and validating installation without runtime fallback.

- AC-01 → REQ-01: Real offline analysis succeeds in executing; missing, corrupt and expired data block; failed preparation preserves published data.
- AC-02 → REQ-02: Real Opengrep fixture tests and project scan identify scanned files and triaged findings.
- AC-03 → REQ-03: Relocation, spaces, PATH, explicit invalid and absent executable tests pass; existing image/result controls remain.
- AC-04 → REQ-01: Optional Trivy and Grype preparation probes accept real compatible datasets and reject incompatible ones when selected.

## Ownership successor — 2026-11-07

The explicit maintainer decision in docs/decisions/scanner-toolbox-ownership.md
supersedes REQ-01 preparation and REQ-03 native preference for Trivy/OSV/Grype.
Only RustSec is locally prepared now. AC-01/03/04 observations above describe the
predecessor contract; new ownership acceptance is scripts-toolchain-config AC-05..07.
