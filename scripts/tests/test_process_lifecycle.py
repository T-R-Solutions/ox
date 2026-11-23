"""Local supervisor lifecycle; does not prove Docker cleanup."""

import json
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

import support as S


class ProcessLifecycle(unittest.TestCase):
    def test_cancellation_waits_for_cleanup_without_affecting_parallel_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            child = root / "child.py"
            child.write_text("""import signal,time,sys
from pathlib import Path
root=Path(sys.argv[1]); name=sys.argv[2]
def stop(*args):
 time.sleep(0.2)
 (root/(name+".cleaned")).touch()
 sys.exit(130)
signal.signal(signal.SIGTERM,stop)
(root/(name+".ready")).touch()
time.sleep(1.5)
""")
            shell = 'source "$1/lib/common.sh"; source "$1/lib/process.sh"; execute "$2" "$3" "$4" "$5" "$3" "$6"'
            processes = []
            for name in ("first", "second"):
                processes.append(
                    subprocess.Popen(
                        [
                            "bash",
                            "-c",
                            shell,
                            "_",
                            str(S.ROOT / "scripts"),
                            str(root / name),
                            str(root),
                            sys.executable,
                            str(child),
                            name,
                        ],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        env=S.environment(),
                    )
                )
            try:
                deadline = time.monotonic() + 5
                while not all(
                    (root / (n + ".ready")).exists() for n in ("first", "second")
                ):
                    self.assertLess(time.monotonic(), deadline)
                    time.sleep(0.01)
                processes[0].send_signal(signal.SIGTERM)
                processes[0].communicate(timeout=5)
                self.assertTrue((root / "first.cleaned").exists())
                self.assertIsNone(processes[1].poll())
                processes[1].communicate(timeout=5)
                self.assertFalse((root / "second.cleaned").exists())
                self.assertEqual(
                    json.loads((root / "first/process.json").read_text())["exit_code"],
                    143,
                )
                self.assertEqual(
                    json.loads((root / "first/process.json").read_text())["child_exit_code"],
                    130,
                )
                self.assertEqual(
                    json.loads((root / "second/process.json").read_text())["exit_code"],
                    0,
                )
            finally:
                for proc in processes:
                    if proc.poll() is None:
                        proc.kill()
                        proc.communicate()

    def test_inherited_progress_flag_without_callbacks_still_supervises_child(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = S.run(
                ["bash", "-c",
                 'source "$1/lib/common.sh"; source "$1/lib/process.sh"; '
                 'execute "$2/output" "$2" bash -c "printf supervised; exit 7"',
                 "_", str(S.ROOT / "scripts"), str(root)],
                env=S.environment(OX_HUMAN_PROGRESS="true"), capture_output=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, b"supervised")
            self.assertNotIn(b"command not found", result.stderr)
            self.assertEqual(json.loads((root / "output/process.json").read_text())["exit_code"], 7)
