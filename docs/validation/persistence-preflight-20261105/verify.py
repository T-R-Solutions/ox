"""Read-only preflight checks. Does not execute encoders, effects, or experiments."""
from pathlib import Path
import copy
import hashlib
import json

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent

def digest(data):
    return hashlib.sha256(data).hexdigest()

def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()

def validate(corpus):
    assert corpus['schema_version'] == 1
    groups = ['tasks', 'attempts', 'checks', 'operations', 'observations', 'dispositions', 'payloads']
    by = {}
    for group in groups:
        by[group] = {x['id']: x for x in corpus[group]}
        assert len(by[group]) == len(corpus[group]), group
    for attempt in corpus['attempts']:
        assert attempt['task_id'] in by['tasks']
    for op in corpus['operations']:
        assert op['payload_sha256'] == digest(canonical(op['payload']))
        p = op['payload']
        if 'attempt_id' in p:
            assert p['attempt_id'] in by['attempts']
        if 'record_id' in p:
            record = (by['observations'] | by['dispositions'])[p['record_id']]
            assert p['record_sha256'] == digest(canonical(record))
            assert p['intent_id'] in by['operations']
        if 'check_id' in p:
            assert p['check_sha256'] == digest(canonical(by['checks'][p['check_id']]))
    for record in corpus['observations'] + corpus['dispositions']:
        assert record['attempt_id'] in by['attempts']
        assert record['check_id'] in by['checks']
        if record.get('kind') == 'applicability':
            assert record['reason'].strip()
            assert record['execution'] == {'tag': 'absent'}
        else:
            assert record['intent_id'] in by['operations']
            for entry in record['evidence']:
                assert entry['payload_id'] in by['payloads']
    assert [a['sequence'] for a in corpus['ack_sequence']] == list(range(1, len(corpus['ack_sequence']) + 1))
    for ack in corpus['ack_sequence']:
        assert ack['operation_id'] in by['operations']
    for p in corpus['payloads']:
        data = (ROOT / p['path']).read_bytes()
        assert len(data) == p['length'] and digest(data) == p['sha256'], p['path']

results = []
for name, count in [('M0', 0), ('M1', 5), ('M32', 32), ('ML', 2)]:
    c = json.loads((HERE / f'{name}.json').read_text())
    validate(c)
    assert len(c['observations']) + len(c['dispositions']) == count
    if name == 'ML':
        assert c['raw_input_content_bytes'] == 120 * 1024 * 1024
    results.append({'corpus': name, 'records': count, 'result': 'PASS'})
base = json.loads((HERE / 'M1.json').read_text())
assert set(x['state'] for x in base['expected_current'].values()) == {'APPROVED', 'REJECTED', 'INCONCLUSIVE', 'UNVERIFIED', 'NOT APPLICABLE'}
for mutation in ['dangling', 'duplicate', 'payload_conflict', 'empty_reason']:
    c = copy.deepcopy(base)
    if mutation == 'dangling':
        c['attempts'][0]['task_id'] = 'missing'
    elif mutation == 'duplicate':
        c['operations'].append(copy.deepcopy(c['operations'][0]))
    elif mutation == 'payload_conflict':
        c['operations'][0]['payload']['task_id'] = 'changed'
    else:
        c['dispositions'][0]['reason'] = ' '
    try:
        validate(c)
    except (AssertionError, KeyError):
        results.append({'negative_control': mutation, 'result': 'REJECTED_AS_EXPECTED'})
    else:
        raise AssertionError(mutation)
for entry in json.loads((HERE / 'observed-inputs.json').read_text()):
    assert digest((ROOT / entry['path']).read_bytes()) == entry['sha256'], entry['path']
for entry in json.loads((HERE / 'fixture-hashes.json').read_text()):
    assert digest((ROOT / entry['path']).read_bytes()) == entry['sha256'], entry['path']
for name in ['Cargo.toml', 'Cargo.lock']:
    assert (HERE / name).read_bytes() == (ROOT / '.local/build/persistence-experiment-preflight-20261105/dependencies' / name).read_bytes()
for row in json.loads((HERE / 'revalidation.json').read_text()):
    before = json.loads((HERE / (row['corpus'] + '.json')).read_text())['expected_current']
    assert all(row['expected'][check] == 'UNVERIFIED' for check in row['affected_checks'])
    assert all(row['expected'][key] == value['state'] for key, value in before.items() if key not in row['affected_checks'])
print(json.dumps({'method': 'neutral manifest integrity/reference checks and negative controls; source/lock byte comparison', 'results': results, 'limitations': ['No storage execution, durability, migration, actual effects, graphical timing or product acceptance checked.']}, indent=2))
