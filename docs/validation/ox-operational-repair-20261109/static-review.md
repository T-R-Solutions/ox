# Static analysis review

Actual native reports: .local/checks/run-0DVmEcXO. All 23 earlier Opengrep
findings were in intentionally unsafe rule fixtures, now stored as .py.txt/.rs.txt
data rather than executable sources. Their bytes are retained. No rule removed.

Bandit B404/B603: importing subprocess and using shell-free argv in governance
or controlled tests are not injection defects. B607: PATH-resolved test tools
operate under caller-controlled local environments. B108: /tmp values are cwd,
tmpfs destinations or intentionally rejected aliases, not predictable file creation.
B405/B314: XML is the local, versioned SVG corpus, not a product upload endpoint.
Ruff mirrors these same false positives. Native per-finding Bandit baseline and
exact-path Ruff dispositions retain scanner raw output and all other rules.
The checked source/policy SHA-256 registry invalidates dispositions on any byte
change. No nosec/noqa, severity threshold or whole-test-tree exclusion is used.
No actual vulnerability is accepted by this review. Negative controls must prove
changed source rejection and detection of newly introduced findings.
