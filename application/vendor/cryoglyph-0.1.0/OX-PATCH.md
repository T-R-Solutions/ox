# Ox dependency patch

This is the published cryoglyph 0.1.0 source with a bounded local patch. Its
upstream licenses, source, examples, benches and samples remain present. The
original 29 archive members were compared against the cached published crate
with SHA-256 `08bc795bdbccdbd461736fb163930a009da6597b226d6f6fce33e7a8eb6ec519`.

The patch changes:

- The lru requirement in Cargo.toml and Cargo.toml.orig from `0.16` to `0.18.2`,
  backporting the dependency requirement in upstream commit
  `a7a4b4b5a9fe9bf621c5c858489520fe0661ae5f`. The workspace resolves lru 0.18.5.
- Two manual raw byte casts to safe bytemuck APIs. GlyphToRender, Resolution and
  Params retain their repr(C) field order and gain derived Pod/Zeroable proofs.
  Their layouts remain 28, 8 and 16 bytes; bytemuck checks absence of implicit
  padding. The implementation retains shared borrows and zero-copy conversion.
- A direct bytemuck 1.25.2 dependency with derive support, already present in the
  Ox lock/cache, plus byte/layout regression tests in src/lib.rs.

The initial manifest-only proposal triggered two actual Ox Opengrep unsafe-block
findings. Those observations are retained. No rule, source selection or advisory
suppression is changed. Removing these two local raw casts does not claim absence
of unsafe code in transitive dependencies, including bytemuck's implementation.

Neither Iced, wgpu, cosmic-text, the configured TinySkia renderer nor Ox edition/
MSRV changes. The path dependency is excluded from automatic workspace membership;
all original 16 Ox members remain selected. The library's development Cargo.lock
is not an operative path-dependency input and is not installed here. The Ox
workspace Cargo.lock remains the sole operative resolution and remains scanned.
Registry installation markers/checksum receipts are omitted because they do not
describe a modified path dependency. Original identities/preimages are retained;
no prior repository artifact or test was removed.

RUSTSEC-2026-0253 is fixed in lru >=0.18.2:
https://rustsec.org/advisories/RUSTSEC-2026-0253.html

Verification records belong to docs/validation/r3-remediation-20261118. Default
TinySkia does not compile this optional renderer path; the separate locked/offline
iced/wgpu-bare compilation and actual layout-test execution are required evidence,
without claiming a GPU runtime test. Final project tests/scanners and independent
review/validation remain necessary before task acceptance.

Reevaluate or remove this patch when a reviewed compatible upstream release
resolves the advisory and the required compatibility, layout and security checks
pass. Any remaining local delta needs explicit disposition.
That future migration or dependency acquisition requires its own authorized scope.
