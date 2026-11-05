from pathlib import Path
import json,hashlib,datetime
R=Path(__file__).resolve().parents[3];B=Path(__file__).resolve().parent;G=R/'docs/validation/f0-reconciliation-20261101/resumption-authority';G.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,obj):p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def bind(paths):return [{'path':str(p.relative_to(R)),'sha256':sha(p),'role':'other'} for p in sorted(set(paths))]
assert json.loads((B/'observation-checks.json').read_text())['status']=='APPROVED'
# Preserve all prior envelopes before modifying their historical references.
archives={}
for item in json.loads((B/'predecessors.json').read_text()):
 src=R/item['snapshot'];assert sha(src)==item['sha256'];dest=G/'before'/(item['path']+'.bin');dest.parent.mkdir(parents=True,exist_ok=True)
 if not dest.exists():dest.write_bytes(src.read_bytes())
 assert sha(dest)==item['sha256'];archives[item['sha256']]=dest
(G/'review.md').write_text('''# Bounded documentary and export successor review

The current delta adopts the explicitly confirmed F0 GUI budgets and records the
operational conclusion in project/architecture authorities. It does not authorize
new roadmap work, storage implementation, publication or a skill-to-product verdict
transfer. Historical project, decision and feature bytes remain under before/.

The governance helper gains exactly one product-record exclusion, for the new F0
resumption evidence directory, under the already adopted product/governance export
boundary. Its preservation/succession/archive routines are unchanged. The existing
export regression gains one assertion: it fails before the predicate change and
passes afterward. Other tests and consumer implementations remain byte-identical.

This scoped semantic review preserves the previous criterion verdicts affected by
these shared documentary/helper inputs. It is not a replay of their historical
executions. Old input hashes are retained and redirected only to identical archived
bytes. Current declared contracts/implementation/oracle inputs are bound separately.
No operational product evidence is required in the governance-only export. Final
checks of current bindings, preservation, negative controls and independent export
are recorded in the resumption checks; operational F0 acceptance is a separate
product feature and is not transferred to library authoring or older releases.
''')
# Retain the regression evidence within the self-contained governance boundary.
for name in ['export-before.log','export-after.log']:(G/name).write_bytes((B/name).read_bytes())
product_names={'product-f0-gate','product-bootstrap','product-plugin-host','product-verification-engine','product-local-task-ui'}
changed=[];documents=[]
for p in (R/'sdd/features').glob('*/evidence.json'):
 doc=json.loads(p.read_text());stale=[]
 for e in doc['evidence']:
  for x in e.get('inputs',[]):
   source=R/x['path']
   if source.is_file() and sha(source)==x['sha256']:continue
   assert x['sha256'] in archives,(p,x)
   stale.append(x['path']);x['path']=str(archives[x['sha256']].relative_to(R))
 if not stale and p.parent.name not in product_names:continue
 old=G/'envelopes'/(p.parent.name+'.json.bin');old.parent.mkdir(exist_ok=True);assert not old.exists();old.write_bytes(p.read_bytes())
 changed.append({'feature':p.parent.name,'changed_inputs':sorted(set(stale)),'prior_envelope':str(old.relative_to(R))})
 documents.append((p,doc))
write(G/'impact.json',changed)
# Compare every inherited acceptance input; only enumerated document/helper changes are allowed.
old_inputs=json.loads((R/'docs/validation/f0-execution-20261102/inputs-acceptance.json').read_text())['inputs'];delta=[]
for item in old_inputs:
 p=R/item['path']
 if sha(p)!=item['sha256']:
  assert item['sha256'] in archives,item
  delta.append(item['path'])
assert not any(x.startswith('application/') for x in delta),delta
write(B/'final-input-comparison.json',{'checked':len(old_inputs),'changed':delta,'application_changes':[],'method':'compare exact current bytes to inherited acceptance manifest; explicit successor review only for changed documents and export helper/test'})
# Hash raw observed evidence, source snapshots and current contracts; avoid envelope/cyclic hashes.
paths={R/x['path'] for x in old_inputs}
paths.update(p for p in (R/'application/crates').rglob('*') if p.is_file())
paths.update([R/'application/Cargo.toml',R/'application/Cargo.lock',R/'application/rust-toolchain.toml',R/'.codex/skills/observability-and-diagnostics/SKILL.md',R/'.codex/skills/observability-and-diagnostics/references/hypothesis-and-evidence.md'])
paths.update(p for p in B.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name not in {'inputs-final.json','checks-final.json'} and 'before' not in p.relative_to(B).parts)
inputs=bind(paths);write(B/'inputs-final.json',{'scope':'New observation and selective reexamination; source/product identities unchanged, historical runs not replayed by rehashing. Raw times retained.','observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'inputs':inputs})
for p,doc in documents:
 name=p.parent.name;needed={p.parent/x for x in ['spec.md','plan.md','tasks.md','traceability.json']}
 for row in json.loads((p.parent/'traceability.json').read_text()):needed.update([R/row['implementation'],R/row['oracle']])
 if name in product_names:
  artifact=B/'report.md';identifier='E-F0-RESUMPTION'
  record={'id':identifier,'kind':'inspection','command_or_method':'Current clause review plus correlated primary/native graphical runs, 12 metric cells, 36 X11 cases, three native and three covered-X11 held cases; exact raw artifact check and inherited-input comparison. Visual review recorded separately.','observed_result':'F0 bounded graphical/measurement blockers supported; adopted limits met. Product source/lockfile unchanged. Original failures retained, isolated versus primary session and client versus physical-presentation limits explicit.','artifact':str(artifact.relative_to(R)),'sha256':sha(artifact),'inputs':inputs+bind(needed-paths)+bind([B/'inputs-final.json'])}
  if name=='product-f0-gate':
   for c in doc['requirements']:c['status']='APPROVED'
  if name=='product-bootstrap':next(c for c in doc['requirements'] if c['id']=='AC-02')['status']='APPROVED'
  if name=='product-local-task-ui':
   for c in doc['requirements']:
    if c['id'] in ['AC-05','AC-10','AC-11']:c['status']='APPROVED'
 else:
  identifier='E-F0-RESUMPTION-DOCUMENTARY';artifact=G/'review.md'
  needed.update([R/'tools/governance/scripts/governance_support.py',R/'tools/governance/tests/test_governance.py',R/'sdd/project.md',R/'docs/architecture/context.md',R/'docs/decisions/f0-boundary-20261102.md',G/'export-before.log',G/'export-after.log'])
  record={'id':identifier,'kind':'inspection','command_or_method':'Review exact shared documentary/export delta against unchanged criterion consumers; retain old hashes and identical predecessors. Regression assertion fails before and passes after the bounded export exclusion.','observed_result':'Existing scoped verdicts retained; no new consumer execution or product approval inferred. Current contracts and actual implementation/oracle identities reexamined; obsolete observations remain historical.','artifact':str(artifact.relative_to(R)),'sha256':sha(artifact),'inputs':bind(needed)}
 assert not any(e['id']==identifier for e in doc['evidence'])
 doc['evidence'].append(record)
 for c in doc['requirements']:c.setdefault('evidence_ids',[]).append(identifier)
 write(p,doc)
print('Bound successor records for',len(documents),'features;',len(inputs),'observed inputs;',len(delta),'document/helper changes; zero application changes')
