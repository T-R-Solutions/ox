"""Publication must own the run directory while the visual heartbeat continues."""

import json
import unittest
from pathlib import Path

import test_terminal_progress as progress


class TerminalPublicationTests(unittest.TestCase):
    def setUp(self):
        self.fixture = progress.TerminalProgressTests()
        self.addCleanup(self.fixture.doCleanups)
        self.fixture.setUp()
        self.fixture.select_checks("ox")
        self.fixture.observe_publication()
        common = self.fixture.root / "scripts/lib/common.sh"
        original = common.read_text()
        self.assertEqual(original.count('    fixture_run_complete "$1"'), 1)
        common.write_text(original.replace('    fixture_run_complete "$1"', '''    # Observe file identity and nanosecond timestamps, including same-byte rewrites.
    find "$1" -printf '%P %i %T@ %s\\n' | sort >"${ROOT}/publication-before.txt"
    sleep 2.2
    find "$1" -printf '%P %i %T@ %s\\n' | sort >"${ROOT}/publication-after.txt"
    fixture_run_complete "$1"
    fixture_code=$?
    # Leave the observer alive across removal as well as retention.
    sleep 1.1
    return "${fixture_code}"
''', 1))

    def test_slow_publication_keeps_heartbeat_without_run_writes_and_cleans_up(self):
        result = self.fixture.run_fixture(tty=True)
        root = self.fixture.root
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            (root / "publication-before.txt").read_bytes(),
            (root / "publication-after.txt").read_bytes(),
            "The finalization observer must not write into the publisher-owned run",
        )
        self.assertRegex(result.stderr, rb"\[3/3\][^\r\n]*decorrido: 00:0[123]")
        self.assertNotIn(b"Directory not empty", result.stderr)
        self.assertNotIn(b"No such file or directory", result.stderr)
        run = Path((root / "publication-run.txt").read_text().strip())
        self.assertFalse(run.exists(), run)
        self.assertEqual(self.fixture.totals(result.stderr)[-1], 100)
        results = json.loads(self.fixture.published("results.json").read_text())
        self.assertEqual([row["check"] for row in results["results"]], ["ox"])
        observed = json.loads(self.fixture.published("progress%2Dobserved.json").read_text())
        self.assertEqual(observed["phase"], "finalization")


if __name__ == "__main__":
    unittest.main()
