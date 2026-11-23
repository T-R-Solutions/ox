# Dependency duplication: proposal research

No live Cargo file, source, policy, dependency cache, or scanner has been changed by this research.

The authenticated baseline already contains both hashbrown and miniz generations. Current LRU has no dependencies because default features are disabled. This is not attributed to the R3 LRU repair.

Local PNG 0.18.1 source contains no executable reference to miniz_oxide. Its CHANGES.md documents removal of remaining decoder uses; src/decoder/zlib.rs now uses fdeflate. The direct Cargo dependency remains. Removing that unused edge while retaining flate2 and all codec sources is a candidate, pending independent review and differential decoding/encoding plus workspace verification.

Upstream primary release notes inspected on 2026-11-19:
- https://github.com/indexmap-rs/indexmap/blob/main/RELEASES.md : 2.14 changes hashbrown to 0.17; later changes include const helpers and macro hygiene. A rollback to 2.13.1 would retain hashbrown 0.16.1 but needs API/source and macro-use assessment.
- https://github.com/rust-lang/flate2-rs/releases : 1.1.10 includes stream EOF and gzip loop fixes as well as miniz 0.9 migration. Rolling back flate2 merely for unification is not proposed.

The locally authorized RustSec snapshot has no package advisories for indexmap, png, flate2 or miniz_oxide; it has hashbrown RUSTSEC-2024-0402. This narrow textual inventory is not a scan or a declaration that candidates are secure. A candidate scan and real OSV assessment remain required.

The unacquired indexmap 2.13.1 artifact, URL, exact local registry checksum, and destination are in proposal.json. Acquisition requires specific user authorization. All source/config changes require independent review before integration; new downloads are not implied by earlier LRU or OSV grants.
