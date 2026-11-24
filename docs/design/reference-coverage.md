# Reference disposition and design trace

This successor records source-level trace separately from native implementation.
The member inventory in `docs/design/reference-members.json`
identifies every file/member by bytes and marks duplicates. Type classification is
not a claim that every historical screenshot has been visually inspected.

## Decisions

- Preserve v4 broader operational model and v3 detailed legacy roles in English.
- Keep Plex. v3 explicitly calls Inter/JetBrains a proposal; no conflict permits migration.
- Preserve all legacy_r12 values. Direction B remains proposed; do not color code categories by status.
- No automatic imports of HTML/CSS/JS, historical reports or browser test quotas into native runtime.
- Do not reproduce unavailable backend actions; do implement useful preview geometry and selection.
- No wholesale icon/font copying: current embedded Plex has checked OFL provenance;
  remaining prototype icons are candidates, not cleared distribution assets.
- Duplicate R10/R11 and duplicate external skill entries require no second integration.

## Composition disposition

| Source family | Contribution | Native consumer / boundary |
|---|---|---|
| R1 vocabulary; R2 master | file navigation, primary artifact, context inspection | document_view: embedded file tree, tabs, code, inspector, tools |
| R2 architecture | directional relation map and provenance | relationship_map: Cargo dependencies, responsive stacking; no graph engine |
| R2 agents | separate roles and instances | agent_roles: responsibility table; instances explicitly unavailable |
| R2 observability | units, provenance, missing values | observability_view: unavailable metrics; no invented series |
| R3 review/recovery/focus | diff symbols, uncertain effects, focus mode | existing labelled diff, recovery and focused document composition |
| R4 projects/tasks | task-first entry and creation boundary | actual local task; general project/task services remain unavailable |
| R5 administration | session preferences and provider boundaries | themes/densities; remote provider connection remains disabled |
| R6–R9 runtime/stress/exports | state and overflow fixtures | native keyboard/capture harness; browser runtime not embedded |
| R10/R11 | duplicate content | retain provenance once; no duplicate code/assets |
| R12 refinements/icons | optical/semantic reference | restrained roles; full icon set remains a candidate |
| Nine reference PNGs / montage | region hierarchy | primary workbench, inspection, roles and map translated selectively |
| R13 | controlled chromatic experiment | proposal retained; no silent default adoption |

## Source heading trace

Line numbers refer to standalone v3 or archive member ox-design-system/DESIGN.md
for v4. `reference-clauses.json` additionally indexes source bullet/emphasis clauses;
this is documentary trace, not independent semantic acceptance of every clause.

