# ADR — Visual documentation delivery

Adopted for the maintainer's 2026-11-04 request to redo README and its references
with images, Mermaid, flowcharts and the technical-documentation method.

D-01: use real, unchanged F0 captures with visible provenance and date. Explain
components with a Lucide icon architecture view, behavior with flow/sequence/state
models and governance with its own route/export diagrams. Keep qualitative views
source-grounded; no invented measurements, features or screenshots.

D-02: repository Markdown is the delivery surface. The inspected local VS Code
Mermaid extension 1.32.1 declares Mermaid 11.12.2. Use that Mermaid version in the
isolated local rendering tool. SVG exports are primary embedding, with opaque light
surfaces in either host theme, full-size links, captions and equivalent text. Keep
.mmd sources, theme config and offline Lucide paths/license. Ordinary Mermaid
sources are also in collapsible fences. Icon-pack registration is provided by the
exporter, not assumed in the user's editor. Local HTML previews do not establish
actual VS Code webview behavior. No editor settings are changed.

D-03: add only the exact README visual successor ahead of readme-preservation-001.
Preserve its registry, original integration records and all historical hashes.
Register updated exact product-reference source bytes separately, retaining the
old reference inventory. Unknown current mutations, rollback, missing/corrupt or
escaping preimages and malformed registries continue failing. Reexamine affected
shared documentary evidence without replaying unchanged product measurements.

Alternatives rejected: Mermaid fences alone as visual delivery; generated UI
images as runtime evidence; unlicensed mixed icons; a blanket broken-link waiver;
renewing old digests in place; global render dependency installation. No application
or policy changes, release, upload, publication or agent delegation.

Review when a figure's source/model, screenshot, export dependencies, source
reference inventory or registered README bytes change. Current acceptance is in
readme-skill-integration AC-05 and the visual review artifacts.
