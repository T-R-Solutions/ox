# Task closure integration — observed acceptance

AC-01 APPROVED: all 92 imported file preimages were preserved outside the active
tree and their SHA256 values rechecked; 90 unused paths are absent and two paths
were rewritten. inventory.json records purpose, dependencies/effects, references,
compatibility, decisions and replacements. No symlinks/archives were present.
recovery-verification.json is the per-file observation. Recovery remains local at
/tmp/ox-scripts-integration/recovery; retain it before temporary-directory cleanup.

AC-02 APPROVED: seven behavioral tests passed (contracts-final.txt): explicit
selection and offline flags, real CLI execution from another directory, paths with
spaces, invalid manifests/arguments, required tool absent, raw binary streams and
exit 23, plus rejection of unknown authority mutation/registry corruption.
No Node/Bun/Gradle/Tauri/service dependency remains in the active scripts.

AC-03 APPROVED within governance scope: current authority/README/SDD/skill-interchange
review, original SDD structural validation, check-ox and 63 fast tests passed via
scripts/automate.py --scope governance. All integration tests passed separately via
python3 tools/governance/scripts/run-tests.py --group integration; see logs for
count/timing. verify-maintenance reports no errors, 485 preserved governed files
and 439 recovered layout inputs. git diff --check passed. Combined groups exercise
the full governance suite without demanding approval of intentionally undecided ACs.
The copy boundary explicitly adds only the two resulting scripts; no package release.
Skills' reusable bodies, catalog and profile remain unchanged. Their local closure
mapping is in docs/development/sdd-skills.md and the workflow/AGENTS contract.

Rust smoke: fmt/check/build/clippy passed offline against the actual workspace;
initial cargo test failed with PermissionDenied on Unix sockets in the sandbox
(raw result retained). The identical cargo test --workspace --locked --offline
passed outside that restriction (observed exec session 61083, exit 0). Six desktop
cases were ignored; this provides no new graphical approval. No product source
was changed by this delivery. Product input revisions include preexisting work,
so this smoke is supplementary, not acceptance of that unrelated work.

Earlier all-suite runs are retained as failed observations during input stabilization;
changes to the registry while earlier processes held old imports and newly stale
fixture bindings explain those failures. Only final fast/integration successors
support this closure. Nothing rewrites their failure logs into success.

Affected old observations are preserved verbatim in historical_evidence and exact
before/ preimages (plus before-fixture-update/ for the later fixture succession).
Dependent criteria remain INCONCLUSIVE pending bounded successor review; see both
affected-*-evidence.json manifests. Unaffected operational observations remain.
No old approval is transferred to changed documentary inputs. This is an explicit
pending acceptance limitation of other features, not approval of the product.

No external solution is newly required, so no erase.md or installation was created.
No commits, publication, hooks or image pulls. Graphical criteria are NOT APPLICABLE
to this governance delivery; subsequent UI changes need separate X11/Wayland methods.
Schema bindings cover the feature, scripts, core authorities, validators and oracles.
The recovery observation depends on local /tmp bytes; the application README and
supplementary product smoke were manually inspected, not automatically bound as
current product acceptance. Automated hashes do not authenticate an oracle or OS
isolation, and an independent-copy test is not distribution publication approval.
