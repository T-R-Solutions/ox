# Plan

Full route: configuration ownership and many execution consumers change.
D-01 / R-01: Adopt Ec declarative catalog and native/rules layout, adapting its frontend, PostgreSQL and browser services as not applicable to Rust/Iced Ox. Preserve CLI scopes and existing security policy rather than copying Ec-specific exception decisions.
D-02 / R-02: Keep shell adapters and native report validation; validated data is never evaluated as shell code. Move policies, preserve their semantics and migrate callers.
D-03 / R-03: Preserve historical evidence; tests establish configuration contracts, not successful real scans or GUI acceptance.

Selected and consulted primary: software-delivery, .codex/skills/software-delivery/SKILL.md; bridge sdd/chain/software-delivery.md version 1. Contribution: input inventory, controlled execution and failure verification. Consulted references/build-inputs-and-trust.md. Actual source hashes are in the validation inventory. No delegation.
