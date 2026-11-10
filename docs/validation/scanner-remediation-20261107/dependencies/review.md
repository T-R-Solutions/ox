# Dependency and license review checkpoint

The real two-crate reproducer distinguishes an inherited local path without a
version requirement from the same path with `version="=0.1.0"`. Deny 0.20.2 emits
both wildcard and bug diagnostics in the first case (exit 2); the second passes
(exit 0). Adding matching exact requirements to the three existing Ox local paths
removes both wildcard diagnostics and the internal diagnostic. Product run:
`.local/checks/security-4ckvhee9/assessment.json`: exit 6, 177 findings, no internal
error. No third-party version, graphical feature or lockfile was changed.

The remaining Deny findings are 165 license-policy diagnostics and 12 duplicate
families. The original `deny-inventory.json` retains their detailed dependency
chains and locations. `license-sources.json` inventories each registry package,
its declared expression, available license/NOTICE paths and missing local sources.
Expressions with OR require an explicit choice; AND obligations accumulate.
The empty allowlist records absent approval, not established legal incompatibility.
The maintainer explicitly kept approval pending inventory review.

Review preparation for notices: retain copyright and permission notices for
[MIT](https://spdx.org/licenses/MIT.html); retain source notices and reproduce the
required materials for binary distribution under
[BSD-2-Clause](https://spdx.org/licenses/BSD-2-Clause.html). For
[Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0), review license delivery,
modified-file notices, retained attribution and applicable NOTICE contents.
These are review prompts, not a complete compatibility determination or permission
to ship. Other expressions, exceptions, Unicode data, bundled fonts, and nine
unavailable registry sources still need individual examination. No allowlist or
blanket duplicate exception was added.

`ttf-parser@0.25.1` enters through fontdb/cosmic-text/Iced and through
owned_ttf_parser/ab_glyph/sctk-adwaita/winit. `pin-utils@0.1.1` enters the lockfile
through wasmtimer and iced_futures; the installed iced_futures manifest restricts
wasmtimer to wasm32. Native Linux inverse-tree inspection prints nothing for
pin-utils. The all-target offline query could not resolve uncached js-sys; this is
not evidence that the warning is absent. Both RustSec warnings remain enabled.
No forced transitive update or graphics-stack upgrade was attempted.

Duplicate-family chains span Iced, Wayland calloop/smithay generations, font stacks
and proc-macro generations. Different major versions cannot be assumed compatible.
Any proposed exception must identify individual crate/version pairs, upstream
constraints, deployment impact and an upstream convergence/update review trigger.
No exception is approved by this checkpoint; compatible unification remains open.
