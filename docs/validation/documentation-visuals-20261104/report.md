# Visual documentation review — 2026-11-04

## Scope and method

Maintainer request: redo README and linked documentation with images, Mermaid,
flowcharts, headings and the technical-documentation method. Full route extends
readme-skill-integration with REQ/AC-05. Actual technical-documentation entry and
mermaid, visual-quality, media-and-data references were read; README lifecycle
entry was read for discovery and canonical first-use ownership. No delegation.

Root README, application guide, docs index, architecture, contracts, governance and
sharing are the maintained reader surfaces. Policy/decision authorities and prior
execution records are preserved, rather than decorated or rewritten as new evidence.
No product code, dependencies, permissions, milestone or public release changes.

## Visual plan and sources

| ID | Reader question | Model / source |
| --- | --- | --- |
| overview | What are the delivered foundation's three pillars? | Original SVG with labeled Lucide icons |
| architecture | Who launches and observes which process? | Icon-based Mermaid component view, desktop/Controller/Runtime/Engine sources |
| task-cycle | How does the README summarize first use without a tall detailed flow? | Compact five-step Mermaid overview |
| first-run | Where does first use branch and how is a result accepted? | Mermaid flowchart, Controller/Engine and existing UI actions |
| execution | Why is completion distinct from verification? | Mermaid sequence, controlled producer/oracle and Engine |
| runtime-states | When is cancellation actually finished? | Mermaid state diagram, runtime reducer |
| plugin-protocol | How are echo grant and correlation enforced? | Mermaid sequence, strict host 1.0 wire contract |
| governance | Which route and evidence does a change need? | Mermaid flowchart, unchanged workflow/evidence authorities |
| sharing | What is excluded from governance export? | Mermaid scope view, existing allowlist/package receipt |
| documentation | Which document should a reader open? | Mermaid navigation map, actual maintained entry paths |
| approved/rejected | What does the actual interface look like? | Byte-identical F0 optimized-native-1-900 captures, historical 2026-11-03 observations |

No numerical chart is needed to answer these qualitative questions. No fabricated
measurements, stock photography, AI screenshots or future UI mockups are included.
Captures are copied without cropping/annotations; originals and failed observations
remain untouched. Asset sources, license and commands are in docs/assets/README.md.

## Renderer, destination and style

Destination: repository Markdown, including the user's VS Code preview. Inspected
installed extension bierner.markdown-mermaid 1.32.1 declares Mermaid 11.12.2. The
exports use Mermaid 11.12.2 and a registered local Lucide subset; native icon-pack
registration in the editor is not assumed. SVGs are the primary embed, accompanied
by source .mmd links or collapsible Mermaid fences and useful alt/captions/text.

Shared theme: docs/assets/mermaid.json. Arial/sans-serif, 18px diagram labels,
neutral surfaces, indigo component accent, teal notes and labeled verdict colors.
Lucide uses a 24-unit grid and stroke 2, with visible role names. Exports have an
opaque white surface in light and dark hosts. View/full-size links and equivalent
prose provide narrow-screen alternatives rather than shrinking all labels silently.

Local HTML preview uses markdown-it with declared CSS and Chromium 141.0.7390.37
(Playwright 1.56.1), at 360/768/1280 CSS px, light/dark, plus a documented 200% complete-document CSS zoom equivalent. It is not an inspected live VS Code
webview or a claim of browser physical-display scaling. No editor settings changed.

Tools are isolated in /tmp. Browser installation downloaded the official Chromium
archive but its automated extraction stalled after the first member. An independent
path/symlink-checked stdlib ZIP extraction of that same downloaded archive supplied
the browser executable used by the renderer; no different browser binary was fetched.
The initial render also rejected a semicolon inside a Mermaid sequence note; the
note was corrected before continuing. XML-only serialization of the state export
was normalized through an SVG-aware HTML container; figure captures then used an
HTML image embed because direct-SVG full-page capture timed out. The final exporter
inserts opaque edge-label backgrounds. The original tall overview and later wide
layout were replaced in the reader-facing architecture with a compact composition
of the same Mermaid model. Diagram labels and process-boundary crossings were
inspected and moved away from arrow text; the README cycle uses wrapped short labels. Network/sandbox and initial syntax failures
are not treated as successful rendering.

## Criteria and recorded observations

| Criterion | Method / observed inputs | Evidence and limitation |
| --- | --- | --- |
| Truth and semantic boundaries | Compare visual nodes/edges/branches, captions and claims with code and authorities | Diagram/source map above plus identified inputs; operational acceptance is not renewed |
| Source and export | Parse then render every .mmd with local icons/theme; check standalone SVG and image loading | render-results.json, exported SVGs, asset inventory and local render captures |
| Layout, typography, contrast and themes | Inspect exported figures and embedded document captures; measure palette contrast, bounds, narrow overflow, assets and headings | visual-review.json and selected reviewed captures; no usability study or WCAG certification |
| Markdown reader paths | Check current images, local links/anchors and documents, and review full-size/text alternatives | final-checks.json; remote links and exact editor webview unverified |
| Historical preservation | Exact README successor before prior layer; negative tests, independent copy and recovery | checks.json / test logs; old registries and observation hashes remain unchanged |
| No product changes | Compare application source/config identities to pre-edit snapshot | protected-inputs.json; equality is not new runtime execution evidence |

The recorded gate states/results are in visual-review.json and final-checks.json.
Absence of a recorded observation does not approve a gate. The review distinguishes
parsing, rendering, automated metrics and visual inspection. 200% review is a CSS
whole-document zoom equivalent, explicitly not a browser UI zoom/physical-display test.

## Preservation and maintenance

readme-visuals-001 records only the exact current README and its immediate preimage.
Old readme-preservation-001 and original integration manifests remain untouched.
A separate exact product-reference inventory permits only declared omitted product
references in the governance-only copy; full source trees still require local files.
Unknown README bytes, rollback and corrupt/missing/escaping metadata remain failures.

Changed documentary/tool inputs are preserved under before/ with the same hashes;
affected old evidence resolves to those preimages. New inspections and test records
identify the current inputs. Render tools, SVG/PNG identities, screenshot origin,
licenses and review observations are inventoried. No global installation, remote
editor upload, application implementation, release, commit or publication occurred.
Owner: contributor and Ox maintainer. Re-render and reexamine affected evidence on
model, source behavior, screenshot, renderer/theme/icon/font or registered-byte changes.
