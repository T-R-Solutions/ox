"""Verify maintenance preservation and reconstructible historical inputs, read-only."""
from pathlib import Path
import hashlib
import json
import tarfile
import sys
from governance_support import distribution_files
ROOT = Path(__file__).resolve().parents[3]
BASE = 'docs/validation/maintenance-001'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def verify(root):
    before = json.loads((root/BASE/'before.json').read_text())
    exported = {str(p.relative_to(root)) for p in distribution_files(root)}
    errors = []
    preserved = 0
    for relative, record in before.items():
        # Local package outputs are intentionally outside the export contract.
        if relative.startswith('dist/'):
            continue
        current = root/relative
        previous = root/BASE/'previous'/(relative+'.bin')
        if current.is_file() and digest(current.read_bytes()) == record['sha256']:
            preserved += 1
        elif previous.is_file() and digest(previous.read_bytes()) == record['sha256']:
            preserved += 1
        else:
            errors.append('Previous bytes unavailable: '+relative)
        if relative not in exported:
            errors.append('Previously governed file excluded: '+relative)
    # Reconstruct the deduplicated governance-layout baseline using authenticated
    # retained files or maintenance originals, and archived prior versions.
    baseline = json.loads((root/'docs/validation/governance-layout/before.json').read_text())
    recovered = 0
    with tarfile.open(root/'docs/validation/governance-layout/before.tar.gz') as archive:
        members = set(archive.getnames())
        for relative, expected in baseline.items():
            candidates = [root/relative, root/BASE/'previous'/(relative+'.bin')]
            data = archive.extractfile(relative).read() if relative in members else None
            if data is None:
                data = next((p.read_bytes() for p in candidates if p.is_file() and digest(p.read_bytes()) == expected), None)
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
