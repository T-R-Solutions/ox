# Current OSV closure correction record — 2026-11-16

Pre-verification record: correction implemented; native verification and independent
acceptance were pending at freeze. Current final outcome is recorded separately in
[outcome.md](outcome.md). This supersedes the initial OSV-05 closure approval for the changed
governance/test inputs. OSV acquisition source is unchanged; prior results and
acceptance-inputs.json remain historical, not proof of the corrected closure.

## Observed regression and causes

The retained ox-run-hqdod3TY aggregate contains 26 results: 23 passed/recorded;
exactly ox, governance-tests and Ruff failed. OSV, Trivy, Grype and Bandit passed
in that run. The three failures are attributable to this delivery:

- ox rejected the convergence section added after the previous final check-ox.
  Nine governance test failures report the same unregistered current bytes.
- Governance reported 21 errors: the new strict current-content rejection escaped
  project/skill errors() APIs that promise diagnostic lists. The first mutation
  left a test fixture altered, causing repeated subtest errors. Registry/preimage
  errors must still raise; silently accepting them is not a correction.
- Ruff reported E741 for alias O in the new successor test. Root renamed it to
  OSV_REVISION without suppressing a rule.

Prior governance run: 326 tests /1886.107s, 9 failures, 21 errors, 1 skip. The
remaining results are preserved as observations, not blanket product acceptance.
Raw aggregate/governance/ox failure bytes are retained alongside this report.

## Bounded correction and documentation disposition

The original document-successors.json remains byte-identical. closure-successor.json
registers only scripts-toolbox-native/converge.md against the existing historical
preimage55cd5e8033aef32798284dee7c349a3af106ab32de09179c32349425fec5d0c3.
The predecessor was reconstructed by removing only the earlier appended section
and matched the immutable instruction registry. The current convergence narrative
now identifies the original closure limitation and points here; it is frozen
before final verification. Earlier convergence/report/code bytes remain in before/.

CurrentContentError marks only changed/downgraded live terminals. project.errors
converts it into its existing diagnostic; skill.errors handles it per file. Other
schema/registry/preimage errors propagate exactly as required by existing tests.
The metadata test includes the new registry and strict closure rejection; alias
rename preserves behavior. No scanner threshold, finding policy or exemption changed.

Reviewed/updated documentation: this plan/report, parent report/plan, parent feature
tasks and convergence. README/project/current OSV ADR, constitution and architecture
reviewed without changes: the defect concerns acceptance integration, not acquisition
policy or product architecture. Central v3 files remain untouched. Existing broad
feature gates remain UNVERIFIED/INCONCLUSIVE. No commit/publication/full run.

## Final observations

Pending the single frozen-input native run and independent review/validation.
The result will be recorded here and in a separate verdict artifact without editing
protected convergence, registry, code or configuration after verification.

Focused rejection testing exposed an additional masked integrity gap: the ADR was
required to exist but its modified content was not rejected. The helper now pins
its exact current SHA256; the original registry stays unchanged and the existing
InstructionCopy assertion remains strict. The new test explicitly mutates/deletes/
symlinks both registries, the ADR and all preimages. First focused expanded attempt
recorded this failure; it is retained separately from the corrected observations.
The registry/preimage exception assertions in ProjectRevisionTests are unchanged.
