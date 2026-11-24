#!/usr/bin/env python3
"""Validador do SDD do Ox: estrutura de sdd/ e gates dos registros de task.

Implementa os gates verificáveis mecanicamente de sdd/workflow.md sobre
sdd/tasks/<ID>.md e sdd/specs/*.md. Usa o parser único sdd/tools/sddtask.py.
Somente leitura; Python 3.11+ stdlib. Um exit 0 prova formato e coerência
declarada, não comportamento do produto nem adequação dos oráculos.

Uso, da raiz do Ox:
  python3 sdd/tools/validate.py --root .                 # estrutura + todas as tasks e specs
  python3 sdd/tools/validate.py --root . --structure-only
  python3 sdd/tools/validate.py --root . --task <ID> [--task <ID>] [--matrix]

`--matrix` imprime a matriz REQ → D → T → AC derivada das seções 3-5 (etapa 6).

Saída 0: sem falhas. Saída 1: falhas de validação (linhas "FAIL: ...").
Saída 2: uso inválido, task inexistente ou arquivo ilegível.
"""
from __future__ import annotations

import argparse
import importlib
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
T = importlib.import_module("sddtask")

REQUIRED_FILES = ("constitution.md", "project.md", "workflow.md", "templates/task.md", "templates/spec.md")
REQUIRED_DIRS = ("tasks", "specs", "tools")
ROUTES = ("Local", "Completa")
TASK_STATES = ("aberta", "concluída", "incompleta", "bloqueada")
ID_RE = re.compile(r"^[A-Z0-9]+(?:-[A-Z0-9]+)*-\d{8}(?:-\d+)?$")
PROMPT_SKILL = ".codex/skills/prompt/SKILL.md"
NO_ORACLE = "sem oráculo separado:"
CLOSURE_FIELDS = ("Documentação", "`sdd/project.md`", "Inputs da seção 8 alterados no fechamento",
                  "Checks de governança", "Pendências", "Estado final")
INHERITED = "(herdado)"
# A coluna Skill da seção 5 vale para tasks Completa abertas a partir desta data; registros
# anteriores foram fechados sem ela e não são reescritos.
SKILL_COLUMN_SINCE = "2026-11-24"
# Em task concluída, arquivo de input alterado ou removido depois do fechamento é caso de
# retomada (sdd/workflow.md, Evidência e retomada), não falha estrutural do registro.
POST_CLOSE_DRIFT = {"stale", "missing"}
LOCAL_DIR = ".local"  # ignorado pelo Git: evidência citada ali não é conferível em outro checkout
LOCAL_RE = re.compile(r"(?<![\w.-])\.local/")
# Tabelas das etapas 4 e 5: primeiro cabeçalho → nome usado nas mensagens.
STAGE_TABLES = {4: {"Decisão": "decisão", "SKILL.md": "skill lida"}, 5: {"Item": "item"}}
SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
EMPTY = {"", "—", "-", "\u2013"}


class UsageError(Exception):
    pass


def forbidden_terms(root: Path) -> list[str]:
    """Termos da coluna "Proibido" da tabela da etapa 1 de sdd/workflow.md."""
    workflow = root / "sdd" / "workflow.md"
    lines = T.unfenced(workflow.read_text(encoding="utf-8").splitlines())
    terms: list[str] = []
    for table in T.parse_tables(lines):
        if table.header and table.header[0] == "Proibido":
            for row in table.rows:
                terms += [t.strip().lower() for t in row["Proibido"].split(",") if t.strip()]
    return terms


def term_pattern(terms: list[str]) -> re.Pattern[str] | None:
    if not terms:
        return None
    variants = []
    for term in terms:
        word = re.escape(term)
        if term.endswith("o") and " " not in term:
            word = re.escape(term[:-1]) + "[oa]s?"
        elif " " not in term:
            word += "s?"
        variants.append(word)
    return re.compile(r"(?<![\w-])(?:" + "|".join(variants) + r")(?![\w-])", re.IGNORECASE)


ID_TOKEN_RE = re.compile(r"\b(?:AC|REQ|D|T|I|Q|POL|GOV|RQ)-\d+[a-z]?\b")
UNITS = (r"ms|s|seg|segundos?|min|minutos?|h|horas?|%|px|pt|dp|fps|b|kb|kib|mb|mib|gb|gib|"
         r"bytes?|itens|linhas|palavras|testes|arquivos|cliques|passos|requisições|req/s|x")
