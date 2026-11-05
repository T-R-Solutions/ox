"""Real read attempts in a private bwrap mount/PID/network namespace."""
import json
import os
import pathlib
import subprocess
import tempfile


def run(binary):
    with tempfile.TemporaryDirectory(prefix='ox-plugin-boundary-') as directory:
        root = pathlib.Path(directory)
        protected = root / 'protected'
        protected.write_bytes(b'fixture-only-secret')
        allowed = root / 'allowed'
        allowed.write_bytes(b'fixture-public')
        commands = []

        def observe(args):
            result = subprocess.run(args, capture_output=True, timeout=10)
            commands.append({'command': args, 'exit': result.returncode,
                             'stdout': result.stdout.decode(), 'stderr': result.stderr.decode()})
            return result

        baseline = observe([binary, 'read', str(protected)])
        assert baseline.returncode == 0 and baseline.stdout == b'fixture-only-secret'
        sandbox = ['bwrap', '--unshare-user', '--unshare-pid', '--unshare-net',
                   '--die-with-parent', '--ro-bind', '/usr', '/usr', '--symlink', 'usr/lib', '/lib',
                   '--symlink', 'usr/lib64', '/lib64', '--proc', '/proc', '--dev', '/dev',
                   '--tmpfs', '/tmp', '--ro-bind', binary, '/probe',
                   '--ro-bind', str(allowed), '/allowed']
        positive = observe(sandbox + ['/probe', 'read', '/allowed'])
        assert positive.returncode == 0 and positive.stdout == b'fixture-public'
        for target in [str(protected), '/proc/1/root' + str(protected)]:
            denied = observe(sandbox + ['/probe', 'read', target])
            assert denied.returncode == 13 and b'READ_DENIED' in denied.stderr
            assert b'fixture-only-secret' not in denied.stdout
        assert protected.read_bytes() == b'fixture-only-secret'
        return {'status': 'PASS', 'commands': commands, 'scope': 'disposable read probe; host paths absent in private mounts; not Ox production sandbox adoption'}


if __name__ == '__main__':
    print(json.dumps(run(os.environ.get('OX_CONSUMER_FIXTURE', '/tmp/ox-consumer-fixture')), indent=2))
