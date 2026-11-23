# Independent review — OSV acquisition successor

Reviewer context: ec_revisor / review_osv, independent of implementation, read-only.
Coordinator transcribes observed findings here; this is not an implementation
self-review. Source review is complete for central v3, Ox policy and the bounded
governance succession. The independent source review ended without remaining findings;
root public-copy execution results are recorded separately.

## Ox source review and guard disposition

Reviewer inspected backends.sh, automation.json and their consumers. No material
Ox defect found: only OSV upstream temporal veto removed; identity/provenance,
report completeness and findings rejection preserved. Trivy retains 120h/future
rejection; Grype and advisory policy configs remain unchanged.

The reviewer expressly approved updating the static source guards for these exact
inputs: changes are helper/test names, timestamp cases and fake OSV reports only;
no new subprocess, shell=True, external interpolation or suppression.

| Source | Reviewed SHA256 |
| --- | --- |
| scripts/tests/test_database_age.py | 3fb3de30be3b449f431bf6275e1b496295bcc914451a966c6bf3b43b7b352e7b |
| scripts/tests/test_backends.py | c5a3f7fe2db3693562f5f6999643e7977a0e9ec22219980062a42bd7f20175cc |
| tools/governance/tests/test_security_quality.py | 585dad004ebaecd7e3fbaed9c0688f80e603acea6e6952fc27a935945176d15e |

Independent metadata tests: 3 passed. Independent backends reexecution after
source guards: 13 passed in 108.281s. Configuration SHA256 after guards:
93384990483e592a4522f3afacc57705d48921c597d2886d4646fab0ad05c273.
Earlier combined invocation had an import-path error; the initial full backends
suite correctly rejected stale source guards (13 tests, 16 subtest failures).
Neither unsuccessful attempt is treated as current success.

Primary supporting review method actually read/applied by reviewer: software-design,
.codex/skills/software-design/SKILL.md, unversioned; contribution: responsibilities,
callers and failure-contract analysis. This guard disposition does not renew old
evidence or certify operational scanner behavior.

## Central finding requiring correction

P2: native.py successful exec --maintenance for OSV republishes a database without
acquired_at, discarding the valid receipt and forcing another download <=12h.
Native maintenance cannot distinguish a scan/copy from a validated acquisition.
Reviewer requested correction and regression before external application. The
coordinator selected early rejection of OSV native maintenance with actionable
update-db guidance; other scanners retain their maintenance paths.

The initial central review independently ran 23 OSV tests successfully, but that
success did not cover the newly discovered native-maintenance consumer. Apply
remains gated on review of the correction and new hashes. Upstream timestamp
validation before publication was also explicitly inspected and covered by a
negative test; failure preserves the previous pointer.

## Legacy acquisition migration finding

The reviewer confirmed a second semantic gap: ignoring a matching legacy
`auto-refresh.json` receipt would force download despite a known acquisition <=12h.
Correct migration must retain the exact recorded timestamp under the exclusive
lock, bind it atomically to the same snapshot, and never replace an existing current
clock or infer acquisition from mtime/now. The maintainer's reuse rule takes
precedence over the initially proposed conservative reacquisition. Correction and
independent regression review are pending; no candidate has been applied externally.

## Final source review — v3

Both P2 findings are closed on the v3 inputs. The central guard rejects native OSV
maintenance before any acquisition or Docker effects, with central update-db guidance.
Migration copies a valid matching legacy acquired_at literally under data→database
lock order only for reuse <=12h; current receipts take precedence; expired legacy
receipts do not prewrite before download, so failure preserves prior state.
Independent v3 OSV suite: 29 passed (0.620s); independent native suite: 33 passed
(0.651s). Final six source identities are in central/patch-manifest.json; read-only
comparison of the installed central files found all six equal to after_sha256.
The independent final validator also ran 29 OSV and 33 native tests against that
installed source, not just the prepared copy.

The reviewed applicator checks all source/replacement hashes before writes, refuses
symlinks and drift, journals prior bytes and replaces each file atomically. It is
not a six-file transaction and requires quiescent source writers. The central
apply-journal records state complete with the expected six v3 replacements. Later
apply attempts rejected drift because those files were already installed. The exact
executor/dispatch attribution of the completed invocation is unresolved in the
returned tool messages (an earlier approved invocation reported aborted before
dispatch); no author is inferred. This does not change the observed installed bytes,
executed tests or the effective explicit write approval.

Governance source review found no remaining defect. The new bounded registry/helper
normalizes only the exact reviewed README/project terminals into their authenticated
predecessors; no old registry/hash is overwritten and unknown content, downgrade,
changed registry/preimage or symlink is rejected. Reviewer independently passed
5 new tests and 15 HistoricalLinkTests. Public-copy results are recorded separately.
The two-line fixture update in test_historical_link_resolution.py introduces no
subprocess, boundary or suppression; exact prior bytes were reconstructed and
matched d77f0c7ad8c510422776121ab430df82e4c4df032479b9b388f0856c40fd6cc6.
The reviewed current SHA is b508bcdc3394c9d2412a647e32f6efcc4b00512366a351ee4f135709142de3c1;
its guard update is recorded in final-config-review.json, separately from earlier
test input hashes.

Limits: offline fixtures/source inspection; no live download, real Docker or full
verification; directory-fsync/hardware crash durability was not exercised. No
review claim substitutes for the independent criterion validation or broad feature
acceptance. Central tests use real temporary filesystem locks and publication with
mocked acquisition, not the operational shared cache.

Reviewer final execution disposition: the duplicate public-copy suite had three
successful methods before the root requested interruption to avoid redundant work;
it exited 130 and does not approve that entire suite. The separate root execution
remains authoritative for its final public-copy result. Source review itself is
complete. The central implementer confirmed four live applicator invocations, all
without --apply (read-only); its --apply invocations targeted only /tmp fixtures.
Coordinator and reviewer did not apply central source. Exact attribution of the
completed central journal remains unknown, rather than guessed from dispatch timing.

Final root public-copy observation: all six methods passed, exit 0, 373.059s,
retained in governance-public-copy.log. This separate completed observation closes
the public-copy execution pending above; the reviewer's duplicate exit-130 remains
historical and is not converted to success. No source changes followed the freeze.