# Métrica = comparador seguido de número, número seguido de unidade, ou percentil (p95).
METRIC_RE = re.compile(rf"(?:[<>≤≥=]\s*=?\s*\d)|(?:\d[\d.,]*\s*(?:{UNITS})(?![\w]))|(?:\bp\d{{2}}\b)",
                       re.IGNORECASE)


def subjective_hits(lines: T.Lines, pattern: re.Pattern[str] | None) -> list[tuple[int, str]]:
    """Termo proibido sem métrica na mesma parte da linha.

    A linha é dividida em partes por " | " (condição, método, esperado de um AC). Um
    termo só é aceito se a própria parte tiver uma métrica (METRIC_RE: comparador com
    número, número com unidade ou percentil), fora de crases e de IDs, ou se a linha for
    um AC pendente (`PENDENTE: Q-n`). Número solto (ex.: "versão 2") não é métrica.
    """
    if pattern is None:
        return []
    hits = []
    for n, line in lines:
        if T.PENDING_RE.search(line):
            continue
        for part in line.split(" | "):
            plain = ID_TOKEN_RE.sub("", re.sub(r"`[^`]*`", "", part))
            m = pattern.search(plain)
            if m and not METRIC_RE.search(plain):
                hits.append((n, m.group(0)))
    return hits


def cell_ids(cell: str, prefix: str) -> list[str]:
    return re.findall(rf"\b{prefix}-\d+[a-z]?\b", cell)


def plan_items(task: T.Task) -> tuple[dict[str, set[str]], dict[str, str]]:
    """Itens da seção 5: ACs citados na coluna Teste e decisão de cada item."""
    item_acs: dict[str, set[str]] = {}
    item_d: dict[str, str] = {}
    items = task.table(5, "Item")
    for row in (items.rows if items else []):
        tid = T.strip_code(row.get("Item", ""))
        item_acs[tid] = set(cell_ids(row.get("Teste", ""), "AC"))
        item_d[tid] = T.strip_code(row.get("D", ""))
    return item_acs, item_d


def coherence_matrix(task: T.Task) -> list[tuple[str, list[str], list[str], list[str]]]:
    """Matriz REQ → D → T → AC derivada das seções 3 (AC → REQ) e 5 (itens)."""
    item_acs, item_d = plan_items(task)
    rows = []
    for req in sorted(task.reqs):
        acs = sorted(a for a, rs in task.ac_req.items() if req in rs)
        items = sorted(t for t, a in item_acs.items() if a & set(acs))
        decisions = sorted({item_d[t] for t in items if item_d[t] not in EMPTY})
        rows.append((req, decisions, items, acs))
    return rows


def opened_dates(task: T.Task) -> list[str]:
    """Datas ISO de abertura: a do ID (`<TEMA>-<AAAAMMDD>`) e a do metadado, quando válidas."""
    dates = []
    m = re.search(r"-(\d{4})(\d{2})(\d{2})(?:-\d+)?$", task.id or "")
    if m:
        dates.append("-".join(m.groups()))
    opened = task.meta.get("Data de abertura", "")
    if DATE_RE.match(opened):
        dates.append(opened)
    return dates


def item_skill_errors(root: Path, task: T.Task, items: T.Table, skills: T.Table | None) -> list[str]:
    """Etapa 5: cada item cita skill existente e lida, ou 'nenhuma: <motivo>'.

    Dispensa só registro cujas duas datas (ID e metadado) existem e são anteriores a
    SKILL_COLUMN_SINCE; data ausente, malformada ou divergente exige a coluna.
    """
    dates = opened_dates(task)
    if len(dates) == 2 and max(dates) < SKILL_COLUMN_SINCE:
        return []
    if "Skill" not in items.header:
        return ["etapa 5: tabela de itens sem a coluna 'Skill'"]
    read = {T.strip_code(r.get("SKILL.md", "")) for r in (skills.rows if skills else [])}
    errs = []
    for row in items.rows:
        tid = T.strip_code(row.get("Item", ""))
        cell = row.get("Skill", "").strip()
        none = re.fullmatch(r"(`?)nenhuma:(.*?)\1", cell)
        if none:
            if not re.search(r"\w{3}", none.group(2)):
                errs.append(f"etapa 5: {tid} com 'nenhuma:' sem motivo")
            continue
        names = re.findall(r"`([^`]*)`", cell)
        if not names:
            errs.append(f"etapa 5: {tid} sem skill (`nome` ou 'nenhuma: <motivo>')")
        elif not re.fullmatch(r"(?:[\s,;]|\be\b)*", re.sub(r"`[^`]*`", "", cell)):
            errs.append(f"etapa 5: {tid} com texto fora de crases na coluna Skill")
        for name in names:
            if not SKILL_NAME_RE.match(name) or not (root / ".codex/skills" / name / "SKILL.md").is_file():
                errs.append(f"etapa 5: {tid} cita skill inexistente '{name}'")
            elif f".codex/skills/{name}/SKILL.md" not in read:
                errs.append(f"etapa 5: {tid} usa '{name}', ausente de Skills lidas")
    return errs


