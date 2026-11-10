# Plan — proposed local persistence

Full route; contract adopted and isolated T009 preparation authorized; historical design sequence below is superseded by D-06. D-01: compare snapshots, journal and embedded transactions against the same seven criteria; no adoption before explicit maintainer decision. D-02: durable intent and observation/reference transaction do not make external effects atomic; reconcile stable operation identities. D-03: versioned backup/restore and bounded UI error handling are part of the slice, not optional afterthoughts. R-01: false current approval or lost acknowledged history after crash. R-02: corrupt migration/backup, competing writers or duplicate effects. R-03: dependency/FFI and unmeasured maintenance costs.

Primary selected, consulted and used: database-engineering; sdd/chain/database-engineering.md bridge_version 1; .codex/skills/database-engineering/SKILL.md has no declared version. Reference consulted: references/model-and-transactions.md. Contribution to REQ/AC-01..07: common invariants, transaction/effect boundary, writer schedules, migration and recovery alternatives. No recursive skill activation or delegation. Source versions are recorded by content in docs/validation/f0-reconciliation-20261101/inputs-final.json.

Implementation alternatives, technical source ledger, consequences and pending decision D1..D4: docs/decisions/local-persistence-proposal.md. The evaluation compares SQLite and snapshots equally; no candidate preference is retained before results. Any future chosen dependency needs pinned version/build/license review; unversioned reference pages do not establish version-specific correctness.

Sequence: prepare proposal → maintainer decision → resolve exact storage envelope/version → explicitly authorized isolated paired comparison → engine adoption and implementation authorization → implement bounded persistence → operational corpus/GUI/restore evidence → convergence. Do not execute a later step merely because this plan lists it.

D-04: the current request supersedes the earlier direct-selection option. D1..D4 in
the ADR prepare milestone, corpus, experiment grant and bounds; D5 chooses only after
results, D6 authorizes integration separately. E01..E08 cover REQ/AC-01..07; correctness
failures disqualify a candidate before performance/maintenance trade-offs. Product
acceptance still requires integrated tests. Retain database-engineering as the
primary selected/consulted/used skill (bridge 1, no declared skill version); contribution
in this follow-up: acknowledgement semantics, uncertain outcomes and matched schedules.
Current source identities and documentary review are in decision-preparation; no
storage experiment or new agent evaluation was run.


## D-05 preparation successor — 2026-11-05

Full route, existing feature reused. Read actual database-engineering entry and
references/model-and-transactions.md; primary bridge version 1, no semantic skill
version. Contribution: durable intent/effect/ack boundary, complete transactions,
unknown result/idempotency, common expected manifest and fault schedules. Rust is
selected separately for the bounded Engine repair, not a storage implementation.
The decision-ready experiment-protocol.md fixes proposed corpus/order/metrics and
D2/D3/D4/D4-deps; D1 placement is already adopted. Dependency freeze remains a
specific pre-run decision, not technology adoption. No candidate code was written.

## D-06 — adopted contract and conditional experiment, 2026-11-05

D2/D4 adopted; D3/D4-deps conditional per the authorization ADR. Full route in
this feature. T009 materializes serializer-independent corpus, verdicts, dependency
resolution and configuration review; candidate code/trials remain gated. D5 then
D6 remain separate. Primary actually read/used: database-engineering,
.codex/skills/database-engineering/SKILL.md (no declared version), bridge
sdd/chain/database-engineering.md version 1; reference model-and-transactions.md.
Contribution: stable entity/reference schema, intent/effect/ack separation, writer
lease, migration/recovery rejection rules and independent expected cases. No other
skill used in this step; no delegation. Source identities: observed-inputs.json
in docs/validation/persistence-preflight-20261105/.

Current Engine/controller sources, including preexisting edits, were inspected and
archived by bytes there. Engine after snapshots and observations are private; public
getters do not export after bytes and no import API exists. Controller uses clock
session IDs, worker-only blocking methods and volatile Engine. T009 is a neutral
contract fixture, not an implemented roundtrip adapter. Snapshot v1 and SQLite
configuration are review designs, not observed operational guarantees.

## D-07 — T009 corrective review

Full route for the explicit corrective request; primary database-engineering actually
read/used again (bridge sdd/chain/database-engineering.md version 1; entry
.codex/skills/database-engineering/SKILL.md has no declared version; reference
references/model-and-transactions.md). Contribution: independent dependency sets,
logical admission accounting, disposition/execution separation and unresolved build
mechanics. Identities are in the successor package index. No delegation.
Preserve original corpus and evidence; add scoped documentary successors only.
Review and residual gates: docs/validation/persistence-preflight-20261105/successor/review.md.

## D-08 — explicit T011 execution scope

Full route before mechanism edits, reusing this feature. Primary software-design
(.codex/skills/software-design/SKILL.md, no declared version; no configured feature
bridge): isolate project succession from the existing README preservation/visual
chain; preserve caller behavior and original checks. Supporting database-engineering
(.codex/skills/database-engineering/SKILL.md, no declared version, bridge
sdd/chain/database-engineering.md version 1): dependency/configuration review only.
Both entries actually read. Compare no change (known failure), generic succession
(unbounded scope), and one explicit content-bound transition (selected). Review
evidence and preimages are mandatory, no historical registry edits. Freeze is a
local review identity, never maintainer approval. No delegation.

## D-09 — bounded pre-execution review successor

Full route, T011/T009, preparation only under the explicit current request. No new
skill selected, consulted or used: this step compares retained primary license
bytes, graphs and documentary bindings using existing project mechanisms; it makes
no new persistence API/design choice. Earlier skill/version records are historical.
Entry state/preimages in docs/validation/persistence-freeze-20261105-r2/entry.json
and before/ precede edits. Specific upstream acquisition was explicitly authorized
in this session, limited to Iced license/manifest bytes at four archive-bound commits.
D1/D2/D4 remain adopted; D3/D4-deps conditional; D5/D6 pending.
Main Iced MIT evidence now has archive → revision → identical original manifest →
workspace member/version → retained main-text applicability chains. Font assets
receive separate review; unresolved asset grants block readiness. Historical
observations retain exact bytes; selective current documentary review and focused
governance regression replace only affected observations. No GUI replay: operational
F0 inputs remain identical. No candidate, effect supervisor, shell or trial authorized.

## D-10 — local retained-source review r3

Full route, existing T011/T009; current explicit request authorizes local documentary
review only. No new skill selected, consulted or used: archive/font/XML inspection
and existing content succession answer this step; no new persistence design or
implementation decision. Earlier skill selections/paths/versions remain historical.
Contribution: exact asset revisions, source/cfg applicability, all 30 Plasma XMLs
with file terms/full-text mappings, sctk borrowed-code scope, scanner attribution
inspection and explicit residual provenance gaps. Entry/preimages, review, local-only
resource copies and obligations are in docs/validation/persistence-freeze-20261105-r3/.
No external acquisition or delegation. D1/D2/D4 retained; D3/D4-deps conditional;
D5/D6 pending. Preparation BLOCKED; F0 operational inputs preserved.
