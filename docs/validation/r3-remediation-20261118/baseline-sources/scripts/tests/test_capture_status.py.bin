"""A failed producer must not become an empty successful inventory."""

import tempfile
import unittest
from pathlib import Path

import support as S


class CaptureStatusTests(unittest.TestCase):
    def test_failed_line_producer_preserves_failure(self):
        with S.rejected(self, returncode=17):
            S.shell('capture_lines rows bash -c \'printf partial; exit 17\'')

    def test_failed_nul_producer_preserves_failure(self):
        with S.rejected(self, returncode=19):
            S.shell('capture_nul rows bash -c \'printf partial; exit 19\'')

    def test_missing_function_has_distinct_status(self):
        with S.rejected(self, returncode=127, message="command not found"):
            S.shell('unset -f capture_lines; capture_lines rows true')

    def test_previous_assessment_cannot_satisfy_a_new_run(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            previous = root / '.local/logs/2026-11-17/ox-security-previous--assessment.json.log'
            previous.parent.mkdir(parents=True)
            previous.write_text('{"state":"passed"}', encoding="utf-8")
            before = S.published_assessments(root)
            with self.assertRaisesRegex(AssertionError, "exactly one new assessment"):
                S.current_assessment(root, before)

    def test_empty_line_inventory_remains_empty(self):
        self.assertEqual(S.shell('capture_lines rows true; printf "%s" "${#rows[@]}"'), b'0')

    def test_nul_inventory_preserves_newlines_and_empty_fields(self):
        self.assertEqual(S.shell('capture_nul rows printf \'a\\nb\\0\\0\'; '
                                 'printf "%s:%s" "${#rows[@]}" "${rows[0]}"'), b'2:a\nb')

    def test_cargo_home_utility_is_available_when_absent_from_path(self):
        with tempfile.TemporaryDirectory() as temporary:
            binary = Path(temporary) / 'bin/cargo-geiger'
            binary.parent.mkdir()
            binary.write_text('#!/bin/sh\nexit 0\n')
            binary.chmod(0o700)
            selected = S.shell('source "$1/lib/backends.sh"; TOOL=cargo-geiger; '
                               'EXECUTOR=native; CARGO_HOME=$2; PATH=/usr/bin:/bin; '
                               'unset OX_CARGO_BIN; select_backend; '
                               'printf "%s" "$TOOL_BIN"', S.ROOT / 'scripts', temporary)
            self.assertEqual(selected.decode(), str(binary))