def structure_errors(root: Path) -> list[str]:
    base = root / "sdd"
    errors = [f"sdd/{name}: ausente" for name in REQUIRED_FILES if not (base / name).is_file()]
    errors += [f"sdd/{name}/: ausente" for name in REQUIRED_DIRS if not (base / name).is_dir()]
    if (base / "workflow.md").is_file() and not forbidden_terms(root):
        errors.append("sdd/workflow.md: tabela de termos proibidos (coluna \"Proibido\") ausente")
    return errors


def local_input(root: Path, task: T.Task, inp: dict[str, str]) -> bool:
    """Input em `.local/` (workflow, Evidência e retomada): na célula, em qualquer forma, ou
    no caminho resolvido (`sdd/../.local/…`, link relativo ao registro, symlink)."""
    if LOCAL_RE.search(inp["source"]):
        return True
    target = T.single_path(inp["source"], task.path.parent, root)
    return (target is not None and T.contained(target, root)
            and target.resolve().is_relative_to((root / LOCAL_DIR).resolve()))


def drifted_after_close(root: Path, task: T.Task, inp: dict[str, str]) -> bool:
    """Input com SHA-256 completo gravado e arquivo comum alterado ou removido depois.

    Hash vazio ou malformado nunca foi uma observação válida; symlink nunca é input
    por bytes. Nos dois casos a falha da etapa 8 continua.
    """
    if not T.SHA_RE.match(inp["sha256"]):
        return False
    target = T.single_path(inp["source"], task.path.parent, root)
    return target is not None and not target.is_symlink()