| Source section | Maintained DESIGN.md destination |
|---|---|
| v3:13 1. Visual Theme & Atmosphere | 2 Identity; 15 references |
| v3:19 Key Characteristics | 2 Identity; 15 references |
| v3:31 Comparative References (Documented Facts vs. Ox Decisions) | 2 Identity; 15 references |
| v3:43 2. Color Palette & Roles | 4 Color roles; 5 tokens |
| v3:47 Primary — Ox Signature Blue (Mandatory Preservation) | 4 Color roles; 5 tokens |
| v3:60 Secondary & Accent — Technical Domains | 4 Color roles; 5 tokens |
| v3:70 Surface & Background | 4 Color roles; 5 tokens |
| v3:84 Neutrals & Text | 4 Color roles; 5 tokens |
| v3:98 Semantic & Accent — Green, Amber/Yellow, and Red | 4 Color roles; 5 tokens |
| v3:127 Gradient System | 4 Color roles; 5 tokens |
| v3:133 Token Architecture — Implementable Light Baseline | 4 Color roles; 5 tokens |
| v3:229 Dark Theme — Dedicated Tokens, Not Automatic Inversion | 4 Color roles; 5 tokens |
| v3:262 High Contrast | 4 Color roles; 5 tokens |
| v3:266 Contrast & Accessibility Rules | 4 Color roles; 5 tokens |
| v3:286 3. Typography Rules | 6 Typography; 5 independent editor theme |
| v3:288 Font Family | 6 Typography; 5 independent editor theme |
| v3:298 Hierarchy | 6 Typography; 5 independent editor theme |
| v3:314 Principles | 6 Typography; 5 independent editor theme |
| v3:323 Note on Font Substitutes | 6 Typography; 5 independent editor theme |
| v3:340 Editor Syntax — Separate from Shell Theming | 6 Typography; 5 independent editor theme |
| v3:346 4. Component Stylings | 8 Components |
| v3:348 Buttons | 8 Components |
| v3:360 Cards & Containers | 8 Components |
| v3:369 Inputs & Forms | 8 Components |
| v3:377 Navigation | 8 Components |
| v3:386 Image Treatment | 8 Components |
| v3:390 Signature Components | 8 Components |
| v3:405 Interaction State Matrix | 8 Components |
| v3:425 5. Layout Principles | 7 Geometry |
| v3:427 Spacing System | 7 Geometry |
| v3:433 Grid & Container | 7 Geometry |
| v3:449 Whitespace Philosophy | 7 Geometry |
| v3:453 Border Radius Scale | 7 Geometry |
| v3:468 6. Depth & Elevation | 7 Geometry / restrained depth |
| v3:480 Decorative Depth | 7 Geometry / restrained depth |
| v3:488 7. Do's and Don'ts | 14 Blocking failures |
| v3:490 Do | 14 Blocking failures |
| v3:502 Don't | 14 Blocking failures |
| v3:516 8. Responsive Behavior | 7 Adaptive behavior; 10 accessibility |
| v3:520 Breakpoints (Test Ranges, Not Mandatory Hardcoded Values) | 7 Adaptive behavior; 10 accessibility |
| v3:531 Touch Targets / Pointer Targets | 7 Adaptive behavior; 10 accessibility |
| v3:537 Collapsing Strategy | 7 Adaptive behavior; 10 accessibility |
| v3:545 Image / Graph / Diff Behavior | 7 Adaptive behavior; 10 accessibility |
| v3:554 9. Agent Prompt Guide | 12 Review; 13 handoff; examples remain non-normative |
| v3:556 Quick Color Reference | 12 Review; 13 handoff; examples remain non-normative |
| v3:575 Example Component Prompts | 12 Review; 13 handoff; examples remain non-normative |
| v3:583 Iteration Guide | 12 Review; 13 handoff; examples remain non-normative |
| v3:596 Quality Gates / Acceptance Criteria | 12 Review; 13 handoff; examples remain non-normative |
| v3:613 Known Gaps / Provenance | 12 Review; 13 handoff; examples remain non-normative |
| v3:623 Official Reference Links | 12 Review; 13 handoff; examples remain non-normative |
| v4:10 0. Contrato de autoridade — LEIA PRIMEIRO | 1 Authority |
| v4:23 0.1. Como utilizar esta especificação | 1 Authority |
| v4:32 1. Identidade, propósito e princípio estético | 2 Identity |
| v4:38 1.1. Princípios inegociáveis | 2 Identity |
| v4:52 1.2. Adaptação de Taste Skill e Impeccable para uma IDE | 2 Identity |
| v4:66 2. Modelo de experiência, autoridade funcional e linguagem de estados | 3 Truth states |
| v4:68 2.1. Entidades visuais | 3 Truth states |
| v4:85 2.2. Matriz canônica de comunicação | 3 Truth states |
| v4:108 2.3. Modelo de evidência visível | 3 Truth states |
| v4:112 3. Sistema cromático — regras de papéis | 4 Color roles |
| v4:114 3.1. Assinatura Ox Signature Blue (`LOCKED` — Light) | 4 Color roles |
| v4:143 3.2. Superfícies neutras e hierarquia | 4 Color roles |
| v4:154 3.3. Cores semânticas (papéis invariantes) | 4 Color roles |
| v4:166 3.4. Cores de contexto técnico (PROPOSED) | 4 Color roles |
| v4:176 3.5. Direções A/B/C para R13 — não confundir recomendação com aprovação | 4 Color roles |
| v4:188 3.6. Sintaxe, dados e status nunca se fundem | 4 Color roles |
| v4:195 4. Arquitetura dos tokens e dos temas | 5 Token architecture |
| v4:209 4.1. API visual de referência (CSS de protótipo, NÃO Iced) | 5 Token architecture |
| v4:224 5. Tipografia e linguagem editorial | 6 Typography |
| v4:226 5.1. Posição sobre fontes — conflito histórico resolvido com evidência | 6 Typography |
| v4:233 5.2. Escala lógica proposta | 6 Typography |
| v4:251 5.3. Conteúdo e microcopy | 6 Typography |
| v4:255 6. Geometria, densidade, alinhamento e profundidade | 7 Geometry |
| v4:275 6.1. Densidade | 7 Geometry |
| v4:279 6.2. Layout adaptativo desktop | 7 Geometry |
| v4:292 7. Sistema de componentes — contrato de cada família | 8 Components |
| v4:296 7.1. Chrome e navegação | 8 Components |
| v4:305 7.2. Botões, inputs, menus e modais | 8 Components |
| v4:315 7.3. Componentes de engenharia | 8 Components |
| v4:333 7.4. Iconografia | 8 Components |
| v4:337 7.5. Grafos, tabelas e visualizações | 8 Components |
| v4:344 8. Layout e composição por superfície | 9 Surface coverage |
| v4:346 8.1. Master Operational Workbench (W00) | 9 Surface coverage |
| v4:362 8.2. Regras por tela/destino | 9 Surface coverage |
| v4:387 9. Temas: Light, Dark e High Contrast | 5 Themes |
| v4:389 9.1. Light | 5 Themes |
| v4:393 9.2. Dark | 5 Themes |
| v4:397 9.3. High Contrast | 5 Themes |
| v4:401 9.4. Editor independente | 5 Themes |
| v4:405 10. Acessibilidade, ergonomia e internacionalização | 10 Accessibility |
| v4:419 11. Movimento, feedback, performance e resiliência visual | 11 Resilience |
| v4:427 12. Gate de design: diagnóstico → execução → repetição | 12 Review protocol |
| v4:429 Gate 0 — inventário e prova de baseline | 12 Review protocol |
| v4:436 Gate 1 — direção controlada e contrato de componente | 12 Review protocol |
| v4:443 Gate 2 — implantação no protótipo e neutralidade funcional | 12 Review protocol |
| v4:450 Gate 3 — QA multidimensional | 12 Review protocol |
| v4:467 Gate 4 — loop até resolução mensurável | 12 Review protocol |
| v4:473 12.1. Definição de pronto por mudança de UX/UI | 12 Review protocol |
| v4:477 13. Roadmap de execução R13+ (não é relatório de implementação) | 9 Planned surfaces; roadmap is not implementation |
| v4:493 14. Política de arquivos, manutenção e responsabilidades | 13 Maintenance |
| v4:517 14.1. Interfaces com a engenharia | 13 Maintenance |
| v4:521 14.2. Responsabilidades e revisão humana | 13 Maintenance |
| v4:531 15. Fontes, diferenças e lacunas conhecidas | 1 Provenance; 15 references |
| v4:533 15.1. Materiais do usuário | 1 Provenance; 15 references |
| v4:541 15.2. Referências externas verificáveis (princípios, **não assets para copiar**) | 1 Provenance; 15 references |
| v4:550 15.3. Limitações transparentes na emissão v4.0.0 | 1 Provenance; 15 references |
| v4:558 16. Resumo normativo — 12 vetos de aprovação | 14 Blocking failures |

