"""Check current Markdown targets, anchors and self-contained documentation SVGs."""
from pathlib import Path
from urllib.parse import urlsplit, unquote
import hashlib
import json
import re
import unicodedata
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / 'docs/validation/documentation-visuals-20261104'
DOCS = ['README.md', 'application/README.md', 'docs/README.md',
        'docs/architecture/application.md', 'docs/architecture/contracts.md',
        'docs/development/governance.md', 'docs/development/sharing.md',
        'docs/assets/README.md']


def anchor(text):
    return ''.join(c for c in text.lower() if c.isalnum() or c in '_- ').replace(' ', '-')


def check():
    failures, links, headings, figures = [], [], [], []
    for name in DOCS:
        text = (ROOT / name).read_text()
        # Fenced Mermaid is source, not another document outline.
        prose = re.sub(r'```.*?```', '', text, flags=re.S)
        levels = [len(m[0]) for m in re.findall(r'^(#+) (.+)$', prose, re.M)]
        if any(b > a+1 for a,b in zip(levels, levels[1:])):
            failures.append('Skipped heading level: '+name)
        headings.append({'path':name,'levels':levels})
        for raw in re.findall(r'\[[^\]]*\]\(([^)]+)\)', text):
            url = urlsplit(raw.strip('<>'))
            if url.scheme or url.netloc: continue
            target = ((ROOT/name).parent/unquote(url.path)).resolve() if url.path else ROOT/name
            valid = target.is_relative_to(ROOT) and target.is_file()
            if valid and url.fragment:
                titles = re.findall(r'^#+ (.+)$', target.read_text(), re.M)
                valid = unquote(url.fragment) in [anchor(h) for h in titles]
            links.append({'source':name,'target':raw,'valid':valid})
            if not valid: failures.append(f'Invalid link: {name}: {raw}')
    for path in sorted((ROOT/'docs/assets').glob('*.svg')):
        svg = ET.fromstring(path.read_bytes())
        ns = '{http://www.w3.org/2000/svg}'
        title = svg.find(ns+'title'); desc = svg.find(ns+'desc')
        rect = svg.find(ns+'rect')
        external = [v for node in svg.iter() for k,v in node.attrib.items()
                    if k.endswith(('href','src')) and v.startswith(('http:','https:','//'))]
        if title is None or desc is None or not title.text or not desc.text:
            failures.append('Missing SVG accessibility: '+str(path.relative_to(ROOT)))
        if rect is None or rect.get('fill') not in ('#fff','#ffffff','#f8fafc'):
            failures.append('Missing opaque SVG surface: '+str(path.relative_to(ROOT)))
        if external: failures.append('Remote SVG dependency: '+str(path.relative_to(ROOT)))
        figures.append({'path':str(path.relative_to(ROOT)),'viewBox':svg.get('viewBox'),
                        'title':title.text if title is not None else None,'external_refs':external})
    for state in ('approved','rejected'):
        source = ROOT/f'docs/validation/f0-resumption-20261103/optimized-native-1-900/{state}.png'
        copied = ROOT/f'docs/assets/ox-{state}.png'
        if source.read_bytes() != copied.read_bytes(): failures.append('Capture changed: '+state)
    result={'links':links,'headings':headings,'figures':figures,'failures':failures}
    (BASE/'asset-checks.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(f'{len(links)} local targets/anchors, {len(figures)} SVGs; {len(failures)} failures')
    for failure in failures: print('FAIL:',failure)
    return bool(failures)


if __name__ == '__main__':
    raise SystemExit(check())
