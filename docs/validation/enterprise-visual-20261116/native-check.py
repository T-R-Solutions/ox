"""Observe the real Ox in private Mutter; never drive the primary desktop."""
import argparse
import hashlib
import importlib.util
import json
import re
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parents[3]
BASE = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--name', required=True)
    parser.add_argument('--monitor', default='1440x900')
    parser.add_argument('--scale', type=float, default=1)
    parser.add_argument('--binary', type=Path, default=ROOT / 'application/target/debug/ox')
    parser.add_argument('--exercise', action='store_true')
    parser.add_argument('--capture-only', action='store_true')
    parser.add_argument('--compact', action='store_true')
    parser.add_argument('--maximize', action='store_true',
                        help='Maximize a known initially windowed large-monitor session')
    parser.add_argument('--manual-tabs', type=int, default=2,
                        help='Observed Start traversal from Open to manual entry')
    parser.add_argument('--theme-tabs', type=int, default=1,
                        help='Observed traversal after command navigation to appearance')
    args = parser.parse_args()
    out = BASE / args.name
    if out.exists():
        raise SystemExit('Preserve earlier observations: choose a fresh --name')
    spec = importlib.util.spec_from_file_location(
        'private_native', ROOT / 'docs/validation/f0-resumption-20261103/native-session.py')
    native = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(native)
    inputs = list((ROOT / 'application/crates/ox-ui/src').rglob('*.rs'))
    inputs += list((ROOT / 'application/crates/ox-ui/assets').rglob('*'))
    inputs += [ROOT / 'application/Cargo.lock', ROOT / 'application/Cargo.toml',
               ROOT / 'application/crates/ox-ui/Cargo.toml', Path(__file__),
               ROOT / 'docs/validation/f0-resumption-20261103/native-session.py']
    record = {
        'method': 'real native Wayland window, isolated Mutter/RemoteDesktop/PipeWire',
        'monitor': args.monitor, 'scale': args.scale, 'exercise': args.exercise,
        'binary_sha256': digest(args.binary),
        'inputs_at_start': {str(p.relative_to(ROOT)): digest(p)
                            for p in sorted(inputs) if p.is_file()},
        'limitations': ['No AT or X11 observation',
                        'Source/binary correspondence requires the recorded build command',
                        'Captures require visual inspection; exit zero is not visual acceptance'],
    }
    session = None
    app = None
    try:
        session = native.Session(out, args.monitor, args.scale)

        def chord(mod, key):
            session.key(mod, True)
            session.key(key)
            session.key(mod, False)

        def type_text(value):
            for char in value:
                session.key(ord(char))

        def tabs(count):
            for _ in range(count):
                session.key(0xFF09)

        def navigate(code):
            chord(0xFFE3, ord('k'))
            type_text(code)
            session.key(0xFF0D)
            time.sleep(.35)

        with (out / 'application.log').open('w') as log:
            app = subprocess.Popen([str(args.binary)], cwd=ROOT,
                env=dict(session.env, WAYLAND_DEBUG='1', XDG_STATE_HOME=str(out / 'state')),
                stdout=log, stderr=log)
            session.children.append(app)
            session.wait(lambda: 'xdg_toplevel' in (out / 'application.log').read_text(),
                         'native toplevel')
            time.sleep(.8)
            session.key(0xFFE1)
            session.wait(lambda: '.enter(' in (out / 'application.log').read_text(),
                         'keyboard focus')
            # Mutter maximizes when the initial window nearly fills the monitor,
            # but leaves the default 1280-wide window unmaximized on ultrawide.
            if args.maximize:
                chord(0xFFE9, 0xFFC7)
                time.sleep(.5)
            configures = re.findall(r'xdg_toplevel#\d+\.configure\((\d+), (\d+),',
                                    (out / 'application.log').read_text())
            record['initial_window_configure'] = [int(v) for v in configures[-1]]
            session.shot('initial')
            surfaces = () if args.capture_only else (
                'S02', 'W00', 'S04', 'S13', 'S14', 'A01', 'S08', 'A03', 'A04', 'TW03')
            for code in surfaces:
                navigate(code)
                session.shot(code)
                assert app.poll() is None, f'App exited on {code}'
            if not args.capture_only:
                navigate('W00')
                chord(0xFFE3, ord('k'))
                session.shot('command-palette')
                session.key(0xFF1B)
                session.shot('command-escape')
            if args.exercise:
                navigate('S01')
                tabs(args.manual_tabs)
                session.shot('manual-trigger-focus')
                session.key(0xFF0D)
                session.shot('manual-entry')
                project = out / 'project-with-a-long-readable-local-name'
                project.mkdir()
                sentinel = project / 'sentinel.txt'
                sentinel.write_text('preserve existing user content\n')
                type_text(str(project))
                session.shot('manual-filled')
                session.key(0xFF0D)
                history = out / 'state/ox/recent-projects.v1'
                session.wait(lambda: history.exists() and str(project).encode() in history.read_bytes(),
                             'actual successful open recorded in history')
                time.sleep(.4)
                session.shot('project-opened')
                assert sentinel.read_text() == 'preserve existing user content\n'
                assert not list(project.glob('.ox-task-*')), 'Opening executed a task'
                record['open_preserves_sentinel_without_task'] = True
                record['history_sha256'] = digest(history)
                navigate('S01')
                session.shot('recent-project')
                # Traverse the complete entry controls, including any recent rows;
                # captures expose focus and scroll reveal for independent review.
                for index in range(1, 10):
                    tabs(1)
                    session.shot(f'entry-focus-{index:02}')
                for theme in ('dark', 'high-contrast', 'light'):
                    navigate('S14')
                    tabs(args.theme_tabs)
                    session.key(0xFF0D)
                    session.shot(f'settings-{theme}')
                    navigate('S01')
                    session.shot(f'welcome-{theme}')
                    navigate('W00')
                    session.shot(f'editor-{theme}')
                navigate('S02')
                session.shot('new-project-focused')
                for index in range(1, 5):
                    tabs(1)
                    session.shot(f'creation-focus-{index:02}')
                session.key(0xFF1B)
                session.shot('creation-escape')
                assert not list(project.glob('.ox-task-*'))
            if args.compact:
                navigate('S14')
                tabs(args.theme_tabs + 1)
                session.key(0xFF0D)
                session.shot('settings-compact')
                navigate('S01')
                session.shot('welcome-compact')
                navigate('W00')
                session.shot('editor-compact')
            chord(0xFFE9, 0xFFC1)
            session.wait(lambda: app.poll() is not None, 'natural supervised close')
            assert app.returncode == 0, f'Exit {app.returncode}'
            record['natural_exit'] = app.returncode
            record['result'] = 'observed'
    except Exception as error:
        record['error'] = str(error)
        if session:
            session.shot('failure')
        raise
    finally:
        if session:
            session.close()
        record['inputs_at_end'] = {str(p.relative_to(ROOT)): digest(p)
                                  for p in sorted(inputs) if p.is_file()}
        record['sources_stable_during_observation'] = (
            record['inputs_at_start'] == record['inputs_at_end'])
        out.mkdir(exist_ok=True)
        (out / 'result.json').write_text(json.dumps(record, indent=2) + '\n')
        print(json.dumps({k: v for k, v in record.items() if not k.startswith('inputs_')}))


if __name__ == '__main__':
    main()
