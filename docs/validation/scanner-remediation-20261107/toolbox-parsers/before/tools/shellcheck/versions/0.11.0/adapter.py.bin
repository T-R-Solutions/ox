from toolbox.adapters import read_report, ReportError


def invocation(spec):
    args = ['--format=json1']
    if spec.get('config'):
        args += ['--rcfile', '/src/' + spec['config']]
    return args + ['--'] + spec['paths'], {}


def classify(code, output):
    if code not in [0, 1]:
        return 'operational_failure', f'shellcheck exit {code}'
    report = read_report(output / 'stdout.log')
    comments = report['comments']
    if not isinstance(comments, list) or any(not isinstance(item, dict) or 'code' not in item for item in comments):
        raise ReportError('invalid ShellCheck report shape')
    if (code == 1) != bool(comments):
        raise ReportError('ShellCheck report and exit code disagree')
    return ('findings' if comments else 'success'), f'{len(comments)} diagnostics'
