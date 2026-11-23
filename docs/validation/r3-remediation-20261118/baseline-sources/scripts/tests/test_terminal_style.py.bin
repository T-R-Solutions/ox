"""Presentation checks reuse the controlled runner; no real scanner is invoked."""

import re
import unittest

import test_terminal_progress as progress


class TerminalStyleTests(unittest.TestCase):
    def setUp(self):
        self.runner = progress.TerminalProgressTests()
        self.runner.setUp()
        self.addCleanup(self.runner.doCleanups)
        self.runner.env.pop("NO_COLOR", None)
        self.runner.env["TERM"] = "xterm-256color"
        self.runner.select_checks("ruff")

    def test_tty_colors_labels_and_preserves_failure_exit(self):
        result = self.runner.run_fixture(
            {"ruff": {"state": "findings", "code": 1, "count": 1,
                      "assessment": {"warnings": ["retained"], "skips": [], "limits": []}}},
            tty=True,
        )
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn(b"\x1b[32mSUCESSO\x1b[0m", result.stderr)
        self.assertIn(b"\x1b[31mFALHA\x1b[0m", result.stderr)
        self.assertIn(b"\x1b[33mWARNING\x1b[0m", result.stderr)
        self.assertNotRegex(result.stderr, rb"\x1b\[(?:9[123]|1;3[123])m")
        plain = re.sub(rb"\x1b\[[0-9;]*[mK]", b"", result.stderr)
        self.assertIn(b"OX", plain)
        self.assertIn(b"    Executado:", plain)
        self.assertIn(b"    Resultado:", plain)
        columns = []
        for line in plain.decode().splitlines():
            for label in ("Executado:", "Resultado:", "WARNING"):
                if line.startswith("    " + label):
                    columns.append(len(line) - len(line[4 + len(label):].lstrip()))
        self.assertTrue(columns)
        self.assertEqual(set(columns), {22})
        summary = plain.split("RESUMO DA EXECUÇÃO".encode())[-1]
        self.assertIn(b"FALHA", summary)
        self.assertNotIn(b"SUCESSO", summary)
        self.assertEqual(result.stdout, b"")

    def test_no_color_and_dumb_remain_readable(self):
        for settings in ({"NO_COLOR": "1"}, {"TERM": "dumb"}):
            with self.subTest(settings=settings):
                result = self.runner.run_fixture(tty=True, env=settings)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertNotRegex(result.stderr, rb"\x1b\[[0-9;]*m")
                self.assertIn(b"SUCESSO", result.stderr)
                if settings.get("TERM") == "dumb":
                    self.assertNotIn(b"\x1b", result.stderr)

    def test_redirected_output_has_hierarchy_without_controls(self):
        result = self.runner.run_fixture()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn(b"\x1b", result.stderr)
        self.assertNotIn(b"\r", result.stderr)
        self.assertIn(b"    Executado:", result.stderr)
        self.assertIn(b"    Resultado:", result.stderr)

    def test_recorded_is_neutral_and_blocked_is_distinct(self):
        for state, code, label in (("recorded", 0, b"REGISTRADO"), ("blocked", 3, b"BLOQUEADA")):
            with self.subTest(state=state):
                result = self.runner.run_fixture({"ruff": {"state": state, "code": code}}, tty=True)
                self.assertEqual(result.returncode, code, result.stderr)
                self.assertIn(label, result.stderr)
                if state == "recorded":
                    self.assertNotIn(b"\x1b[32mREGISTRADO", result.stderr)
                else:
                    self.assertIn(b"\x1b[33mBLOQUEADA\x1b[0m", result.stderr)

    def test_legacy_scope_uses_same_color_projection(self):
        command = self.runner.command
        self.runner.command = lambda operation="run": command(operation)[:2] + ["--scope", "governance"]
        result = self.runner.run_fixture(tty=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(b"\x1b[32mSUCESSO\x1b[0m", result.stderr)

    def test_tty_measured_members_remain_visible_on_compact_line(self):
        self.runner.select_checks("geiger")
        result = self.runner.run_fixture(
            {"geiger": {"members": [1, 2], "total": 2, "state": "recorded"}},
            tty=True, env=self.runner.controlled_cargo(),
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        plain = re.sub(rb"\x1b\[[0-9;]*[mK]", b"", result.stderr)
        lines = [line for line in re.split(rb"[\r\n]", plain) if b"membros:" in line]
        self.assertTrue(lines, result.stderr)
        self.assertTrue(any(b"membros: 1/2" in line for line in lines))
        self.assertTrue(any(b"membros: 2/2" in line for line in lines))
        self.assertTrue(all(len(line) <= 80 for line in lines))
