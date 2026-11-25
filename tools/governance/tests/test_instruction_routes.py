"""Static instruction contracts and real plan-only CLI routing; no model execution.

Profiles and the workflow are checked by structure (TOML fields, existing anchors, single
location of commands, model values and rule text), never by frozen wording.
"""

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
COMMON = "sdd/workflow.md"
SKILL = ".codex/skills/commit-governance/SKILL.md"
CONFIG = ".codex/config.toml"
NORMATIVE = ("AGENTS.md", "sdd/constitution.md", "sdd/project.md", COMMON,
             "sdd/templates/task.md", "sdd/templates/spec.md")
# Profiles only point to the workflow: any script, flag or tool invocation is a copied procedure.
COMMAND_RE = re.compile(r"\b[\w-]+\.(?:py|sh)\b|(?<![\w-])--[a-z]|\b(?:python3?|cargo|git|bash)\b")
EFFORT_RE = r"\b{}\b"
SHINGLE = 8
sys.dont_write_bytecode = True


def agent_text(source):
    return (ROOT / source).read_text()


def sections(text):
    return dict(
        re.findall(r"^## ([^\n]+)\n(.*?)(?=^## |\Z)", text, re.MULTILINE | re.DOTALL)
    )


def anchors(text):
    return {
        re.sub(r"[^\w\- ]", "", h.strip().lower()).replace(" ", "-")
        for h in re.findall(r"^#{1,6} (.+)$", text, re.MULTILINE)
    }


def profiles():
    return {p.stem: tomllib.loads(p.read_text()) for p in sorted((ROOT / ".codex/agents").glob("*.toml"))}


def toml_paths():
    return [CONFIG, *sorted(str(p.relative_to(ROOT)) for p in (ROOT / ".codex/agents").glob("*.toml"))]


def normative_texts():
    """Rule text per file: whole Markdown; for TOML, comments, description and instructions."""
    texts = {path: [agent_text(path)] for path in NORMATIVE}
    for path in toml_paths():
        raw = agent_text(path)
        data = tomllib.loads(raw)
        texts[path] = [line for line in raw.splitlines() if line.lstrip().startswith("#")]
        texts[path] += [str(data[k]) for k in ("description", "developer_instructions") if k in data]
    return texts


def shingles(text):
    words = re.findall(r"\w+", text.lower())
    return {" ".join(words[i:i + SHINGLE]) for i in range(len(words) - SHINGLE + 1)}


def model_names(model):
    """Identifier and display form (`gpt-<version>-<name>` -> `<Name> <version>`) of a model."""
    names = {model}
    m = re.fullmatch(r"gpt-([\d.]+)-([a-z]+)", model)
    if m:
        names.add(f"{m.group(2).capitalize()} {m.group(1)}")
    return names


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

    def test_profiles_point_only_to_existing_workflow_roles(self):
        workflow = agent_text(COMMON)
        known = anchors(workflow)
        config = tomllib.loads(agent_text(CONFIG))
        instructions = {CONFIG: config["developer_instructions"]}
        for stem, agent in profiles().items():
            self.assertEqual(agent["name"], stem)
            for key in ("description", "model", "model_reasoning_effort"):
                self.assertTrue(str(agent.get(key, "")).strip(), f"{stem}: {key} vazio")
            instructions[stem] = agent["developer_instructions"]
            instructions[f"{stem} (description)"] = agent["description"]
        for key in ("model", "model_reasoning_effort"):
            self.assertTrue(str(config.get(key, "")).strip(), f"{CONFIG}: {key} vazio")
        for source, text in instructions.items():
            cited = re.findall(r"sdd/workflow\.md#([\w-]+)", text)
            if not source.endswith("(description)"):
                self.assertTrue(cited, f"{source}: sem âncora do workflow")
            self.assertLessEqual(set(cited), known, f"{source}: âncora inexistente")
            self.assertNotRegex(text, COMMAND_RE, f"{source}: comando ou procedimento fora do workflow")
        self.assertIsInstance(config["agents"]["max_concurrent_threads_per_session"], int)
        self.assertIn("max_concurrent_threads_per_session", workflow, "vagas lidas do config.toml")

    def test_workflow_names_exactly_the_installed_profiles(self):
        section = sections(agent_text(COMMON))["Agentes"]
        self.assertEqual(set(re.findall(r"`(ec_[a-z_]+)`", section)), set(profiles()))

    def test_model_and_effort_values_live_only_in_toml(self):
        agents = [*profiles().values(), tomllib.loads(agent_text(CONFIG))]
        models = set().union(*(model_names(str(a["model"])) for a in agents))
        efforts = {str(a["model_reasoning_effort"]) for a in agents}
        for path in NORMATIVE:
            text = agent_text(path)
            for name in models:
                self.assertNotIn(name.lower(), text.lower(), f"{path} repete o modelo {name}")
            for effort in efforts:
                self.assertNotRegex(text, EFFORT_RE.format(re.escape(effort)), f"{path} repete o esforço {effort}")

    def test_stage_8_writes_before_full_check_and_owns_the_sequence(self):
        workflow = agent_text(COMMON)
        stage = re.search(r"^### 8\. [^\n]*\n(.*?)(?=^##)", workflow, re.M | re.S).group(1)
        write, check = stage.find("--write"), stage.find("--check --require-all")
        self.assertGreaterEqual(write, 0, "etapa 8 sem --write")
        self.assertGreater(check, write, "a etapa 8 grava os hashes antes de conferir")
        everywhere = sum(agent_text(path).count("--write") for path in (*NORMATIVE, *toml_paths()))
        self.assertEqual(everywhere, stage.count("--write"), "--write só na etapa 8")
        for path in [COMMON, "sdd/templates/task.md", *toml_paths()]:
            for line in agent_text(path).splitlines():
                if "validate.py" in line and "--task" in line:
                    self.assertIn("--matrix", line, f"{path}: {line}")

    def test_no_rule_text_repeated_across_normative_files(self):
        owners = {}
        for path, parts in normative_texts().items():
            for piece in set().union(*(shingles(part) for part in parts)):
                owners.setdefault(piece, set()).add(path)
        shared = {piece: sorted(paths) for piece, paths in owners.items() if len(paths) > 1}
        self.assertEqual(shared, {}, "trecho de 8 palavras repetido: aponte para a fonte única")

    def test_template_keeps_the_tables_the_validator_reads(self):
        if str(ROOT / "sdd/tools") not in sys.path:
            sys.path.insert(0, str(ROOT / "sdd/tools"))
        sddtask = importlib.import_module("sddtask")
        task = sddtask.parse(ROOT / "sdd/templates/task.md")
        self.assertIn("Skill", task.table(5, "Item").header)
        self.assertIsNotNone(task.table(4, "SKILL.md"))
        self.assertEqual([t.header[0] for t in task.tables(8)], ["Input", "AC"])


if __name__ == "__main__":
    unittest.main()
