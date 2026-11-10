"""Copy the governance allowlist to a new directory; never compress or publish."""
from pathlib import Path
import argparse
import json
from governance_support import copy_distribution, distribution_files, inspect_tree, sha

ROOT = Path(__file__).resolve().parents[3]


def export(root, destination):
    root = root.resolve()
    destination = destination.resolve()
    if destination == root or destination.is_relative_to(root) or destination.exists():
        raise ValueError('Destination must be a new directory outside the source tree')
    errors = inspect_tree(root)
    if errors:
        raise ValueError('\n'.join(errors))
    manifest = {str(p.relative_to(root)): sha(p) for p in distribution_files(root)}
    destination.mkdir(parents=True, exist_ok=False)
    copy_distribution(root, destination)
    actual = {str(p.relative_to(destination)): sha(p) for p in destination.rglob('*') if p.is_file()}
    if manifest != actual:
        raise ValueError('Source changed during export or copied bytes differ; preserve destination for inspection')
    (destination/'export-manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destination', type=Path)
    args = parser.parse_args()
    manifest = export(ROOT, args.destination)
    print(f'Copied {len(manifest)} governance files. No compression or publication.')
