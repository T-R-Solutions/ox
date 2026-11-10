from pathlib import Path
import json,hashlib,subprocess
r=Path(__file__).resolve().parents[3];b=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
paths=set()
for x in json.loads((b/'current-product-inputs.json').read_text()):
 p=r/x['path'];assert sha(p)==x['sha256'];paths.add(p)
for f in ['product-f0-gate','product-local-task-ui','product-verification-engine']:
 base=r/'sdd/features'/f
 paths.update(base/n for n in ['spec.md','plan.md','tasks.md','traceability.json','converge.md'])
 for row in json.loads((base/'traceability.json').read_text()):paths.update([r/row['implementation'],r/row['oracle']])
for f in json.loads((r/'docs/validation/f0-reconciliation-20261101/skill-t004.json').read_text()):
 paths.update(r/'sdd/features'/f['feature']/n for n in ['spec.md','tasks.md','evidence.json'])
paths.update(p for p in b.glob('*.py'))
paths.update(r/n for n in ['AGENTS.md','docs/constitution.md','docs/architecture/context.md','sdd/project.md','sdd/workflow.md','sdd/evidence.md','docs/decisions/f0-boundary-20261102.md','docs/decisions/local-persistence-proposal.md','sdd/features/product-local-persistence/experiment-protocol.md','.codex/skills/performance-engineering/SKILL.md','.codex/skills/iced-engineering/SKILL.md','.codex/skills/rust/SKILL.md'])
paths.update(b/n for n in ['current-checks.json','current-history-checks.json','documentary-review.md','documentary-scenarios.json','persistence-decisions.md','environment.json','current-product-inputs.json','coverage/summary.json'])
inputs=[{'path':str(p.relative_to(r)),'sha256':sha(p),'role':'implementation' if 'application' in p.relative_to(r).parts else 'other'} for p in sorted(paths)]
# Retain exact source/observer snapshot and a raw artifact inventory (special files are identified, never read).
artifacts=[]
for p in sorted(b.rglob('*')):
 if p.is_file() and p.name!='artifact-inventory.json':artifacts.append({'path':str(p.relative_to(r)),'sha256':sha(p),'bytes':p.stat().st_size})
 elif p.exists() and not p.is_dir():artifacts.append({'path':str(p.relative_to(r)),'mode':oct(p.stat().st_mode),'content_read':False})
(b/'artifact-inventory.json').write_text(json.dumps(artifacts,indent=2)+'\n')
for f in ['product-f0-gate','product-local-task-ui','product-verification-engine']:
 p=r/'sdd/features'/f/'evidence.json';d=json.loads(p.read_text());d['environment']='T903 2026-11-05 successor: real isolated X11/native Wayland current inputs, see docs/validation/t903-20261105/report.md; full-count RSS applicability INCONCLUSIVE.'
 d['evidence'].append({'id':'E-T903-20261105','kind':'inspection','command_or_method':'Actual isolated compositor keyboard/pointer and rendered-state journeys; per-cell 3+20 response samples/all frame logs, three10s idle windows; 32-observation journeys; FIFO/held worker/direct-child observations; original binary corroboration; backend and fixed large-history metrics; current coverage/Rust tests; scoped documentary successor review. See report and exact per-run commands.','observed_result':'Current functional journeys and adopted small GUI 12-cell matrix pass; full32 history draw failure159.935ms repaired and reobserved <=74.384ms. Full32 GUI RSS90.63–133.69MiB exceeds64MiB small corpus; applicability of separate256MiB fixed stress envelope is not adopted for this workload. T903 remains OPEN/current F0 INCONCLUSIVE, no limit relaxed. Documentary preparation inspected separately.','artifact':str((b/'report.md').relative_to(r)),'sha256':sha(b/'report.md'),'inputs':inputs})
 for q in d['requirements']:
  q['evidence_ids'].append('E-T903-20261105')
  if f=='product-f0-gate':q['status']='INCONCLUSIVE' if q['id']=='AC-05' else 'APPROVED'
  elif f=='product-local-task-ui':q['status']='APPROVED'
  # Engine API accepted by robustness focused tests and current suite; no API code change here.
 d['limitations'].insert(0,'T903 successor: current F0/full-count GUI RSS acceptance INCONCLUSIVE, T903 open; small GUI/functional/worker observations and documentary preparation are independently bounded. See report. Historical limitations below retain original scope.')
 p.write_text(json.dumps(d,indent=2)+'\n')
