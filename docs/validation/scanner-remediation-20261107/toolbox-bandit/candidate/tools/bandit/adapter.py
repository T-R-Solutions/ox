from toolbox.adapters import read_report, ReportError


def invocation(spec):
    if not spec.get('config'):
        raise ValueError('bandit requires explicit consumer configuration')
    return ['--configfile', '/src/' + spec['config'], '--ini', '/toolbox/bandit.ini',
            '--ignore-nosec', '--recursive', '--format', 'json', *['/src/' + p for p in spec['paths']]], {}


def classify(code, output):
    if code not in (0, 1):
        return 'operational_failure', f'bandit exit {code}'
    report = read_report(output / 'stdout.log')
    if not isinstance(report, dict) or report.get('errors') != []:
        raise ReportError('Bandit parse errors or missing errors field')
    metrics, results = report.get('metrics'), report.get('results')
    if not isinstance(metrics, dict) or metrics.get('_totals', {}).get('loc', 0) <= 0 or not isinstance(results, list):
        raise ReportError('Bandit report missing source metrics/results')
    if any(not isinstance(row, dict) or not all(row.get(k) for k in ('test_id', 'filename', 'line_number', 'issue_severity', 'issue_confidence')) for row in results):
        raise ReportError('Bandit incomplete diagnostic')
    if (code == 1) != bool(results):
        raise ReportError('Bandit report and exit disagree')
    return ('findings' if results else 'success'), f'{len(results)} findings'
