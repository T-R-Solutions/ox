> Current follow-up — 2026-11-17: the blanket closure below is historical.
> Review found the D-14 translation claim false and the V-11 focus repair erased
> button-role/state colors. Those assertions and their acceptance are superseded
> by [the follow-up](../audit-followup-20261117/report.md). Exact prior bytes are
> retained there; historical test results are not renewed. Native/product-wide
> acceptance still requires its own observations.

# Independent validation — bounded audit correction

Fresh ec_validador_alta context; read-only, separate from implementation and review.
The coordinator materialized this record from the validator's returned observations.

| Criterion | Final state | Basis and limits |
| --- | --- | --- |
| AC-01 | APPROVED | All 151 findings have differentiated dispositions, sources and limits. Optional proposals and historical observations were not silently promoted into defects or operational acceptance. |
| AC-02 | APPROVED | Integral comparison against preserved envelopes: 40 observation objects moved intact, none lost; only three APPROVED→UNVERIFIED changes. Mandatory evidence inputs and SDD checker preserved. |
| AC-03 | APPROVED | Documentation/source inspection and focused tests support the bounded repairs; 17/17 skill postimages match. No native acceptance follows. |
| AC-04 | APPROVED | Independent execution, preserved copy artifacts and final separate gate review support checks and limits. Gate review found no remaining finding; final input hashes match. |

## Independently observed methods

- Cargo test for ox-ui with the selected local cache, locked/offline: exit 0;
  49 unit tests plus five integration tests passed. One subprocess helper is
  ignored at top level and exercised through parent process tests.
- Design generation and contrast: exit 0. SDD structure: exit 0.
- SDD acceptance over 35 explicitly selected affected features, with
  --require-approved --require-fresh --check-convergence: exit 1 exclusively for
  187 INCONCLUSIVE/UNVERIFIED states. No additional schema, freshness or projection
  failure. Wrapper inspection exit 0 does not change the child checker's exit 1.
- New audit suite: seven adversarial tests passed, exit 0, after the final helper
  correction. Root check-ox passed before that bounded helper correction; the
  changed branch was tested independently and in the final copy. The separate
  reviewer later reran root check-ox on final bytes, exit 0.
- Copy artifacts inspected directly: initial failure contains exactly two DESIGN
  links; final log records PASS. Receipt is explicit, application is absent and
  copied code/helper/registry bytes match the source. The validator did not rerun
  the copy. Its Python audit hook constrains observed Python access, not the OS.

Final gate identities independently checked:

- audit_revision.py: `330c9f17d54e47389cdcbf67a12f7c28f20b955405268bfe6e0f7f7a97767aef`
- readme_revision.py: `257888da876617b8d84f04e1a6f29788948e9c41aaf79c955dbb710c8eff6b16`
- test_audit_revision.py: `91990d3a5ccfc85c226692b3207d31d22bd68a763c1bbdae8d38faba600e23ec`
- succession.json: `fc5127b589f98df748aef6caa01fc392fae8649ccb8378b4a6216a6461085709`
- Cargo.lock: `99d3907a15d227674b420a6cfcede596be840144c3db9ff070547c948bc40ab8`

UI inputs match final-ui-inputs.json. Full checks and snapshots are described in
governance.md, succession.md, review.md and the execution records, not inferred
from an implementer's completion statement.

## Preserved provisional decision and successor

The initial validator result approved AC-01–03 and left AC-04 INCONCLUSIVE because
final separate gate review had not yet reached that context. No code/registry/UI
input changed between that result and resumption. On resumption the validator read
the final independent gate review and rechecked the four gate hashes (inspection
exit 0, no divergence). It then explicitly changed AC-04 to APPROVED for this manual
supplement, without repeating unaffected tests. That final review had independently
executed seven audit tests, five Windows tests, one origin test and check-ox,
all exit 0. Agreement alone was not used as operational proof.

Limits remain: no global feature approval, native interaction, AT, SVG render-fit,
VS Enterprise parity, full scanner run, OS sandbox claim or publication/distribution
approval. Changed relevant inputs require new dependent observations; preserve these
records. No validator file edits or live subprocesses remain.
