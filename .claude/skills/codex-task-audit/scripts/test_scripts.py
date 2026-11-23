#!/usr/bin/env python3
"""Testes dos scripts da skill em repositórios Git temporários (stdlib apenas).

Execute: python3 -I .claude/skills/codex-task-audit/scripts/test_scripts.py -v
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
INVENTORY = HERE / "task_inventory.py"
SIGNALS = HERE / "diff_signals.py"


def sh(cwd: Path, *args: str) -> None:
    subprocess.run(args, cwd=cwd, check=True, capture_output=True)


def run(script: Path, root: Path, *extra: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, "-I", str(script), "--root", str(root), *extra],
                          capture_output=True, text=True, check=False)


class Repo:
    def __init__(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        sh(self.root, "git", "init", "-q")
        sh(self.root, "git", "config", "user.email", "t@example.invalid")
        sh(self.root, "git", "config", "user.name", "t")

    def write(self, rel: str, text: str) -> None:
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)

    def commit(self) -> None:
        sh(self.root, "git", "add", "-A")
        sh(self.root, "git", "commit", "-q", "-m", "base")

    def close(self) -> None:
        self.tmp.cleanup()


LOG_V1 = "---\n## 2026-11-17T10:00:00-03:00 — Primeira\n\n- Pedido: x em `src/a.py`.\n"

PLANNING = """# Corrigir a()

## Plano

1. Alterar `src/a.py` para retornar 2.
2. Atualizar `docs/a.md`.

## Critérios de finalização

- [ ] `a()` retorna 2.
- [x] Teste em `tests/test_a.py` cobre o caso.

```text
- item dentro de bloco de código não é critério
```

## Riscos

- nenhum item daqui é critério
"""

COMPLETED = """# Concluído

