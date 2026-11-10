from pathlib import Path
import importlib.util,json,copy
r=Path(__file__).resolve().parents[3];b=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('validator',r/'sdd/tools/validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
results=[]
for name in ['product-f0-gate','product-local-task-ui','product-verification-engine']:
 p=r/'sdd/features'/name;d=json.loads((p/'evidence.json').read_text());rows=json.loads((p/'traceability.json').read_text())
 def errors(doc):return v.evidence_errors(doc,r)+v.trace_errors(rows,r,p,doc)+v.input_errors(doc,r,rows,p,True)
 actual=errors(d);assert not actual,(name,actual)
 expected=v.acceptance_ids((p/'spec.md').read_text());assert all(q['status'] in ['APPROVED','NOT APPLICABLE'] for q in d['requirements'] if q['id'] in expected)
 bad=copy.deepcopy(d);bad['evidence'][-1]['inputs'][0]['sha256']='0'*64;assert errors(bad),'changed input must fail'
 bad=copy.deepcopy(d);bad['evidence']=[x for x in bad['evidence'] if x['id']!=d['evidence'][-1]['id']];assert errors(bad),'missing evidence must fail'
 results.append({'feature':name,'current_schema_trace_freshness':'PASS','acceptance_states':{q['id']:q['status'] for q in d['requirements']},'changed_input_negative_control':'REJECTED as expected','missing_evidence_negative_control':'REJECTED as expected'})
(b/'acceptance.json').write_text(json.dumps(results,indent=2)+'\n');print('All three feature gates/current bindings and negative controls pass')
