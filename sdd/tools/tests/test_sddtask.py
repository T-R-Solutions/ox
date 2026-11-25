#!/usr/bin/env python3
"""Testes do parser único de tasks (sdd/tools/sddtask.py). Stdlib apenas.

Execute da raiz: PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s sdd/tools/tests -v
"""
from __future__ import annotations

import contextlib
import hashlib
import importlib
import io
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sddtask = importlib.import_module("sddtask")
validate = importlib.import_module("validate")
TEMPLATE = Path(__file__).resolve().parents[2] / "templates" / "task.md"

AC1 = "- AC-01: a() retorna 2 | método: `python3 -m unittest` | esperado: exit 0"
AC2 = "- AC-02: doc revisada | método: leitura | esperado: seção X presente"


def sha(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def record(evidence: str, extra: str = "", criteria: str = f"{AC1}\n{AC2}") -> str:
    return f"""# FIX-1 — Corrigir

- Rota: Local — reparo
- Estado: aberta

## 1. Prompt

### 1 - Objetivos

x

### 4 - Critérios de Aceitação

{criteria}

## 3. Especificação

- REQ-01: a
- AC-01 → REQ-01
- AC-02 → REQ-01

## 8. Validação

{evidence}
{extra}"""


def inputs_table(rows: str) -> str:
    return "| Input | Caminho ou saída | Papel | SHA-256 |\n|---|---|---|---|\n" + rows + "\n"


def ac_table(rows: str) -> str:
    return ("| AC | Critério (SHA-256) | Método executado | Inputs | Resultado observado | Estado |\n"
            "|---|---|---|---|---|---|\n" + rows + "\n")


class ParserTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "src").mkdir()
        (self.root / "src/a.py").write_text("a = 2\n")
        self.a_sha = hashlib.sha256(b"a = 2\n").hexdigest()

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def write(self, text: str) -> sddtask.Task:
        path = self.root / "FIX-1.md"
        path.write_text(text)
        return sddtask.parse(path)

    def statuses(self, task: sddtask.Task) -> dict[tuple[str, str], str]:
        return {(r["kind"], r["id"]): r["status"] for r in sddtask.freshness(task, self.root)}

    def base(self) -> str:
        return (inputs_table(f"| I-01 | `src/a.py` | material | `{self.a_sha}` |")
                + "\n" + ac_table(f"| AC-01 | `{sha(AC1)}` | unittest | I-01 | exit 0 | APPROVED |"))

    def test_happy_path(self) -> None:
        task = self.write(record(self.base()))
        self.assertEqual([c.id for c in task.criteria], ["AC-01", "AC-02"])
        st = self.statuses(task)
        self.assertEqual(st, {("criterion", "AC-01"): "fresh", ("input", "I-01"): "fresh"})

    def test_revision_overrides_state_and_inputs(self) -> None:
        rev = ("## Revisão r2 — 2026-11-24\n\n### 8. Validação\n\n"
               + inputs_table(f"| I-02 | `src/a.py` | material | `{'0' * 64}` |") + "\n"
               + ac_table(f"| AC-01 | `{sha(AC1)}` | rerun | I-02 | falhou | UNVERIFIED |"))
        task = self.write(record(self.base(), extra="\n" + rev))
        obs, _ = sddtask.effective_observations(task)
        self.assertEqual(obs["AC-01"]["Estado"], "UNVERIFIED")
        self.assertEqual(obs["AC-01"]["_layer"], "r2")
        st = self.statuses(task)
        self.assertEqual(st[("input", "I-02")], "stale", "input de revisão também é verificado")

    def test_revised_criterion_is_the_current_one(self) -> None:
        ac1b = "- AC-01: a() retorna 2 em 3 execuções | método: `python3 -m unittest` | esperado: exit 0"
        base = (inputs_table(f"| I-01 | `src/a.py` | material | `{'0' * 64}` |") + "\n"
                + ac_table(f"| AC-01 | `{sha(AC1)}` | unittest | I-01 | exit 0 | APPROVED |"))
        rev = ("## Revisão r2 — 2026-11-24\n\n### 1. Prompt\n\n" + ac1b + "\n\n### 8. Validação\n\n"
               + inputs_table(f"| I-02 | `src/a.py` | material | `{self.a_sha}` |") + "\n"
               + ac_table(f"| AC-01 | `{sha(ac1b)}` | rerun | I-02 | exit 0 | APPROVED |"))
        task = self.write(record(base, extra="\n" + rev))
        self.assertEqual(next(c for c in task.criteria if c.id == "AC-01").line, ac1b)
        self.assertEqual([c.id for c in task.criteria], ["AC-01", "AC-02"])
        st = self.statuses(task)
        self.assertEqual(st[("criterion", "AC-01")], "fresh", "o critério revisado é o vigente")
        self.assertEqual(st[("input", "I-02")], "fresh")
        self.assertEqual(st[("input", "I-01")], "unreferenced",
                         "input só da observação substituída é histórico, não problema")
        problems = [r for r in sddtask.freshness(task, self.root) if r["status"] in sddtask.PROBLEM_STATUSES]
        self.assertEqual(problems, [])

    def test_revision_remaps_ac_to_req(self) -> None:
        rev = "## Revisão r2 — 2026-11-24\n\n### 3. Especificação\n\n- REQ-02: b\n- AC-02 → REQ-02\n"
        task = self.write(record(self.base(), extra="\n" + rev))
        self.assertEqual(task.ac_req["AC-02"], ["REQ-02"])
        self.assertEqual(task.ac_req["AC-01"], ["REQ-01"])
        self.assertIn("REQ-02", task.reqs)

    def test_obsolete_subsection_is_ignored(self) -> None:
        old = "### Observações r0 (obsoletas)\n\n" + ac_table("| AC-02 | `abc` | antigo | — | — | APPROVED |")
        task = self.write(record("### Observações r1 (vigentes)\n\n" + self.base() + "\n" + old))
        obs, _ = sddtask.effective_observations(task)
        self.assertNotIn("AC-02", obs)

    def test_inline_inputs_without_ids_are_reported(self) -> None:
        inline = ac_table(f"| AC-01 | `{sha(AC1)}` | unittest | `src/a.py` · material · `{'0' * 64}` | exit 0 | APPROVED |")
        st = self.statuses(self.write(record(inline)))
        self.assertEqual(st[("reference", "AC-01")], "no-inputs",
                         "formato inline não verificável não pode passar despercebido")

    def test_missing_reference(self) -> None:
        ev = (inputs_table(f"| I-01 | `src/a.py` | material | `{self.a_sha}` |") + "\n"
              + ac_table(f"| AC-01 | `{sha(AC1)}` | unittest | I-01, I-09 | exit 0 | APPROVED |"))
        st = self.statuses(self.write(record(ev)))
        self.assertEqual(st[("reference", "AC-01→I-09")], "missing")

    def test_duplicate_input_cannot_hide_stale_hash(self) -> None:
        ev = (inputs_table(f"| I-01 | `src/a.py` | material | `{'0' * 64}` |\n"
                           f"| I-01 | `src/a.py` | material | `{self.a_sha}` |") + "\n"
              + ac_table(f"| AC-01 | `{sha(AC1)}` | unittest | I-01 | exit 0 | APPROVED |"))
        st = self.statuses(self.write(record(ev)))
        self.assertEqual(st[("input", "I-01")], "stale", "vale a primeira definição")
        self.assertEqual(st[("duplicate-input", "I-01")], "duplicate")

    def test_duplicate_observation_in_same_layer(self) -> None:
        ev = self.base() + f"| AC-01 | `{sha(AC1)}` | outro | I-01 | ok | APPROVED |\n"
        st = self.statuses(self.write(record(ev.replace("APPROVED |\n\n|", "APPROVED |\n|"))))
        self.assertEqual(st[("duplicate-observation", "AC-01")], "duplicate")

    def test_missing_input_file_and_stale_criterion(self) -> None:
        ev = (inputs_table(f"| I-01 | `src/nope.py` | material | `{self.a_sha}` |") + "\n"
              + ac_table(f"| AC-01 | `{sha(AC1 + ' x')}` | unittest | I-01 | exit 0 | APPROVED |"))
        st = self.statuses(self.write(record(ev)))
        self.assertEqual(st[("input", "I-01")], "missing")
        self.assertEqual(st[("criterion", "AC-01")], "stale")

    def test_truncated_hash_is_malformed(self) -> None:
        ev = self.base().replace(sha(AC1), sha(AC1)[:16])
        self.assertEqual(self.statuses(self.write(record(ev)))[("criterion", "AC-01")], "malformed")

    def test_fenced_heading_does_not_change_section(self) -> None:
        criteria = f"{AC1}\n\n```markdown\n## 8. Validação\n- AC-09: exemplo | método: x | esperado: y\n```\n\n{AC2}"
        task = self.write(record(self.base(), criteria=criteria))
        self.assertEqual([c.id for c in task.criteria], ["AC-01", "AC-02"],
                         "título e AC dentro de bloco cercado não são estrutura")

    def test_html_comment_is_not_structure(self) -> None:
        criteria = f"{AC1}\n<!-- exemplo:\n- AC-08: comentado | método: x | esperado: y\n## Revisão r9\n-->\n{AC2}"
        task = self.write(record(self.base(), criteria=criteria))
        self.assertEqual([c.id for c in task.criteria], ["AC-01", "AC-02"])
        self.assertEqual(task.revisions, [])

    def test_fenced_tilde_and_longer_fence(self) -> None:
        criteria = f"{AC1}\n~~~~\n```\n- AC-07: dentro | método: x | esperado: y\n```\n~~~~\n{AC2}"
        task = self.write(record(self.base(), criteria=criteria))
        self.assertEqual([c.id for c in task.criteria], ["AC-01", "AC-02"])

    def test_duplicate_criterion_and_unknown_observation(self) -> None:
        ev = self.base() + f"| AC-05 | `{'1' * 64}` | x | I-01 | ok | APPROVED |\n"
        task = self.write(record(ev.replace("APPROVED |\n\n|", "APPROVED |\n|"), criteria=f"{AC1}\n{AC1}"))
        st = self.statuses(task)
        self.assertEqual(st[("duplicate-criterion", "AC-01")], "duplicate")
        self.assertEqual(st[("criterion", "AC-05")], "unknown-criterion")

    def test_real_template_parses(self) -> None:
        task = sddtask.parse(TEMPLATE)
        self.assertEqual(sorted(task.sections), list(range(1, 10)))
        self.assertEqual(sorted(task.divisions), [1, 2, 3, 4, 5])
        self.assertEqual([c.id for c in task.criteria], ["AC-01"])
        self.assertEqual(task.revisions, [])
        tables = sddtask.parse_tables(task.sections[8])
        self.assertEqual([t.header[0] for t in tables][:2], ["Input", "AC"],
                         "o template usa o formato único de inputs (tabela I-n)")



