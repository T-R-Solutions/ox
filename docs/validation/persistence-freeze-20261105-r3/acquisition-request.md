# Proposed bounded acquisitions — PENDING, not executed

No external access occurred in r3. Prior Iced LICENSE/manifest grant is insufficient
for every item below. These are reviewable future access requests, not execution
instructions or a standing network grant. Retain raw HTTP responses, failures,
origin/revision, UTC time and SHA-256 under the next successor's primary/ directory.
No contact with maintainers/third parties, full repository cloning, dependency update,
binary download or experiment is requested.

| Component / gap | Primary origin / revision | Intended files and method / access limit |
| --- | --- | --- |
| Iced-Icons grant and glyph chain | https://github.com/iced-rs/iced at 3997291f318a8bc06fa522f5579836fb3feb94df, graphics/fonts/ | Read-only HTTPS repository tree metadata for this directory and font-generation config/font-specific license/notice files at that commit; retain raw responses. Inspect returned config before requesting any glyph upstream. Limit 20 files, 5 MiB. No generic fontello grant assumed. |
| FiraSans 4.203 grant/notice linkage | https://github.com/mozilla/Fira (source link https://mozilla.github.io/Fira/ is in concrete archive) | Read-only HTTPS release/tag/tree metadata to identify 4.203, then LICENSE/OFL/copyright and Regular font bytes only for byte comparison. No identified immutable upstream revision yet: record resolution before file acquisition. Limit 20 files, 10 MiB; do not substitute FiraMono. |
| Cantarell 0.05 full notice linkage | https://github.com/PolyMeilex/sctk-adwaita at d5f343c45c04d4a026db57f76760819b7325db00, src/title/ | Read-only HTTPS tree and path-specific history metadata for Cantarell-Regular.ttf and adjacent notices. Limit 20 files/responses, 10 MiB. Upstream Cantarell revision/origin must first be identified; any different repository acquisition requires an additional specific request. |
| sctk borrowed portion and MPL grant | https://gitlab.com/snakedye/snui/ (exact source named at lib.rs:720; original revision unknown); https://github.com/PolyMeilex/sctk-adwaita at pinned revision above | Read-only HTTPS tree/history for rounded-headerbar code and matching original source, LICENSE and file notices including secondary-license exclusions. Limit 30 responses, 10 MiB; resolve immutable revision before retaining source. If unavailable, retain failure and keep blocker. No latest-version substitution. |
| fullscreen-shell.xml provenance | https://github.com/smithay/wayland-rs at a3d7927d87799b2955bf491b51c7c2a3a82da661, wayland-protocols-plasma; submodule origin https://github.com/KDE/plasma-wayland-protocols | Read-only HTTPS tree/submodule metadata at exact parent commit to establish Plasma revision; then exact XML, per-file license/REUSE notices and path history at resolved revision. Limit 30 responses, 10 MiB. Full COPYING.LIB already local; do not refetch as a substitute for applicability. |

Destination: a new, not-yet-created docs/validation/persistence-freeze-<successor>/primary/
with original bytes retained as .bin and explicit origin index. Approval is needed
because current authorization permits local review only and the previous grant was
limited to Iced LICENSE/manifest bytes. These requests do not themselves authorize
acquisition. Generated-output verification remains a separate execution authorization.