def task_errors(root: Path, path: Path, pattern: re.Pattern[str] | None) -> list[str]:
    task = T.parse(path)
    errs: list[str] = []
    add = errs.append

    # Cabeçalho e metadados
    if not task.id or not task.title:
        add("primeira linha deve ser '# <ID> — <título>'")
    elif task.id != path.stem:
        add(f"ID '{task.id}' difere do nome do arquivo '{path.stem}'")
    elif not ID_RE.match(task.id):
        add(f"ID '{task.id}' fora do formato <TEMA>-<AAAAMMDD>")
    route = task.meta.get("Rota", "")
    completa = route.startswith("Completa")
    if not route.startswith(ROUTES):
        add("metadado 'Rota' deve começar com Local ou Completa")
    if not task.meta.get("Estado", "").startswith(TASK_STATES):
        add("metadado 'Estado' deve começar com " + ", ".join(TASK_STATES))
    if "Revisão atual" not in task.meta:
        add("metadado 'Revisão atual' ausente")
    missing = [n for n in range(1, 10) if n not in task.sections]
    if missing:
        add("seções ausentes: " + ", ".join(f"## {n}." for n in missing))

    # Etapa 1 — prompt
    for n, name in T.DIVISIONS.items():
        if n not in task.divisions:
            add(f"etapa 1: divisão '### {n} - {name}' ausente")
    if 3 in task.divisions and not any(re.match(r"^\s*[-*] \S", text) for _, text in task.divisions[3]):
        add("etapa 1: '3 - Restrições' sem guardrail listado")
    if 5 in task.divisions and "Regra de conclusão" not in "\n".join(text for _, text in task.divisions[5]):
        add("etapa 1: '5 - Entrega' sem 'Regra de conclusão'")
    if not task.criteria:
        add("etapa 1: nenhum critério '- AC-n: …' em '4 - Critérios de Aceitação'")
    for c in task.criteria:
        if not c.pending and not (c.method and c.expected):
            add(f"etapa 1: {c.id} (linha {c.lineno}) sem 'método:' e 'esperado:' nem 'PENDENTE: Q-n'")
    for div in (2, 4):
        for n, term in subjective_hits(task.divisions.get(div, []), pattern):
            add(f"etapa 1: termo subjetivo sem métrica '{term}' (linha {n})")

    # Etapa 2 — perguntas dos ACs pendentes registradas
    q_text = task.section_text(2)
    for c in task.criteria:
        if c.pending and not re.search(rf"\b{re.escape(c.pending)}\b", q_text):
            add(f"etapa 2: {c.id} pendente de {c.pending}, que não está registrada na seção 2")

    # Etapa 3 — REQ ↔ AC
    ac_ids = {c.id for c in task.criteria}
    if completa or task.reqs:
        for ac in sorted(ac_ids - set(task.ac_req)):
            add(f"etapa 3: {ac} sem REQ ('- {ac} → REQ-n')")
        mapped_reqs = {r for rs in task.ac_req.values() for r in rs}
        for req in sorted(set(task.reqs) - mapped_reqs):
            add(f"etapa 3: {req} sem AC")
        for ac, rs in sorted(task.ac_req.items()):
            for r in rs:
                if ac not in ac_ids or r not in task.reqs:
                    add(f"etapa 3: mapeamento {ac} → {r} com ID inexistente")

    # Etapa 4 — skills lidas (toda rota) e decisões (rota Completa)
    skills = task.table(4, "SKILL.md")
    if skills is None or not any(PROMPT_SKILL in r.get("SKILL.md", "") for r in skills.rows):
        add(f"etapa 4: tabela 'Skills lidas' sem a linha de `{PROMPT_SKILL}`")
    decisions = task.table(4, "Decisão")
    dec_ids = {T.strip_code(r["Decisão"]) for r in decisions.rows} if decisions else set()
    dec_reqs = {T.strip_code(r["Decisão"]): set(cell_ids(r.get("REQ", ""), "REQ"))
                for r in (decisions.rows if decisions else [])}
    if completa:
        covered = {r for row in (decisions.rows if decisions else []) for r in cell_ids(row.get("REQ", ""), "REQ")}
        for req in sorted(set(task.reqs) - covered):
            add(f"etapa 4: {req} sem decisão")

    # Etapas 4-5 — tabelas reconhecidas, IDs presentes e únicos por camada (seção e revisões)
    for num, known in STAGE_TABLES.items():
        for t in task.stage_tables(num):
            if t.header and t.header[0] not in known:
                add(f"etapa {num}: tabela '{t.header[0]}' não reconhecida; a primeira coluna é "
                    + " ou ".join(f"'{h}'" for h in known))
        for first, label in known.items():
            merged = task.table(num, first)
            for dup in dict.fromkeys(merged.duplicates if merged else []):
                add(f"etapa {num}: {label} com ID {dup or '(vazio)'} repetido na mesma camada")
            for row in (merged.rows if merged else []):
                if T.strip_code(row.get(first, "")) in EMPTY:
                    add(f"etapa {num}: linha de {label} sem ID")

    # Etapas 5-6 — itens e matriz derivada (rota Completa); a matriz não é redigida à mão
    items = task.table(5, "Item")
    if completa:
        if items is None:
            add("etapa 5: tabela de itens ausente")
        else:
            item_acs, item_d = plan_items(task)
            for row in items.rows:
                tid = T.strip_code(row.get("Item", ""))
                acs = item_acs[tid]
                if row.get("Teste", "").strip() in EMPTY:
                    add(f"etapa 5: {tid} sem teste")
                for ac in sorted(acs - ac_ids):
                    add(f"etapa 5: {tid} testa {ac}, que não existe")
                if item_d[tid] not in EMPTY and item_d[tid] not in dec_ids:
                    add(f"etapa 5: {tid} cita {item_d[tid]}, que não está nas decisões")
                elif item_d[tid] in dec_ids:
                    for ac in sorted(acs & ac_ids):
                        for req in task.ac_req.get(ac, []):
                            if req not in dec_reqs[item_d[tid]]:
                                add(f"etapa 5: {tid} usa {item_d[tid]}, que não atende {req} (de {ac})")
                if row.get("Pronto quando", "").strip() in EMPTY:
                    add(f"etapa 5: {tid} sem condição de pronto")
            for ac in sorted(ac_ids - set().union(*item_acs.values())):
                add(f"etapa 5: {ac} não é coberto por nenhum item")
            for d in sorted(dec_ids - set(item_d.values())):
                add(f"etapa 5: {d} não é coberto por nenhum item")
            for req, _, tids, _ in coherence_matrix(task):
                if not tids:
                    add(f"etapa 6: {req} sem item que teste seus AC")
            errs += item_skill_errors(root, task, items, skills)

    # Etapa 8 — evidência vigente
    observations, obs_issues = T.effective_observations(task)
    concluded = task.meta.get("Estado", "").startswith("concluída")
    inputs, input_issues = T.recorded_inputs(task)
    status = {(r["kind"], r["id"]): r["status"] for r in T.freshness(task, root)}
    for issue in task.issues + obs_issues + input_issues:
        add(f"etapa 8: {issue['kind']} {issue['id']} (linha {issue['line']})")
    by_id = {c.id: c for c in task.criteria}
    for ac, row in sorted(observations.items()):
        state = row.get("Estado", "").split("(")[0].strip()
        if state not in T.STATES:
            add(f"etapa 8: {ac} com estado '{state}' fora dos cinco estados")
            continue
        if ac in by_id and by_id[ac].pending:
            add(f"etapa 8: {ac} observado enquanto PENDENTE")
        if state == "NOT APPLICABLE" and row.get("Resultado observado", "").strip() in EMPTY:
            add(f"etapa 8: {ac} NOT APPLICABLE sem motivo")
        if state not in T.DECIDED:
            continue
        crit = status.get(("criterion", ac))
        if crit != "fresh":
            add(f"etapa 8: {ac} {state} com critério {crit}")
        refs = T.INPUT_ID_RE.findall(row.get("Inputs", ""))
        if not refs:
            add(f"etapa 8: {ac} {state} sem inputs I-n")
        for ref in refs:
            if ref in inputs and local_input(root, task, inputs[ref]):
                add(f"etapa 8: {ac} {state} com input {ref} em {LOCAL_DIR}/, fora do Git; versione em sdd/tasks/<ID>/")
            st = status.get(("input", ref), "missing") if ref in inputs else "missing"
            if concluded and ref in inputs and st in POST_CLOSE_DRIFT and drifted_after_close(root, task, inputs[ref]):
                continue  # input mudou depois do fechamento: retomada (`evidence --check`), não falha
            if st in T.PROBLEM_STATUSES:
                add(f"etapa 8: {ac} {state} com input {ref} {st}")
        roles = {inputs[r]["role"] for r in refs if r in inputs}
        if refs and "material" not in roles:
            add(f"etapa 8: {ac} {state} sem input 'material'")
        justified = re.search(re.escape(NO_ORACLE) + r"\s*([^;|]*)", row.get("Inputs", ""))
        if "oráculo" not in roles and not (justified and re.search(r"\w{3}", justified.group(1))):
            add(f"etapa 8: {ac} {state} sem input 'oráculo' nem '{NO_ORACLE} <motivo>'")
        for column in ("Método executado", "Resultado observado"):
            if row.get(column, "").strip() in EMPTY:
                add(f"etapa 8: {ac} {state} com '{column}' vazio")

    # Etapa 9 — fechamento
    if task.meta.get("Estado", "").startswith("concluída"):
        for c in task.criteria:
            st = observations.get(c.id, {}).get("Estado", "").split("(")[0].strip()
            if st not in ("APPROVED", "NOT APPLICABLE"):
                add(f"etapa 9: task concluída com {c.id} em '{st or 'sem observação'}'")
        closing = task.section_text(9)
        if re.search(r"<[^>\n]+>", closing):
            add("etapa 9: seção 9 com marcador de template '<…>'")
        for fieldname in CLOSURE_FIELDS:
            m = re.search(rf"^- {re.escape(fieldname)}: *(.*)$", closing, re.M)
            if not m or m.group(1).strip() in EMPTY:
                add(f"etapa 9: campo '{fieldname}' ausente ou vazio na seção 9")
        # A revisão mais recente decide (workflow): a última linha, não a do fechamento original.
        finals = re.findall(r"^- Estado final: *(\S+)", closing, re.M)
        if finals and not finals[-1].startswith("concluída"):
            add("etapa 9: 'Estado final' difere do metadado 'Estado: concluída'")
    return errs


