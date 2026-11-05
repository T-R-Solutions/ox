"""Verify maintenance preservation and reconstructible historical inputs, read-only."""
from pathlib import Path
import hashlib
import json
import tarfile
import sys
from governance_support import distribution_files, preservation_bytes, succession_errors, sha
ROOT = Path(__file__).resolve().parents[3]
BASE = 'docs/validation/maintenance-001'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def historical_bytes(root, relative, expected):
    candidates = [root/relative, root/BASE/'previous'/(relative+'.bin')]
    if relative == 'docs/structure/profile-revisions.json':
        candidates.append(root/'docs/validation/governance-reconciliation/previous/docs/structure/profile-revisions.json.bin')
    if relative == 'AGENTS.md':
        candidates.append(root/'docs/validation/governance-reconciliation/recovered/AGENTS.md.bin')
    if relative == 'docs/structure/files.json':
        candidates.append(root/'docs/validation/skill-ui-metadata/inventory-before/docs/structure/files.json')
    for path in candidates:
        if path.is_file() and digest(path.read_bytes()) == expected:
            return path.read_bytes()
    if (root/relative).is_file():
        data = preservation_bytes(root, relative)
        if digest(data) == expected:
            return data
    if relative in {'.codex/skills/prompt/agents/openai.yaml', '.codex/skills/rust/agents/openai.yaml'}:
        with tarfile.open(root/'docs/validation/adoption-baseline/copied-before-adaptation.tar.gz') as archive:
            data = archive.extractfile(relative.removeprefix('.codex/')).read()
            if digest(data) == expected:
                return data
    return None


def verify(root):
    before = json.loads((root/BASE/'before.json').read_text())
    exported = {str(p.relative_to(root)) for p in distribution_files(root)}
    errors = succession_errors(root)
    revisions = json.loads((root/'docs/structure/files.json').read_text())['revisions']
    metadata = next(r for r in revisions if r['id'] == 'skill-ui-metadata-001')
    for row in metadata['records']:
        path = root/row['destination']
        if not path.is_file() or path.is_symlink() or sha(path) != row['sha256']:
            errors.append('UI metadata changed/missing: '+row['destination'])
    preserved = 0
    for relative, record in before.items():
        if relative.startswith('dist/'):
            continue
        if historical_bytes(root, relative, record['sha256']) is None:
            errors.append('Previous bytes unavailable: '+relative)
        else:
            preserved += 1
        if relative not in exported:
            errors.append('Previously governed file excluded: '+relative)
    # Reconstruct the deduplicated governance-layout baseline using authenticated
    # retained files or maintenance originals, and archived prior versions.
    baseline = json.loads((root/'docs/validation/governance-layout/before.json').read_text())
    recovered = 0
    with tarfile.open(root/'docs/validation/governance-layout/before.tar.gz') as archive:
        members = set(archive.getnames())
        for relative, expected in baseline.items():
            data = archive.extractfile(relative).read() if relative in members else None
            if data is None:
                data = historical_bytes(root, relative, expected)
            if data is None or digest(data) != expected:
                errors.append('Layout recovery mismatch: '+relative)
            else:
                recovered += 1
    return {'errors':errors, 'preserved_governed_files':preserved,
            'recovered_layout_inputs':recovered, 'layout_input_count':len(baseline),
            'scope':'governance recovery; no product acceptance'}


if __name__ == '__main__':
    result = verify(ROOT)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(bool(result['errors']))
