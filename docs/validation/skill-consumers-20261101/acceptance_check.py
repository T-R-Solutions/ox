"""Check current nine-skill acceptance without changing their original feature paths."""
from pathlib import Path
import importlib.util
import json
import sys
root = Path.cwd().resolve()
sys.path.insert(0, str(root / 'tools/governance/scripts'))
import technical_acceptance
spec = importlib.util.spec_from_file_location('sdd_validator', root / 'sdd/tools/validate.py')
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)
errors = validator.audit(root, require_fresh=True)
count = 0
for name in json.loads((root / 'config/governance/profile.json').read_text())['new']:
    feature = root / 'sdd/features' / ('skill-' + name)
    document = validator.strict_json(feature / 'evidence.json')
    rows = validator.strict_json(feature / 'traceability.json')
    errors += technical_acceptance.technical_errors(root, feature, document, rows, validator)
    expected = validator.acceptance_ids((feature / 'spec.md').read_text())
    assert len(expected) == 6
    for requirement in document['requirements']:
        if requirement['id'] in expected:
            count += 1
            if validator.state(requirement['status']) != 'APPROVED':
                errors.append(name + '/' + requirement['id'] + ' is not APPROVED')
assert count == 54
if '--delivery' in sys.argv:
    delivery = json.loads((root / 'sdd/features/skill-consumer-validation/evidence.json').read_text())
    assert len(delivery['requirements']) == 4
    errors += [q['id'] + ' delivery pending' for q in delivery['requirements'] if q['status'] != 'APPROVED']
for error in errors:
    print(error)
print(f'{"FAIL" if errors else "PASS"}: {count} skill criteria, schema/content bindings and technical execution reviews. Scope remains each evaluated consumer.')
raise SystemExit(bool(errors))
