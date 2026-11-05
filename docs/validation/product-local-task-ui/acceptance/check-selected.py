"""Apply the existing validator's structural/freshness/acceptance checks to selected features."""
from pathlib import Path
import importlib.util,json
root=Path(__file__).resolve().parents[4]
spec=importlib.util.spec_from_file_location('sdd_validator',root/'sdd/tools/validate.py')
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
features=['product-local-task-ui','governance-reconciliation','skill-ui-metadata-inventory','product-bootstrap','product-plugin-host','product-agent-runtime','product-verification-engine']
results=[]
for name in features:
 feature=root/'sdd/features'/name
 doc=v.strict_json(feature/'evidence.json');rows=v.strict_json(feature/'traceability.json')
 errors=v.evidence_errors(doc,root)+v.trace_errors(rows,root,feature,doc)+v.input_errors(doc,root,rows,feature,True)
 expected=v.acceptance_ids((feature/'spec.md').read_text())
 for req in doc['requirements']:
  if req['id'] in expected and v.state(req['status']) not in {'APPROVED','NOT APPLICABLE'}:errors.append('Unaccepted '+req['id'])
 results.append(dict(feature=name,criteria=len(expected),errors=errors))
print(json.dumps(dict(method='Existing validator evidence_errors, trace_errors, input_errors(require_fresh=True), and declared-criterion acceptance gate; not semantic proof.',results=results),indent=2))
raise SystemExit(int(any(r['errors'] for r in results)))
