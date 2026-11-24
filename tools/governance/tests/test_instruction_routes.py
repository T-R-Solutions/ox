"""Static instruction contracts and real plan-only CLI routing; no model execution."""

import json
import os
import re
import shlex
import subprocess
import tomllib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
COMMON = "sdd/workflow.md"
SKILL = ".codex/skills/commit-governance/SKILL.md"


def agent_text(source):
    return (ROOT / source).read_text()


def sections(text):
    return dict(
        re.findall(r"^## ([^\n]+)\n(.*?)(?=^## |\Z)", text, re.MULTILINE | re.DOTALL)
    )


def complete_recipe(text):
    """Read the documented command as argv, never evaluate its shell source."""
    section = sections(text)["Local full-verification environment"]
    block = re.search(r"```bash\n(.*?)```", section, re.DOTALL).group(1)
    tokens = shlex.split(block.replace("\\\n", " "))
    environment = {}
    while tokens and re.match(r"^[A-Z_]+=", tokens[0]):
        key, value = tokens.pop(0).split("=", 1)
        environment[key] = value.replace("$PWD", str(ROOT))
    return environment, tokens


class InstructionRoutes(unittest.TestCase):
    def test_commit_affirmative_resolves_current_complete_recipe(self):
        skill = (ROOT / SKILL).read_text()
        choice = sections(skill)["Pre-commit automation choice"]
        yes = choice.split("- **Sim:**", 1)[1].split("- **Não:**", 1)[0]
        self.assertIn("`AGENTS.md`", yes)
        self.assertIn("`scripts/README.md`", yes)
        self.assertIn("Local full-verification", yes)
        # A copied executable command reintroduces a second recipe owner.
        self.assertNotRegex(yes, r"`(?:bash |\./)?scripts/automate\.sh[^`]*`")
        environment, argv = complete_recipe((ROOT / "AGENTS.md").read_text())
        self.assertEqual(argv, ["./scripts/automate.sh", "run", "--scope", "complete"])
        self.assertEqual(
            set(environment), {"TOOLBOX_BIN", "TOOLBOX_SELINUX_LABEL", "CARGO_HOME"}
        )
        self.assertEqual(environment["TOOLBOX_SELINUX_LABEL"], "shared")
        self.assertTrue(Path(environment["TOOLBOX_BIN"]).is_absolute())
        self.assertEqual(environment["CARGO_HOME"], str(ROOT / ".cache/ox/cargo-home"))

    def test_plan_only_selection_matches_catalog_without_running_checks(self):
        environment, argv = complete_recipe((ROOT / "AGENTS.md").read_text())
        argv[1] = "plan"
        run = subprocess.run(
            ["/bin/bash", *argv],
            cwd=ROOT,
            env=dict(os.environ, **environment),
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(run.returncode, 0, run.stderr)
        planned = json.loads(run.stdout)
        names = [row[0] for row in planned]
        catalog = json.loads((ROOT / "scripts/config/automation.json").read_text())
        expected = {
            name
            for surface in catalog["selection"]["surfaces"].values()
            for name in surface
        }
        self.assertEqual(set(names), expected)
        self.assertEqual(len(names), len(set(names)))
        self.assertTrue(set(catalog["selection"]["complete_only"]) <= set(names))
        legacy = subprocess.run(
            ["/bin/bash", "scripts/automate.sh", "--scope", "full", "--plan"],
            cwd=ROOT,
            env=dict(os.environ, **environment),
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(legacy.returncode, 0, legacy.stderr)
        legacy_names = [row[0] for row in json.loads(legacy.stdout)]
        self.assertEqual(legacy_names, catalog["scopes"]["full"])
        self.assertLess(set(legacy_names), set(names))

    def test_commit_choice_safety_and_negative_route_preserved(self):
        choice = sections((ROOT / SKILL).read_text())["Pre-commit automation choice"]
        self.assertIn("**Sim** and **Não**", choice)
        self.assertIn("No answer, a timeout or a preselected option is\nnot consent", choice)
        self.assertIn("already explicitly settled the choice", choice)
        self.assertIn("that instruction takes precedence", choice)
        yes, no = choice.split("- **Sim:**", 1)[1].split("- **Não:**", 1)
        self.assertIn("exit code 0", yes)
        self.assertIn("block every commit", yes)
        self.assertIn("Do not silently reduce", yes)
        self.assertIn("do not substitute automatic individual validators", no)

    def test_model_effort_and_role_boundaries(self):
        config = tomllib.loads(agent_text(".codex/config.toml"))
        expected = {
            "ec_implementador": ("gpt-6.1-sol", "high"),
            "ec_implementador_extra_alto": ("gpt-6.1-sol", "xhigh"),
            "ec_orquestrador_alta": ("gpt-6-astra", "high"),
            "ec_orquestrador_normal": ("gpt-6-astra", "medium"),
            "ec_planejador": ("gpt-6.1-sol", "high"),
            "ec_verificador": ("gpt-6.1-sol", "high"),
        }
        workflow = agent_text(COMMON)
        headings = {
            re.sub(r"[^\w\- ]", "", h.strip().lower()).replace(" ", "-")
            for h in re.findall(r"^#{1,6} (.+)$", workflow, re.MULTILINE)
        }
        observed = {}
        for path in sorted((ROOT / ".codex/agents").glob("*.toml")):
            agent = tomllib.loads(path.read_text())
            self.assertEqual(agent["name"], path.stem)
            observed[agent["name"]] = (agent["model"], agent["model_reasoning_effort"])
            instruction = agent["developer_instructions"]
            self.assertIn(COMMON, instruction)
            anchors = re.findall(r"#(papel-[a-z]+)", instruction)
            self.assertTrue(anchors, f"{path.name} sem âncora de papel")
            self.assertLessEqual(set(anchors), headings, f"{path.name} cita âncora inexistente")
            self.assertNotIn("procedimento", instruction)
        self.assertEqual(observed, expected)
        for name in expected:
            self.assertIn(f"`{name}`", workflow, f"{name} ausente da seção Agentes")
        self.assertEqual((config["model"], config["model_reasoning_effort"]), ("gpt-6.1-sol", "medium"))
        self.assertEqual(config["agents"]["max_concurrent_threads_per_session"], 3)
        root = config["developer_instructions"]
        self.assertIn(COMMON, root)
        self.assertIn("ec_orquestrador_alta", root)
        self.assertIn("ec_verificador", root)
        self.assertIn("bloqueie a etapa dependente", root)
        verifier = tomllib.loads(agent_text(".codex/agents/ec_verificador.toml"))["developer_instructions"]
        self.assertIn("Não edite implementação", verifier)
        self.assertNotIn("sddtask.py evidence", verifier, "o verificador devolve linhas sem hashes")
        self.assertIn("sem hashes", verifier)
        self.assertIn("a skill do item", verifier)

    def test_stage_8_sequence_and_item_skill(self):
        workflow = agent_text(COMMON)

        def stage(title):
            return re.search(rf"^### {title}\n(.*?)(?=^##)", workflow, re.M | re.S).group(1)

        self.assertIn("roda `--write` e depois `--check --require-all`", stage(r"8\. Validar"))
        self.assertIn("etapa 8, passo 2", stage("Papel orquestrador"))
        self.assertNotRegex(workflow, r"\b9\.[12]\b", "etapa 8 não depende de passos da etapa 9")
        self.assertIn("documentação afetada", stage(r"7\. Executar"))
        for name in ("ec_orquestrador_normal", "ec_orquestrador_alta"):
            text = tomllib.loads(agent_text(f".codex/agents/{name}.toml"))["developer_instructions"]
            self.assertIn("sddtask.py evidence --task <ID> --write e depois --check --require-all", text, name)
        self.assertIn("skill", stage(r"5\. Quebrar em itens de trabalho"))
        self.assertIn("todo item tem teste, condição de pronto e skill", workflow)
        self.assertIn("itens `T-n` com a skill", stage("Delegação"))
        for name in ("ec_implementador", "ec_implementador_extra_alto"):
            text = tomllib.loads(agent_text(f".codex/agents/{name}.toml"))["developer_instructions"]
            self.assertIn("Use a skill indicada no item", text, name)
        template = agent_text("sdd/templates/task.md")
        self.assertIn("| Item | D | Arquivos (dono) | Depende de | Teste | Pronto quando | Skill |", template)
        for path in [COMMON, "sdd/templates/task.md", *sorted(str(p.relative_to(ROOT)) for p in (ROOT / ".codex/agents").glob("*.toml"))]:
            for line in agent_text(path).splitlines():
                if "validate.py" in line and "--task" in line:
                    self.assertIn("--matrix", line, f"{path}: {line}")


if __name__ == "__main__":
    unittest.main()