def spec_errors(path: Path) -> list[str]:
    lines = T.unfenced(path.read_text(encoding="utf-8").splitlines())
    errs = []
    if not lines or not lines[0][1].startswith("# Spec — "):
        errs.append("primeira linha deve ser '# Spec — <capacidade>'")
    reqs = {m.group("id") for _, text in lines if (m := T.REQ_RE.match(text))}
    acs: dict[str, list[str]] = {}
    for n, line in lines:
        m = re.match(r"^- (AC-\d+) → (REQ-\d+): (.+)$", line)
        if m:
            acs[m.group(1)] = [m.group(2)]
            inherited = line.rstrip().endswith(INHERITED)
            if not inherited and not (" | método:" in line and " | esperado:" in line):
                errs.append(f"{m.group(1)} (linha {n}) sem 'método:' e 'esperado:'")
            if m.group(2) not in reqs:
                errs.append(f"{m.group(1)} → {m.group(2)}: REQ inexistente")
    for req in sorted(reqs - {r for rs in acs.values() for r in rs}):
        errs.append(f"{req} sem AC")
    for table in T.parse_tables(lines):
        if table.header and table.header[0] == "AC" and "Estado" in table.header:
            for row in table.rows:
                state = row["Estado"].strip()
                if state not in T.STATES:
                    errs.append(f"estado atual de {row['AC']} fora dos cinco estados: '{state}'")
    return errs


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=".", type=Path)
    ap.add_argument("--structure-only", action="store_true", help="só a estrutura de sdd/")
    ap.add_argument("--task", action="append", default=[], help="ID de task (repetível)")
    ap.add_argument("--matrix", action="store_true", help="imprime a matriz derivada das tasks de --task")
    args = ap.parse_args(argv)
    root = args.root.resolve()
    if args.structure_only and args.task:
        print("--structure-only não combina com --task", file=sys.stderr)
        return 2
    if args.matrix and not args.task:
        print("--matrix exige --task", file=sys.stderr)
        return 2
    try:
        failures = [f"FAIL: {e}" for e in structure_errors(root)]
        checked_tasks = checked_specs = 0
        if not args.structure_only and not failures:
            pattern = term_pattern(forbidden_terms(root))
            if args.task:
                paths = []
                for tid in args.task:
                    if not ID_RE.match(tid):
                        raise UsageError(f"ID de task inválido: {tid}")
                    p = root / "sdd" / "tasks" / f"{tid}.md"
                    if not p.is_file() or p.is_symlink():
                        raise UsageError(f"task inexistente: sdd/tasks/{tid}.md")
                    paths.append(p)
                specs: list[Path] = []
            else:
                paths = T.find_tasks(root)
                specs = sorted(p for p in (root / "sdd" / "specs").glob("*.md")
                               if p.name != "README.md" and p.is_file() and not p.is_symlink())
            for p in paths:
                rel = p.relative_to(root).as_posix()
                failures += [f"FAIL: {rel}: {e}" for e in task_errors(root, p, pattern)]
                checked_tasks += 1
                if args.matrix:
                    print(f"Matriz {rel}:")
                    for req, ds, ts, acs in coherence_matrix(T.parse(p)):
                        print(f"  {req} → {', '.join(ds) or '—'} → {', '.join(ts) or '—'} → {', '.join(acs) or '—'}")
            for p in specs:
                rel = p.relative_to(root).as_posix()
                failures += [f"FAIL: {rel}: {e}" for e in spec_errors(p)]
                checked_specs += 1
    except UsageError as exc:
        print(exc, file=sys.stderr)
        return 2
    except (OSError, UnicodeDecodeError) as exc:
        print(f"erro de leitura: {exc}", file=sys.stderr)
        return 2
    for line in failures:
        print(line)
    if failures:
        print(f"{len(failures)} falha(s).")
        return 1
    scope = "estrutura" if args.structure_only else f"estrutura, {checked_tasks} task(s), {checked_specs} spec(s)"
    print(f"PASS: {scope}. Formato e coerência declarada; não prova comportamento do produto.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
