# Final UI integration observations — 2026-11-19

This record follows the independently reviewed UI revision02 and PNG dependency
integration. The product SHA-256 is
`58a91a46a462afae671a97ebc81d6d906b57fad1ba981dc8209fb3648e15f0dd`.
It does not declare the R3 task complete. The catalog Clippy still rejects two
hashbrown versions; the user declined acquisition of indexmap2.13.1. No suppression,
policy, feature selection or assertion was relaxed.

## Change and independent review

The high coordinator assigned root exactly four additional UI sources, with
whole-file preconditions preserving earlier edits. The exact review, before/after
identities, retained proposals, source preimages and integration receipt are in
[ui-lint-integration](../ui-lint-integration/integration.json).

- `desktop/hint.rs`: descriptive parameter names; original lifetimes and behavior.
- `desktop/icons.rs`: move existing ordered primitives into bounded helpers,
  preserve exhaustive dispatch, merge already-guarded identical match arms,
  use lossless u8 conversion and fused multiply-add for cog coordinates.
- `design.rs`: fused multiply-add only in the test contrast helper; production
  prefix byte-identical, original assertions and thresholds preserved.
- `desktop.rs`: borrow the drag event, update its two callers and mark the pure
  match const. The first combined Clippy observation found const eligibility;
  proposal01 and that failed result remain preserved.

The independent reviewer accepted the exact revision02 bytes before integration.
The standalone characterization compared 36,000 cases/185,400 ordered quads:
non-cog output was bit-identical; cog differences were confined to x/y, maximum
observed absolute delta0.0000019073486 pixel. Two deliberately changed geometry
cases were rejected by the differential oracle. The contrast helper compared
12,996 pairs from114 current palette colors, with no changed decisions at3/4.5/7.
These tests compare emitted geometry/helper values, not real Iced rendering.

## Executed checks

Commands below ran in `application/`, with the root checkout CARGO_HOME and
PYTHONDONTWRITEBYTECODE=1. Each [application-checks](application-checks/cargo-test-ui03-result.json)
observation retains argv, environment, raw streams and observed input identities;
all reported no changed inputs.

| Command / purpose | Observed result | Evidence |
| --- | --- | --- |
| `cargo build --workspace --locked --offline` |0; new product above | cargo-build-ui03 files |
| `cargo test --workspace --locked --offline` |0; ordinary workspace tests, including modal/title/dispatch tests | cargo-test-ui03 files |
| `cargo fmt --all -- --check` |0 | cargo-fmt-ui03 files |
| `cargo clippy --workspace --all-targets --locked --offline -- -D warnings` |0 | cargo-clippy-ui03 files |
| Catalog Clippy with all-targets/all-features/keep-going and all/pedantic/nursery/cargo groups |101; only hashbrown0.16.1/0.17.1, plus compilation summaries | [catalog result](clippy-catalog/result.json) |
| `cargo doc --workspace --no-deps --locked --offline` |0 | cargo-doc-ui03 files |
| `python3 tools/build_design.py --check` |0 | design-generated-ui03 files |
| `python3 tools/check_contrast.py` |0 | design-contrast-ui03 files |
| `cargo test --locked --offline -p ox-app --test desktop -- --ignored --nocapture --test-threads=1` |0; six passed, no failed/ignored/filtered,57.38s | [native result](x11/result.json), raw test streams |
| Maintained `application/tools/native_review.py`, actual current path |0,46.92s; natural0 | [Wayland result](wayland/result.json) |
| Maintained `application/tools/native_composition_review.py`, actual current path |0,32.35s; natural0 | [composition result](composition/result.json) |
| Private WC08 replay, actual current product |0,102.37s;100 checks/seven natural exits0 | [WC08 result](wc08/result.json) |
| Reviewed real-pointer drag supplement02 |0,9.71s;256→336→336 | [drag result](drag/result.json) |
| Current recent-reopen/menu sequence |0,6.58s; natural0 | [menu result](menu/result.json) |
| Fields supplement03, old navigation method |1,22.42s; timeout first S03, before a task action | [failed result](evidence-fields-failed03/result.json) |
| Fields supplement04, reviewed pointer method |0,10.67s; natural0, ACK1600×1400 | [current result](evidence-fields04/result.json) |

