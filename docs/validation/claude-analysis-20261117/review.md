# Independent review record — 2026-11-17

Recorded by the coordinator from the final message of the independent ec_revisor
context `/root/correcoes_analise/revisao`; the reviewer itself remained read-only.
This record is not an implementation self-review or an independent validation verdict.

Final disposition: no open implementation findings in the examined scope.
Compared the preserved preimages with changes to runner/report/selection, typed
argv, lifecycle ownership, dataset/source integrity, canonical hashing, tests,
static policies and exact documentary succession. Consulted software-design.

Findings corrected and reexamined:

1. Missing `os` import in the PTY fixture: restored; four terminal/cancellation/
   publication scenarios passed in 6.754s.
2. Governance callers still expecting ValueError: migrated to ShellError with
   expected status; four consumer methods passed in 0.666s.
3. Removed Python Geiger helper still used externally: consumer now invokes the
   production manifest guard; 16 paths plus traversal/symlink/missing rejection
   passed in 0.050s.
4. Real opt-in timeout shorter than native budget: now configured native timeout
   plus 600 seconds; inspected, no real scanner execution claimed.
5. JSON oracle shell branch still caught ValueError: now catches ShellError and
   asserts status 1/5; independent Python parser ValueError unchanged. Retest passed
   in 0.384s. The original suite's 17 subcase errors remain in scripts-tests.log.

Other executed review observations: new 15 regressions passed in 2.036s;
capture/status 7 passed in 0.039s; documentary successor/audit 13 passed in 5.568s.
The second full scripts run was still in progress at final review, so this review
does not claim its outcome. The validator evaluates the final run separately.

Semantic disposition is favorable to updating only the existing 16 source bindings
and one Ruff policy binding in reviews.static. No baseline expansion, ignored
rules or historical evidence renewal. Bandit baseline remains:
`b2456e9e072de702ef2c8c41dd2d23829470be48066a2c4e44ae4f5948dc32a7`.
Detailed old/new bindings are in static-review-update.json.

Observed final identities:

| Path | SHA-256 |
| --- | --- |
| scripts/checks/run.sh | 5cc5720715a2fb185dc90d883b81b6a50f45c183e0ca501d47986d79c55f57ec |
| scripts/lib/process.sh | 95d14d3e90c3479b1ca95f3403e3763c0f2d9593ab670d20e74c0c9a44762b90 |
| scripts/lib/files.sh | ffa04cc54a571e98eabdc8bbb5fbf6423b2e939af3ce211eadc238e29b4ae6bb |
| scripts/tests/test_json_guard.py | 32414bfcd57fc628dd519b2998186e8065e03ad63dd7a031b8d82a4384f3c3be |
| tools/governance/tests/test_security_quality.py | af99abf086ddf4b4b4fbd66457df131d70754080619e5145166267634fda3c43 |

Prepared Rust/YARA fixtures and expectations were inspected: Rust covers all
alternatives of the three added reference rules; six YARA HEX records decode to
positive/negative examples for the three rules. HEX avoids triggering the normal
recursive source scan with permanent synthetic positives. Native matching remains
UNVERIFIED. Existing broad AC01–07 receive no renewed approval.
