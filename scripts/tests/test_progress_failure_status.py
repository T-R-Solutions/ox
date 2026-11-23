"""Conditional rendering must not hide failed metadata producers."""

import json
import tempfile
import unittest
from pathlib import Path

import support as S


class ProgressFailureStatusTests(unittest.TestCase):
    def test_conditional_renderer_propagates_each_jq_failure(self):
        projection = {"streams": [{"stream": "stdout", "recognized": 1,
            "unknown_records": 0, "truncated": False, "status": "nonempty",
            "display_groups": [{"source": "a.md", "target": "b.md", "count": 1}],
            "omitted_groups": 0, "omitted_occurrences": 0, "unsafe_fields": 0}]}
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "projection.json"
            path.write_text(json.dumps(projection), encoding="utf-8")
            for field in (".stream", ".recognized", ".unknown_records", ".truncated",
                          ".status", '.source//"indisponível"',
                          '.target//"indisponível"', ".count", ".omitted_groups",
                          ".omitted_occurrences", ".unsafe_fields", "formatter"):
                script = '''source "$1/lib/common.sh"
source "$1/lib/progress.sh"
rejected_filter=$3
jq() { if [[ ${2:-} == "$rejected_filter" ]]; then return 7; fi; command jq "$@"; }
if [[ $rejected_filter == formatter ]]; then progress_problem() { return 7; }; fi
if value=$(progress_governance "$2" 1); then printf 'accepted:%s' "$value"; exit 0
else exit "$?"; fi
'''
                result = S.run(["bash", "-c", script, "fixture",
                                str(S.ROOT / "scripts"), str(path), field],
                               capture_output=True)
                with self.subTest(field=field):
                    self.assertEqual(result.returncode, 2, result.stderr)
                    self.assertEqual(result.stdout, b"")
