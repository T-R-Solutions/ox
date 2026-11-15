"""A failed producer must not become an empty successful inventory."""

import tempfile
import unittest
from pathlib import Path

import support as S


class CaptureStatusTests(unittest.TestCase):
    def test_failed_line_producer_preserves_failure(self):
        with self.assertRaises(ValueError):
            S.shell('capture_lines rows bash -c \'printf partial; exit 17\'')

    def test_failed_nul_producer_preserves_failure(self):
        with self.assertRaises(ValueError):
            S.shell('capture_nul rows bash -c \'printf partial; exit 19\'')

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
