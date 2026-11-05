"""Scoped method validation, exact content bindings and unchanged inherited diagnostics."""
from pathlib import Path
import importlib.util
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[3]
BASE = Path(__file__).resolve().parent
FEATURE = ROOT / 'sdd/features/technical-documentation-visuals'
spec = importlib.util.spec_from_file_location('visual_feature_validator', ROOT / 'sdd/tools/validate.py')
V = importlib.util.module_from_spec(spec)
spec.loader.exec_module(V)
document = V.strict_json(FEATURE / 'evidence.json')
rows = V.strict_json(FEATURE / 'traceability.json')
errors = V.evidence_errors(document, ROOT)
errors += V.trace_errors(rows, ROOT, FEATURE, document)
errors += V.input_errors(document, ROOT, rows, FEATURE, True)
expected = V.acceptance_ids((FEATURE / 'spec.md').read_text())
statuses = {r['id']: r['status'] for r in document['requirements']}
if any(statuses.get(key) not in ('APPROVED', 'NOT APPLICABLE') for key in expected):
    errors.append('Feature acceptance is not decided')
links = 0
for path in (ROOT / '.codex/skills/technical-documentation').rglob('*.md'):
    for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', path.read_text()):
        if '://' in target or target.startswith('#'):
            continue
        links += 1
        candidate = (path.parent / target.split('#')[0]).resolve()
        if not candidate.is_relative_to(ROOT) or not candidate.exists():
            errors.append('Broken/escaping skill link: ' + target)
command = ['python3', 'tools/governance/scripts/check-ox.py']
result = subprocess.run(command, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
(BASE / 'current-governance-check.log').write_text(result.stdout)
previous = (BASE / 'baseline-check.log').read_text()
if result.stdout != previous:
    errors.append('Governance diagnostics differ from the preserved baseline')
report = {'feature_errors': errors, 'criteria': statuses, 'skill_links_checked': links,
          'global_checker_exit': result.returncode, 'global_diagnostics_unchanged': result.stdout == previous,
          'scope': 'New method/feature bindings and no new governance diagnostics; inherited README failure is not waived.'}
(BASE / 'checks.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
raise SystemExit(bool(errors))
