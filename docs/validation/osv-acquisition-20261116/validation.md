# Independent final validation — 2026-11-16

Verdict: **OSV-01..05 APPROVED in the bounded manual offline scope**.
Validator: ec_validador_alta / validate_osv, fresh context independent of all
implementers and the source reviewer. The validator made no file changes.
The coordinator transcribes the final returned verdict here without altering its
observed input manifest or promoting broad feature gates.

| Criterion | Method and observed result | State |
| --- | --- | --- |
| OSV-01 | Inspected backends/config/native policies; independently passed 3 metadata and 16 security-quality tests; reviewed log of 13 backends tests. OSV upstream veto removed; provenance/findings, Trivy/Grype and advisory exceptions preserved. | APPROVED |
| OSV-02 | Independently ran 29 OSV tests against installed central source, exit 0: absent/unknown acquisition, 43200/43200.001 boundaries, repeated analyses and literal legacy receipt migration. | APPROVED |
| OSV-03 | Same 29 OSV and 33 independent native tests passed: manual/identical acquisitions renew only on success; failures preserve state; generic OSV maintenance rejects before refresh/Docker. | APPROVED |
| OSV-04 | Real temporary filesystem flock and atomic replacement tests demonstrate serialized acquisition, consistent identity/timestamp pairs and retention of prior snapshots. | APPROVED |
| OSV-05 | Final docs inspected; 5 independent succession tests and check-ox passed; logs of 32 focused governance and 6 public-copy tests examined. Historical evidence preserved; broad gates not promoted. | APPROVED |

Independent commands used PYTHONDONTWRITEBYTECODE=1 with python3 -m unittest
discover and patterns test_osv_refresh.py, test_native.py, test_database_age.py,
test_security_quality.py and test_osv_acquisition_revision.py. Central tests ran
from /home/rodrigo/Projetos/dev_audit/shared-toolbox against actual installed source,
with temporary stores and controlled HTTP/Docker boundaries; Ox tests ran from
the checkout. The final security-quality observation used configuration SHA256
f59d5f2a4755740da36a91501204af051b9fa3d6435a4cecaaec0169f779fef5
and passed 16 tests in 15.787s. Its earlier recorded run remains historical.

Final read-only comparison: 31 inputs in acceptance-inputs.json matched their
current hashes, all six installed central files matched central/patch-manifest.json,
and central configuration retained osv_refresh_hours = 12.
Acceptance manifest SHA256:
89a8f6452a253a7a8a47c6ec15cab6e0401656511d4eee62c69b6aa1b3add790.
The manifest identifies current closure inputs, separately from older execution
manifests; it does not silently renew their historical results.

The selected automated checker command was:

```text
python3 sdd/tools/validate.py --root . --features sdd/features --feature scripts-toolbox-native --feature scripts-toolchain-config --require-approved --require-fresh --check-convergence
```

It returned exit 1 exclusively for the ten broad gates still UNVERIFIED or
INCONCLUSIVE. This manual bounded approval does not constitute automated
acceptance of those features or complete scanner/product qualification.

Limits: no real download, live Docker qualification, complete run or physical-crash
experiment. Installed hashes and the completed journal prove the observed central
state; the invocation's executor/dispatch attribution remains unknown. No attribution
or broader operational success is inferred. Reevaluate affected observations if
inputs change; operational qualification requires its own authorized executions
and independent evidence.
