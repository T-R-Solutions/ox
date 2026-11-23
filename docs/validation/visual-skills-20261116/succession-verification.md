# Visual skill successor implementation — 2026-11-16

Scope: new tools/governance/scripts/visual_skill_revision.py; minimal integrations
in closure_revision.py, check-ox.py and instruction_revision.py; new
 tools/governance/tests/test_visual_skill_revision.py; new
 docs/validation/visual-skills-20261116/succession.json. No writes to existing
skill_revision.py or historical registries/archives. No new predecessor backups.

The fixed registry authenticates five existing paths (three SKILL entries, native
visual reference, checker source) and three new references. Byte-range edits
reconstruct predecessor bytes in memory, authenticated by predecessor SHA-256.
The three new files have current SHA-256 checks and no predecessor. Registry
SHA-256 fixed in the module:
8d758bb831971529df7af2adb580faf48d2496c172c800977797852acb1d7208.
Unknown live bytes never normalize; original preservation checks remain active.
Root/parent traversal and symlinks are rejected, as are missing/extra/duplicate scope,
malformed/overlapping edits, predecessor downgrade, and mutated registry/current bytes.
The checker authenticates the same registry byte buffer it parses. No path exemption
or missing-registry compatibility branch remains. errors() requires the registry.

The instruction registry protects checker-source bytes. The narrow new normalization
runs before its existing log/historical normalizers without modifying their hashes.
The coordinator/root authorized a one-line update to the already-dirty
log_repair_revision.fixture_paths helper: include the new registry when isolated
fixtures copy current checker source. Observed whole-file SHA before the edit:
d59a01f8f25e82aa9620d0dbd07b2949e026654b280d25a5ef63d695d048331d;
after: 62e66b040f5600613a7ef756cd9ea7e4f1c45f1643d773afcc68a7f46fb9ff81.
The precondition compared the complete read bytes immediately before replacing the
single exact return line. All other dirty content was preserved.

This is exact documentary succession, not a generic patch/rollback interface. It
does not approve skill effectiveness, product rendering, accessibility or a broader
UI delivery. Publication, commits, upstream execution and full scanner verification
were not performed. The coordinator owns ADR/feature acceptance/doc closure.

## Observations

- PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools/governance/tests -p test_visual_skill_revision.py -v: 7 tests PASS, exit 0 after final source stabilization. Covers each current mutation/deletion/symlink/downgrade, exact predecessor normalization, unknown buffers, registry mandatory current gate, registry mutation/missing/symlink, closed scope/malformed edits, duplicate JSON and symlinked parents; literal synthetic predecessor is an independent small oracle. Earlier test iteration failed when an intentionally huge first edit also overlapped a later edit; fixture now enlarges the last edit to exercise bounds validation separately, without relaxing implementation.
- Same unittest command with -p test_visual_succession.py: 5 tests PASS, exit 0; old visual registry behavior unchanged.
- Same unittest command with -p test_readme_skill_integration.py: 11 tests PASS, exit 0 on final2 source set, including copied independent-distribution checker and unknown-resource rejection; /tmp/ox-visual-readme-tests-final2.log. Earlier runs correctly rejected an inconsistent in-flight registry during the final description change, then detected the checker-source instruction succession gap; those were corrected and rerun.
- Same unittest command with -p test_instruction_copy.py: 6 tests PASS, exit 0, final2 log /tmp/ox-visual-instruction-tests-final2.log. Earlier runs rejected the fixture with missing registry; copying its explicit new dependency resolved this without weakening missing-registry checks.
- Independent manual observation compares R.predecessor for all five existing paths against git show HEAD:path, byte-for-byte. Every comparison passed. These paths were clean at task entry. /tmp/ox-visual-predecessor-oracle.log identifies exact hashes; the shipped test suite remains Python stdlib and does not require Git.
- git diff --check for assigned existing source paths: exit 0.
- PYTHONDONTWRITEBYTECODE=1 python3 tools/governance/scripts/check-ox.py: exit 0, PASS local profile/catalog/bridges/skill copies/SDD/normative IDs/links/archive inspection; /tmp/ox-visual-check-final.log. This is structural/governance success, not product acceptance. Earlier checker observation found the new checker-source instruction binding gap; no preexisting failure is inferred from it.

## Limitations and documentation disposition

Tests exercise preservation and rejection contracts in local/disposable fixtures,
not resilience against an adversary who can rewrite checker code and its anchors.
Filesystem path validation and one-buffer registry authentication do not constitute
OS isolation or a general concurrent-filesystem transaction guarantee. No performance
or visual-quality improvement was measured. The required documentation update is
returned to the coordinator: ADR visual-skill-refinement, new feature and analysis
report need to describe the fixed source scope, inline transformation and isolated
fixture dependency. Existing application/design policy is unaffected because this
subtask changes only skill evolution checks. Historical evidence is preserved.
