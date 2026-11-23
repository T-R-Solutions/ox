"""Isolated headless Mutter capture of the IDE shell; never touches the primary desktop."""
import importlib.util, json, subprocess, sys, time, hashlib
from pathlib import Path
ROOT = Path("/home/rodrigo/Projetos/ox")
spec = importlib.util.spec_from_file_location("ox_native_session", ROOT / "docs/validation/f0-resumption-20261103/native-session.py")
native = importlib.util.module_from_spec(spec); spec.loader.exec_module(native)
out = ROOT / "docs/validation/ide-shell-20261118" / sys.argv[1]
monitor = sys.argv[2] if len(sys.argv) > 2 else "1600x1000"
session = native.Session(out, monitor, 1.0)
binary = ROOT / "application/target/debug/ox"
record = {"binary_sha256": hashlib.sha256(binary.read_bytes()).hexdigest(), "monitor": monitor, "steps": []}
app = None
TAB, ENTER, DOWN, SHIFT, CTRL, ALT, F10 = 0xff09, 0xff0d, 0xff54, 0xffe1, 0xffe3, 0xffe9, 0xffc7
def chord(mod, key):
    session.key(mod, True); session.key(key); session.key(mod, False); time.sleep(.25)
def go(code):
    chord(CTRL, ord("k"))
    for c in code: session.key(ord(c))
    session.key(ENTER); time.sleep(.35)
def tab(n=1, back=False):
    for _ in range(n):
        if back: chord(SHIFT, TAB)
        else: session.key(TAB); time.sleep(.08)
def shot(name):
    time.sleep(.4); session.shot(name); record["steps"].append(name)
def view_item(downs):
    # focus is on the Exibir trigger (601) after a menu action
    session.key(ENTER); time.sleep(.3)
    for _ in range(downs): session.key(DOWN); time.sleep(.05)
try:
    log = (out / "wayland.log").open("w")
    app = subprocess.Popen([str(binary)], env=dict(session.env, WAYLAND_DEBUG="1", OX_VALIDATION_SESSION="ide-shell"), cwd=ROOT, stdout=log, stderr=log)
    session.children.append(app)
    session.wait(lambda: "xdg_toplevel" in (out / "wayland.log").read_text(), "native toplevel")
    time.sleep(.8); session.key(SHIFT)
    session.wait(lambda: ".enter(" in (out / "wayland.log").read_text(), "keyboard focus")
    session.key(ALT, True); session.key(F10); session.key(ALT, False); time.sleep(.8)
    shot("01-s01-light")
    tab(4); session.key(ENTER); time.sleep(.5)
    shot("02-s12-light")
    go("s05"); shot("03-s05-light")
    chord(CTRL, ord("j")); shot("04-s05-dock-light")
    go("w00"); shot("05-w00-light")
    tab(2, back=True)  # 213 -> 602 -> 601
    session.key(ENTER); time.sleep(.4); shot("06-menu-view-light")
    for _ in range(4): session.key(DOWN); time.sleep(.05)
    session.key(ENTER); time.sleep(.4); shot("07-w00-dark")
    go("s12"); shot("08-s12-dark")
    go("s05"); shot("09-s05-dark")
    tab(2, back=True); tab(1, back=True)  # 213 -> 602 -> 601 -> 600
    session.key(ENTER); time.sleep(.3); session.key(ENTER); time.sleep(.6)
    shot("10-s01-dark")
    tab(1); session.key(ENTER); time.sleep(.6)  # 273 -> 275 Plugins
    go("s05")
    tab(2, back=True); view_item(4); session.key(ENTER); time.sleep(.4); shot("11-s05-hc")
    view_item(5); session.key(ENTER); time.sleep(.4); shot("12-s05-hc-compact")
    view_item(4); session.key(ENTER); time.sleep(.4); shot("13-s05-light-compact")
    record["result"] = "captured"
finally:
    record["events"] = len(session.events)
    (out / "record.json").write_text(json.dumps(record, indent=2) + "\n")
    session.close()
