"""Docker subprocess boundary. No shell interpolation, no implicit pull."""
import json
import os
import shutil
import subprocess
import time
import uuid
from pathlib import Path


class DockerError(RuntimeError):
    pass


def capture(args, timeout=30):
    try:
        p = subprocess.run(['docker', *args], text=True, capture_output=True, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired) as e:
        raise DockerError(str(e)) from e
    if p.returncode:
        raise DockerError(p.stderr.strip() or p.stdout.strip() or f'docker exit {p.returncode}')
    return p.stdout


def inspect(image, timeout=30):
    return json.loads(capture(['image', 'inspect', image], timeout=timeout))[0]


def doctor():
    result = {'docker_cli': shutil.which('docker'), 'uid': os.getuid(), 'gid': os.getgid(),
              'python': os.sys.version, 'machine': os.uname().machine,
              'remote_daemon_supported': False}
    try:
        context = json.loads(capture(['context', 'inspect']))[0]
        endpoint = os.environ.get('DOCKER_HOST', context['Endpoints']['docker']['Host'])
        result['endpoint'] = endpoint
        if not endpoint.startswith('unix://'):
            raise DockerError('only a local Unix socket is supported: bind mounts must refer to this host')
        result['version'] = json.loads(capture(['version', '--format', '{{json .}}']))
        result['ready'] = True
    except (DockerError, KeyError, ValueError) as e:
        result.update(ready=False, error=str(e))
    return result


def bind_mount(source, target, readonly=False, label=None):
    label = label if label is not None else os.environ.get('TOOLBOX_SELINUX_LABEL', '')
    if not label:
        return ['--mount', f'type=bind,src={source},dst={target}' + (',readonly' if readonly else '')]
    if label not in ('private', 'shared'):
        raise ValueError('TOOLBOX_SELINUX_LABEL must be empty, private or shared')
    source = Path(source)
    if not source.is_absolute() or not source.is_dir() or any(c in str(source) for c in ':,\n\r'):
        raise ValueError('SELinux bind source must be an existing absolute directory without delimiters')
    suffix = 'Z' if label == 'private' else 'z'
    return ['--volume', f'{source}:{target}:' + ('ro,' if readonly else 'rw,') + suffix]


def command(image, argv, source, output, network='none', env=None, database=None, mount_label=None):
    name = 'toolbox-' + uuid.uuid4().hex
    args = ['run', '--pull=never', '--name', name, '--init', '--read-only',
            '--user', f'{os.getuid()}:{os.getgid()}', '--cap-drop=ALL',
            '--security-opt=no-new-privileges:true', '--network', network,
            '--tmpfs', '/tmp:rw,nosuid,nodev,mode=1777', '--shm-size=256m',
            *bind_mount(source, '/src', readonly=True, label=mount_label),
            *bind_mount(output, '/out', label=mount_label),
            '--workdir', '/src', '--env', 'HOME=/tmp/home', '--env', 'XDG_CACHE_HOME=/tmp/cache']
    if network != 'none':
        args += ['--add-host', 'host.docker.internal:host-gateway']
    if database:
        args += bind_mount(database, '/db', readonly=True, label=mount_label)
    for key, value in sorted((env or {}).items()):
        args += ['--env', f'{key}={value}']
    return name, ['docker', *args, image, *argv]


def execute(cmd, name, output, timeout):
    output = Path(output)
    start = time.monotonic()
    timed_out = cancelled = False
    state, runtime_error = {}, None
    with (output / 'stdout.log').open('wb') as stdout, (output / 'stderr.log').open('wb') as stderr:
        process = subprocess.Popen(cmd, stdout=stdout, stderr=stderr)
        try:
            runtime_code = process.wait(timeout=timeout)
        except (subprocess.TimeoutExpired, KeyboardInterrupt) as e:
            timed_out = isinstance(e, subprocess.TimeoutExpired)
            cancelled = not timed_out
            try:
                capture(['stop', '--time', '10', name], timeout=20)
            except DockerError as stop_error:
                runtime_error = str(stop_error)
            process.terminate()
            try:
                runtime_code = process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                runtime_code = process.wait()
        try:
            state = json.loads(capture(['inspect', '--format', '{{json .State}}', name]))
        except (DockerError, ValueError) as e:
            runtime_error = str(e)
        finally:
            try:
                capture(['rm', '--force', name])
            except DockerError as e:
                runtime_error = (runtime_error or '') + '\ncleanup: ' + str(e)
    return {'runtime_exit_code': runtime_code, 'tool_exit_code': state.get('ExitCode'),
            'container_state': state, 'timed_out': timed_out, 'cancelled': cancelled,
            'runtime_error': runtime_error, 'duration_seconds': round(time.monotonic() - start, 3)}
