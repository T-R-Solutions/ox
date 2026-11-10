# SELinux bind access correction — 2026-11-08

User authorized applying the researched correction and real tests. Scope: Ox
wrapper, bounded shared-label support in Shared Toolbox, tests and documentation.
No downloads, image builds, central production activations, database changes,
commits or host policy/Unix permission changes. SELinux relabeling intentionally
changes xattrs only on disposable fixtures/results and isolated tool volumes.

Cause confirmed by controlled comparison: existing Ruff image on the same clean
fixture exited 1 with E902 Permission denied without relabel; existing private Z
mode exited 0 and reported All checks passed. Host SELinux enforcing and input
user_home_t labels were observed. UID/GID remained 1000:1000. Baseline and fixed
streams, native exits and cleanup diagnostics retained separately. Earlier
operational probes had malformed newline fixtures; this experiment uses corrected
real newline fixtures and validates actual report contents, not exit alone.

Implementation: shared-toolbox/toolbox/docker.py accepts explicit shared label
and emits ro,z or rw,z; unset/empty and private retain prior behavior.
shared-toolbox/tests/test_core.py covers shared, readonly, UID and isolation.
shared-toolbox/docs/operations.md documents contexts and relabel effects. Ox
scripts/toolbox.sh defaults only exec to shared; explicit overrides persist.
scripts/tests/test_selinux_transport.py covers overrides, non-exec and public
failure propagation. No label=disable or --privileged path introduced.

Verification (exit 0 unless specified): platform unittest discover: 70 passed.
Ox scripts unittest discover: 28 cases, 27 passed and one real prerequisite suite skipped.
Eight private-label real probes passed; eight shared-label probes passed:
Ruff clean/findings/invalid option, Bandit clean/findings, ShellCheck clean/
findings, Gitleaks clean. Findings were verified in native reports; Bandit LOC
was positive and errors empty; ShellCheck JSON counts matched. Two concurrent
Ruff/Bandit probes reported real findings; source hashes unchanged and both
containers removed. All eight shared probe containers also reported removed.
Public wrapper with no manual SELinux variable ran Ruff clean and exited 0.

Artifacts: results.json, shared/results.json, concurrent/results.json,
public-wrapper.{stdout,stderr,json}, platform.{stdout,stderr},
scripts.{stdout,stderr}; execution.json and native streams in each probe folder.
Local scripts qualify.py, selinux_probe.py, shared_probe.py and concurrent_probe.py
under .local/build/operational-qualification preserve reproduction commands.
Production Shared Toolbox code matches the tested isolated docker.py correction;
production active revisions remain empty. No production data was relabeled.

Governance: changed-input observations were archived verbatim, with new evidence
for current contracts. No old execution was relabeled with new hashes. This
fixes file access only: OSV/Trivy public age metadata, fresh RustSec, centrally
active qualified versions and complete scanner/report/cancellation/DB lifecycle
coverage remain pending. Native AC-03 and toolchain AC-05/06/07 stay UNVERIFIED.

Recovery: preserve this directory. For code rollback, compare current content
with changes.json in .local/build/operational-qualification/patch, then restore
individual preimages in before-shared-toolbox and before-ox only if no subsequent
changes occurred. Explicit TOOLBOX_SELINUX_LABEL= disables relabel selection,
but restores the original access failure on this host. Restoring code does not
restore SELinux xattrs; only disposable isolated paths were relabeled. Do not
relabel production roots or alter global enforcing mode to recover.

Historical platform Markdown preimages use .md.bin to preserve the exact bytes
without treating copied foreign-relative links as current Ox documentation.
The first check-ox attempt reported those foreign links; its output is retained.
These are authenticated historical snapshots, not active instructions.
