"""Private native capture/input observation; never sends primary-desktop input."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parents[3]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--name', required=True)
parser.add_argument('--monitor', default='1440x900')
parser.add_argument('--exercise', action='store_true')
args = parser.parse_args()
out = Path(__file__).resolve().parent / args.name
spec = importlib.util.spec_from_file_location('native', ROOT / 'docs/validation/f0-resumption-20261103/native-session.py')
native = importlib.util.module_from_spec(spec)
spec.loader.exec_module(native)
session = None
record = {'monitor': args.monitor, 'exercise': args.exercise}

def chord(mod, key):
    session.key(mod, True)
    session.key(key)
    session.key(mod, False)

def navigate(query):
    chord(0xFFE3, ord('k'))
    for char in query:
        session.key(ord(char))
    session.key(0xFF0D)
    time.sleep(.4)

try:
    session = native.Session(out, args.monitor, 1)
    binary = ROOT / 'application/target/debug/ox'
    record['binary_sha256'] = hashlib.sha256(binary.read_bytes()).hexdigest()
    record['inputs'] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in sorted((ROOT / 'application/crates/ox-ui/src').rglob('*.rs'))}
    with (out / 'application.log').open('w') as log:
        app = subprocess.Popen([str(binary)], cwd=ROOT,
            env=dict(session.env, WAYLAND_DEBUG='1', XDG_STATE_HOME=str(out / 'state')),
            stdout=log, stderr=log)
        session.children.append(app)
        session.wait(lambda: 'xdg_toplevel' in (out / 'application.log').read_text(), 'toplevel')
        time.sleep(1)
        session.key(0xFFE1)
        session.wait(lambda: '.enter(' in (out / 'application.log').read_text(), 'keyboard focus')
        # Mutter initially maximizes the application in this private session.
        # Do not toggle Alt+F10: it would restore a smaller, different geometry.
        session.shot('initial')
        if args.exercise:
            # Existing traversal starts with Settings, Open, New, Manual.
            for _ in range(4):
                session.key(0xFF09)
            session.key(0xFF0D)
            time.sleep(.3)
            session.shot('manual-path')
            project = out / 'project-with-a-long-readable-local-name'
            project.mkdir()
            (project / 'sentinel.txt').write_text('preserve\n')
            for char in str(project):
                session.key(ord(char))
            session.shot('manual-filled')
            session.key(0xFF0D)
            history = out / 'state/ox/recent-projects.v1'
            session.wait(lambda: history.exists() and str(project).encode() in history.read_bytes(),
                         'successful open recorded in real history')
            time.sleep(.4)
            session.shot('project-open')
            assert not list(project.glob('.ox-task-*')), 'Opening started a task'
            assert (project / 'sentinel.txt').read_text() == 'preserve\n'
            record['open_preserves_project_without_task'] = True
            navigate('S01')
            session.shot('recent-project')
            for _ in range(6):
                session.key(0xFF09)
            session.shot('recent-keyboard-focus')
            session.key(0xFF09)
            session.shot('remove-keyboard-focus')
            # Existing preferences remain session-only. Exercise native theme
            # changes and return to the same project entry, including focus.
            for theme in ('dark', 'high-contrast', 'light'):
                navigate('S14')
                session.key(0xFF09)
                session.key(0xFF0D)
                navigate('S01')
                session.shot(theme)
            navigate('S02')
            session.shot('new-project-form')
            session.key(0xFF1B)
            session.shot('cancel-return')
        chord(0xFFE9, 0xFFC1)
        session.wait(lambda: app.poll() is not None, 'clean application close')
        record['exit'] = app.returncode
        assert app.returncode == 0
        record['result'] = 'observed'
except Exception as error:
    record['error'] = str(error)
    if session:
        session.shot('failure')
    raise
finally:
    if session:
        session.close()
    out.mkdir(exist_ok=True)
    (out / 'result.json').write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps({k: v for k, v in record.items() if k != 'inputs'}))
