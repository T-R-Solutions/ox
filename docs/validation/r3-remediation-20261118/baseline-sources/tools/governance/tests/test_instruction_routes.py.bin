"""Static instruction contracts and real plan-only CLI routing; no model execution."""

import importlib
import json
import os
import re
import shlex
import subprocess
import sys
import tomllib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BEFORE = ROOT / "docs/validation/governance-corrections-20261114/before"
COMMON = "docs/development/codex-agents.md"
SKILL = ".codex/skills/commit-governance/SKILL.md"


sys.path.insert(0, str(ROOT / 'tools/governance/scripts'))
IR = importlib.import_module('instruction_revision')


def agent_text(source):
    if IR.governance_copy(ROOT):
        row = next(row for row in IR.agent_snapshots(ROOT) if row['source'] == source)
        return (ROOT / row['snapshot']).read_text()
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
        if BEFORE.is_dir():
            previous = sections((BEFORE / f"{SKILL}.bin").read_text())[
                "Pre-commit automation choice"
            ]
            self.assertEqual(
                previous.split("- **Não:**", 1)[1].split("\n\n", 1)[0],
                no.split("\n\n", 1)[0],
            )
            failure = "Wait for completion and inspect its exit status and results."
            self.assertEqual(
                previous.split(failure, 1)[1].split("- **Não:**", 1)[0],
                yes.split(failure, 1)[1],
            )

    def test_model_effort_and_role_boundaries(self):
        config = tomllib.loads(agent_text(".codex/config.toml"))
        expected = {
            "ec_analista": ("gpt-6.1-sol", "medium"),
            "ec_analista_alta": ("gpt-6.1-sol", "high"),
            "ec_implementador": ("gpt-6.1-sol", "high"),
            "ec_implementador_extra_alto": ("gpt-6.1-sol", "xhigh"),
            "ec_orquestrador_alta": ("gpt-6-astra", "high"),
            "ec_orquestrador_normal": ("gpt-6-astra", "medium"),
            "ec_planejador": ("gpt-6.1-sol", "high"),
            "ec_planejador_alta": ("gpt-6-astra", "medium"),
            "ec_revisor": ("gpt-6.1-sol", "high"),
            "ec_testador": ("gpt-6.1-sol", "high"),
            "ec_triador": ("gpt-6.1-sol", "medium"),
            "ec_validador": ("gpt-6.1-sol", "high"),
            "ec_validador_alta": ("gpt-6-astra", "medium"),
        }
        observed = {}
        sources = [row["source"] for row in IR.agent_snapshots(ROOT) if row["source"].startswith(".codex/agents/")] if IR.governance_copy(ROOT) else [str(p.relative_to(ROOT)) for p in (ROOT / ".codex/agents").glob("*.toml")]
        for source in sources:
            path = Path(source)
            agent = tomllib.loads(agent_text(source))
            self.assertEqual(agent["name"], path.stem)
            observed[agent["name"]] = (agent["model"], agent["model_reasoning_effort"])
            self.assertIn(COMMON, agent["developer_instructions"])
        self.assertEqual(observed, expected)
        self.assertEqual((config["model"], config["model_reasoning_effort"]), ("gpt-6.1-sol", "medium"))
        self.assertEqual(config["agents"]["max_concurrent_threads_per_session"], 3)
        root = config["developer_instructions"]
        self.assertNotIn("aplica diretamente ec_triador", root)
        self.assertIn("controlador", root)
        self.assertIn("ec_orquestrador_alta", root)
        self.assertIn("bloqueie a etapa dependente", root)
        triager = tomllib.loads(agent_text(".codex/agents/ec_triador.toml"))[
            "developer_instructions"
        ]
        self.assertIn("Quando delegado", triager)
        self.assertIn("não implemente", triager)
        self.assertIn("não execute testes e não crie agentes", triager)
        for name in ("ec_validador", "ec_validador_alta"):
            instruction = tomllib.loads(agent_text(f".codex/agents/{name}.toml"))[
                "developer_instructions"
            ]
            self.assertIn("--features/--feature", instruction)
            self.assertIn("todos os gates", instruction)
            self.assertIn("não exija aprovação global", instruction)

    @unittest.skipUnless(BEFORE.is_dir(), "bounded preimages unavailable in this copy")
    def test_all_skill_methods_and_bridge_contributions_preserved(self):
        profile = json.loads((ROOT / "config/governance/profile.json").read_text())
        names = set(profile["general"]) | set(profile["conditional"]) | set(profile["new"])
        self.assertEqual(len(names), 31)
        for name in sorted(names):
            with self.subTest(skill=name):
                skill_path = f".codex/skills/{name}/SKILL.md"
                skill = (ROOT / skill_path).read_bytes()
                prior = (BEFORE / f"{skill_path}.bin").read_bytes()
                if name != "commit-governance":
                    self.assertEqual(skill, prior)
                else:
                    before_sections, after_sections = sections(prior.decode()), sections(skill.decode())
                    self.assertEqual(before_sections.keys(), after_sections.keys())
                    for title in before_sections.keys() - {"Commit workflow", "Pre-commit automation choice"}:
                        self.assertEqual(before_sections[title], after_sections[title])
                bridge_path = f"sdd/chain/{name}.md"
                bridge = (ROOT / bridge_path).read_text()
                previous = (BEFORE / f"{bridge_path}.bin").read_text()
                self.assertEqual(bridge.split("---", 2)[:2], previous.split("---", 2)[:2])
                before_sections, after_sections = sections(previous), sections(bridge)
                for title in before_sections:
                    if title in {"Completion and authority", "Inputs and contributions"}:
                        continue
                    if title == "Conditional project profile":
                        # The old file appended shared policy after this selection paragraph.
                        self.assertEqual(
                            before_sections[title].strip().split("\n\n", 1)[0],
                            after_sections[title].strip().split("\n\n", 1)[0],
                        )
                    else:
                        self.assertEqual(before_sections[title].strip(), after_sections[title].strip())
                old_contribution = before_sections.get("Inputs and contributions", "")
                new_contribution = after_sections.get("Inputs and contributions", "")
                if name == "autonomous-verification-engineering":
                    old_contribution = old_contribution.replace(
                        "Separate states: pending, approved, rejected, inconclusive, justified not applicable.", ""
                    )
                    new_contribution = new_contribution.replace(
                        "Separate domain lifecycle states (including pending) from SDD verdicts; pending is not an SDD status. Record acceptance with the five states in [evidence](../evidence.md), using UNVERIFIED when required evidence has not been collected.", ""
                    )
                self.assertEqual(old_contribution, new_contribution)
                for target in re.findall(r"\]\(([^)]+)\)", bridge):
                    if not re.match(r"[a-z]+://", target):
                        self.assertTrue(((ROOT / bridge_path).parent / target.split("#", 1)[0]).is_file(), target)


if __name__ == "__main__":
    unittest.main()
