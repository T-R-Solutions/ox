#!/usr/bin/env python3
"""Leitura do registro de task do SDD do Ox (formato de sdd/templates/task.md).

Módulo único de parsing, usado pelo validador (sdd/tools/validate.py) e por
ferramentas de revisão. Python 3.11+ stdlib. Somente leitura, exceto
`evidence --write`, que regrava apenas as células SHA-256 da evidência vigente.

Uso, da raiz do Ox:
  python3 sdd/tools/sddtask.py evidence --task <ID>           # mostra o estado dos hashes
  python3 sdd/tools/sddtask.py evidence --task <ID> --write   # grava os hashes atuais
  python3 sdd/tools/sddtask.py evidence --task <ID> --check   # exit 1 se algum não estiver atual

Regras de leitura (sdd/workflow.md):
- Linhas dentro de blocos cercados (``` ou ~~~) e de comentários HTML iniciados no
  começo da linha (`<!-- … -->`) nunca são estrutura.
- Seções `## 1.`…`## 9.`; revisões `## Revisão rN — data` acrescentadas ao final,
  com subseções `### <n>. <nome>` das etapas afetadas.
- Critérios, mapa AC → REQ e tabelas das etapas 4 e 5 (`Task.table`): a seção original e o
  `### 1.`/`### 3.`/`### 4.`/`### 5.` de cada revisão; por ID vale a revisão mais recente.
- Evidência vigente: tabelas da seção 8 e de cada `### 8.` de revisão, fora de
  subseções cujo título contém "obsolet". Por AC vale a observação da revisão mais
  recente. IDs de input (`I-n`) são únicos no registro inteiro; só os citados por uma
  observação vigente são verificados.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

SHA_RE = re.compile(r"^[0-9a-f]{64}$")
SECTION_RE = re.compile(r"^## (?P<num>[1-9])\. (?P<name>.+?)\s*$")
REVISION_RE = re.compile(r"^## Revisão (?P<rev>r\d+)\b.*$")
REV_STAGE_RE = re.compile(r"^### (?P<num>[1-9])\. (?P<name>.+?)\s*$")
DIVISION_RE = re.compile(r"^### (?P<num>[1-5]) - (?P<name>.+?)\s*$")
HEADING_RE = re.compile(r"^(?P<hashes>#{1,6}) ")
FENCE_RE = re.compile(r"^\s{0,3}(?P<fence>`{3,}|~{3,})")
META_RE = re.compile(r"^- (?P<key>[^:]+): (?P<value>.*)$")
AC_LINE_RE = re.compile(r"^- (?P<id>AC-\d+): (?P<body>.+)$")
AC_REQ_RE = re.compile(r"^- (?P<ac>AC-\d+) → (?P<req>REQ-\d+)\b")
REQ_RE = re.compile(r"^- (?P<id>REQ-\d+): (?P<text>.+)$")
PENDING_RE = re.compile(r"\bPENDENTE: (?P<q>Q-\d+)\b")
AC_ID_RE = re.compile(r"^AC-\d+$")
INPUT_ID_RE = re.compile(r"\bI-\d+\b")
CRITERION_HEADERS = ("Critério (SHA-256)", "Critério (sha256 da linha)")

DIVISIONS = {1: "Objetivos", 2: "Requisitos", 3: "Restrições", 4: "Critérios de Aceitação", 5: "Entrega"}
STATES = {"APPROVED", "REJECTED", "UNVERIFIED", "INCONCLUSIVE", "NOT APPLICABLE"}
DECIDED = {"APPROVED", "REJECTED"}

Lines = list[tuple[int, str]]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_line(line: str) -> str:
    """SHA-256 do critério: a linha do AC em UTF-8, sem o newline final."""
    return sha256_bytes(line.rstrip("\n").encode("utf-8"))


def strip_code(cell: str) -> str:
    return cell.strip().strip("`").strip()


def unfenced(lines: list[str]) -> list[tuple[int, str]]:
    """(número da linha, texto) das linhas fora de blocos cercados e de comentários HTML
    que ocupam linhas inteiras; as linhas delimitadoras também são omitidas."""
    out, fence, comment = [], None, False
    for n, line in enumerate(lines, 1):
        if comment:
            comment = "-->" not in line
            continue
        if fence is None and line.lstrip().startswith("<!--"):
            comment = "-->" not in line
            continue
        m = FENCE_RE.match(line)
        if fence is None and m:
            fence = m.group("fence")
            continue
        if fence is not None:
            if m and m.group("fence")[0] == fence[0] and len(m.group("fence")) >= len(fence) \
                    and not line.strip()[len(m.group("fence")):].strip():
                fence = None
            continue
        out.append((n, line))
    return out


@dataclass
class Criterion:
    id: str
    line: str
    lineno: int
    sha256: str
    method: str | None
    expected: str | None
    pending: str | None


@dataclass
class Table:
    header: list[str]
    rows: list[dict[str, str]]
    lineno: int
    row_linenos: list[int]
    duplicates: list[str] = field(default_factory=list)  # IDs repetidos numa mesma camada (Task.table)


@dataclass
class Revision:
    rev: str
    lineno: int
    stages: dict[int, Lines]


@dataclass
class Task:
    path: Path
    id: str | None
    title: str | None
    meta: dict[str, str]
    sections: dict[int, Lines]
    revisions: list[Revision]
    divisions: dict[int, Lines]
    criteria: list[Criterion] = field(default_factory=list)
    reqs: dict[str, str] = field(default_factory=dict)
    ac_req: dict[str, list[str]] = field(default_factory=dict)
    issues: list[dict[str, str]] = field(default_factory=list)

    def section_text(self, num: int) -> str:
        parts = [line for _, line in self.sections.get(num, [])]
        for r in self.revisions:
            parts += [line for _, line in r.stages.get(num, [])]
        return "\n".join(parts)

    def tables(self, num: int) -> list[Table]:
        return parse_tables(self.sections.get(num, []))

    def stage_layers(self, num: int) -> list[Lines]:
        """Linhas da etapa `num`: a seção original e o `### num.` de cada revisão, em ordem."""
        return [self.sections.get(num, [])] + [r.stages[num] for r in self.revisions if num in r.stages]

    def stage_tables(self, num: int) -> list[Table]:
        """Todas as tabelas da etapa `num`, em todas as camadas."""
        return [t for lines in self.stage_layers(num) for t in parse_tables(lines)]

    def table(self, num: int, first_header: str) -> Table | None:
        """Tabela da etapa `num` cujo primeiro cabeçalho é `first_header`, com as revisões aplicadas.

        Camadas: a seção original e o `### num.` de cada revisão, em ordem; numa camada, todas
        as tabelas com esse cabeçalho contam. A linha de uma revisão substitui, na mesma posição,
        a de camada anterior com o mesmo ID (primeira coluna); ID novo é acrescentado. ID repetido
        na mesma camada mantém as duas linhas e entra em `duplicates`, para o validador reprovar.
        Colunas novas de uma revisão entram no cabeçalho.
        """
        merged: Table | None = None
        index: dict[str, int] = {}
        for lines in self.stage_layers(num):
            in_layer: set[str] = set()
            for t in parse_tables(lines):
                if not t.header or t.header[0] != first_header:
                    continue
                if merged is None:
                    merged = Table(list(t.header), [], t.lineno, [])
                else:
                    merged.header += [h for h in t.header if h not in merged.header]
                for row, n in zip(t.rows, t.row_linenos, strict=True):
                    key = strip_code(row.get(first_header, ""))
                    if key in in_layer:
                        merged.duplicates.append(key)
                    if key in index and key not in in_layer:
                        merged.rows[index[key]], merged.row_linenos[index[key]] = row, n
                    else:
                        index.setdefault(key, len(merged.rows))
                        merged.rows.append(row)
                        merged.row_linenos.append(n)
                    in_layer.add(key)
        return merged

    def evidence_layers(self) -> list[tuple[str, Lines]]:
        """Linhas vigentes da seção 8 e de cada `### 8.` de revisão, em ordem."""
        layers = [("r0", current_lines(self.sections.get(8, [])))]
        for r in self.revisions:
            if 8 in r.stages:
                layers.append((r.rev, current_lines(r.stages[8])))
        return layers


def current_lines(lines: Lines) -> Lines:
    """Remove subseções cujo título contém "obsolet" (até o próximo título de nível igual ou maior)."""
    out: Lines = []
    skip_level: int | None = None
    for n, line in lines:
        m = HEADING_RE.match(line)
        if m:
            level = len(m.group("hashes"))
            if skip_level is not None and level <= skip_level:
                skip_level = None
            if skip_level is None and "obsolet" in line.lower():
                skip_level = level
                continue
        if skip_level is None:
            out.append((n, line))
    return out


def split_row(line: str) -> list[str]:
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|"):
        body = body[:-1]
    cells, cur, tick, prev = [], "", False, ""
    for ch in body:
        if ch == "`":
            tick = not tick
        if ch == "|" and not tick and prev != "\\":
            cells.append(cur.strip())
            cur = ""
        else:
            cur += ch
        prev = ch
    cells.append(cur.strip())
    return cells


def parse_tables(lines: Lines) -> list[Table]:
    tables: list[Table] = []
    i = 0
    while i < len(lines):
        n, line = lines[i]
        nxt = lines[i + 1][1] if i + 1 < len(lines) else ""
        consecutive = i + 1 < len(lines) and lines[i + 1][0] == n + 1
        if line.lstrip().startswith("|") and consecutive and re.match(r"^\s*\|[\s:|-]+\|\s*$", nxt):
            header = split_row(line)
            rows, nums, j = [], [], i + 2
            while j < len(lines) and lines[j][1].lstrip().startswith("|") and lines[j][0] == lines[j - 1][0] + 1:
                cells = split_row(lines[j][1])
                rows.append({h: (cells[k] if k < len(cells) else "") for k, h in enumerate(header)})
                nums.append(lines[j][0])
                j += 1
            tables.append(Table(header, rows, n, nums))
            i = j
        else:
            i += 1
    return tables


def parse_criterion(line: str, lineno: int) -> Criterion | None:
    m = AC_LINE_RE.match(line)
    if not m:
        return None
    parts = [p.strip() for p in m.group("body").split(" | ")]
    method = next((p.split(":", 1)[1].strip() for p in parts if p.startswith("método:")), None)
    expected = next((p.split(":", 1)[1].strip() for p in parts if p.startswith("esperado:")), None)
    pend = PENDING_RE.search(m.group("body"))
    return Criterion(m.group("id"), line, lineno, sha256_line(line), method or None,
                     expected or None, pend.group("q") if pend else None)


def parse(path: Path) -> Task:
    raw_lines = path.read_text(encoding="utf-8").splitlines()
    tid = title = None
    if raw_lines and raw_lines[0].startswith("# "):
        tid, _, title = raw_lines[0][2:].partition(" — ")
        tid, title = tid.strip() or None, title.strip() or None
    meta: dict[str, str] = {}
    sections: dict[int, Lines] = {}
    revisions: list[Revision] = []
    current: int | None = None
    rev: Revision | None = None
    rev_stage: int | None = None
    for n, line in unfenced(raw_lines):
        if m := REVISION_RE.match(line):
            rev = Revision(m.group("rev"), n, {})
            revisions.append(rev)
            current = rev_stage = None
            continue
        if rev is None and (m := SECTION_RE.match(line)):
            current = int(m.group("num"))
            sections.setdefault(current, [])
            continue
        if rev is not None:
            if m := REV_STAGE_RE.match(line):
                rev_stage = int(m.group("num"))
                rev.stages.setdefault(rev_stage, [])
            elif rev_stage is not None:
                rev.stages[rev_stage].append((n, line))
            continue
        if current is None:
            if not sections and (mm := META_RE.match(line)):
                meta[mm.group("key").strip()] = mm.group("value").strip()
            continue
        sections[current].append((n, line))

    divisions: dict[int, Lines] = {}
    cur_div: int | None = None
    for n, line in sections.get(1, []):
        if m := DIVISION_RE.match(line):
            cur_div = int(m.group("num"))
            divisions.setdefault(cur_div, [])
        elif cur_div is not None:
            divisions[cur_div].append((n, line))

    task = Task(path, tid, title, meta, sections, revisions, divisions)
    # Camadas: o texto original e, em ordem, o `### 1.`/`### 3.` de cada revisão.
    # Por ID vale a camada mais recente; ID repetido na mesma camada é problema.
    crit_layers = [divisions.get(4, [])] + [r.stages.get(1, []) for r in revisions]
    by_id: dict[str, Criterion] = {}
    for layer in crit_layers:
        seen: set[str] = set()
        for n, line in layer:
            if c := parse_criterion(line, n):
                if c.id in seen:
                    task.issues.append({"kind": "duplicate-criterion", "id": c.id, "line": str(n)})
                    continue
                seen.add(c.id)
                by_id[c.id] = c
    task.criteria = list(by_id.values())
    for layer in [sections.get(3, [])] + [r.stages.get(3, []) for r in revisions]:
        layer_map: dict[str, list[str]] = {}
        for _, line in layer:
            if m := REQ_RE.match(line):
                task.reqs[m.group("id")] = m.group("text")
            elif m := AC_REQ_RE.match(line):
                layer_map.setdefault(m.group("ac"), []).append(m.group("req"))
        task.ac_req |= layer_map
    return task


def recorded_inputs(task: Task) -> tuple[dict[str, dict[str, str]], list[dict[str, str]]]:
    """Inputs de todas as camadas vigentes e os IDs repetidos (o primeiro vale)."""
    out: dict[str, dict[str, str]] = {}
    issues: list[dict[str, str]] = []
    for layer, lines in task.evidence_layers():
        for t in parse_tables(lines):
            if not t.header or t.header[0] != "Input":
                continue
            for row, n in zip(t.rows, t.row_linenos, strict=True):
                iid = strip_code(row.get("Input", ""))
                if iid in out:
                    issues.append({"kind": "duplicate-input", "id": iid, "line": str(n)})
                    continue
                out[iid] = {"source": row.get("Caminho ou saída", ""), "role": row.get("Papel", "").strip(),
                            "sha256": strip_code(row.get("SHA-256", "")), "layer": layer, "line": str(n),
                            "column": str(t.header.index("SHA-256")) if "SHA-256" in t.header else ""}
    return out, issues


def effective_observations(task: Task) -> tuple[dict[str, dict[str, str]], list[dict[str, str]]]:
    """Observação vigente por AC (a da camada mais recente) e ACs repetidos na mesma camada."""
    out: dict[str, dict[str, str]] = {}
    issues: list[dict[str, str]] = []
    for layer, lines in task.evidence_layers():
        in_layer: set[str] = set()
        for t in parse_tables(lines):
            if not t.header or t.header[0] != "AC":
                continue
            for row, n in zip(t.rows, t.row_linenos, strict=True):
                ac = strip_code(row.get("AC", ""))
                if not AC_ID_RE.match(ac):
                    continue  # linhas de faixa (AC-08 a AC-11, unidos por travessão) não decidem critério
                if ac in in_layer:
                    issues.append({"kind": "duplicate-observation", "id": ac, "line": str(n)})
                    continue
                in_layer.add(ac)
                out[ac] = dict(row) | {"_layer": layer, "_line": str(n)}
    return out, issues


def single_path(cell: str, task_dir: Path, root: Path) -> Path | None:
    """Arquivo citado pela célula: `caminho` (relativo à raiz) ou [texto](link)
    (relativo ao registro da task). Outras formas não são verificáveis por bytes."""
    m = re.fullmatch(r"\s*`([^`\s]+)`\s*", cell)
    if m:
        return root / m.group(1)
    m = re.match(r"\s*\[[^\]]+\]\(([^)#\s]+)", cell)
    return task_dir / m.group(1) if m else None


def contained(target: Path, root: Path) -> bool:
    """O input precisa estar dentro do repositório (caminho absoluto ou `..` não vale)."""
    try:
        return target.resolve().is_relative_to(root.resolve())
    except (OSError, RuntimeError):
        return False


def freshness(task: Task, root: Path) -> list[dict[str, str]]:
    """Compara a evidência vigente com os bytes atuais.

    Uma linha por verificação: kind (criterion|input|reference), id, recorded,
    current, status. Status: fresh, stale, malformed, unverifiable, missing,
    unknown-criterion, no-inputs, unreferenced (input que nenhuma observação
    vigente cita; não é verificado nem conta como problema).
    """
    results: list[dict[str, str]] = []
    by_id = {c.id: c for c in task.criteria}
    inputs, input_issues = recorded_inputs(task)
    observations, obs_issues = effective_observations(task)
    for ac, row in observations.items():
        state = row.get("Estado", "").split("(")[0].strip()
        rec = next((strip_code(row[h]) for h in CRITERION_HEADERS if h in row), "")
        if ac not in by_id:
            results.append({"kind": "criterion", "id": ac, "recorded": rec, "current": "", "status": "unknown-criterion",
                            "state": state, "layer": row["_layer"]})
            continue
        cur = by_id[ac].sha256
        status = "malformed" if not SHA_RE.match(rec) else ("fresh" if rec == cur else "stale")
        results.append({"kind": "criterion", "id": ac, "recorded": rec, "current": cur, "status": status,
                        "state": state, "layer": row["_layer"]})
        refs = INPUT_ID_RE.findall(row.get("Inputs", ""))
        if state in DECIDED and not refs:
            results.append({"kind": "reference", "id": ac, "recorded": row.get("Inputs", ""), "current": "",
                            "status": "no-inputs", "state": state, "layer": row["_layer"]})
        for ref in refs:
            if ref not in inputs:
                results.append({"kind": "reference", "id": f"{ac}→{ref}", "recorded": "", "current": "",
                                "status": "missing", "state": state, "layer": row["_layer"]})
    referenced = {ref for row in observations.values() for ref in INPUT_ID_RE.findall(row.get("Inputs", ""))}
    for iid, inp in inputs.items():
        rec = inp["sha256"]
        if iid not in referenced:
            # Só a observação vigente sustenta estado; input sem referência vigente é histórico.
            results.append({"kind": "input", "id": iid, "recorded": rec, "current": "", "status": "unreferenced",
                            "layer": inp["layer"]})
            continue
        target = single_path(inp["source"], task.path.parent, root)
        if target is None:
            # Saída derivada: o hash é o da saída do comando registrado; precisa ser SHA-256 completo.
            status = "unverifiable" if SHA_RE.match(rec) else "malformed"
            results.append({"kind": "input", "id": iid, "recorded": rec, "current": "", "status": status,
                            "layer": inp["layer"]})
            continue
        if not contained(target, root):
            results.append({"kind": "input", "id": iid, "recorded": rec, "current": "", "status": "escaping",
                            "layer": inp["layer"]})
            continue
        if not target.is_file() or target.is_symlink():
            results.append({"kind": "input", "id": iid, "recorded": rec, "current": "", "status": "missing",
                            "layer": inp["layer"]})
            continue
        cur = sha256_bytes(target.read_bytes())
        status = "malformed" if not SHA_RE.match(rec) else ("fresh" if rec == cur else "stale")
        results.append({"kind": "input", "id": iid, "recorded": rec, "current": cur, "status": status,
                        "layer": inp["layer"]})
    for issue in task.issues + input_issues + obs_issues:
        results.append({"kind": issue["kind"], "id": issue["id"], "recorded": "", "current": "",
                        "status": "duplicate", "layer": "", "line": issue["line"]})
    return results


PROBLEM_STATUSES = {"stale", "malformed", "missing", "unknown-criterion", "no-inputs", "duplicate", "escaping"}
TASK_ID_RE = re.compile(r"^[A-Z0-9]+(?:-[A-Z0-9]+)*-\d{8}(?:-\d+)?$")


def find_tasks(root: Path) -> list[Path]:
    base = root / "sdd" / "tasks"
    if not base.is_dir():
        return []
    return sorted(p for p in base.glob("*.md")
                  if p.is_file() and not p.is_symlink() and not p.name.endswith(".review.md")
                  and p.name != "README.md")


PLACEHOLDER_RE = re.compile(r"^(?:|—|-|<[^<>]*>)$")


def _replace_cell(lines: list[str], lineno: int, column: int, value: str) -> bool:
    """Preenche a célula `column` da linha `lineno` (1-based) só se ela está vazia ou é um
    marcador de template (`<…>`, `—`).

    Qualquer outro conteúdo, inclusive um hash registrado em qualquer forma, nunca é
    sobrescrito: hash que diverge dos bytes atuais indica observação desatualizada, que precisa
    ser refeita (sdd/workflow.md, Evidência e retomada), não renovada. Linha com crase
    desbalanceada não é reescrita.
    """
    raw = lines[lineno - 1]
    body = raw.rstrip("\r\n")
    cells = split_row(body)
    if body.count("`") % 2 or column >= len(cells) or not PLACEHOLDER_RE.match(strip_code(cells[column])):
        return False
    cells[column] = value
    lines[lineno - 1] = "| " + " | ".join(cells) + " |" + raw[len(body):]
    return True


def write_hashes(task: Task, root: Path) -> int:
    """Preenche os sha256 ainda ausentes da evidência vigente; devolve o número de células preenchidas.

    Critério: sha256 da linha do AC. Input: sha256 dos bytes do arquivo citado, só para inputs
    referenciados por observação vigente, com caminho verificável dentro do repositório.
    Observações obsoletas, inputs não referenciados e hashes já registrados não são tocados.
    """
    lines = task.path.read_text(encoding="utf-8").splitlines(keepends=True)
    by_id = {c.id: c for c in task.criteria}
    observations, _ = effective_observations(task)
    inputs, _ = recorded_inputs(task)
    headers = {n: t.header for _, layer in task.evidence_layers()
               for t in parse_tables(layer) for n in t.row_linenos}
    changed = 0
    for ac, row in observations.items():
        header = headers.get(int(row["_line"]), [])
        column = next((header.index(h) for h in CRITERION_HEADERS if h in header), None)
        if ac in by_id and column is not None:
            changed += _replace_cell(lines, int(row["_line"]), column, f"`{by_id[ac].sha256}`")
    referenced = {ref for row in observations.values() for ref in INPUT_ID_RE.findall(row.get("Inputs", ""))}
    for iid, inp in inputs.items():
        if iid not in referenced or not inp["column"]:
            continue
        target = single_path(inp["source"], task.path.parent, root)
        if target is None or not contained(target, root) or not target.is_file() or target.is_symlink():
            continue
        if target.resolve() == task.path.resolve():
            continue  # o próprio registro não é input (sdd/workflow.md, etapa 8)
        digest = sha256_bytes(target.read_bytes())
        changed += _replace_cell(lines, int(inp["line"]), int(inp["column"]), f"`{digest}`")
    if changed:
        task.path.write_text("".join(lines), encoding="utf-8")
    return changed


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="command", required=True)
    ev = sub.add_parser("evidence", help="estado e gravação dos hashes da seção 8")
    ev.add_argument("--root", default=".", type=Path)
    ev.add_argument("--task", required=True, help="ID da task")
    mode = ev.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true", help="preenche os hashes ainda ausentes")
    mode.add_argument("--check", action="store_true", help="mostra só problemas; exit 1 se houver")
    ev.add_argument("--require-all", action="store_true",
                    help="exige observação vigente com critério atual para cada AC da seção 1")
    args = ap.parse_args(argv)
    root = args.root.resolve()
    if not TASK_ID_RE.fullmatch(args.task):
        print(f"ID de task inválido: {args.task}", file=sys.stderr)
        return 2
    path = root / "sdd" / "tasks" / f"{args.task}.md"
    if not path.is_file() or path.is_symlink():
        print(f"task inexistente: sdd/tasks/{args.task}.md", file=sys.stderr)
        return 2
    try:
        if args.write:
            print(f"{write_hashes(parse(path), root)} célula(s) SHA-256 preenchida(s).")
        task = parse(path)
        rows = freshness(task, root)
    except (OSError, UnicodeDecodeError) as exc:
        print(f"erro de leitura: {exc}", file=sys.stderr)
        return 2
    problems = [r for r in rows if r["status"] in PROBLEM_STATUSES]
    if args.require_all:
        fresh = {r["id"] for r in rows if r["kind"] == "criterion" and r["status"] == "fresh"}
        problems += [{"kind": "criterion", "id": c.id, "recorded": "", "current": c.sha256, "status": "unobserved"}
                     for c in task.criteria if c.id not in fresh]
    for r in (problems if args.check else rows):
        print(f"{r['status']:<18} {r['kind']:<10} {r['id']:<12} registrado={r['recorded'][:12] or '—'} "
              f"atual={r['current'][:12] or '—'}")
    print(f"{len(problems)} problema(s) em {len(rows)} verificação(ões).")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
