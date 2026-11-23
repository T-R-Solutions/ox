# Independent criterion validation

Validator: `/root/repair/validate`, ec_validador_alta, fresh read-only context.
Coordinator transcribed the returned final semantic opinion.

| Criterion | Verdict | Observed basis |
| --- | --- | --- |
| terminal AC-01 | APPROVED | Controlled 1/3 check plans versus JSON, N+2 and phase identity. |
| terminal AC-02 | APPROVED | Monotonic measured/opaque progress, no premature 100% on failure/cancellation. |
| terminal AC-03 | APPROVED | Success/findings/errors/blocked/skipped/cancelled/recorded states, codes/limits/references. |
| terminal AC-04 | APPROVED | Location/cause certainty/counts and secret/control rejection oracles. |
| terminal AC-05 | APPROVED | PTY/plain ANSI32/31/33, hierarchy, NO_COLOR, TERM=dumb, JSON/raw bytes. |
| terminal AC-06 | APPROVED | Slow publication without competing writes, cleanup, signals/EOF and failure paths; independent review. |
| history AC-03 | APPROVED | Manual inspection of both fixed acceptance sentences plus state/code regressions. |
| history AC-01/02 | UNVERIFIED | Historical scanner observations are not renewed. |

Executed sha256sum -c against implementation/inputs.sha256 and artifacts.sha256:
all records OK, exit0. Inspected full 28-terminal and13-lifecycle logs, Bash syntax,
paired preimage FAIL/current PASS oracle; no unnecessary suite repetition.
Main hashes: progress.sh 8a36dd6db249943f1b5a62a7fd53a5f6b8952ac239b93053949cc4a1b55e088d;
new test 79aa40faedda0de16d7cfa51295b5eed0707b104530e8ceff6320238b70a89a9;
original test 665987e42c74b38db9c21d09b26155473c32550ac45d59c6f6cbbf254c99855f.

Limits at semantic verdict: native ShellCheck and final documentary gate were
pending. Replay proves competing writes, not the exact incident interleaving.
Fixtures do not qualify scanners or product acceptance. Mandatory governance had
failures, so no pipeline approval. Final gate disposition is recorded separately
after receiving native results and documentary freeze.
