# Script configuration centralization

REQ-01: Adapt the complete Ec script configuration organization to Ox, preserving existing local work and Ox execution contracts.
REQ-02: One declarative catalog owns scopes, scanner metadata, policy paths and execution parameters; native policies and local rules have dedicated homes.
REQ-03: Reject malformed catalogs and retain fail-closed reports, explicit Toolbox discovery, offline Cargo and reviewed exceptions.

- AC-01 → REQ-01: Reference inventory and migration disposition cover the Ec configuration surfaces.
- AC-02 → REQ-02: Plans and checks consume the central catalog with no obsolete policy copies.
- AC-03 → REQ-03: Focused regression tests pass; operational limitations remain explicit.

Authorization: explicit maintainer request on 2026-11-13 for complete local Ox script configuration refactoring using read-only Ec as reference. No commits or publication.
