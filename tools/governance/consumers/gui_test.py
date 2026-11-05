"""Bounded dedicated Xwayland session; preserves raw logs and screenshots."""
import json
import os
import pathlib
import select
import subprocess
import sys

root = pathlib.Path(__file__).resolve().parents[3]
report = pathlib.Path(sys.argv[1]).resolve()
report.mkdir()
readfd, writefd = os.pipe()
result = {}
with (report / 'server.log').open('x') as log:
    args = ['Xwayland', '-displayfd', str(writefd), '-fullscreen', '-geometry', '1800x1200', '-nolisten', 'tcp', '-shm']
    result['server_command'] = args
    server = subprocess.Popen(args, pass_fds=(writefd,), stdout=log, stderr=subprocess.STDOUT)
    os.close(writefd)
    try:
        if not select.select([readfd], [], [], 10)[0]:
            raise RuntimeError('Xwayland readiness exceeded 10s')
        display = os.read(readfd, 32).decode().strip()
        if not display.isdigit():
            raise RuntimeError('Invalid display: ' + repr(display))
        result['display'] = ':' + display
        env = dict(os.environ, DISPLAY=result['display'], OX_DESKTOP_CAPTURE_DIR=str(report),
                   OX_GUI_CONSUMER='/tmp/ox-consumer-gui')
        env.pop('WAYLAND_DISPLAY', None)
        args = ['/tmp/ox-consumer-gui-tests', '--nocapture', '--test-threads=1']
        result['test_command'] = args
        with (report / 'tests.log').open('x') as out:
            run = subprocess.run(args, cwd=root, env=env, stdout=out, stderr=subprocess.STDOUT, timeout=55)
        result['exit'] = run.returncode
    except Exception as error:
        result['error'] = str(error)
    finally:
        os.close(readfd)
        server.terminate()
        try:
            result['server_exit'] = server.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server.kill()
            result['server_exit'] = server.wait()
(report / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
if (report / 'tests.log').exists():
    print((report / 'tests.log').read_text())
raise SystemExit(0 if result.get('exit') == 0 else 1)
