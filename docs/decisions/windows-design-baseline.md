# Visual Studio 2026 Enterprise visual baseline

Adopted 2026-11-17 by explicit maintainer request. DESIGN revision 5.0 makes
VISUAL STUDIO 2026 ENTERPRISE the primary visual base. Microsoft's Windows app
design guidance supports foundations and interaction, translated to Rust/Iced and
Ox domain contracts. Historical reference precedence is superseded only for visual
conflicts; identity, Plex, semantic roles and evidence history remain preserved.

Alternatives: generic Fluent would omit the requested IDE identity; literal WinUI
or screenshot cloning would import unsupported APIs/assets and ignore Ox semantics.
Adopt compositional and interaction contracts with explicit source/version and
surface mapping. Enterprise is the reference edition, not proof of exclusive styling.
No new framework/platform/dependency or runtime capability follows from this choice.

Revisit when verified reference sources change, a native translation conflicts with
accessibility/domain requirements, or the maintainer requests a new baseline.
Documented target and native acceptance remain separate. Research/dispositions:
[analysis](../design/windows-apps-analysis.md); criteria and evidence:
[feature](../../sdd/features/windows-design-baseline/spec.md).