class EvidenceCommandTests(unittest.TestCase):
    """`evidence --write/--check`: hashes vêm dos bytes reais, nunca do registro."""

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "src").mkdir()
        (self.root / "src/a.py").write_text("a = 2\n")
        (self.root / "sdd/tasks").mkdir(parents=True)
        self.path = self.root / "sdd/tasks/FIX-20261124.md"
        self.placeholder = "<64 hex>"

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_cmd(self, *args: str) -> int:
        return sddtask.main(["evidence", "--root", str(self.root), "--task", "FIX-20261124", *args])

    def write_record(self, obsolete: str = "") -> None:
        evidence = (inputs_table(f"| I-01 | `src/a.py` | material | `{self.placeholder}` |\n"
                                 f"| I-02 | `src/missing.py` | oráculo | `{self.placeholder}` |") + "\n"
                    + ac_table(f"| AC-01 | `{self.placeholder}` | unittest | I-01 | exit 0 | APPROVED |"))
        self.path.write_text(record(evidence, extra=obsolete))

    def test_write_fills_hashes_from_real_bytes_and_check_passes(self) -> None:
        self.write_record()
        self.assertEqual(self.run_cmd("--check"), 1, "placeholder não é hash atual")
        self.assertEqual(self.run_cmd("--write"), 0)
        text = self.path.read_text()
        self.assertIn(f"`{sha(AC1)}`", text)
        self.assertIn(f"`{hashlib.sha256(b'a = 2' + bytes([10])).hexdigest()}`", text)
        self.assertIn(f"| I-02 | `src/missing.py` | oráculo | `{self.placeholder}` |", text,
                      "input não referenciado não é tocado")
        self.assertEqual(self.run_cmd("--check"), 0)

    def test_write_never_renews_a_stale_observation(self) -> None:
        self.write_record()
        self.run_cmd("--write")
        recorded = self.path.read_text()
        (self.root / "src/a.py").write_text("a = 3\n")
        self.assertEqual(self.run_cmd("--check"), 1)
        self.assertEqual(self.run_cmd("--write"), 1, "stale continua problema depois de --write")
        self.assertEqual(self.path.read_text(), recorded, "hash válido registrado não é sobrescrito")
        (self.root / "src/a.py").write_text("a = 2\n")
        self.assertEqual(self.run_cmd("--check"), 0)
        self.path.write_text(self.path.read_text().replace(AC1, AC1.replace("exit 0", "exit 1"), 1))
        self.assertEqual(self.run_cmd("--check"), 1, "critério alterado fica stale")
        self.assertEqual(self.run_cmd("--write"), 1)

    def test_missing_referenced_input_stays_a_problem(self) -> None:
        evidence = (inputs_table(f"| I-01 | `src/missing.py` | material | `{self.placeholder}` |") + "\n"
                    + ac_table(f"| AC-01 | `{self.placeholder}` | unittest | I-01 | exit 0 | APPROVED |"))
        self.path.write_text(record(evidence))
        self.assertEqual(self.run_cmd("--write"), 1)
        self.assertIn(f"| I-01 | `src/missing.py` | material | `{self.placeholder}` |", self.path.read_text())

    def test_obsolete_observations_are_not_rewritten(self) -> None:
        old = ("\n### Observações antigas (obsoletas)\n\n"
               + ac_table(f"| AC-02 | `{'1' * 64}` | antigo | I-01 | ok | APPROVED |"))
        self.write_record(obsolete=old)
        self.run_cmd("--write")
        self.assertIn(f"| AC-02 | `{'1' * 64}` | antigo |", self.path.read_text())

    def test_write_keeps_any_recorded_hash_form(self) -> None:
        stale = "a" * 64
        for cell in (f"`{stale}` (r0)", f"`{stale.upper()}`", f"sha256:{stale}", f"`{stale[:16]}`"):
            with self.subTest(cell=cell):
                evidence = (inputs_table(f"| I-01 | `src/a.py` | material | {cell} |") + "\n"
                            + ac_table(f"| AC-01 | {cell} | unittest | I-01 | exit 0 | APPROVED |"))
                self.path.write_text(record(evidence))
                before = self.path.read_text()
                self.assertEqual(self.run_cmd("--write"), 1)
                self.assertEqual(self.path.read_text(), before, "só célula vazia ou marcador é preenchida")

    def test_write_uses_real_column_with_repeated_header_names(self) -> None:
        evidence = (inputs_table(f"| I-01 | `src/a.py` | material | `{self.placeholder}` |") + "\n"
                    "| AC | Nota | Nota | Critério (SHA-256) | Método executado | Inputs | Resultado observado | Estado |\n"
                    "|---|---|---|---|---|---|---|---|\n"
                    f"| AC-01 | n1 | n2 | `{self.placeholder}` | unittest | I-01 | exit 0 | APPROVED |\n")
        self.path.write_text(record(evidence))
        self.run_cmd("--write")
        self.assertIn(f"| AC-01 | n1 | n2 | `{sha(AC1)}` | unittest |", self.path.read_text())

    def test_unknown_or_invalid_task_exits_2(self) -> None:
        self.assertEqual(sddtask.main(["evidence", "--root", str(self.root), "--task", "NOPE-20261124"]), 2)
        self.assertEqual(sddtask.main(["evidence", "--root", str(self.root), "--task", "../../x"]), 2)
        self.assertEqual(sddtask.main(["evidence", "--root", str(self.root), "--task", "FIX-20261124\n"]), 2)

    def test_input_outside_repository_is_a_problem_and_not_hashed(self) -> None:
        evidence = (inputs_table(f"| I-01 | `/etc/hostname` | material | `{self.placeholder}` |\n"
                                 f"| I-02 | `../fora.txt` | oráculo | `{self.placeholder}` |") + "\n"
                    + ac_table(f"| AC-01 | `{self.placeholder}` | unittest | I-01, I-02 | exit 0 | APPROVED |"))
        (self.root.parent / "fora.txt").write_text("x") if self.root.parent.is_dir() else None
        self.path.write_text(record(evidence))
        self.assertEqual(self.run_cmd("--write"), 1)
        text = self.path.read_text()
        self.assertEqual(text.count(f"`{self.placeholder}` |\n"), 2, "input fora da raiz não recebe hash")
        statuses = {(r["kind"], r["id"]): r["status"] for r in sddtask.freshness(sddtask.parse(self.path), self.root)}
        self.assertEqual(statuses[("input", "I-01")], "escaping")
        self.assertEqual(statuses[("input", "I-02")], "escaping")

    def test_derived_input_needs_full_sha256(self) -> None:
        evidence = (inputs_table("| I-01 | saída de `ls` | material | `qualquer` |\n"
                                 f"| I-02 | saída de `cmd` | oráculo | `{'a' * 64}` |") + "\n"
                    + ac_table(f"| AC-01 | `{sha(AC1)}` | x | I-01, I-02 | ok | APPROVED |"))
        self.path.write_text(record(evidence))
        statuses = {(r["kind"], r["id"]): r["status"] for r in sddtask.freshness(sddtask.parse(self.path), self.root)}
        self.assertEqual(statuses[("input", "I-01")], "malformed")
        self.assertEqual(statuses[("input", "I-02")], "unverifiable")
        self.assertEqual(self.run_cmd("--check"), 1)

    def test_escaped_pipe_and_unbalanced_backtick_rows_are_preserved(self) -> None:
        evidence = (inputs_table(f"| I-01 | `src/a.py` | material \\| extra | `{self.placeholder}` |") + "\n"
                    + ac_table(f"| AC-01 | `{self.placeholder}` | unit`test | I-01 | exit 0 | APPROVED |"))
        self.path.write_text(record(evidence))
        self.run_cmd("--write")
        text = self.path.read_text()
        self.assertIn("| material \\| extra |", text, "pipe escapado continua na mesma célula")
        self.assertIn(f"| AC-01 | `{self.placeholder}` | unit`test |", text, "linha com crase desbalanceada não é reescrita")

    def test_require_all_needs_a_fresh_row_per_criterion(self) -> None:
        self.path.write_text(record(""))
        self.assertEqual(self.run_cmd("--check"), 0, "sem --require-all, registro vazio não tem problema")
        self.assertEqual(self.run_cmd("--check", "--require-all"), 1)
        self.write_record()
        self.run_cmd("--write")
        self.assertEqual(self.run_cmd("--check", "--require-all"), 1, "AC-02 sem observação")


