#!/usr/bin/env python3
"""Testes dos scripts da skill em repositórios Git temporários (stdlib apenas).

Execute: python3 -I .claude/skills/codex-task-audit/scripts/test_scripts.py -v
"""
from __future__ import annotations

import hashlib
import json
import os
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


PARSER = HERE.parents[3] / "sdd" / "tools" / "sddtask.py"


def task_text(ac1_sha: str = "", in1_sha: str = "") -> str:
    return f"""# FIX-20261123 — Corrigir a()

- Rota: Local — reparo reversível
- Revisão atual: r1
- Estado: aberta

## 1. Prompt

### 1 - Objetivos

Corrigir `a()`.

### 2 - Requisitos

- `a()` retorna 2.

### 3 - Restrições

- NÃO alterar `src/b.py`.

### 4 - Critérios de Aceitação

- AC-01: a() retorna 2 | método: `python3 -m unittest tests.test_a` | esperado: exit 0
- AC-02: documentação revisada | PENDENTE: Q-1

### 5 - Entrega

- Regra de conclusão: AC-01 e AC-02 APPROVED.

## 2. Esclarecimentos

## 3. Especificação

- REQ-01: a() retorna 2.
- REQ-02: requisito sem critério.
- AC-01 → REQ-01

## 5. Itens de trabalho

| Item | D | Arquivos (dono) | Depende de | Teste | Pronto quando |
|---|---|---|---|---|---|
| T-01 | — | `src/a.py` | — | AC-01 | exit 0 |

## 7. Execução

| Item | Arquivos alterados | Teste executado | Exit | Observação |
|---|---|---|---|---|
| T-01 | `src/a.py`, `src/ghost.py`, `sdd/tasks/FIX-20261123.md` | `tests/test_a.py` | 0 | — |

## 8. Validação

### Observações r1 (vigentes)

| Input | Caminho ou saída | Papel | SHA-256 |
|---|---|---|---|
| I-01 | `src/a.py` | material | `{in1_sha}` |
| I-02 | stdout de `ls` | material | `{"0" * 64}` |

| AC | Critério (SHA-256) | Método executado | Inputs | Resultado observado | Estado |
|---|---|---|---|---|---|
| AC-01 | `{ac1_sha}` | unittest | I-01, I-02 | exit 0 | APPROVED |

### Observações r0 (obsoletas)

| AC | Critério (SHA-256) | Método executado | Inputs | Resultado observado | Estado |
|---|---|---|---|---|---|
| AC-01 | `abc` | antigo | — | — | APPROVED |
"""


def ac_line_sha(text: str, ac: str) -> str:
    line = next(l for l in text.splitlines() if l.startswith(f"- {ac}:"))
    return hashlib.sha256(line.encode()).hexdigest()


class InventoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = Repo()
        self.repo.write("src/a.py", "def a():\n    return 1\n")
        self.repo.write("src/b.py", "b = 1\n")
        self.repo.write("tests/test_a.py", "x = 1\n")
        self.repo.commit()
        self.repo.write("src/a.py", "def a():\n    return 2\n")
        a_sha = hashlib.sha256((self.repo.root / "src/a.py").read_bytes()).hexdigest()
        draft = task_text("", a_sha)
        self.repo.write("sdd/tasks/FIX-20261123.md", task_text(ac_line_sha(draft, "AC-01"), a_sha))

    def tearDown(self) -> None:
        self.repo.close()

    def inventory(self, *extra: str) -> dict:
        res = run(INVENTORY, self.repo.root, *extra)
        self.assertEqual(res.returncode, 0, res.stderr)
        return json.loads(res.stdout)

    def test_happy_path_structure_and_fresh_hashes(self) -> None:
        inv = self.inventory()
        self.assertEqual(inv["task"]["id"], "FIX-20261123")
        self.assertEqual(inv["divisions_missing"], [])
        self.assertEqual(inv["criteria_incomplete"], [])
        self.assertEqual(inv["criteria_pending"], ["AC-02"])
        status = {(f["kind"], f["id"]): f["status"] for f in inv["freshness"]}
        self.assertEqual(status, {("criterion", "AC-01"): "fresh", ("input", "I-01"): "fresh",
                                  ("input", "I-02"): "unverifiable"},
                         "linha obsoleta (r0) não entra na verificação")
        self.assertEqual(inv["freshness_problems"], [])

    def test_orphans_between_sections(self) -> None:
        inv = self.inventory()
        self.assertEqual(inv["ac_without_req"], ["AC-02"])
        self.assertEqual(inv["req_without_ac"], ["REQ-02"])

    def test_changed_input_and_criterion_become_stale(self) -> None:
        self.repo.write("src/a.py", "def a():\n    return 3\n")
        path = self.repo.root / "sdd/tasks/FIX-20261123.md"
        path.write_text(path.read_text().replace("| esperado: exit 0", "| esperado: exit 0 em 2 execuções"))
        probs = {(f["kind"], f["id"]): f["status"] for f in self.inventory()["freshness_problems"]}
        self.assertEqual(probs, {("criterion", "AC-01"): "stale", ("input", "I-01"): "stale"})

    def test_truncated_hash_is_malformed(self) -> None:
        path = self.repo.root / "sdd/tasks/FIX-20261123.md"
        text = path.read_text()
        full = ac_line_sha(text, "AC-01")
        path.write_text(text.replace(full, full[:16]))
        probs = {f["id"]: f["status"] for f in self.inventory()["freshness_problems"]}
        self.assertEqual(probs, {"AC-01": "malformed"})

    def test_git_diff_versus_section_7(self) -> None:
        self.repo.write("src/c.py", "c = 1\n")
        self.repo.write(".claude/skills/x/SKILL.md", "x\n")
        inv = self.inventory()
        self.assertEqual([c["path"] for c in inv["changed_uncited"]], [".claude/skills/x/SKILL.md", "src/c.py"],
                         "o próprio registro da task não conta como órfão")
        self.assertIn("src/ghost.py", inv["cited_without_change"])
        self.assertIn("tests/test_a.py", inv["cited_without_change"])
        self.assertNotIn("src/a.py", inv["cited_without_change"])
        self.assertNotIn("sdd/tasks/FIX-20261123.md", inv["cited_without_change"],
                         "o próprio registro não é alegação de mudança")

    def test_review_revisions_and_task_selection(self) -> None:
        self.repo.write("sdd/tasks/FIX-20261123.review.md", "# p\n\n## Revisão r1 — x\n\n## Revisão r2 — y\n")
        inv = self.inventory("--task", "FIX-20261123")
        self.assertEqual(inv["review"]["revisions"], ["r1", "r2"])
        self.assertEqual([c["path"] for c in inv["changed_uncited"]], [], "o parecer não conta como órfão")

    def test_failures_exit_2(self) -> None:
        res = run(INVENTORY, self.repo.root, "--task", "NOPE-1")
        self.assertEqual(res.returncode, 2)
        self.assertIn("ausente", res.stderr)
        (self.repo.root / "sdd/tasks/FIX-20261123.md").write_text("sem cabeçalho\n")
        res = run(INVENTORY, self.repo.root, "--task", "FIX-20261123")
        self.assertEqual(res.returncode, 2)
        self.assertIn("primeira linha", res.stderr)
        with tempfile.TemporaryDirectory() as plain:
            res = run(INVENTORY, Path(plain))
            self.assertEqual(res.returncode, 2)
            self.assertIn("git", res.stderr)

    def test_json_output_with_revision(self) -> None:
        path = self.repo.root / "sdd/tasks/FIX-20261123.md"
        path.write_text(path.read_text() + "\n## Revisão r2 — 2026-11-24\n\nMotivo: x\n\n### 7. Execução\n\nnada\n")
        inv = self.inventory()  # formato padrão: JSON
        self.assertEqual(inv["task"]["revisions"], ["r2"])

    def test_audited_parser_is_not_executed(self) -> None:
        marker = self.repo.root / "PWNED"
        self.repo.write("sdd/tools/sddtask.py", f"open({str(marker)!r}, 'w').write('x')\n")
        inv = self.inventory()
        self.assertFalse(marker.exists(), "o parser do --root auditado não pode ser executado")
        self.assertEqual(Path(inv["parser"]["path"]), PARSER)

    def test_git_index_is_not_rewritten(self) -> None:
        index = self.repo.root / ".git/index"
        tracked = self.repo.root / "src/b.py"
        st = tracked.stat()
        os.utime(tracked, ns=(st.st_atime_ns, st.st_mtime_ns + 5_000_000_000))
        before = (index.read_bytes(), index.stat().st_mtime_ns)
        self.inventory()
        res = run(SIGNALS, self.repo.root)
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertEqual((index.read_bytes(), index.stat().st_mtime_ns), before,
                         "inventário e diff_signals não podem regravar .git/index")

    def test_markdown_output(self) -> None:
        res = run(INVENTORY, self.repo.root, "--format", "md")
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertIn("# Inventário — FIX-20261123 — Corrigir a()", res.stdout)
        self.assertIn("## ACs PENDENTE: 1", res.stdout)


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
