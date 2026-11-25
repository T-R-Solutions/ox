#!/usr/bin/env bash
# AC-01 a AC-03 de AUDIT-AUTORIDADE-20261124: a referência da skill de auditoria troca a ordem de
# autoridade própria por um link para a seção da constituição, sem outra mudança. Rode da raiz do Ox.
# O AC-03 compara com o commit-base fixo (antes da correção), não com HEAD, para continuar
# reproduzível depois do commit. O argumento opcional troca a base (usado por mutations.sh).
set -euo pipefail
base=${1:-10d9570ba57d98597491b2372e3e310dd46a7851}
ref=.claude/skills/codex-task-audit/references/ox-governance.md
git rev-parse --quiet --verify "$base^{commit}" >/dev/null || { echo "commit-base ausente: $base"; exit 2; }
diff_out=$(git diff -U0 "$base" -- "$ref")
python3 -I - "$ref" "$diff_out" <<'PY'
import re
import sys
from pathlib import Path

ref, diff = Path(sys.argv[1]), sys.argv[2]
lines = ref.read_text(encoding="utf-8").splitlines()
link = "../../../../sdd/constitution.md#governança-do-processo"
expected = f"Consulte a seção [Governança do processo]({link}) da constituição do Ox."
old = [
    "As regras estão no SDD; esta lista só diz **onde olhar**. Em divergência, vale o SDD:",
    "`sdd/constitution.md` > `AGENTS.md` > `sdd/workflow.md` (etapas, skills e agentes) > skills.",
]

# AC-01: a abertura é só a linha pedida; nenhuma ordem de autoridade em arquivo da skill.
skill_md = sorted(Path(".claude/skills/codex-task-audit").rglob("*.md"))
chain = re.compile(r"`[^`]+`\s*>\s*`[^`]+`")
chains = [f"{p}:{n}" for p in skill_md
          for n, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1)
          if chain.search(line) or "Em divergência" in line]

# AC-02: o link resolve para arquivo e título existentes, e a seção é a da cadeia de autoridade.
target, fragment = link.split("#")
path = (ref.parent / target).resolve()
text = path.read_text(encoding="utf-8") if path.is_file() else ""


def slug(heading):
    return re.sub(r"[^\w\- ]", "", heading.strip().lower()).replace(" ", "-")


headings = {slug(h): h for h in re.findall(r"^#{1,6} (.+)$", text, re.M)}
section = re.search(r"^## Governança do processo\n(.*?)(?=^## |\Z)", text, re.M | re.S)

# AC-03: o diff contra o commit-base remove só as duas linhas antigas e adiciona só a nova.
removed = [l[1:] for l in diff.splitlines() if l.startswith("-") and not l.startswith("---")]
added = [l[1:] for l in diff.splitlines() if l.startswith("+") and not l.startswith("+++")]

checks = {
    "AC-01 linhas 1-5 da referência": lines[:5] == ["# O que conferir no Ox", "", expected, "",
                                                    "## Por seção do registro da task (`sdd/tasks/<ID>.md`)"],
    "AC-01 sem ordem de autoridade na skill": not chains,
    "AC-02 alvo é sdd/constitution.md": path == Path("sdd/constitution.md").resolve(),
    "AC-02 âncora existe": fragment in headings,
    "AC-02 seção traz a cadeia de autoridade": bool(section and "**Cadeia de autoridade:**" in section.group(1)),
    "AC-03 removidas só as duas linhas antigas": removed == old,
    "AC-03 adicionada só a linha nova": added == [expected],
}
for name, ok in checks.items():
    print(f"{'ok' if ok else 'FALHA'}  {name}")
for where in chains:
    print(f"       ordem de autoridade em {where}")
failures = sum(not ok for ok in checks.values())
print(f"{failures} falha(s)")
sys.exit(1 if failures else 0)
PY
