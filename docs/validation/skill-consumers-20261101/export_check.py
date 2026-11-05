"""Copy governed bytes and check them with source access denied by the existing audit oracle."""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys
import tempfile
root = Path.cwd().resolve()
out = Path(sys.argv[1]).resolve()
out.mkdir()
sys.path.insert(0, str(root / 'tools/governance/scripts'))
from governance_support import copy_distribution, distribution_files
parent = Path(tempfile.mkdtemp(prefix='ox-consumer-export-'))
dest = parent / 'export'
dest.mkdir()
manifest = {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in distribution_files(root)}
copy_distribution(root, dest)
assert not (dest / 'application').exists()
assert all(hashlib.sha256((dest / p).read_bytes()).hexdigest() == sha for p, sha in manifest.items())
commands = [
    ['sdd/tools/validate.py', '--root', '.', '--require-fresh'],
    ['sdd/tools/validate.py', '--root', '.', '--structure-only'],
    ['tools/governance/scripts/check-ox.py'],
    ['tools/governance/scripts/verify-maintenance.py'],
    ['-m', 'unittest', 'discover', '-s', 'tools/governance/tests', '-p', 'test_technical_acceptance.py', '-v'],
    ['docs/validation/skill-consumers-20261101/acceptance_check.py'] + (['--delivery'] if '--delivery' in sys.argv else []),
]
checks = []
for i, command in enumerate(commands):
    invocation = [sys.executable, 'tools/governance/scripts/isolated-run.py', str(root), *command]
    run = subprocess.run(invocation, cwd=dest, env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'), capture_output=True, text=True, timeout=90)
    log = out / f'export-{i}.log'
    log.write_text(run.stdout + run.stderr)
    checks.append({'command': invocation, 'exit': run.returncode, 'artifact': log.name})
receipt = {'destination': str(dest), 'manifest': manifest, 'checks': checks,
           'application_present': False,
           'limit': 'The Python audit hook observes stdlib file access and is not an OS security boundary. Native consumer execution occurred separately, not in this export.'}
(out / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
print([(c['artifact'], c['exit']) for c in checks])
raise SystemExit(any(c['exit'] for c in checks))
