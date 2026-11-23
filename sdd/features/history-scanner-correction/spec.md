# History scanner correction

The maintainer requests correction on 2026-11-15 after identifying a Gitleaks
history finding on a validation SHA-256 and ambiguous terminal acceptance text.
Scope includes reviewing the same-cause findings in the observed report, bounded
exceptions, clearer presentation, focused real checks and independent acceptance.
No complete pipeline, downloads, central changes, repository commits or publication.

- REQ-01: Suppress only individually demonstrated false positives with exact commit/path/rule/line fingerprints and preserve the authenticated ignore mechanism.
- REQ-02: Continue detecting secrets in documentation/history; do not exclude paths or rules globally, and reject a changed unauthenticated ignore file.
- REQ-03: Explain that functional product acceptance is evaluated separately, without implying a failed check or changing execution states/codes.

- AC-01 → REQ-01: Every added fingerprint is supported by committed source context and reviewed digest provenance; a real history scan removes the reviewed findings.
- AC-02 → REQ-02: A real synthetic secret in documentation remains detectable; altered fingerprints do not suppress the original finding; authentication mismatch still blocks.
- AC-03 → REQ-03: Both terminal messages explicitly separate functional acceptance; focused terminal regressions pass without state/code changes.

Unknown findings remain findings. A clean focused history report is not approval
of all scanners, the entire historical corpus's safety, or the application.
