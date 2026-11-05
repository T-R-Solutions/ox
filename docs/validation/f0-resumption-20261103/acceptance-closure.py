"""Use the repository validator on the three affected features, plus negative controls."""
import pathlib,importlib.util,json,copy,datetime
B=pathlib.Path(__file__).resolve().parent;R=B.parents[2]
s=importlib.util.spec_from_file_location('validator',R/'sdd/tools/validate.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
result={'observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'features':[],'limits':['schema/hash validation does not establish authenticity or oracle suitability; operational and visual evidence reviewed separately']}
for name in ['product-f0-gate','product-bootstrap','product-local-task-ui']:
 f=R/'sdd/features'/name;doc=v.strict_json(f/'evidence.json');rows=v.strict_json(f/'traceability.json')
 errors=v.evidence_errors(doc,R)+v.trace_errors(rows,R,f,doc)+v.input_errors(doc,R,rows,f,True)
 expected=v.acceptance_ids((f/'spec.md').read_text());states={c['id']:c['status'] for c in doc['requirements'] if c['id'] in expected}
 errors += [f'{c}: {state}' for c,state in states.items() if state not in ['APPROVED','NOT APPLICABLE']]
 assert not errors,(name,errors)
 mutant=copy.deepcopy(doc);mutant['evidence'][-1]['inputs'][0]['sha256']='0'*64
 stale=v.input_errors(mutant,R,rows,f,True);assert any('Stale input' in e for e in stale)
 mutant=copy.deepcopy(doc);mutant['requirements'][0]['evidence_ids']=[]
 missing=v.evidence_errors(mutant,R);assert missing
 result['features'].append({'name':name,'states':states,'current_schema_trace_inputs':'PASS','changed_input_negative_control':'REJECTED as expected','missing_evidence_negative_control':'REJECTED as expected'})
(B/'acceptance-closure.json').write_text(json.dumps(result,indent=2)+'\n');print('Three affected features: current acceptance bindings PASS; changed-input/missing-evidence controls rejected')
