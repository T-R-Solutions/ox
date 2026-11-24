"""Check current Markdown targets, anchors and self-contained documentation SVGs."""

import hashlib
import json
import re
import xml.etree.ElementTree as ET
from itertools import pairwise
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / ".local/docs-assets"
DOCS = [
    "README.md",
    "application/README.md",
    "docs/README.md",
    "docs/architecture/application.md",
    "docs/architecture/contracts.md",
    "docs/assets/README.md",
]
# F0 captures of 2026-11-03, copied byte for byte; see docs/assets/README.md.
CAPTURES = {
    "approved": "5b3c14acdf0bf4e1a174920bdd28c78f17eb26658109658d342ea75149253762",
    "rejected": "633848ef2e724fb362919c09c25d1978035532f0cd23491cf0d573caf26c532f",
}


def anchor(text):
    return "".join(c for c in text.lower() if c.isalnum() or c in "_- ").replace(
        " ", "-"
    )


def check():
    failures, links, headings, figures = [], [], [], []
    for name in DOCS:
        text = (ROOT / name).read_text()
        # Fenced Mermaid is source, not another document outline.
        prose = re.sub(r"```.*?```", "", text, flags=re.S)
        levels = [len(m[0]) for m in re.findall(r"^(#+) (.+)$", prose, re.M)]
        if any(b > a + 1 for a, b in pairwise(levels)):
            failures.append("Skipped heading level: " + name)
        headings.append({"path": name, "levels": levels})
        for raw in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
            url = urlsplit(raw.strip("<>"))
            if url.scheme or url.netloc:
                continue
            target = (
                ((ROOT / name).parent / unquote(url.path)).resolve()
                if url.path
                else ROOT / name
            )
            valid = target.is_relative_to(ROOT) and target.is_file()
            if valid and url.fragment:
                titles = re.findall(r"^#+ (.+)$", target.read_text(), re.M)
                valid = unquote(url.fragment) in [anchor(h) for h in titles]
            links.append({"source": name, "target": raw, "valid": valid})
            if not valid:
                failures.append(f"Invalid link: {name}: {raw}")
    for path in sorted((ROOT / "docs/assets").glob("*.svg")):
        svg = ET.fromstring(path.read_bytes())
        ns = "{http://www.w3.org/2000/svg}"
        title = svg.find(ns + "title")
        desc = svg.find(ns + "desc")
        rect = svg.find(ns + "rect")
        external = [
            v
            for node in svg.iter()
            for k, v in node.attrib.items()
            if k.endswith(("href", "src")) and v.startswith(("http:", "https:", "//"))
        ]
        if title is None or desc is None or not title.text or not desc.text:
            failures.append("Missing SVG accessibility: " + str(path.relative_to(ROOT)))
        if rect is None or rect.get("fill") not in ("#fff", "#ffffff", "#f8fafc"):
            failures.append(
                "Missing opaque SVG surface: " + str(path.relative_to(ROOT))
            )
        if external:
            failures.append("Remote SVG dependency: " + str(path.relative_to(ROOT)))
        figures.append(
            {
                "path": str(path.relative_to(ROOT)),
                "viewBox": svg.get("viewBox"),
                "title": title.text if title is not None else None,
                "external_refs": external,
            }
        )
    for state, expected in CAPTURES.items():
        copied = ROOT / f"docs/assets/ox-{state}.png"
        if hashlib.sha256(copied.read_bytes()).hexdigest() != expected:
            failures.append("Capture changed: " + state)
    result = {
        "links": links,
        "headings": headings,
        "figures": figures,
        "failures": failures,
    }
    BASE.mkdir(parents=True, exist_ok=True)
    (BASE / "asset-checks.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    )
    print(
        f"{len(links)} local targets/anchors, {len(figures)} SVGs; {len(failures)} failures"
    )
    for failure in failures:
        print("FAIL:", failure)
    return bool(failures)


if __name__ == "__main__":
    raise SystemExit(check())
