"""Bind a new acceptance review while retaining exact historical inputs and envelopes."""
from pathlib import Path
import hashlib,json,datetime
R=Path(__file__).resolve().parents[3];B=Path(__file__).resolve().parent;G=R/'docs/validation/f0-reconciliation-20261101/resumption-authority'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,o):p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
def bind(paths):return [{'path':str(p.relative_to(R)),'sha256':sha(p),'role':'other'} for p in sorted(set(paths))]
assert json.loads((B/'optimized-checks.json').read_text())['status']=='APPROVED'
assert all(x['exit']==0 for x in json.loads((B/'optimized-product-checks.json').read_text())['checks'])
archives={}
for root in [B/'before',G/'before',G/'before-history-review',G/'before-closure']:
 for p in root.rglob('*'):
  if p.is_file():archives[sha(p)]=p
review=G/'closure-review.md'
review.write_text('''# Documentary successor after full-history counterevidence

The provisional F0 conclusion was withdrawn when complete history draw times
exceeded the adopted budget. Current project/architecture authorities now record
the bounded package-only tiny-skia dev optimization and new twelve-cell validation.
No first-party product source, dependency version, lockfile, protocol, persistence
scope or authorization changed. Existing governance helper/test bytes are unchanged
from the previously verified exact product-record exclusion.

Review of the changed authority text preserves each independent governance
criterion's scope and verdict. It does not transfer product test outcomes into
skill consumers, authorize another roadmap phase or claim historical observations
were replayed. Historical hashes below point to identical archived bytes. Current
contracts and implementation/oracle identities are bound separately. Product raw
captures remain excluded from governance-only distribution. Full governance tests
were already executed after the actual helper/test change; current document/input
and export-boundary checks are rerun for this successor.
''')
products={'product-f0-gate','product-bootstrap','product-plugin-host','product-agent-runtime','product-verification-engine','product-local-task-ui'}
documents=[];impact=[]
for p in (R/'sdd/features').glob('*/evidence.json'):
 doc=json.loads(p.read_text());stale=[]
 for e in doc['evidence']:
  for x in e.get('inputs',[]):
   q=R/x['path']
   if q.is_file() and sha(q)==x['sha256']:continue
   assert x['sha256'] in archives,(p,x)
   stale.append(x['path']);x['path']=str(archives[x['sha256']].relative_to(R))
  if e.get('artifact') and sha(R/e['artifact'])!=e['sha256']:
   assert e['sha256'] in archives,(p,e['artifact'])
   stale.append(e['artifact']);e['artifact']=str(archives[e['sha256']].relative_to(R))
 if not stale and p.parent.name not in products:continue
 snapshot=G/'closure-envelopes'/(p.parent.name+'.json.bin');snapshot.parent.mkdir(exist_ok=True);assert not snapshot.exists();snapshot.write_bytes(p.read_bytes())
 impact.append({'feature':p.parent.name,'changed_input_paths':sorted(set(stale)),'prior_envelope':str(snapshot.relative_to(R))});documents.append((p,doc))
write(G/'closure-impact.json',impact)
# Bind the newly observed corpus and relevant unchanged sources. Earlier raw records
# stay bound in their historical envelopes; avoid circular hashes of evidence/check outputs.
paths={R/x['path'] for x in json.loads((B/'optimized-build-inputs.json').read_text())['product_inputs']}
paths.update([R/'sdd/project.md',R/'docs/architecture/context.md',R/'docs/decisions/f0-boundary-20261102.md',R/'docs/decisions/open-questions.md',R/'tools/governance/scripts/governance_support.py',R/'tools/governance/tests/test_governance.py'])
for p in B.iterdir():
 if p.is_file() and (p.name.startswith(('optimized-','check-optimized','prepare-optimized','history-counter','raster-profile')) or p.name in ['report.md','matrix.json','graphical-review.md','reproduce.md','reconcile-closure.py','acceptance-closure.py']):paths.add(p)
for pattern in ['optimized-native-*','optimized-x11-*','optimized-separated-x11-*','optimized-original-*','optimized-backend*-workspace']:
 for folder in B.glob(pattern):
  if folder.is_dir():paths.update(p for p in folder.rglob('*') if p.is_file())
inputs=bind(paths);manifest=B/'inputs-closure.json';assert not manifest.exists();write(manifest,{'observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Current package-only rasterizer profile and affected graphical corpus; historical inputs preserved, no assertion that rehashing reexecutes tests.','inputs':inputs})
for p,doc in documents:
 name=p.parent.name;needed={p.parent/x for x in ['spec.md','plan.md','tasks.md','traceability.json']}
 for row in json.loads((p.parent/'traceability.json').read_text()):needed.update([R/row['implementation'],R/row['oracle']])
 if name in products:
  identifier='E-F0-RASTER-CLOSURE';artifact=B/'report.md'
  record={'id':identifier,'kind':'inspection','command_or_method':'Review full-history counterevidence, bounded tiny-skia dev-profile correction, twelve separately observed graphical cells, raw maximum/client/resource checks, ordinary workspace checks, current clause matrix and preserved input identity. See optimized-checks.json and graphical-review.md.','observed_result':'All applicable F0 clauses supported in the adopted bounded corpus; full-history frame limits met after correction. Prior provisional closure withdrawn and preserved. Historical unchanged domain/security/coverage observations reused by scope, not represented as reruns.','artifact':str(artifact.relative_to(R)),'sha256':sha(artifact),'inputs':inputs+bind(needed-paths)+bind([manifest])}
  if name=='product-f0-gate':
   for c in doc['requirements']:c['status']='APPROVED'
  if name=='product-bootstrap':next(c for c in doc['requirements'] if c['id']=='AC-02')['status']='APPROVED'
  if name=='product-local-task-ui':
   for c in doc['requirements']:
    if c['id'] in ['AC-05','AC-10','AC-11']:c['status']='APPROVED'
 else:
  identifier='E-F0-RASTER-DOCUMENTARY';artifact=review
  needed.update([R/'sdd/project.md',R/'docs/architecture/context.md',R/'docs/decisions/f0-boundary-20261102.md',R/'tools/governance/scripts/governance_support.py',R/'tools/governance/tests/test_governance.py'])
  record={'id':identifier,'kind':'inspection','command_or_method':'Bounded semantic review of current F0 authority text and unchanged criterion consumers; exact old bytes preserved.','observed_result':'Existing governance verdict and authorization scope retained; no product acceptance inferred from documentary checks.','artifact':str(artifact.relative_to(R)),'sha256':sha(artifact),'inputs':bind(needed)}
 assert not any(e['id']==identifier for e in doc['evidence']);doc['evidence'].append(record)
 for c in doc['requirements']:c.setdefault('evidence_ids',[]).append(identifier)
 write(p,doc)
print('Successor bound:',len(documents),'features;',len(inputs),'current observed inputs')
