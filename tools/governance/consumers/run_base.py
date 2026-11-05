"""Rebuild and execute bounded consumers; never infer approval from this receipt."""
import argparse
import hashlib
import json
import os
import pathlib
import platform
import subprocess
import tempfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('report', type=pathlib.Path)
    parser.add_argument('--isolation', action='store_true', help='Also require working Bubblewrap namespaces')
    args = parser.parse_args()
    report = args.report.resolve()
    report.mkdir()
    source = pathlib.Path(__file__).resolve().parent
    build = pathlib.Path(tempfile.mkdtemp(prefix='ox-consumer-build-'))
    records = []
    identities = {str(p.name): hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in source.iterdir() if p.is_file()}
    environment = dict(os.environ, OX_CONSUMER_FIXTURE=str(build / 'fixture'),
                       OX_PLUGIN_FIXTURE=str(build / 'plugin'), OX_OUTPUT_FIXTURE=str(build / 'output'))

    def execute(command, name):
        with (report / name).open('xb') as output:
            result = subprocess.run(command, env=environment, stdout=output, stderr=subprocess.STDOUT, timeout=30)
        records.append({'command': command, 'exit': result.returncode, 'log': name})
        if result.returncode:
            raise RuntimeError(f'{name}: exit {result.returncode}')

    error = None
    try:
        execute(['rustc', '+1.99.1', '-Vv'], 'compiler.log')
        for src, dest, test in [('fixture.rs', 'fixture', False), ('plugin_fixture.rs', 'plugin', False),
                                ('output_fixture.rs', 'output', False), ('model_tests.rs', 'models', True),
                                ('operation_tests.rs', 'operations', True)]:
            command = ['rustc', '+1.99.1', '--edition=2024', '-Dwarnings']
            if test:
                command.append('--test')
            command.extend([str(source / src), '-o', str(build / dest)])
            execute(command, 'build-' + dest + '.log')
        execute([str(build / 'models'), '--nocapture'], 'models.log')
        execute([str(build / 'operations'), '--nocapture', '--test-threads=1'], 'operations.log')
        if args.isolation:
            execute(['python3', str(source / 'isolation_test.py')], 'isolation.json')
    except Exception as exc:
        error = str(exc)
    receipt = {'platform': platform.platform(), 'sources_sha256': identities,
               'binaries_sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in build.iterdir()},
               'build_directory': str(build), 'commands': records, 'error': error,
               'isolation_requested': args.isolation, 'status': 'PASS' if error is None else 'FAIL'}
    (report / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({'status': receipt['status'], 'report': str(report), 'error': error}))
    return int(error is not None)


if __name__ == '__main__':
    raise SystemExit(main())