class NewCommandTests(unittest.TestCase):
    """`new`: registro inicial a partir do template real; nunca sobrescreve."""

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "sdd/templates").mkdir(parents=True)
        (self.root / "sdd/tasks").mkdir()
        shutil.copyfile(TEMPLATE, self.root / "sdd/templates/task.md")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def new(self, tid: str, route: str, title: str = "Ajuste") -> int:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return sddtask.main(["new", "--root", str(self.root), "--task", tid, "--route", route,
                                 "--title", title])

    def test_local_record_has_only_the_local_sections_and_validates(self) -> None:
        self.assertEqual(self.new("FIX-20261124", "Local", "Corrigir link"), 0)
        path = self.root / "sdd/tasks/FIX-20261124.md"
        text = path.read_text()
        task = sddtask.parse(path)
        self.assertEqual((task.id, task.title), ("FIX-20261124", "Corrigir link"))
        self.assertEqual(task.meta["Data de abertura"], "2026-11-24")
        self.assertEqual(task.meta["Estado"], "aberta")
        self.assertTrue(task.meta["Rota"].startswith("Local — "))
        self.assertNotIn("<!--", text)
        self.assertEqual(sorted(task.sections), list(range(1, 10)))
        for num in sddtask.LOCAL_NA_SECTIONS:
            self.assertEqual(task.section_text(num).strip(), sddtask.LOCAL_NA, f"seção {num}")
        self.assertEqual([t.header[0] for t in task.tables(4)], ["SKILL.md"])
        self.assertIn(validate.PROMPT_SKILL, task.section_text(4))
        self.assertNotIn("ADR:", task.section_text(4))
        self.assertEqual(validate.task_errors(self.root, path, None), [])

    def test_full_route_keeps_every_template_section(self) -> None:
        self.assertEqual(self.new("PLAN-20261124-2", "Completa"), 0)
        task = sddtask.parse(self.root / "sdd/tasks/PLAN-20261124-2.md")
        template = sddtask.parse(TEMPLATE)
        self.assertTrue(task.meta["Rota"].startswith("Completa — "))
        for num in range(1, 10):
            self.assertEqual(task.section_text(num), template.section_text(num), f"seção {num}")

    def test_existing_record_is_never_overwritten(self) -> None:
        with self.subTest("arquivo existente"):
            path = self.root / "sdd/tasks/FIX-20261124.md"
            path.write_text("trabalho existente\n")
            self.assertEqual(self.new("FIX-20261124", "Local"), 2)
            self.assertEqual(path.read_text(), "trabalho existente\n")
        with self.subTest("symlink pendente"):
            link = self.root / "sdd/tasks/LINK-20261124.md"
            link.symlink_to(self.root / "alvo-inexistente.md")
            self.assertEqual(self.new("LINK-20261124", "Local"), 2)
            self.assertFalse((self.root / "alvo-inexistente.md").exists(), "symlink não é seguido")

    def test_invalid_id_date_or_title_writes_nothing(self) -> None:
        cases = [("../x-20261124", "t"), ("FIX-20261340", "t"), ("FIX-20261124-20261340", "t"),
                 ("FIX-20261124-0", "t"), ("FIX-20261124-1", "t"),
                 ("FIX-20261124", " "), ("FIX-20261124", "a\udcffb")]
        cases += [("FIX-20261124", f"a{sep}b") for sep in ("\n", "\r", "\v", "\f", "\x1c", "\x85", "\u2028")]
        for tid, title in cases:
            with self.subTest(tid=tid, title=title):
                self.assertEqual(self.new(tid, "Local", title), 2)
                self.assertEqual(list((self.root / "sdd/tasks").iterdir()), [], "nada é escrito, nem vazio")

    def test_date_comes_from_the_group_before_the_repeat_suffix(self) -> None:
        self.assertEqual(self.new("FIX-20261124-20261125", "Local"), 0)
        task = sddtask.parse(self.root / "sdd/tasks/FIX-20261124-20261125.md")
        self.assertEqual(task.meta["Data de abertura"], "2026-11-25")
        self.assertEqual(self.new("FIX-20261124-2", "Local"), 0)
        task = sddtask.parse(self.root / "sdd/tasks/FIX-20261124-2.md")
        self.assertEqual(task.meta["Data de abertura"], "2026-11-24")

    def test_missing_or_redirected_tasks_dir_and_template_without_skills(self) -> None:
        tasks = self.root / "sdd/tasks"
        with self.subTest("sdd/tasks ausente"):
            tasks.rmdir()
            self.assertEqual(self.new("FIX-20261124", "Local"), 2)
            tasks.mkdir()
        with self.subTest("sdd/tasks symlink para fora da raiz"):
            outside = Path(self.tmp.name + "-fora")
            outside.mkdir()
            self.addCleanup(shutil.rmtree, outside)
            tasks.rmdir()
            tasks.symlink_to(outside, target_is_directory=True)
            self.assertEqual(self.new("FIX-20261124", "Local"), 2)
            self.assertEqual(list(outside.iterdir()), [], "nada escrito fora da raiz")
            tasks.unlink()
            tasks.mkdir()
        with self.subTest("template sem Skills lidas"):
            template = self.root / "sdd/templates/task.md"
            template.write_text(template.read_text().replace("Skills lidas:", "Leituras:"))
            self.assertEqual(self.new("FIX-20261124", "Local"), 2)
            self.assertEqual(list(tasks.iterdir()), [])

    def test_evidence_reports_next_free_input_including_obsolete(self) -> None:
        path = self.root / "sdd/tasks/FIX-20261124.md"
        obsolete = "\n### Antigas (obsoletas)\n\n" + inputs_table("| I-07 | `x` | material | — |")
        fenced = "\n```\n| I-90 | `x` | material | — |\n```\n<!--\n| I-91 | `x` | material | — |\n-->\n"
        path.write_text(record(inputs_table("| I-01 | `x` | material | — |\n| `I-03` | `x` | material | — |"),
                               extra=obsolete + fenced))
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            sddtask.main(["evidence", "--root", str(self.root), "--task", "FIX-20261124"])
        self.assertIn("próximo input livre: I-08", out.getvalue())
        path.write_text(record(""))
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            sddtask.main(["evidence", "--root", str(self.root), "--task", "FIX-20261124"])
        self.assertIn("próximo input livre: I-01", out.getvalue())


if __name__ == "__main__":
    unittest.main()