The workspace command alone does not execute the six ignored desktop scenarios.
They were actually executed by the separate native command. The sole remaining
ignored Rust item is the internal `subprocess_store_child` helper. Its two passing
parents invoke four real child modes: busy/record return through the harness;
exit-before-rename/exit-after-rename exit0 deliberately before Rust destructors.
The four nested starts, two normal helper results and parent snapshot assertions
are retained in Cargo03 stdout. This is an invoked helper, not an omitted scenario.
Python opt-in skips are not counted as real backend integration acceptance.

## Actual native observations and limits

The tests use a private headless Mutter with dedicated Xwayland/RemoteDesktop and
PipeWire. They do not control the primary desktop. WC08 confirmed actual configured
640×480,1024×1000,1600×1000 and2560×1000 windows. Real GTK Zenity confirmation/cancel,
exclusive creation/collision, MRU reopen/move/missing/remove/restart and explicit
corruption recovery were repeated on private fixtures. User data was not used.
No default desktop portal, assistive technology, hostile-writer atomicity or GPU
runtime claim follows.

The original WC07 outside-click image showed an open menu and remains unchanged.
The current WC08 image shows the menu closed with focus returned to File; the
independent reviewer explicitly inspected both. No cause of the earlier image is
asserted. The recent-reopen diagnostic also retains protocol, images and buffer
identities; region differences synchronize observations without proving semantics.

The drag method's first proposal lacked a sufficient post-release redraw witness
and selected the rightmost tied candidate. Independent review required uniqueness,
rejection of the former column and a public visible hover after unpressed motion.
The final method passed these checks. Independent review inspected idle256,
held336 with the4px active divider, released336 and unpressed-motion336 with a
visible Validate-directory button hover. PNG/crop/geometry are tied to one immutable
sample; received186583.383017463 was later than pre-hover186581.11852941, with
changed crop hashes and matching pointer protocol. Receipt time is not presentation
time and does not alone establish freshness or latency.

Fields03 failed during its supplemental navigation setup; no producer ran and its
failure remains a failure. Fields04 uses the visible Execute-correct and Verify
buttons after checking the actual geometry, live process and Tasks title before
each click. It retains one exclusive attempt, request identity, exact result42 and
sentinel assertions. Root inspected Verify enabled after the producer completed,
then the approved badge, criterion, run reference, observation/freshness note, request/result/producer
entries, task-oracle identity (four observed inputs total) and execution history. Independent validation
must assess the same images before any criterion disposition. This is Tasks-only
field evidence, not all five evidence states or keyboard/navigation acceptance.

## Raster comparison and retained bytes

[Bound comparison](ox-r3-native-ui03-compare-bound.json) names old/new paths and
SHA-256 identities checked before/after reading, dimensions, full-image differences
and explicit geometric regions. It covers40 Wayland,21 composition and40 WC PNG
pairs. The top content band is RGB-identical in100/101 pairs; the sole difference
is the earlier-open/current-closed WC menu image. The geometric left column does
not imply a sidebar exists in every view. Independent review recomputed all101
pairs and inspected real expanded/collapsed content, settings cog and dynamic-path
cases. Neither differences nor equality alone approve the product.

The original maintainer visual approval and bound index remain intact. The current
comparison is a new independent observation; it does not say the maintainer
approved a new binary directly.

Raw X11 PPMs are unchanged. [Lossless views](x11-lossless-views/manifest.json)
records31 PNG conversions with source/view hashes and identical decoded RGB bytes,
mode and dimensions. [Retention](retention.json), [X11 retention](x11-retention.json)
and [fields04 addendum](retention-addendum-fields04.json) identify exact retained
files. Prior native failures, proposals and results remain in the earlier
native-remediation/native-final artifacts.

The complete automation, final real opt-in backends, package/export consumers,
applicable feature gates and append-only closure record still require their own
current observations. These focused results do not replace them.