- Alterado `src/a.py` (`src/a.py:2`).
- Testes em [teste](tests/test_a.py); versão `0.13` sem impacto.
"""


class InventoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = Repo()
        self.repo.write("src/a.py", "def a():\n    return 1\n")
        self.repo.write("tests/test_a.py", "x = 1\n")
        self.repo.write("task_finalizada.md", LOG_V1)
        self.repo.commit()
        self.repo.write(".ai/task_planning.md", PLANNING)
        self.repo.write(".ai/task_completed.md", COMPLETED)

    def tearDown(self) -> None:
        self.repo.close()

    def inventory(self) -> dict:
        res = run(INVENTORY, self.repo.root)
        self.assertEqual(res.returncode, 0, res.stderr)
        return json.loads(res.stdout)

    def test_happy_path_criteria_and_paths_match(self) -> None:
        self.repo.write("src/a.py", "def a():\n    return 2\n")
        self.repo.write("tests/test_a.py", "x = 2\n")
        inv = self.inventory()
        self.assertEqual(inv["ai"]["planning"]["title"], "Corrigir a()")
        self.assertEqual([(c["text"][:7], c["checked"]) for c in inv["criteria"]],
                         [("`a()` r", False), ("Teste e", True)])
        self.assertEqual(inv["reported_paths"], ["src/a.py", "tests/test_a.py"], "versão 0.13 não é caminho")
        self.assertEqual(inv["changed_uncited"], [])
        self.assertEqual(inv["cited_without_change"], [])
        self.assertEqual(inv["planned_not_reported"], ["docs/a.md"])
        self.assertEqual([c["path"] for c in inv["changes"]], ["src/a.py", "tests/test_a.py"], ".ai/ fica fora")
        self.assertEqual(inv["warnings"], [])

    def test_cited_without_change_and_uncited_change(self) -> None:
        self.repo.write(".ai/task_completed.md", COMPLETED + "- Criado `src/ghost.py`.\n")
        self.repo.write("src/b.py", "y = 1\n")
        inv = self.inventory()
        self.assertEqual([c["path"] for c in inv["changed_uncited"]], ["src/b.py"])
        missing = {c["path"]: c["exists"] for c in inv["cited_without_change"]}
        self.assertEqual(missing, {"src/a.py": True, "src/ghost.py": False, "tests/test_a.py": True})

    def test_missing_or_empty_ai_file_fails(self) -> None:
        (self.repo.root / ".ai/task_completed.md").unlink()
        res = run(INVENTORY, self.repo.root)
        self.assertEqual(res.returncode, 2)
        self.assertIn("task_completed.md ausente", res.stderr)
        self.repo.write(".ai/task_completed.md", "\n  \n")
        res = run(INVENTORY, self.repo.root)
        self.assertEqual(res.returncode, 2)
        self.assertIn("vazio", res.stderr)

    def test_planning_without_criteria_warns(self) -> None:
        self.repo.write(".ai/task_planning.md", "# X\n\n## Plano\n\n- fazer algo\n")
        inv = self.inventory()
        self.assertEqual(inv["criteria"], [])
        self.assertEqual(len(inv["warnings"]), 1)

    def test_append_only_preserved_and_violation(self) -> None:
        self.assertEqual(self.inventory()["task_log"]["append_only"]["HEAD"], "sem alteração")
        self.repo.write("task_finalizada.md", LOG_V1 + "\n## 2026-11-17T11:00:00-03:00 — Segunda\n")
        log = self.inventory()["task_log"]
        self.assertTrue(log["changed"])
        self.assertEqual(log["append_only"]["HEAD"], "prefixo preservado")
        self.repo.write("task_finalizada.md", LOG_V1.replace("Primeira", "Reescrita"))
        self.assertTrue(self.inventory()["task_log"]["append_only"]["HEAD"].startswith("VIOLAÇÃO"))

    def test_not_a_repo(self) -> None:
        with tempfile.TemporaryDirectory() as plain:
            res = run(INVENTORY, Path(plain))
            self.assertEqual(res.returncode, 2)
            self.assertIn("git", res.stderr)

    def test_markdown_output(self) -> None:
        res = run(INVENTORY, self.repo.root, "--format", "md")
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertIn("# Inventário da task — Corrigir a()", res.stdout)
        self.assertIn("rodada 1", res.stdout)


class SignalTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = Repo()
        self.repo.write("crate/src/lib.rs", "pub fn old() {}\n")
        self.repo.write("crate/tests/it.rs", "#[test]\nfn t() { old(); }\n")
        self.repo.commit()

    def tearDown(self) -> None:
        self.repo.close()

    def signals(self, *extra: str) -> dict:
        res = run(SIGNALS, self.repo.root, *extra)
        self.assertEqual(res.returncode, 0, res.stderr)
        return json.loads(res.stdout)

    def test_flags_debt_and_skips_unwrap_in_tests(self) -> None:
        self.repo.write("crate/src/lib.rs", "pub fn old() {}\n#[allow(dead_code)]\nfn fresh() { let _ = x.unwrap(); } // TODO\n"
                        "#[cfg(test)]\nmod tests { fn t() { y.unwrap(); } }\n")
        out = self.signals()
        names = {(f["signal"], f["line"]) for f in out["findings"]}
        self.assertIn(("dead-code-allow", 2), names)
        self.assertIn(("unwrap-expect", 3), names)
        self.assertIn(("todo", 3), names)
        self.assertNotIn(("unwrap-expect", 5), names, "unwrap em #[cfg(test)] não é sinal")
        self.assertEqual([u["function"] for u in out["new_functions_not_named_in_tests"]], ["fresh"])

    def test_untracked_shell_dead_handler_and_artifact(self) -> None:
        self.repo.write("scripts/x.sh", "#!/bin/bash\nf() {\n  x=${y} || fail 'nunca'\n}\n")
        self.repo.write("scripts/__pycache__/m.cpython-313.pyc", "bin")
        out = self.signals()
        self.assertTrue(any(f["signal"] == "dead-handler" and f["path"] == "scripts/x.sh" for f in out["findings"]))
        self.assertIn("scripts/__pycache__/m.cpython-313.pyc", out["artifacts_in_diff"])

    def test_clean_tree_has_no_findings(self) -> None:
        out = self.signals("--summary")
        self.assertEqual(out["summary"], {})
        self.assertNotIn("findings", out)


if __name__ == "__main__":
    unittest.main()
