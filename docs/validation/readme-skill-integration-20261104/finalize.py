"""Finalize this feature only after the observed integration/governance checks pass."""
from pathlib import Path
import hashlib,json,datetime,importlib.util,copy
R=Path(__file__).resolve().parents[3];B=Path(__file__).resolve().parent;F=R/'sdd/features/readme-skill-integration'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,obj):p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
tests=json.loads((B/'tests.json').read_text());assert tests['failures']==tests['errors']==tests['skipped']==0
assert json.loads((B/'maintenance.log').read_text())['errors']==[]
# Confirm supplied source/installed resource mapping; no source ZIP dependency is added to export.
mapping=json.loads((B/'import-map.json').read_text())
assert all(sha(R/x['destination'])==x['installed_sha256'] for x in mapping['mappings'])
assert (B/'import-tests-after.log').read_text().endswith('OK\n')
report=B/'report.md';report.write_text(f'''# README skill integration acceptance

APPROVED for the bounded local library/profile/documentation integration requested
by the maintainer. No application implementation or new roadmap phase is included.

| Criterion | Method / observed result | Limit |
| --- | --- | --- |
| AC-01 complete portable import | All 13 ZIP members accounted for in package.json/import-map.json: 11 skill files and one configured bridge installed; wrapper retained as source notes. Entry/metadata validated; Ec-only active rules neutralized; imported source ledger labeled historical. | External URLs/scientific results not newly verified; no reader-effectiveness study. |
| AC-02 profile/consumers | 31 skills/bridges: 17 general, 5 conditional, 9 existing specializations. Catalog/profile/bridge checks and new negative cases pass. General technical-documentation unchanged. | Availability is not automatic activation or mandatory dual consultation. |
| AC-03 preservation | Exact predecessor snapshots and an appended 19-path revision preserve all older revisions. Corruption, deletion, unregistered mutation, scope/digest/decision changes, escaping/symlink predecessors and extra resources rejected. Independent distribution passes. Maintenance recovers 439 layout inputs and preserves 485 governed inputs. | Local content-identity checks, not OS isolation or authenticated authorship. |
| AC-04 current reader path | Current counts and README F0 status aligned to project authority. Six import tests pass; complete suite: {tests['executed']} tests, zero failures/errors/skips. Shared inputs in 24 features selectively reviewed; 75 application inputs unchanged. | No GUI/runtime rerun inferred from documentation checks; prior F0 corpus keeps its original inputs and scope. |

The wrapper README from the archive was not copied over Ox's README. The complete
skill lives in .codex/skills/readme-lifecycle-engineering/ and its optional bridge
points to that actual SKILL.md. Imported scientific/source claims remain attributed
to the supplied package. The ZIP stays locally preserved; validation/export needs
installed resources and the recorded provenance, not access to the original ZIP.

AGENTS.md is unchanged: its existing catalog/authority selection contract applies.
The root README's stale F0 line was corrected from existing accepted authorities;
its initial link to excluded operational records failed independent export. The
replacement points to the exported project authority. That failed draft and logs
remain in attempt-1 and import-tests-first.log. check-first.log preserves the
expected stale bindings; historical hashes were redirected only to identical saved
bytes, followed by scoped successor review, not refreshed to claim old execution.

No commits, publication, global installation, new product permissions or deletion of
existing work. Scope and alternatives are in docs/decisions/readme-skill-integration.md.
Revisit when README ownership, entry commands/status, imported metadata/resources,
profile membership or preservation/export formats change. Final freshness/trace
checks supplement these observations; they do not establish reader usability.
''')
p=F/'tasks.md';s=p.read_text().replace('- [ ] T003','- [x] T003').replace('- [ ] T004','- [x] T004');p.write_text(s)
p=F/'converge.md';p.write_text('''# Convergence: README skill integration

AC-01..04 APPROVED for local skill/profile/bridge integration and current navigation.
The exact sources, mappings, negative cases, independent distribution and complete
governance test results are recorded in docs/validation/readme-skill-integration-20261104/.
The initial export-link and stale-input failures are preserved with their correction.
Earlier evidence inputs remain exact historical snapshots; the new31-entry profile
has independent acceptance. Application sources/accepted F0 inputs are unchanged.
No runtime, scientific-effectiveness, reader study or publication claim follows.
AGENTS needs no duplicate rule. Recheck affected records on subsequent content changes.
''')
paths={R/x['destination'] for x in mapping['mappings']}
paths.update([R/x['path'] for x in json.loads((B/'before.json').read_text())])
paths.update(R/x for x in ['tools/governance/scripts/skill_revision.py','tools/governance/tests/test_readme_skill_integration.py','sdd/tools/validate.py','docs/decisions/readme-skill-integration.md'])
paths.update(F/x for x in ['spec.md','plan.md','tasks.md','traceability.json'])
paths.update(p for p in B.iterdir() if p.is_file() and p.name not in ['inputs.json','acceptance.json'])
paths.update(p for p in (R/'.codex/skills/readme-lifecycle-engineering').rglob('*') if p.is_file())
inputs=[{'path':str(p.relative_to(R)),'sha256':sha(p),'role':'other'} for p in sorted(paths)]
write(B/'inputs.json',{'observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'inputs':inputs,'scope':'New integration observations and selective semantic review; unchanged application inputs compared to F0 closure, not reexecuted.'})
p=F/'evidence.json';before=B/'feature-envelope-before-approval.json.bin';assert not before.exists();before.write_bytes(p.read_bytes());d=json.loads(p.read_text());record={'id':'E-README-INTEGRATION','kind':'inspection','command_or_method':'Exact ZIP member/installation mapping, source adaptation/selection review, skill validation, focused denied-mutation tests, independent export and full governance suite; current reader/status review and inherited-input comparison.','observed_result':f'AC-01..04 supported in bounded integration: {tests["executed"]} complete-suite tests, no failures/errors/skips; current profile/bridge/resource/preservation behavior checked. External effectiveness/runtime behavior not inferred.','artifact':str(report.relative_to(R)),'sha256':sha(report),'inputs':inputs+[{'path':str((B/'inputs.json').relative_to(R)),'sha256':sha(B/'inputs.json'),'role':'other'}]}
d['evidence'].append(record)
for c in d['requirements']:c['status']='APPROVED';c['evidence_ids']=['E-README-INTEGRATION']
write(p,d)
spec=importlib.util.spec_from_file_location('v',R/'sdd/tools/validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);trace=v.strict_json(F/'traceability.json')
errors=v.evidence_errors(d,R)+v.trace_errors(trace,R,F,d)+v.input_errors(d,R,trace,F,True);assert not errors,errors
mutant=copy.deepcopy(d);mutant['evidence'][0]['inputs'][0]['sha256']='0'*64;assert any('Stale input' in e for e in v.input_errors(mutant,R,trace,F,True))
mutant=copy.deepcopy(d);mutant['requirements'][0]['evidence_ids']=[];assert v.evidence_errors(mutant,R)
write(B/'acceptance.json',{'states':{c['id']:c['status'] for c in d['requirements']},'schema_trace_current_inputs':'PASS','changed_input_negative_control':'REJECTED as expected','missing_evidence_negative_control':'REJECTED as expected','limits':'Metadata and content checks complement semantic/integration evidence; no usability/runtime proof.'})
print('Four integration criteria APPROVED; current bindings and two negative controls PASS')
