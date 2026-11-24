#!/usr/bin/env python3
"""Testes do validador do SDD (sdd/tools/validate.py). Stdlib apenas.

Cada rejeição exigida pelos gates do workflow tem ao menos um teste. A tabela de
termos proibidos é lida do sdd/workflow.md real, copiado para a raiz temporária.
"""
from __future__ import annotations

import hashlib
import importlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
TOOLS = Path(__file__).resolve().parents[1]
REPO = TOOLS.parents[1]
sys.path.insert(0, str(TOOLS))
V = importlib.import_module("validate")

AC1 = "- AC-01: f() retorna 2 | método: `python3 -m unittest t` | esperado: exit 0"
AC2 = "- AC-02: g() rejeita vazio | método: `python3 -m unittest t2` | esperado: exit 0"


SKILLS = ("| `.codex/skills/prompt/SKILL.md` | etapa 1 | prompt |\n"
          "| `.codex/skills/software-testing/SKILL.md` | etapa 5 | casos |")


def sha(data: str | bytes) -> str:
    return hashlib.sha256(data.encode() if isinstance(data, str) else data).hexdigest()


def task(src_sha: str, *, oracle_sha: str = "", route="Completa — risco", state="aberta", ac1=AC1, ac2=AC2, requisitos="- f() retorna 2.",
         reqs="- REQ-01: f\n- REQ-02: g\n- AC-01 → REQ-01\n- AC-02 → REQ-02", decisions=None, items=None,
         skills=SKILLS, obs=None, section9="- Estado final: aberta", questions="", opened="2026-11-24") -> str:
    decisions = decisions or "| D-01 | REQ-01, REQ-02 | x | y |"
    items = items or ("| T-01 | D-01 | `src/f.py` | — | AC-01 | exit 0 | `software-testing` |\n"
                      "| T-02 | D-01 | `src/g.py` | T-01 | AC-02 | exit 0 | nenhuma: só renomeia |")
    obs = obs if obs is not None else f"| AC-01 | `{sha(ac1)}` | unittest | I-01, I-02 | exit 0 | APPROVED |"
    return f"""# FIX-20261124 — Corrigir f

- Data de abertura: {opened}
- Rota: {route}
- Revisão atual: r1
- Estado: {state}

## 1. Prompt

### 1 - Objetivos

Corrigir f.

### 2 - Requisitos

{requisitos}

### 3 - Restrições

- NÃO alterar `src/h.py`.

### 4 - Critérios de Aceitação

{ac1}
{ac2}

### 5 - Entrega

- Regra de conclusão: AC-01 e AC-02 APPROVED.

## 2. Esclarecimentos

{questions}

## 3. Especificação

{reqs}

## 4. Plano

| Decisão | REQ | Escolha | Alternativa descartada e motivo |
|---|---|---|---|
{decisions}

| SKILL.md | Motivo | Contribuição |
|---|---|---|
{skills}

## 5. Itens de trabalho

| Item | D | Arquivos (dono) | Depende de | Teste | Pronto quando | Skill |
|---|---|---|---|---|---|---|
{items}

## 6. Coerência

`validate.py --task FIX-20261124 --matrix`: exit 0. Conflitos: nenhum.

## 7. Execução

nada

## 8. Validação

| Input | Caminho ou saída | Papel | SHA-256 |
|---|---|---|---|
| I-01 | `src/f.py` | material | `{src_sha}` |
| I-02 | `src/t.py` | oráculo | `{oracle_sha}` |

| AC | Critério (SHA-256) | Método executado | Inputs | Resultado observado | Estado |
|---|---|---|---|---|---|
{obs}

## 9. Fechamento

{section9}
"""


class ValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        sdd = self.root / "sdd"
        for name in V.REQUIRED_FILES:
            (sdd / name).parent.mkdir(parents=True, exist_ok=True)
            (sdd / name).write_text("# x\n")
        (sdd / "workflow.md").write_bytes((REPO / "sdd/workflow.md").read_bytes())
        for name in V.REQUIRED_DIRS:
            (sdd / name).mkdir(exist_ok=True)
        (self.root / "src").mkdir()
        for name in ("prompt", "software-testing", "rust"):
            (self.root / ".codex/skills" / name).mkdir(parents=True)
            (self.root / ".codex/skills" / name / "SKILL.md").write_text(f"# {name}\n")
        (self.root / "src/f.py").write_text("f = 2\n")
        (self.root / "src/t.py").write_text("assert f == 2\n")
        self.src_sha = sha((self.root / "src/f.py").read_bytes())
        self.t_sha = sha((self.root / "src/t.py").read_bytes())
        self.pattern = V.term_pattern(V.forbidden_terms(self.root))

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def errors(self, text: str) -> list[str]:
        path = self.root / "sdd/tasks/FIX-20261124.md"
        path.write_text(text)
        return V.task_errors(self.root, path, self.pattern)

    def assertError(self, text: str, fragment: str) -> None:
        errs = self.errors(text)
        self.assertTrue(any(fragment in e for e in errs), f"esperado '{fragment}' em {errs}")

    def test_forbidden_terms_come_from_workflow(self) -> None:
        terms = V.forbidden_terms(self.root)
        for term in ("rápido", "sem erros", "bonito", "completo", "simples"):
            self.assertIn(term, terms)

    def test_valid_task_passes(self) -> None:
        self.assertEqual(self.errors(task(self.src_sha, oracle_sha=self.t_sha)), [])

    def test_real_task_record_passes(self) -> None:
        tasks = sorted((REPO / "sdd/tasks").glob("*.md"))
        pattern = V.term_pattern(V.forbidden_terms(REPO))
        for path in tasks:
            if path.name.endswith(".review.md") or path.name == "README.md":
                continue
            with self.subTest(task=path.name):
                self.assertEqual(V.task_errors(REPO, path, pattern), [])

    def test_rejects_subjective_term_without_metric(self) -> None:
        self.assertError(task(self.src_sha, oracle_sha=self.t_sha, requisitos="- A tela deve ser rápida e bonita."), "termo subjetivo")
        ac = "- AC-02: g() roda sem erros | método: leitura | esperado: ok"
        self.assertError(task(self.src_sha, oracle_sha=self.t_sha, ac2=ac), "termo subjetivo")

    def test_term_with_metric_or_pending_is_accepted(self) -> None:
        ok = "- A busca deve ser rápida: p95 < 200 ms em 1000 itens."
        self.assertEqual(self.errors(task(self.src_sha, oracle_sha=self.t_sha, requisitos=ok)), [])
        pend = "- AC-02: busca rápida | PENDENTE: Q-1"
        text = task(self.src_sha, oracle_sha=self.t_sha, ac2=pend, questions="| Q-1 | limite? | — | AC-02 |")
        self.assertFalse(any("termo subjetivo" in e for e in self.errors(text)))

    def test_number_in_another_part_does_not_excuse_term(self) -> None:
        ac = "- AC-02: interface bonita | método: leitura | esperado: exit 0"
        self.assertError(task(self.src_sha, oracle_sha=self.t_sha, ac2=ac), "termo subjetivo sem métrica 'bonita'")
        ok = "- AC-02: abre em menos de 2 s, rápido | método: `bench` | esperado: p95 < 2 s"
        self.assertFalse(any("termo subjetivo" in e for e in self.errors(task(self.src_sha, oracle_sha=self.t_sha, ac2=ok))))

    def test_matrix_is_derived_from_sections_3_to_5(self) -> None:
        path = self.root / "sdd/tasks/FIX-20261124.md"
        path.write_text(task(self.src_sha, oracle_sha=self.t_sha))
        self.assertEqual(V.coherence_matrix(V.T.parse(path)),
                         [("REQ-01", ["D-01"], ["T-01"], ["AC-01"]), ("REQ-02", ["D-01"], ["T-02"], ["AC-02"])])

    def test_rejects_req_whose_criteria_no_item_tests(self) -> None:
        items = "| T-01 | D-01 | `src/f.py` | — | AC-01 | exit 0 |"
        errs = self.errors(task(self.src_sha, oracle_sha=self.t_sha, items=items))
        self.assertTrue(any("etapa 6: REQ-02 sem item que teste seus AC" in e for e in errs), errs)
        self.assertTrue(any("AC-02 não é coberto por nenhum item" in e for e in errs), errs)
        path = self.root / "sdd/tasks/FIX-20261124.md"
        path.write_text(task(self.src_sha, oracle_sha=self.t_sha, items=items))
        self.assertIn(("REQ-02", [], [], ["AC-02"]), V.coherence_matrix(V.T.parse(path)))

    DEC_HEADER = "| Decisão | REQ | Escolha | Alternativa descartada e motivo |\n|---|---|---|---|\n"
    ITEM_HEADER = ("| Item | D | Arquivos (dono) | Depende de | Teste | Pronto quando | Skill |\n"
                   "|---|---|---|---|---|---|---|\n")

    def revised(self, *stages: str, **kw: str) -> str:
        """Task válida com uma revisão r2 contendo as subseções dadas."""
        return task(self.src_sha, oracle_sha=self.t_sha, **kw) + "\n## Revisão r2 — 2026-11-24 — Ajuste\n\n" + "\n".join(stages)

    def test_revision_tables_override_original_by_id(self) -> None:
        # Revisão externa de SDD-ENXUTO, achado 3: uma r2 que liga D-01 ao REQ errado passava com exit 0.
        wrong = f"### 4. Plano\n\n{self.DEC_HEADER}| D-01 | REQ-01 | x | y |\n"
        self.assertError(self.revised(wrong), "T-02 usa D-01, que não atende REQ-02 (de AC-02)")
        self.assertError(task(self.src_sha, oracle_sha=self.t_sha, decisions="| D-01 | REQ-01 | x | y |"),
                         "T-02 usa D-01, que não atende REQ-02 (de AC-02)")
        bad_item = f"### 5. Itens de trabalho\n\n{self.ITEM_HEADER}| T-02 | D-01 | `src/g.py` | T-01 | AC-09 | exit 0 | `rust` |\n"
        errs = self.errors(self.revised(bad_item))
        self.assertTrue(any("T-02 testa AC-09, que não existe" in e for e in errs), errs)
        self.assertTrue(any("AC-02 não é coberto por nenhum item" in e for e in errs), errs)
        self.assertTrue(any("T-02 usa 'rust', ausente de Skills lidas" in e for e in errs), errs)

    def test_revision_tables_accept_valid_change_and_feed_matrix(self) -> None:
        dec = f"### 4. Plano\n\n{self.DEC_HEADER}| D-02 | REQ-02 | z | w |\n"
        item = f"### 5. Itens de trabalho\n\n{self.ITEM_HEADER}| T-02 | D-02 | `src/g.py` | T-01 | AC-02 | exit 0 | `software-testing` |\n"
        text = self.revised(dec, item)
        self.assertEqual(self.errors(text), [])
        path = self.root / "sdd/tasks/FIX-20261124.md"
        path.write_text(text)
        parsed = V.T.parse(path)
        self.assertEqual(V.coherence_matrix(parsed),
                         [("REQ-01", ["D-01"], ["T-01"], ["AC-01"]), ("REQ-02", ["D-02"], ["T-02"], ["AC-02"])])
        items = parsed.table(5, "Item")
        self.assertEqual([V.T.strip_code(r["Item"]) for r in items.rows], ["T-01", "T-02"], "substitui na mesma posição")
        skill_rev = (f"### 4. Plano\n\n| SKILL.md | Motivo | Contribuição |\n|---|---|---|\n"
                     f"| `.codex/skills/rust/SKILL.md` | r2 | código |\n\n"
                     f"### 5. Itens de trabalho\n\n{self.ITEM_HEADER}| T-03 | D-01 | `src/h.py` | — | AC-01 | exit 0 | `rust` |\n")
        self.assertEqual(self.errors(self.revised(skill_rev)), [], "skill lida na r2 vale para item da r2")

    def test_duplicate_id_in_same_layer_keeps_both_rows(self) -> None:
        # A linha errada vem primeiro: a checagem não pode depender de a última linha vencer.
        # Com ID repetido, as checagens por ID veem uma só linha; a repetição já reprova.
        items = ("| T-01 | D-01 | `src/f.py` | — | AC-01 | exit 0 | `software-testing` |\n"
                 "| T-02 | D-01 | `src/g.py` | T-01 | AC-09 | exit 0 | `software-testing` |\n"
                 "| T-02 | D-01 | `src/g.py` | T-01 | AC-02 | exit 0 | `software-testing` |")
        errs = self.errors(task(self.src_sha, oracle_sha=self.t_sha, items=items))
        self.assertTrue(any("item com ID T-02 repetido na mesma camada" in e for e in errs), errs)
        decisions = "| D-01 | REQ-01 | x | y |\n| D-01 | REQ-01, REQ-02 | x | y |"
        self.assertError(task(self.src_sha, oracle_sha=self.t_sha, decisions=decisions),
                         "decisão com ID D-01 repetido na mesma camada")
        twice = (f"### 5. Itens de trabalho\n\n{self.ITEM_HEADER}"
                 "| T-02 | D-01 | `src/g.py` | T-01 | AC-09 | exit 0 | `rust` |\n"
                 "| T-02 | D-01 | `src/g.py` | T-01 | AC-02 | exit 0 | `software-testing` |\n")
        self.assertError(self.revised(twice), "item com ID T-02 repetido na mesma camada")

    def test_rejects_unrecognized_or_split_stage_tables(self) -> None:
        # Tabela de revisão com outro cabeçalho não pode ser ignorada em silêncio (achado 3).
        other = "### 4. Plano\n\n| D | REQ | Escolha | Alternativa |\n|---|---|---|---|\n| D-01 | REQ-01 | x | y |\n"
        self.assertError(self.revised(other), "etapa 4: tabela 'D' não reconhecida")
        split = (f"### 5. Itens de trabalho\n\n{self.ITEM_HEADER}| T-01 | D-01 | `src/f.py` | — | AC-01 | exit 0 | `rust` |\n\n"
                 f"{self.ITEM_HEADER}| T-02 | D-01 | `src/g.py` | T-01 | AC-09 | exit 0 | `rust` |\n")
        self.assertError(self.revised(split), "T-02 testa AC-09, que não existe")
        blank = f"### 5. Itens de trabalho\n\n{self.ITEM_HEADER}| — | D-01 | `src/g.py` | — | AC-02 | exit 0 | `rust` |\n"
        self.assertError(self.revised(blank), "etapa 5: linha de item sem ID")

    def test_rejects_input_kept_in_local_dir(self) -> None:
        log = self.root / ".local/tasks/FIX-20261124/ac01.log"
        log.parent.mkdir(parents=True)
        log.write_text("exit 0\n")
        log_sha = sha("exit 0\n")
        for state, section9 in (("aberta", "- Estado final: aberta"), ("concluída", self.FULL9)):
            obs = (f"| AC-01 | `{sha(AC1)}` | unittest | I-01, I-02, I-03 | exit 0 | APPROVED |\n"
                   f"| AC-02 | `{sha(AC2)}` | unittest | I-01, I-02 | exit 0 | APPROVED |")
            text = task(self.src_sha, oracle_sha=self.t_sha, state=state, obs=obs, section9=section9).replace(
                "| I-02 | `src/t.py`", f"| I-03 | `.local/tasks/FIX-20261124/ac01.log` | material | `{log_sha}` |\n| I-02 | `src/t.py`")
            with self.subTest(state=state):
                errs = self.errors(text)
                self.assertTrue(any("AC-01 APPROVED com input I-03 em .local/, fora do Git" in e for e in errs), errs)
                self.assertEqual(len(errs), 1, errs)
            for cell in ("`sdd/../.local/tasks/FIX-20261124/ac01.log`", "[log](../../.local/tasks/FIX-20261124/ac01.log)",
                         "`.local/tasks/FIX-20261124/ac01.log` (log)", "saída em .local/tasks/FIX-20261124/ac01.log"):
                with self.subTest(state=state, cell=cell):
                    errs = self.errors(text.replace("`.local/tasks/FIX-20261124/ac01.log`", cell))
                    self.assertTrue(any("input I-03 em .local/" in e for e in errs), errs)
            versioned = text.replace(".local/tasks/FIX-20261124/ac01.log", "sdd/tasks/FIX-20261124/ac01.log")
            linked = self.root / "sdd/tasks/LINK-20261124"
            if not linked.exists():
                linked.symlink_to(log.parent, target_is_directory=True)
            with self.subTest(state=state, cell="diretório symlink para .local/"):
                errs = self.errors(text.replace(".local/tasks/FIX-20261124/ac01.log", "sdd/tasks/LINK-20261124/ac01.log"))
                self.assertTrue(any("input I-03 em .local/" in e for e in errs), errs)
            (self.root / "sdd/tasks/FIX-20261124").mkdir(exist_ok=True)
            (self.root / "sdd/tasks/FIX-20261124/ac01.log").write_text("exit 0\n")
            self.assertEqual(self.errors(versioned), [])

    def test_rejects_item_citing_unknown_decision(self) -> None:
        items = "| T-01 | D-99 | `src/f.py` | — | AC-01 | exit 0 |\n| T-02 | D-01 | `src/g.py` | T-01 | AC-02 | exit 0 |"
        self.assertError(task(self.src_sha, oracle_sha=self.t_sha, items=items), "T-01 cita D-99, que não está nas decisões")

    def test_rejects_empty_method_result_and_missing_oracle(self) -> None:
        obs = f"| AC-01 | `{sha(AC1)}` |  | I-01 |  | APPROVED |"
        errs = self.errors(task(self.src_sha, oracle_sha=self.t_sha, obs=obs))
        self.assertTrue(any("'Método executado' vazio" in e for e in errs), errs)
        self.assertTrue(any("'Resultado observado' vazio" in e for e in errs), errs)
        self.assertTrue(any("sem input 'oráculo'" in e for e in errs), errs)
        justified = f"| AC-01 | `{sha(AC1)}` | unittest | I-01; sem oráculo separado: esperado no critério | exit 0 | APPROVED |"
        self.assertEqual(self.errors(task(self.src_sha, oracle_sha=self.t_sha, obs=justified)), [])

    def concluded(self, section9: str) -> list[str]:
        obs = (f"| AC-01 | `{sha(AC1)}` | unittest | I-01, I-02 | exit 0 | APPROVED |\n"
               f"| AC-02 | `{sha(AC2)}` | unittest | I-01, I-02 | exit 0 | APPROVED |")
        return self.errors(task(self.src_sha, oracle_sha=self.t_sha, state="concluída", obs=obs, section9=section9))

    FULL9 = ("- Documentação: README revisado → sem impacto: nenhum comando mudou\n- `sdd/project.md`: sem mudança\n"
             "- Inputs da seção 8 alterados no fechamento: nenhum\n- Checks de governança: check-ox exit 0\n"
             "- Pendências: nenhuma\n- Estado final: concluída")

    def test_concluded_task_passes_with_full_closure(self) -> None:
        self.assertEqual(self.concluded(self.FULL9), [])

    def test_rejects_concluded_with_empty_closure(self) -> None:
        errs = self.concluded("")
        self.assertTrue(any("campo 'Documentação' ausente ou vazio" in e for e in errs), errs)
        errs = self.concluded(self.FULL9.replace("- Estado final: concluída", "- Estado final: incompleta"))
        self.assertTrue(any("'Estado final' difere" in e for e in errs), errs)

    def test_latest_revision_closure_decides_final_state(self) -> None:
        earlier = self.FULL9.replace("- Estado final: concluída", "- Estado final: incompleta")
        closed_later = f"{earlier}\n\n## Revisão r2 — 2026-11-24 — Fechamento\n\n### 9. Fechamento\n\n{self.FULL9}"
        errs = self.concluded(closed_later)
        self.assertFalse(any("'Estado final' difere" in e for e in errs), errs)
        reopened = f"{self.FULL9}\n\n## Revisão r2 — 2026-11-24 — Retomada\n\n### 9. Fechamento\n\n{earlier}"
        errs = self.concluded(reopened)
        self.assertTrue(any("'Estado final' difere" in e for e in errs), errs)

    def test_bare_number_is_not_a_metric(self) -> None:
        self.assertError(task(self.src_sha, oracle_sha=self.t_sha, requisitos="- Na versão 2 a interface deve ser bonita."),
                         "termo subjetivo sem métrica 'bonita'")
        for ok in ("- Abrir rápido: p95 < 200 ms.", "- Rápido: abre em 2 s em 1000 itens.", "- Leve: ≤ 30 MB de memória."):
            with self.subTest(text=ok):
                errs = self.errors(task(self.src_sha, oracle_sha=self.t_sha, requisitos=ok))
                self.assertFalse(any("termo subjetivo" in e for e in errs), errs)

    def test_rejects_decision_that_does_not_serve_the_tested_req(self) -> None:
        decisions = "| D-01 | REQ-01 | x | y |\n| D-02 | REQ-02 | x | y |"
        items = ("| T-01 | D-01 | `src/f.py` | — | AC-01 | exit 0 |\n"
                 "| T-02 | D-01 | `src/g.py` | T-01 | AC-02 | exit 0 |\n"
                 "| T-03 | D-02 | `src/h.py` | — | AC-02 | exit 0 |")
        self.assertError(task(self.src_sha, oracle_sha=self.t_sha, decisions=decisions, items=items),
                         "T-02 usa D-01, que não atende REQ-02 (de AC-02)")

    def test_rejects_empty_no_oracle_reason(self) -> None:
        for cell in ("I-01; sem oráculo separado:", "I-01; sem oráculo separado:  ", "I-01; sem oráculo separado: ;"):
            with self.subTest(cell=cell):
                obs = f"| AC-01 | `{sha(AC1)}` | unittest | {cell} | exit 0 | APPROVED |"
                self.assertError(task(self.src_sha, oracle_sha=self.t_sha, obs=obs), "sem input 'oráculo'")

    def test_rejects_criterion_without_method(self) -> None:
        self.assertError(task(self.src_sha, oracle_sha=self.t_sha, ac2="- AC-02: g() rejeita vazio"), "sem 'método:'")

    def test_rejects_pending_without_registered_question(self) -> None:
        self.assertError(task(self.src_sha, oracle_sha=self.t_sha, ac2="- AC-02: limite | PENDENTE: Q-7"), "Q-7")

    def test_rejects_orphan_req_and_ac(self) -> None:
        self.assertError(task(self.src_sha, oracle_sha=self.t_sha, reqs="- REQ-01: f\n- REQ-02: g\n- REQ-03: h\n- AC-01 → REQ-01\n- AC-02 → REQ-02"),
                         "REQ-03 sem AC")
        self.assertError(task(self.src_sha, oracle_sha=self.t_sha, reqs="- REQ-01: f\n- REQ-02: g\n- AC-01 → REQ-01\n- AC-02 → REQ-02\n- AC-09 → REQ-01"),
                         "AC-09 → REQ-01 com ID inexistente")

    def test_rejects_item_without_test(self) -> None:
        items = "| T-01 | D-01 | `src/f.py` | — | — | exit 0 |\n| T-02 | D-01 | `src/g.py` | T-01 | AC-02 | exit 0 |"
        errs = self.errors(task(self.src_sha, oracle_sha=self.t_sha, items=items))
        self.assertTrue(any("T-01 sem teste" in e for e in errs), errs)
        self.assertTrue(any("AC-01 não é coberto" in e for e in errs), errs)

    def test_rejects_req_without_decision(self) -> None:
        self.assertError(task(self.src_sha, oracle_sha=self.t_sha, decisions="| D-01 | REQ-01 | x | y |"), "REQ-02 sem decisão")

    def test_rejects_missing_prompt_skill_record(self) -> None:
        self.assertError(task(self.src_sha, oracle_sha=self.t_sha, skills="| `.codex/skills/rust/SKILL.md` | x | y |"), "Skills lidas")

    def test_rejects_stale_input_and_truncated_criterion(self) -> None:
        (self.root / "src/f.py").write_text("f = 3\n")
        self.assertError(task(self.src_sha, oracle_sha=self.t_sha), "AC-01 APPROVED com input I-01 stale")
        obs = f"| AC-01 | `{sha(AC1)[:16]}` | unittest | I-01 | exit 0 | APPROVED |"
        self.assertError(task(self.src_sha, oracle_sha=self.t_sha, obs=obs), "com critério malformed")

    def test_rejects_item_without_valid_skill(self) -> None:
        row2 = "| T-02 | D-01 | `src/g.py` | T-01 | AC-02 | exit 0 |"
        cases = {
            "": "T-01 sem skill",
            "skill de testes": "T-01 sem skill",
            "nenhuma:": "T-01 com 'nenhuma:' sem motivo",
            "`gleam`": "T-01 cita skill inexistente 'gleam'",
            "`../prompt`": "T-01 cita skill inexistente '../prompt'",
            "`rust`": "T-01 usa 'rust', ausente de Skills lidas",
        }
        for cell, fragment in cases.items():
            with self.subTest(cell=cell):
                items = f"| T-01 | D-01 | `src/f.py` | — | AC-01 | exit 0 | {cell} |\n{row2} nenhuma: x y z |"
                self.assertError(task(self.src_sha, oracle_sha=self.t_sha, items=items), fragment)
        no_column = task(self.src_sha, oracle_sha=self.t_sha).replace(" Skill |", "").replace("|---|---|---|---|---|---|---|",
                                                                                         "|---|---|---|---|---|---|")
        self.assertError(no_column, "tabela de itens sem a coluna 'Skill'")

    def errors_as(self, text: str, task_id: str) -> list[str]:
        path = self.root / f"sdd/tasks/{task_id}.md"
        path.write_text(text.replace("FIX-20261124", task_id))
        return V.task_errors(self.root, path, self.pattern)

    def without_skill_column(self, **kw) -> str:
        items = "| T-01 | D-01 | `src/f.py` | — | AC-01 | exit 0 |\n| T-02 | D-01 | `src/g.py` | T-01 | AC-02 | exit 0 |"
        text = task(self.src_sha, oracle_sha=self.t_sha, items=items, **kw).replace(" Skill |", "")
        return text.replace("|---|---|---|---|---|---|---|", "|---|---|---|---|---|---|")

    def test_task_opened_before_skill_column_passes_without_it(self) -> None:
        self.assertEqual(self.errors_as(self.without_skill_column(opened="2026-11-23"), "FIX-20261123"), [])
        local = self.without_skill_column(route="Local — reparo")
        self.assertFalse(any("Skill" in e for e in self.errors(local)))

    def test_skill_column_exemption_needs_both_dates_before_cutoff(self) -> None:
        missing = "tabela de itens sem a coluna 'Skill'"
        antedated = self.without_skill_column(opened="2026-11-01")
        self.assertTrue(any(missing in e for e in self.errors(antedated)), "ID de 2026-11-24 com metadado antedatado")
        for opened in ("", "23/11/2026", "2026-11-24"):
            with self.subTest(opened=opened):
                text = self.without_skill_column(opened="2026-11-23").replace("- Data de abertura: 2026-11-23",
                                                                              f"- Data de abertura: {opened}")
                self.assertTrue(any(missing in e for e in self.errors_as(text, "FIX-20261123")))

    def test_skill_cell_forms(self) -> None:
        row2 = "| T-02 | D-01 | `src/g.py` | T-01 | AC-02 | exit 0 | nenhuma: só renomeia |"

        def errs(cell: str, skills: str = SKILLS) -> list[str]:
            items = f"| T-01 | D-01 | `src/f.py` | — | AC-01 | exit 0 | {cell} |\n{row2}"
            return self.errors(task(self.src_sha, oracle_sha=self.t_sha, items=items, skills=skills))

        self.assertEqual(errs("`nenhuma: edição de texto`"), [], "forma com crases do contrato")
        self.assertEqual(errs("`software-testing`, `prompt`"), [])
        self.assertTrue(any("texto fora de crases" in e for e in errs("`software-testing` e rust")))
        bak = SKILLS.replace(".codex/skills/software-testing/SKILL.md", "x.codex/skills/software-testing/SKILL.md.bak")
        self.assertTrue(any("ausente de Skills lidas" in e for e in errs("`software-testing`", bak)))
        traversal = SKILLS + "\n| `.codex/skills/../skills/prompt/SKILL.md` | x | y |"
        self.assertTrue(any("inexistente '../skills/prompt'" in e for e in errs("`../skills/prompt`", traversal)))

    def test_concluded_task_tolerates_input_drift_after_closure_only(self) -> None:
        (self.root / "src/f.py").write_text("f = 3\n")
        self.assertEqual(self.concluded(self.FULL9), [], "input alterado depois do fechamento é retomada")
        (self.root / "src/f.py").unlink()
        self.assertEqual(self.concluded(self.FULL9), [], "input removido depois do fechamento é retomada")
        open_errs = self.errors(task(self.src_sha, oracle_sha=self.t_sha))
        self.assertTrue(any("input I-01 missing" in e for e in open_errs), open_errs)
        obs = (f"| AC-01 | `{sha(AC1)}` | unittest | I-01, I-09 | exit 0 | APPROVED |\n"
               f"| AC-02 | `{sha(AC2 + ' ')}` | unittest | I-01, I-02 | exit 0 | APPROVED |")
        errs = self.errors(task(self.src_sha, oracle_sha=self.t_sha, state="concluída", obs=obs, section9=self.FULL9))
        self.assertTrue(any("AC-02 APPROVED com critério stale" in e for e in errs), errs)
        self.assertTrue(any("AC-01 APPROVED com input I-09 missing" in e for e in errs), errs)
        (self.root / "src/f.py").write_text("f = 2\n")
        malformed = task(self.src_sha[:20], oracle_sha=self.t_sha, state="concluída", obs=obs, section9=self.FULL9)
        self.assertTrue(any("AC-01 APPROVED com input I-01 malformed" in e for e in self.errors(malformed)))

    def test_concluded_task_still_rejects_inputs_never_hashed(self) -> None:
        obs = (f"| AC-01 | `{sha(AC1)}` | unittest | I-01, I-02 | exit 0 | APPROVED |\n"
               f"| AC-02 | `{sha(AC2)}` | unittest | I-01, I-02 | exit 0 | APPROVED |")

        def errs(src_hash: str) -> list[str]:
            return self.errors(task(src_hash, oracle_sha=self.t_sha, state="concluída", obs=obs, section9=self.FULL9))

        (self.root / "src/f.py").unlink()
        for recorded in (self.src_sha[:20], "", "<64 hex>"):
            with self.subTest(recorded=recorded, case="arquivo ausente"):
                self.assertTrue(any("input I-01" in e for e in errs(recorded)))
        (self.root / "real.py").write_text("f = 2\n")
        (self.root / "src/f.py").symlink_to(self.root / "real.py")
        self.assertTrue(any("input I-01 missing" in e for e in errs("zz")), "symlink com hash malformado")
        self.assertTrue(any("input I-01 missing" in e for e in errs(self.src_sha)), "symlink com hash válido")

    def test_rejects_invalid_state_and_observed_pending(self) -> None:
        obs = f"| AC-01 | `{sha(AC1)}` | unittest | I-01 | exit 0 | APROVADO |"
        self.assertError(task(self.src_sha, oracle_sha=self.t_sha, obs=obs), "fora dos cinco estados")
        pend = "- AC-02: limite | PENDENTE: Q-1"
        obs2 = (f"| AC-01 | `{sha(AC1)}` | unittest | I-01 | exit 0 | APPROVED |\n"
                f"| AC-02 | `{sha(pend)}` | x | I-01 | ok | UNVERIFIED |")
        self.assertError(task(self.src_sha, oracle_sha=self.t_sha, ac2=pend, obs=obs2, questions="| Q-1 | ? | — | AC-02 |"),
                         "AC-02 observado enquanto PENDENTE")

    def test_rejects_concluded_task_with_open_criterion(self) -> None:
        errs = self.errors(task(self.src_sha, oracle_sha=self.t_sha, state="concluída", section9="- Estado final: concluída"))
        self.assertTrue(any("task concluída com AC-02" in e for e in errs), errs)

    def test_local_route_skips_plan_tables_but_keeps_prompt_skill(self) -> None:
        text = task(self.src_sha, oracle_sha=self.t_sha, route="Local — reparo").replace("| D-01 | REQ-01, REQ-02 | x | y |", "")
        self.assertEqual([e for e in self.errors(text) if "etapa 4: REQ" in e], [])
        local = task(self.src_sha, oracle_sha=self.t_sha, route="Local — reparo", skills="")
        self.assertTrue(any("Skills lidas" in e for e in self.errors(local)))

    def test_rejects_header_and_metadata(self) -> None:
        text = task(self.src_sha, oracle_sha=self.t_sha).replace("# FIX-20261124 —", "# OUTRO-20261124 —").replace("- Rota: Completa", "- Rota: Rápida")
        errs = self.errors(text)
        self.assertTrue(any("difere do nome do arquivo" in e for e in errs), errs)
        self.assertTrue(any("'Rota'" in e for e in errs), errs)

    def run_cli(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, "-B", str(TOOLS / "validate.py"), "--root", str(self.root), *args],
                              capture_output=True, text=True, check=False)

    def test_cli_exit_codes(self) -> None:
        (self.root / "sdd/tasks/FIX-20261124.md").write_text(task(self.src_sha, oracle_sha=self.t_sha))
        self.assertEqual(self.run_cli("--task", "FIX-20261124").returncode, 0)
        self.assertEqual(self.run_cli("--structure-only").returncode, 0)
        missing = self.run_cli("--task", "NOPE-20261124")
        self.assertEqual(missing.returncode, 2)
        self.assertIn("task inexistente", missing.stderr)
        self.assertEqual(self.run_cli("--structure-only", "--task", "FIX-20261124").returncode, 2)
        self.assertEqual(self.run_cli("--matrix").returncode, 2)
        matrix = self.run_cli("--task", "FIX-20261124", "--matrix")
        self.assertEqual(matrix.returncode, 0)
        self.assertIn("REQ-02 → D-01 → T-02 → AC-02", matrix.stdout)
        (self.root / "sdd/tasks/FIX-20261124.md").write_text(task(self.src_sha, oracle_sha=self.t_sha, ac2="- AC-02: x"))
        bad = self.run_cli()
        self.assertEqual(bad.returncode, 1)
        self.assertIn("FAIL: sdd/tasks/FIX-20261124.md: etapa 1", bad.stdout)

    def test_structure_only_reports_missing_file(self) -> None:
        (self.root / "sdd/project.md").unlink()
        res = self.run_cli("--structure-only")
        self.assertEqual(res.returncode, 1)
        self.assertIn("FAIL: sdd/project.md: ausente", res.stdout)

    def test_spec_rules(self) -> None:
        spec = self.root / "sdd/specs/cap.md"
        spec.write_text("# Spec — cap\n\n- REQ-01: a\n- REQ-02: b\n\n- AC-01 → REQ-01: x | método: y | esperado: z\n"
                        "- AC-02 → REQ-03: x\n\n| AC | Estado | Decidido por (task) | Data |\n|---|---|---|---|\n"
                        "| AC-01 | APROVADO | — | — |\n")
        errs = V.spec_errors(spec)
        for fragment in ("AC-02 (linha", "REQ-03: REQ inexistente", "REQ-02 sem AC", "fora dos cinco estados"):
            self.assertTrue(any(fragment in e for e in errs), (fragment, errs))

    def test_spec_inherited_criterion_needs_no_method_but_keeps_links(self) -> None:
        spec = self.root / "sdd/specs/cap.md"
        spec.write_text("# Spec — cap\n\n- REQ-01: a\n\n- AC-01 → REQ-01: texto migrado (herdado)\n\n"
                        "| AC | Estado | Decidido por (task) | Data |\n|---|---|---|---|\n| AC-01 | INCONCLUSIVE | — | — |\n")
        self.assertEqual(V.spec_errors(spec), [])
        spec.write_text("# Spec — cap\n\n- REQ-01: a\n\n- AC-01 → REQ-02: texto (herdado)\n- AC-02 → REQ-01: (herdado) no meio\n")
        errs = V.spec_errors(spec)
        self.assertTrue(any("REQ-02: REQ inexistente" in e for e in errs), errs)
        self.assertTrue(any("AC-02 (linha" in e for e in errs), errs)


if __name__ == "__main__":
    unittest.main()
