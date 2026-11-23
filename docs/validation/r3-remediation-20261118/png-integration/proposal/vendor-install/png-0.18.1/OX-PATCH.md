# Ox dependency patch

Published PNG 0.18.1, authenticated against the cached crates.io archive with
SHA-256 `60769b8b31b2a9f263dae2776c37b1b28ae246943cf719eb6946a1db05128a61`.
The original source, examples, benches and MIT/Apache licenses remain unchanged.

The only upstream delta removes the unused direct miniz_oxide 0.8 dependency
from Cargo.toml and Cargo.toml.orig. The decoder uses fdeflate; the encoder keeps
flate2 1.1.11 and its miniz_oxide 0.9.1 backend. No codec, feature, test, bench,
development dependency or rejection rule is removed. No advisory or scanner
suppression is added.

The published crate's development Cargo.lock is preserved in remediation
evidence, not installed as a second operative application resolution. The Ox
workspace lock remains authoritative. The crate is excluded from automatic
workspace membership, as with the existing cryoglyph patch. Registry cache
receipts are not installed as authentication of this modified path dependency.

Original and patched public image APIs were tested using an independent RGBA
fixture, roundtrip, truncated data, corrupted payload, CRC-only corruption and
the three bundled identity assets. The maintained regression is
crates/ox-ui/tests/png_assets.rs. These observations do not claim the entire
upstream suite: the published crate omits its pngsuite corpus and development
dependencies are not all available in the authorized cache. No upstream test
was removed or rewritten to make that suite pass.

This dependency edge was already duplicated in the pre-R3 lock. The separate
hashbrown duplication remains a mandatory Clippy finding; this patch does not
claim the complete gate passes. Reevaluate this patch when an authorized and
reviewed compatible upstream release removes the unused dependency.
