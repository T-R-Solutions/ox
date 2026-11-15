"""Read-only selected-feature gate using the existing SDD validator contracts."""
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[3]
FEATURE = ROOT / 'sdd/features/repository-maintenance'
loader = importlib.util.spec_from_file_location('maintenance_sdd', ROOT / 'sdd/tools/validate.py')
V = importlib.util.module_from_spec(loader)
loader.loader.exec_module(V)
document = V.strict_json(FEATURE / 'evidence.json')
rows = V.strict_json(FEATURE / 'traceability.json')
errors = V.evidence_errors(document, ROOT)
errors += V.trace_errors(rows, ROOT, FEATURE, document)
errors += V.input_errors(document, ROOT, rows, FEATURE, require_fresh=True)
expected = V.acceptance_ids((FEATURE / 'spec.md').read_text())
reported = {row['id']: row for row in document['requirements']}
for criterion in sorted(expected):
    if criterion not in reported or V.state(reported[criterion]['status']) != 'APPROVED':
        errors.append('Applicable criterion is not APPROVED: ' + criterion)
for error in errors:
    print('FAIL:', error)
if errors:
    raise SystemExit(1)
print(f'PASS: {len(expected)} selected criteria APPROVED; schema, traceability and current input bindings verified.')
print('Existing validator APIs; no feature relocation or global acceptance request. Semantic adequacy rests on recorded methods and observations.')
