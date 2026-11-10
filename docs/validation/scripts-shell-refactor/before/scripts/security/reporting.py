"""Strict scanner report classification; stdout keywords are never an oracle."""
ConfigError = ValueError


def collection(obj, key):
    if not isinstance(obj, dict) or not isinstance(obj.get(key), list):
        raise ConfigError(f'missing report array {key}')
    return obj[key]


def findings(parser, value):
    if parser in {'gitleaks', 'shellcheck', 'pssa'}:
        if not isinstance(value, list) or any(not isinstance(v, dict) for v in value):
            raise ConfigError('expected array of findings')
        return len(value)
    if parser == 'opengrep':
        results = collection(value, 'results'); errors = collection(value, 'errors')
        scanned = collection(value.get('paths'), 'scanned')
        if errors or not scanned: raise ConfigError('incomplete SAST scan')
        # Conservative: any reported skip must be reviewed instead of assuming it benign.
        if value['paths'].get('skipped'): raise ConfigError('SAST skipped targets')
        if any(not isinstance(r, dict) or not isinstance(r.get('check_id'), str) for r in results):
            raise ConfigError('invalid SAST finding')
        if any(r.get('extra', {}).get('is_ignored') for r in results): raise ConfigError('unreviewed inline suppression')
        return len(results)
    if parser == 'osv':
        results = collection(value, 'results')
        packages = [p for source in results for p in collection(source, 'packages')]
        if not packages: raise ConfigError('no extracted dependency inventory')
        if value.get('errors'): raise ConfigError('dependency extraction errors')
        total = 0
        for package in packages:
            if not isinstance(package, dict) or not isinstance(package.get('package'), dict): raise ConfigError('invalid package')
            vulns = package.get('vulnerabilities', [])
            if not isinstance(vulns, list): raise ConfigError('invalid vulnerabilities')
            total += len(vulns)
        return total
    if parser == 'sarif':
        runs = collection(value, 'runs')
        if not runs: raise ConfigError('empty SARIF runs')
        total = 0
        for run in runs:
            if not isinstance(run, dict) or not isinstance(run.get('tool'), dict): raise ConfigError('invalid SARIF run')
            if not run.get('invocations') or any(i.get('executionSuccessful') is not True for i in run['invocations']):
                raise ConfigError('SARIF lacks successful invocation evidence')
            total += len(collection(run, 'results'))
        return total
    if parser == 'json-findings':
        if value.get('complete') is not True: raise ConfigError('custom report incomplete')
        return len(collection(value, 'findings'))
    if parser == 'syft':
        artifacts = collection(value, 'artifacts')
        if not artifacts or not isinstance(value.get('descriptor'), dict): raise ConfigError('empty/invalid SBOM')
        return 0
    if parser == 'grype':
        collection(value, 'matches')
        if not isinstance(value.get('descriptor'), dict) or not isinstance(value.get('source'), dict): raise ConfigError('invalid Grype report')
        return len(value['matches'])
    if parser == 'yara':
        # Upstream CLI JSON is {version, matches:[{rule,file,...}]}, unlike NDJSON.
        matches = collection(value, 'matches')
        if not isinstance(value.get('version'), str) or any(not isinstance(m, dict) or not isinstance(m.get('rule'), str) or not isinstance(m.get('file'), str) for m in matches):
            raise ConfigError('invalid YARA report')
        return len(matches)
    raise ConfigError(f'unsupported parser {parser}')


# Strict JSON and normalized exception validation shared by CLI and adapters.
import json
import datetime as dt


def unique(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError('duplicate JSON key: ' + key)
        obj[key] = value
    return obj


def read_json(path):
    return json.loads(path.read_text(), object_pairs_hook=unique,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError('invalid JSON number')))


def exceptions(document, today=None):
    today=today or dt.date.today(); seen=set()
    if not isinstance(document,list): raise ValueError('exceptions require array')
    for row in document:
        if not isinstance(row,dict): raise ValueError('invalid exception')
        required={'id','tool','finding','component','owner','reason','reviewed','expires','control'}
        if set(row)!=required or any(not isinstance(v,str) or not v.strip() for v in row.values()): raise ValueError('exception metadata missing/unknown')
        identity=(row['tool'],row['finding'],row['component'])
        if identity in seen: raise ValueError('duplicate scoped exception')
        seen.add(identity)
        if dt.date.fromisoformat(row['reviewed'])>today or dt.date.fromisoformat(row['expires'])<=today: raise ValueError('expired/future exception')
    return {'valid':len(document),'passed':True,'applied':False}

