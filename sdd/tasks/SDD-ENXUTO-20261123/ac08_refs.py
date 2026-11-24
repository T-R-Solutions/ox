#!/usr/bin/env python3
"""AC-08 (r3) de SDD-ENXUTO-20261123: arquivos ativos não referenciam o legado (exit 0 = nenhuma).

Substitui ac08_legacy_grep.sh, cujo padrão omitia caminhos removidos (revisão externa,
achado 1). Ativo = listado por `git ls-files -co --exclude-standard` e existente no disco
(o índice ainda lista arquivos apagados). Base: o commit ea3cf0f, último com o legado, fixado
em ac08_refs.sh para a cobertura não depender do HEAD (revisão externa 2). Três buscas:

1. termos do legado (o padrão do script anterior; "procedimento canônico" só em `.codex/`,
   como antes: em `scripts/README.md` o termo descreve o shared-toolbox);
2. todo token com `/` (texto, código inline, link, com ou sem `/` inicial ou prefixo `x:`) que,
   relativo à raiz ou ao arquivo, aponta para caminho da base ou de removed-paths.txt ausente;
3. nome de arquivo sem diretório que existia em exatamente um caminho da base, removido, e em
   nenhum arquivo ativo. Nomes que existiam em vários caminhos (`plan.md`, `result.txt`…) são
   genéricos demais para busca automática; a revisão manual deles está na seção 7 da r2.

Não contam (motivo em cada entrada de EXCLUDE e ALLOWED):
- referência a histórico Git `<commit>:<caminho>`: `git show` recupera os bytes;
- URL: aponta para fora do repositório; caminho com barra invertida: o repositório não usa;
- linhas `"reason"` de `scripts/config/automation.json`: registro cumulativo de revisões.

Sem subprocess: as listas do Git chegam por arquivo, separadas por NUL. Uso, da raiz do Ox:
bash sdd/tasks/SDD-ENXUTO-20261123/ac08_refs.sh
"""
from __future__ import annotations

import posixpath
import re
import sys
from pathlib import Path

ROOT = Path.cwd()
HERE = "sdd/tasks/SDD-ENXUTO-20261123"
# Arquivo inteiro fora da busca → motivo.
EXCLUDE = {
    "sdd/tasks/SDD-ENXUTO-20261123.md": "registro desta task: lista o legado de propósito",
    "sdd/tasks/SDD-ENXUTO-20261123.review.md": "revisão externa citada literalmente",
    "docs/decisions/sdd-model.md": "ADR que registra a remoção do legado e seus motivos",
    "scripts/config/native/gitleaks/gitleaks-history.ignore":
        "o scan do histórico Git ainda vê os caminhos antigos (histórico não foi reescrito)",
    "scripts/tests/test_governance_diagnostics.py": "corpus sintético de diagnóstico de links",
    "scripts/tests/fixtures/governance-links.txt": "corpus sintético de diagnóstico de links",
    "application/vendor/cryoglyph-0.1.0/OX-PATCH.md":
        "vendor: a seção 1.3 proíbe alterar; a linha 37 cita docs/validation (pendência da r2)",
    "docs/licensing/copy-provenance.json": "ledger de proveniência: origem histórica de cada cópia",
    "docs/licensing/license-inventory.json": "ledger de proveniência: origem histórica de cada licença",
}
EXCLUDE_DIR = (f"{HERE}/", "registro e artefatos desta task")
# (arquivo, regex da linha) aceitos depois de revisão → motivo.
ALLOWED = [
    ("scripts/config/automation.json", re.compile(r'^\s*"reason":'), "registro cumulativo de revisões"),
    (".codex/skills/readme-lifecycle-engineering/references/sources-and-decisions.md", re.compile(r"^\| E0\d \|"),
     "tabela de fontes: caminhos dentro de arquivos zip externos (ec_skills.zip, ox_resume.zip)"),
    ("scripts/tests/rules/README.md", re.compile(r"ox\.py/ox\.rs"), "nome de cópia descartável, não o arquivo removido"),
    ("docs/assets/render.mjs", re.compile(r"'package\.json'"), "package.json do toolRoot externo"),
    ("scripts/README.md", re.compile(r"`progress-observed\.json`"), "nome de saída gerada pelos scripts"),
    ("scripts/tests/test_defaults.py", re.compile(r"'redaction\.json'"), "saída gerada pelo teste"),
    ("scripts/tests/test_automation.py", re.compile(r"fixture\.rs"), "fonte gerada pelo próprio teste"),
]
TERMS = re.compile(
    r"sdd/history|docs/validation|\.ai/|task_finalizada|profile\.json|normative-coverage|history-manifest"
    r"|codex-agents\.md|ec_triador|ec_validador|ec_revisor|ec_testador|ec_analista|sdd/skills\.md"
    r"|sdd/agents\.md"
)
CODEX_TERM = re.compile(r"procedimento canônico")
PATH_TOKEN = re.compile(r"(?<![\w.@/-])/?(?:\.{1,2}/)*[\w.-]+(?:/[\w.-]+)+/?")
NAME_TOKEN = re.compile(
    r"(?<![\w./-])[\w-]+(?:\.[\w-]+)*\.(?:py|sh|md|json|toml|mmd|svg|txt|ya?ml|rs|js|mjs|png)\b")
