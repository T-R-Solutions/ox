"""Contratos do check-ox.py: mapa de skills do workflow, links locais e inspeção de conteúdo
externo (GOV-01). Raízes temporárias; stdlib."""

import hashlib
import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "tools/governance/scripts/check-ox.py"
SPEC = importlib.util.spec_from_file_location("check_ox_subject", SCRIPT)
OX = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(OX)


def sha(data):
    return hashlib.sha256(data if isinstance(data, bytes) else data.encode()).hexdigest()


class TempRoot(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, rel, data):
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(data, bytes):
            path.write_bytes(data)
        else:
            path.write_text(data)
        return path


class SkillMapTests(TempRoot):
    WORKFLOW = ("# W\n\n## Skills\n\nRegras.\n\n| Skill | Etapa | Usar quando |\n|---|---|---|\n"
                "| `alpha` | 1 | x |\n| `beta` | 4 | y |\n\nFora do perfil: `gamma` não é instalada.\n\n"
                "## Agentes\n\n| Skill | x |\n|---|---|\n| `fora-da-secao` | z |\n")

    def setUp(self):
        super().setUp()
        self.write("sdd/tools/sddtask.py", (ROOT / "sdd/tools/sddtask.py").read_bytes())
        self.write("sdd/workflow.md", self.WORKFLOW)
        self.write(".codex/skills/alpha/SKILL.md", "x")
        self.write(".codex/skills/beta/SKILL.md", "x")

    def test_inventory_equal_to_workflow_table_passes(self):
        self.assertEqual(OX.skill_errors(self.root), [])

    def test_unmapped_missing_and_excluded_skills_fail(self):
        self.write(".codex/skills/delta/SKILL.md", "x")
        self.write(".codex/skills/gamma/SKILL.md", "x")
        (self.root / ".codex/skills/beta/SKILL.md").unlink()
        errors = OX.skill_errors(self.root)
        self.assertIn("Skill not mapped in sdd/workflow.md#skills: delta", errors)
        self.assertIn("Mapped skill not installed: beta", errors)
        self.assertIn("Excluded skill installed: gamma", errors)
        self.assertNotIn("Mapped skill not installed: fora-da-secao", errors, "só a seção Skills conta")

    def test_missing_or_duplicate_table_fails(self):
        self.write("sdd/workflow.md", "# W\n\n## Skills\n\nsem tabela\n")
        self.assertEqual(OX.skill_errors(self.root), ["Skill table missing in sdd/workflow.md#skills"])
        self.write("sdd/workflow.md", self.WORKFLOW.replace("| `beta` | 4 | y |", "| `beta` | 4 | y |\n| `alpha` | 5 | z |"))
        self.assertIn("Duplicate skill in sdd/workflow.md#skills", OX.skill_errors(self.root))


class NormativeIdTests(TempRoot):
    def test_unique_ids_pass_and_duplicates_fail(self):
        self.write("sdd/constitution.md", "# C\n\n- POL-01: a.\n- GOV-01: b\n  continua.\n- RQ-01: c.\n")
        self.assertEqual(OX.normative_errors(self.root), [])
        self.write("sdd/constitution.md", "# C\n\n- POL-01: a.\n- POL-01: de novo.\n- GOV-02: x.\n")
        self.assertEqual(OX.normative_errors(self.root), ["Duplicate local normative ID: POL-01"])


class LinkTests(TempRoot):
    def setUp(self):
        super().setUp()
        self.write("sdd/tools/sddtask.py", (ROOT / "sdd/tools/sddtask.py").read_bytes())
        self.write("sdd/workflow.md", "# W\n\n### 9. Fechar\n\n### 3. Especificar (o quê e por quê)\n\n## Dup\n\n## Dup\n")

    def errors(self, text, rel="docs/a.md"):
        self.write(rel, text)
        return OX.link_errors(self.root, OX.governance_files(self.root))

    def test_valid_links_and_unicode_anchors(self):
        text = ("[w](../sdd/workflow.md#9-fechar) [e](../sdd/workflow.md#3-especificar-o-quê-e-por-quê) "
                "[d](../sdd/workflow.md#dup-1) [web](https://example.com/x) [dir](../sdd/)\n")
        self.assertEqual(self.errors(text), [])

    def test_broken_escaping_and_bad_anchor(self):
        text = "[a](missing.md) [b](../../outside.md) [c](../sdd/workflow.md#nao-existe)\n"
        errors = self.errors(text)
        self.assertEqual(errors, ["Broken/escaping link: docs/a.md: missing.md",
                                  "Broken/escaping link: docs/a.md: ../../outside.md",
                                  "Broken/escaping link: docs/a.md: ../sdd/workflow.md#nao-existe"])

    def test_code_is_ignored_and_every_markdown_is_checked(self):
        text = "```\n[x](missing.md)\n```\n`[y](missing.md)`\n"
        self.assertEqual(self.errors(text), [])
        self.assertEqual(self.errors("[z](gone.md)\n", rel="docs/antigo/old.md"),
                         ["Broken/escaping link: docs/antigo/old.md: gone.md"], "não há mais pasta isenta")


class ExternalContentTests(TempRoot):
    STUDY = "linha um do estudo\nlinha dois\nlinha tres\nlinha quatro\nlinha cinco\nlinha seis\n"

    def setUp(self):
        super().setUp()
        hashes = [sha(line.strip()) for line in self.STUDY.encode().splitlines() if line.strip()]
        self.write(OX.FINGERPRINTS, json.dumps({"estudo.md": {"sha256": sha(self.STUDY), "line_hashes": hashes}}))

    def errors(self):
        return OX.external_errors(self.root, OX.governance_files(self.root))

    def test_clean_tree_passes(self):
        self.write("docs/ok.md", "nada\n")
        self.assertEqual(self.errors(), [])

    def test_embedded_study_and_name_are_rejected(self):
        self.write("docs/copia.md", "prefixo\n" + self.STUDY + "sufixo\n")
        self.write("docs/Ox_Roadmap_Arquitetura_v0.2.md", "x")
        errors = self.errors()
        self.assertIn("External document content: docs/copia.md: estudo.md", errors)
        self.assertIn("External document name: docs/Ox_Roadmap_Arquitetura_v0.2.md", errors)

    def test_archive_content_and_unsafe_member(self):
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as z:
            z.writestr("dentro/estudo.txt", self.STUDY)
            z.writestr("../fora.txt", "x")
        self.write("docs/pacote.zip", buf.getvalue())
        errors = self.errors()
        self.assertIn("External document content: docs/pacote.zip::dentro/estudo.txt: estudo.md", errors)
        self.assertIn("Unsafe archive path: docs/pacote.zip::../fora.txt", errors)


class CliTests(TempRoot):
    def run_cli(self, *args):
        return subprocess.run([sys.executable, "-B", str(SCRIPT), *args], capture_output=True, text=True, check=False)

    def test_configuration_error_exits_2(self):
        res = self.run_cli("--root", str(self.root))
        self.assertEqual(res.returncode, 2)
        self.assertTrue(res.stdout.startswith("FAIL:"))



class RealRepositoryTests(unittest.TestCase):
    integration = True

    def test_real_repository_passes(self):
        res = subprocess.run([sys.executable, "-B", str(SCRIPT)], capture_output=True, text=True, check=False)
        self.assertEqual(res.returncode, 0, res.stdout[-4000:] + res.stderr[-2000:])
        self.assertTrue(res.stdout.startswith("PASS:"))


if __name__ == "__main__":
    unittest.main()
