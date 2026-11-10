"""Ox leaves SELinux relabel selection to the caller, as the consumer guide requires."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]


class SelinuxTransport(unittest.TestCase):
    def invoke(self, command='exec', override=None, code=0):
        with tempfile.TemporaryDirectory() as folder:
            tool = Path(folder) / 'toolbox'
            tool.write_text('#!/bin/sh\nprintf "%s" "${TOOLBOX_SELINUX_LABEL-unset}"\nexit '+str(code)+'\n')
            tool.chmod(0o700)
            env = dict(os.environ, TOOLBOX_BIN=str(tool))
            env.pop('TOOLBOX_SELINUX_LABEL', None)
            if override is not None:
                env['TOOLBOX_SELINUX_LABEL'] = override
            return subprocess.run(['bash', str(ROOT/'scripts/toolbox.sh'), command], env=env, capture_output=True)

    def test_exec_does_not_select_label(self):
        self.assertEqual(self.invoke().stdout, b'unset')

    def test_explicit_policy_is_preserved(self):
        for policy in ('', 'private', 'shared'):
            with self.subTest(policy=policy):
                self.assertEqual(self.invoke(override=policy).stdout, policy.encode())

    def test_non_exec_does_not_select_label(self):
        self.assertEqual(self.invoke('central').stdout, b'unset')

    def test_public_wrapper_preserves_failure(self):
        self.assertEqual(self.invoke(code=125).returncode, 125)
