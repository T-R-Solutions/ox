# Locked lru dependency remediation — 2026-11-18

Status: proposed integration. Source and layout proof were independently reviewed;
the maintained test entry awaits its own independent review. Final workspace/native/
security observations remain required.

The authorized R3 verification found OSV RUSTSEC-2026-0253 in lru 0.16.4 in the
operative application lock. The user separately authorized acquisition of exactly
lru 0.18.5 into the checkout Cargo cache; this is not permission to update the
central Toolbox or acquire other dependencies. The downloaded 19,761-byte crate
matches the checksum in the existing registry index and proposed lock:
`ef9ac18847474e638e3702b76c65d4eb93428471a74778ef0f1be711717f89b5`.

## Decision and alternatives

Use the published cryoglyph 0.1.0 sources as a documented local path patch, retaining
all source/examples/benches/samples and upstream licenses. Backport the lru
requirement change from `0.16` to `0.18.2` in normalized/original manifests. The
workspace lock resolves compatible lru 0.18.5. Preserve Iced 0.14.0, wgpu 27,
cosmic-text 0.15, the configured TinySkia renderer, edition 2024 and Rust 1.99.
Exclude the dependency folder from automatic workspace membership: the same
16 first-party members remain subject to workspace commands.

The published archive was already cached and matches its lock checksum
`08bc795bdbccdbd461736fb163930a009da6597b226d6f6fce33e7a8eb6ec519`;
all 29 members were compared against that archive before patching. Keep provenance
and an explicit patch notice with the vendor. Omit only the upstream library's
non-operative development lock and registry installation receipts. Its original
lock identity/bytes remain in the retained preimage. The Ox workspace lock stays
operative and scanned, without a scanner exclusion or advisory suppression.

A direct lru lock bump cannot satisfy cryoglyph's existing `^0.16` requirement.
Upstream's manifest-only correction exists, but its Git revision also depends on
a different wgpu/cosmic-text stack. Adopting that stack would broaden this repair.
Deleting an operative dependency from the lock, disabling scanning, or suppressing
the advisory would not satisfy the requested acceptance criterion.

## Safe conversion follow-up and reproducible tests

The manifest-only proposal introduced two real findings under the unchanged Ox
Opengrep unsafe-block rules in vendored text_render.rs and viewport.rs. Instead
of excluding vendor sources or suppressing those findings, replace their two raw
slice conversions with bytemuck::cast_slice/bytes_of. Derive Pod/Zeroable for the
three repr(C) structures without reordering fields or adding implicit padding.
The already cached bytemuck 1.25.2 and derive dependency are reused; no additional
acquisition was required. No first-party renderer feature or GPU backend changes.

The contract remains GlyphToRender 28 bytes, Resolution 8 bytes and Params 16
bytes. Four actual library tests check literal sizes/offsets, independent native
byte encodings (including floating-point negative zero and NaN bits), explicit
padding, empty/multiple glyph slices and zero-copy pointer identity. Compile-fail
fixtures independently reject implicit padding and a bool field as invalid Pod.
Derived checks do not imply absence of unsafe internals in bytemuck or other
transitive dependencies. Actual unchanged Opengrep rules scanned all nine Rust
files: initial proposal two findings; corrected proposal zero findings, no errors.

application/tools/test_vendor_layout.py is the maintained development test entry.
It locates the already installed pinned compiler without requesting installation,
uses locked/offline Cargo to build the actual optional iced/wgpu-bare path, binds
all six direct externs by exact Cargo package IDs and observed artifact hashes,
and compiles/tests the actual vendored lib.rs with rustc. A new report directory
retains every command, exit, stream and before/after input identity. Required tests
must all run; ignored/filtered tests or changed inputs reject acceptance. The two
expected compile failures require their specific layout diagnostics.

The entry explicitly reuses the checkout's existing test-only process adapter in
scripts/tests/support.py. Calls use argument lists, no shell, explicit environment,
cwd and raw streams, and timeout=None; source provenance includes the adapter.
Bandit does not perform transitive argument analysis through this adapter: source
review must examine the new caller independently. Raw scanning of both files
reports only the three preexisting adapter occurrences; the unchanged source-bound
baseline filters those occurrences. No scanner rules or baseline entries change.

Upstream dev dependencies, examples and benches remain present. The direct unit
entry executes all library tests (currently four); it does not execute upstream
benchmarks/examples or download their unavailable criterion/pollster dependencies.
This explicit method is necessary because the vendor is not a workspace member;
workspace cargo test alone cannot provide this layout-test coverage.

## Exposure and limits

RustSec describes an unsound pop operation when key destruction panics and unwinds;
the patch starts at lru 0.18.2. Current default Ox features do not select lru.
Upstream additionally notes Copy cache keys and pop_lru usage in cryoglyph. These
observations bound current exposure; neither proves universal non-exploitability
nor removes the actual lockfile finding.

An offline metadata attempt with the optional `iced/wgpu` feature failed because
the index lacks `wgpu-core-deps-apple`. No additional package was acquired. The
official `iced/wgpu-bare` feature selects the complete relevant API path without
default platform backends: ox-ui → iced → iced_renderer → iced_wgpu → the patched
cryoglyph → lru 0.18.5. That explicit path compiled with locked/offline Cargo in
25.01 s, exit zero, with proposal inputs unchanged. This establishes type/API
compatibility in the observed environment, not a GPU runtime or presentation test.
No mandatory project test or feature selection was reduced.

Integration requires final offline/locked workspace tests, formatting, lint,
native scenarios and actual scanners, with unchanged-input evidence and independent
validation. Preserve the old finding and failed metadata attempt. Do not relabel
historical evidence or infer success from a hypothetical advisory exception.

Maintenance owner is the Ox application dependency maintainer. Remove the local
patch only when a reviewed compatible published cryoglyph release includes the
advisory fix and the required compatibility, layout and security checks pass. Any
remaining local delta requires explicit disposition.
That later migration is not authorized by this decision. Recovery retains the
original workspace files and published-source identities and changes only this
patch, preserving unrelated work and all verification history.

Primary references:

- [RustSec advisory](https://rustsec.org/advisories/RUSTSEC-2026-0253.html).
- [Published cryoglyph manifest](https://docs.rs/crate/cryoglyph/0.1.0/source/Cargo.toml).
- [Upstream manifest correction](https://github.com/iced-rs/cryoglyph/commit/a7a4b4b5a9fe9bf621c5c858489520fe0661ae5f).
- [Cargo lockfile roles](https://doc.rust-lang.org/cargo/faq.html#why-have-cargolock-in-version-control).
- [Cargo workspace membership](https://doc.rust-lang.org/cargo/reference/workspaces.html).
