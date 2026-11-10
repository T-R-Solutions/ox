# Pre-execution review r3 — BLOCKED

Predecessor: persistence-freeze-20261105-r2, manifest SHA-256
4ad4c04f01adf0f0a3b3ce492d6dc3bfe9d414b2d1b24842ad70f1dc3ef61c02.
Entry verification passed all 2275 files and 1388 inherited links before edits.
No later freeze was found at entry. `entry.json` records the dirty workspace;
`before/` retains exact documentary/evidence preimages. Previous package directories
are preserved. The inherited-resource map distinguishes historical bytes from current
paths; no historical verdict is renewed by assigning new input hashes.

D1/D2/D4 adopted; D3/D4-deps conditional; D5/D6 pending. T009/T011 OPEN;
AC-01..07 UNVERIFIED. F0 remains APPROVED only in its existing operational envelope.
This is a blocked review submission, not technical readiness, maintainer approval,
execution authorization or distribution clearance. No external acquisition, product
edit, candidate, encoder, effect/ack supervisor, shell, E01..E08, benchmark, fault
trial, commit or publication occurred.

| Criterion / blocker | Method and observed inputs | Favorable evidence | Counterevidence / conclusion / resumption |
| --- | --- | --- | --- |
| A1 Iced-Icons | Local archive checksum, full font name table, VCS record, text.rs and retained Linux graph; asset-matrix.json and primary-index.json | Exact font Version 1.0, FontForge ID dated 4-2-2023; archive-bound Iced commit 3997291f318a8bc06fa522f5579836fb3feb94df; unconditional include_bytes in font_system | Copyright names original authors at fontello.com but no concrete grant or glyph-source chain. Main crate MIT cannot resolve. BLOCKED: obtain font generation config, glyph origins and full applicable grants/attributions at this font revision. No binary inclusion was observed. |
| A2 FiraSans | Same archive/graph/source inspection; complete name table in asset-matrix.json | Exact Fira Sans 4.203 identifies Mozilla Foundation and Telefonica S.A., 2012–2016, with embedded OFL 1.1-or-later declaration; fira-sans enabled in graph | Full corresponding notice/grant not found in this archive. FiraMono-LICENSE is a different family and not used as proof. BLOCKED pending full original Fira Sans 4.203 notices and revision/byte linkage. Source incorporation conditional on feature; no observed binary. |
| A3 Cantarell | sctk-adwaita archive, VCS d5f343c45c04d4a026db57f76760819b7325db00, title.rs and ab_glyph_renderer.rs; font table | Exact Cantarell 0.05, FontForge ID dated 21-3-2011; Understanding Limited (2009–2011), Jakub Steiner (2010–2011); OFL 1.1 declaration on concrete font and renderer | Metadata says license copied below but contains only declaration/link, not full terms. Root MIT does not resolve font rights. BLOCKED pending matching full notices/grant. ab_glyph enabled and crossfont absent selects renderer; fallback usage depends on system font but source embeds bytes regardless. No observed binary. |
| B borrowed sctk code | Full src/lib.rs, manifest, MIT LICENSE and VCS retained as original member bytes | Warning identifies snui repository and function rounded_headerbar_shape, lines 712–771; calls and drawing context inspectable in full source | Lines 719–722 conflict with MIT-only metadata; exact original revision/function, holders and MPL grant absent. BLOCKED. Comment neither proves complete chain nor incompatibility with GPL-3.0-only. Obtain original source/notice, full MPL and any secondary-license exclusion; compare adapted portion. Do not infer entire crate is MPL or MIT. |
| C protocol XML / generated bindings | All 30 XMLs parsed locally, all module paths matched, per-file SPDX/holders/full archive license texts mapped; macro and scanner source inspected | 29 XMLs have explicit file terms and matching full text: LGPL-2.1-or-later, MIT-CMU, BSD-3-Clause, MIT. `protocol-notices.json` records each holder verbatim and complete text path/hash. client enabled; server absent. No XML removed | fullscreen-shell.xml lacks notice/terms; COPYING.LIB presence alone cannot bind it. Newly explicit material gap. Scanner parses copyright but no generator use was found in any .rs member: no automatic attribution assumed. BLOCKED overall pending this file's provenance/terms and disposition of generated-code obligations. |
| Documentary succession | Compare old bindings to exact before bytes; review changed paragraphs, statuses and actual retained primary inputs | No operational contract, product source, manifest or dependency change; selective current observation with preserved historical bindings | `freshness-impact.json` identifies affected consumers. Old results remain historical; new observation covers only documentary delta. No GUI reexecution needed when operational inputs are unchanged. |
| Freeze / resources | Manifest enumerates files, local-only archives/payload copies and inherited preimages; SHA verification | Local resources copied into resources/.local, primary-index records original archive members. `verify-freeze.py` verifies manifest, path containment, hashes and inherited map | Hashes prove identity only. Preserve the whole manifest resource closure when sharing; isolated Git checkout is insufficient. See checks.json and freeze-verification.log for actual observations. |

## Applicability, obligations and limits

`asset-matrix.json` retains the full r2 asset inventory and adds exact archive/revision,
font revision strings and source/feature distinctions for the three blocked fonts.
Other test assets remain recorded as test/archive material, not observed embedding.
All source files of the four reviewed crates are retained byte-for-byte with `.bin`
suffixes to prevent upstream documentation links from becoming local project rules.
Original source paths, origins and SHA-256 are in primary-index.json. Acquisition
history for inherited archives remains in the predecessor; r3 only reads local bytes.

`obligations.json` and `protocol-notices.json` are the attribution inventory. Full
texts, including COPYING.LIB and LICENSES, are retained; extracted holders and
summaries do not replace them. MIT/MIT-CMU require preservation of applicable
copyright/permission notices; BSD requires source/binary notice reproduction and no
endorsement. LGPL portions require their own license/source/change and combination
disposition; own GPL-3.0-only does not erase these terms. The retained LGPL 2.1
section 3 provides a GPL conversion mechanism and the file identifiers permit later
LGPL versions, but no blanket conversion or whole-package compatibility approval is
made: missing fullscreen provenance and actual generated/source packaging must be
resolved first. MPL compatibility depends on original grant and secondary-license
conditions, unavailable here. Root own-material GPL is never used to relicense assets.
These are bounded source-based interpretations; distribution has not been reviewed.

Macro invocation exposes every mapped protocol module under client generation,
including fullscreen_shell. No per-protocol exclusion feature was found. Scanner
uses CARGO_MANIFEST_DIR to read XML for interfaces/client macros. This demonstrates
inputs/mechanism by inspection; compilation, expanded output, linking and effective
binary notices require later explicitly authorized work. Source-level absence of
copyright propagation warrants separate retained attribution even if bindings are
later generated. It does not prove the generated code is free of XML license duties.

## Maintainer review and exact resumption

Review the five unresolved source/grant chains and the new fullscreen-shell gap;
review the distinction between file terms mapped (29 XMLs) and effective generated
attribution/compatibility (not established). Requested future acquisitions are
specified in acquisition-request.md; no access was attempted or authorized by r3.
Primary files may instead be supplied locally with provenance. Resume by retaining
original bytes/revision/method/time/SHA, comparing exact font or adapted-source
identities and recording positive and negative results, then issuing a new successor.
If provenance cannot be established, retain the block; do not exclude components.
Only after material gaps are resolved can T009/T011 closure and a technically ready
package be considered. Maintainer review approval must bind that concrete freeze;
implementation and trials require separate explicit authorization, followed later by
D5 and D6. Real ENOSPC also retains its separate grant requirement.
