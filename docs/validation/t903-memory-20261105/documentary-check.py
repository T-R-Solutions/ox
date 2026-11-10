from pathlib import Path
import json,re,hashlib,collections
r=Path(__file__).resolve().parents[3];b=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();paths=set();results=[]
source=r/'docs/validation/f0-reconciliation-20261101/skill-t004.json';rows=json.loads(source.read_text());paths.add(source)
assert len(rows)==36 and set(collections.Counter(x['feature'] for x in rows).values())=={4}
for x in rows:
 base=r/'sdd/features'/x['feature'];spec=base/'spec.md';tasks=base/'tasks.md';ep=base/'evidence.json';paths.update([spec,tasks,ep]);doc=json.loads(ep.read_text())
 q=next(q for q in doc['requirements'] if q['id']==x['criterion'])
 assert q['status']==x['recorded_status']=='APPROVED'
 assert re.search(r'(?m)^- (?:'+re.escape(x['criterion'])+r')(?:\s*→|:)',spec.read_text())
 assert re.search(r'\[x\].*\bT004\b',tasks.read_text(),re.I)
 for key in ['consumer','oracle','review']:
  p=r/x[key];assert p.is_file(),p;paths.add(p)
 for e in x.get('execution',[]):
  p=r/e['artifact'];assert sha(p)==e['sha256'];paths.add(p)
 results.append({'feature':x['feature'],'criterion':x['criterion'],'status':'APPROVED','scope':'documentary consistency only; no replay of historical consumer execution'})
mp=r/'docs/validation/f0-resumption-20261103/matrix.json';m=json.loads(mp.read_text());assert len(m['requirements'])==20;paths.add(mp)
p=r/'sdd/features/product-local-persistence/evidence.json';pd=json.loads(p.read_text());assert len(pd['requirements'])==7 and all(q['status']=='UNVERIFIED' for q in pd['requirements']);paths.add(p)
paths.update(r/'sdd/features/product-local-persistence'/n for n in ['spec.md','plan.md','tasks.md','converge.md','traceability.json','experiment-protocol.md'])
paths.update(r/n for n in ['docs/decisions/local-persistence-proposal.md','docs/validation/t903-20261105/persistence-decisions.md','docs/validation/t903-20261105/documentary-review.md'])
assert all(x['identical'] for x in json.loads((b/'predecessor-product-comparison.json').read_text()))
result={'scenario_consistency':results,'f0_clauses':20,'persistence':'7 UNVERIFIED, proposal only, no candidate implementation','preservation':'77/77 resumption product preimages equal; historical binding resolver and freshness checks required separately','inputs':[{'path':str(p.relative_to(r)),'sha256':sha(p),'role':'other'} for p in sorted(paths)]}
(b/'documentary-checks.json').write_text(json.dumps(result,indent=2)+'\n');print('36 documentary records,20 F0 clauses and7 pending persistence criteria inspected; no borrowed product approval')
