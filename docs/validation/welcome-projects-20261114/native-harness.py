"""Replay explicit keyboard/pointer plans in a private Mutter desktop.

State and project fixtures live only beneath this run's output directory. The
plan and resulting event stream are retained; this harness does not infer PASS
from a screenshot. No primary-desktop input is used.
"""
import argparse
import hashlib
import importlib.util
import json
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--name', required=True)
parser.add_argument('--monitor', default='1440x900')
parser.add_argument('--plan', type=Path, required=True)
args = parser.parse_args()
plan = json.loads(args.plan.read_text())
out = Path(__file__).resolve().parent / args.name
spec = importlib.util.spec_from_file_location('session', ROOT / 'docs/validation/f0-resumption-20261103/native-session.py')
native = importlib.util.module_from_spec(spec)
spec.loader.exec_module(native)
session = None
app = None
logs = []
record = {'method': 'private Mutter Wayland, RemoteDesktop real input, PipeWire captures', 'monitor': args.monitor, 'plan': plan, 'launches': []}

def chord(mod, key):
    session.key(mod, True)
    session.key(key)
    session.key(mod, False)

def expand(value):
    return value.replace('{out}', str(out))

def start():
    global app
    binary = ROOT / 'application/target/debug/ox'
    log = (out / f'wayland-{len(logs)}.log').open('w')
    logs.append(log)
    env = dict(session.env, WAYLAND_DEBUG='1', OX_VALIDATION_SESSION=args.name,
               XDG_STATE_HOME=str(out / 'state'), GDK_DEBUG='no-portals',
               GTK_A11Y='none', GSETTINGS_BACKEND='memory', GTK_USE_PORTAL='0')
    app = subprocess.Popen([str(binary)], cwd=ROOT, env=env, stdout=log, stderr=log)
    session.children.append(app)
    record['launches'].append({'pid': app.pid, 'binary_sha256': hashlib.sha256(binary.read_bytes()).hexdigest()})
    session.wait(lambda: 'xdg_toplevel' in Path(log.name).read_text(), 'application toplevel')
    time.sleep(1)
    session.key(0xFFE1)
    session.wait(lambda: '.enter(' in Path(log.name).read_text(), 'keyboard focus')

def children():
    found = set()
    for path in Path(f'/proc/{app.pid}/task').glob('*/children'):
        try:
            found.update(path.read_text().split())
        except FileNotFoundError:
            pass
    return [pid for pid in found if Path(f'/proc/{pid}/cmdline').exists() and b'zenity' in Path(f'/proc/{pid}/cmdline').read_bytes()]

try:
    session = native.Session(out, args.monitor, 1)
    # Mutter creates the virtual pointer on first motion. Prime it before the
    # client binds wl_seat; otherwise the first intended click can be lost.
    session.call('RemoteDesktop', session.rd, 'NotifyPointerMotionAbsolute', '(sdd)', (session.stream, 1.0, 1.0))
    time.sleep(.5)
    (out / 'plan.json').write_text(json.dumps(plan, indent=2) + '\n')
    record['inputs'] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT / 'application/crates/ox-ui/src').rglob('*.rs')}
    start()
    for step in plan:
        op = step[0]
        if op == 'shot':
            session.shot(step[1])
        elif op == 'tab':
            for _ in range(abs(step[1])):
                chord(0xFFE1, 0xFF09) if step[1] < 0 else session.key(0xFF09)
        elif op == 'key':
            session.key(step[1])
            time.sleep(.3)
        elif op == 'chord':
            chord(step[1], step[2])
            time.sleep(.3)
        elif op == 'text':
            for char in expand(step[1]):
                session.key(ord(char) if ord(char) < 256 else 0x01000000 | ord(char))
        elif op == 'nav':
            chord(0xFFE3, ord('k'))
            for char in step[1]:
                session.key(ord(char))
            session.key(0xFF0D)
            time.sleep(.4)
        elif op == 'click':
            session.call('RemoteDesktop', session.rd, 'NotifyPointerMotionAbsolute', '(sdd)', (session.stream, float(step[1]), float(step[2])))
            time.sleep(.2)
            session.call('RemoteDesktop', session.rd, 'NotifyPointerButton', '(ib)', (272, True))
            session.call('RemoteDesktop', session.rd, 'NotifyPointerButton', '(ib)', (272, False))
            session.events.append({'pointer_click': step[1:3], 'time': time.monotonic()})
            time.sleep(.4)
        elif op == 'wait':
            time.sleep(step[1])
        elif op == 'mkdir':
            Path(expand(step[1])).mkdir(parents=True)
        elif op == 'write':
            Path(expand(step[1])).write_text(step[2])
        elif op == 'rename':
            Path(expand(step[1])).rename(expand(step[2]))
        elif op == 'assert_exists':
            assert Path(expand(step[1])).exists(), step
        elif op == 'assert_absent':
            assert not Path(expand(step[1])).exists(), step
        elif op == 'assert_text':
            assert Path(expand(step[1])).read_text() == step[2], step
        elif op == 'assert_empty':
            assert not list(Path(expand(step[1])).iterdir()), step
        elif op == 'chooser_ready':
            session.wait(lambda: bool(children()), 'real Zenity child')
            record.setdefault('chooser_pids', []).append(children())
            time.sleep(30)
        elif op == 'chooser_gone':
            session.wait(lambda: not children(), 'chooser reaped')
        elif op == 'stop':
            chord(0xFFE9, 0xFFC1)
            session.wait(lambda: app.poll() is not None, 'natural application close')
            record['launches'][-1]['exit'] = app.returncode
            assert app.returncode == 0
        elif op == 'start':
            assert app.poll() is not None
            start()
        else:
            raise ValueError(step)
    record['result'] = 'observed'
except Exception as error:
    record['error'] = str(error)
    if session:
        session.shot('failure')
    raise
finally:
    if session:
        session.close()
    for log in logs:
        log.close()
    out.mkdir(exist_ok=True)
    (out / 'result.json').write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps({k: v for k, v in record.items() if k not in ('inputs', 'plan')}))
