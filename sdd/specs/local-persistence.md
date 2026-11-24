# Spec — local-persistence

Spec viva da capacidade `local-persistence`. Migrada em 2026-11-23 da feature `product-local-persistence` do modelo
anterior (título original: "Proposed local persistence for the existing controlled task flow"). Texto original preservado; ACs marcados
`(herdado)` mantêm o estado registrado até 2026-11-23, mas a evidência bruta foi removida e
não sustenta nova aprovação. A task que tocar a capacidade reescreve o AC na forma
`| método: … | esperado: …` e o reavalia. As limitações técnicas foram mantidas; as notas de
controle de evidência do modelo anterior, não.

## O quê e por quê

Status: D2 contract and D4 experiment parameters adopted on 2026-11-05; T009 preparation authorized. D3 comparison and D4-deps review are conditional on pre-run freeze/review. Product implementation and engine selection are NOT authorized. Actor: local user; owner: maintainer. Full route due to persisted state, recovery, concurrency and unresolved contract decisions. Requirements below express the adopted common contract; operational acceptance remains UNVERIFIED.

Scope: durable task/attempt/check/verification history for product-local-task-ui; integration through ox-storage, ox-verification and the existing controller/Iced flow after authorization. Preserve local policy, provenance and all five states. Do not scan/reconstruct arbitrary .ox-task directories as trusted history.

Exclusions: remote agents/network/sync, graph/FTS/search, marketplace, generalized orchestration, automatic task replay, secrets/encryption guarantees, hostile writers, other OS targets, automatic deletion and public release. These exclusions do not waive missing-evidence or corruption handling. Power-loss durability requires a separately adopted model and observation.

Dependencies: explicit maintainer scope/implementation decision; already adopted post-F0/pre-MVP placement; engine/driver/version/configuration and dependency review; selected local directory/filesystem, quota/retention, bounded busy/recovery/UI deadlines (proposed defaults and directory/quota in ADR, not yet adopted); versioned serialization contract; accepted product-local-task-ui/Engine/runtime APIs. Proposed fault corpus and mechanism comparison are in docs/decisions/local-persistence-proposal.md. No commands for nonexistent persistence tests are claimed.

Each criterion must record initial store/fixture, exact engine/driver/source/configuration/FS, command, fault point, expected/observed values, artifact and limitations. Independent expected histories are authored before implementation. The same corpus applies to snapshots, journal and embedded database; a schedule model is not actual storage execution. Missing implementation leaves all criteria UNVERIFIED.

### Comparative preparation constraint

Adopted milestone assignment (F0 boundary ADR): independent delivery after F0 and
before F3/MVP. This placement does not authorize implementation. The common E01..E08 protocol and selection rule
in the ADR apply equally to SQLite and snapshots. Contract/corpus/operational bounds
precede experiments; comparative results precede technology selection. Journal is a
documented alternative only. D3 conditionally grants the disposable experiment after freeze/review; this step grants preparation only and no integration.
Prototype evidence cannot alone approve these seven product criteria.

Effective authority: docs/decisions/local-persistence-experiment-20261105.md. Adopted D4 experimental quotas are distinct from the Engine logical 128 MiB limit; no retained-byte deduplication changes admission. No OS/power-loss/hostile-writer/remote-sync guarantee.

### T011 succession contract

Governance must authenticate the original README integration and each reviewed
project-state transition by exact content; unknown current bytes, ambiguous records,
missing/corrupt preimages and escaping/symlinked paths must fail closed. No path
allowlist or mere preimage existence grants acceptance. Freeze preparation inputs
including local-only resources; material license gaps block technical readiness.

### Boundary clarification — audit correction 2026-11-17

The implementation prohibition here concerns general product/task/evidence storage.
It does not revoke the separately authorized product-visual-workbench WC-02/03
recent-project metadata snapshot in ox-ui/src/desktop/project_store.rs (at most
20 canonical recent paths). That convenience store does not select D5/D6 or accept
the AC-01–07 criteria of this feature. Moving its ownership to ox-storage would be a separate
architectural change; this correction makes no such migration.

## Requisitos

- REQ-01: Stable durable identity and complete provenance.
- REQ-02: Recover safely without replaying uncertain effects.
- REQ-03: Current acceptance follows current inputs.
- REQ-04: Recoverable schema evolution.
- REQ-05: Consistent portable local backup.
- REQ-06: Bounded observable storage failures in Iced.
- REQ-07: Writer authority and idempotency.

## Critérios de aceitação

- AC-01 → REQ-01: Across two separate processes, task/attempt/check/observation/history round-trip with identical identities, arguments, expected result and before/after content identities; unknown remains distinct from zero/missing. Oracle: independent expected manifest, not serializer output. (herdado)
- AC-02 → REQ-02: Run clean restart and kills before/after intent, after effect, before/after commit acknowledgement; truncate/corrupt owned copies. Oracle: expected acknowledged histories, no invented approval/relaunch, preserved damaged bytes and explicit interrupted state within adopted durability envelope. (herdado)
- AC-03 → REQ-03: After restart change one input, oracle, arguments or criterion independently; only dependent acceptance becomes stale. Missing evidence never approves. Exercise all five states, including justified inapplicability. Oracle: independent verdict/dependency table with negative controls. (herdado)
- AC-04 → REQ-04: Old/current/future schemas, interrupted upgrade and rejected downgrade preserve recoverable original bytes; no partial migrated visibility. Oracle: independent version/entity manifest and before/after original-byte comparison. (herdado)
- AC-05 → REQ-05: While a writer is active, produce a consistent store+evidence manifest; restore into a fresh directory/process and compare expected entities/provenance, marking missing/changed external inputs stale. Incomplete/tampered backup fails visibly without overwriting originals. Oracle: independent manifest and restored-state query. (herdado)
- AC-06 → REQ-06: Permission denied, disk full, corrupt/unavailable store and bounded busy/restore failures remain visible; UI interaction/heartbeat continues within adopted bound; no silent volatile approval. Oracle: injected real storage errors plus independent graphical/heartbeat observation. (herdado)
- AC-07 → REQ-07: Two actual processes race to write the same store; second writer obeys adopted exclusion/deadline. Same operation+payload is one result, conflicting payload is rejected; lost acknowledgement resolves durable ID without executing effect twice. Oracle: independent operation/effect counter and recorded interleaving. (herdado)

## Estado atual

| AC | Estado | Decidido por (task) | Data |
|---|---|---|---|
| AC-01 | UNVERIFIED | modelo anterior (herdado) | ≤ 2026-11-23 |
| AC-02 | UNVERIFIED | modelo anterior (herdado) | ≤ 2026-11-23 |
| AC-03 | UNVERIFIED | modelo anterior (herdado) | ≤ 2026-11-23 |
| AC-04 | UNVERIFIED | modelo anterior (herdado) | ≤ 2026-11-23 |
| AC-05 | UNVERIFIED | modelo anterior (herdado) | ≤ 2026-11-23 |
| AC-06 | UNVERIFIED | modelo anterior (herdado) | ≤ 2026-11-23 |
| AC-07 | UNVERIFIED | modelo anterior (herdado) | ≤ 2026-11-23 |
| T009-PREFLIGHT | INCONCLUSIVE | modelo anterior (herdado) | ≤ 2026-11-23 |

## Limites e questões abertas

- D2/D4 adopted; D3/D4-deps conditionally authorized. T009 preparation and isolated acquisition do not validate product storage; D5/D6 pending.
- Traceability implementation points to an exact source-inspection snapshot of the empty storage boundary; oracle points to the proposed expected-result contract, not an executable test. Replace with authorized real implementation/oracles before acceptance.
