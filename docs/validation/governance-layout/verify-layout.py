"""Observe relocation and continuity against the pre-edit content baseline."""
from pathlib import Path
import hashlib
import json
import re
import sys
import tarfile

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT/'tools/governance/scripts'))
from governance_support import relocated_path, relocated_traceability


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    folder = ROOT/'docs/validation/governance-layout'
    baseline = json.loads((folder/'before.json').read_text())
    moves = json.loads((folder/'relocation.json').read_text())
    errors = []
    checked = []

    def compare(label, actual, expected):
        checked.append(label)
        if actual != expected:
            errors.append(label)

    recovery = json.loads((folder/'recovery.json').read_text())
    packed = set(recovery['archive_members'])
    retained = set(recovery['retained_paths'])
    compare('complete recovery inventory', packed | retained, set(baseline))
    compare('disjoint recovery inventory', packed & retained, set())
    with tarfile.open(folder/'before.tar.gz') as archive:
        compare('archive inventory', set(archive.getnames()), packed)
        originals = {name: archive.extractfile(name).read() for name in packed}
    for name in retained:
        originals[name] = (ROOT/name).read_bytes()
    for name, data in originals.items():
        compare('baseline bytes: '+name, sha(data), baseline[name])
    sources = {name for name in baseline if name.startswith('src/')}
    compare('23 source files', len(sources), 23)
    compare('complete move inventory', {row['source'] for row in moves}, sources)
    compare('unique destinations', len({row['destination'] for row in moves}), 23)
    compare('src has no governance files', list((ROOT/'src').rglob('*')), [])
    for row in moves:
        compare('mapping: '+row['source'], row['destination'], relocated_path(row['source']))
        compare('source identity: '+row['source'], row['previous_sha256'], baseline[row['source']])
        compare('destination exists: '+row['destination'], (ROOT/row['destination']).is_file(), True)
        if row['source'].startswith('src/fixtures/') and not row['source'].endswith('normative-coverage.json'):
            compare('unchanged data: '+row['destination'], sha((ROOT/row['destination']).read_bytes()), row['previous_sha256'])
    for name, data in originals.items():
        immutable = (name.startswith(('.codex/skills/', 'docs/validation/', 'docs/structure/'))
                     or name.startswith(('sdd/tools/', 'sdd/templates/', 'sdd/chain/'))
                     or name in {'AGENTS.md', 'sdd/workflow.md', 'sdd/evidence.md', 'sdd/README.md',
                                 'docs/decisions/adoption.md', 'docs/decisions/governance-externalization.md',
                                 'docs/decisions/implementation-transition.md'}
                     or (name.startswith('sdd/features/') and Path(name).name in {'spec.md', 'plan.md', 'tasks.md', 'traceability.json'}))
        if not immutable:
            continue
        current = (ROOT/name).read_bytes()
        if name == 'docs/structure/files.json':
            compare('prior provenance revisions', json.loads(current)['revisions'][:-1], json.loads(data)['revisions'])
        else:
            if name.startswith('sdd/features/') and Path(name).name == 'traceability.json':
                data = relocated_traceability(data)
            compare('preserved contract/history: '+name, sha(current), sha(data))
    constitution = (ROOT/'docs/constitution.md').read_bytes()
    compare('constitution link-only change', constitution,
            originals['docs/constitution.md'].replace(b'../src/fixtures/profile.json', b'../config/governance/profile.json'))
    expected = json.loads(originals['src/fixtures/normative-coverage.json'])
    for row in expected.values():
        row['oracle'] = relocated_path(row['oracle'])
    rule = re.search(r'^- GOV-04: (.+)$', constitution.decode(), re.M)[1]
    expected['GOV-04']['rule_sha256'] = sha(rule.encode())
    compare('coverage reference-only change', json.loads((ROOT/'config/governance/normative-coverage.json').read_text()), expected)
    result = {'method': 'Reconstruct baseline from archived old versions and hash-verified unchanged distributed files; compare exact bytes except authorized path translations.',
              'baseline_manifest_sha256': sha((folder/'before.json').read_bytes()),
              'baseline_archive_sha256': sha((folder/'before.tar.gz').read_bytes()),
              'checks': checked, 'errors': errors, 'status': 'PASS' if not errors else 'FAIL',
              'limitations': ['Local continuity inspection; no application implementation or new model evaluation.']}
    (folder/'inventory.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(result['status']+f': {len(checked)} comparisons; {len(errors)} differences outside authorized changes.')
    for error in errors:
        print('FAIL:', error)
    return bool(errors)


if __name__ == '__main__':
    sys.exit(main())
