"""Create a new local package, inspect it and smoke-test a clean extraction."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import zipfile
from governance_support import (distribution_files, inspect_bytes, inspect_tree, sha,
                                PACKAGE_NAME, governance_scope, scope_errors)

ROOT = Path(__file__).resolve().parents[3]


def create_archive(root, package):
    """Serialize the actual governance boundary and scope into a new ZIP."""
    paths = distribution_files(root)
    manifest = {p.relative_to(root).as_posix():sha(p) for p in paths}
    scope = governance_scope()
    if scope_errors(scope):
        raise ValueError('Invalid governance package scope')
    with zipfile.ZipFile(package, 'x', compression=zipfile.ZIP_DEFLATED) as archive:
        for path in paths:
            archive.write(path, path.relative_to(root).as_posix())
        archive.writestr('package-manifest.json', json.dumps(manifest, indent=2)+'\n')
        archive.writestr('package-scope.json', json.dumps(scope, indent=2)+'\n')
    return manifest, scope


def main():
    output = ROOT/'dist'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    output.mkdir(parents=True, exist_ok=False)
    errors = inspect_tree(ROOT)
    if errors:
        (output/'inspection-errors.json').write_text(json.dumps(errors, indent=2)+'\n')
        print('\n'.join(errors))
        return 1
    package = output/PACKAGE_NAME
    manifest, scope = create_archive(ROOT, package)
    fingerprints = json.loads((ROOT/'docs/validation/governance-externalization/external-fingerprints.json').read_text())
    errors = inspect_bytes(package.name, package.read_bytes(), fingerprints)
    if errors:
        (output/'inspection-errors.json').write_text(json.dumps(errors, indent=2)+'\n')
        print('\n'.join(errors))
        return 1
    commands = [
        ['sdd/tools/validate.py','--root','.'],
        ['sdd/tools/validate.py','--root','.','--structure-only'],
        ['tools/governance/scripts/check-ox.py'],
        ['-m','unittest','discover','-s','tools/governance/tests','-v'],
        ['tools/governance/scripts/run-checks.py'],
    ]
    results = []
    with tempfile.TemporaryDirectory(prefix='ox-package-') as temporary:
        extracted = Path(temporary)/'ox'
        extracted.mkdir()
        with zipfile.ZipFile(package) as archive:
            # Archive was inspected for links, traversal and content before extraction.
            archive.extractall(extracted)
        actual = {p.relative_to(extracted).as_posix():sha(p) for p in extracted.rglob('*')
                  if p.is_file() and p.relative_to(extracted).as_posix()
                  not in {'package-manifest.json', 'package-scope.json'}}
        if actual != manifest:
            raise ValueError('Extracted inventory differs from package manifest')
        extracted_scope = json.loads((extracted/'package-scope.json').read_text())
        if extracted_scope != scope or scope_errors(extracted_scope):
            raise ValueError('Extracted package scope differs from governance receipt')
        for index, args in enumerate(commands, 1):
            command = [sys.executable,'tools/governance/scripts/isolated-run.py',str(ROOT),*args]
            process = subprocess.run(command, cwd=extracted,
                env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1', OX_ISOLATION_ORIGIN=str(ROOT)),
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            log = output/f'{index:02}.log'
            log.write_text(process.stdout)
            results.append({'command':'PYTHONDONTWRITEBYTECODE=1 python3 '+' '.join(args),
                            'exit_code':process.returncode,'log':log.name,'sha256':sha(log)})
            print(f'{index}/5 exit={process.returncode}: '+ ' '.join(args), flush=True)
        # Preserve the runner's new evidence from the disposable extraction.
        observed = output/'extracted-runs'
        observed.mkdir()
        for run in (extracted/'docs/validation/runs').iterdir():
            if not (ROOT/'docs/validation/runs'/run.name).exists():
                import shutil
                shutil.copytree(run, observed/run.name)
    unchanged = manifest == {p.relative_to(ROOT).as_posix():sha(p) for p in distribution_files(ROOT)}
    result = {**scope, 'package':package.name,'sha256':sha(package),'file_count':len(manifest)+2,
              'archive_inspection':'PASS','manifest_and_extraction':'PASS',
              'source_unchanged_during_build':unchanged,'results':results,
              'isolation':'Python audit hook rejects original parent and external document reads; not an OS sandbox'}
    (output/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('Governance package evidence (no application):',output.relative_to(ROOT))
    return int(not unchanged or any(row['exit_code'] for row in results))


if __name__ == '__main__':
    sys.exit(main())