GIT_REF = re.compile(r"[0-9a-f]{7,40}:$")
GIT_REF_TOKEN = re.compile(r"\b[0-9a-f]{7,40}:[^\s`)\]]+")
URL_BEFORE = re.compile(r"[a-z][\w+.-]*://\S*$")


def read_list(path: str) -> list[str]:
    """Lista separada por NUL (`git ... -z`), sem aspas em nomes não ASCII."""
    return [p for p in Path(path).read_text(encoding="utf-8").split("\0") if p]


def dead_paths(base: list[str]) -> tuple[set[str], set[str]]:
    """Caminhos da base e de removed-paths.txt ausentes (com diretórios) e nomes únicos na base."""
    files = {p for p in base if not (ROOT / p).exists()}
    removed = (ROOT / HERE / "removed-paths.txt").read_text(encoding="utf-8").split()
    files |= {p.rstrip("/") for p in removed if not (ROOT / p).exists()}
    dead = set(files)
    for p in files:
        parent = posixpath.dirname(p)
        while parent and not (ROOT / parent).exists():
            dead.add(parent)
            parent = posixpath.dirname(parent)
    count: dict[str, int] = {}
    for p in base:
        name = posixpath.basename(p)
        count[name] = count.get(name, 0) + 1
    unique = {posixpath.basename(p) for p in files if count.get(posixpath.basename(p), 0) <= 1}
    return dead, unique


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("uso: ac08_refs.py <lista da base> <lista de ativos>", file=sys.stderr)
        return 2
    base = read_list(argv[0])
    if not base:
        print("falha: lista da base vazia; a busca de caminhos removidos ficaria sem cobertura", file=sys.stderr)
        return 2
    dead, dead_names = dead_paths(base)
    active = sorted({p for p in read_list(argv[1]) if (ROOT / p).is_file() and not (ROOT / p).is_symlink()})
    names = dead_names - {posixpath.basename(p) for p in active}
    hits: list[str] = []
    for rel in active:
        if rel in EXCLUDE or rel.startswith(EXCLUDE_DIR[0]):
            continue
        try:
            text: str | None = (ROOT / rel).read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = None  # binário: fora da busca (sem continue no except, regra B112 do Bandit)
        if text is None:
            continue
        base = posixpath.dirname(rel)
        for n, line in enumerate(text.splitlines(), 1):
            if any(rel == f and rx.search(line) for f, rx, _ in ALLOWED):
                continue
            if rel.startswith(".codex/") and CODEX_TERM.search(line):
                hits.append(f"{rel}:{n}: termo procedimento canônico")
            for m in TERMS.finditer(GIT_REF_TOKEN.sub("", line)):
                hits.append(f"{rel}:{n}: termo {m.group(0)}")
            for m in PATH_TOKEN.finditer(line):
                before = line[: m.start()]
                if GIT_REF.search(before) or URL_BEFORE.search(before):
                    continue
                token = m.group(0).rstrip("/.")
                plain = token.lstrip("/").removeprefix("./")
                cands = {posixpath.normpath(plain), posixpath.normpath(posixpath.join(base, token))}
                if any((ROOT / c).exists() for c in cands):
                    continue
                if cands & dead:
                    hits.append(f"{rel}:{n}: caminho removido {token}")
            for m in NAME_TOKEN.finditer(line):
                if m.group(0) in names and not GIT_REF.search(line[: m.start()]):
                    hits.append(f"{rel}:{n}: arquivo removido {m.group(0)}")
    for h in dict.fromkeys(hits):
        print(h)
    print(f"ocorrencias={len(dict.fromkeys(hits))} ativos={len(active)} removidos={len(dead)}")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
