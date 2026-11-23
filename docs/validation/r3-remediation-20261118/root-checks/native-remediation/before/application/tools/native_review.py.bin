"""Isolated native Wayland workbench review; never drives the primary desktop.

Reuses the preserved Mutter/RemoteDesktop/PipeWire session mechanism. Dependencies:
Mutter, PyGObject/GStreamer, Pillow and the current local Cargo build.
"""
import argparse
import hashlib
import importlib.util
import json
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "docs/validation/visual-workbench-20261111"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", action="store_true")
    parser.add_argument("--output", default="native-review")
    parser.add_argument("--binary", type=Path)
    parser.add_argument("--monitor", default="1600x1000")
    parser.add_argument("--scale", type=float, default=1)
    parser.add_argument("--capture-only", action="store_true")
    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location(
        "ox_native_session", ROOT / "docs/validation/f0-resumption-20261103/native-session.py"
    )
    native = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(native)
    output = BASE / args.output
    if output.exists():
        raise SystemExit("Output already exists; preserve observations and choose a new name")
    session = None
    record = {"method": "isolated native Wayland via Mutter RemoteDesktop and PipeWire", "baseline": args.baseline}
    log = None
    app = None
    try:
        session = native.Session(output, args.monitor, args.scale)
        binary = args.binary or ROOT / "application/target/debug/ox"
        record["binary_sha256"] = hashlib.sha256(binary.read_bytes()).hexdigest()
        log = (output / "wayland.log").open("w")
        env = dict(session.env, WAYLAND_DEBUG="1", OX_VALIDATION_SESSION=args.output)
        app = subprocess.Popen([str(binary)], env=env, cwd=ROOT, stdout=log, stderr=log)
        session.children.append(app)
        session.wait(lambda: "xdg_toplevel" in (output / "wayland.log").read_text(), "native toplevel")
        time.sleep(0.7)
        session.key(0xFFE1)
        session.wait(lambda: ".enter(" in (output / "wayland.log").read_text(), "keyboard focus")
        # Same maximized monitor and scale for baseline/candidate comparison.
        session.key(0xFFE9, True)
        session.key(0xFFC7)  # F10
        session.key(0xFFE9, False)
        time.sleep(0.5)
        session.shot("initial")
        if args.capture_only:
            record["capture_only"] = True
        elif args.baseline:
            session.key(0xFF09)
            session.key(0xFF0D)
            time.sleep(0.2)
            session.shot("details")
            session.key(0xFF09)
            session.key(0xFF0D)
            session.wait(lambda: app.poll() is not None, "supervised exit")
            if app.returncode != 0:
                raise RuntimeError("Baseline did not exit successfully")
        else:
            def chord(mod, key):
                session.key(mod, True)
                session.key(key)
                session.key(mod, False)
            def navigate(code):
                chord(0xFFE3, ord("k"))
                for char in code:
                    session.key(ord(char))
                session.key(0xFF0D)
                time.sleep(.2)
            # Every destination is entered by real keyboard input.
            codes = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S08", "S09", "S10", "S11", "S12", "S13", "S14", "W00", "A01", "A02", "A03", "A04", "A05", "A06", "TW01", "TW02", "TW03", "TW04", "SDD", "SKL"]
            for code in codes:
                navigate(code)
                session.shot(code)
            navigate("S14")
            # Navigate returns focus to command trigger, then theme/density.
            session.key(0xFF09)
            session.key(0xFF0D)
            session.shot("dark")
            session.key(0xFF0D)
            session.shot("high-contrast")
            session.key(0xFF09)
            session.key(0xFF0D)
            session.shot("compact-hc")
            chord(0xFFE3, ord("k"))
            session.shot("command-focus")
            session.key(0xFF1B)
            session.shot("escape-return")
            navigate("S04")
            for _ in range(5):
                session.key(0xFF09)
            fixture=output / "workspace"
            fixture.mkdir()
            for char in str(fixture):
                session.key(ord(char))
            session.key(0xFF0D)
            time.sleep(.8)
            session.key(0xFF09)
            session.key(0xFF09)
            session.key(0xFF0D)
            session.wait(lambda:bool(list(fixture.rglob("candidate.txt"))) or bool(list(fixture.rglob("result.txt"))), "task artifact")
            time.sleep(.5)
            session.shot("task-executed")
            record["artifacts"]=[{"path":str(p.relative_to(output)),"sha256":hashlib.sha256(p.read_bytes()).hexdigest()} for p in fixture.rglob("*") if p.is_file()]
            for _ in range(4):
                session.key(0xFF09)
            session.key(0xFF0D)
            time.sleep(.8)
            session.shot("task-verified")
            chord(0xFFE9,0xFFC1) # Alt+F4, supervised close
            session.wait(lambda:app.poll() is not None,"supervised exit")
            record["events"]=session.events
        record["result"] = "observed"
    except Exception as error:
        record["error"] = str(error)
        raise
    finally:
        if app is not None:
            record["natural_exit"] = app.poll()
        if session is not None:
            session.close()
        if log is not None:
            log.close()
        output.mkdir(exist_ok=True)
        (output / "result.json").write_text(json.dumps(record, indent=2) + "\n")
        print(json.dumps(record), flush=True)


if __name__ == "__main__":
    main()
