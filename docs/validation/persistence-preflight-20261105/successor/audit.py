"""Supplemental read-only contract audit; never invokes fixture executables."""
import copy
import hashlib
import json
from pathlib import Path
R = Path(__file__).resolve().parents[4]
B = Path(__file__).resolve().parent.parent
S = B / 'successor'
STATES = {'APPROVED', 'REJECTED', 'INCONCLUSIVE', 'UNVERIFIED', 'NOT APPLICABLE'}
def load(name):
    return json.loads((B / name).read_text())
def check(c):
    tables = {g: {x['id']: x for x in c[g]} for g in ['tasks','attempts','checks','operations','observations','dispositions','payloads']}
    assert all(len(tables[g]) == len(c[g]) for g in tables)
    assert c['provenance']['completeness'] == 'complete'
    assert set(c['expected_current']) == set(tables['checks'])
    for t in c['tasks']: assert t['store_id'] == c['store_id']
    for a in c['attempts']: assert a['task_id'] in tables['tasks']
    for k in c['checks']:
        assert k['executable_payload_id'] in tables['payloads']
        assert k['directory'] == '/fixture' and k['inputs'] and k['description']
    for o in c['operations']:
        p=o['payload']
        assert o['payload_sha256'] == hashlib.sha256(json.dumps(p,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
        if 'task_id' in p: assert p['task_id'] in tables['tasks']
        if 'attempt_id' in p: assert p['attempt_id'] in tables['attempts']
        if 'record_id' in p:
            rec=(tables['observations']|tables['dispositions'])[p['record_id']]
            assert rec['check_id']==p['check_id']
            assert p['intent_id'] in tables['operations']
    for o in c['observations']:
        assert o['provenance_ref']=='store.provenance'
        assert o['historical_state'] in STATES
        assert o['intent_id'] in tables['operations']
        assert o['check_id'] in tables['checks'] and o['attempt_id'] in tables['attempts']
        for e in o['evidence']: assert e['payload_id'] in tables['payloads'] and e['phase'] in ['before','after']
        for x in o['oracle_captures'].values():
            assert x in tables['payloads'] if isinstance(x,str) else x=={'tag':'absent'}
    for d in c['dispositions']:
        assert d['state']=='NOT APPLICABLE' and d['reason'].strip() and d['execution']=={'tag':'absent'}
        assert d['check_id'] in tables['checks']
    for k,v in c['expected_current'].items(): assert v['state'] in STATES
    assert len({a['operation_id'] for a in c['ack_sequence']})==len(c['ack_sequence'])
    assert all(a['operation_id'] in tables['operations'] for a in c['ack_sequence'])
    return tables
corpora={n:load(n+'.json') for n in ['M0','M1','M32','ML']}
for c in corpora.values(): check(c)
assert (len(corpora['M32']['observations']),len(corpora['M32']['dispositions']))==(26,6)
# Reconstruct dependencies from shared executable identity, independently of affected_checks.
for row in load('revalidation.json'):
    c=corpora[row['corpus']]; target=next(k for k in c['checks'] if k['id']==row['dependent_check'])
    affected={k['id'] for k in c['checks'] if k['executable_payload_id']==target['executable_payload_id']} if row['mutation']=='oracle_bytes' else {target['id']}
    assert set(row['affected_checks'])==affected
    assert row['expected']=={k:('UNVERIFIED' if k in affected else v['state']) for k,v in c['expected_current'].items()}
# Per-capture and history totals count logical occurrences, including repeated oracle bytes.
summary=[]
for name,c in corpora.items():
    sizes={p['id']:p['length'] for p in c['payloads']}; retained=0; admissions=[]
    for o in c['observations']:
        totals={phase:sum(sizes[e['payload_id']] for e in o['evidence'] if e['phase']==phase)+(sizes[o['oracle_captures'][phase]] if isinstance(o['oracle_captures'][phase],str) else 0) for phase in ['before','after']}
        assert all(sizes[e['payload_id']]<=16*1024**2 for e in o['evidence'])
        assert max(totals.values())<=32*1024**2
        admissions.append(retained+totals['before']+32*1024**2<=128*1024**2)
        retained+=sum(totals.values())
    assert all(admissions)
    summary.append({'corpus':name,'observations':len(c['observations']),'dispositions':len(c['dispositions']),'logical_retained_bytes':retained,'all_observation_prefixes_fit_128MiB':all(admissions)})
for v in load('admission.json')['boundary_vectors']:
    assert ('admit' if v['retained']+v['new_before']+v['reserved_after']<=128*1024**2 else 'refuse_before_effect')==v['expected']
# Supplemental invalid-record controls do not rewrite adopted inputs.
negative=[]
for label in ['oracle_reference','provenance','state','disposition_execution','ack_duplicate']:
    c=copy.deepcopy(corpora['M1'])
    if label=='oracle_reference': c['checks'][0]['executable_payload_id']='missing'
    elif label=='provenance': c['observations'][0]['provenance_ref']='missing'
    elif label=='state': c['expected_current']['C1']['state']='SUCCESS'
    elif label=='disposition_execution': c['dispositions'][0]['execution']={'tag':'exited','code':0}
    else: c['ack_sequence'].append(c['ack_sequence'][0])
    try: check(c)
    except (AssertionError,KeyError): negative.append(label)
    else: raise AssertionError(label)
# Recheck native-source bytes and locally retained license texts.
for e in load('native-source.json')['source_files']:
    assert hashlib.sha256((R/e['path']).read_bytes()).hexdigest()==e['sha256']
for p in json.loads((S/'licenses.json').read_text()):
    for e in p['texts']: assert hashlib.sha256((R/e['path']).read_bytes()).hexdigest()==e['sha256']
print(json.dumps({'result':'PASS','corpora':summary,'negative_controls_rejected':negative,'limitations':'Manifest consistency and arithmetic only. Expected tables remain independent of candidate code; no storage/effect execution or legal distribution acceptance.'},indent=2))