## Start-screen source disposition — 2026-11-14

R4 `welcome-first-1x.png` contributes existing-folder entry and local-context
inspection; `welcome-returning-1x.png` contributes resumption semantics. R12's
`r11-start-center-light-comfortable-1440x900.png` and
`r10-start-smaller-920x620.png` refine compact selection/context composition.
The actual source members and hashes are recorded with the start-screen evidence.
Only the currently validated session is shown. Fictional recent projects, dates,
branches, decisions and agents are excluded. Native typography/neutral roles and
narrow stacking follow DESIGN; source hero sizing and two-column narrow geometry
are not copied. Images were inspected as references, not embedded in the product.

## IDE welcome reference successor — 2026-11-14

The maintainer identified JetBrains IntelliJ IDEA and supplied a native welcome
screenshot, /tmp/pasted-image-.png, SHA-256
64a5901d7c862240c763e0010e2b69aee8125dd7cdc8bd7bb4c7926f510ab663.
Root and coordinator inspected the image: neutral project navigation, concise
welcome text and grouped start/open actions inform S01 organization. The product
version and interactive behavior are not established by the screenshot. Clone,
remote-development entries, branded assets and onboarding promotion are not adopted.
R4/R12 remain inspiration for hierarchy; DESIGN owns roles, fonts and themes.
Recent rows now require actual successful-open metadata under the newly authorized
welcome contract; fictional projects remain excluded. No pixel-identical copy claimed.

