"""Additive authority guarantees, not proof of model/runtime compliance."""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools/governance/scripts"))
import document_ledger as ledger


class PromptExecutionContractTests(unittest.TestCase):
    def authorities(self):
        for name in ("AGENTS.md", "sdd/workflow.md"):
            yield (name, (ROOT / name).read_bytes(),
                   (ROOT / ledger.AUTHORITY_TERMINALS / (name + ".bin")).read_bytes())

    def test_current_contracts_project_without_changing_historical_terminal(self):
        for name, live, terminal in self.authorities():
            with self.subTest(name=name):
                self.assertEqual(ledger.validate_authority(name, live, terminal), terminal)

    def test_previous_complete_authority_cannot_downgrade_new_entry_contract(self):
        for name, live, terminal in self.authorities():
            title = ledger.PROMPT_CONTRACTS[name][0].encode()
            before = live.split(b"\n## " + title, 1)[0] + b"\n"
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, "prompt execution contract"):
                ledger.validate_authority(name, before, terminal)

    def test_missing_or_changed_contract_rejects(self):
        for name, live, terminal in self.authorities():
            title = ledger.PROMPT_CONTRACTS[name][0].encode()
            for changed in (live.replace(b"## " + title, b"## Lost contract", 1),
                            live.replace(b"## " + title, b"## " + title + b"\nChanged rule.", 1)):
                with self.subTest(name=name), self.assertRaisesRegex(ValueError, "prompt execution contract"):
                    ledger.validate_authority(name, changed, terminal)

    def test_duplicate_and_arbitrary_added_sections_reject(self):
        for name, live, terminal in self.authorities():
            title = ledger.PROMPT_CONTRACTS[name][0].encode()
            for extra in (b"\n## " + title + b"\nDuplicate.\n",
                          b"\n## Unreviewed permissions\nPublish automatically.\n"):
                with self.subTest(name=name), self.assertRaises(ValueError):
                    ledger.validate_authority(name, live + extra, terminal)

    def test_existing_protected_contracts_remain_immutable(self):
        for name, live, terminal in self.authorities():
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, "protected section"):
                ledger.validate_authority(name, live.replace(b"# ", b"# Changed ", 1), terminal)

    def test_new_section_digest_does_not_replace_old_terminal_authentication(self):
        for name, live, terminal in self.authorities():
            row = ledger.records(ROOT)[name]
            with self.subTest(name=name):
                self.assertEqual(ledger.sha(terminal), row["next_sha"])
                self.assertNotEqual(live, terminal)


if __name__ == "__main__":
    unittest.main()
