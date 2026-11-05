# Plan: visual technical documentation

Full route: imported library method and bounded preservation-consumer extension.
Authority: maintainer's explicit 2026-11-04 request; existing project policies apply.

## Decisions and risks

- D-01 / REQ-01: retain the skill's technical writing/verification core; add a short visual workflow and progressive references. Alternative: one long style manual loaded for every correction; rejected for context cost. R-01: decoration displaces usable, accurate instructions.
- D-02 / REQ-02: measurable release gates for truth, legibility, contrast, typography, icons, layout and compatibility; configurable editorial budgets identified as defaults. Alternative: subjective enterprise score; rejected. R-02: aesthetic measurements misrepresented as universal standards or accessibility certification.
- D-03 / REQ-03: Mermaid is canonical for relationships; retain editable source, use render-tested SVG/PNG fallback when host cannot register icons. Chart data and screenshot provenance are mandatory when used. R-03: unrendered syntax, missing icons, misleading data or disclosure through external rendering.
- D-04 / REQ-04: separate exact-content revision registry with original skill/bridge preimages, resolved before older preservation layers. Do not overwrite historical manifests or broaden allowed paths. Keep metadata/profile unchanged. R-04: drift accepted as authorized or historical tests silently renewed.

## Selected methods

Primary: skill-creator, /home/rodrigo/.codex/skills/.system/skill-creator/SKILL.md,
no declared version/bridge, actually read; contribution: concise entry, resource
routing, appropriate scope, semantic validation. Its openai_yaml reference was read;
existing metadata remains accurate and is unchanged.
Supporting content method: technical-documentation, bridge v1 at
sdd/chain/technical-documentation.md and actual entry at
.codex/skills/technical-documentation/SKILL.md, no declared version; contribution:
source-grounded references, contract semantics and explicit rendering limitations.
Official Mermaid and W3C pages consulted for icon registration, flowchart icon
syntax, theme/accessibility and contrast; URLs/date are in the new references.
Thresholds other than cited contrast rules are local editorial defaults.

## Implementation and validation

Only the skill, its bridge, new references, a scoped preservation helper and its
two existing consumers, plus this feature/evidence are changed. Preimages in
`docs/validation/technical-documentation-visuals-20261104/before/` bind edits to
observed bytes. Shared old evidence referring to changed consumer files retains
exact historical snapshots; any new compatibility observation is separately named.
A baseline check records the preexisting README failure. Focused negative tests
must pass and current diagnostics must not add new preservation failures. The
inherited README work is not repaired through this unrelated skill change.
Review on renderer, icon pack, visual contract or preservation boundary changes.