## Definitive identity integration — 2026-11-16

The supplied `.local/assets/definitivo/README.md` and `prancha.png` were inspected.
Identity revision identidade-definitiva-01 selects Catalisador v2 study 06,
Valência v1 study 01 and the cotton mascot v5 study 17, with approved Ferris tag
revision algodao-etiqueta-vetorial-05. S01 embeds byte-identical `logo-escuro.png`,
`logo-branco.png` and `mascote-ox.png`; proportions, negative space and alpha remain
intact. No source board, historical study, generator or `.local` path is loaded
at runtime. Signature layout is preserved inside the artwork; its integration
adapts to the native project-entry geometry rather than reproducing the board's
informational captions. The mascot is raster; no vectorization/animation is claimed.
Source/copy SHA-256 values are listed in the
[embedded identity README](../../application/crates/ox-ui/assets/identity/README.md).

## Enterprise desktop reference successor — 2026-11-16

The two newly supplied IntelliJ Home captures show the same structural direction:
window-filling context bar, slim navigation, docked project actions/recents, expansive
neutral workspace and discreet status/tools. The maintainer contrasts these with
the rejected Ox floating welcome card. Adopt hierarchy, restrained density and
docked layout across native presentation; preserve DESIGN palette and IBM Plex.
Third-party branding, clone/remote/terminal effects and unknown interaction behavior
are not imported. Definitive OX assets remain intact with a compact signature and
secondary mascot. Version and runtime behavior cannot be inferred from captures.

## Windows / Visual Studio successor — 2026-11-17

The maintained [Windows design analysis](windows-apps-analysis.md) inventories
consulted sources, topics, dispositions and remaining limits. It supplies the
source trace for DESIGN revision 5.0 and the windows-design-baseline SDD feature.

| Reference | Disposition | Boundary |
| --- | --- | --- |
| VISUAL STUDIO 2026 ENTERPRISE | mandatory primary visual base by explicit request | IDE shell/workspace hierarchy; no edition-exclusive visual claims |
| Windows app design / Fluent | supporting principles, foundations, controls, interaction and accessibility | translated to Rust/Iced and actual target platforms |
| R2–R13 and previous enterprise/IntelliJ references | historical/supporting, subordinate in visual conflicts | retain domain details, identity provenance and observed evidence |
| WinUI/XAML/API samples and Windows shell integrations | implementation-specific, deferred where no Ox capability exists | no dependency or platform adoption |
| Microsoft fonts/icons/material samples | reference only unless separately licensed/adopted | retain Plex and Ox assets |

Every affected visual task must identify its actual source/version, surface/component,
adoption or justified adaptation, and future native evidence. Documentary coverage
does not establish visual, interaction or accessibility parity.

## Identity and implementation correction — 2026-11-17

The identity/enterprise entries above record their dated observations. The current
UI embeds only the two signature PNGs at 128×40 logical units; the mascot remains
historical artwork. S01 has a fixed 280-unit action column, 210 below 900, with
Plugins docked at the bottom and projects scrolling independently. S09/S13 share
a cog: 27 destinations use 26 geometries. S13/S14 share the settings canvas and
have no Details specimens. See the audit correction report for checks and limits.
The IntelliJ temporary screenshot path above is historical acquisition metadata;
its hash identifies the earlier input but that temporary path is not a retained
reproduction source. It is not a build or current acceptance dependency.
