"""Real opt-in consumer scans; central OSV may acquire its database automatically."""
import json
import os
import unittest

import support as S


@unittest.skipUnless(os.environ.get('OX_REAL_SECURITY') == '1', 'requires explicitly enabled central images and Docker')
class RealSecurity(unittest.TestCase):
    def test_native_scans(self):
        registry = S.run([str(S.ROOT/'scripts/toolbox.sh'), 'central', 'list'], capture_output=True,
                         env=dict(os.environ), timeout=120)
        self.assertEqual(registry.returncode, 0, registry.stderr)
        self.assertTrue(json.loads(registry.stdout), 'No central active revisions; zero scanner operations available')
        catalog = json.loads((S.ROOT / 'scripts/config/automation.json').read_text())
        for name in ('ruff','bandit','gitleaks','history','shellcheck','opengrep','osv','trivy','grype','sbom','malware'):
            with self.subTest(check=name):
                run=S.run(['bash',str(S.ROOT/'scripts/checks/run.sh'),'--check',name],capture_output=True,
                          env=dict(os.environ), timeout=catalog["checks"][name].get(
                              "native_timeout", catalog["runtime"]["native_timeout"]) + 600)
                # Findings are valid operational outcomes; blocked/error are not.
                self.assertIn(run.returncode,(0,1),run.stderr.decode(errors='replace'))
