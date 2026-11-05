"""Preserve historical envelopes and reexamine only this integration's input delta."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[3];B=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
archives={x['sha256']:R/x['snapshot'] for x in json.loads((B/'before.json').read_text())}
# Save all envelopes first, so cross-feature references can never depend on loop order.
for p in (R/'sdd/features').glob('*/evidence.json'):
 q=B/'envelopes'/(p.parent.name+'.json.bin');q.parent.mkdir(exist_ok=True);assert not q.exists();q.write_bytes(p.read_bytes());archives[sha(q)]=q
review=B/'shared-input-review.md'
review.write_text('''# Scoped shared-input review

Criteria/method: examine each stale input against its exact preimage, changed
contract and actual consumer; preserve all historical input/artifact digests.
The reviewed delta adds one conditional README lifecycle skill and bridge; older
skills/bridges and their scoped consumer implementations are unchanged. General
technical-documentation keeps standalone manuals/references. Current profile is31
entries, while earlier counts remain historical at their original observations.

The source consumer changes only layer this exact19-path revision before existing
preservation checks and recognize its enumerated imported resources. Unknown
current bytes are never translated to an approved predecessor. Scope, hash,
missing/corrupt paths, symlinks and traversal are exercised by the new regression
cases; previous suites retain their original behavioral oracles. The SDD validator,
five states, minimum evidence bindings and specialization gates are unchanged.

README/project/catalog changes describe availability and current accepted F0 status;
they authorize no new product feature or phase. Application sources, toolchain,
lockfile, support matrix, graphical environment observations and acceptance limits
are untouched by this integration. F0 runtime/security/coverage/performance evidence
is retained only for its unchanged product inputs, not replayed by documentary checks.

Result: retain existing scoped criterion states. Historical adoption/authoring and
metadata observations remain historical; the new31-entry profile is independently
accepted in readme-skill-integration, not asserted as the old profile. No skill or
new README claim inherits product runtime approval. Documentary review establishes
scope and identity only, not scientific effectiveness, new reader studies or GUI
behavior. First independent-export failure and draft correction remain in attempt-1.
''')
changes=[]
for p in (R/'sdd/features').glob('*/evidence.json'):
 d=json.loads(p.read_text());stale=[]
 for e in d['evidence']:
  for x in e.get('inputs',[]):
   q=R/x['path']
   if q.is_file() and sha(q)==x['sha256']:continue
   assert x['sha256'] in archives,(p,x)
   stale.append(x['path']);x['path']=str(archives[x['sha256']].relative_to(R))
  if e.get('artifact') and sha(R/e['artifact'])!=e['sha256']:
   assert e['sha256'] in archives,(p,e['artifact'])
   stale.append(e['artifact']);e['artifact']=str(archives[e['sha256']].relative_to(R))
 if not stale:continue
 needed={p.parent/x for x in ['spec.md','plan.md','tasks.md','traceability.json']}
 for row in json.loads((p.parent/'traceability.json').read_text()):needed.update([R/row['implementation'],R/row['oracle']])
 needed.update(R/x for x in ['config/governance/profile.json','docs/structure/files.json','docs/structure/profile-revisions.json','sdd/project.md','.codex/skills/README.md','sdd/chain/README.md','tools/governance/scripts/governance_support.py','tools/governance/scripts/check-ox.py','tools/governance/scripts/skill_revision.py','tools/governance/tests/test_readme_skill_integration.py','docs/decisions/readme-skill-integration.md'])
 identifier='E-README-SKILL-INTEGRATION-REVIEW';assert not any(e['id']==identifier for e in d['evidence'])
 d['evidence'].append({'id':identifier,'kind':'inspection','command_or_method':'Compare actual enumerated profile/import/preservation/doc delta against each affected criterion consumer. Retain old observations and identical input/artifact bytes; current profile receives independent import acceptance.','observed_result':'Existing scoped criterion states retained; no product execution or scientific/reader-effectiveness claim inferred. New conditional resource identity and negative preservation cases examined separately.','artifact':str(review.relative_to(R)),'sha256':sha(review),'inputs':[{'path':str(q.relative_to(R)),'sha256':sha(q),'role':'other'} for q in sorted(needed)]})
 for c in d['requirements']:c.setdefault('evidence_ids',[]).append(identifier)
 write(p,d);changes.append({'feature':p.parent.name,'changed_inputs':sorted(set(stale)),'previous_envelope':str((B/'envelopes'/(p.parent.name+'.json.bin')).relative_to(R))})
write(B/'impact.json',changes)
old=R/'docs/validation/f0-resumption-20261103/inputs-closure.json';items=[x for x in json.loads(old.read_text())['inputs'] if x['path'].startswith('application/')];assert all(sha(R/x['path'])==x['sha256'] for x in items)
write(B/'product-input-review.json',{'checked':len(items),'changed':[],'method':'Current application inputs compared to accepted F0 closure manifest; no application change in README skill integration.'})
print('Selective successor review for',len(changes),'features;',len(items),'unchanged application inputs')
