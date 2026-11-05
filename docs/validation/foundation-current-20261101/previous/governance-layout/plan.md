# Plan — governance organization

Full route: the change reaches the distribution allowlist, preservation guards
and evidence consumers. Authorization: the maintainer's request in this session.
Baseline without Git in docs/validation/governance-layout/before.tar.gz and
before.json, captured before edits; the original check-ox passed.

| ID | Decision / risk | Relationship |
| --- | --- | --- |
| D-01 | Scripts and tests in tools/governance/; fixtures under tests/; profile and coverage in config/governance/ | REQ-01, REQ-02 |
| D-02 | Update Python roots, commands and traceability; preserve SDD methods and skills; dedicated ADR documents historical paths | REQ-02, REQ-04 |
| D-03 | Explicit allowlist for tools/governance/ and config/governance/, removing src/ | REQ-03 |
| D-04 | Archive old envelopes; reexamine affected criteria; translate only paths when comparing historical traceability | REQ-04 |
| R-01 | Incorrect Python root or fixture treated as configuration | REQ-01, REQ-02 |
| R-02 | Stale path or guard weakened by migration | REQ-02, REQ-04 |
| R-03 | Package includes application or omits necessary configuration | REQ-03 |
| R-04 | Recycling old result hashes or promoting scenarios without implementation | REQ-04 |

Primary skill selected, consulted and used: software-delivery,
`.codex/skills/software-delivery/SKILL.md`; version not declared by the entry;
bridge `sdd/chain/software-delivery.md`, bridge_version 1. Contribution:
define artifact inputs and boundaries, adjust the allowlist, check ZIP identity
and run existing commands in an independent extraction. No promotion, publication,
installation or need for supporting skills/delegation.

Rejected alternative: generic scripts/ and tests/ at the root would scatter
governance-specific tools. Keeping src/ in the allowlist could include future
application sources. Copying the profile into fixtures would duplicate a current authority.

Preservation: profile and fixtures retain their bytes; coverage updates the oracle
and GOV-04 hash after correcting the profile link without changing policy.
Historical records in docs/validation/, revisions and old ADRs remain intact.
The original guard accepts only the same profile at its new destination and
deterministic path translation in traceability JSON, compared against original
baseline bytes. Any other change to those contracts continues to fail.

Recovery: copy the distribution into an empty directory, check the 384 unchanged
files in recovery.json against before.json, then overlay the 55 previous versions
from before.tar.gz; compare the set of 439 inputs. The archive contains only
changed/moved versions to avoid duplicating historical archives and exceeding the
128 MiB recursive inspection budget. The original full copy remains in
dist/governance-layout-recovery/, outside distribution and unnecessary for recovery.
Before selectively restoring into the working tree, preserve unexpected versions.
Do not overwrite the whole tree.
Acceptance: existing tests, focused guard mutations, mapping inspection, continuity
review, freshness and an independent package. Inputs and outputs from new observations
are recorded separately without circular hashes.
