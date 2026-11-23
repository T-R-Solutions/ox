"""Focused native observation of the existing Details toggle on preferences."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent / 'final03-preferences-details'
spec = importlib.util.spec_from_file_location(
    'native', ROOT / 'docs/validation/f0-resumption-20261103/native-session.py')
native = importlib.util.module_from_spec(spec)
spec.loader.exec_module(native)
session = None
record = {'method': 'private native Mutter, keyboard navigation and Details toggle'}
try:
    session = native.Session(OUT, '1440x900', 1)
    binary = ROOT / 'application/target/debug/ox'
    paths = list((ROOT / 'application/crates/ox-ui/src').rglob('*.rs')) + [Path(__file__)]
    record['binary_sha256'] = hashlib.sha256(binary.read_bytes()).hexdigest()
    record['inputs'] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in sorted(paths)}
    with (OUT / 'application.log').open('w') as log:
        app = subprocess.Popen([str(binary)], cwd=ROOT,
            env=dict(session.env, WAYLAND_DEBUG='1', XDG_STATE_HOME=str(OUT / 'state')),
            stdout=log, stderr=log)
        session.children.append(app)
        session.wait(lambda: 'xdg_toplevel' in (OUT / 'application.log').read_text(), 'toplevel')
        time.sleep(.8)
        session.key(0xFFE1)
        session.wait(lambda: '.enter(' in (OUT / 'application.log').read_text(), 'keyboard focus')
        session.key(0xFFE3, True)
        session.key(ord('k'))
        session.key(0xFFE3, False)
        for char in 'S14':
            session.key(ord(char))
        session.key(0xFF0D)
        session.shot('preferences-default')
        for _ in range(3):
            session.key(0xFF09)
        session.key(0xFF0D)
        session.shot('preferences-details')
        session.key(0xFF0D)
        session.shot('preferences-details-hidden')
        session.key(0xFFE9, True)
        session.key(0xFFC1)
        session.key(0xFFE9, False)
        session.wait(lambda: app.poll() is not None, 'natural exit')
        assert app.returncode == 0
        record['natural_exit'] = app.returncode
        record['inputs_stable'] = all(hashlib.sha256((ROOT / p).read_bytes()).hexdigest() == h
                                      for p, h in record['inputs'].items())
        record['result'] = 'observed; inspect captures for toggle states'
finally:
    if session:
        session.close()
    OUT.mkdir(exist_ok=True)
    (OUT / 'result.json').write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps({k: v for k, v in record.items() if k != 'inputs'}))
